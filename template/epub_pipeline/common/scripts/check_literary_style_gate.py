from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
HIGH_IMPACT_RE = re.compile(
    r"(preface|introduction|advertisement|prologue|foreword|author|"
    r"序言|前言|作者序|原序|凡例|导言|引言|绪论|开篇|首章|第一章)",
    flags=re.IGNORECASE,
)
STYLE_CANDIDATES = {
    "literal_or_source_syntax": re.compile(
        r"(原因在于|其原因是|以.*为.*衡量|要是只能|也就不能|就必然|从而|由此可见|这意味着)"
    ),
    "explanatory_or_analytical_bridge": re.compile(
        r"(换言之|也就是说|这说明|可以理解为|正对应|意在说明|这段.*说明|这种.*体现|因此.*共同)"
    ),
    "flat_abstract_noun_chain": re.compile(
        r"(进行|具有|予以|加以|对于|关于|方面|机制|维度|层面|路径|能力|性质|态度|状态)"
    ),
    "awkward_translationese": re.compile(
        r"(中文接口|原文意思是|表达 意思是|大意是|被.*所|把.*作为.*来|使.*的一切能力)"
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan and validate literary smoothness review artifacts.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--source-dir", default="chapters/final", help="Reader-facing final chapter directory.")
    parser.add_argument("--review", default="qa/literary_style/literary_style_review.md", help="Literary review record.")
    parser.add_argument("--write-report", action="store_true", help="Write qa/literary_style/literary_style_gate.json.")
    parser.add_argument(
        "--require-review-pass",
        action="store_true",
        help="Require a completed literary review PASS. Use this before final release/private artifact creation.",
    )
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def rel(book_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(book_root).as_posix()
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def markdown_body(text: str) -> str:
    body = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    body = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", body)
    return body


def chapter_files(source_dir: Path) -> list[Path]:
    if not source_dir.exists():
        return []
    return [path for path in sorted(source_dir.rglob("*.md")) if path.is_file() and not path.name.startswith("_")]


def is_high_impact(path: Path, index: int, text: str) -> bool:
    heading_match = re.search(r"(?m)^\s{0,3}#{1,6}\s+(.+)$", text)
    heading = heading_match.group(1) if heading_match else ""
    if index <= 1:
        return True
    return bool(HIGH_IMPACT_RE.search(f"{path.stem} {heading}"))


def collect_scan(book_root: Path, source_dir: Path) -> dict:
    files = chapter_files(source_dir)
    candidate_rows: list[dict] = []
    high_impact_files: list[str] = []
    totals = {name: 0 for name in STYLE_CANDIDATES}
    high_impact_totals = {name: 0 for name in STYLE_CANDIDATES}

    for index, path in enumerate(files):
        text = markdown_body(read_text(path))
        high_impact = is_high_impact(path, index, text)
        if high_impact:
            high_impact_files.append(rel(book_root, path))
        for name, pattern in STYLE_CANDIDATES.items():
            matches = list(pattern.finditer(text))
            totals[name] += len(matches)
            if high_impact:
                high_impact_totals[name] += len(matches)
            for match in matches[:20]:
                start = max(0, match.start() - 40)
                end = min(len(text), match.end() + 80)
                candidate_rows.append(
                    {
                        "file": rel(book_root, path),
                        "high_impact": high_impact,
                        "family": name,
                        "trigger": match.group(0),
                        "context": " ".join(text[start:end].split()),
                    }
                )

    return {
        "source_dir": rel(book_root, source_dir),
        "chapter_file_count": len(files),
        "high_impact_files": high_impact_files,
        "candidate_counts": totals,
        "high_impact_candidate_counts": high_impact_totals,
        "candidate_examples": candidate_rows[:200],
        "note": (
            "Pattern hits are candidates, not automatic defects. Final release requires a target-language "
            "literary review that resolves or justifies them, especially in author/source prefaces, "
            "introductions, openings, and first chapters."
        ),
    }


def read_field(text: str, field: str) -> str | None:
    matches = re.findall(rf"(?im)^\s*{re.escape(field)}\s*:\s*(.*?)\s*$", text)
    if not matches:
        return None
    value = matches[-1].strip()
    if value.startswith(("'", '"')) and len(value) >= 2:
        value = value.strip("'\"")
    return value.split("#", 1)[0].strip()


def read_number(text: str, field: str) -> float | None:
    value = read_field(text, field)
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def read_bool(text: str, field: str) -> bool | None:
    value = read_field(text, field)
    if value is None:
        return None
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return None


def validate_review(book_root: Path, review_path: Path) -> list[dict]:
    issues: list[dict] = []
    if not review_path.exists():
        return [
            {
                "rule": "missing_literary_style_review",
                "path": rel(book_root, review_path),
                "detail": "Missing qa/literary_style/literary_style_review.md.",
            }
        ]

    text = read_text(review_path)
    status = read_field(text, "status")
    target_score = read_number(text, "target_only_reading_score")
    awkward_count = read_number(text, "read_aloud_awkward_sentence_count")
    unresolved_debt = read_number(text, "unresolved_style_debt_count")
    literal_debt = read_number(text, "literal_explanatory_style_debt_count")
    high_impact_reviewed = read_bool(text, "high_impact_sections_reviewed")
    opening_reviewed = read_bool(text, "author_preface_and_first_chapter_reviewed")
    source_backcheck = read_bool(text, "source_fidelity_backcheck_after_polish")

    def add(rule: str, detail: str) -> None:
        issues.append({"rule": rule, "path": rel(book_root, review_path), "detail": detail})

    if status != "PASS":
        add("literary_style_review_not_pass", "Literary style review must set status: PASS before final release.")
    if target_score is None or target_score < 5:
        add("literary_target_only_score_below_final_bar", "Final literary review requires target_only_reading_score: 5.")
    if awkward_count is None or awkward_count != 0:
        add("literary_read_aloud_has_awkward_sentences", "Final literary review requires read_aloud_awkward_sentence_count: 0.")
    if unresolved_debt is None or unresolved_debt != 0:
        add("literary_unresolved_style_debt", "Final literary review requires unresolved_style_debt_count: 0.")
    if literal_debt is None or literal_debt != 0:
        add(
            "literary_literal_explanatory_style_debt",
            "Final literary review requires literal_explanatory_style_debt_count: 0.",
        )
    if high_impact_reviewed is not True:
        add(
            "literary_high_impact_not_reviewed",
            "Author/source prefaces, introductions, openings, and first chapters must be reviewed as high impact.",
        )
    if opening_reviewed is not True:
        add(
            "literary_author_preface_first_chapter_not_reviewed",
            "author_preface_and_first_chapter_reviewed must be true.",
        )
    if source_backcheck is not True:
        add(
            "literary_source_backcheck_missing",
            "After target-language polish, source_fidelity_backcheck_after_polish must be true.",
        )
    return issues


def main() -> None:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    source_dir = (book_root / args.source_dir).resolve() if not Path(args.source_dir).is_absolute() else Path(args.source_dir)
    review_path = (book_root / args.review).resolve() if not Path(args.review).is_absolute() else Path(args.review)

    scan = collect_scan(book_root, source_dir)
    issues = validate_review(book_root, review_path) if args.require_review_pass else []
    report = {
        "ok": not issues,
        "require_review_pass": args.require_review_pass,
        "review_path": rel(book_root, review_path),
        "scan": scan,
        "issues": issues,
    }

    if args.write_report:
        out = book_root / "qa" / "literary_style" / "literary_style_gate.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if issues:
        for issue in issues:
            print(f"ERROR {issue['rule']}: {issue['path']} {issue['detail']}")
        raise SystemExit(1)
    print("literary style gate PASS" if args.require_review_pass else "literary style scan complete")


if __name__ == "__main__":
    main()
