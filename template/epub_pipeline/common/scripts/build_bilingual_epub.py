from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import NAMESPACE_URL, uuid4, uuid5


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


def navigation_labels(metadata: dict[str, str], language: str) -> dict[str, str]:
    defaults = (
        {"toc": "目录", "landmarks": "导览", "cover": "封面", "book_info": "书籍信息"}
        if language.startswith("zh") else
        {"toc": "Contents", "landmarks": "Guide", "cover": "Cover", "book_info": "Book Information"}
    )
    fields = {"toc": "navigation_title", "landmarks": "navigation_landmarks_title",
              "cover": "navigation_cover_title", "book_info": "navigation_book_info_title"}
    return {key: metadata.get(fields[key]) or value for key, value in defaults.items()}


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


def load_reader_titles(book_root: Path) -> dict[str, str]:
    path = book_root / "references" / "reader_facing_titles.json"
    if not path.exists():
        return {}
    data = read_json(path)
    if not isinstance(data, dict):
        raise SystemExit(f"Reader-facing titles must be a JSON object: {path}")
    return {str(key).replace("\\", "/"): str(value).strip() for key, value in data.items() if str(value).strip()}


def reader_title(path: Path, book_root: Path, reader_titles: dict[str, str]) -> str:
    key = path.resolve().relative_to(book_root.resolve()).as_posix()
    override = reader_titles.get(key)
    if override:
        return override
    match = re.search(r"^#\s+(.+?)\s*$", read_text(path), flags=re.MULTILINE)
    if match and match.group(1).strip():
        return match.group(1).strip()
    raise SystemExit(f"Missing reader-facing Markdown title and override: {key}")


def has_markdown_heading(path: Path) -> bool:
    return bool(re.search(r"^#\s+(.+?)\s*$", read_text(path), flags=re.MULTILINE))


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
        # Keep CommonMark hard breaks (two trailing spaces or a trailing backslash) visible to join_lines().
        if raw.endswith("  ") or line.endswith("\\"):
            line = line.rstrip("\\") + LINE_BREAK
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


CJK_TEXT = "、-〿぀-ヿ㐀-䶿一-鿿豈-﫿！-／：-＠［-｀｛-･"
CJK_CHAR = re.compile(f"[{CJK_TEXT}]")
CJK_QUOTES = "“”‘’"
# Sentence-level storage sometimes rejoins CJK sentences with ASCII spaces; readers must not see them.
SPACE_AFTER_CJK_PUNCT = re.compile(f"(?<=[，。！？；：、）」』〉》】…”’])[  ]+(?=[{CJK_TEXT}“‘「『（《〈【])")
LINE_BREAK = " "
TRAILING_BR = re.compile(r"<br\s*/?>\s*$", re.IGNORECASE)
ESCAPED_BR = re.compile(r"&lt;br\s*/?&gt;", re.IGNORECASE)
ESCAPED_SAFE_INLINE = re.compile(r"&lt;(/?)(em|strong|i|b|sup|sub|small)&gt;", re.IGNORECASE)
ESCAPED_STRAY_BLOCK = re.compile(r"&lt;/?(?:blockquote|p|div|section)(?:\s[^&]*)?&gt;", re.IGNORECASE)
THEMATIC_BREAK = re.compile(r"^(?:[*\-_]\s*){3,}$")
QUOTE_LINE = re.compile(r"^>\s?")
LIST_LINE = re.compile(r"^(?:([-*+])|(\d{1,3})[.)])\s+(\S.*)$")
HEADING_LINE = re.compile(r"^(#{1,6})\s+(.+)$")
RAW_TAG_LINE = re.compile(r"^</?(?:blockquote|ol|ul|section|aside|div|figure|table)\b[^>]*>$", re.IGNORECASE)
RAW_BLOCK_START = re.compile(r"^</?(h[1-6]|section|p|aside|div|span|blockquote|ol|ul|li|dl|dt|dd|sup|sub|a|em|strong|br|table|figure)\b")
VERSE_LINE_MAX_CJK = 32
VERSE_LINE_MAX_LATIN = 48


