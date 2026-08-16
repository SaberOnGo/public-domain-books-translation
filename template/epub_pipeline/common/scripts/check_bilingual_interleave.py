from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = "output/bilingual_interleave_check.json"
STAGING_DIRECTORY = "output/epub_work_bilingual/EPUB"
BILINGUAL_EPUB = "output/book_bilingual_parallel.epub"
ALIGNMENT_MAP = "qa/bilingual_parallel/alignment_map.json"

VOID_HTML_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}
NOTE_CLASS_TOKENS = {
    "bitext-note",
    "chapter-notes",
    "endnote",
    "endnotes",
    "footnote",
    "footnotes",
    "note",
    "note-unit",
    "notes",
    "rearnote",
    "rearnotes",
}
NOTE_TYPE_TOKENS = {
    "endnote",
    "endnotes",
    "footnote",
    "footnotes",
    "note",
    "notes",
    "rearnote",
    "rearnotes",
}


@dataclass
class Node:
    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    children: list["Node"] = field(default_factory=list)


@dataclass
class StructureStats:
    unit_count: int = 0
    body_unit_count: int = 0
    note_unit_count: int = 0
    source_wrapper_count: int = 0
    target_wrapper_count: int = 0
    chapter_note_section_count: int = 0
    source_note_ref_count: int = 0
    target_note_ref_count: int = 0
    source_endnote_count: int = 0
    target_endnote_count: int = 0
    source_content_block_count: int = 0
    target_content_block_count: int = 0
    max_source_content_blocks_per_unit: int = 0
    max_target_content_blocks_per_unit: int = 0
    max_consecutive_source_blocks: int = 0
    max_consecutive_target_blocks: int = 0

    def merge(self, other: "StructureStats") -> None:
        self.unit_count += other.unit_count
        self.body_unit_count += other.body_unit_count
        self.note_unit_count += other.note_unit_count
        self.source_wrapper_count += other.source_wrapper_count
        self.target_wrapper_count += other.target_wrapper_count
        self.chapter_note_section_count += other.chapter_note_section_count
        self.source_note_ref_count += other.source_note_ref_count
        self.target_note_ref_count += other.target_note_ref_count
        self.source_endnote_count += other.source_endnote_count
        self.target_endnote_count += other.target_endnote_count
        self.source_content_block_count += other.source_content_block_count
        self.target_content_block_count += other.target_content_block_count
        self.max_source_content_blocks_per_unit = max(
            self.max_source_content_blocks_per_unit,
            other.max_source_content_blocks_per_unit,
        )
        self.max_target_content_blocks_per_unit = max(
            self.max_target_content_blocks_per_unit,
            other.max_target_content_blocks_per_unit,
        )
        self.max_consecutive_source_blocks = max(
            self.max_consecutive_source_blocks,
            other.max_consecutive_source_blocks,
        )
        self.max_consecutive_target_blocks = max(
            self.max_consecutive_target_blocks,
            other.max_consecutive_target_blocks,
        )


@dataclass
class InspectionResult:
    kind: str
    path: str
    file_count: int = 0
    parsed_file_count: int = 0
    xml_file_count: int = 0
    html_fallback_file_count: int = 0
    stats: StructureStats = field(default_factory=StructureStats)

    def as_report(self) -> dict:
        return {
            "kind": self.kind,
            "path": self.path,
            "file_count": self.file_count,
            "parsed_file_count": self.parsed_file_count,
            "xml_file_count": self.xml_file_count,
            "html_fallback_file_count": self.html_fallback_file_count,
            **asdict(self.stats),
        }


