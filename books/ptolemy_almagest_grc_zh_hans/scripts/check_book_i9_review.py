from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "009_book_i_09_review_check.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "009_book_i_09_review_check.md"
REQUIRED = [
    ("review_exists", "reviews/chapters/009_book_i_09_on_individual_preliminaries.review.md", [
        "PASS_FOR_DRAFT_REVIEW__FINAL_PENDING",
        "total | 100 | 92",
        "未发现 P0/P1",
        "总括预设",
        "逐项证明",
        "前述两极间大圈弧",
        "圆内直线大小",
        "不允许写 `chapters/final/009_book_i_09_on_individual_preliminaries.md`",
    ]),
    ("translation_check_exists", "qa/pretranslation/009_book_i_09_translation_check.md", ["PASS_TRANSLATION_DRAFT__REVIEW_PENDING"]),
    ("translation_exists", "chapters/translated/009_book_i_09_on_individual_preliminaries.md", ["CONTROLLED_DRAFT_TRANSLATION__REVIEW_PENDING"]),
]
FORBIDDEN = ["chapters/final/009_book_i_09_on_individual_preliminaries.md", "output/book.epub"]


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
            text = path.read_text(encoding="utf-8")
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
    status = "PASS_REVIEW__TECHNICAL_RECHECK_PENDING" if not failures else "FAIL"
    OUT_JSON.write_text(json.dumps({"status": status, "created_at_utc": created, "chapter": "Book I.9", "final_allowed": False, "formal_epub_allowed": False, "checks": checks, "failures": failures}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Book I.9 评审检查 / Review Check", "", f"check_status: `{status}`", f"created_at_utc: `{created}`", "", "## 检查项", "", "| id | status | path | missing | sha256 |", "|---|---|---|---|---|"]
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
    print("Book I.9 review check passed; technical recheck remains pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
