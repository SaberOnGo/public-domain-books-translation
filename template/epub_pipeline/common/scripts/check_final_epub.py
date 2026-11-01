"""Reader-facing gate for finished EPUB files.

Every other text gate in this pipeline reads Markdown or QA records. This one
opens the EPUB a reader actually receives (target-only, bilingual parallel, or
source-language edition) and checks the rendered XHTML for production residue:
escaped HTML tags, Markdown markup, empty or placeholder pages, visible spaces
between CJK characters, pipeline and tool traces, cover-page text, illustration
placeholders, file-name navigation labels, and package metadata problems.

本脚本检查读者真正拿到的 EPUB（单语版、双语版、原文版），而不是 Markdown 或 QA 记录。
"""
from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
import sys
import zipfile
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = "output/final_epub_check.json"
MAX_SAMPLES_PER_RULE = 12

OPF_NS = "http://www.idpf.org/2007/opf"
DC_NS = "http://purl.org/dc/elements/1.1/"

# Ideographs, kana and CJK punctuation. Hangul is excluded on purpose: Korean uses spaces between words.
CJK = r"、-〿぀-ヿ㐀-䶿一-鿿豈-﫿！-／：-＠［-｀｛-･"
CJK_CHAR = re.compile(f"[{CJK}]")

RULES = {
    # rule id: (severity, zh, en)
    "escaped_html_tag": ("error", "转义后的 HTML 标签作为文字显示", "escaped HTML tag shown as text"),
    "markdown_heading_marker": ("error", "段落以 Markdown 标题符号 # 开头", "paragraph starts with a Markdown heading marker"),
    "markdown_emphasis_marker": ("error", "Markdown 强调符号（** __ _x_ *x*）残留", "Markdown emphasis marker left in text"),
    "markdown_quote_marker": ("error", "Markdown 引文符号 > 残留", "Markdown quote marker '>' left in text"),
    "markdown_list_marker": ("error", "段落以 Markdown 列表符号开头", "paragraph starts with a Markdown list marker"),
    "markdown_link_or_image": ("error", "Markdown 链接或图片语法残留", "Markdown link or image syntax left in text"),
    "markdown_code_backtick": ("error", "反引号残留", "backtick code markup left in text"),
    "markdown_footnote_syntax": ("error", "Markdown 脚注语法 [^n] 残留", "Markdown footnote syntax left in text"),
    "print_separator": ("error", "旧纸书分隔符（* * * / ---）残留", "print-era separator left in text"),
    "empty_page": ("error", "空白页（没有任何可见内容）", "page has no visible content"),
    "placeholder_page": ("error", "只有占位标题的前言/译者说明/注释页", "placeholder preface, translator-note or notes page with no body"),
    "heading_only_page": ("warning", "只有标题、没有正文的页面（若是部分标题页可忽略）", "page with headings only (ignore for part-title pages)"),
    "placeholder_text": ("error", "模板占位文字或待办标记", "template placeholder or to-do text"),
    "pipeline_trace": ("error", "流水线内部标记泄漏到读者文本", "internal pipeline token visible to readers"),
    "source_scaffold": ("error", "拆章或抽取脚本注入的脚手架行被当作正文", "split/extraction scaffold line rendered as text"),
    "tool_name_in_frontmatter": ("error", "封面、书籍信息页或元数据出现 AI 工具名", "AI tool name on the cover, book-info page or in metadata"),
    "tool_name_elsewhere": ("warning", "AI 工具名或 AI 辅助说明（若属原书内容可忽略）", "AI tool name or AI-assistance wording (ignore if it is source content)"),
    "process_words_in_frontmatter": ("error", "前置页出现制作流程用语", "production-process wording in front matter"),
    "illustration_placeholder": ("error", "插图占位文字残留", "illustration placeholder text"),
    "gutenberg_boilerplate": ("error", "Project Gutenberg 样板文字或制作者署名进入读者文本", "Project Gutenberg boilerplate or producer credit in reader text"),
    "cjk_ascii_space": ("error", "中日文字符之间有可见半角空格", "visible ASCII space between CJK characters"),
    "cjk_ascii_space_in_heading_or_frontmatter": ("warning", "标题或前置页里中日文字符之间有半角空格", "ASCII space between CJK characters in a heading or front matter"),
    "ascii_quote_in_cjk": ("error", "中文里使用直引号 \"", "straight double quote inside CJK text"),
    "cover_visible_text": ("error", "封面页显示了图片以外的文字（标题、图注等）", "cover page shows text besides the image"),
    "cover_missing": ("warning", "未找到封面页或封面图", "no cover page or cover image found"),
    "nav_label_looks_like_filename": ("error", "目录条目显示为文件名或内部单元名", "navigation label looks like a file or unit name"),
    "nav_repeated_label": ("warning", "目录中同一条目名称连续重复多次", "same navigation label repeated many times in a row"),
    "metadata_missing": ("error", "OPF 缺少必需的元数据", "required OPF metadata missing"),
    "metadata_placeholder": ("error", "OPF 元数据是模板默认值", "OPF metadata still holds a template default"),
    "bilingual_language_metadata": ("error", "双语版 OPF 缺少源语言或目标语言 dc:language", "bilingual edition lacks both dc:language entries"),
    "duplicate_identifier_across_editions": ("error", "同一本书的不同版本共用 dc:identifier", "editions of one book share a dc:identifier"),
    "bare_note_label": ("warning", "正文段落以裸“译注：/原注：”开头", "body paragraph starts with a bare note label"),
    "midparagraph_list_dash": ("warning", "段落中间出现“ - ”列表残留", "list dash inside a paragraph"),
}