def is_cjk_boundary(left: str, right: str) -> bool:
    left_cjk, right_cjk = bool(CJK_CHAR.match(left)), bool(CJK_CHAR.match(right))
    return (left_cjk or left in CJK_QUOTES) and (right_cjk or right in CJK_QUOTES) and (left_cjk or right_cjk)


SENTENCE_END = re.compile(r"[。！？!?…]+[”’」』）)]*$")


def looks_like_verse(lines: list[str]) -> bool:
    """Several short lines in one block are verse, a song, an address or a letter heading: keep the breaks.

    Two short lines that each end a sentence are more likely two prose sentences stored one per line.
    """
    if len(lines) < 2:
        return False
    limit = VERSE_LINE_MAX_CJK if any(CJK_CHAR.search(line) for line in lines) else VERSE_LINE_MAX_LATIN
    if not all(len(line) <= limit for line in lines):
        return False
    return len(lines) >= 3 or not SENTENCE_END.search(lines[0])


def join_lines(text: str) -> str:
    """Join a block's source lines: verse and hard breaks keep LINE_BREAK, CJK prose joins without spaces."""
    lines: list[tuple[str, bool]] = []
    for raw in text.split("\n"):
        hard = raw.endswith(LINE_BREAK) or bool(TRAILING_BR.search(raw.strip()))
        line = TRAILING_BR.sub("", raw.replace(LINE_BREAK, "").strip()).strip()
        if line:
            lines.append((line, hard))
    if not lines:
        return ""
    verse = looks_like_verse([line for line, _ in lines])
    out = lines[0][0]
    for (_, hard), (line, _) in zip(lines, lines[1:]):
        if verse or hard:
            out += LINE_BREAK + line
        elif is_cjk_boundary(out[-1], line[0]):
            out += line
        else:
            out += " " + line
    return out


def inline_markdown(text: str) -> str:
    joined = SPACE_AFTER_CJK_PUNCT.sub("", join_lines(text))
    escaped = html.escape(joined, quote=True)
    escaped = ESCAPED_BR.sub(LINE_BREAK, escaped)
    escaped = ESCAPED_STRAY_BLOCK.sub("", escaped)
    escaped = ESCAPED_SAFE_INLINE.sub(lambda m: f"<{m.group(1)}{m.group(2).lower()}>", escaped)
    escaped = re.sub(
        r"(^|[^\w])\[(\d+)\](?!\w)",
        r'\1<sup class="note-ref">[\2]</sup>',
        escaped,
        flags=re.ASCII,
    )
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    escaped = re.sub(r"(?<![_\w])_([^_]+)_(?![_\w])", r"<em>\1</em>", escaped)
    return escaped.replace(LINE_BREAK, "<br />")


