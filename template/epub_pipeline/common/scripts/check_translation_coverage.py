from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
TARGET_DIRS = ("chapters/translated", "chapters/final")

FOOTNOTE_REF_RE = re.compile(r"(?<!\!)\[\^([^\]\s]+)\]")
FOOTNOTE_DEF_RE = re.compile(r"(?m)^\s*\[\^([^\]\s]+)\]\s*[:：]")
LEGACY_NOTE_DEF_RE = re.compile(r"(?m)^\s*(\d+[A-Za-z]*)\s+\(return\)\s*\[")
UNNUMBERED_NOTE_DEF_RE = re.compile(r"(?m)^\s*((?:\*?\s*)?Note:\s+.+)$")
LEGACY_NOTE_REF_RE = re.compile(r"(?<![A-Za-z0-9])(\d+[a-z])(?=\s|[.,;:);\]])")
SQUARE_NOTE_REF_RE = re.compile(r"(?<!\!)\[(\d+)\]")
CHAPTER_ENDNOTE_SECTION_RE = re.compile(r'(?ms)<section\s+class="chapter-notes"(?:\s[^>]*)?>.*?</section>')
CHAPTER_ENDNOTE_DEF_RE = re.compile(r'(?m)\bid="note-(\d+)"')
CJK_CHAR_RE = re.compile(r"[\u3400-\u9FFF]")
LATIN_WORD_RE = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)|<img\b", re.IGNORECASE)
TABLE_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*tbl[^)]*\)", re.IGNORECASE)
FORMULA_BLOCK_RE = re.compile(
    r"(?ms)(^\s*\$\$.*?^\s*\$\$)|(^\s*\\\[.*?^\s*\\\])|\\begin\{(?:equation|align|gather|multline)[^}]*\}.*?\\end\{(?:equation|align|gather|multline)[^}]*\}"
)


@dataclass(frozen=True)
class ChapterMetrics:
    headings: int
    paragraph_blocks: int
    nonspace_chars: int
    note_refs: int
    note_defs: int
    tables: int
    images: int
    formulas: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check source-to-translation structural coverage for chapter Markdown. "
            "This catches severe AI output shrinkage and note loss before chapters can pass preflight."
        )
    )
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--write-report", action="store_true", help="Write output/translation_coverage.json.")
    parser.add_argument(
        "--source-dir",
        default="chapters/src",
        help="Source chapter directory relative to book root.",
    )
    parser.add_argument(
        "--target-dir",
        action="append",
        default=[],
        help="Target chapter directory relative to book root. May be repeated. Defaults to translated and final.",
    )
    parser.add_argument(
        "--min-paragraph-block-ratio",
        type=float,
        default=0.75,
        help="Minimum target/source paragraph-block ratio for chapters with at least 4 source blocks.",
    )
    parser.add_argument(
        "--min-char-ratio",
        type=float,
        default=0.35,
        help="Minimum target/source non-space character ratio for chapters with at least 800 source characters.",
    )
    parser.add_argument(
        "--min-note-coverage-ratio",
        type=float,
        default=1.0,
        help="Minimum target/source note reference and definition ratio when source notes exist.",
    )
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def rel(book_root: Path, path: Path) -> str:
    try:
        return path.relative_to(book_root).as_posix()
    except ValueError:
        return str(path)


def logical_scope(path: Path) -> str:
    stem = path.stem
    numeric = re.match(r"^(\d+)_", stem)
    if not numeric:
        return stem
    if int(numeric.group(1)) == 1:
        return stem
    return re.sub(r"_part_[A-Za-z0-9]+$", "", stem[numeric.end() :])


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def strip_footnote_definitions(text: str) -> str:
    normalized = CHAPTER_ENDNOTE_SECTION_RE.sub("", normalize_newlines(text))
    normalized = re.sub(r"(?m)^\s*##\s+本章注释\s*$\n?", "", normalized)
    blocks = re.split(r"\n[ \t]*\n", normalized)
    kept = []
    for block in blocks:
        first_line = next((line for line in block.splitlines() if line.strip()), "")
        if (
            FOOTNOTE_DEF_RE.match(first_line)
            or LEGACY_NOTE_DEF_RE.match(first_line)
            or UNNUMBERED_NOTE_DEF_RE.match(first_line)
        ):
            continue
        kept.append(block)
    return "\n\n".join(kept)


def strip_fenced_blocks(text: str) -> str:
    lines = []
    in_fence = False
    for line in normalize_newlines(text).splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return "\n".join(lines)


