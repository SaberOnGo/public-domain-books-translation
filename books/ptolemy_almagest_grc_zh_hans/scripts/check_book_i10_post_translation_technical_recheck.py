from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "010_book_i_10_post_translation_technical_recheck.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "010_book_i_10_post_translation_technical_recheck.md"
REQUIRED = [
    ("post_translation_recheck_exists", "qa/technical/010_book_i_10_chords.post_translation_technical_recheck.md", [
        "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING",
        "几何图",
        "Euclid",
        "六十进制",
        "Book I.11 弦表本体",
        "不得写 `chapters/final/010_book_i_10_chords.md`",
        "不允许生成正式 `output/book.epub`",
    ]),
    ("translation_exists", "chapters/translated/010_book_i_10_chords.md", ["CONTROLLED_DRAFT_TRANSLATION__REVIEW_PENDING", "1p02′50″", "Book I.11"]),
    ("review_exists", "reviews/chapters/010_book_i_10_chords.review.md", ["PASS_FOR_DRAFT_REVIEW__FINAL_PENDING", "未发现 P0/P1"]),
    ("diagram_audit_exists", "qa/technical/010_book_i_10_chords.diagram_table_audit.md", ["BOOK_I10_TRIAL_FIGURE_LABEL_AUDIT_PASS"]),
    ("proof_dependency_exists", "qa/technical/proof_dependency_map.md", ["I.10", "Eucl."]),
    ("numeric_validation_exists", "qa/technical/numeric_validation_log.md", ["I.10", "sexagesimal"]),
]
FORBIDDEN = ["chapters/final/010_book_i_10_chords.md", "output/book.epub"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def collect_checks() -> tuple[list[dict[str, object]], list[str]]:
    checks: list[dict[str, object]] = []
    failures: list[str] = []
    for check_id, rel_path, needles in REQUIRED:
        path = PROJECT_ROOT / rel_path
        missing: list[str] = []
        if not path.exists():
            status = "FAIL"
            digest = ""
            failures.append(f"missing {rel_path}")
        else:
            digest = sha256(path)
            text = path.read_text(encoding="utf-8", errors="replace")
            missing = [needle for needle in needles if needle not in text]
            status = "PASS" if not missing else "FAIL"
            if missing:
                failures.append(f"{rel_path} missing required strings: {missing}")
        checks.append({"id": check_id, "path": rel_path, "status": status, "missing": missing, "sha256": digest})
    for rel_path in FORBIDDEN:
        exists = (PROJECT_ROOT / rel_path).exists()
        checks.append({"id": "forbidden_file_absent", "path": rel_path, "status": "PASS" if not exists else "FAIL"})
        if exists:
            failures.append(f"forbidden output exists: {rel_path}")
    return checks, failures


def write_reports(checks: list[dict[str, object]], failures: list[str], created: str) -> None:
    status = "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING" if not failures else "FAIL"
    OUT_JSON.write_text(json.dumps({"status": status, "created_at_utc": created, "chapter": "Book I.10", "final_allowed": False, "formal_epub_allowed": False, "next_gate": "chapter quality gate", "checks": checks, "failures": failures}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Book I.10 译后技术复核检查 / Post-Translation Technical Recheck", "", f"check_status: `{status}`", f"created_at_utc: `{created}`", "", "| id | status | path/detail | missing | sha256 |", "|---|---|---|---|---|"]
    for check in checks:
        lines.append(f"| {check['id']} | {check['status']} | `{check.get('path', '')}` | `{check.get('missing', '')}` | `{check.get('sha256', '')}` |")
    if failures:
        lines += ["", "## Failures", *[f"- {failure}" for failure in failures]]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    created = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    checks, failures = collect_checks()
    write_reports(checks, failures, created)
    print(f"wrote {OUT_JSON.relative_to(PROJECT_ROOT)}")
    print(f"wrote {OUT_MD.relative_to(PROJECT_ROOT)}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("Book I.10 post-translation technical recheck passed; chapter quality gate remains pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
