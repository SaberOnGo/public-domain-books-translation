from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "007_book_i_07_chapter_quality_gate.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "007_book_i_07_chapter_quality_gate.md"


REQUIRED_JSON_STATUSES = [
    (
        "source_extraction",
        "qa/pretranslation/007_book_i_07_source_extraction_check.json",
        "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING",
    ),
    (
        "formal_source_recheck",
        "qa/pretranslation/007_book_i_07_formal_source_recheck.json",
        "PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING",
    ),
    (
        "chapter_control",
        "qa/pretranslation/007_book_i_07_chapter_control_check.json",
        "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED",
    ),
    (
        "translation_draft",
        "qa/pretranslation/007_book_i_07_translation_check.json",
        "PASS_TRANSLATION_DRAFT__REVIEW_PENDING",
    ),
    (
        "draft_review",
        "qa/pretranslation/007_book_i_07_review_check.json",
        "PASS_REVIEW__TECHNICAL_RECHECK_PENDING",
    ),
    (
        "post_translation_technical_recheck",
        "qa/pretranslation/007_book_i_07_post_translation_technical_recheck.json",
        "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING",
    ),
]

REQUIRED_MARKDOWN = [
    {
        "id": "chapter_quality_gate_record",
        "path": "qa/chapter_controls/007_book_i_07_earth_has_no_translational_motion.quality_gate.md",
        "contains": [
            "PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING",
            "不允许写 `chapters/final/007_book_i_07_earth_has_no_translational_motion.md`",
            "不允许生成正式 `output/book.epub`",
            "地球无平移运动",
            "重物趋向中心",
            "地球每日自转设想",
            "空气现象反驳",
        ],
    },
    {
        "id": "translation_file",
        "path": "chapters/translated/007_book_i_07_earth_has_no_translational_motion.md",
        "contains": [
            "CONTROLLED_DRAFT_TRANSLATION__REVIEW_PENDING",
            "英译本只可作为 reference witness",
            "## 正文",
            "## 章末注",
        ],
    },
]

FORBIDDEN_FILES = [
    "chapters/final/007_book_i_07_earth_has_no_translational_motion.md",
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

    for gate_id, rel_path, expected in REQUIRED_JSON_STATUSES:
        path = PROJECT_ROOT / rel_path
        if not path.exists():
            checks.append({"id": gate_id, "path": rel_path, "status": "FAIL", "expected": expected, "actual": ""})
            failures.append(f"missing required gate JSON: {rel_path}")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        actual = data.get("status")
        status = "PASS" if actual == expected else "FAIL"
        if status == "FAIL":
            failures.append(f"{rel_path} status {actual!r} does not match {expected!r}")
        checks.append(
            {"id": gate_id, "path": rel_path, "status": status, "expected": expected, "actual": actual, "sha256": sha256(path)}
        )

    for item in REQUIRED_MARKDOWN:
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

    for rel_path in FORBIDDEN_FILES:
        path = PROJECT_ROOT / rel_path
        status = "PASS" if not path.exists() else "FAIL"
        if status == "FAIL":
            failures.append(f"forbidden output exists: {rel_path}")
        checks.append({"id": "forbidden_file_absent", "path": rel_path, "status": status})

    return checks, failures


def write_reports(checks: list[dict[str, object]], failures: list[str], created: str) -> None:
    status = "PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING" if not failures else "FAIL"
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(
            {
                "status": status,
                "created_at_utc": created,
                "chapter": "Book I.7",
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
        "# Book I.7 章节质量门禁检查 / Chapter Quality Gate Check",
        "",
        f"check_status: `{status}`",
        f"created_at_utc: `{created}`",
        "",
        "## 控制结论",
        "",
        "- Book I.7 章节级质量门禁通过，可进入终稿前全书一致性审校队列。",
        "- 本检查不允许写 `chapters/final/007_book_i_07_earth_has_no_translational_motion.md`，不允许生成正式 EPUB。",
        "- 本检查不放开 Book I.8-I.16 或全书批量翻译。",
        "",
        "## 检查项",
        "",
        "| id | status | path | expected/actual/missing | sha256 |",
        "|---|---|---|---|---|",
    ]
    for check in checks:
        detail = check.get("expected", check.get("missing", ""))
        if "actual" in check:
            detail = f"{check.get('expected')} / {check.get('actual')}"
        lines.append(
            f"| {check['id']} | {check['status']} | `{check.get('path', '')}` | `{detail}` | `{check.get('sha256', '')}` |"
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
    print("Book I.7 chapter quality gate passed; final promotion remains pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
