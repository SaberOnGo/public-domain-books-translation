from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "010_book_i_10_chapter_control_check.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "010_book_i_10_chapter_control_check.md"
REQUIRED = [
    ("control_exists", "qa/chapter_controls/010_book_i_10_chords.control.md", [
        "PASS_FOR_CONTROLLED_TRANSLATION_PREP__DRAFT_EXISTS",
        "Book I.10",
        "不允许进入 `chapters/final/`",
        "不允许翻译 Book I.11 弦表",
    ]),
    ("source_recheck_exists", "qa/pretranslation/010_book_i_10_formal_source_recheck.md", ["PASS_FOR_FORMAL_SOURCE_RECHECK__NOT_FINAL_GATE"]),
    ("technical_audit_exists", "qa/technical/010_book_i_10_chords.technical_audit.md", ["PASS_FOR_TRIAL"]),
    ("diagram_audit_exists", "qa/technical/010_book_i_10_chords.diagram_table_audit.md", ["BOOK_I10_TRIAL_FIGURE_LABEL_AUDIT_PASS"]),
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
        checks.append({"id": "forbidden_absent", "path": rel_path, "status": "PASS" if not exists else "FAIL"})
        if exists:
            failures.append(f"forbidden output exists: {rel_path}")
    return checks, failures


def write_reports(checks: list[dict[str, object]], failures: list[str], created: str) -> None:
    status = "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED" if not failures else "FAIL"
    OUT_JSON.write_text(json.dumps({"status": status, "created_at_utc": created, "chapter": "Book I.10", "final_allowed": False, "formal_epub_allowed": False, "checks": checks, "failures": failures}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Book I.10 章节控制检查 / Chapter Control Check", "", f"check_status: `{status}`", f"created_at_utc: `{created}`", "", "| id | status | path | missing | sha256 |", "|---|---|---|---|---|"]
    for check in checks:
        lines.append(f"| {check['id']} | {check['status']} | `{check['path']}` | {', '.join(str(x) for x in check.get('missing', []))} | `{check.get('sha256', '')}` |")
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
    print("Book I.10 chapter control check passed; controlled translation prep is allowed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