def render_text_block(text: str) -> list[str]:
    """Render one Markdown block that starts with plain text.

    Lines that open a blockquote, a list, a heading or a raw block tag start their own element, so a
    paragraph followed by quoted verse no longer collapses into one paragraph full of '>' and '<br />'.
    """
    out: list[str] = []
    buffer: list[str] = []
    kind = ""

    def flush() -> None:
        nonlocal buffer, kind
        if buffer:
            if kind == "quote":
                paragraphs, current = [], []
                for line in buffer:
                    if line.strip():
                        current.append(line)
                    elif current:
                        paragraphs.append(current)
                        current = []
                if current:
                    paragraphs.append(current)
                inner = "".join(f"<p>{inline_markdown(chr(10).join(lines))}</p>" for lines in paragraphs)
                out.append(f"<blockquote>{inner}</blockquote>")
            elif kind in {"ul", "ol"}:
                items = "".join(f"<li>{inline_markdown(item)}</li>" for _, item in buffer)
                start = buffer[0][0]
                attrs = f' start="{start}"' if kind == "ol" and start not in ("", "1") else ""
                out.append(f"<{kind}{attrs}>{items}</{kind}>")
            else:
                out.append(f"<p>{inline_markdown(chr(10).join(buffer))}</p>")
        buffer, kind = [], ""

    for raw in text.split("\n"):
        line = raw.strip()
        if not line or THEMATIC_BREAK.match(line):
            flush()
            continue
        if RAW_TAG_LINE.match(line):
            flush()
            out.append(line)
            continue
        heading = HEADING_LINE.match(line)
        if heading:
            flush()
            level = min(len(heading.group(1)), 3)
            out.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            continue
        if QUOTE_LINE.match(line):
            if kind != "quote":
                flush()
                kind = "quote"
            buffer.append(QUOTE_LINE.sub("", line, count=1))
            continue
        listed = LIST_LINE.match(line)
        if listed and kind != "quote":
            item_kind = "ul" if listed.group(1) else "ol"
            if kind != item_kind:
                flush()
                kind = item_kind
            buffer.append((listed.group(2) or "", listed.group(3)))
            continue
        if kind in {"ul", "ol"} and buffer:
            number, item = buffer[-1]
            buffer[-1] = (number, f"{item}\n{line}")
            continue
        if kind not in {"", "para"}:
            flush()
        kind = "para"
        buffer.append(raw)
    flush()
    return out


class ImageAssets:
    """Package referenced local images once, preserving book-relative identity."""
    MEDIA_TYPES = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
                   '.gif': 'image/gif', '.svg': 'image/svg+xml', '.webp': 'image/webp'}

    def __init__(self, book_root: Path, work_dir: Path):
        self.root = book_root.resolve()
        self.work = work_dir
        self.entries: dict[Path, dict] = {}
        self.cover_source: Path | None = None

    def register(self, from_file: Path, reference: str, cover: bool = False) -> str:
        if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', reference) or reference.startswith(('/', '\\')):
            raise SystemExit(f'EPUB image reference must be relative: {reference}')
        source = (from_file.parent / reference).resolve()
        if not source.is_relative_to(self.root):
            raise SystemExit(f'EPUB image escapes book root: {reference}')
        if not source.is_file():
            raise SystemExit(f'Missing EPUB image: {reference}')
        media_type = self.MEDIA_TYPES.get(source.suffix.lower())
        if not media_type:
            raise SystemExit(f'Unsupported EPUB image type: {reference}')
        if source not in self.entries:
            relative = source.relative_to(self.root)
            # Preserve folders, so two images with the same filename cannot collide.
            href = relative.as_posix() if relative.parts[0] == 'assets' else f'assets/{relative.as_posix()}'
            target = self.work / 'EPUB' / href
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            self.entries[source] = {'href': href, 'media_type': media_type}
        if cover and self.cover_source is None:
            self.cover_source = source
        return self.entries[source]['href']

    def manifest_items(self) -> list[str]:
        items = []
        for index, (source, entry) in enumerate(self.entries.items(), start=1):
            properties = ' properties="cover-image"' if source == self.cover_source else ''
            items.append(f'\n    <item id="image{index}" href="{html.escape(entry["href"], quote=True)}" '
                         f'media-type="{entry["media_type"]}"{properties} />')
        return items


IMAGE_BLOCK = re.compile(r'^!\[([^\]\n]*)\]\(([^)\n]+)\)$')


