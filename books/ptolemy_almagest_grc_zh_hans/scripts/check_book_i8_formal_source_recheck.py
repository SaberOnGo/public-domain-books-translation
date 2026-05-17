from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "008_book_i_08_formal_source_recheck.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "008_book_i_08_formal_source_recheck.md"


REQUIRED = [
    {
        "id": "source_file_exists",
        "path": "chapters/src/008_book_i_08_two_primary_motions.md",
        "contains": [
            "FORMAL_SOURCE_EXTRACTED_FROM_PAL_AUXILIARY_TRANSCRIPTION__PDF_RECHECK_REQUIRED",
            "Greek_title | ηʹ. Ὅτι δύο διαφοραὶ τῶν πρώτων κινήσεών",
            "estimated_pdf_viewer_pages | `17-19`",
            "Use English translations only as reference witnesses",
        ],
    },
    {
        "id": "source_extraction_check_exists",
        "path": "qa/pretranslation/008_book_i_08_source_extraction_check.md",
        "contains": ["PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"],
    },
    {
        "id": "pdf_contact_sheet_exists",
        "path": "qa/technical/page_screenshots/book_i08_pages_017_019_contact_sheet.jpg",
        "contains": [],
    },
    {
        "id": "technical_audit_exists",
        "path": "qa/technical/008_book_i_08_two_primary_motions.technical_audit.md",
        "contains": [
            "PASS_FOR_TRANSLATION_PREP__NOT_TRANSLATED",
            "第一运动",
            "第二运动",
            "赤道圈",
            "黄道斜圈",
            "子午圈",
            "二分点",
            "二至点",
        ],
    },
    {
        "id": "term_lock_updated",
        "path": "qa/technical/mathematical_term_lock.md",
        "contains": [
            "Book I.8 天球两种基本运动术语",
            "πρῶται κινήσεις",
            "πρώτη φορά / πρώτη περιαγωγή",
            "δευτέρα φορά / δευτέρα διαφορά",
            "ἰσημερινός",
            "λοξὸς κύκλος",
            "μεσημβρινός",
            "τροπικά",
        ],
    },
]

FORBIDDEN = [
    "chapters/final/008_book_i_08_two_primary_motions.md",
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
                "chapter": "Book I.8",
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
        "# Book I.8 正式 source recheck / Formal Source Recheck",
        "",
        f"recheck_status: `{status}`",
        f"created_at_utc: `{created}`",
        "",
        "## 控制结论",
        "",
        "- 本报告确认 Book I.8 source extraction candidate、PDF 页图证据和译前技术审计已建立。",
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
        lines.append(f"| {check['id']} | {check['status']} | `{check['path']}` | {missing} | `{check.get('sha256', '')}` |")
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
    print("Book I.8 formal source recheck passed; chapter control remains pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