class StandardHTMLTreeBuilder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("__document__")
        self.stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Node(tag, {name: value or "" for name, value in attrs})
        self.stack[-1].children.append(node)
        if local_name(tag) not in VOID_HTML_ELEMENTS:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.stack[-1].children.append(Node(tag, {name: value or "" for name, value in attrs}))

    def handle_endtag(self, tag: str) -> None:
        wanted = local_name(tag)
        for index in range(len(self.stack) - 1, 0, -1):
            if local_name(self.stack[index].tag) == wanted:
                del self.stack[index:]
                return


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check direct source-target interleave in a bilingual EPUB.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--write-report", action="store_true", help=f"Write {DEFAULT_REPORT}.")
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def rel(book_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(book_root).as_posix()
    except ValueError:
        return str(path)


def add_issue(issues: list[dict], rule: str, path: str, detail: str) -> None:
    issues.append({"rule": rule, "path": path, "detail": detail})


def local_name(value: str) -> str:
    return value.rsplit("}", 1)[-1].rsplit(":", 1)[-1].lower()


def attribute(node: Node, wanted: str) -> str:
    wanted = wanted.lower()
    for name, value in node.attrs.items():
        if local_name(name) == wanted:
            return value
    return ""


def class_tokens(node: Node) -> set[str]:
    return {item.lower() for item in attribute(node, "class").split() if item}


def has_class(node: Node, class_name: str) -> bool:
    return class_name in class_tokens(node)


def from_xml(element: ElementTree.Element) -> Node:
    return Node(
        tag=str(element.tag),
        attrs={str(name): str(value) for name, value in element.attrib.items()},
        children=[from_xml(child) for child in list(element) if isinstance(child.tag, str)],
    )


def decode_markup(data: bytes) -> str:
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace")


def parse_markup(data: bytes) -> tuple[Node, str]:
    try:
        return Node("__document__", children=[from_xml(ElementTree.fromstring(data))]), "xml"
    except ElementTree.ParseError as xml_error:
        parser = StandardHTMLTreeBuilder()
        try:
            parser.feed(decode_markup(data))
            parser.close()
        except Exception as html_error:
            raise ValueError(f"XML parse failed ({xml_error}); HTML parse failed ({html_error})") from html_error
        if not parser.root.children:
            raise ValueError(f"XML parse failed ({xml_error}); HTML parser found no elements") from xml_error
        return parser.root, "html"


def iter_nodes(
    root: Node,
    ancestors: tuple[Node, ...] = (),
) -> Iterable[tuple[Node, Node | None, tuple[Node, ...]]]:
    for child in root.children:
        yield child, root, ancestors
        yield from iter_nodes(child, ancestors + (child,))


def role_tokens(node: Node) -> tuple[bool, bool]:
    tokens = class_tokens(node)
    return "bitext-source" in tokens, "bitext-target" in tokens


def direct_role_sequence(unit: Node) -> tuple[list[str], int, int]:
    roles: list[str] = []
    source_count = 0
    target_count = 0
    for child in unit.children:
        is_source, is_target = role_tokens(child)
        source_count += int(is_source)
        target_count += int(is_target)
        if is_source and is_target:
            roles.append("source+target")
        elif is_source:
            roles.append("source")
        elif is_target:
            roles.append("target")
    return roles, source_count, target_count


def longest_run(roles: list[str], wanted: str) -> int:
    longest = 0
    current = 0
    for role in roles:
        if role == wanted:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def is_note_unit(unit: Node, ancestors: tuple[Node, ...]) -> bool:
    for node in (*ancestors, unit):
        if class_tokens(node) & NOTE_CLASS_TOKENS:
            return True
        node_id = attribute(node, "id").lower()
        if node_id == "notes" or node_id.startswith(("note-", "footnote-", "endnote-")):
            return True
        for name, value in node.attrs.items():
            if local_name(name) not in {"type", "role", "data-kind", "data-unit-kind", "data-unit-type"}:
                continue
            if {item.lower() for item in value.split()} & NOTE_TYPE_TOKENS:
                return True
    return False


def unit_label(unit: Node, index: int) -> str:
    return attribute(unit, "data-align-id") or attribute(unit, "id") or f"unit[{index}]"


def inspect_document(data: bytes, path: str, issues: list[dict]) -> tuple[StructureStats, str]:
    root, parser_kind = parse_markup(data)
    entries = list(iter_nodes(root))
    units = [(node, ancestors) for node, _parent, ancestors in entries if has_class(node, "bitext-unit")]
    unit_nodes = {id(node) for node, _ancestors in units}
    stats = StructureStats(unit_count=len(units))

    for node, parent, ancestors in entries:
        is_source, is_target = role_tokens(node)
        stats.source_wrapper_count += int(is_source)
        stats.target_wrapper_count += int(is_target)
        if has_class(node, "chapter-notes"):
            stats.chapter_note_section_count += 1
        role_container = next(
            (item for item in reversed(ancestors) if any(role_tokens(item))),
            None,
        )
        if role_container is not None and has_class(node, "note-ref"):
            in_source, in_target = role_tokens(role_container)
            stats.source_note_ref_count += int(in_source)
            stats.target_note_ref_count += int(in_target)
        if role_container is not None and has_class(node, "endnote") and not has_class(node, "note-gap"):
            in_source, in_target = role_tokens(role_container)
            stats.source_endnote_count += int(in_source)
            stats.target_endnote_count += int(in_target)
        if not (is_source or is_target):
            continue
        if is_source and is_target:
            add_issue(
                issues,
                "ambiguous_bilingual_content_block",
                path,
                "An element cannot have both bitext-source and bitext-target classes.",
            )
        containing_unit = next((item for item in reversed(ancestors) if id(item) in unit_nodes), None)
        if containing_unit is None:
            add_issue(
                issues,
                "orphan_bilingual_content_block",
                path,
                "Every bitext-source and bitext-target block must belong to a bitext-unit.",
            )
        elif parent is not containing_unit:
            add_issue(
                issues,
                "indirect_bilingual_content_block",
                path,
                "bitext-source and bitext-target blocks must be direct children of their bitext-unit.",
            )

    for index, (unit, ancestors) in enumerate(units, start=1):
        label = unit_label(unit, index)
        issue_path = f"{path}#{label}"
        roles, source_count, target_count = direct_role_sequence(unit)
        source_wrappers = [child for child in unit.children if role_tokens(child)[0]]
        target_wrappers = [child for child in unit.children if role_tokens(child)[1]]
        source_content_count = sum(len(wrapper.children) for wrapper in source_wrappers)
        target_content_count = sum(len(wrapper.children) for wrapper in target_wrappers)
        stats.source_content_block_count += source_content_count
        stats.target_content_block_count += target_content_count
        if is_note_unit(unit, ancestors):
            stats.note_unit_count += 1
        else:
            stats.body_unit_count += 1

        stats.max_source_content_blocks_per_unit = max(
            stats.max_source_content_blocks_per_unit,
            source_content_count,
        )
        stats.max_target_content_blocks_per_unit = max(
            stats.max_target_content_blocks_per_unit,
            target_content_count,
        )
        stats.max_consecutive_source_blocks = max(
            stats.max_consecutive_source_blocks,
            longest_run(roles, "source"),
        )
        stats.max_consecutive_target_blocks = max(
            stats.max_consecutive_target_blocks,
            longest_run(roles, "target"),
        )

        if source_count > 1:
            add_issue(
                issues,
                "multiple_direct_source_blocks",
                issue_path,
                f"A bitext-unit may contain at most one direct bitext-source block; found {source_count}.",
            )
        if target_count > 1:
            add_issue(
                issues,
                "multiple_direct_target_blocks",
                issue_path,
                f"A bitext-unit may contain at most one direct bitext-target block; found {target_count}.",
            )
        if roles != ["source", "target"]:
            rendered_roles = ", ".join(roles) if roles else "<none>"
            add_issue(
                issues,
                "invalid_direct_source_target_order",
                issue_path,
                "Direct bilingual content blocks must be exactly source then target; "
                f"found [{rendered_roles}].",
            )
        if source_content_count != 1:
            add_issue(
                issues,
                "invalid_source_content_block_count",
                issue_path,
                f"The source wrapper must contain exactly one direct content block; found {source_content_count}.",
            )
        if target_content_count != 1:
            add_issue(
                issues,
                "invalid_target_content_block_count",
                issue_path,
                f"The target wrapper must contain exactly one direct content block; found {target_content_count}.",
            )

    if stats.source_content_block_count != stats.target_content_block_count:
        add_issue(
            issues,
            "uneven_source_target_block_count",
            path,
            f"source blocks ({stats.source_content_block_count}) must equal target blocks "
            f"({stats.target_content_block_count}).",
        )
    return stats, parser_kind


def inspect_payload(
    result: InspectionResult,
    data: bytes,
    path: str,
    issues: list[dict],
) -> None:
    try:
        stats, parser_kind = inspect_document(data, path, issues)
    except ValueError as exc:
        add_issue(issues, "unparseable_bilingual_markup", path, str(exc))
        return
    result.parsed_file_count += 1
    if parser_kind == "xml":
        result.xml_file_count += 1
    else:
        result.html_fallback_file_count += 1
    result.stats.merge(stats)


def inspect_staging(book_root: Path, issues: list[dict]) -> InspectionResult:
    root = book_root / STAGING_DIRECTORY
    result = InspectionResult(kind="staging", path=STAGING_DIRECTORY)
    if not root.is_dir():
        add_issue(issues, "missing_bilingual_staging", STAGING_DIRECTORY, "Missing bilingual EPUB staging directory.")
        return result
    files = sorted(
        path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in {".html", ".xhtml"}
    )
    result.file_count = len(files)
    if not files:
        add_issue(issues, "missing_staged_bilingual_markup", STAGING_DIRECTORY, "No XHTML or HTML files found.")
        return result
    for path in files:
        display_path = rel(book_root, path)
        try:
            data = path.read_bytes()
        except OSError as exc:
            add_issue(issues, "unreadable_staged_bilingual_markup", display_path, str(exc))
            continue
        inspect_payload(result, data, display_path, issues)
    return result


def inspect_epub(book_root: Path, issues: list[dict]) -> InspectionResult:
    epub_path = book_root / BILINGUAL_EPUB
    result = InspectionResult(kind="epub", path=BILINGUAL_EPUB)
    if not epub_path.is_file():
        add_issue(issues, "missing_bilingual_epub", BILINGUAL_EPUB, "Missing bilingual EPUB artifact.")
        return result
    try:
        with ZipFile(epub_path) as archive:
            names = sorted(
                name for name in archive.namelist() if name.lower().endswith((".html", ".xhtml"))
            )
            result.file_count = len(names)
            if not names:
                add_issue(issues, "missing_epub_bilingual_markup", BILINGUAL_EPUB, "No XHTML or HTML files found.")
                return result
            for name in names:
                display_path = f"{BILINGUAL_EPUB}!/{name}"
                try:
                    data = archive.read(name)
                except (KeyError, OSError) as exc:
                    add_issue(issues, "unreadable_epub_bilingual_markup", display_path, str(exc))
                    continue
                inspect_payload(result, data, display_path, issues)
    except (BadZipFile, OSError) as exc:
        add_issue(issues, "invalid_bilingual_epub", BILINGUAL_EPUB, str(exc))
    return result


def target_only_class_counts(book_root: Path, issues: list[dict]) -> dict[str, int]:
    path = book_root / "output" / "book.epub"
    counts = {"note-ref": 0, "endnote": 0, "chapter-notes": 0}
    try:
        with ZipFile(path) as archive:
            for name in archive.namelist():
                if not name.lower().endswith((".html", ".xhtml")):
                    continue
                root, _kind = parse_markup(archive.read(name))
                for node, _parent, _ancestors in iter_nodes(root):
                    for class_name in counts:
                        if has_class(node, class_name) and not has_class(node, "note-gap"):
                            counts[class_name] += 1
    except (BadZipFile, OSError, ValueError) as exc:
        add_issue(issues, "invalid_target_only_epub", "output/book.epub", str(exc))
    return counts


def read_min_interleaved_units(book_root: Path, issues: list[dict]) -> int:
    state_path = book_root / "state" / "pipeline_state.json"
    state_display = "state/pipeline_state.json"
    if not state_path.is_file():
        add_issue(issues, "missing_pipeline_state", state_display, "Missing pipeline state file.")
        return 1
    try:
        state = json.loads(state_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        add_issue(issues, "invalid_pipeline_state", state_display, str(exc))
        return 1
    if not isinstance(state, dict):
        add_issue(issues, "invalid_pipeline_state", state_display, "Pipeline state must be a JSON object.")
        return 1
    bilingual = state.get("bilingual_parallel")
    if bilingual is None:
        return 1
    if not isinstance(bilingual, dict):
        add_issue(
            issues,
            "invalid_bilingual_parallel_state",
            state_display,
            "bilingual_parallel must be a JSON object.",
        )
        return 1
    value = bilingual.get("min_interleaved_units", 1)
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        add_issue(
            issues,
            "invalid_min_interleaved_units",
            state_display,
            "bilingual_parallel.min_interleaved_units must be an integer greater than or equal to 1.",
        )
        return 1
    return value


def read_bilingual_enabled(book_root: Path, issues: list[dict]) -> bool:
    path = book_root / "state" / "pipeline_state.json"
    try:
        state = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        add_issue(issues, "invalid_pipeline_state", "state/pipeline_state.json", str(exc))
        return False
    if not isinstance(state, dict):
        return False
    if state.get("edition_type") == "bilingual_parallel":
        return True
    bilingual = state.get("bilingual_parallel")
    if isinstance(bilingual, dict) and bilingual.get("enabled") is True:
        return True
    return any(
        isinstance(item, dict)
        and item.get("enabled") is True
        and item.get("edition_type") == "bilingual_parallel"
        for item in state.get("output_editions", [])
    )


def read_alignment_unit_count(book_root: Path, issues: list[dict]) -> int:
    path = book_root / ALIGNMENT_MAP
    if not path.is_file():
        add_issue(issues, "missing_alignment_map", ALIGNMENT_MAP, "Missing bilingual alignment map.")
        return 0
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        add_issue(issues, "invalid_alignment_map", ALIGNMENT_MAP, str(exc))
        return 0
    units = data.get("alignment_units") if isinstance(data, dict) else None
    if not isinstance(units, list) or not units:
        add_issue(issues, "invalid_alignment_units", ALIGNMENT_MAP, "alignment_units must be a non-empty list.")
        return 0
    unmatched = {"source": 0, "target": 0}
    for index, unit in enumerate(units, start=1):
        if not isinstance(unit, dict):
            add_issue(issues, "invalid_alignment_unit", ALIGNMENT_MAP, f"alignment_units[{index}] is not an object.")
            continue
        side = str(unit.get("unmatched_side") or "")
        if not side:
            continue
        if unit.get("unit_type") != "note" or side not in unmatched:
            add_issue(
                issues,
                "invalid_unmatched_alignment_unit",
                ALIGNMENT_MAP,
                f"{unit.get('id') or index} has unsupported unmatched_side={side!r}.",
            )
            continue
        if not str(unit.get("exception_reason") or "").strip():
            add_issue(
                issues,
                "missing_note_alignment_exception_reason",
                ALIGNMENT_MAP,
                f"{unit.get('id') or index} lacks exception_reason.",
            )
        unmatched[side] += 1
    metrics = data.get("metrics") if isinstance(data, dict) else None
    if isinstance(metrics, dict):
        expected = {
            "source": metrics.get("unmatched_source_notes"),
            "target": metrics.get("unmatched_target_notes"),
        }
        for side in unmatched:
            if unmatched[side] != expected[side]:
                add_issue(
                    issues,
                    "note_alignment_exception_count_mismatch",
                    ALIGNMENT_MAP,
                    f"{side} exceptions={unmatched[side]} metrics={expected[side]}.",
                )
    return len(units)


def check_minimum(result: InspectionResult, minimum: int, issues: list[dict]) -> None:
    if result.stats.unit_count < minimum:
        add_issue(
            issues,
            "insufficient_interleaved_units",
            result.path,
            f"Found {result.stats.unit_count} bitext units; required at least {minimum}.",
        )


def check_exact_artifact(result: InspectionResult, alignment_units: int, issues: list[dict]) -> None:
    stats = result.stats
    if alignment_units and stats.unit_count != alignment_units:
        add_issue(
            issues,
            "stale_or_incomplete_bilingual_artifact",
            result.path,
            f"Found {stats.unit_count} bitext units; alignment map requires exactly {alignment_units}.",
        )
    for side, count in (("source", stats.source_wrapper_count), ("target", stats.target_wrapper_count)):
        if count != stats.unit_count:
            add_issue(
                issues,
                f"uneven_{side}_wrapper_count",
                result.path,
                f"Found {count} {side} wrappers for {stats.unit_count} bitext units.",
            )


def check_target_note_parity(
    result: InspectionResult,
    target_only: dict[str, int],
    issues: list[dict],
) -> None:
    comparisons = (
        ("note-ref", result.stats.target_note_ref_count),
        ("endnote", result.stats.target_endnote_count),
        ("chapter-notes", result.stats.chapter_note_section_count),
    )
    for class_name, actual in comparisons:
        expected = target_only[class_name]
        if actual != expected:
            add_issue(
                issues,
                "target_note_structure_regression",
                result.path,
                f"Bilingual target {class_name} count is {actual}; target-only EPUB requires {expected}.",
            )


def main() -> int:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    issues: list[dict] = []
    minimum = read_min_interleaved_units(book_root, issues)
    enabled = read_bilingual_enabled(book_root, issues)
    if not enabled and not issues:
        report = {"book_root": ".", "ok": True, "bilingual_enabled": False, "issues": []}
        if args.write_report:
            report_path = book_root / DEFAULT_REPORT
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("bilingual interleave gate PASS: bilingual edition disabled")
        return 0
    alignment_units = read_alignment_unit_count(book_root, issues)
    target_only_notes = target_only_class_counts(book_root, issues)
    staging = inspect_staging(book_root, issues)
    epub = inspect_epub(book_root, issues)
    check_minimum(staging, minimum, issues)
    check_minimum(epub, minimum, issues)
    check_exact_artifact(staging, alignment_units, issues)
    check_exact_artifact(epub, alignment_units, issues)
    check_target_note_parity(staging, target_only_notes, issues)
    check_target_note_parity(epub, target_only_notes, issues)

    combined = StructureStats()
    combined.merge(staging.stats)
    combined.merge(epub.stats)
    if combined.source_content_block_count != combined.target_content_block_count:
        add_issue(
            issues,
            "uneven_combined_source_target_block_count",
            ".",
            f"source blocks ({combined.source_content_block_count}) must equal target blocks "
            f"({combined.target_content_block_count}).",
        )

    report = {
        "book_root": ".",
        "ok": not issues,
        "bilingual_enabled": enabled,
        "min_interleaved_units": minimum,
        "alignment_units": alignment_units,
        "target_only_note_counts": target_only_notes,
        **asdict(combined),
        "inspections": [staging.as_report(), epub.as_report()],
        "issues": issues,
    }
    if args.write_report:
        report_path = book_root / DEFAULT_REPORT
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if issues:
        for issue in issues[:80]:
            print(f"ERROR {issue['rule']}: {issue['path']} {issue['detail']}")
        if len(issues) > 80:
            print(f"... {len(issues) - 80} more issues")
        print(
            "bilingual interleave gate FAIL: "
            f"issues={len(issues)} unit_count={combined.unit_count} "
            f"source_blocks={combined.source_content_block_count} "
            f"target_blocks={combined.target_content_block_count}"
        )
        return 1

    print(
        "bilingual interleave gate PASS: "
        f"alignment_units={alignment_units} min_interleaved_units={minimum} "
        f"staging_units={staging.stats.unit_count} epub_units={epub.stats.unit_count} "
        f"unit_count={combined.unit_count} body_unit_count={combined.body_unit_count} "
        f"note_unit_count={combined.note_unit_count} "
        f"source_blocks={combined.source_content_block_count} "
        f"target_blocks={combined.target_content_block_count} "
        f"max_source_content_blocks_per_unit={combined.max_source_content_blocks_per_unit} "
        f"max_target_content_blocks_per_unit={combined.max_target_content_blocks_per_unit} "
        f"max_consecutive_source_blocks={combined.max_consecutive_source_blocks} "
        f"max_consecutive_target_blocks={combined.max_consecutive_target_blocks}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
