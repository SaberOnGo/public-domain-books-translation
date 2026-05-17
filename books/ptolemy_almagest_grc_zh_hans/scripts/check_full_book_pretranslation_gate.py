from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATE = PROJECT_ROOT / "state" / "pipeline_state.json"
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "full_book_pretranslation_gate.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "full_book_pretranslation_gate.md"


REQUIRED_PRE_RESEARCH_FILES = [
    "goal/2026-05-17_almagest_full_book_translation_goal.md",
    "qa/pretranslation/full_book_pre_research_plan.md",
    "qa/pretranslation/pretranslation_report.md",
    "source/full_toc_draft.json",
    "source/full_book_translation_outline.md",
    "qa/pretranslation/full_book_risk_map.md",
    "qa/pretranslation/full_book_risk_map.json",
    "source/book_i_segmentation.md",
    "source/book_i_segmentation.json",
    "chapters/src/001_book_i_01_proem.md",
    "qa/pretranslation/001_book_i_01_source_extraction_check.md",
    "qa/pretranslation/001_book_i_01_source_extraction_check.json",
    "chapters/src/002_book_i_02_order_of_the_theorems.md",
    "qa/pretranslation/002_book_i_02_source_extraction_check.md",
    "qa/pretranslation/002_book_i_02_source_extraction_check.json",
    "chapters/src/003_book_i_03_heaven_moves_spherically.md",
    "qa/pretranslation/003_book_i_03_source_extraction_check.md",
    "qa/pretranslation/003_book_i_03_source_extraction_check.json",
    "chapters/src/004_book_i_04_earth_is_spherical.md",
    "qa/pretranslation/004_book_i_04_source_extraction_check.md",
    "qa/pretranslation/004_book_i_04_source_extraction_check.json",
    "qa/technical/004_book_i_04_earth_is_spherical.technical_audit.md",
    "qa/pretranslation/004_book_i_04_formal_source_recheck.md",
    "qa/pretranslation/004_book_i_04_formal_source_recheck.json",
    "qa/chapter_controls/004_book_i_04_earth_is_spherical.control.md",
    "qa/pretranslation/004_book_i_04_chapter_control_check.md",
    "qa/pretranslation/004_book_i_04_chapter_control_check.json",
    "chapters/translated/004_book_i_04_earth_is_spherical.md",
    "qa/pretranslation/004_book_i_04_translation_check.md",
    "qa/pretranslation/004_book_i_04_translation_check.json",
    "reviews/chapters/004_book_i_04_earth_is_spherical.review.md",
    "qa/pretranslation/004_book_i_04_review_check.md",
    "qa/pretranslation/004_book_i_04_review_check.json",
    "qa/technical/004_book_i_04_earth_is_spherical.post_translation_technical_recheck.md",
    "qa/pretranslation/004_book_i_04_post_translation_technical_recheck.md",
    "qa/pretranslation/004_book_i_04_post_translation_technical_recheck.json",
    "qa/chapter_controls/004_book_i_04_earth_is_spherical.quality_gate.md",
    "qa/pretranslation/004_book_i_04_chapter_quality_gate.md",
    "qa/pretranslation/004_book_i_04_chapter_quality_gate.json",
    "chapters/src/005_book_i_05_earth_is_central.md",
    "qa/pretranslation/005_book_i_05_source_extraction_check.md",
    "qa/pretranslation/005_book_i_05_source_extraction_check.json",
    "qa/technical/page_screenshots/book_i05_pages_012_014_contact_sheet.jpg",
    "qa/technical/005_book_i_05_earth_is_central.technical_audit.md",
    "qa/pretranslation/005_book_i_05_formal_source_recheck.md",
    "qa/pretranslation/005_book_i_05_formal_source_recheck.json",
    "qa/chapter_controls/005_book_i_05_earth_is_central.control.md",
    "qa/pretranslation/005_book_i_05_chapter_control_check.md",
    "qa/pretranslation/005_book_i_05_chapter_control_check.json",
    "chapters/translated/005_book_i_05_earth_is_central.md",
    "qa/pretranslation/005_book_i_05_translation_check.md",
    "qa/pretranslation/005_book_i_05_translation_check.json",
    "reviews/chapters/005_book_i_05_earth_is_central.review.md",
    "qa/pretranslation/005_book_i_05_review_check.md",
    "qa/pretranslation/005_book_i_05_review_check.json",
    "qa/technical/005_book_i_05_earth_is_central.post_translation_technical_recheck.md",
    "qa/pretranslation/005_book_i_05_post_translation_technical_recheck.md",
    "qa/pretranslation/005_book_i_05_post_translation_technical_recheck.json",
    "qa/chapter_controls/005_book_i_05_earth_is_central.quality_gate.md",
    "qa/pretranslation/005_book_i_05_chapter_quality_gate.md",
    "qa/pretranslation/005_book_i_05_chapter_quality_gate.json",
    "chapters/src/006_book_i_06_earth_as_point_to_heavens.md",
    "qa/pretranslation/006_book_i_06_source_extraction_check.md",
    "qa/pretranslation/006_book_i_06_source_extraction_check.json",
    "qa/technical/page_screenshots/book_i06_page_014_contact_sheet.jpg",
    "qa/technical/006_book_i_06_earth_as_point_to_heavens.technical_audit.md",
    "qa/pretranslation/006_book_i_06_formal_source_recheck.md",
    "qa/pretranslation/006_book_i_06_formal_source_recheck.json",
    "qa/chapter_controls/006_book_i_06_earth_as_point_to_heavens.control.md",
    "qa/pretranslation/006_book_i_06_chapter_control_check.md",
    "qa/pretranslation/006_book_i_06_chapter_control_check.json",
    "chapters/translated/006_book_i_06_earth_as_point_to_heavens.md",
    "qa/pretranslation/006_book_i_06_translation_check.md",
    "qa/pretranslation/006_book_i_06_translation_check.json",
    "reviews/chapters/006_book_i_06_earth_as_point_to_heavens.review.md",
    "qa/pretranslation/006_book_i_06_review_check.md",
    "qa/pretranslation/006_book_i_06_review_check.json",
    "qa/technical/006_book_i_06_earth_as_point_to_heavens.post_translation_technical_recheck.md",
    "qa/pretranslation/006_book_i_06_post_translation_technical_recheck.md",
    "qa/pretranslation/006_book_i_06_post_translation_technical_recheck.json",
    "qa/chapter_controls/006_book_i_06_earth_as_point_to_heavens.quality_gate.md",
    "qa/pretranslation/006_book_i_06_chapter_quality_gate.md",
    "qa/pretranslation/006_book_i_06_chapter_quality_gate.json",
    "chapters/src/007_book_i_07_earth_has_no_translational_motion.md",
    "qa/pretranslation/007_book_i_07_source_extraction_check.md",
    "qa/pretranslation/007_book_i_07_source_extraction_check.json",
    "qa/technical/page_screenshots/book_i07_pages_015_017_contact_sheet.jpg",
    "qa/technical/007_book_i_07_earth_has_no_translational_motion.technical_audit.md",
    "qa/pretranslation/007_book_i_07_formal_source_recheck.md",
    "qa/pretranslation/007_book_i_07_formal_source_recheck.json",
    "qa/chapter_controls/007_book_i_07_earth_has_no_translational_motion.control.md",
    "qa/pretranslation/007_book_i_07_chapter_control_check.md",
    "qa/pretranslation/007_book_i_07_chapter_control_check.json",
    "chapters/translated/007_book_i_07_earth_has_no_translational_motion.md",
    "qa/pretranslation/007_book_i_07_translation_check.md",
    "qa/pretranslation/007_book_i_07_translation_check.json",
    "reviews/chapters/007_book_i_07_earth_has_no_translational_motion.review.md",
    "qa/pretranslation/007_book_i_07_review_check.md",
    "qa/pretranslation/007_book_i_07_review_check.json",
    "qa/technical/007_book_i_07_earth_has_no_translational_motion.post_translation_technical_recheck.md",
    "qa/pretranslation/007_book_i_07_post_translation_technical_recheck.md",
    "qa/pretranslation/007_book_i_07_post_translation_technical_recheck.json",
    "qa/chapter_controls/007_book_i_07_earth_has_no_translational_motion.quality_gate.md",
    "qa/pretranslation/007_book_i_07_chapter_quality_gate.md",
    "qa/pretranslation/007_book_i_07_chapter_quality_gate.json",
    "chapters/src/008_book_i_08_two_primary_motions.md",
    "qa/pretranslation/008_book_i_08_source_extraction_check.md",
    "qa/pretranslation/008_book_i_08_source_extraction_check.json",
    "qa/technical/page_screenshots/book_i08_pages_017_019_contact_sheet.jpg",
    "qa/technical/008_book_i_08_two_primary_motions.technical_audit.md",
    "qa/pretranslation/008_book_i_08_formal_source_recheck.md",
    "qa/pretranslation/008_book_i_08_formal_source_recheck.json",
    "qa/chapter_controls/008_book_i_08_two_primary_motions.control.md",
    "qa/pretranslation/008_book_i_08_chapter_control_check.md",
    "qa/pretranslation/008_book_i_08_chapter_control_check.json",
    "chapters/translated/008_book_i_08_two_primary_motions.md",
    "qa/pretranslation/008_book_i_08_translation_check.md",
    "qa/pretranslation/008_book_i_08_translation_check.json",
    "reviews/chapters/008_book_i_08_two_primary_motions.review.md",
    "qa/pretranslation/008_book_i_08_review_check.md",
    "qa/pretranslation/008_book_i_08_review_check.json",
    "qa/technical/008_book_i_08_two_primary_motions.post_translation_technical_recheck.md",
    "qa/pretranslation/008_book_i_08_post_translation_technical_recheck.md",
    "qa/pretranslation/008_book_i_08_post_translation_technical_recheck.json",
    "qa/chapter_controls/008_book_i_08_two_primary_motions.quality_gate.md",
    "qa/pretranslation/008_book_i_08_chapter_quality_gate.md",
    "qa/pretranslation/008_book_i_08_chapter_quality_gate.json",
    "chapters/src/009_book_i_09_on_individual_preliminaries.md",
    "qa/pretranslation/009_book_i_09_source_extraction_check.md",
    "qa/pretranslation/009_book_i_09_source_extraction_check.json",
    "qa/technical/page_screenshots/book_i09_page_019_contact_sheet.jpg",
    "qa/technical/009_book_i_09_on_individual_preliminaries.technical_audit.md",
    "qa/pretranslation/009_book_i_09_formal_source_recheck.md",
    "qa/pretranslation/009_book_i_09_formal_source_recheck.json",
    "qa/chapter_controls/009_book_i_09_on_individual_preliminaries.control.md",
    "qa/pretranslation/009_book_i_09_chapter_control_check.md",
    "qa/pretranslation/009_book_i_09_chapter_control_check.json",
    "chapters/translated/009_book_i_09_on_individual_preliminaries.md",
    "qa/pretranslation/009_book_i_09_translation_check.md",
    "qa/pretranslation/009_book_i_09_translation_check.json",
    "reviews/chapters/009_book_i_09_on_individual_preliminaries.review.md",
    "qa/pretranslation/009_book_i_09_review_check.md",
    "qa/pretranslation/009_book_i_09_review_check.json",
    "qa/technical/009_book_i_09_on_individual_preliminaries.post_translation_technical_recheck.md",
    "qa/pretranslation/009_book_i_09_post_translation_technical_recheck.md",
    "qa/pretranslation/009_book_i_09_post_translation_technical_recheck.json",
    "qa/chapter_controls/009_book_i_09_on_individual_preliminaries.quality_gate.md",
    "qa/pretranslation/009_book_i_09_chapter_quality_gate.md",
    "qa/pretranslation/009_book_i_09_chapter_quality_gate.json",
    "qa/technical/003_book_i_03_heaven_moves_spherically.technical_audit.md",
    "qa/pretranslation/003_book_i_03_formal_source_recheck.md",
    "qa/pretranslation/003_book_i_03_formal_source_recheck.json",
    "qa/chapter_controls/003_book_i_03_heaven_moves_spherically.control.md",
    "qa/pretranslation/003_book_i_03_chapter_control_check.md",
    "qa/pretranslation/003_book_i_03_chapter_control_check.json",
    "chapters/translated/003_book_i_03_heaven_moves_spherically.md",
    "qa/pretranslation/003_book_i_03_translation_check.md",
    "qa/pretranslation/003_book_i_03_translation_check.json",
    "reviews/chapters/003_book_i_03_heaven_moves_spherically.review.md",
    "qa/pretranslation/003_book_i_03_review_check.md",
    "qa/pretranslation/003_book_i_03_review_check.json",
    "qa/technical/003_book_i_03_heaven_moves_spherically.post_translation_technical_recheck.md",
    "qa/pretranslation/003_book_i_03_post_translation_technical_recheck.md",
    "qa/pretranslation/003_book_i_03_post_translation_technical_recheck.json",
    "qa/chapter_controls/003_book_i_03_heaven_moves_spherically.quality_gate.md",
    "qa/pretranslation/003_book_i_03_chapter_quality_gate.md",
    "qa/pretranslation/003_book_i_03_chapter_quality_gate.json",
    "qa/technical/002_book_i_02_order_of_the_theorems.technical_audit.md",
    "qa/pretranslation/002_book_i_02_formal_source_recheck.md",
    "qa/pretranslation/002_book_i_02_formal_source_recheck.json",
    "qa/chapter_controls/002_book_i_02_order_of_the_theorems.control.md",
    "qa/pretranslation/002_book_i_02_chapter_control_check.md",
    "qa/pretranslation/002_book_i_02_chapter_control_check.json",
    "chapters/translated/002_book_i_02_order_of_the_theorems.md",
    "qa/pretranslation/002_book_i_02_translation_check.md",
    "qa/pretranslation/002_book_i_02_translation_check.json",
    "reviews/chapters/002_book_i_02_order_of_the_theorems.review.md",
    "qa/pretranslation/002_book_i_02_review_check.md",
    "qa/pretranslation/002_book_i_02_review_check.json",
    "qa/technical/002_book_i_02_order_of_the_theorems.post_translation_technical_recheck.md",
    "qa/pretranslation/002_book_i_02_post_translation_technical_recheck.md",
    "qa/pretranslation/002_book_i_02_post_translation_technical_recheck.json",
    "qa/chapter_controls/002_book_i_02_order_of_the_theorems.quality_gate.md",
    "qa/pretranslation/002_book_i_02_chapter_quality_gate.md",
    "qa/pretranslation/002_book_i_02_chapter_quality_gate.json",
    "qa/technical/001_book_i_01_proem.technical_audit.md",
    "qa/pretranslation/001_book_i_01_formal_source_recheck.md",
    "qa/pretranslation/001_book_i_01_formal_source_recheck.json",
    "qa/chapter_controls/001_book_i_01_proem.control.md",
    "qa/pretranslation/001_book_i_01_chapter_control_check.md",
    "qa/pretranslation/001_book_i_01_chapter_control_check.json",
    "chapters/translated/001_book_i_01_proem.md",
    "qa/pretranslation/001_book_i_01_translation_check.md",
    "qa/pretranslation/001_book_i_01_translation_check.json",
    "reviews/chapters/001_book_i_01_proem.review.md",
    "qa/pretranslation/001_book_i_01_review_check.md",
    "qa/pretranslation/001_book_i_01_review_check.json",
    "qa/technical/001_book_i_01_proem.post_translation_technical_recheck.md",
    "qa/pretranslation/001_book_i_01_post_translation_technical_recheck.md",
    "qa/pretranslation/001_book_i_01_post_translation_technical_recheck.json",
    "qa/chapter_controls/001_book_i_01_proem.quality_gate.md",
    "qa/pretranslation/001_book_i_01_chapter_quality_gate.md",
    "qa/pretranslation/001_book_i_01_chapter_quality_gate.json",
    "qa/pretranslation/book_i_source_split_readiness.md",
    "qa/pretranslation/book_i_source_split_readiness.json",
    "qa/pretranslation/010_book_i_10_source_extraction_check.md",
    "qa/pretranslation/010_book_i_10_source_extraction_check.json",
    "qa/pretranslation/010_book_i_10_formal_source_recheck.md",
    "qa/pretranslation/010_book_i_10_formal_source_recheck.json",
    "qa/pretranslation/010_book_i_10_chapter_control_check.md",
    "qa/pretranslation/010_book_i_10_chapter_control_check.json",
    "qa/pretranslation/010_book_i_10_translation_check.md",
    "qa/pretranslation/010_book_i_10_translation_check.json",
    "reviews/chapters/010_book_i_10_chords.review.md",
    "qa/pretranslation/010_book_i_10_review_check.md",
    "qa/pretranslation/010_book_i_10_review_check.json",
    "qa/technical/010_book_i_10_chords.post_translation_technical_recheck.md",
    "qa/pretranslation/010_book_i_10_post_translation_technical_recheck.md",
    "qa/pretranslation/010_book_i_10_post_translation_technical_recheck.json",
    "qa/chapter_controls/010_book_i_10_chords.quality_gate.md",
    "qa/pretranslation/010_book_i_10_chapter_quality_gate.md",
    "qa/pretranslation/010_book_i_10_chapter_quality_gate.json",
    "qa/technical/011_book_i_11_chord_table_strategy.md",
    "qa/pretranslation/011_book_i_11_table_strategy_check.md",
    "qa/pretranslation/011_book_i_11_table_strategy_check.json",
    "metadata/source_witness_manifest.md",
    "metadata/reference_witness_policy.md",
]


