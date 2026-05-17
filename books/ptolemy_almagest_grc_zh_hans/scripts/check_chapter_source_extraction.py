from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_I_SEGMENTATION = PROJECT_ROOT / "source" / "book_i_segmentation.json"
STATE = PROJECT_ROOT / "state" / "pipeline_state.json"
OUT_DIR = PROJECT_ROOT / "qa" / "pretranslation"


CHAPTERS = {
    "I.1": {
        "source": "chapters/src/001_book_i_01_proem.md",
        "check_json": "001_book_i_01_source_extraction_check.json",
        "check_md": "001_book_i_01_source_extraction_check.md",
        "translated": "chapters/translated/001_book_i_01_proem.md",
        "control_check": "qa/pretranslation/001_book_i_01_chapter_control_check.json",
        "final": "chapters/final/001_book_i_01_proem.md",
        "required_title": "αʹ. Προοίμιον.",
    },
    "I.2": {
        "source": "chapters/src/002_book_i_02_order_of_the_theorems.md",
        "check_json": "002_book_i_02_source_extraction_check.json",
        "check_md": "002_book_i_02_source_extraction_check.md",
        "translated": "chapters/translated/002_book_i_02_order_of_the_theorems.md",
        "control_check": "qa/pretranslation/002_book_i_02_chapter_control_check.json",
        "final": "chapters/final/002_book_i_02_order_of_the_theorems.md",
        "required_title": "βʹ. Περὶ τῆς τάξεως τῶν θεωρημάτων.",
    },
    "I.3": {
        "source": "chapters/src/003_book_i_03_heaven_moves_spherically.md",
        "check_json": "003_book_i_03_source_extraction_check.json",
        "check_md": "003_book_i_03_source_extraction_check.md",
        "translated": "chapters/translated/003_book_i_03_heaven_moves_spherically.md",
        "control_check": "qa/pretranslation/003_book_i_03_chapter_control_check.json",
        "final": "chapters/final/003_book_i_03_heaven_moves_spherically.md",
        "required_title": "γʹ. Ὅτι σφαιροειδῶς ὁ οὐρανὸς φέρεται.",
    },
    "I.4": {
        "source": "chapters/src/004_book_i_04_earth_is_spherical.md",
        "check_json": "004_book_i_04_source_extraction_check.json",
        "check_md": "004_book_i_04_source_extraction_check.md",
        "translated": "chapters/translated/004_book_i_04_earth_is_spherical.md",
        "control_check": "qa/pretranslation/004_book_i_04_chapter_control_check.json",
        "final": "chapters/final/004_book_i_04_earth_is_spherical.md",
        "required_title": "δʹ. Ὅτι καὶ ἡ γῆ σφραιροειδής ἐστιν πρὸς αἴσθησιν ὡς καθʼ ὅλα μέρη.",
    },
    "I.5": {
        "source": "chapters/src/005_book_i_05_earth_is_central.md",
        "check_json": "005_book_i_05_source_extraction_check.json",
        "check_md": "005_book_i_05_source_extraction_check.md",
        "translated": "chapters/translated/005_book_i_05_earth_is_central.md",
        "control_check": "qa/pretranslation/005_book_i_05_chapter_control_check.json",
        "final": "chapters/final/005_book_i_05_earth_is_central.md",
        "required_title": "εʹ. Ὅτι μέση τοῦ οὐρανοῦ ἐστιν ἡ γῆ.",
    },
    "I.6": {
        "source": "chapters/src/006_book_i_06_earth_as_point_to_heavens.md",
        "check_json": "006_book_i_06_source_extraction_check.json",
        "check_md": "006_book_i_06_source_extraction_check.md",
        "translated": "chapters/translated/006_book_i_06_earth_as_point_to_heavens.md",
        "control_check": "qa/pretranslation/006_book_i_06_chapter_control_check.json",
        "final": "chapters/final/006_book_i_06_earth_as_point_to_heavens.md",
        "required_title": "ϛʹ. Ὅτι σημείου λόγον ἔχει πρὸς τὰ οὐράνια",
    },
    "I.7": {
        "source": "chapters/src/007_book_i_07_earth_has_no_translational_motion.md",
        "check_json": "007_book_i_07_source_extraction_check.json",
        "check_md": "007_book_i_07_source_extraction_check.md",
        "translated": "chapters/translated/007_book_i_07_earth_has_no_translational_motion.md",
        "control_check": "qa/pretranslation/007_book_i_07_chapter_control_check.json",
        "final": "chapters/final/007_book_i_07_earth_has_no_translational_motion.md",
        "required_title": "ζʹ. Ὅτι οὐδὲ κίνησίν τινα μεταβατικὴν ποιεῖται",
    },
    "I.8": {
        "source": "chapters/src/008_book_i_08_two_primary_motions.md",
        "check_json": "008_book_i_08_source_extraction_check.json",
        "check_md": "008_book_i_08_source_extraction_check.md",
        "translated": "chapters/translated/008_book_i_08_two_primary_motions.md",
        "control_check": "qa/pretranslation/008_book_i_08_chapter_control_check.json",
        "final": "chapters/final/008_book_i_08_two_primary_motions.md",
        "required_title": "ηʹ. Ὅτι δύο διαφοραὶ τῶν πρώτων κινήσεών",
    },
    "I.9": {
        "source": "chapters/src/009_book_i_09_on_individual_preliminaries.md",
        "check_json": "009_book_i_09_source_extraction_check.json",
        "check_md": "009_book_i_09_source_extraction_check.md",
        "translated": "chapters/translated/009_book_i_09_on_individual_preliminaries.md",
        "control_check": "qa/pretranslation/009_book_i_09_chapter_control_check.json",
        "final": "chapters/final/009_book_i_09_on_individual_preliminaries.md",
        "required_title": "θʹ. Περὶ τῶν κατὰ μέρος καταλήψεων.",
    },
    "I.10": {
        "source": "chapters/src/010_book_i_10_chords.md",
        "check_json": "010_book_i_10_source_extraction_check.json",
        "check_md": "010_book_i_10_source_extraction_check.md",
        "translated": "chapters/translated/010_book_i_10_chords.md",
        "control_check": "qa/pretranslation/010_book_i_10_chapter_control_check.json",
        "final": "chapters/final/010_book_i_10_chords.md",
        "required_title": "ιʹ. Περὶ τῆς πηλικότητος τῶν ἐν τῷ κύκλῳ",
    },
    "I.12": {
        "source": "chapters/src/012_book_i_12_arc_between_tropics.md",
        "check_json": "012_book_i_12_source_extraction_check.json",
        "check_md": "012_book_i_12_source_extraction_check.md",
        "translated": "chapters/translated/012_book_i_12_arc_between_tropics.md",
        "control_check": "qa/pretranslation/012_book_i_12_chapter_control_check.json",
        "final": "chapters/final/012_book_i_12_arc_between_tropics.md",
        "required_title": "ιβʹ. Περὶ τῆς μεταξὺ τῶν τροπικῶν περιφερείας.",
    },
    "I.13": {
        "source": "chapters/src/013_book_i_13_preliminaries_for_spherical_proofs.md",
        "check_json": "013_book_i_13_source_extraction_check.json",
        "check_md": "013_book_i_13_source_extraction_check.md",
        "translated": "chapters/translated/013_book_i_13_preliminaries_for_spherical_proofs.md",
        "control_check": "qa/pretranslation/013_book_i_13_chapter_control_check.json",
        "final": "chapters/final/013_book_i_13_preliminaries_for_spherical_proofs.md",
        "required_title": "ιγʹ. Προλαμβανόμενα εἰς τὰς σφαιρικὰς δείξεις.",
    },
    "I.14": {
        "source": "chapters/src/014_book_i_14_arcs_between_equator_and_ecliptic.md",
        "check_json": "014_book_i_14_source_extraction_check.json",
        "check_md": "014_book_i_14_source_extraction_check.md",
        "translated": "chapters/translated/014_book_i_14_arcs_between_equator_and_ecliptic.md",
        "control_check": "qa/pretranslation/014_book_i_14_chapter_control_check.json",
        "final": "chapters/final/014_book_i_14_arcs_between_equator_and_ecliptic.md",
        "required_title": "ιδʹ. Περὶ τῶν μεταξὺ τοῦ ἰσημερινοῦ καὶ τοῦ λοξοῦ κύκλου περιφερειῶν.",
    },
    "I.15": {
        "source": "chapters/src/015_book_i_15_obliquity_table.md",
        "check_json": "015_book_i_15_source_extraction_check.json",
        "check_md": "015_book_i_15_source_extraction_check.md",
        "translated": "chapters/translated/015_book_i_15_obliquity_table.md",
        "control_check": "qa/pretranslation/015_book_i_15_chapter_control_check.json",
        "final": "chapters/final/015_book_i_15_obliquity_table.md",
        "required_title": "ιεʹ. Κανόνιον λοξώσεως.",
    },
    "I.16": {
        "source": "chapters/src/016_book_i_16_risings_on_right_sphere.md",
        "check_json": "016_book_i_16_source_extraction_check.json",
        "check_md": "016_book_i_16_source_extraction_check.md",
        "translated": "chapters/translated/016_book_i_16_risings_on_right_sphere.md",
        "control_check": "qa/pretranslation/016_book_i_16_chapter_control_check.json",
        "final": "chapters/final/016_book_i_16_risings_on_right_sphere.md",
        "required_title": "ιϛʹ. Περὶ τῶν ἐπʼ ὀρθῆς τῆς σφαίρας ἀναφορῶν.",
    },
}


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def segmentation_entry(anchor: str) -> dict[str, object]:
    data = json.loads(BOOK_I_SEGMENTATION.read_text(encoding="utf-8"))
    for entry in data["entries"]:
        if entry.get("anchor") == anchor:
            return entry
    raise RuntimeError(f"Missing segmentation entry for {anchor}")


