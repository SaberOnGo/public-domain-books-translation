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
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)|<img\b", re.IGNORECASE)
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


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def strip_footnote_definitions(text: str) -> str:
    lines = []
    skipping = False
    for line in normalize_newlines(text).splitlines():
        if FOOTNOTE_DEF_RE.match(line):
            skipping = True
            continue
        if skipping and (line.startswith(" ") or line.startswith("\t")):
            continue
        skipping = False
        lines.append(line)
    return "\n".join(lines)


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
    return sum(1 for block in normalize_newlines(text).split("\n\n") if is_table_block(block))


def count_formulas(text: str) -> int:
    return len(FORMULA_BLOCK_RE.findall(normalize_newlines(text)))


def metrics_for(text: str) -> ChapterMetrics:
    normalized = normalize_newlines(text)
    body_for_blocks = strip_fenced_blocks(strip_footnote_definitions(normalized))
    blocks = [block for block in body_for_blocks.split("\n\n") if is_reader_paragraph(block)]
    return ChapterMetrics(
        headings=len(re.findall(r"(?m)^\s{0,3}#{1,6}\s+\S", normalized)),
        paragraph_blocks=len(blocks),
        nonspace_chars=len(re.sub(r"\s+", "", body_for_blocks)),
        note_refs=len(set(FOOTNOTE_REF_RE.findall(strip_footnote_definitions(normalized)))),
        note_defs=len(set(FOOTNOTE_DEF_RE.findall(normalized))),
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
    source_metrics = metrics_for(source_path.read_text(encoding="utf-8", errors="replace"))
    target_metrics = metrics_for(target_path.read_text(encoding="utf-8", errors="replace"))
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

    char_ratio = ratio(target_metrics.nonspace_chars, source_metrics.nonspace_chars)
    if source_metrics.nonspace_chars >= 800 and char_ratio < min_char_ratio:
        add_issue(
            issues,
            "chapter_char_coverage_low",
            target_rel,
            f"Target has {target_metrics.nonspace_chars}/{source_metrics.nonspace_chars} non-space characters; minimum ratio is {min_char_ratio}.",
            source_metrics,
            target_metrics,
        )

    if source_metrics.note_refs and ratio(target_metrics.note_refs, source_metrics.note_refs) < min_note_coverage_ratio:
        add_issue(
            issues,
            "note_reference_coverage_low",
            target_rel,
            f"Target has {target_metrics.note_refs}/{source_metrics.note_refs} unique note references; minimum ratio is {min_note_coverage_ratio}.",
            source_metrics,
            target_metrics,
        )

    if source_metrics.note_defs and ratio(target_metrics.note_defs, source_metrics.note_defs) < min_note_coverage_ratio:
        add_issue(
            issues,
            "note_definition_coverage_low",
            target_rel,
            f"Target has {target_metrics.note_defs}/{source_metrics.note_defs} unique note definitions; minimum ratio is {min_note_coverage_ratio}.",
            source_metrics,
            target_metrics,
        )

    if target_metrics.note_refs > target_metrics.note_defs:
        add_issue(
            issues,
            "target_note_references_without_definitions",
            target_rel,
            f"Target has {target_metrics.note_refs} unique note references but only {target_metrics.note_defs} note definitions.",
            source_metrics,
            target_metrics,
        )

    for field, rule in [
        ("tables", "table_coverage_low"),
        ("images", "image_coverage_low"),
        ("formulas", "formula_coverage_low"),
    ]:
        source_count = getattr(source_metrics, field)
        target_count = getattr(target_metrics, field)
        if source_count and target_count < source_count:
            add_issue(
                issues,
                rule,
                target_rel,
                f"Target has {target_count}/{source_count} {field}; source structural units may have been lost.",
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

    return {
        "book_root": ".",
        "ok": not issues,
        "chapters_checked": len(chapters),
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