FRONTMATTER_NAME = re.compile(
    r"(?:^|[/_-])(cover|book[_-]?info|translator[_-]?note|translators?[_-]?note|edition[_-]?note|preface|colophon|"
    r"copyright|about|license|private[_-]?use|front[_-]?matter|title[_-]?page)",
    re.IGNORECASE,
)
PLACEHOLDER_TITLES = re.compile(
    r"^(?:preface|foreword|translator'?s?\s+note|translator\s+notes?|notes?|introduction|前言|序言|序|译者说明|译者附记|译者前言|"
    r"附记|题记|版本说明|编者说明|注释|注|原注|本章注释|章末注|译本前言模板|译者说明模板)$",
    re.IGNORECASE,
)
NOTES_HEADING = re.compile(r"注释|原注|本章注释|章末注|^notes?\b|footnotes", re.IGNORECASE)
ESCAPED_TAG = re.compile(
    r"&lt;/?(?:br|p|div|span|blockquote|em|strong|i|b|u|sup|sub|a|h[1-6]|ul|ol|li|table|tr|td|th|figure|figcaption|img|section|aside)\b[^&<>]{0,120}?/?&gt;",
    re.IGNORECASE,
)
MD_HEADING = re.compile(r"^#{1,6}\s+\S")
MD_STRONG = re.compile(r"\*\*[^*\n]{1,120}\*\*|(?<![\w_])__[^_\n]{1,120}__(?![\w_])")
MD_UNDERSCORE_EM = re.compile(r"(?<![\w/\\_.-])_[^\s_<][^_\n<]{0,80}?[^\s_<]_(?![\w_])")
MD_STAR_EM = re.compile(r"(?<![\w*])\*[^\s*][^*\n]{0,80}?[^\s*]\*(?![\w*])")
MD_QUOTE_START = re.compile(r"^>\s*\S")
MD_QUOTE_INNER = re.compile(r"[。！？；，：、”’」』）]\s*>\s+\S")
MD_LIST_START = re.compile(r"^[-*+]\s+\S")
MD_LIST_INNER = re.compile(r"[。！？”」\.!?]\s+-\s+[\S]")
MD_LINK = re.compile(r"!?\[[^\]\n]{1,160}\]\((?:https?://|\.{0,2}/|#|[\w.-]+\.(?:x?html?|md|png|jpe?g|svg|webp))[^)\s]{0,300}\)")
MD_BACKTICK = re.compile(r"`[^`'\n]{1,80}`")
MD_FOOTNOTE = re.compile(r"\[\^[\w-]{1,20}\]")
SEPARATOR = re.compile(r"^[\s*\-_=~·•—–]{3,}$")
PLACEHOLDER_TEXT = re.compile(
    r"模板占位|本页为模板|前言模板|说明模板|Translator Name|Book Title|\bTODO\b|\bTBD\b|\bFIXME\b|lorem ipsum|\{\{|\}\}|【待补|待补充|待填写|此处填写",
    re.IGNORECASE,
)
PIPELINE_TRACE = re.compile(
    r"issues_found|fixes_applied|FIXED_RECHECK|latest_round_status|allow_next_chapter|random_spotcheck|chapter_controls?\b|"
    r"chapters/(?:final|translated|src)|translation_units|pipeline_state|lifebook-unit|\{\{\s*pn:|\bround_\d{2,}|"
    r"qa/(?:gates|fidelity|readability|chapter|random)|release_state\.json|manifest\.json",
    re.IGNORECASE,
)
SCAFFOLD = re.compile(r"^(?:Source part|Source chapter|Source file)\s*:|^(?:来源部|来源分部|来源部分|来源章节|源文件)\s*[：:]", re.IGNORECASE)
TOOL_NAMES = re.compile(r"\bCodex\b|ChatGPT|\bGPT-?\d|\bGPT\b|\bClaude\b|\bGemini\b|\bOpenAI\b|\bAnthropic\b|\bCopilot\b")
AI_WORDING = re.compile(r"\bLLM\b|大模型|AI\s*辅助|AI\s*翻译|人工智能辅助|机器翻译")
# Producer lines prescribed by the cover and private-use policies contain spaces between CJK words,
# and Chinese chapter labels conventionally put a space before the title ("第一章 家族").
ALLOWED_CJK_SPACE = re.compile(r"书坊 译制|开源项目 个人自制|(?:^|\n)第[一二三四五六七八九十百千零〇两\d]+[章节卷部篇回集] ")
COVER_OR_INFO_NAME = re.compile(r"(?:^|[/_-])(cover|book[_-]?info|title[_-]?page|colophon)", re.IGNORECASE)
PROCESS_WORDS = re.compile(
    r"\bQA\b|门禁|抽检|章节控制|LifeBook Digest|站点外壳|制作日志|工作文件|质量记录|\bprompt\b|审校流程记录|流水线",
    re.IGNORECASE,
)
ILLUSTRATION = re.compile(r"\[(?:插图|插画|图片|图像|Illustration|ILLUSTRATION|Picture|Image)\s*[：:\]]")
GUTENBERG = re.compile(
    r"Project Gutenberg(?:-tm)? License|\*\*\*\s*(?:START|END) OF|Transcriber['’]s Note|pgdp\.net|Distributed Proofread|"
    r"分布式校对|古腾堡计划许可",
    re.IGNORECASE,
)
GUTENBERG_CREDIT_START = re.compile(r"^(?:Produced by|This (?:e-?book|etext) was produced by|E-text prepared by)\b")
CJK_SPACE = re.compile(f"(?<=[{CJK}])[  ]+(?=[{CJK}])")
ASCII_QUOTE = re.compile(f'[{CJK}]"|"[{CJK}]')
BARE_NOTE = re.compile(r"^(?:译注|原注|脚注|尾注|附注)[：:]")
NAV_FILENAME = re.compile(r"^\d{2,4}[_-][A-Za-z0-9_-]+$|_unit_|\.x?html?$|^(?:chapter|vol)\d*_[A-Za-z0-9_]+$|^[A-Za-z]+(?:_[A-Za-z0-9]+){2,}$")
METADATA_PLACEHOLDER = re.compile(r"^(?:Translator Name|Untitled Book|Unknown|project-book-id-v1|Book Title|TODO|TBD)$", re.IGNORECASE)