def contains(text: str, needle: str) -> bool:
    return needle in text


def collect_checks(anchor: str) -> tuple[list[dict[str, object]], list[str]]:
    if anchor not in CHAPTERS:
        raise RuntimeError(f"Unsupported chapter for this check: {anchor}")
    cfg = CHAPTERS[anchor]
    source = PROJECT_ROOT / str(cfg["source"])
    translated = PROJECT_ROOT / str(cfg["translated"])
    final = PROJECT_ROOT / str(cfg["final"])
    entry = segmentation_entry(anchor)
    state = json.loads(STATE.read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []
    failures: list[str] = []

    if not source.exists():
        failures.append(f"source file missing: {cfg['source']}")
        text = ""
    else:
        text = source.read_text(encoding="utf-8")
    checks.append({"id": "source_file_exists", "status": "PASS" if source.exists() else "FAIL", "path": str(cfg["source"])})

    required_strings = [
        "FORMAL_SOURCE_EXTRACTED_FROM_PAL_AUXILIARY_TRANSCRIPTION__PDF_RECHECK_REQUIRED",
        "translation_status: `NOT_TRANSLATED`",
        "formal_translation_scope: `SOURCE_ONLY_NOT_TRANSLATION`",
        "primary_facsimile",
        "auxiliary_transcription",
        "Use English translations only as reference witnesses",
        str(cfg["required_title"]),
    ]
    missing = [item for item in required_strings if not contains(text, item)]
    if missing:
        failures.append(f"source file missing required source-control wording: {missing}")
    checks.append({"id": "source_control_wording", "status": "PASS" if not missing else "FAIL", "missing": missing})

    marker_count = len(re.findall(r"\[I_[^\]]+\]", text))
    expected_count = int(entry["reserve_marker_count"])
    if marker_count != expected_count:
        failures.append(f"marker count mismatch: expected {expected_count}, got {marker_count}")
    checks.append(
        {
            "id": "marker_count_matches_segmentation",
            "status": "PASS" if marker_count == expected_count else "FAIL",
            "expected": expected_count,
            "actual": marker_count,
        }
    )

    expected_pages = str(entry["pdf_viewer_pages_estimated"])
    if expected_pages not in text:
        failures.append(f"source file does not record estimated PDF viewer pages {expected_pages}")
    checks.append(
        {
            "id": "pdf_viewer_pages_recorded",
            "status": "PASS" if expected_pages in text else "FAIL",
            "expected": expected_pages,
        }
    )

    control_check = PROJECT_ROOT / str(cfg["control_check"])
    translated_allowed = False
    if control_check.exists():
        control_data = json.loads(control_check.read_text(encoding="utf-8"))
        translated_allowed = control_data.get("status") == "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED"
    if translated.exists() and not translated_allowed:
        failures.append(f"translated chapter exists before source gate permits it: {cfg['translated']}")
    checks.append(
        {
            "id": "translated_absent_or_allowed_by_control",
            "status": "PASS" if not translated.exists() or translated_allowed else "FAIL",
            "path": str(cfg["translated"]),
        }
    )

    if final.exists():
        failures.append(f"final chapter exists before source gate permits it: {cfg['final']}")
    checks.append({"id": "final_absent", "status": "PASS" if not final.exists() else "FAIL", "path": str(cfg["final"])})

    formal_allowed = state.get("formal_translation_allowed") is True
    if formal_allowed:
        failures.append("formal_translation_allowed is true; this source check expects gated pretranslation")
    checks.append({"id": "formal_translation_still_gated", "status": "PASS" if not formal_allowed else "FAIL"})

    return checks, failures


def write_reports(anchor: str, checks: list[dict[str, object]], failures: list[str], created: str) -> None:
    cfg = CHAPTERS[anchor]
    status = "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING" if not failures else "FAIL"
    out_json = OUT_DIR / str(cfg["check_json"])
    out_md = OUT_DIR / str(cfg["check_md"])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(
            {
                "status": status,
                "created_at_utc": created,
                "chapter": anchor,
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
        f"# Book {anchor} Source Extraction Check",
        "",
        f"check_status: `{status}`",
        f"created_at_utc: `{created}`",
        "",
        "## 控制结论",
        "",
        "- 本检查只确认章节 source extraction candidate 已生成。",
        "- 本检查不允许翻译本章，不允许写 `chapters/final/`，不允许生成正式 EPUB。",
        "- 章节仍需 PDF formal recheck、章节控制、技术审计和译后评审。",
        "",
        "## 检查项",
        "",
        "| id | status | detail |",
        "|---|---|---|",
    ]
    for check in checks:
        detail = check.get("path", check.get("expected", check.get("missing", "")))
        lines.append(f"| {check['id']} | {check['status']} | `{detail}` |")
    if failures:
        lines.extend(["", "## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check one extracted chapter source file.")
    parser.add_argument("--anchor", required=True)
    args = parser.parse_args()
    created = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    checks, failures = collect_checks(args.anchor)
    write_reports(args.anchor, checks, failures, created)
    cfg = CHAPTERS[args.anchor]
    print(f"wrote {cfg['check_json']}")
    print(f"wrote {cfg['check_md']}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print(f"{args.anchor} source extraction check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