def image_block(text: str, from_file: Path | None, assets: ImageAssets | None, cover: bool = False) -> str | None:
    match = IMAGE_BLOCK.fullmatch(text.strip())
    if not match:
        return None
    if assets is None or from_file is None:
        raise SystemExit('Image rendering requires a book-relative file and asset registry.')
    alt, reference = match.groups()
    if not alt.strip():
        raise SystemExit(f'EPUB image needs descriptive alt text: {reference}')
    href = assets.register(from_file, reference.strip(), cover=cover)
    image = f'<img src="{html.escape(href, quote=True)}" alt="{html.escape(alt, quote=True)}" />'
    # A cover page shows the cover image only: no visible caption or "封面/Cover" text.
    if cover:
        return f'<figure class="cover">{image}</figure>'
    return f'<figure>{image}<figcaption>{inline_markdown(alt)}</figcaption></figure>'


def is_cover_file(path: Path) -> bool:
    return path.stem.lower() == "cover"


PLACEHOLDER_MARKER = re.compile(r"<!--\s*lifebook:placeholder\b", re.IGNORECASE)
LEGACY_PLACEHOLDER = re.compile(r"本页为模板占位|译本前言模板|译者说明模板|模板占位|Translator Name", re.IGNORECASE)


def frontmatter_status(path: Path) -> str:
    """'skip' for marked or heading-only placeholders, 'fail' for unedited template text, else 'ok'."""
    text = read_text(path)
    if PLACEHOLDER_MARKER.search(text):
        return "skip"
    body = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    if LEGACY_PLACEHOLDER.search(body):
        return "fail"
    content = [line for line in body.split("\n") if line.strip() and not re.match(r"^\s*#{1,6}\s", line)]
    return "ok" if content else "skip"


def markdown_body(path: Path, assets: ImageAssets | None = None) -> str:
    out: list[str] = []
    cover = is_cover_file(path)
    for block in iter_markdown_blocks(path):
        if not block:
            continue
        image = image_block(block, path, assets, cover=cover)
        if image is not None:
            out.append(image)
            continue
        if cover:
            continue
        if RAW_BLOCK_START.match(block):
            out.append(block.strip())
            continue
        out.extend(render_text_block(block))
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_alignment_provenance(data: dict, book_root: Path, required: bool) -> None:
    provenance = data.get("provenance")
    if not isinstance(provenance, dict):
        if required:
            raise SystemExit("Alignment map lacks required input-file provenance hashes.")
        return
    groups = (
        ("source_file_sha256", provenance.get("source_file_sha256")),
        ("target_file_sha256", provenance.get("target_file_sha256")),
    )
    for name, entries in groups:
        if not isinstance(entries, dict) or not entries:
            raise SystemExit(f"Alignment provenance {name} must be a non-empty object.")
        for relative_path, expected in entries.items():
            input_path = book_root / str(relative_path)
            if not input_path.is_file():
                raise SystemExit(f"Alignment input is missing: {relative_path}")
            actual = sha256_file(input_path)
            if actual != expected:
                raise SystemExit(f"Alignment input changed; regenerate map: {relative_path}")
    note_path = book_root / "qa" / "notes" / "note_reflow_final.json"
    if sha256_file(note_path) != provenance.get("note_mapping_sha256"):
        raise SystemExit("Note reflow mapping changed; regenerate bilingual alignment map.")
    generator_path = book_root / "scripts" / "generate_bilingual_alignment.py"
    if sha256_file(generator_path) != provenance.get("generator_sha256"):
        raise SystemExit("Alignment generator changed; regenerate bilingual alignment map.")