BLOCK_TAGS = ("p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "td", "th", "figcaption", "dt", "dd", "blockquote", "caption", "pre")
HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}


@dataclass
class Doc:
    href: str
    raw: str
    lang: str = ""


@dataclass
class EpubData:
    path: Path
    identifier: str = ""
    titles: list[str] = field(default_factory=list)
    creators: list[str] = field(default_factory=list)
    contributors: list[str] = field(default_factory=list)
    publishers: list[str] = field(default_factory=list)
    languages: list[str] = field(default_factory=list)
    spine: list[Doc] = field(default_factory=list)
    nav: Doc | None = None
    cover_image_hrefs: set[str] = field(default_factory=set)
    cover_doc_hrefs: set[str] = field(default_factory=set)


@dataclass
class Report:
    epub: str
    edition: str = ""
    issues: list[dict] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)

    def add(self, rule: str, href: str, sample: str) -> None:
        self.counts[rule] = self.counts.get(rule, 0) + 1
        if self.counts[rule] <= MAX_SAMPLES_PER_RULE:
            severity, zh, en = RULES[rule]
            self.issues.append({
                "rule": rule,
                "severity": severity,
                "file": href,
                "sample": compact(sample),
                "message_zh": zh,
                "message_en": en,
            })

    def summary(self) -> dict:
        errors = sum(n for rule, n in self.counts.items() if RULES[rule][0] == "error")
        warnings = sum(n for rule, n in self.counts.items() if RULES[rule][0] == "warning")
        return {
            "epub": self.epub,
            "edition": self.edition,
            "status": "FAIL" if errors else "PASS",
            "error_count": errors,
            "warning_count": warnings,
            "rule_counts": dict(sorted(self.counts.items())),
            "issues": self.issues,
        }


