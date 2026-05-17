from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET


BOOK_ROOT = Path(__file__).resolve().parents[1]
TRANSLATION = BOOK_ROOT / "chapters" / "translated" / "010_book_i_10_chords.md"
STAGE2 = BOOK_ROOT / "preproduction" / "stage2_sample"
EPUB_SRC = STAGE2 / "sample_epub_source"
EPUB_OUT = STAGE2 / "sample_book.epub"
STANDALONE_XHTML = STAGE2 / "sample_chapter.xhtml"
STANDALONE_ASSETS = STAGE2 / "sample_assets"
FACSIMILE_DIR = BOOK_ROOT / "assets" / "figures" / "facsimile" / "book_i10"

FACSIMILE_MAP = {
    "i10_fig01_decagon_pentagon.svg": "i10_fig01_decagon_pentagon_facsimile.png",
    "i10_fig02_cyclic_quadrilateral_lemma.svg": "i10_fig02_cyclic_quadrilateral_lemma_facsimile.png",
    "i10_fig03_difference_of_arcs.svg": "i10_fig03_difference_of_arcs_facsimile.png",
    "i10_fig04_half_arc.svg": "i10_fig04_half_arc_facsimile.png",
    "i10_fig05_sum_of_arcs.svg": "i10_fig05_sum_of_arcs_facsimile.png",
    "i10_fig06_chord_arc_ratio.svg": "i10_fig06_chord_arc_ratio_facsimile.png",
    "i10_fig07_one_degree_bracket.svg": "i10_fig07_one_degree_bracket_facsimile.png",
}

CONSTRAINT_CHECK = BOOK_ROOT / "scripts" / "check_translation_constraints.py"


def clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def inline_markup(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return re.sub(
        r"（依据《几何原本》[^）]+?〔\d+〕）",
        lambda match: f'<span class="source-ref">{match.group(0)}</span>',
        escaped,
    )


def image_lines(markdown: str) -> list[tuple[str, Path]]:
    results: list[tuple[str, Path]] = []
    for alt, src in re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", markdown):
        source = (TRANSLATION.parent / src).resolve()
        try:
            source.relative_to(BOOK_ROOT.resolve())
        except ValueError as exc:
            raise ValueError(f"Image path escapes book root: {src}") from exc
        if not source.exists():
            raise FileNotFoundError(f"Missing image: {source}")
        results.append((alt, source))
    return results


def epub_image_for(markdown_src: str) -> Path:
    basename = Path(markdown_src).name
    facsimile_name = FACSIMILE_MAP.get(basename)
    if facsimile_name:
        source = FACSIMILE_DIR / facsimile_name
        if not source.exists():
            raise FileNotFoundError(f"Missing facsimile image: {source}")
        return source
    source = (TRANSLATION.parent / markdown_src).resolve()
    try:
        source.relative_to(BOOK_ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"Image path escapes book root: {markdown_src}") from exc
    if not source.exists():
        raise FileNotFoundError(f"Missing image: {source}")
    return source


def md_to_body(markdown: str, image_prefix: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    in_blockquote = False
    in_ordered_list = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(item.strip() for item in paragraph)
            out.append(f"<p>{inline_markup(text)}</p>")
            paragraph = []

    def close_blockquote() -> None:
        nonlocal in_blockquote
        if in_blockquote:
            out.append("</blockquote>")
            in_blockquote = False

    def close_ordered_list() -> None:
        nonlocal in_ordered_list
        if in_ordered_list:
            out.append("</ol>")
            in_ordered_list = False

    for raw in lines:
        line = raw.rstrip()
        image_match = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", line.strip())
        if not line.strip():
            flush_paragraph()
            close_blockquote()
            close_ordered_list()
            continue
        if image_match:
            flush_paragraph()
            close_blockquote()
            close_ordered_list()
            alt = image_match.group(1)
            src = image_match.group(2)
            basename = epub_image_for(src).name
            escaped_alt = html.escape(alt, quote=True)
            caption = inline_markup(alt)
            out.append(
                '<figure class="facsimile-figure">'
                f'<img src="{image_prefix}{basename}" alt="{escaped_alt}" />'
                f"<figcaption>{caption}</figcaption>"
                "</figure>"
            )
            continue
        if line.startswith("# "):
            flush_paragraph()
            close_blockquote()
            close_ordered_list()
            out.append(f"<h1>{inline_markup(line[2:].strip())}</h1>")
            continue
        if line.startswith("## "):
            flush_paragraph()
            close_blockquote()
            close_ordered_list()
            out.append(f"<h2>{inline_markup(line[3:].strip())}</h2>")
            continue
        if line.startswith("### "):
            flush_paragraph()
            close_blockquote()
            close_ordered_list()
            out.append(f"<h3>{inline_markup(line[4:].strip())}</h3>")
            continue
        metadata_match = re.fullmatch(r"([A-Za-z_]+):\s*(.*)", line.strip())
        if metadata_match:
            flush_paragraph()
            close_blockquote()
            close_ordered_list()
            key = html.escape(metadata_match.group(1), quote=False)
            value = inline_markup(metadata_match.group(2))
            out.append(f'<p class="metadata"><strong>{key}:</strong> {value}</p>')
            continue
        ordered_match = re.fullmatch(r"\d+\.\s+(.*)", line.strip())
        if ordered_match:
            flush_paragraph()
            close_blockquote()
            if not in_ordered_list:
                out.append("<ol>")
                in_ordered_list = True
            out.append(f"<li>{inline_markup(ordered_match.group(1))}</li>")
            continue
        if line.startswith("> "):
            flush_paragraph()
            close_ordered_list()
            if not in_blockquote:
                out.append("<blockquote>")
                in_blockquote = True
            out.append(f"<p>{inline_markup(line[2:].strip())}</p>")
            continue
        paragraph.append(line)

    flush_paragraph()
    close_blockquote()
    close_ordered_list()
    return "\n".join(out)


def xhtml_document(title: str, body: str, css_href: str) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN" lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="{css_href}" />
</head>
<body>
{body}
</body>
</html>
"""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def copy_assets(markdown: str) -> list[str]:
    copied: list[str] = []
    for _, markdown_source in re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", markdown):
        source = epub_image_for(markdown_source)
        target_name = source.name
        shutil.copy2(source, EPUB_SRC / "EPUB" / "images" / target_name)
        shutil.copy2(source, STANDALONE_ASSETS / target_name)
        copied.append(target_name)
    return copied


def write_epub_container() -> None:
    write_text(
        EPUB_SRC / "mimetype",
        "application/epub+zip",
    )
    write_text(
        EPUB_SRC / "META-INF" / "container.xml",
        """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml" />
  </rootfiles>
</container>
""",
    )


def write_css() -> None:
    css = """html {
  width: 100%;
}
body {
  box-sizing: border-box;
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 1.2em;
  line-height: 1.72;
  orphans: 2;
  widows: 2;
  overflow-wrap: break-word;
}
h1 {
  font-size: 1.55em;
  line-height: 1.25;
  margin: 0 0 1em;
}
h2 {
  font-size: 1.18em;
  line-height: 1.35;
  margin: 1.5em 0 0.55em;
}
h3 {
  font-size: 1.03em;
  line-height: 1.4;
  margin: 1.25em 0 0.45em;
}
p {
  margin: 0 0 0.65em;
  text-indent: 2em;
}
ol {
  margin: 0.4em 0 1em;
  padding-left: 1.5em;
}
li {
  margin: 0 0 0.55em;
}
code {
  font-family: monospace;
  font-size: 0.92em;
  overflow-wrap: anywhere;
}
.source-ref {
  font-size: 0.7em;
  line-height: 1.2;
  color: #555;
}
figure {
  margin: 1.2em 0;
  page-break-inside: avoid;
  break-inside: avoid;
  text-align: center;
}
img {
  max-width: 100%;
  height: auto;
}
figcaption {
  font-size: 0.88em;
  line-height: 1.45;
  margin-top: 0.35em;
  text-align: center;
}
figure.facsimile-figure img {
  display: block;
  width: 100%;
  max-width: 34em;
  margin: 0 auto;
}
blockquote {
  margin: 1em 0;
  padding-left: 1em;
  border-left: 0.18em solid #777;
}
blockquote p {
  text-indent: 0;
}
.metadata {
  text-indent: 0;
  margin: 0 0 0.25em;
  line-height: 1.45;
  font-size: 0.92em;
}
.trial-note {
  margin: 1em 0;
  padding: 0.8em 0;
  border-top: 1px solid #999;
  border-bottom: 1px solid #999;
}
.cover {
  text-align: center;
  padding-top: 15%;
}
.cover h1 {
  font-size: 1.7em;
}
"""
    write_text(EPUB_SRC / "EPUB" / "styles" / "book.css", css)
    write_text(STANDALONE_ASSETS / "book.css", css)


def write_cover() -> None:
    cover_svg = """<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1800" viewBox="0 0 1200 1800" role="img" aria-label="Book I.10 trial sample cover">
  <rect width="1200" height="1800" fill="#f7f4ec" />
  <rect x="100" y="120" width="1000" height="1560" fill="none" stroke="#202020" stroke-width="6" />
  <circle cx="600" cy="760" r="260" fill="none" stroke="#202020" stroke-width="7" />
  <line x1="340" y1="760" x2="860" y2="760" stroke="#202020" stroke-width="7" />
  <line x1="600" y1="500" x2="760" y2="960" stroke="#202020" stroke-width="5" />
  <line x1="440" y1="960" x2="760" y2="960" stroke="#202020" stroke-width="5" />
  <text x="600" y="1180" text-anchor="middle" font-size="74" font-family="serif" fill="#202020">天文学大成</text>
  <text x="600" y="1280" text-anchor="middle" font-size="46" font-family="serif" fill="#202020">Book I.10 试译样本</text>
  <text x="600" y="1370" text-anchor="middle" font-size="34" font-family="serif" fill="#202020">圆内弦长之论</text>
  <text x="600" y="1510" text-anchor="middle" font-size="30" font-family="serif" fill="#202020">TRIAL SAMPLE EPUB</text>
</svg>
"""
    write_text(EPUB_SRC / "EPUB" / "images" / "cover.svg", cover_svg)

    cover_xhtml = xhtml_document(
        "天文学大成 Book I.10 试译样本",
        """<section class="cover">
  <h1>天文学大成</h1>
  <p>Book I.10 试译样本</p>
  <p>圆内弦长之论</p>
  <p>TRIAL SAMPLE EPUB</p>
</section>
""",
        "styles/book.css",
    )
    write_text(EPUB_SRC / "EPUB" / "cover.xhtml", cover_xhtml)


def write_book_info() -> None:
    body = """<section>
  <h1>版本说明</h1>
  <p>中文书名：天文学大成</p>
  <p>原名：Μαθηματικὴ Σύνταξις / Almagest</p>
  <p>作者：克劳狄乌斯·托勒密</p>
  <p>译制：LifeBook 书坊试译样本</p>
  <p>试译时间：2026-05-17</p>
  <p>公版来源候选：Wikimedia Commons, Heiberg Greek edition PDF。</p>
  <p>版权状态：研究与预翻译试点；正式出版前仍需完成来源页、文件哈希和公版状态复核。</p>
  <p>本 EPUB 只用于 Book I.10 单章节试译预制作评审，不代表全书翻译、正式 EPUB 或可发布版本。</p>
</section>
"""
    write_text(
        EPUB_SRC / "EPUB" / "book-info.xhtml",
        xhtml_document("版本说明", body, "styles/book.css"),
    )


def write_nav() -> None:
    nav = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-CN" lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <title>目录</title>
  <link rel="stylesheet" type="text/css" href="styles/book.css" />
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>目录</h1>
    <ol>
      <li><a href="book-info.xhtml">版本说明</a></li>
      <li><a href="sample_chapter.xhtml">Book I.10 圆内弦长之论</a></li>
    </ol>
  </nav>
</body>
</html>
"""
    write_text(EPUB_SRC / "EPUB" / "nav.xhtml", nav)


def media_type(filename: str) -> str:
    if filename.endswith(".svg"):
        return "image/svg+xml"
    if filename.endswith(".png"):
        return "image/png"
    raise ValueError(f"Unsupported asset type: {filename}")


def write_package(figure_names: list[str]) -> None:
    modified = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    figure_items = "\n".join(
        f'    <item id="fig{i:02d}" href="images/{html.escape(name)}" media-type="{media_type(name)}" />'
        for i, name in enumerate(figure_names, 1)
    )
    spine = """    <itemref idref="cover" />
    <itemref idref="book-info" />
    <itemref idref="chapter" />"""
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package version="3.0" unique-identifier="bookid" xmlns="http://www.idpf.org/2007/opf">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/">
    <dc:identifier id="bookid">urn:uuid:ptolemy-almagest-book-i10-trial-sample</dc:identifier>
    <dc:title>天文学大成：Book I.10 试译样本</dc:title>
    <dc:creator>Claudius Ptolemaeus</dc:creator>
    <dc:contributor>LifeBook 书坊试译样本</dc:contributor>
    <dc:language>zh-CN</dc:language>
    <dc:source>https://commons.wikimedia.org/wiki/File:Almagest_Complete,_Heiberg.pdf</dc:source>
    <dc:description>Book I.10 controlled trial translation sample. Not a full-book translation or publishable EPUB.</dc:description>
    <dc:rights>Research and pretranslation trial only; source rights and publication gates remain open.</dc:rights>
    <dc:publisher>LifeBook 书坊</dc:publisher>
    <dcterms:modified>{modified}</dcterms:modified>
    <meta property="schema:accessMode">textual</meta>
    <meta property="schema:accessMode">visual</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav" />
    <item id="cover" href="cover.xhtml" media-type="application/xhtml+xml" />
    <item id="book-info" href="book-info.xhtml" media-type="application/xhtml+xml" />
    <item id="chapter" href="sample_chapter.xhtml" media-type="application/xhtml+xml" />
    <item id="css" href="styles/book.css" media-type="text/css" />
    <item id="cover-image" href="images/cover.svg" media-type="image/svg+xml" properties="cover-image" />
{figure_items}
  </manifest>
  <spine>
{spine}
  </spine>
</package>
"""
    write_text(EPUB_SRC / "EPUB" / "package.opf", opf)


def build_zip() -> None:
    if EPUB_OUT.exists():
        EPUB_OUT.unlink()
    with zipfile.ZipFile(EPUB_OUT, "w") as zf:
        zf.write(EPUB_SRC / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for path in sorted(EPUB_SRC.rglob("*")):
            if path.is_file() and path.name != "mimetype":
                zf.write(path, path.relative_to(EPUB_SRC).as_posix(), compress_type=zipfile.ZIP_DEFLATED)


def validate_xml_files() -> None:
    for path in [
        EPUB_SRC / "META-INF" / "container.xml",
        EPUB_SRC / "EPUB" / "package.opf",
        EPUB_SRC / "EPUB" / "nav.xhtml",
        EPUB_SRC / "EPUB" / "cover.xhtml",
        EPUB_SRC / "EPUB" / "book-info.xhtml",
        EPUB_SRC / "EPUB" / "sample_chapter.xhtml",
    ]:
        ET.parse(path)


def main() -> None:
    subprocess.run([sys.executable, str(CONSTRAINT_CHECK), "--scope=trial-book-i10"], cwd=BOOK_ROOT, check=True)

    markdown = TRANSLATION.read_text(encoding="utf-8")
    if "translation_status: `TRIAL_TRANSLATION`" not in markdown:
        raise ValueError("Input is not marked as a trial translation.")

    clean_dir(EPUB_SRC)
    clean_dir(STANDALONE_ASSETS)
    (EPUB_SRC / "META-INF").mkdir(parents=True, exist_ok=True)
    (EPUB_SRC / "EPUB" / "images").mkdir(parents=True, exist_ok=True)
    (EPUB_SRC / "EPUB" / "styles").mkdir(parents=True, exist_ok=True)

    write_epub_container()
    write_css()
    write_cover()
    write_book_info()
    write_nav()

    figure_names = copy_assets(markdown)
    body = md_to_body(markdown, "images/")
    chapter = xhtml_document("Book I.10 圆内弦长之论", body, "styles/book.css")
    write_text(EPUB_SRC / "EPUB" / "sample_chapter.xhtml", chapter)

    standalone_body = md_to_body(markdown, "sample_assets/")
    standalone = xhtml_document("Book I.10 圆内弦长之论", standalone_body, "sample_assets/book.css")
    write_text(STANDALONE_XHTML, standalone)

    write_package(figure_names)
    validate_xml_files()
    build_zip()
    print(f"wrote {EPUB_OUT.relative_to(BOOK_ROOT)}")
    print(f"figures={len(figure_names)}")


if __name__ == "__main__":
    main()
