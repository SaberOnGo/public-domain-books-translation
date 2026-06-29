from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ALIGNMENT_MAP = "qa/bilingual_parallel/alignment_map.json"
DEFAULT_BILINGUAL_EPUB = "output/book_bilingual_parallel.epub"
WORK_DIR_NAME = "epub_work_bilingual"


@dataclass
class Paragraph:
    text: str
    aliases: list[str]
    file: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the bilingual parallel EPUB edition.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read_text(path))


def parse_yaml(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data: dict[str, str] = {}
    for line in read_text(path).split("\n"):
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            data[match.group(1)] = match.group(2).strip().strip("'\"")
    return data


def slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", value).strip("_") or "doc"


def normalize_lang(value: str, fallback: str) -> str:
    value = (value or fallback).strip()
    if value == "zh-CN":
        return "zh-Hans"
    if value == "zh-TW":
        return "zh-Hant"
    return value or fallback


def bilingual_enabled(state: dict) -> bool:
    if state.get("edition_type") == "bilingual_parallel":
        return True
    bilingual = state.get("bilingual_parallel")
    if isinstance(bilingual, dict) and bilingual.get("enabled") is True:
        return True
    for item in state.get("output_editions") or []:
        if isinstance(item, dict) and item.get("enabled") is True and item.get("edition_type") == "bilingual_parallel":
            return True
    return False


def bilingual_artifact(state: dict) -> str:
    for item in state.get("output_editions") or []:
        if isinstance(item, dict) and item.get("enabled") is True and item.get("edition_type") == "bilingual_parallel":
            return str(item.get("artifact") or DEFAULT_BILINGUAL_EPUB)
    return DEFAULT_BILINGUAL_EPUB


def alignment_map_path(book_root: Path, state: dict) -> Path:
    bilingual = state.get("bilingual_parallel") if isinstance(state.get("bilingual_parallel"), dict) else {}
    return book_root / str(bilingual.get("alignment_map") or DEFAULT_ALIGNMENT_MAP)


def first_heading(path: Path) -> str:
    if not path.exists():
        return path.stem
    match = re.search(r"^#\s+(.+?)\s*$", read_text(path), flags=re.MULTILINE)
    return match.group(1).strip() if match else path.stem


def frontmatter_rank(path: Path) -> tuple[int, str]:
    ranks = {
        "cover": 0,
        "book_info": 1,
        "book-info": 1,
        "translator_note": 2,
        "translator-note": 2,
        "edition_note": 2,
        "edition-note": 2,
        "preface": 3,
    }
    stem = path.stem.lower()
    return ranks.get(stem, 10), path.name


ID_COMMENT = re.compile(r"<!--\s*(?:id|paragraph-id|para-id)\s*:\s*([A-Za-z0-9_.:-]+)\s*-->\s*")
ID_PREFIX = re.compile(r"^\s*\[id:([A-Za-z0-9_.:-]+)\]\s*")
ID_BRACE = re.compile(r"\s*\{#([A-Za-z0-9_.:-]+)\}\s*$")


def strip_paragraph_id(block: str) -> tuple[str | None, str]:
    explicit_id: str | None = None

    def take_comment(match: re.Match[str]) -> str:
        nonlocal explicit_id
        explicit_id = explicit_id or match.group(1)
        return ""

    block = ID_COMMENT.sub(take_comment, block).strip()
    prefix = ID_PREFIX.match(block)
    if prefix:
        explicit_id = explicit_id or prefix.group(1)
        block = block[prefix.end() :].strip()
    brace = ID_BRACE.search(block)
    if brace:
        explicit_id = explicit_id or brace.group(1)
        block = block[: brace.start()].strip()
    return explicit_id, block


def iter_markdown_blocks(path: Path) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    for raw in read_text(path).split("\n"):
        line = raw.rstrip()
        if not line.strip():
            if current:
                blocks.append("\n".join(current).strip())
                current = []
            continue
        current.append(line)
    if current:
        blocks.append("\n".join(current).strip())
    return blocks


def is_reader_paragraph(block: str) -> bool:
    stripped = block.strip()
    if not stripped:
        return False
    if stripped.startswith("#"):
        return False
    if re.match(r"^[-*_]{3,}$", stripped):
        return False
    return True


def collect_paragraphs(root: Path, prefix: str) -> dict[str, Paragraph]:
    files = sorted(root.glob("*.md")) if root.exists() else []
    paragraph_map: dict[str, Paragraph] = {}
    global_index = 0
    for file in files:
        local_index = 0
        for block in iter_markdown_blocks(file):
            if not is_reader_paragraph(block):
                continue
            explicit_id, text = strip_paragraph_id(block)
            if not text:
                continue
            global_index += 1
            local_index += 1
            generated_global = f"{prefix}{global_index:04d}"
            generated_local = f"{file.stem}:p{local_index:04d}"
            aliases = [
                generated_global,
                generated_local,
                f"{prefix}:{file.stem}:p{local_index:04d}",
            ]
            if explicit_id:
                aliases.insert(0, explicit_id)
            aliases = list(dict.fromkeys(aliases))
            paragraph = Paragraph(text=text, aliases=aliases, file=file)
            for alias in aliases:
                if alias in paragraph_map:
                    raise SystemExit(f"Duplicate paragraph id in {root}: {alias}")
                paragraph_map[alias] = paragraph
    return paragraph_map


def inline_markdown(text: str) -> str:
    escaped = html.escape(" ".join(part.strip() for part in text.split("\n") if part.strip()), quote=True)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def markdown_body(path: Path) -> str:
    out: list[str] = []
    for block in iter_markdown_blocks(path):
        if not block:
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", block)
        if heading:
            level = min(len(heading.group(1)), 3)
            out.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            continue
        out.append(f"<p>{inline_markdown(block)}</p>")
    return "\n".join(out)


def resolve_texts(unit: dict, field: str, paragraph_map: dict[str, Paragraph], unit_id: str) -> list[str]:
    text_field = "source_text" if field == "source_paragraphs" else "target_text"
    direct_text = unit.get(text_field)
    if isinstance(direct_text, str) and direct_text.strip():
        return [direct_text.strip()]
    if isinstance(direct_text, list):
        values = [str(item).strip() for item in direct_text if str(item).strip()]
        if values:
            return values

    ids = unit.get(field)
    if not isinstance(ids, list) or not ids:
        raise SystemExit(f"{unit_id} must contain non-empty {field}.")
    resolved: list[str] = []
    for paragraph_id in ids:
        key = str(paragraph_id).strip()
        paragraph = paragraph_map.get(key)
        if paragraph is None:
            raise SystemExit(f"{unit_id} references missing {field} id: {key}")
        resolved.append(paragraph.text)
    return resolved


def load_alignment_units(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"Missing bilingual alignment map: {path}")
    data = read_json(path)
    if isinstance(data, list):
        units = data
    else:
        units = data.get("alignment_units")
    if not isinstance(units, list) or not units:
        raise SystemExit("Alignment map must contain a non-empty alignment_units list.")
    for index, unit in enumerate(units, start=1):
        if not isinstance(unit, dict):
            raise SystemExit(f"alignment_units[{index}] must be an object.")
    return units


def render_paragraphs(paragraphs: list[str]) -> str:
    return "\n".join(f"<p>{inline_markdown(text)}</p>" for text in paragraphs)


def group_units(units: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for unit in units:
        key = str(unit.get("chapter") or unit.get("target_file") or unit.get("source_file") or "body")
        grouped.setdefault(key, []).append(unit)
    return grouped


def xhtml_doc(title: str, body: str, language: str) -> str:
    escaped_title = html.escape(title, quote=True)
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{language}" lang="{language}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escaped_title}</title>
  <link rel="stylesheet" type="text/css" href="styles/book.css" />
</head>
<body>
{body}
</body>
</html>
"""


def write_css(work_dir: Path) -> None:
    write_text(
        work_dir / "EPUB" / "styles" / "book.css",
        (
            "body{line-height:1.72;margin:0;padding:1.2em;overflow-wrap:break-word}"
            "p{margin:0 0 .7em;text-indent:2em}"
            "h1{font-size:1.55em;line-height:1.25}h2{font-size:1.2em}h3{font-size:1.05em}"
            ".bitext-unit{margin:0 0 1.15em}"
            ".bitext-source{font-size:.92em;line-height:1.5;color:#555;margin:0 0 .35em;text-indent:0}"
            ".bitext-source p{text-indent:0;margin:0 0 .55em}"
            ".bitext-target{font-size:1em;line-height:1.72;color:inherit;margin:0}"
            ".bitext-target p{margin:0 0 .7em;text-indent:2em}"
        ),
    )


def write_container(work_dir: Path) -> None:
    write_text(work_dir / "mimetype", "application/epub+zip")
    write_text(
        work_dir / "META-INF" / "container.xml",
        """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml" />
  </rootfiles>
</container>
""",
    )


def zip_epub(work_dir: Path, epub_path: Path) -> None:
    epub_path.parent.mkdir(parents=True, exist_ok=True)
    if epub_path.exists():
        epub_path.unlink()
    with zipfile.ZipFile(epub_path, "w") as archive:
        archive.write(work_dir / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for path in sorted(work_dir.rglob("*")):
            if path.is_file() and path.name != "mimetype":
                archive.write(path, path.relative_to(work_dir).as_posix(), compress_type=zipfile.ZIP_DEFLATED)


def package_opf(
    title: str,
    metadata: dict[str, str],
    source_language: str,
    target_language: str,
    manifest_items: list[str],
    spine_items: list[str],
) -> str:
    creator = metadata.get("author") or metadata.get("creator") or "Unknown"
    contributor = metadata.get("contributor") or "LifeBook"
    publisher = metadata.get("publisher") or "LifeBook"
    source = metadata.get("source_url") or metadata.get("source") or metadata.get("source_text_url") or ""
    description = metadata.get("description") or metadata.get("subtitle") or ""
    rights = metadata.get("rights") or ""
    date = metadata.get("date") or ""
    identifier = metadata.get("identifier") or f"urn:uuid:{uuid4()}"
    languages = [target_language]
    if source_language and source_language not in languages:
        languages.append(source_language)
    dc_languages = "\n    ".join(f"<dc:language>{html.escape(item)}</dc:language>" for item in languages)
    modified = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""<?xml version="1.0" encoding="utf-8"?>
<package version="3.0" unique-identifier="bookid" xmlns="http://www.idpf.org/2007/opf">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/">
    <dc:identifier id="bookid">{html.escape(identifier)}</dc:identifier>
    <dc:title>{html.escape(title)}</dc:title>
    <dc:creator>{html.escape(creator)}</dc:creator>
    <dc:contributor>{html.escape(contributor)}</dc:contributor>
    <dc:publisher>{html.escape(publisher)}</dc:publisher>
    {dc_languages}
    {f"<dc:date>{html.escape(date)}</dc:date>" if date else ""}
    {f"<dc:source>{html.escape(source)}</dc:source>" if source else ""}
    {f"<dc:description>{html.escape(description)}</dc:description>" if description else ""}
    {f"<dc:rights>{html.escape(rights)}</dc:rights>" if rights else ""}
    <meta property="dcterms:modified">{modified}</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav" />
    <item id="css" href="styles/book.css" media-type="text/css" />
    {"".join(manifest_items)}
  </manifest>
  <spine>
    {"".join(spine_items)}
  </spine>
</package>
"""


def edition_title(title: str, target_language: str) -> str:
    if target_language.lower() in {"zh-hans", "zh-cn"}:
        return f"{title}（双语对照版）"
    if target_language.lower() in {"zh-hant", "zh-tw", "zh-hk"}:
        return f"{title}（雙語對照版）"
    return f"{title} - Bilingual Parallel Edition"


def main() -> None:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    state_path = book_root / "state" / "pipeline_state.json"
    if not state_path.exists():
        raise SystemExit("Missing state/pipeline_state.json")
    state = read_json(state_path)
    if not bilingual_enabled(state):
        print("bilingual EPUB build skipped: bilingual edition disabled")
        return

    source_language = normalize_lang(str(state.get("source_language") or ""), "en")
    metadata = parse_yaml(book_root / "metadata" / "book.yaml")
    target_language = normalize_lang(str(state.get("target_language") or metadata.get("language") or ""), "zh-Hans")
    alignment_units = load_alignment_units(alignment_map_path(book_root, state))
    source_paragraphs = collect_paragraphs(book_root / "chapters" / "src", "s")
    target_paragraphs = collect_paragraphs(book_root / "chapters" / "final", "t")

    grouped = group_units(alignment_units)
    title = metadata.get("title") or metadata.get("title_zh") or metadata.get("title_zh_hans") or "Untitled Book"
    title_for_package = edition_title(title, target_language)
    work_dir = book_root / "output" / WORK_DIR_NAME
    shutil.rmtree(work_dir, ignore_errors=True)
    (work_dir / "META-INF").mkdir(parents=True, exist_ok=True)
    (work_dir / "EPUB" / "styles").mkdir(parents=True, exist_ok=True)
    write_container(work_dir)
    write_css(work_dir)

    manifest_items: list[str] = []
    spine_items: list[str] = []
    nav_items: list[str] = []
    doc_index = 0

    for frontmatter in sorted((book_root / "frontmatter").glob("*.md"), key=frontmatter_rank):
        doc_index += 1
        href = f"{slug(frontmatter.stem)}.xhtml"
        title_text = first_heading(frontmatter)
        body = markdown_body(frontmatter)
        write_text(work_dir / "EPUB" / href, xhtml_doc(title_text, body, target_language))
        manifest_items.append(f'\n    <item id="doc{doc_index}" href="{href}" media-type="application/xhtml+xml" />')
        spine_items.append(f'\n    <itemref idref="doc{doc_index}" />')
        nav_items.append(f'<li><a href="{href}">{html.escape(title_text)}</a></li>')

    for group_key, group in grouped.items():
        doc_index += 1
        key_path = Path(group_key)
        href = f"bilingual_{slug(key_path.stem if key_path.suffix else group_key)}.xhtml"
        title_text = first_heading(book_root / group_key) if (book_root / group_key).exists() else key_path.stem or "正文"
        sections: list[str] = [f"<h1>{html.escape(title_text)}</h1>"]
        for index, unit in enumerate(group, start=1):
            unit_id = str(unit.get("id") or f"u{index:04d}")
            source_texts = resolve_texts(unit, "source_paragraphs", source_paragraphs, unit_id)
            target_texts = resolve_texts(unit, "target_paragraphs", target_paragraphs, unit_id)
            sections.append(
                f'<section class="bitext-unit" data-align-id="{html.escape(unit_id, quote=True)}">\n'
                f'<div class="bitext-source" xml:lang="{source_language}" lang="{source_language}">\n'
                f"{render_paragraphs(source_texts)}\n"
                "</div>\n"
                f'<div class="bitext-target" xml:lang="{target_language}" lang="{target_language}">\n'
                f"{render_paragraphs(target_texts)}\n"
                "</div>\n"
                "</section>"
            )
        write_text(work_dir / "EPUB" / href, xhtml_doc(title_text, "\n".join(sections), target_language))
        manifest_items.append(f'\n    <item id="doc{doc_index}" href="{href}" media-type="application/xhtml+xml" />')
        spine_items.append(f'\n    <itemref idref="doc{doc_index}" />')
        nav_items.append(f'<li><a href="{href}">{html.escape(title_text)}</a></li>')

    write_text(
        work_dir / "EPUB" / "nav.xhtml",
        xhtml_doc(
            "目录",
            f'<nav epub:type="toc" id="toc"><h1>目录</h1><ol>{"".join(nav_items)}</ol></nav>',
            target_language,
        ),
    )
    write_text(
        work_dir / "EPUB" / "package.opf",
        package_opf(title_for_package, metadata, source_language, target_language, manifest_items, spine_items),
    )

    epub_path = book_root / bilingual_artifact(state)
    zip_epub(work_dir, epub_path)
    print(f"wrote {epub_path.relative_to(book_root).as_posix()}")


if __name__ == "__main__":
    main()