FORBIDDEN_WHILE_GATED = [
    "output/book.epub",
]


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def collect_checks() -> tuple[list[dict[str, object]], list[str]]:
    checks: list[dict[str, object]] = []
    failures: list[str] = []

    state = json.loads(STATE.read_text(encoding="utf-8"))
    formal_allowed = state.get("formal_translation_allowed") is True
    checks.append(
        {
            "id": "formal_translation_allowed_flag",
            "status": "INFO" if not formal_allowed else "PASS",
            "value": formal_allowed,
            "note": "false means pre-research may continue, but formal translation/final EPUB remain gated",
        }
    )

    for item in REQUIRED_PRE_RESEARCH_FILES:
        path = PROJECT_ROOT / item
        status = "PASS" if path.exists() else "FAIL"
        if status == "FAIL":
            failures.append(f"missing required pre-research file: {item}")
        checks.append({"id": "required_file", "path": item, "status": status})

    final_dir = PROJECT_ROOT / "chapters" / "final"
    final_files = sorted(path for path in final_dir.glob("*.md")) if final_dir.exists() else []
    if not formal_allowed and final_files:
        failures.append("chapters/final contains files while formal translation is gated")
    checks.append(
        {
            "id": "no_chapters_final_while_gated",
            "status": "PASS" if formal_allowed or not final_files else "FAIL",
            "files": [rel(path) for path in final_files],
        }
    )

    for item in FORBIDDEN_WHILE_GATED:
        path = PROJECT_ROOT / item
        status = "PASS" if formal_allowed or not path.exists() else "FAIL"
        if status == "FAIL":
            failures.append(f"forbidden formal output exists while gated: {item}")
        checks.append({"id": "forbidden_output_absent_while_gated", "path": item, "status": status})

    pretranslation_report = PROJECT_ROOT / "qa" / "pretranslation" / "pretranslation_report.md"
    report_text = pretranslation_report.read_text(encoding="utf-8") if pretranslation_report.exists() else ""
    accepted_statuses = [
        "FULL_BOOK_PRE_RESEARCH_STARTED__BULK_TRANSLATION_GATED",
        "BOOK_I_TRANSLATION_SCOPE_STARTED__FINAL_GATED",
    ]
    status = "PASS" if any(item in report_text for item in accepted_statuses) else "FAIL"
    if status == "FAIL":
        failures.append("pretranslation_report.md does not record the current gated Book I/full-book status")
    checks.append({"id": "pretranslation_report_gated_status", "status": status})

    return checks, failures


def write_reports(checks: list[dict[str, object]], failures: list[str], created: str) -> None:
    status = "PASS_PRE_RESEARCH_ACTIVE__FORMAL_TRANSLATION_GATED" if not failures else "FAIL"
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(
            {
                "status": status,
                "created_at_utc": created,
                "formal_translation_gate": "gated until full-book pretranslation PASS",
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
        "# 全书预翻译门禁 / Full-Book Pretranslation Gate",
        "",
        f"gate_status: `{status}`",
        f"created_at_utc: `{created}`",
        "",
        "## 控制结论",
        "",
        "- 本门禁允许继续全书预研究、source split 准备、术语/图表/表格/数值 QA 建设。",
        "- 本门禁不允许写 `chapters/final/`，不允许生成正式 `output/book.epub`。",
        "- 英译本只能作 reference witness；正式翻译底本仍是 Heiberg PDF + PAL 古希腊辅助转写。",
        "",
        "## 检查项",
        "",
        "| id | status | path/value |",
        "|---|---|---|",
    ]
    for check in checks:
        value = check.get("path", check.get("value", ""))
        lines.append(f"| {check['id']} | {check['status']} | `{value}` |")
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
    print("pretranslation gate passed: formal translation remains gated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