def load_alignment_units(path: Path, book_root: Path, state: dict) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"Missing bilingual alignment map: {path}")
    data = read_json(path)
    bilingual = state.get("bilingual_parallel") if isinstance(state.get("bilingual_parallel"), dict) else {}
    require_provenance = bilingual.get("require_alignment_input_hashes") is True
    if isinstance(data, list):
        if require_provenance:
            raise SystemExit("Alignment map list format lacks required input-file provenance hashes.")
        units = data
    else:
        if data.get("schema_version") == "canonical-units-1.0":
            store = book_root / str(data.get("canonical_unit_store") or "")
            manifest_path = book_root / "output" / "translation_unit_manifest.json"
            if not store.is_file() or sha256_file(store) != data.get("canonical_unit_store_sha256"):
                raise SystemExit("Canonical unit store changed; rematerialize bilingual alignment map.")
            if not manifest_path.is_file():
                raise SystemExit("Canonical translation-unit manifest is missing.")
            manifest = read_json(manifest_path)
            if manifest.get("target_unit_manifest_sha256") != data.get("target_unit_manifest_sha256"):
                raise SystemExit("Canonical target manifest changed; rematerialize bilingual alignment map.")
        else:
            validate_alignment_provenance(data, book_root, require_provenance)
        units = data.get("alignment_units")
    if not isinstance(units, list) or not units:
        raise SystemExit("Alignment map must contain a non-empty alignment_units list.")
    for index, unit in enumerate(units, start=1):
        if not isinstance(unit, dict):
            raise SystemExit(f"alignment_units[{index}] must be an object.")
    return units


def render_paragraphs(paragraphs: list[str], unit_type: str = "body", heading_level: int = 0,
                      from_file: Path | None = None, assets: ImageAssets | None = None) -> str:
    if unit_type == "heading":
        if len(paragraphs) != 1:
            raise SystemExit("Canonical heading unit must contain exactly one source or target text block.")
        level = max(1, min(6, heading_level or 2))
        return f'<h{level} class="bitext-section-heading">{inline_markdown(paragraphs[0])}</h{level}>'
    rendered: list[str] = []
    for text in paragraphs:
        stripped = text.strip()
        image = image_block(stripped, from_file, assets)
        if image is not None:
            rendered.append(image)
            continue
        if RAW_BLOCK_START.match(stripped):
            rendered.append(stripped)
        else:
            rendered.extend(render_text_block(text))
    return "\n".join(rendered)