def note_keys_for(text: str) -> tuple[set[str], set[str]]:
    normalized = normalize_newlines(text)
    note_body = strip_footnote_definitions(normalized)
    refs = (
        set(FOOTNOTE_REF_RE.findall(note_body))
        | set(LEGACY_NOTE_REF_RE.findall(note_body))
        | set(SQUARE_NOTE_REF_RE.findall(note_body))
    )
    defs = (
        set(FOOTNOTE_DEF_RE.findall(normalized))
        | set(LEGACY_NOTE_DEF_RE.findall(normalized))
        | set(UNNUMBERED_NOTE_DEF_RE.findall(normalized))
        | set(CHAPTER_ENDNOTE_DEF_RE.findall(normalized))
    )
    return refs, defs


def translation_units_for(text: str) -> tuple[int, int]:
    body = strip_fenced_blocks(strip_footnote_definitions(text))
    return len(CJK_CHAR_RE.findall(body)) + len(LATIN_WORD_RE.findall(body)), len(CJK_CHAR_RE.findall(body))


def is_table_block(block: str) -> bool:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    return (
        len(lines) >= 2
        and lines[0].startswith("|")
        and lines[1].startswith("|")
        and bool(re.search(r"\|\s*:?-{3,}:?\s*\|", lines[1]))
    )


def is_reader_paragraph(block: str) -> bool:
    stripped = block.strip()
    if not stripped:
        return False
    if stripped.startswith("#"):
        return False
    if is_table_block(stripped):
        return False
    if IMAGE_RE.search(stripped):
        return False
    if FORMULA_BLOCK_RE.search(stripped):
        return False
    if FOOTNOTE_DEF_RE.match(stripped):
        return False
    text = re.sub(r"^[>\-\*\+\d.\s]+", "", stripped)
    return len(re.sub(r"\s+", "", text)) >= 20


def count_tables(text: str) -> int:
    lines = normalize_newlines(text).splitlines()
    count = 0
    index = 0
    while index + 1 < len(lines):
        current = lines[index].strip()
        separator = lines[index + 1].strip()
        if current.startswith("|") and separator.startswith("|") and bool(re.search(r"\|\s*:?-{3,}:?\s*\|", separator)):
            count += 1
            index += 2
            while index < len(lines) and lines[index].strip().startswith("|"):
                index += 1
            continue
        index += 1
    return count


def count_table_images(text: str) -> int:
    """Count raster table assets that may be replaced by an accessible Markdown table."""
    return len(TABLE_IMAGE_RE.findall(text))


def count_formulas(text: str) -> int:
    return len(FORMULA_BLOCK_RE.findall(normalize_newlines(text)))


def metrics_for(text: str) -> ChapterMetrics:
    normalized = normalize_newlines(text)
    body_for_blocks = strip_fenced_blocks(strip_footnote_definitions(normalized))
    note_refs, note_defs = note_keys_for(normalized)
    blocks = [block for block in body_for_blocks.split("\n\n") if is_reader_paragraph(block)]
    return ChapterMetrics(
        headings=len(re.findall(r"(?m)^\s{0,3}#{1,6}\s+\S", normalized)),
        paragraph_blocks=len(blocks),
        nonspace_chars=len(re.sub(r"\s+", "", body_for_blocks)),
        note_refs=len(note_refs),
        note_defs=len(note_defs),
        tables=count_tables(normalized),
        images=len(IMAGE_RE.findall(normalized)),
        formulas=count_formulas(normalized),
    )


def add_issue(issues: list[dict], rule: str, path: str, detail: str, source: ChapterMetrics, target: ChapterMetrics) -> None:
    issues.append(
        {
            "rule": rule,
            "path": path,
            "detail": detail,
            "source": asdict(source),
            "target": asdict(target),
        }
    )


def ratio(target: int, source: int) -> float:
    if source <= 0:
        return 1.0
    return target / source