def compact(text: str, width: int = 160) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= width else text[: width - 1] + "…"


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def read_epub(path: Path) -> EpubData:
    data = EpubData(path=path)
    with zipfile.ZipFile(path) as archive:
        container = ET.fromstring(archive.read("META-INF/container.xml"))
        opf_path = next(el.attrib["full-path"] for el in container.iter() if local(el.tag) == "rootfile")
        base = posixpath.dirname(opf_path)
        opf = ET.fromstring(archive.read(opf_path))
        unique_id = opf.attrib.get("unique-identifier", "")
        manifest: dict[str, dict] = {}
        for el in opf.iter():
            name = local(el.tag)
            text = (el.text or "").strip()
            if el.tag == f"{{{DC_NS}}}identifier" and (not data.identifier or el.attrib.get("id") == unique_id):
                data.identifier = text
            elif el.tag == f"{{{DC_NS}}}title" and text:
                data.titles.append(text)
            elif el.tag == f"{{{DC_NS}}}creator" and text:
                data.creators.append(text)
            elif el.tag == f"{{{DC_NS}}}contributor" and text:
                data.contributors.append(text)
            elif el.tag == f"{{{DC_NS}}}publisher" and text:
                data.publishers.append(text)
            elif el.tag == f"{{{DC_NS}}}language" and text:
                data.languages.append(text)
            elif name == "item" and el.tag.startswith(f"{{{OPF_NS}}}"):
                manifest[el.attrib.get("id", "")] = el.attrib
            elif name == "meta" and el.attrib.get("name") == "cover" and el.attrib.get("content"):
                cover_item = el.attrib["content"]
                data.cover_image_hrefs.add(cover_item)  # resolved below
        resolved_cover_ids = set(data.cover_image_hrefs)
        data.cover_image_hrefs = set()
        for item_id, item in manifest.items():
            href = posixpath.normpath(posixpath.join(base, item.get("href", "")))
            if "cover-image" in item.get("properties", "") or item_id in resolved_cover_ids:
                data.cover_image_hrefs.add(href)
            if "nav" in item.get("properties", "").split():
                data.nav = Doc(href=href, raw=archive.read(href).decode("utf-8", "replace"))
        for el in opf.iter():
            if local(el.tag) != "itemref":
                continue
            item = manifest.get(el.attrib.get("idref", ""))
            if not item or "html" not in item.get("media-type", ""):
                continue
            href = posixpath.normpath(posixpath.join(base, item.get("href", "")))
            try:
                raw = archive.read(href).decode("utf-8", "replace")
            except KeyError:
                continue
            lang_match = re.search(r"<html[^>]*\b(?:xml:)?lang=\"([^\"]+)\"", raw)
            data.spine.append(Doc(href=href, raw=raw, lang=lang_match.group(1) if lang_match else ""))
        if data.nav is not None:
            for match in re.finditer(r"<a\b[^>]*epub:type=\"cover\"[^>]*href=\"([^\"#]+)", data.nav.raw):
                nav_base = posixpath.dirname(data.nav.href)
                data.cover_doc_hrefs.add(posixpath.normpath(posixpath.join(nav_base, match.group(1))))
    return data


