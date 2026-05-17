from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRANSLATION = PROJECT_ROOT / "chapters" / "translated" / "004_book_i_04_earth_is_spherical.md"
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "004_book_i_04_post_translation_technical_recheck.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "004_book_i_04_post_translation_technical_recheck.md"


REQUIRED = [
    {
        "id": "post_translation_recheck_exists",
        "path": "qa/technical/004_book_i_04_earth_is_spherical.post_translation_technical_recheck.md",
        "contains": [
            "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING",
            "本章不含几何图、表格、六十进制数值、角度或天文学计算",
            "英译本只作 reference witness",
            "月食时刻差异",
            "东西向升落差异",
            "地表形状反证",
            "南北星象变化",
            "航近高地证据",
            "不得写 `chapters/final/004_book_i_04_earth_is_spherical.md`",
            "不允许生成正式 `output/book.epub`",
        ],
    },
    {
        "id": "translation_exists",
        "path": "chapters/translated/004_book_i_04_earth_is_spherical.md",
        "contains": [
            "CONTROLLED_DRAFT_TRANSLATION__REVIEW_PENDING",
            "本章译文依据 `chapters/src/004_book_i_04_earth_is_spherical.md`",
            "英译本只可作为 reference witness",
            "本章无图表、无数值表",
            "食象",
            "月食",
            "小时差同各地距离成比例",
            "圆柱形",
            "世界的两极",
            "航近山",
            "水面有凸曲",
            "## 章末注",
        ],
    },
    {
        "id": "review_exists",
        "path": "reviews/chapters/004_book_i_04_earth_is_spherical.review.md",
        "contains": [
            "PASS_FOR_DRAFT_REVIEW__FINAL_PENDING",
            "未发现 P0/P1",
            "术语一致性",
            "古今概念边界",
            "下一步",
        ],
    },
    {
        "id": "term_lock_contains_book_i4_terms",
        "path": "qa/technical/mathematical_term_lock.md",
        "contains": [
            "Book I.4 地球球形与观测证据术语",
            "πρὸς αἴσθησιν",
            "ἐκλειπτικὰς φαντασίας",
            "κυρτότης",
            "κυλινδροειδής",
            "προσπλέωμεν",
        ],
    },
]

FORBIDDEN_BODY_STRINGS = [
    "现代测地学",
    "现代时区",
    "地球椭球",
    "大地水准面",
    "现代光学",
    "translated from English",
    "英译为底稿",
]

FORBIDDEN_FILES = [
    "chapters/final/004_book_i_04_earth_is_spherical.md",
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

    translation_text = TRANSLATION.read_text(encoding="utf-8") if TRANSLATION.exists() else ""
    body_text = body_without_notes(translation_text)
    forbidden_hits = [needle for needle in FORBIDDEN_BODY_STRINGS if needle in body_text]
    if forbidden_hits:
        failures.append(f"translation body contains forbidden modernizing wording: {forbidden_hits}")
    checks.append({"id": "translation_body_modernizing_terms_absent", "status": "PASS" if not forbidden_hits else "FAIL", "hits": forbidden_hits})

    expected_absent_topics = ["Eucl.", "37p", "37;", "弦表"]
    topic_hits = [needle for needle in expected_absent_topics if needle in body_text]
    if topic_hits:
        failures.append(f"Book I.4 body contains unexpected geometry/table/numeric markers: {topic_hits}")
    checks.append({"id": "geometry_table_numeric_markers_absent_for_i4", "status": "PASS" if not topic_hits else "FAIL", "hits": topic_hits})

    for rel_path in FORBIDDEN_FILES:
        path = PROJECT_ROOT / rel_path
        status = "PASS" if not path.exists() else "FAIL"
        if status == "FAIL":
            failures.append(f"forbidden output exists: {rel_path}")
        checks.append({"id": "forbidden_file_absent", "path": rel_path, "status": status})

    return checks, failures


def write_reports(checks: list[dict[str, object]], failures: list[str], created: str) -> None:
    status = "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING" if not failures else "FAIL"
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(
            {
                "status": status,
                "created_at_utc": created,
                "chapter": "Book I.4",
                "final_allowed": False,
                "formal_epub_allowed": False,
                "next_gate": "chapter quality gate",
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
        "# Book I.4 译后技术复核检查 / Post-Translation Technical Recheck",
        "",
        f"check_status: `{status}`",
        f"created_at_utc: `{created}`",
        "",
        "## 控制结论",
        "",
        "- 本检查确认 Book I.4 已通过译后技术复核，可进入章节质量门禁准备。",
        "- 本检查不允许进入 `chapters/final/`，不允许生成正式 EPUB。",
        "- Book I.4 无图表、无数值、无 Euclid 依赖；技术风险集中在月食时刻、形状反证、南北星象和航海观察证据。",
        "",
        "## 检查项",
        "",
        "| id | status | path/detail | missing/hits | sha256 |",
        "|---|---|---|---|---|",
    ]
    for check in checks:
        detail = check.get("path", "")
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
    print("Book I.4 post-translation technical recheck passed; chapter quality gate remains pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
