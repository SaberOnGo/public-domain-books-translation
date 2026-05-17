from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRANSLATION = PROJECT_ROOT / "chapters" / "translated" / "009_book_i_09_on_individual_preliminaries.md"
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "009_book_i_09_post_translation_technical_recheck.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "009_book_i_09_post_translation_technical_recheck.md"
REQUIRED = [
    ("post_translation_recheck_exists", "qa/technical/009_book_i_09_on_individual_preliminaries.post_translation_technical_recheck.md", [
        "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING",
        "本章不含几何图、表格、六十进制数值、角度或数学计算",
        "英译本只作 reference witness",
        "总括预设",
        "逐项证明",
        "前述两极间大圈弧",
        "圆内直线大小",
        "不得写 `chapters/final/009_book_i_09_on_individual_preliminaries.md`",
        "不允许生成正式 `output/book.epub`",
    ]),
    ("translation_exists", "chapters/translated/009_book_i_09_on_individual_preliminaries.md", [
        "CONTROLLED_DRAFT_TRANSLATION__REVIEW_PENDING",
        "本章译文依据 `chapters/src/009_book_i_09_on_individual_preliminaries.md`",
        "英译本只可作为 reference witness",
        "前述两极之间那段弧",
        "圆内直线大小",
        "## 章末注",
    ]),
    ("review_exists", "reviews/chapters/009_book_i_09_on_individual_preliminaries.review.md", ["PASS_FOR_DRAFT_REVIEW__FINAL_PENDING", "未发现 P0/P1"]),
    ("term_lock_contains_book_i9_terms", "qa/technical/mathematical_term_lock.md", ["Book I.9 具体测定与弦论引入术语", "κατὰ μέρος καταλήψεις", "γραμμικῶς ἀποδεικνύειν"]),
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
    body = body_without_notes(TRANSLATION.read_text(encoding="utf-8") if TRANSLATION.exists() else "")
    hits = [needle for needle in FORBIDDEN_BODY_STRINGS if needle in body]
    if hits:
        failures.append(f"translation body contains forbidden wording: {hits}")
    checks.append({"id": "translation_body_forbidden_terms_absent", "status": "PASS" if not hits else "FAIL", "hits": hits})
    marker_hits = [needle for needle in ["Eucl.", "37p", "37;", "弦表"] if needle in body]
    if marker_hits:
        failures.append(f"Book I.9 body contains unexpected geometry/table/numeric markers: {marker_hits}")
    checks.append({"id": "geometry_table_numeric_markers_absent_for_i9", "status": "PASS" if not marker_hits else "FAIL", "hits": marker_hits})
    for rel_path in FORBIDDEN_FILES:
        exists = (PROJECT_ROOT / rel_path).exists()
        checks.append({"id": "forbidden_file_absent", "path": rel_path, "status": "PASS" if not exists else "FAIL"})
        if exists:
            failures.append(f"forbidden output exists: {rel_path}")
    return checks, failures


def write_reports(checks: list[dict[str, object]], failures: list[str], created: str) -> None:
    status = "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING" if not failures else "FAIL"
    OUT_JSON.write_text(json.dumps({"status": status, "created_at_utc": created, "chapter": "Book I.9", "final_allowed": False, "formal_epub_allowed": False, "next_gate": "chapter quality gate", "checks": checks, "failures": failures}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Book I.9 译后技术复核检查 / Post-Translation Technical Recheck", "", f"check_status: `{status}`", f"created_at_utc: `{created}`", "", "## 检查项", "", "| id | status | path/detail | missing/hits | sha256 |", "|---|---|---|---|---|"]
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
    print("Book I.9 post-translation technical recheck passed; chapter quality gate remains pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
