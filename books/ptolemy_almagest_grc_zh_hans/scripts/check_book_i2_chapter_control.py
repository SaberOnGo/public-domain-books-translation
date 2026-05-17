from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "002_book_i_02_chapter_control_check.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "002_book_i_02_chapter_control_check.md"


REQUIRED = [
    {
        "id": "control_exists",
        "path": "qa/chapter_controls/002_book_i_02_order_of_the_theorems.control.md",
        "contains": [
            "PASS_FOR_CONTROLLED_TRANSLATION_PREP__NOT_TRANSLATED",
            "source_path: `chapters/src/002_book_i_02_order_of_the_theorems.md`",
            "全书论证次序",
            "观测与证明方法",
            "英译本只作 reference witness",
            "不得写 `chapters/final/002_book_i_02_order_of_the_theorems.md`",
            "当前仍未翻译，不能进入终稿",
        ],
    },
    {
        "id": "source_recheck_exists",
        "path": "qa/pretranslation/002_book_i_02_formal_source_recheck.md",
        "contains": ["PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING"],
    },
    {
        "id": "technical_audit_exists",
        "path": "qa/technical/002_book_i_02_order_of_the_theorems.technical_audit.md",
        "contains": ["PASS_FOR_TRANSLATION_PREP__NOT_TRANSLATED"],
    },
]

FORBIDDEN = [
    "chapters/final/002_book_i_02_order_of_the_theorems.md",
    "output/book.epub",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def collect_checks() -> tuple[list[dict[str, object]], list[str]]:
    checks: list[dict[str, object]] = []
    failures: list[str] = []
    for item in REQUIRED:
        path = PROJECT_ROOT / str(item["path"])
        missing: list[str] = []
        if not path.exists():
            failures.append(f"missing {item['path']}")
            status = "FAIL"
            digest = ""
        else:
            digest = sha256(path)
            text = path.read_text(encoding="utf-8")
            missing = [needle for needle in item["contains"] if needle not in text]  # type: ignore[index]
            status = "PASS" if not missing else "FAIL"
            if missing:
                failures.append(f"{item['path']} missing required strings: {missing}")
        checks.append({"id": item["id"], "path": item["path"], "status": status, "missing": missing, "sha256": digest})
    for rel_path in FORBIDDEN:
        path = PROJECT_ROOT / rel_path
        status = "PASS" if not path.exists() else "FAIL"
        if status == "FAIL":
            failures.append(f"forbidden output exists: {rel_path}")
        checks.append({"id": "forbidden_absent", "path": rel_path, "status": status})
    return checks, failures


def write_reports(checks: list[dict[str, object]], failures: list[str], created: str) -> None:
    status = "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED" if not failures else "FAIL"
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(
            {
                "status": status,
                "created_at_utc": created,
                "chapter": "Book I.2",
                "translation_file_allowed_next": "chapters/translated/002_book_i_02_order_of_the_theorems.md"
                if not failures
                else "",
                "final_allowed": False,
                "formal_epub_allowed": False,
                "checks": checks,
                "failures": failures,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Book I.2 章节控制检查 / Chapter Control Check",
        "",
        f"check_status: `{status}`",
        f"created_at_utc: `{created}`",
        "",
        "## 控制结论",
        "",
        "- 本检查确认 Book I.2 章节控制文件已建立。",
        "- 若本检查 PASS，下一步只允许写受控译文 `chapters/translated/002_book_i_02_order_of_the_theorems.md`。",
        "- 本检查不允许写 `chapters/final/`，不允许生成正式 EPUB。",
        "",
        "## 检查项",
        "",
        "| id | status | path | missing | sha256 |",
        "|---|---|---|---|---|",
    ]
    for check in checks:
        missing = ", ".join(str(item) for item in check.get("missing", []))
        lines.append(
            f"| {check['id']} | {check['status']} | `{check['path']}` | {missing} | `{check.get('sha256', '')}` |"
        )
    if failures:
        lines.extend(["", "## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
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
    print("Book I.2 chapter control check passed; controlled translation prep is allowed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
