from __future__ import annotations

import html
import json
import re
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any
from xml.etree import ElementTree as ET


CONTAINER_NS = "urn:oasis:names:tc:opendocument:xmlns:container"
OPF_NS = "http://www.idpf.org/2007/opf"
XHTML_NS = "http://www.w3.org/1999/xhtml"
OPS_NS = "http://www.idpf.org/2007/ops"
DC_NS = "http://purl.org/dc/elements/1.1/"

ET.register_namespace("", OPF_NS)
ET.register_namespace("dc", DC_NS)
ET.register_namespace("epub", OPS_NS)


@dataclass(frozen=True)
class DigestConfig:
    enabled: bool | None
    merge_into_epub: bool
    source_epub: Path
    output_epub: Path
    title: str
    max_section_chars: int
    language: str | None


@dataclass(frozen=True)
class EpubPaths:
    package_path: str
    package_dir: PurePosixPath
    nav_path: str


@dataclass(frozen=True)
class SectionDigest:
    title: str
    href: str
    summary: str


@dataclass(frozen=True)
class AutoDecision:
    generate: bool
    category: str
    reason: str


def run_digest(book_root: str | Path) -> dict[str, Any]:
    root = Path(book_root).resolve()
    config = load_config(root)
    if config.enabled is False:
        return {"status": "SKIPPED", "reason": "disabled", "merged": False}

    if config.merge_into_epub and config.source_epub == config.output_epub:
        raise ValueError("Digest output_epub must not overwrite source_epub")

    sections = read_epub_sections(config.source_epub, config.max_section_chars)
    language = config.language or read_epub_language(config.source_epub) or "und"
    book_title = read_epub_title(config.source_epub)
    auto_decision = AutoDecision(True, "forced", "enabled_by_config")
    if config.enabled is None:
        auto_decision = decide_auto_digest(book_title, sections)
        if not auto_decision.generate:
            return {
                "status": "SKIPPED",
                "reason": "auto_policy_excluded",
                "merged": False,
                "auto_decision": "skipped",
                "auto_category": auto_decision.category,
                "auto_reason": auto_decision.reason,
            }

    topology = build_topology(sections)
    knowledge_graph = build_knowledge_graph(book_title or config.title, sections)
    digest_xhtml = render_digest_xhtml(config.title, sections, language, topology, knowledge_graph)

    digest_dir = root / "output" / "digest"
    qa_dir = root / "qa" / "digest"
    digest_dir.mkdir(parents=True, exist_ok=True)
    qa_dir.mkdir(parents=True, exist_ok=True)
    agent_manifest = write_agent_packets(digest_dir, config, book_title, sections)
    review_checklist = render_review_checklist(config, sections, auto_decision)
    (digest_dir / "digest.xhtml").write_text(digest_xhtml, "utf-8")
    (digest_dir / "knowledge_map.svg").write_text(
        render_knowledge_map_svg(knowledge_graph),
        "utf-8",
    )
    (qa_dir / "digest_review_checklist.md").write_text(review_checklist, "utf-8")
    (digest_dir / "digest_state.json").write_text(
        json.dumps(
            {
                "status": "PASS",
                "source_epub": relpath(config.source_epub, root),
                "merge_into_epub": config.merge_into_epub,
                "title": config.title,
                "book_title": book_title,
                "language": language,
                "sections": [section.__dict__ for section in sections],
                "topology": topology,
                "knowledge_graph": knowledge_graph,
                "agent_packet_manifest": agent_manifest,
                "auto_decision": "generated" if config.enabled is None else "forced",
                "auto_category": auto_decision.category,
                "auto_reason": auto_decision.reason,
            },
            ensure_ascii=False,
            indent=2,
        ),
        "utf-8",
    )

    merged = False
    if config.merge_into_epub:
        merge_digest_chapter(
            source_epub=config.source_epub,
            output_epub=config.output_epub,
            digest_xhtml=digest_xhtml,
            title=config.title,
        )
        merged = True

    report = {
        "status": "PASS",
        "merged": merged,
        "source_epub": relpath(config.source_epub, root),
        "output_epub": relpath(config.output_epub, root) if merged else "",
        "digest_xhtml": "output/digest/digest.xhtml",
        "knowledge_map": "output/digest/knowledge_map.svg",
        "agent_packet_manifest": "output/digest/agent_packets/manifest.json",
        "review_checklist": "qa/digest/digest_review_checklist.md",
        "section_count": len(sections),
        "auto_decision": "generated" if config.enabled is None else "forced",
        "auto_category": auto_decision.category,
        "auto_reason": auto_decision.reason,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    (qa_dir / "digest_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        "utf-8",
    )
    return report


def load_config(root: Path) -> DigestConfig:
    path = root / "digest.config.json"
    data: dict[str, Any] = {}
    if path.exists():
        data = json.loads(path.read_text("utf-8"))
    enabled = parse_enabled(data.get("enabled", None if not path.exists() else False))

    source_epub = root / data.get("source_epub", "output/book.epub")
    output_epub = root / data.get("output_epub", "output/book_digest.epub")
    return DigestConfig(
        enabled=enabled,
        merge_into_epub=bool(data.get("merge_into_epub", False)),
        source_epub=source_epub.resolve(),
        output_epub=output_epub.resolve(),
        title=str(data.get("title", "全书导读")),
        max_section_chars=int(data.get("max_section_chars", 240)),
        language=normalize_optional_string(data.get("language")),
    )


def parse_enabled(value: Any) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized == "auto":
        return None
    return normalized in {"1", "true", "yes", "on", "enabled"}


def normalize_optional_string(value: Any) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None


def read_epub_sections(epub_path: Path, max_chars: int) -> list[SectionDigest]:
    if not epub_path.exists():
        raise FileNotFoundError(f"Missing EPUB: {epub_path}")

    with zipfile.ZipFile(epub_path) as archive:
        paths = read_epub_paths(archive)
        package = ET.fromstring(archive.read(paths.package_path))
        manifest = manifest_href_by_id(package)
        sections: list[SectionDigest] = []
        for itemref in package.findall(f"{{{OPF_NS}}}spine/{{{OPF_NS}}}itemref"):
            idref = itemref.attrib.get("idref")
            href = manifest.get(idref or "")
            if not href or not href.endswith((".xhtml", ".html")):
                continue
            archive_path = (paths.package_dir / href).as_posix()
            if archive_path not in archive.namelist():
                continue
            title, text = read_xhtml_title_and_text(archive.read(archive_path))
            summary = summarize_text(text, max_chars)
            if summary:
                sections.append(SectionDigest(title=title or href, href=href, summary=summary))
        return sections


def read_epub_language(epub_path: Path) -> str | None:
    if not epub_path.exists():
        return None
    with zipfile.ZipFile(epub_path) as archive:
        paths = read_epub_paths(archive)
        package = ET.fromstring(archive.read(paths.package_path))
        for element in package.findall(f"{{{OPF_NS}}}metadata/{{{DC_NS}}}language"):
            text = normalize_space("".join(element.itertext()))
            if text:
                return text
    return None


def read_epub_title(epub_path: Path) -> str:
    if not epub_path.exists():
        return ""
    with zipfile.ZipFile(epub_path) as archive:
        paths = read_epub_paths(archive)
        package = ET.fromstring(archive.read(paths.package_path))
        for element in package.findall(f"{{{OPF_NS}}}metadata/{{{DC_NS}}}title"):
            text = normalize_space("".join(element.itertext()))
            if text:
                return text
    return ""


def decide_auto_digest(book_title: str, sections: list[SectionDigest]) -> AutoDecision:
    title = book_title.lower()
    if any(token in title for token in ["短篇", "short story", "short stories", "自然科学", "自然科學", "natural science"]):
        return AutoDecision(False, "excluded", "short_story_or_natural_science")
    if any(token in title for token in ["长篇", "長篇", "novel", "专业", "專業", "specialist", "哲学", "哲學", "philosophy"]):
        return AutoDecision(True, "eligible", "title_matches_digest_book_type")
    if len(sections) >= 4:
        return AutoDecision(True, "eligible", "chapter_count_suggests_long_book")
    return AutoDecision(False, "excluded", "not_long_novel_specialist_or_philosophy")


def read_epub_paths(archive: zipfile.ZipFile) -> EpubPaths:
    container = ET.fromstring(archive.read("META-INF/container.xml"))
    rootfile = container.find(f".//{{{CONTAINER_NS}}}rootfile")
    if rootfile is None:
        raise ValueError("EPUB container does not declare a rootfile")
    package_path = rootfile.attrib["full-path"]
    package_dir = PurePosixPath(package_path).parent
    package = ET.fromstring(archive.read(package_path))
    nav_href = None
    for item in package.findall(f"{{{OPF_NS}}}manifest/{{{OPF_NS}}}item"):
        properties = set(item.attrib.get("properties", "").split())
        if "nav" in properties:
            nav_href = item.attrib.get("href")
            break
    if not nav_href:
        raise ValueError("EPUB package does not declare a nav document")
    return EpubPaths(
        package_path=package_path,
        package_dir=package_dir,
        nav_path=(package_dir / nav_href).as_posix(),
    )


def manifest_href_by_id(package: ET.Element) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in package.findall(f"{{{OPF_NS}}}manifest/{{{OPF_NS}}}item"):
        item_id = item.attrib.get("id")
        href = item.attrib.get("href")
        if item_id and href:
            result[item_id] = href
    return result


def read_xhtml_title_and_text(content: bytes) -> tuple[str, str]:
    root = ET.fromstring(content)
    title = first_text(root, "h1") or first_text(root, "title")
    parts: list[str] = []
    for element in root.iter():
        if local_name(element.tag) in {"p", "li", "blockquote", "figcaption"}:
            text = normalize_space("".join(element.itertext()))
            if text:
                parts.append(text)
    return normalize_space(title), normalize_space(" ".join(parts))


def first_text(root: ET.Element, local: str) -> str:
    for element in root.iter():
        if local_name(element.tag) == local:
            return normalize_space("".join(element.itertext()))
    return ""


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def summarize_text(text: str, max_chars: int) -> str:
    text = normalize_space(text)
    if len(text) <= max_chars:
        return text
    return f"{text[:max_chars].rstrip()}..."


def render_digest_xhtml(
    title: str,
    sections: list[SectionDigest],
    language: str,
    topology: dict[str, Any],
    knowledge_graph: dict[str, Any],
) -> str:
    topology_map = render_topology_svg(topology)
    knowledge_map = render_knowledge_map_svg(knowledge_graph)
    items = "\n".join(
        f"""    <section class="digest-section">
      <h2>{escape(section.title)}</h2>
      <p>{escape(section.summary)}</p>
    </section>"""
        for section in sections
    )
    if not items:
        items = "    <p>本书没有可提取的章节摘要。</p>"
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{escape(language)}" lang="{escape(language)}">
<head>
  <meta charset="utf-8" />
  <title>{escape(title)}</title>
</head>
<body>
  <section epub:type="bodymatter" class="lifebook-digest">
    <h1>{escape(title)}</h1>
    <section class="digest-topology">
      <h2>章节拓扑</h2>
{topology_map}
    </section>
    <section class="digest-knowledge-map">
      <h2>知识脉络图</h2>
{knowledge_map}
    </section>
    <section class="digest-summaries">
      <h2>章节摘要</h2>
{items}
    </section>
  </section>
</body>
</html>
"""


def build_topology(sections: list[SectionDigest]) -> dict[str, Any]:
    nodes = [
        {
            "id": f"section-{index}",
            "title": section.title,
            "href": section.href,
        }
        for index, section in enumerate(sections, start=1)
    ]
    edges = [
        {
            "source": nodes[index]["id"],
            "target": nodes[index + 1]["id"],
            "kind": "reading_order",
        }
        for index in range(len(nodes) - 1)
    ]
    return {"nodes": nodes, "edges": edges}


def build_knowledge_graph(book_title: str, sections: list[SectionDigest]) -> dict[str, Any]:
    root_id = "book"
    nodes: list[dict[str, str]] = [{"id": root_id, "label": book_title or "Book", "kind": "book"}]
    edges: list[dict[str, str]] = []
    seen_keywords: set[str] = set()
    for index, section in enumerate(sections, start=1):
        section_id = f"section-{index}"
        nodes.append({"id": section_id, "label": section.title, "kind": "section"})
        edges.append({"source": root_id, "target": section_id, "kind": "contains"})
        for keyword in extract_keywords(section.summary)[:2]:
            keyword_id = f"keyword-{slugify(keyword)}"
            if keyword_id not in seen_keywords:
                nodes.append({"id": keyword_id, "label": keyword, "kind": "keyword"})
                seen_keywords.add(keyword_id)
            edges.append({"source": section_id, "target": keyword_id, "kind": "theme"})
    return {"nodes": nodes, "edges": edges}


def extract_keywords(text: str) -> list[str]:
    words = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z][A-Za-z-]{3,}", text)
    stop_words = {
        "这是",
        "这个",
        "说明",
        "主要",
        "内容",
        "chapter",
        "section",
        "with",
        "from",
        "that",
        "this",
    }
    result: list[str] = []
    for word in words:
        normalized = word.strip()
        if not normalized or normalized.lower() in stop_words or normalized in stop_words:
            continue
        if normalized not in result:
            result.append(normalized)
    return result or ["核心主题"]


def slugify(text: str) -> str:
    ascii_text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    if ascii_text:
        return ascii_text
    return str(abs(hash(text)))


def render_topology_svg(topology: dict[str, Any]) -> str:
    nodes = topology.get("nodes", [])
    if not nodes:
        return ""
    row_height = 44
    width = 720
    height = 32 + row_height * len(nodes)
    rows: list[str] = []
    for index, node in enumerate(nodes, start=1):
        y = 24 + (index - 1) * row_height
        rows.append(
            f"""      <g>
        <circle cx="32" cy="{y}" r="10" />
        <text x="52" y="{y + 5}">{escape(str(index))}. {escape(str(node.get("title", "")))}</text>
      </g>"""
        )
        if index < len(nodes):
            rows.append(
                f"""      <line x1="32" y1="{y + 10}" x2="32" y2="{y + row_height - 10}" />"""
            )
    return f"""    <figure class="digest-map">
      <svg xmlns="http://www.w3.org/2000/svg" role="img" aria-label="章节拓扑" viewBox="0 0 {width} {height}">
        <title>章节拓扑</title>
        <style>circle{{fill:#2f5d62}}line{{stroke:#9aa6a6;stroke-width:2}}text{{font-size:18px;fill:#1f1f1f}}</style>
{chr(10).join(rows)}
      </svg>
      <figcaption>章节拓扑</figcaption>
    </figure>"""


def render_knowledge_map_svg(knowledge_graph: dict[str, Any]) -> str:
    nodes = knowledge_graph.get("nodes", [])
    edges = knowledge_graph.get("edges", [])
    if not nodes:
        return ""
    width = 760
    height = max(220, 80 + len(nodes) * 28)
    positions: dict[str, tuple[int, int]] = {}
    positions["book"] = (120, height // 2)
    section_nodes = [node for node in nodes if node.get("kind") == "section"]
    keyword_nodes = [node for node in nodes if node.get("kind") == "keyword"]
    for index, node in enumerate(section_nodes, start=1):
        positions[str(node["id"])] = (330, 48 + (index - 1) * 58)
    for index, node in enumerate(keyword_nodes, start=1):
        positions[str(node["id"])] = (590, 40 + (index - 1) * 36)

    lines: list[str] = []
    for edge in edges:
        source = positions.get(str(edge.get("source")))
        target = positions.get(str(edge.get("target")))
        if source and target:
            lines.append(f'      <line x1="{source[0]}" y1="{source[1]}" x2="{target[0]}" y2="{target[1]}" />')

    circles: list[str] = []
    for node in nodes:
        node_id = str(node.get("id"))
        x, y = positions.get(node_id, (120, 40))
        kind = node.get("kind")
        radius = 22 if kind == "book" else 16 if kind == "section" else 11
        label = escape(str(node.get("label", "")))
        circles.append(
            f"""      <g>
        <circle class="{escape(str(kind))}" cx="{x}" cy="{y}" r="{radius}" />
        <text x="{x + radius + 8}" y="{y + 5}">{label}</text>
      </g>"""
        )
    return f"""    <figure class="digest-knowledge-figure">
      <svg xmlns="http://www.w3.org/2000/svg" role="img" aria-label="知识脉络图" viewBox="0 0 {width} {height}">
        <title>知识脉络图</title>
        <style>line{{stroke:#a8b0b3;stroke-width:1.6}}circle.book{{fill:#2f5d62}}circle.section{{fill:#4f7f8c}}circle.keyword{{fill:#b08d57}}text{{font-size:16px;fill:#1f1f1f}}</style>
{chr(10).join(lines)}
{chr(10).join(circles)}
      </svg>
      <figcaption>知识脉络图</figcaption>
    </figure>"""


def write_agent_packets(
    digest_dir: Path,
    config: DigestConfig,
    book_title: str,
    sections: list[SectionDigest],
) -> dict[str, Any]:
    packet_dir = digest_dir / "agent_packets"
    packet_dir.mkdir(parents=True, exist_ok=True)
    packet_path = packet_dir / "000_digest_generation.md"
    section_lines = "\n".join(
        f"## {index}. {section.title}\n\nSource href: `{section.href}`\n\nExcerpt:\n{section.summary}\n"
        for index, section in enumerate(sections, start=1)
    )
    packet_path.write_text(
        f"""# LifeBook Digest Agent Packet

Book title: {book_title or config.title}
Digest title: {config.title}

请基于下面的章节摘录，为读者生成可审校的 Digest 草稿：

- 全书核心问题：3-6 条。
- 章节拓扑：按阅读顺序说明章节之间的推进关系。
- 知识脉络图：提取主题节点、人物/概念节点和关系边。
- 章节摘要：每章 1 段，不要添加原文没有的信息。
- 风险标记：指出需要人工复核的概括、术语或事实。

不要输出制作日志、prompt 痕迹、本地绝对路径或未审校声明。最终发布文本必须经过 `qa/digest/digest_review_checklist.md`。

{section_lines}
""",
        "utf-8",
    )
    manifest = {
        "packets": [
            {
                "id": "000_digest_generation",
                "path": "output/digest/agent_packets/000_digest_generation.md",
                "section_count": len(sections),
            }
        ],
        "review_checklist": "qa/digest/digest_review_checklist.md",
    }
    (packet_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), "utf-8")
    return manifest


def render_review_checklist(
    config: DigestConfig,
    sections: list[SectionDigest],
    auto_decision: AutoDecision,
) -> str:
    return f"""# LifeBook Digest QA Checklist

- Digest title: {config.title}
- Section count: {len(sections)}
- Auto decision: {auto_decision.category} / {auto_decision.reason}

## 必查项

- [ ] Digest 只作为 post-EPUB optional step 生成，没有改写原正文、封面、book-info 或前置页。
- [ ] 若合并进 EPUB，OPF manifest、spine、nav 已更新，并重新运行 EPUBCheck。
- [ ] Digest 章节没有 prompt、制作日志、本地绝对路径、QA 草稿或未审校声明。
- [ ] 章节摘要没有虚构原文没有的信息。
- [ ] 章节拓扑与原 EPUB 阅读顺序一致。
- [ ] 知识脉络图的节点和关系可从原书或译文中找到依据。
- [ ] 若作为 release 发布，已按书籍工程规则生成新版本产物。
"""


def merge_digest_chapter(
    *,
    source_epub: Path,
    output_epub: Path,
    digest_xhtml: str,
    title: str,
) -> None:
    output_epub.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source_epub) as source:
        paths = read_epub_paths(source)
        package = ET.fromstring(source.read(paths.package_path))
        nav = ET.fromstring(source.read(paths.nav_path))
        digest_archive_path = (paths.package_dir / "text/lifebook-digest.xhtml").as_posix()
        digest_href = rel_from_package(paths.package_dir, digest_archive_path)
        ensure_manifest_item(package, "lifebook-digest", digest_href)
        ensure_spine_item(package, "lifebook-digest")
        ensure_nav_item(nav, digest_href, title)

        replacements = {
            paths.package_path: serialize_xml(package),
            paths.nav_path: serialize_xml(nav),
            digest_archive_path: digest_xhtml.encode("utf-8"),
        }
        write_epub_copy(source, output_epub, replacements)


def rel_from_package(package_dir: PurePosixPath, archive_path: str) -> str:
    package_parts = package_dir.parts
    path_parts = PurePosixPath(archive_path).parts
    if package_parts and path_parts[: len(package_parts)] == package_parts:
        return PurePosixPath(*path_parts[len(package_parts) :]).as_posix()
    return archive_path


def ensure_manifest_item(package: ET.Element, item_id: str, href: str) -> None:
    manifest = package.find(f"{{{OPF_NS}}}manifest")
    if manifest is None:
        raise ValueError("EPUB package manifest is missing")
    for item in manifest.findall(f"{{{OPF_NS}}}item"):
        if item.attrib.get("id") == item_id:
            item.set("href", href)
            item.set("media-type", "application/xhtml+xml")
            return
    ET.SubElement(
        manifest,
        f"{{{OPF_NS}}}item",
        {"id": item_id, "href": href, "media-type": "application/xhtml+xml"},
    )


def ensure_spine_item(package: ET.Element, item_id: str) -> None:
    spine = package.find(f"{{{OPF_NS}}}spine")
    if spine is None:
        raise ValueError("EPUB package spine is missing")
    for itemref in spine.findall(f"{{{OPF_NS}}}itemref"):
        if itemref.attrib.get("idref") == item_id:
            return
    ET.SubElement(spine, f"{{{OPF_NS}}}itemref", {"idref": item_id})


def ensure_nav_item(nav: ET.Element, href: str, title: str) -> None:
    toc = find_toc_nav(nav)
    if toc is None:
        raise ValueError("EPUB nav document does not contain a toc nav")
    ordered = first_child(toc, "ol")
    if ordered is None:
        ordered = ET.SubElement(toc, f"{{{XHTML_NS}}}ol")
    for link in ordered.findall(f".//{{{XHTML_NS}}}a"):
        if link.attrib.get("href") == href:
            link.text = title
            return
    li = ET.SubElement(ordered, f"{{{XHTML_NS}}}li")
    link = ET.SubElement(li, f"{{{XHTML_NS}}}a", {"href": href})
    link.text = title


def find_toc_nav(root: ET.Element) -> ET.Element | None:
    for element in root.iter():
        if local_name(element.tag) != "nav":
            continue
        epub_type = element.attrib.get(f"{{{OPS_NS}}}type") or element.attrib.get("epub:type")
        if epub_type and "toc" in epub_type.split():
            return element
    return None


def first_child(root: ET.Element, local: str) -> ET.Element | None:
    for child in list(root):
        if local_name(child.tag) == local:
            return child
    return None


def serialize_xml(root: ET.Element) -> bytes:
    namespace = namespace_uri(root.tag)
    if namespace in {OPF_NS, XHTML_NS}:
        ET.register_namespace("", namespace)
    ET.register_namespace("dc", DC_NS)
    ET.register_namespace("epub", OPS_NS)
    return b'<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=False,
    )


def namespace_uri(tag: str) -> str:
    if tag.startswith("{") and "}" in tag:
        return tag[1:].split("}", 1)[0]
    return ""


def write_epub_copy(
    source: zipfile.ZipFile,
    output_epub: Path,
    replacements: dict[str, bytes | str],
) -> None:
    names = source.namelist()
    with zipfile.ZipFile(output_epub, "w") as target:
        if "mimetype" in names:
            target.writestr("mimetype", source.read("mimetype"), compress_type=zipfile.ZIP_STORED)
        for info in source.infolist():
            if info.filename == "mimetype":
                continue
            payload = replacements.pop(info.filename, None)
            target.writestr(info, encode_payload(payload) if payload is not None else source.read(info.filename))
        for name, payload in sorted(replacements.items()):
            target.writestr(name, encode_payload(payload), compress_type=zipfile.ZIP_DEFLATED)


def encode_payload(payload: bytes | str) -> bytes:
    return payload if isinstance(payload, bytes) else payload.encode("utf-8")


def escape(text: str) -> str:
    return html.escape(text, quote=True)


def relpath(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