def body_of(raw: str) -> str:
    match = re.search(r"<body\b[^>]*>(.*)</body>", raw, flags=re.DOTALL | re.IGNORECASE)
    body = match.group(1) if match else raw
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    return re.sub(r"<(script|style)\b.*?</\1>", "", body, flags=re.DOTALL | re.IGNORECASE)


def strip_tags(fragment: str) -> str:
    fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.IGNORECASE)
    return html.unescape(re.sub(r"<[^>]+>", "", fragment))


class BlockCollector(HTMLParser):
    """Collect visible text per innermost block element; <br> becomes a newline."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[list] = []
        self.blocks: list[tuple[str, str]] = []
        self.skip = 0

    def _emit(self, tag: str, parts: list[str]) -> None:
        text = "".join(parts).strip()
        if text:
            self.blocks.append((tag, text))

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        elif tag == "br":
            self.handle_data("\n")
        elif tag in CONTAINER_TAGS:
            if self.stack:
                top = self.stack[-1]
                self._emit(top[0], top[1])
                top[1] = []
            self.stack.append([tag, []])

    def handle_startendtag(self, tag: str, attrs: list) -> None:
        if tag == "br":
            self.handle_data("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
            return
        if tag not in CONTAINER_TAGS:
            return
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                while len(self.stack) > index:
                    popped = self.stack.pop()
                    self._emit(popped[0], popped[1])
                break

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        if self.stack:
            self.stack[-1][1].append(data)
        elif data.strip():
            self.blocks.append(("body", data.strip()))

    def close(self) -> None:
        super().close()
        while self.stack:
            popped = self.stack.pop()
            self._emit(popped[0], popped[1])


CONTAINER_TAGS = set(BLOCK_TAGS) | {"div", "section", "aside", "nav", "header", "footer", "figure", "ol", "ul", "dl", "table", "tr", "body"}


def block_texts(body: str) -> list[tuple[str, str]]:
    """Return (tag, visible text) for each innermost text block."""
    collector = BlockCollector()
    collector.feed(body)
    collector.close()
    return collector.blocks


def is_frontmatter(href: str, index: int, first_body_index: int) -> bool:
    name = posixpath.basename(href)
    return bool(FRONTMATTER_NAME.search(name)) or index < first_body_index


def find_first_body_index(spine: list[Doc]) -> int:
    for index, doc in enumerate(spine):
        name = posixpath.basename(doc.href)
        if not FRONTMATTER_NAME.search(name):
            return index
    return len(spine)


def is_cover_doc(doc: Doc, data: EpubData, index: int) -> bool:
    if doc.href in data.cover_doc_hrefs:
        return True
    name = posixpath.basename(doc.href).lower()
    if name.startswith("cover") or "_cover." in name:
        return True
    if index == 0 and data.cover_image_hrefs:
        body = body_of(doc.raw)
        doc_dir = posixpath.dirname(doc.href)
        for src in re.findall(r"<img\b[^>]*\bsrc=\"([^\"]+)\"", body):
            if posixpath.normpath(posixpath.join(doc_dir, src)) in data.cover_image_hrefs:
                return True
    return False


def check_doc(doc: Doc, data: EpubData, index: int, first_body_index: int, report: Report) -> None:
    body = body_of(doc.raw)
    for match in ESCAPED_TAG.finditer(body):
        report.add("escaped_html_tag", doc.href, html.unescape(body[max(0, match.start() - 40): match.end() + 40]))
    visible = strip_tags(body)
    has_image = bool(re.search(r"<(?:img|svg|image)\b", body, flags=re.IGNORECASE))
    blocks = block_texts(body)
    headings = [text for tag, text in blocks if tag in HEADING_TAGS]
    paragraphs = [text for tag, text in blocks if tag not in HEADING_TAGS]
    frontmatter = is_frontmatter(doc.href, index, first_body_index)

    if is_cover_doc(doc, data, index):
        if visible.strip():
            report.add("cover_visible_text", doc.href, visible)
        return

    if not visible.strip() and not has_image:
        report.add("empty_page", doc.href, posixpath.basename(doc.href))
        return
    if headings and not paragraphs and not has_image:
        joined = " / ".join(headings)
        if any(PLACEHOLDER_TITLES.match(h.strip()) or NOTES_HEADING.search(h) for h in headings):
            report.add("placeholder_page", doc.href, joined)
        else:
            report.add("heading_only_page", doc.href, joined)

    cover_or_info = bool(COVER_OR_INFO_NAME.search(posixpath.basename(doc.href)))
    block_checks = (
        ("markdown_emphasis_marker", MD_STRONG),
        ("markdown_emphasis_marker", MD_UNDERSCORE_EM),
        ("markdown_emphasis_marker", MD_STAR_EM),
        ("markdown_link_or_image", MD_LINK),
        ("markdown_code_backtick", MD_BACKTICK),
        ("markdown_footnote_syntax", MD_FOOTNOTE),
        ("placeholder_text", PLACEHOLDER_TEXT),
        ("pipeline_trace", PIPELINE_TRACE),
        ("illustration_placeholder", ILLUSTRATION),
        ("gutenberg_boilerplate", GUTENBERG),
        ("ascii_quote_in_cjk", ASCII_QUOTE),
    )
    for tag, text in blocks:
        stripped = text.strip()
        heading = tag in HEADING_TAGS
        if MD_HEADING.match(stripped):
            report.add("markdown_heading_marker", doc.href, stripped)
        if MD_QUOTE_START.match(stripped) or MD_QUOTE_INNER.search(stripped):
            report.add("markdown_quote_marker", doc.href, stripped)
        if tag != "li" and MD_LIST_START.match(stripped):
            report.add("markdown_list_marker", doc.href, stripped)
        elif MD_LIST_INNER.search(stripped):
            report.add("midparagraph_list_dash", doc.href, stripped)
        if SEPARATOR.match(stripped):
            report.add("print_separator", doc.href, stripped)
        if SCAFFOLD.match(stripped):
            report.add("source_scaffold", doc.href, stripped)
        if GUTENBERG_CREDIT_START.match(stripped):
            report.add("gutenberg_boilerplate", doc.href, stripped)
        if not frontmatter and BARE_NOTE.match(stripped):
            report.add("bare_note_label", doc.href, stripped)
        for rule, pattern in block_checks:
            for match in pattern.finditer(stripped):
                report.add(rule, doc.href, stripped[max(0, match.start() - 30): match.end() + 30])
        spaced = ALLOWED_CJK_SPACE.sub("", stripped)
        for match in CJK_SPACE.finditer(spaced):
            rule = "cjk_ascii_space_in_heading_or_frontmatter" if (heading or frontmatter) else "cjk_ascii_space"
            report.add(rule, doc.href, spaced[max(0, match.start() - 30): match.end() + 30])
        for match in TOOL_NAMES.finditer(stripped):
            rule = "tool_name_in_frontmatter" if cover_or_info else "tool_name_elsewhere"
            report.add(rule, doc.href, stripped[max(0, match.start() - 30): match.end() + 30])
        if frontmatter:
            for match in AI_WORDING.finditer(stripped):
                report.add("tool_name_elsewhere", doc.href, stripped[max(0, match.start() - 30): match.end() + 30])
            for match in PROCESS_WORDS.finditer(stripped):
                report.add("process_words_in_frontmatter", doc.href, stripped[max(0, match.start() - 30): match.end() + 30])


def check_nav(data: EpubData, report: Report) -> None:
    if data.nav is None:
        return
    toc = re.search(r"<nav\b[^>]*epub:type=\"toc\"[^>]*>(.*?)</nav>", data.nav.raw, flags=re.DOTALL)
    labels = [strip_tags(m).strip() for m in re.findall(r"<a\b[^>]*>(.*?)</a>", toc.group(1) if toc else "", flags=re.DOTALL)]
    for label in labels:
        if NAV_FILENAME.search(label):
            report.add("nav_label_looks_like_filename", data.nav.href, label)
    run_label, run_length = "", 0
    for label in labels + [""]:
        if label == run_label:
            run_length += 1
            continue
        if run_label and run_length > 3:
            report.add("nav_repeated_label", data.nav.href, f"{run_label} ×{run_length}")
        run_label, run_length = label, 1


def check_metadata(data: EpubData, report: Report) -> None:
    for name, values in (("identifier", [data.identifier] if data.identifier else []), ("title", data.titles),
                         ("creator", data.creators), ("language", data.languages)):
        if not values:
            report.add("metadata_missing", "package.opf", f"dc:{name}")
    for name, values in (("identifier", [data.identifier]), ("title", data.titles), ("creator", data.creators),
                         ("contributor", data.contributors)):
        for value in values:
            if value and METADATA_PLACEHOLDER.match(value.strip()):
                report.add("metadata_placeholder", "package.opf", f"dc:{name}={value}")
    for value in data.creators + data.contributors + data.publishers:
        if TOOL_NAMES.search(value):
            report.add("tool_name_in_frontmatter", "package.opf", value)
    bilingual = any('class="bitext-' in doc.raw or "class='bitext-" in doc.raw for doc in data.spine)
    if bilingual and len({lang.lower() for lang in data.languages}) < 2:
        report.add("bilingual_language_metadata", "package.opf", ", ".join(data.languages) or "(none)")
    if not data.cover_image_hrefs and not data.cover_doc_hrefs:
        report.add("cover_missing", "package.opf", "no cover-image manifest item or cover landmark")


def display_path(path: Path, base: Path | None) -> str:
    """Reports are committed QA evidence, so they record paths relative to the book or library root."""
    for root in (base, Path.cwd()):
        if root is not None:
            try:
                return path.resolve().relative_to(root.resolve()).as_posix()
            except ValueError:
                continue
    return path.name


def check_epub(path: Path, edition: str = "", base: Path | None = None) -> tuple[Report, EpubData]:
    report = Report(epub=display_path(path, base), edition=edition)
    data = read_epub(path)
    first_body_index = find_first_body_index(data.spine)
    for index, doc in enumerate(data.spine):
        check_doc(doc, data, index, first_body_index, report)
    check_nav(data, report)
    check_metadata(data, report)
    return report, data


def check_editions(paths: list[tuple[Path, str]], base: Path | None = None) -> list[dict]:
    results: list[tuple[Report, EpubData]] = [check_epub(path, edition, base) for path, edition in paths]
    seen: dict[str, str] = {}
    for report, data in results:
        if not data.identifier:
            continue
        if data.identifier in seen and seen[data.identifier] != str(data.path):
            report.add("duplicate_identifier_across_editions", "package.opf",
                       f"{data.identifier} also used by {Path(seen[data.identifier]).name}")
        seen.setdefault(data.identifier, str(data.path))
    return [report.summary() for report, _ in results]


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}


def book_editions(book_root: Path) -> list[tuple[Path, str]]:
    state = read_json(book_root / "state" / "pipeline_state.json")
    editions: list[tuple[Path, str]] = []
    for item in state.get("output_editions") or []:
        if isinstance(item, dict) and item.get("enabled") is True:
            artifact = book_root / str(item.get("artifact") or "output/book.epub")
            if artifact.is_file():
                editions.append((artifact, str(item.get("edition_type") or "target_only")))
    if not editions:
        for name, edition in (("output/book.epub", "target_only"), ("output/book_bilingual_parallel.epub", "bilingual_parallel")):
            if (book_root / name).is_file():
                editions.append((book_root / name, edition))
    return editions


VERSION_IN_NAME = re.compile(r"v(\d+)\.(\d+)\.(\d+)")


def newest_epubs_in(directory: Path) -> list[tuple[Path, str]]:
    """Fallback when a release state is missing or stale: the highest-version EPUBs, else the newest file."""
    epubs = sorted(directory.glob("*.epub"))
    versioned = [(tuple(int(x) for x in m.groups()), path) for path in epubs if (m := VERSION_IN_NAME.search(path.name))]
    if versioned:
        top = max(version for version, _ in versioned)
        return [(path, "") for version, path in versioned if version == top]
    return [(max(epubs, key=lambda path: path.stat().st_mtime), "")] if epubs else []


def library_editions(books_root: Path) -> list[list[tuple[Path, str]]]:
    """Latest release or private artifact EPUBs per book, grouped by book."""
    groups: list[list[tuple[Path, str]]] = []
    directories = sorted({path.parent for pattern in ("**/output/release/*.epub", "**/output/private_artifacts/*.epub")
                          for path in books_root.glob(pattern)})
    for directory in directories:
        if "node_modules" in directory.parts or "build" in directory.parts:
            continue
        state = read_json(directory / "release_state.json") or read_json(directory / "private_artifact_state.json")
        entries = state.get("latest_epubs") or state.get("latest_artifacts") or []
        names = [str(entry.get("epub") or entry.get("artifact") or "") for entry in entries if isinstance(entry, dict)]
        kinds = [str(entry.get("edition_type") or "") for entry in entries if isinstance(entry, dict)]
        if not names:
            single = state.get("latest_epub") or state.get("latest_artifact")
            names, kinds = ([str(single)], [""]) if single else ([], [])
        group = [(directory / Path(name).name, kind) for name, kind in zip(names, kinds) if name]
        group = [(path, kind) for path, kind in group if path.is_file()] or newest_epubs_in(directory)
        if group:
            groups.append(group)
    return groups


def write_report(path: Path, results: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    status = "FAIL" if any(item["status"] == "FAIL" for item in results) else "PASS"
    payload = {"schema_version": "1.0", "status": status, "results": results}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def print_summary(results: list[dict]) -> None:
    for item in results:
        rules = ", ".join(f"{rule}={count}" for rule, count in item["rule_counts"].items())
        line = f"{item['status']} errors={item['error_count']} warnings={item['warning_count']} {Path(item['epub']).name}"
        print(line + (f" [{rules}]" if rules else ""))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check finished EPUB files for reader-visible production residue.")
    parser.add_argument("--book-root", default=None, help="Book project root (defaults to the parent of scripts/).")
    parser.add_argument("--epub", action="append", default=[], help="EPUB file to check; repeatable. Overrides book discovery.")
    parser.add_argument("--library", default=None, help="Scan the latest release/private artifact EPUBs of every book under this directory.")
    parser.add_argument("--write-report", action="store_true", help=f"Write {DEFAULT_REPORT} under the book root.")
    parser.add_argument("--report", default=None, help="Explicit report path.")
    parser.add_argument("--warn-only", action="store_true", help="Exit 0 even when errors are found.")
    return parser.parse_args()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = parse_args()
    results: list[dict] = []
    book_root = Path(args.book_root).resolve() if args.book_root else DEFAULT_BOOK_ROOT
    if args.library:
        library_root = Path(args.library).resolve()
        for group in library_editions(library_root):
            results.extend(check_editions(group, library_root))
    elif args.epub:
        results = check_editions([(Path(value).resolve(), "") for value in args.epub])
    else:
        editions = book_editions(book_root)
        if not editions:
            print("ERROR: no built EPUB found; run the build first.")
            return 1
        results = check_editions(editions, book_root)
    if not results:
        print("ERROR: no EPUB was checked.")
        return 1
    report_path = Path(args.report).resolve() if args.report else (book_root / DEFAULT_REPORT if args.write_report else None)
    if report_path is not None:
        write_report(report_path, results)
    print_summary(results)
    failed = any(item["status"] == "FAIL" for item in results)
    return 0 if (args.warn_only or not failed) else 1


if __name__ == "__main__":
    raise SystemExit(main())
