from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "005_book_i_05_review_check.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "005_book_i_05_review_check.md"


REQUIRED = [
    {
        "id": "review_exists",
        "path": "reviews/chapters/005_book_i_05_earth_is_central.review.md",
        "contains": [
            "PASS_FOR_DRAFT_REVIEW__FINAL_PENDING",
            "total | 100 | 91",
            "未发现 P0/P1",
            "地球居中命题",
            "三种非居中位置",
            "地平圈等分",
            "东西地平与中天时间",
            "月食反证",
            "不允许写 `chapters/final/005_book_i_05_earth_is_central.md`",
        ],
    },
    {
        "id": "translation_check_exists",
        "path": "qa/pretranslation/005_book_i_05_translation_check.md",
        "contains": ["PASS_TRANSLATION_DRAFT__REVIEW_PENDING"],
    },
    {
        "id": "translation_exists",
        "path": "chapters/translated/005_book_i_05_earth_is_central.md",
        "contains": ["CONTROLLED_DRAFT_TRANSLATION__REVIEW_PENDING"],
    },
]

FORBIDDEN = [
    "chapters/final/005_book_i_05_earth_is_central.md",
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
    status = "PASS_REVIEW__TECHNICAL_RECHECK_PENDING" if not failures else "FAIL"
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(
            {
                "status": status,
                "created_at_utc": created,
                "chapter": "Book I.5",
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
        "# Book I.5 评审检查 / Review Check",
        "",
        f"check_status: `{status}`",
        f"created_at_utc: `{created}`",
        "",
        "## 控制结论",
        "",
        "- 本检查确认 Book I.5 译后评审记录存在并通过草稿级评审。",
        "- 本检查不允许进入 `chapters/final/`，不允许生成正式 EPUB。",
        "- 下一步仍需译后技术复核和章节质量门禁。",
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
    print("Book I.5 review check passed; technical recheck remains pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
