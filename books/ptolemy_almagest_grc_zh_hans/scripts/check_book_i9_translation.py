from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRANSLATION = PROJECT_ROOT / "chapters" / "translated" / "009_book_i_09_on_individual_preliminaries.md"
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "009_book_i_09_translation_check.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "009_book_i_09_translation_check.md"
REQUIRED = [
    ("translation_file_exists", "chapters/translated/009_book_i_09_on_individual_preliminaries.md", [
        "CONTROLLED_DRAFT_TRANSLATION__REVIEW_PENDING",
        "source_file: `../src/009_book_i_09_on_individual_preliminaries.md`",
        "英译本只可作为 reference witness",
        "总括性的预先说明",
        "各项具体证明",
        "前述两极之间那段弧",
        "通过这些极画出的大圈",
        "圆内直线大小",
        "几何方法",
        "## 章末注",
    ]),
    ("chapter_control_exists", "qa/chapter_controls/009_book_i_09_on_individual_preliminaries.control.md", ["PASS_FOR_CONTROLLED_TRANSLATION_PREP__NOT_TRANSLATED"]),
    ("technical_audit_exists", "qa/technical/009_book_i_09_on_individual_preliminaries.technical_audit.md", ["PASS_FOR_TRANSLATION_PREP__NOT_TRANSLATED"]),
]
FORBIDDEN_BODY_STRINGS = ["代数函数", "现代教材", "弦表如下", "translated from English", "英译为底稿"]
FORBIDDEN_FILES = ["chapters/final/009_book_i_09_on_individual_preliminaries.md", "output/book.epub"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def body_without_notes(text: str) -> str:
    return text.split("## 章末注", 1)[0].split("## 正文", 1)[-1]


def collect_checks() -> tuple[list[dict[str, object]], list[str]]:
    checks: list[dict[str, object]] = []
    failures: list[str] = []
    translation_text = TRANSLATION.read_text(encoding="utf-8") if TRANSLATION.exists() else ""
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
    body = body_without_notes(translation_text)
    hits = [needle for needle in FORBIDDEN_BODY_STRINGS if needle in body]
    if hits:
        failures.append(f"translation body contains forbidden wording: {hits}")
    checks.append({"id": "forbidden_wording_absent", "status": "PASS" if not hits else "FAIL", "hits": hits})
    if translation_text.count("1.") < 1:
        failures.append("chapter note appears incomplete")
    checks.append({"id": "chapter_note_present", "status": "PASS" if translation_text.count("1.") >= 1 else "FAIL"})
    for rel_path in FORBIDDEN_FILES:
        exists = (PROJECT_ROOT / rel_path).exists()
        checks.append({"id": "forbidden_file_absent", "path": rel_path, "status": "PASS" if not exists else "FAIL"})
        if exists:
            failures.append(f"forbidden output exists: {rel_path}")
    return checks, failures


def write_reports(checks: list[dict[str, object]], failures: list[str], created: str) -> None:
    status = "PASS_TRANSLATION_DRAFT__REVIEW_PENDING" if not failures else "FAIL"
    OUT_JSON.write_text(json.dumps({"status": status, "created_at_utc": created, "chapter": "Book I.9", "final_allowed": False, "formal_epub_allowed": False, "checks": checks, "failures": failures}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Book I.9 译文检查 / Translation Check", "", f"check_status: `{status}`", f"created_at_utc: `{created}`", "", "## 检查项", "", "| id | status | path/detail | missing/hits | sha256 |", "|---|---|---|---|---|"]
    for check in checks:
        misses = check.get("missing", check.get("hits", ""))
        lines.append(f"| {check['id']} | {check['status']} | `{check.get('path', '')}` | `{misses}` | `{check.get('sha256', '')}` |")
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
    print("Book I.9 translation check passed; review remains pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
