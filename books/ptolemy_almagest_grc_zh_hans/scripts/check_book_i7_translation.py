from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRANSLATION = PROJECT_ROOT / "chapters" / "translated" / "007_book_i_07_earth_has_no_translational_motion.md"
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "007_book_i_07_translation_check.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "007_book_i_07_translation_check.md"


REQUIRED = [
    {
        "id": "translation_file_exists",
        "path": "chapters/translated/007_book_i_07_earth_has_no_translational_motion.md",
        "contains": [
            "CONTROLLED_DRAFT_TRANSLATION__REVIEW_PENDING",
            "source_file: `../src/007_book_i_07_earth_has_no_translational_motion.md`",
            "英译本只可作为 reference witness",
            "平移运动",
            "位于中心的处所",
            "重物都向地球运动",
            "切平面成直角",
            "上方",
            "下方",
            "保持静止",
            "从西向东大约旋转一周",
            "空气中的现象",
            "云向东方经过",
            "飞行物或抛射物",
            "滞后",
            "## 章末注",
        ],
    },
    {
        "id": "chapter_control_exists",
        "path": "qa/chapter_controls/007_book_i_07_earth_has_no_translational_motion.control.md",
        "contains": ["PASS_FOR_CONTROLLED_TRANSLATION_PREP__NOT_TRANSLATED"],
    },
    {
        "id": "technical_audit_exists",
        "path": "qa/technical/007_book_i_07_earth_has_no_translational_motion.technical_audit.md",
        "contains": ["PASS_FOR_TRANSLATION_PREP__NOT_TRANSLATED"],
    },
]

FORBIDDEN_BODY_STRINGS = [
    "科里奥利力",
    "惯性系",
    "参照系",
    "角速度",
    "真实地球自转",
    "万有引力",
    "translated from English",
    "英译为底稿",
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


def body_without_notes(text: str) -> str:
    if "## 正文" in text:
        text = text.split("## 正文", 1)[1]
    return text.split("## 章末注", 1)[0]


def collect_checks() -> tuple[list[dict[str, object]], list[str]]:
    checks: list[dict[str, object]] = []
    failures: list[str] = []
    translation_text = TRANSLATION.read_text(encoding="utf-8") if TRANSLATION.exists() else ""

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

    body_text = body_without_notes(translation_text)
    forbidden_hits = [needle for needle in FORBIDDEN_BODY_STRINGS if needle in body_text]
    if forbidden_hits:
        failures.append(f"translation body contains forbidden modernizing wording: {forbidden_hits}")
    checks.append({"id": "forbidden_modernizing_wording_absent", "status": "PASS" if not forbidden_hits else "FAIL", "hits": forbidden_hits})

    note_count = sum(translation_text.count(f"{index}.") for index in range(1, 6))
    if note_count < 5:
        failures.append("chapter notes appear incomplete")
    checks.append({"id": "chapter_notes_present", "status": "PASS" if note_count >= 5 else "FAIL", "note_count": note_count})

    for rel_path in FORBIDDEN_FILES:
        path = PROJECT_ROOT / rel_path
        status = "PASS" if not path.exists() else "FAIL"
        if status == "FAIL":
            failures.append(f"forbidden output exists: {rel_path}")
        checks.append({"id": "forbidden_file_absent", "path": rel_path, "status": status})
    return checks, failures


def write_reports(checks: list[dict[str, object]], failures: list[str], created: str) -> None:
    status = "PASS_TRANSLATION_DRAFT__REVIEW_PENDING" if not failures else "FAIL"
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
        "# Book I.7 译文检查 / Translation Check",
        "",
        f"check_status: `{status}`",
        f"created_at_utc: `{created}`",
        "",
        "## 控制结论",
        "",
        "- 本检查确认 Book I.7 受控译文草稿已建立。",
        "- 本检查不允许进入 `chapters/final/`，不允许生成正式 EPUB。",
        "- 下一步必须进行忠实度、中文可读性、术语一致性、天文学证明链和古今概念边界审校。",
        "",
        "## 检查项",
        "",
        "| id | status | path/detail | missing/hits | sha256 |",
        "|---|---|---|---|---|",
    ]
    for check in checks:
        detail = check.get("path", check.get("note_count", ""))
        misses = check.get("missing", check.get("hits", ""))
        lines.append(f"| {check['id']} | {check['status']} | `{detail}` | `{misses}` | `{check.get('sha256', '')}` |")
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
    print("Book I.7 translation check passed; review remains pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