def check_pair(
    *,
    book_root: Path,
    source_path: Path,
    target_path: Path,
    min_paragraph_block_ratio: float,
    min_char_ratio: float,
    min_note_coverage_ratio: float,
    issues: list[dict],
    chapters: list[dict],
) -> None:
    source_text = source_path.read_text(encoding="utf-8", errors="replace")
    target_text = target_path.read_text(encoding="utf-8", errors="replace")
    source_metrics = metrics_for(source_text)
    target_metrics = metrics_for(target_text)
    target_rel = rel(book_root, target_path)
    chapters.append(
        {
            "source_path": rel(book_root, source_path),
            "target_path": target_rel,
            "source": asdict(source_metrics),
            "target": asdict(target_metrics),
            "ratios": {
                "paragraph_blocks": round(ratio(target_metrics.paragraph_blocks, source_metrics.paragraph_blocks), 4),
                "nonspace_chars": round(ratio(target_metrics.nonspace_chars, source_metrics.nonspace_chars), 4),
                "note_refs": round(ratio(target_metrics.note_refs, source_metrics.note_refs), 4),
                "note_defs": round(ratio(target_metrics.note_defs, source_metrics.note_defs), 4),
            },
        }
    )

    paragraph_ratio = ratio(target_metrics.paragraph_blocks, source_metrics.paragraph_blocks)
    if source_metrics.paragraph_blocks >= 4 and paragraph_ratio < min_paragraph_block_ratio:
        add_issue(
            issues,
            "paragraph_block_coverage_low",
            target_rel,
            f"Target has {target_metrics.paragraph_blocks}/{source_metrics.paragraph_blocks} reader paragraph blocks; minimum ratio is {min_paragraph_block_ratio}.",
            source_metrics,
            target_metrics,
        )

    source_units, _ = translation_units_for(source_text)
    target_units, target_cjk_chars = translation_units_for(target_text)
    if target_cjk_chars >= 100:
        char_ratio = ratio(target_units, source_units)
        coverage_detail = (
            f"Target has {target_units}/{source_units} cross-language translation units "
            f"(raw non-space characters {target_metrics.nonspace_chars}/{source_metrics.nonspace_chars}); "
            f"minimum ratio is {min_char_ratio}."
        )
    else:
        char_ratio = ratio(target_metrics.nonspace_chars, source_metrics.nonspace_chars)
        coverage_detail = (
            f"Target has {target_metrics.nonspace_chars}/{source_metrics.nonspace_chars} non-space characters; "
            f"minimum ratio is {min_char_ratio}."
        )
    if source_metrics.nonspace_chars >= 800 and char_ratio < min_char_ratio:
        add_issue(
            issues,
            "chapter_char_coverage_low",
            target_rel,
            coverage_detail,
            source_metrics,
            target_metrics,
        )

    if source_metrics.tables and target_metrics.tables < source_metrics.tables:
        add_issue(
            issues,
            "table_coverage_low",
            target_rel,
            f"Target has {target_metrics.tables}/{source_metrics.tables} tables; source structural units may have been lost.",
            source_metrics,
            target_metrics,
        )

    source_table_images = count_table_images(source_text)
    target_table_images = count_table_images(target_text)
    replaced_table_images = max(0, source_table_images - target_table_images)
    if replaced_table_images and target_metrics.tables < replaced_table_images:
        add_issue(
            issues,
            "table_coverage_low",
            target_rel,
            f"Target has {target_metrics.tables} structured tables for {replaced_table_images} replaced raster table assets; source structural units may have been lost.",
            source_metrics,
            target_metrics,
        )

    source_non_table_images = max(0, source_metrics.images - source_table_images)
    target_non_table_images = max(0, target_metrics.images - target_table_images)
    if source_non_table_images and target_non_table_images < source_non_table_images:
        add_issue(
            issues,
            "image_coverage_low",
            target_rel,
            f"Target has {target_non_table_images}/{source_non_table_images} non-table images; source structural units may have been lost.",
            source_metrics,
            target_metrics,
        )

    if source_metrics.formulas and target_metrics.formulas < source_metrics.formulas:
        add_issue(
            issues,
            "formula_coverage_low",
            target_rel,
            f"Target has {target_metrics.formulas}/{source_metrics.formulas} formulas; source structural units may have been lost.",
            source_metrics,
            target_metrics,
        )