def group_units(units: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for unit in units:
        key = str(unit.get("chapter") or unit.get("target_file") or unit.get("source_file") or "body")
        grouped.setdefault(key, []).append(unit)
    return grouped


def first_heading_is_reader_title(units: list[dict], reader_title_text: str) -> bool:
    """Avoid emitting a second target-language chapter title in bilingual XHTML.

    The EPUB document title and navigation label remain target-language titles.
    When the first canonical unit already pairs that same title in both
    languages, the paired heading itself should be the body heading.
    """
    if not units or str(units[0].get("unit_type") or "") != "heading":
        return False
    target_text = units[0].get("target_text")
    if not isinstance(target_text, str) or not target_text.strip():
        return False
    # A canonical top-level heading already supplies the page's title system.
    # A deliberately shorter navigation label must not add another visible title.
    if int(units[0].get("markdown_heading_level") or 0) == 1:
        return True

    def normalize(value: str) -> str:
        value = re.sub(r"^#{1,6}\s+", "", value.strip())
        return " ".join(value.split()).casefold()

    return normalize(target_text) == normalize(reader_title_text)


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
            ".bitext-unit{margin:0 0 1em}"
            ".bitext-source{display:block!important;visibility:visible!important;font-size:.92em;line-height:1.55;margin:0 0 .24em;text-indent:0}"
            ".bitext-source p{text-indent:0;margin:0}"
            ".bitext-target{display:block!important;visibility:visible!important;font-size:1em;line-height:1.72;color:inherit;margin:0}"
            ".bitext-target p{margin:0;text-indent:2em}"
            ".bitext-section-heading{font-size:1.12em;line-height:1.35;margin:.25em 0 .6em;text-indent:0}"
            ".note-ref{font-size:.58em;line-height:0;vertical-align:super;white-space:nowrap}"
            ".chapter-notes{margin-top:2.2em;border-top:1px solid #999;padding-top:.8em}"
            ".chapter-notes>h2{font-size:1.15em;line-height:1.35;margin:0 0 .9em}"
            ".bitext-note-unit{margin:0 0 .8em}"
            ".chapter-notes .bitext-source{font-size:.86em;line-height:1.5;margin-bottom:.18em}"
            ".chapter-notes .bitext-target{font-size:.9em;line-height:1.55}"
            ".chapter-notes p.endnote{text-indent:0;margin:0}"
            ".note-gap{display:none!important}"
            ".endnote-label{font-size:.9em;font-weight:600;margin-right:.25em}"
            "img{max-width:100%;height:auto}figure{margin:1.2em 0;text-align:center;break-inside:avoid}"
            "figcaption{font-size:.88em;line-height:1.45;text-indent:0}"
            "figure.cover{margin:0}blockquote{margin:.6em 0 .9em 2em}blockquote p{text-indent:0}"
            "ul,ol{margin:.4em 0 .8em 2em;padding:0}li{margin:0 0 .3em}"
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


def edition_identifier(metadata: dict[str, str]) -> str:
    """The bilingual edition is a separate publication, so it must not reuse the target-only dc:identifier."""
    explicit = metadata.get("bilingual_identifier")
    if explicit:
        return explicit
    base = metadata.get("identifier") or ""
    if not base:
        return f"urn:uuid:{uuid4()}"
    if base.lower().startswith("urn:uuid:"):
        return f"urn:uuid:{uuid5(NAMESPACE_URL, base + '#bilingual_parallel')}"
    return f"{base}-bilingual-parallel"


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
    identifier = edition_identifier(metadata)
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
    labels = navigation_labels(metadata, target_language)
    reader_titles = load_reader_titles(book_root)
    alignment_units = load_alignment_units(alignment_map_path(book_root, state), book_root, state)
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
    images = ImageAssets(book_root, work_dir)

    manifest_items: list[str] = []
    spine_items: list[str] = []
    nav_items: list[str] = []
    translation_manifest = book_root / "output" / "translation_unit_manifest.json"
    if translation_manifest.is_file():
        shutil.copyfile(translation_manifest, work_dir / "EPUB" / "translation-unit-manifest.json")
        manifest_items.append('\n    <item id="translation-unit-manifest" href="translation-unit-manifest.json" media-type="application/json" />')
    doc_index = 0

    packaged_frontmatter: list[Path] = []
    for frontmatter in sorted((book_root / "frontmatter").glob("*.md"), key=frontmatter_rank):
        status = frontmatter_status(frontmatter)
        if status == "fail":
            raise SystemExit(
                f"frontmatter/{frontmatter.name} still contains template placeholder text; "
                "rewrite it for readers or delete the file. / 前置页仍是模板占位文字，请改写为读者内容或删除该文件。"
            )
        if status == "skip":
            print(f"skipped placeholder frontmatter: frontmatter/{frontmatter.name}")
            continue
        packaged_frontmatter.append(frontmatter)
        doc_index += 1
        href = f"{slug(frontmatter.stem)}.xhtml"
        title_text = reader_title(frontmatter, book_root, reader_titles)
        body = markdown_body(frontmatter, images)
        if not has_markdown_heading(frontmatter) and not is_cover_file(frontmatter):
            body = f"<h1>{html.escape(title_text)}</h1>\n{body}"
        write_text(work_dir / "EPUB" / href, xhtml_doc(title_text, body, target_language))
        manifest_items.append(f'\n    <item id="doc{doc_index}" href="{href}" media-type="application/xhtml+xml" />')
        spine_items.append(f'\n    <itemref idref="doc{doc_index}" />')
        nav_items.append(f'<li><a href="{href}">{html.escape(title_text)}</a></li>')

    for group_key, group in grouped.items():
        doc_index += 1
        key_path = Path(group_key)
        href = f"bilingual_{slug(key_path.stem if key_path.suffix else group_key)}.xhtml"
        title_text = reader_title(book_root / group_key, book_root, reader_titles)
        sections: list[str] = []
        if not first_heading_is_reader_title(group, title_text):
            sections.append(f'<h1 data-lifebook-editorial="reader-title">{html.escape(title_text)}</h1>')
        for index, unit in enumerate(group, start=1):
            unit_id = str(unit.get("id") or f"u{index:04d}")
            source_hash = str(unit.get("source_sha256") or "")
            target_hash = str(unit.get("target_sha256") or "")
            if not re.fullmatch(r"[0-9a-f]{64}", source_hash) or not re.fullmatch(r"[0-9a-f]{64}", target_hash):
                raise SystemExit(f"Canonical bilingual unit lacks source/target hashes: {unit_id}")
            source_texts = resolve_texts(unit, "source_paragraphs", source_paragraphs, unit_id)
            target_texts = resolve_texts(unit, "target_paragraphs", target_paragraphs, unit_id)
            unit_type = str(unit.get("unit_type") or "body")
            heading_level = int(unit.get("markdown_heading_level") or 0)
            source_file = book_root / str(unit.get("source_file") or group_key)
            target_file = book_root / str(unit.get("target_file") or group_key)
            note_class = " bitext-note-unit" if unit_type == "note" else ""
            sections.append(
                f'<section class="bitext-unit{note_class}" data-align-id="{html.escape(unit_id, quote=True)}" '
                f'data-source-sha256="{source_hash}" data-target-sha256="{target_hash}">\n'
                f'<div class="bitext-source" xml:lang="{source_language}" lang="{source_language}">\n'
                f"{render_paragraphs(source_texts, unit_type, heading_level, source_file, images)}\n"
                "</div>\n"
                f'<div class="bitext-target" xml:lang="{target_language}" lang="{target_language}">\n'
                f"{render_paragraphs(target_texts, unit_type, heading_level, target_file, images)}\n"
                "</div>\n"
                "</section>"
            )
        write_text(work_dir / "EPUB" / href, xhtml_doc(title_text, "\n".join(sections), target_language))
        manifest_items.append(f'\n    <item id="doc{doc_index}" href="{href}" media-type="application/xhtml+xml" />')
        spine_items.append(f'\n    <itemref idref="doc{doc_index}" />')
        nav_items.append(f'<li><a href="{href}">{html.escape(title_text)}</a></li>')

    cover_href = next((f"{slug(file.stem)}.xhtml" for file in packaged_frontmatter if file.stem == "cover"), "")
    info_href = next((f"{slug(file.stem)}.xhtml" for file in packaged_frontmatter if file.stem in {"book-info", "book_info"}), "")
    landmark_links = []
    if cover_href:
        landmark_links.append(f'<li><a epub:type="cover" href="{cover_href}">{html.escape(labels["cover"])}</a></li>')
    if info_href:
        landmark_links.append(f'<li><a epub:type="frontmatter" href="{info_href}">{html.escape(labels["book_info"])}</a></li>')
    landmarks = (
        f'<nav epub:type="landmarks" id="landmarks" hidden="hidden"><h2>{html.escape(labels["landmarks"])}</h2>'
        f'<ol>{"".join(landmark_links)}</ol></nav>' if landmark_links else ""
    )
    write_text(
        work_dir / "EPUB" / "nav.xhtml",
        xhtml_doc(
            labels["toc"],
            f'<nav epub:type="toc" id="toc"><h1>{html.escape(labels["toc"])}</h1><ol>{"".join(nav_items)}</ol></nav>{landmarks}',
            target_language,
        ),
    )
    write_text(
        work_dir / "EPUB" / "package.opf",
        package_opf(title_for_package, metadata, source_language, target_language,
                    manifest_items + images.manifest_items(), spine_items),
    )

    epub_path = book_root / bilingual_artifact(state)
    zip_epub(work_dir, epub_path)
    print(f"wrote {epub_path.relative_to(book_root).as_posix()}")


if __name__ == "__main__":
    main()
