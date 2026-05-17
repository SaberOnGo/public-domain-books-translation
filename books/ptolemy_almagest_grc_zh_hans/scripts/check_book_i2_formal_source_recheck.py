from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "002_book_i_02_formal_source_recheck.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "002_book_i_02_formal_source_recheck.md"


REQUIRED = [
    {
        "id": "source_file_exists",
        "path": "chapters/src/002_book_i_02_order_of_the_theorems.md",
        "contains": [
            "FORMAL_SOURCE_EXTRACTED_FROM_PAL_AUXILIARY_TRANSCRIPTION__PDF_RECHECK_REQUIRED",
            "Greek_title | βʹ. Περὶ τῆς τάξεως τῶν θεωρημάτων.",
            "estimated_pdf_viewer_pages | `8-9`",
            "Use English translations only as reference witnesses",
        ],
    },
    {
        "id": "source_extraction_check_exists",
        "path": "qa/pretranslation/002_book_i_02_source_extraction_check.md",
        "contains": ["PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"],
    },
    {
        "id": "pdf_contact_sheet_exists",
        "path": "qa/technical/page_screenshots/book_i02_pages_008_009_contact_sheet.jpg",
        "contains": [],
    },
    {
        "id": "technical_audit_exists",
        "path": "qa/technical/002_book_i_02_order_of_the_theorems.technical_audit.md",
        "contains": [
            "PASS_FOR_TRANSLATION_PREP__NOT_TRANSLATED",
            "整部论著的论证次序",
            "观测与证明关系",
            "本章无图表、无表格",
            "本章不含数学计算或六十进制值",
        ],
    },
    {
        "id": "term_lock_updated",
        "path": "qa/technical/mathematical_term_lock.md",
        "contains": [
            "Book I.2 全书次序与天文学对象术语",
            "τάξις",
            "λοξὸς κύκλος",
            "οἰκουμένη",
            "ὁρίζων",
            "ἀπλανῶν σφαῖρα",
            "πέντε πλανῆται",
            "γραμμικαὶ ἔφοδοι",
        ],
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


def check_required() -> tuple[list[dict[str, object]], list[str]]:
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
            text = "" if path.suffix.lower() in {".jpg", ".png"} else path.read_text(encoding="utf-8")
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
    status = "PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING" if not failures else "FAIL"
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(
            {
                "status": status,
                "created_at_utc": created,
                "chapter": "Book I.2",
                "translation_allowed": False,
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
        "# Book I.2 正式 source recheck / Formal Source Recheck",
        "",
        f"recheck_status: `{status}`",
        f"created_at_utc: `{created}`",
        "",
        "## 控制结论",
        "",
        "- 本报告确认 Book I.2 source extraction candidate、PDF 页图证据和译前技术审计已建立。",
        "- 本报告不允许直接翻译；下一步必须先创建章节控制文件，再进入受控翻译。",
        "- 本报告不允许写 `chapters/final/`，不允许生成正式 EPUB。",
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
    checks, failures = check_required()
    write_reports(checks, failures, created)
    print(f"wrote {OUT_JSON.relative_to(PROJECT_ROOT)}")
    print(f"wrote {OUT_MD.relative_to(PROJECT_ROOT)}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("Book I.2 formal source recheck passed; chapter control remains pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