def check_note_scopes(
    *,
    book_root: Path,
    source_paths: list[Path],
    target_paths: list[Path],
    target_dir: str,
    min_note_coverage_ratio: float,
    issues: list[dict],
    note_scopes: list[dict],
) -> None:
    source_by_scope: dict[str, list[Path]] = {}
    target_by_scope: dict[str, list[Path]] = {}
    for path in source_paths:
        source_by_scope.setdefault(logical_scope(path), []).append(path)
    for path in target_paths:
        target_by_scope.setdefault(logical_scope(path), []).append(path)

    for scope in sorted(source_by_scope.keys() & target_by_scope.keys()):
        source_refs: set[str] = set()
        source_defs: set[str] = set()
        target_refs: set[str] = set()
        target_defs: set[str] = set()
        for path in source_by_scope[scope]:
            refs, defs = note_keys_for(path.read_text(encoding="utf-8", errors="replace"))
            source_refs.update(refs)
            source_defs.update(defs)
        for path in target_by_scope[scope]:
            refs, defs = note_keys_for(path.read_text(encoding="utf-8", errors="replace"))
            target_refs.update(refs)
            target_defs.update(defs)

        source_metrics = ChapterMetrics(0, 0, 0, len(source_refs), len(source_defs), 0, 0, 0)
        target_metrics = ChapterMetrics(0, 0, 0, len(target_refs), len(target_defs), 0, 0, 0)
        target_rel = rel(book_root, target_by_scope[scope][-1])
        note_scopes.append(
            {
                "scope": scope,
                "target_dir": target_dir,
                "source_paths": [rel(book_root, path) for path in source_by_scope[scope]],
                "target_paths": [rel(book_root, path) for path in target_by_scope[scope]],
                "source": asdict(source_metrics),
                "target": asdict(target_metrics),
                "ratios": {
                    "note_refs": round(ratio(target_metrics.note_refs, source_metrics.note_refs), 4),
                    "note_defs": round(ratio(target_metrics.note_defs, source_metrics.note_defs), 4),
                },
            }
        )
        if source_metrics.note_refs and ratio(target_metrics.note_refs, source_metrics.note_refs) < min_note_coverage_ratio:
            add_issue(
                issues,
                "note_reference_coverage_low",
                target_rel,
                f"Logical chapter {scope} has {target_metrics.note_refs}/{source_metrics.note_refs} unique note references; minimum ratio is {min_note_coverage_ratio}.",
                source_metrics,
                target_metrics,
            )
        if source_metrics.note_defs and ratio(target_metrics.note_defs, source_metrics.note_defs) < min_note_coverage_ratio:
            add_issue(
                issues,
                "note_definition_coverage_low",
                target_rel,
                f"Logical chapter {scope} has {target_metrics.note_defs}/{source_metrics.note_defs} unique note definitions; minimum ratio is {min_note_coverage_ratio}.",
                source_metrics,
                target_metrics,
            )
        if target_metrics.note_refs > target_metrics.note_defs:
            add_issue(
                issues,
                "target_note_references_without_definitions",
                target_rel,
                f"Logical chapter {scope} has {target_metrics.note_refs} unique note references but only {target_metrics.note_defs} note definitions.",
                source_metrics,
                target_metrics,
            )

def check_coverage(
    book_root: Path,
    *,
    source_dir: str = "chapters/src",
    target_dirs: tuple[str, ...] = TARGET_DIRS,
    min_paragraph_block_ratio: float = 0.75,
    min_char_ratio: float = 0.35,
    min_note_coverage_ratio: float = 1.0,
) -> dict:
    source_root = book_root / source_dir
    issues: list[dict] = []
    chapters: list[dict] = []
    if not source_root.exists():
        return {"book_root": ".", "ok": True, "chapters_checked": 0, "chapters": [], "issues": []}

    source_chapters = sorted(path for path in source_root.glob("*.md") if not path.name.startswith("_"))
    note_scopes: list[dict] = []
    for target_dir in target_dirs:
        target_root = book_root / target_dir
        if not target_root.exists():
            continue
        for source_path in source_chapters:
            target_path = target_root / source_path.name
            if not target_path.exists():
                continue
            check_pair(
                book_root=book_root,
                source_path=source_path,
                target_path=target_path,
                min_paragraph_block_ratio=min_paragraph_block_ratio,
                min_char_ratio=min_char_ratio,
                min_note_coverage_ratio=min_note_coverage_ratio,
                issues=issues,
                chapters=chapters,
            )
        target_chapters = sorted(path for path in target_root.glob("*.md") if not path.name.startswith("_"))
        check_note_scopes(
            book_root=book_root,
            source_paths=source_chapters,
            target_paths=target_chapters,
            target_dir=target_dir,
            min_note_coverage_ratio=min_note_coverage_ratio,
            issues=issues,
            note_scopes=note_scopes,
        )

    return {
        "book_root": ".",
        "ok": not issues,
        "chapters_checked": len(chapters),
        "note_scopes": note_scopes,
        "settings": {
            "source_dir": source_dir,
            "target_dirs": list(target_dirs),
            "min_paragraph_block_ratio": min_paragraph_block_ratio,
            "min_char_ratio": min_char_ratio,
            "min_note_coverage_ratio": min_note_coverage_ratio,
        },
        "chapters": chapters,
        "issues": issues,
    }


def main() -> None:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    target_dirs = tuple(args.target_dir) if args.target_dir else TARGET_DIRS
    report = check_coverage(
        book_root,
        source_dir=args.source_dir,
        target_dirs=target_dirs,
        min_paragraph_block_ratio=args.min_paragraph_block_ratio,
        min_char_ratio=args.min_char_ratio,
        min_note_coverage_ratio=args.min_note_coverage_ratio,
    )
    if args.write_report:
        out = book_root / "output" / "translation_coverage.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if report["issues"]:
        for issue in report["issues"]:
            print(f"ERROR {issue['rule']}: {issue['path']} {issue['detail']}")
        raise SystemExit(1)
    print("translation coverage PASS")


if __name__ == "__main__":
    main()
