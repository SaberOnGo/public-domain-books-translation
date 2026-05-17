from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "010_book_i_10_formal_source_recheck.json"
REPORT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "010_book_i_10_formal_source_recheck.md"


CHECKS = [
    {
        "id": "source_file_exists",
        "path": "chapters/src/010_book_i_10_chords.md",
        "required": ["I_31_7", "I_48", "primary_facsimile", "auxiliary_transcription", "reference witness"],
    },
    {
        "id": "page_verification_exists",
        "path": "qa/technical/book_i_page_verification.md",
        "required": ["Book I.10", "20-27", "viewer page `28`", "book_i_pages_019_029_contact_sheet.jpg"],
    },
    {
        "id": "technical_audit_exists",
        "path": "qa/technical/010_book_i_10_chords.technical_audit.md",
        "required": ["PASS_FOR_TRIAL", "I_31_7", "I_48", "do not translate Book I.11"],
    },
    {
        "id": "diagram_audit_exists",
        "path": "qa/technical/010_book_i_10_chords.diagram_table_audit.md",
        "required": ["BOOK_I10_TRIAL_FIGURE_LABEL_AUDIT_PASS", "PASS_FOR_TRIAL_TRANSLATION", "Book I.11"],
    },
    {
        "id": "proof_dependency_exists",
        "path": "qa/technical/proof_dependency_map.md",
        "required": ["I.10", "PASS_FOR_TRIAL", "Eucl.", "I.10-table-transition"],
    },
    {
        "id": "numeric_validation_exists",
        "path": "qa/technical/numeric_validation_log.md",
        "required": ["I.10", "PASS_FOR_TRIAL", "sexagesimal", "Book I.11"],
    },
    {
        "id": "trial_translation_exists",
        "path": "chapters/translated/010_book_i_10_chords.md",
        "required": ["translation_status", "Book I.10"],
    },
    {
        "id": "trial_review_exists",
        "path": "reviews/trial_chapter/010_book_i_10_chords.review.md",
        "required": ["PASS", "Book I.10"],
    },
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run_check(spec: dict[str, object]) -> dict[str, object]:
    rel_path = str(spec["path"])
    path = PROJECT_ROOT / rel_path
    result: dict[str, object] = {
        "id": spec["id"],
        "path": rel_path,
        "status": "PASS",
        "missing": [],
        "sha256": "",
    }
    if not path.exists():
        result["status"] = "FAIL"
        result["missing"] = ["file"]
        return result
    text = path.read_text(encoding="utf-8", errors="replace")
    missing = [needle for needle in spec["required"] if str(needle) not in text]
    if missing:
        result["status"] = "FAIL"
        result["missing"] = missing
    result["sha256"] = sha256(path)
    return result


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# Book I.10 正式 source recheck / Formal Source Recheck",
        "",
        f"recheck_status: `{report['status']}`",
        f"created_at_utc: `{report['created_at_utc']}`",
        "",
        "## 控制结论",
        "",
        "- 本报告只判断 Book I.10 是否具备从 trial source 进入 formal source extraction recheck 的证据。",
        "- 本报告不允许写入 `chapters/final/`，不允许翻译 Book I.11 弦表，不允许生成正式 `output/book.epub`。",
        "- 英译本仍只能作 reference witness，不得成为底稿或 OCR/转写 authority。",
        "",
        "## 检查项",
        "",
        "| id | status | path | missing | sha256 |",
        "|---|---|---|---|---|",
    ]
    for item in report["checks"]:
        missing = ", ".join(item["missing"]) if item["missing"] else ""
        lines.append(
            f"| {item['id']} | {item['status']} | `{item['path']}` | {missing} | `{item['sha256']}` |"
        )
    lines.extend(
        [
            "",
            "## 下一步",
            "",
            "1. 若本报告 PASS，可把 Book I.10 作为第一个 formal source extraction recheck 章节。",
            "2. 仍必须重建或复核正式 `chapters/src` 元数据，不能把 trial PASS 直接当 final PASS。",
            "3. 进入翻译或终稿前，必须重新执行章节 control、技术审计、图表审计和章节门禁。",
        ]
    )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = [run_check(spec) for spec in CHECKS]
    status = "PASS_FOR_FORMAL_SOURCE_RECHECK__NOT_FINAL_GATE"
    if any(item["status"] != "PASS" for item in checks):
        status = "BLOCKED"
    report = {
        "status": status,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "chapter": "Book I.10",
        "formal_final_allowed": False,
        "book_i11_translation_allowed": False,
        "formal_epub_allowed": False,
        "checks": checks,
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(f"wrote {REPORT_JSON.relative_to(PROJECT_ROOT)}")
    print(f"wrote {REPORT_MD.relative_to(PROJECT_ROOT)}")
    print(f"status={status}")
    if status == "BLOCKED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
