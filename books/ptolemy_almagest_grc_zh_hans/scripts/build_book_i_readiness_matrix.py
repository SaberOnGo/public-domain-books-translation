from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEGMENTATION = PROJECT_ROOT / "source" / "book_i_segmentation.json"
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "book_i_source_split_readiness.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "book_i_source_split_readiness.md"
I10_FORMAL_RECHECK = PROJECT_ROOT / "qa" / "pretranslation" / "010_book_i_10_formal_source_recheck.json"
I10_SOURCE_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "010_book_i_10_source_extraction_check.json"
I10_CONTROL_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "010_book_i_10_chapter_control_check.json"
I10_TRANSLATION_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "010_book_i_10_translation_check.json"
I10_REVIEW_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "010_book_i_10_review_check.json"
I10_POST_TECHNICAL_RECHECK = (
    PROJECT_ROOT / "qa" / "pretranslation" / "010_book_i_10_post_translation_technical_recheck.json"
)
I10_CHAPTER_QUALITY_GATE = PROJECT_ROOT / "qa" / "pretranslation" / "010_book_i_10_chapter_quality_gate.json"
I11_TABLE_STRATEGY_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "011_book_i_11_table_strategy_check.json"
I11_TABLE_REGION_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "011_book_i_11_table_region_extraction_check.json"
I12_SOURCE_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "012_book_i_12_source_extraction_check.json"
I13_SOURCE_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "013_book_i_13_source_extraction_check.json"
I14_SOURCE_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "014_book_i_14_source_extraction_check.json"
I15_SOURCE_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "015_book_i_15_source_extraction_check.json"
I16_SOURCE_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "016_book_i_16_source_extraction_check.json"
I1_SOURCE_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "001_book_i_01_source_extraction_check.json"
I2_SOURCE_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "002_book_i_02_source_extraction_check.json"
I3_SOURCE_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "003_book_i_03_source_extraction_check.json"
I4_SOURCE_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "004_book_i_04_source_extraction_check.json"
I5_SOURCE_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "005_book_i_05_source_extraction_check.json"
I6_SOURCE_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "006_book_i_06_source_extraction_check.json"
I7_SOURCE_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "007_book_i_07_source_extraction_check.json"
I1_FORMAL_RECHECK = PROJECT_ROOT / "qa" / "pretranslation" / "001_book_i_01_formal_source_recheck.json"
I2_FORMAL_RECHECK = PROJECT_ROOT / "qa" / "pretranslation" / "002_book_i_02_formal_source_recheck.json"
I3_FORMAL_RECHECK = PROJECT_ROOT / "qa" / "pretranslation" / "003_book_i_03_formal_source_recheck.json"
I4_FORMAL_RECHECK = PROJECT_ROOT / "qa" / "pretranslation" / "004_book_i_04_formal_source_recheck.json"
I5_FORMAL_RECHECK = PROJECT_ROOT / "qa" / "pretranslation" / "005_book_i_05_formal_source_recheck.json"
I6_FORMAL_RECHECK = PROJECT_ROOT / "qa" / "pretranslation" / "006_book_i_06_formal_source_recheck.json"
I7_FORMAL_RECHECK = PROJECT_ROOT / "qa" / "pretranslation" / "007_book_i_07_formal_source_recheck.json"
I1_CONTROL_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "001_book_i_01_chapter_control_check.json"
I2_CONTROL_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "002_book_i_02_chapter_control_check.json"
I3_CONTROL_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "003_book_i_03_chapter_control_check.json"
I4_CONTROL_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "004_book_i_04_chapter_control_check.json"
I5_CONTROL_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "005_book_i_05_chapter_control_check.json"
I6_CONTROL_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "006_book_i_06_chapter_control_check.json"
I7_CONTROL_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "007_book_i_07_chapter_control_check.json"
I1_TRANSLATION_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "001_book_i_01_translation_check.json"
I2_TRANSLATION_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "002_book_i_02_translation_check.json"
I3_TRANSLATION_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "003_book_i_03_translation_check.json"
I4_TRANSLATION_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "004_book_i_04_translation_check.json"
I5_TRANSLATION_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "005_book_i_05_translation_check.json"
I6_TRANSLATION_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "006_book_i_06_translation_check.json"
I7_TRANSLATION_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "007_book_i_07_translation_check.json"
I1_REVIEW_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "001_book_i_01_review_check.json"
I2_REVIEW_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "002_book_i_02_review_check.json"
I3_REVIEW_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "003_book_i_03_review_check.json"
I4_REVIEW_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "004_book_i_04_review_check.json"
I5_REVIEW_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "005_book_i_05_review_check.json"
I6_REVIEW_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "006_book_i_06_review_check.json"
I7_REVIEW_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "007_book_i_07_review_check.json"
I1_POST_TECHNICAL_RECHECK = (
    PROJECT_ROOT / "qa" / "pretranslation" / "001_book_i_01_post_translation_technical_recheck.json"
)
I2_POST_TECHNICAL_RECHECK = (
    PROJECT_ROOT / "qa" / "pretranslation" / "002_book_i_02_post_translation_technical_recheck.json"
)
I3_POST_TECHNICAL_RECHECK = (
    PROJECT_ROOT / "qa" / "pretranslation" / "003_book_i_03_post_translation_technical_recheck.json"
)
I4_POST_TECHNICAL_RECHECK = (
    PROJECT_ROOT / "qa" / "pretranslation" / "004_book_i_04_post_translation_technical_recheck.json"
)
I5_POST_TECHNICAL_RECHECK = (
    PROJECT_ROOT / "qa" / "pretranslation" / "005_book_i_05_post_translation_technical_recheck.json"
)
I6_POST_TECHNICAL_RECHECK = (
    PROJECT_ROOT / "qa" / "pretranslation" / "006_book_i_06_post_translation_technical_recheck.json"
)
I7_POST_TECHNICAL_RECHECK = (
    PROJECT_ROOT / "qa" / "pretranslation" / "007_book_i_07_post_translation_technical_recheck.json"
)
I1_CHAPTER_QUALITY_GATE = PROJECT_ROOT / "qa" / "pretranslation" / "001_book_i_01_chapter_quality_gate.json"
I2_CHAPTER_QUALITY_GATE = PROJECT_ROOT / "qa" / "pretranslation" / "002_book_i_02_chapter_quality_gate.json"
I3_CHAPTER_QUALITY_GATE = PROJECT_ROOT / "qa" / "pretranslation" / "003_book_i_03_chapter_quality_gate.json"
I4_CHAPTER_QUALITY_GATE = PROJECT_ROOT / "qa" / "pretranslation" / "004_book_i_04_chapter_quality_gate.json"
I5_CHAPTER_QUALITY_GATE = PROJECT_ROOT / "qa" / "pretranslation" / "005_book_i_05_chapter_quality_gate.json"
I6_CHAPTER_QUALITY_GATE = PROJECT_ROOT / "qa" / "pretranslation" / "006_book_i_06_chapter_quality_gate.json"
I7_CHAPTER_QUALITY_GATE = PROJECT_ROOT / "qa" / "pretranslation" / "007_book_i_07_chapter_quality_gate.json"
I8_SOURCE_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "008_book_i_08_source_extraction_check.json"
I8_FORMAL_RECHECK = PROJECT_ROOT / "qa" / "pretranslation" / "008_book_i_08_formal_source_recheck.json"
I8_CONTROL_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "008_book_i_08_chapter_control_check.json"
I8_TRANSLATION_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "008_book_i_08_translation_check.json"
I8_REVIEW_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "008_book_i_08_review_check.json"
I8_POST_TECHNICAL_RECHECK = (
    PROJECT_ROOT / "qa" / "pretranslation" / "008_book_i_08_post_translation_technical_recheck.json"
)
I8_CHAPTER_QUALITY_GATE = PROJECT_ROOT / "qa" / "pretranslation" / "008_book_i_08_chapter_quality_gate.json"
I9_SOURCE_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "009_book_i_09_source_extraction_check.json"
I9_FORMAL_RECHECK = PROJECT_ROOT / "qa" / "pretranslation" / "009_book_i_09_formal_source_recheck.json"
I9_CONTROL_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "009_book_i_09_chapter_control_check.json"
I9_TRANSLATION_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "009_book_i_09_translation_check.json"
I9_REVIEW_CHECK = PROJECT_ROOT / "qa" / "pretranslation" / "009_book_i_09_review_check.json"
I9_POST_TECHNICAL_RECHECK = (
    PROJECT_ROOT / "qa" / "pretranslation" / "009_book_i_09_post_translation_technical_recheck.json"
)
I9_CHAPTER_QUALITY_GATE = PROJECT_ROOT / "qa" / "pretranslation" / "009_book_i_09_chapter_quality_gate.json"


SPECIAL_REQUIREMENTS: dict[int, list[str]] = {
    1: ["philosophical framing check", "title/person-name policy"],
    2: ["whole-work order terminology", "astronomical discipline vocabulary"],
    3: ["spherical motion concept boundary", "observational argument check"],
    4: ["earth-sphericity proof chain", "observation terminology"],
    5: ["geocentric premise check", "proof dependency record"],
    6: ["scale argument check", "point/ratio terminology"],
    7: ["ancient physics vocabulary", "modern concept boundary note"],
    8: ["celestial motion vocabulary", "two-motion distinction"],
    9: ["geometric prerequisite terminology", "Euclidean dependency scan"],
    10: ["trial source formal recheck", "figure label audit already exists"],
    11: ["structured chord table extraction", "sexagesimal numeric validation", "XHTML table strategy"],
    12: ["spherical astronomy diagram audit", "tropic/ecliptic terminology"],
    13: ["spherical proof dependency map", "diagram/table audit"],
    14: ["equator/ecliptic arc relation check", "numeric/diagram audit"],
    15: ["obliquity table extraction", "ancient value preservation", "numeric validation"],
    16: ["right-sphere rising terminology", "cross-reference check"],
}


def i10_formal_recheck_passed() -> bool:
    if not I10_FORMAL_RECHECK.exists():
        return False
    data = json.loads(I10_FORMAL_RECHECK.read_text(encoding="utf-8"))
    return (
        data.get("status") == "PASS_FOR_FORMAL_SOURCE_RECHECK__NOT_FINAL_GATE"
        and data.get("formal_final_allowed") is False
        and data.get("formal_epub_allowed") is False
    )


def i11_table_strategy_passed() -> bool:
    if not I11_TABLE_STRATEGY_CHECK.exists():
        return False
    data = json.loads(I11_TABLE_STRATEGY_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_BOOK_I11_TABLE_STRATEGY__SOURCE_EXTRACTION_PENDING"


def i1_source_extraction_passed() -> bool:
    if not I1_SOURCE_CHECK.exists():
        return False
    data = json.loads(I1_SOURCE_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"


def i2_source_extraction_passed() -> bool:
    if not I2_SOURCE_CHECK.exists():
        return False
    data = json.loads(I2_SOURCE_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"


def i3_source_extraction_passed() -> bool:
    if not I3_SOURCE_CHECK.exists():
        return False
    data = json.loads(I3_SOURCE_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"


def i4_source_extraction_passed() -> bool:
    if not I4_SOURCE_CHECK.exists():
        return False
    data = json.loads(I4_SOURCE_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"


def i5_source_extraction_passed() -> bool:
    if not I5_SOURCE_CHECK.exists():
        return False
    data = json.loads(I5_SOURCE_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"


def i6_source_extraction_passed() -> bool:
    if not I6_SOURCE_CHECK.exists():
        return False
    data = json.loads(I6_SOURCE_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"


def i7_source_extraction_passed() -> bool:
    if not I7_SOURCE_CHECK.exists():
        return False
    data = json.loads(I7_SOURCE_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"


def i1_formal_recheck_passed() -> bool:
    if not I1_FORMAL_RECHECK.exists():
        return False
    data = json.loads(I1_FORMAL_RECHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING"


def i2_formal_recheck_passed() -> bool:
    if not I2_FORMAL_RECHECK.exists():
        return False
    data = json.loads(I2_FORMAL_RECHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING"


def i3_formal_recheck_passed() -> bool:
    if not I3_FORMAL_RECHECK.exists():
        return False
    data = json.loads(I3_FORMAL_RECHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING"


def i4_formal_recheck_passed() -> bool:
    if not I4_FORMAL_RECHECK.exists():
        return False
    data = json.loads(I4_FORMAL_RECHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING"


def i5_formal_recheck_passed() -> bool:
    if not I5_FORMAL_RECHECK.exists():
        return False
    data = json.loads(I5_FORMAL_RECHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING"


def i6_formal_recheck_passed() -> bool:
    if not I6_FORMAL_RECHECK.exists():
        return False
    data = json.loads(I6_FORMAL_RECHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING"


def i7_formal_recheck_passed() -> bool:
    if not I7_FORMAL_RECHECK.exists():
        return False
    data = json.loads(I7_FORMAL_RECHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING"


def i1_chapter_control_passed() -> bool:
    if not I1_CONTROL_CHECK.exists():
        return False
    data = json.loads(I1_CONTROL_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED"


def i2_chapter_control_passed() -> bool:
    if not I2_CONTROL_CHECK.exists():
        return False
    data = json.loads(I2_CONTROL_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED"


def i3_chapter_control_passed() -> bool:
    if not I3_CONTROL_CHECK.exists():
        return False
    data = json.loads(I3_CONTROL_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED"


def i4_chapter_control_passed() -> bool:
    if not I4_CONTROL_CHECK.exists():
        return False
    data = json.loads(I4_CONTROL_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED"


def i5_chapter_control_passed() -> bool:
    if not I5_CONTROL_CHECK.exists():
        return False
    data = json.loads(I5_CONTROL_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED"


def i6_chapter_control_passed() -> bool:
    if not I6_CONTROL_CHECK.exists():
        return False
    data = json.loads(I6_CONTROL_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED"


def i7_chapter_control_passed() -> bool:
    if not I7_CONTROL_CHECK.exists():
        return False
    data = json.loads(I7_CONTROL_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED"


def i1_translation_check_passed() -> bool:
    if not I1_TRANSLATION_CHECK.exists():
        return False
    data = json.loads(I1_TRANSLATION_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_TRANSLATION_DRAFT__REVIEW_PENDING"


def i2_translation_check_passed() -> bool:
    if not I2_TRANSLATION_CHECK.exists():
        return False
    data = json.loads(I2_TRANSLATION_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_TRANSLATION_DRAFT__REVIEW_PENDING"


def i3_translation_check_passed() -> bool:
    if not I3_TRANSLATION_CHECK.exists():
        return False
    data = json.loads(I3_TRANSLATION_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_TRANSLATION_DRAFT__REVIEW_PENDING"


def i4_translation_check_passed() -> bool:
    if not I4_TRANSLATION_CHECK.exists():
        return False
    data = json.loads(I4_TRANSLATION_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_TRANSLATION_DRAFT__REVIEW_PENDING"


def i5_translation_check_passed() -> bool:
    if not I5_TRANSLATION_CHECK.exists():
        return False
    data = json.loads(I5_TRANSLATION_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_TRANSLATION_DRAFT__REVIEW_PENDING"


def i6_translation_check_passed() -> bool:
    if not I6_TRANSLATION_CHECK.exists():
        return False
    data = json.loads(I6_TRANSLATION_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_TRANSLATION_DRAFT__REVIEW_PENDING"


def i7_translation_check_passed() -> bool:
    if not I7_TRANSLATION_CHECK.exists():
        return False
    data = json.loads(I7_TRANSLATION_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_TRANSLATION_DRAFT__REVIEW_PENDING"


def i1_review_check_passed() -> bool:
    if not I1_REVIEW_CHECK.exists():
        return False
    data = json.loads(I1_REVIEW_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_REVIEW__TECHNICAL_RECHECK_PENDING"


def i2_review_check_passed() -> bool:
    if not I2_REVIEW_CHECK.exists():
        return False
    data = json.loads(I2_REVIEW_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_REVIEW__TECHNICAL_RECHECK_PENDING"


def i3_review_check_passed() -> bool:
    if not I3_REVIEW_CHECK.exists():
        return False
    data = json.loads(I3_REVIEW_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_REVIEW__TECHNICAL_RECHECK_PENDING"


def i4_review_check_passed() -> bool:
    if not I4_REVIEW_CHECK.exists():
        return False
    data = json.loads(I4_REVIEW_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_REVIEW__TECHNICAL_RECHECK_PENDING"


def i5_review_check_passed() -> bool:
    if not I5_REVIEW_CHECK.exists():
        return False
    data = json.loads(I5_REVIEW_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_REVIEW__TECHNICAL_RECHECK_PENDING"


def i6_review_check_passed() -> bool:
    if not I6_REVIEW_CHECK.exists():
        return False
    data = json.loads(I6_REVIEW_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_REVIEW__TECHNICAL_RECHECK_PENDING"


def i7_review_check_passed() -> bool:
    if not I7_REVIEW_CHECK.exists():
        return False
    data = json.loads(I7_REVIEW_CHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_REVIEW__TECHNICAL_RECHECK_PENDING"


def i1_post_technical_recheck_passed() -> bool:
    if not I1_POST_TECHNICAL_RECHECK.exists():
        return False
    data = json.loads(I1_POST_TECHNICAL_RECHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING"


def i2_post_technical_recheck_passed() -> bool:
    if not I2_POST_TECHNICAL_RECHECK.exists():
        return False
    data = json.loads(I2_POST_TECHNICAL_RECHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING"


def i3_post_technical_recheck_passed() -> bool:
    if not I3_POST_TECHNICAL_RECHECK.exists():
        return False
    data = json.loads(I3_POST_TECHNICAL_RECHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING"


def i4_post_technical_recheck_passed() -> bool:
    if not I4_POST_TECHNICAL_RECHECK.exists():
        return False
    data = json.loads(I4_POST_TECHNICAL_RECHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING"


def i5_post_technical_recheck_passed() -> bool:
    if not I5_POST_TECHNICAL_RECHECK.exists():
        return False
    data = json.loads(I5_POST_TECHNICAL_RECHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING"


def i6_post_technical_recheck_passed() -> bool:
    if not I6_POST_TECHNICAL_RECHECK.exists():
        return False
    data = json.loads(I6_POST_TECHNICAL_RECHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING"


def i7_post_technical_recheck_passed() -> bool:
    if not I7_POST_TECHNICAL_RECHECK.exists():
        return False
    data = json.loads(I7_POST_TECHNICAL_RECHECK.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING"


def i1_chapter_quality_gate_passed() -> bool:
    if not I1_CHAPTER_QUALITY_GATE.exists():
        return False
    data = json.loads(I1_CHAPTER_QUALITY_GATE.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING"


def i2_chapter_quality_gate_passed() -> bool:
    if not I2_CHAPTER_QUALITY_GATE.exists():
        return False
    data = json.loads(I2_CHAPTER_QUALITY_GATE.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING"


def i3_chapter_quality_gate_passed() -> bool:
    if not I3_CHAPTER_QUALITY_GATE.exists():
        return False
    data = json.loads(I3_CHAPTER_QUALITY_GATE.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING"


def i4_chapter_quality_gate_passed() -> bool:
    if not I4_CHAPTER_QUALITY_GATE.exists():
        return False
    data = json.loads(I4_CHAPTER_QUALITY_GATE.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING"


def i5_chapter_quality_gate_passed() -> bool:
    if not I5_CHAPTER_QUALITY_GATE.exists():
        return False
    data = json.loads(I5_CHAPTER_QUALITY_GATE.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING"


def i6_chapter_quality_gate_passed() -> bool:
    if not I6_CHAPTER_QUALITY_GATE.exists():
        return False
    data = json.loads(I6_CHAPTER_QUALITY_GATE.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING"


def i7_chapter_quality_gate_passed() -> bool:
    if not I7_CHAPTER_QUALITY_GATE.exists():
        return False
    data = json.loads(I7_CHAPTER_QUALITY_GATE.read_text(encoding="utf-8"))
    return data.get("status") == "PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING"


def gate_status(path: Path, expected: str) -> bool:
    if not path.exists():
        return False
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("status") == expected


def readiness_for(
    entry: dict[str, object],
    i1_source_passed: bool,
    i2_source_passed: bool,
    i3_source_passed: bool,
    i4_source_passed: bool,
    i5_source_passed: bool,
    i6_source_passed: bool,
    i7_source_passed: bool,
    i1_recheck_passed: bool,
    i2_recheck_passed: bool,
    i3_recheck_passed: bool,
    i4_recheck_passed: bool,
    i5_recheck_passed: bool,
    i6_recheck_passed: bool,
    i7_recheck_passed: bool,
    i1_control_passed: bool,
    i2_control_passed: bool,
    i3_control_passed: bool,
    i4_control_passed: bool,
    i5_control_passed: bool,
    i6_control_passed: bool,
    i7_control_passed: bool,
    i1_translation_passed: bool,
    i2_translation_passed: bool,
    i3_translation_passed: bool,
    i4_translation_passed: bool,
    i5_translation_passed: bool,
    i6_translation_passed: bool,
    i7_translation_passed: bool,
    i1_review_passed: bool,
    i2_review_passed: bool,
    i3_review_passed: bool,
    i4_review_passed: bool,
    i5_review_passed: bool,
    i6_review_passed: bool,
    i7_review_passed: bool,
    i1_post_technical_passed: bool,
    i2_post_technical_passed: bool,
    i3_post_technical_passed: bool,
    i4_post_technical_passed: bool,
    i5_post_technical_passed: bool,
    i6_post_technical_passed: bool,
    i7_post_technical_passed: bool,
    i1_chapter_gate_passed: bool,
    i2_chapter_gate_passed: bool,
    i3_chapter_gate_passed: bool,
    i4_chapter_gate_passed: bool,
    i5_chapter_gate_passed: bool,
    i6_chapter_gate_passed: bool,
    i7_chapter_gate_passed: bool,
    i10_recheck_passed: bool,
    i11_strategy_passed: bool,
) -> str:
    chapter = int(entry["chapter"])
    if chapter == 8 and gate_status(I8_CHAPTER_QUALITY_GATE, "PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING"):
        return "CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING"
    if chapter == 8 and gate_status(I8_POST_TECHNICAL_RECHECK, "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING"):
        return "TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING"
    if chapter == 8 and gate_status(I8_REVIEW_CHECK, "PASS_REVIEW__TECHNICAL_RECHECK_PENDING"):
        return "REVIEW_PASS__TECHNICAL_RECHECK_PENDING"
    if chapter == 8 and gate_status(I8_TRANSLATION_CHECK, "PASS_TRANSLATION_DRAFT__REVIEW_PENDING"):
        return "TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING"
    if chapter == 8 and gate_status(I8_CONTROL_CHECK, "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED"):
        return "CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED"
    if chapter == 8 and gate_status(I8_FORMAL_RECHECK, "PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING"):
        return "FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING"
    if chapter == 8 and gate_status(I8_SOURCE_CHECK, "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"):
        return "SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"
    if chapter == 9 and gate_status(I9_CHAPTER_QUALITY_GATE, "PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING"):
        return "CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING"
    if chapter == 9 and gate_status(I9_POST_TECHNICAL_RECHECK, "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING"):
        return "TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING"
    if chapter == 9 and gate_status(I9_REVIEW_CHECK, "PASS_REVIEW__TECHNICAL_RECHECK_PENDING"):
        return "REVIEW_PASS__TECHNICAL_RECHECK_PENDING"
    if chapter == 9 and gate_status(I9_TRANSLATION_CHECK, "PASS_TRANSLATION_DRAFT__REVIEW_PENDING"):
        return "TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING"
    if chapter == 9 and gate_status(I9_CONTROL_CHECK, "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED"):
        return "CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED"
    if chapter == 9 and gate_status(I9_FORMAL_RECHECK, "PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING"):
        return "FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING"
    if chapter == 9 and gate_status(I9_SOURCE_CHECK, "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"):
        return "SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"
    if chapter == 10 and gate_status(I10_CHAPTER_QUALITY_GATE, "PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING"):
        return "CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING"
    if chapter == 10 and gate_status(I10_POST_TECHNICAL_RECHECK, "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING"):
        return "TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING"
    if chapter == 10 and gate_status(I10_REVIEW_CHECK, "PASS_REVIEW__TECHNICAL_RECHECK_PENDING"):
        return "REVIEW_PASS__TECHNICAL_RECHECK_PENDING"
    if chapter == 10 and gate_status(I10_TRANSLATION_CHECK, "PASS_TRANSLATION_DRAFT__REVIEW_PENDING"):
        return "TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING"
    if chapter == 10 and gate_status(I10_CONTROL_CHECK, "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED"):
        return "CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED"
    if chapter == 10 and i10_recheck_passed:
        return "FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING"
    if chapter == 10 and gate_status(I10_SOURCE_CHECK, "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"):
        return "SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"
    if int(entry["chapter"]) == 1 and i1_chapter_gate_passed:
        return "CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING"
    if int(entry["chapter"]) == 2 and i2_chapter_gate_passed:
        return "CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING"
    if int(entry["chapter"]) == 3 and i3_chapter_gate_passed:
        return "CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING"
    if int(entry["chapter"]) == 4 and i4_chapter_gate_passed:
        return "CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING"
    if int(entry["chapter"]) == 5 and i5_chapter_gate_passed:
        return "CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING"
    if int(entry["chapter"]) == 6 and i6_chapter_gate_passed:
        return "CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING"
    if int(entry["chapter"]) == 7 and i7_chapter_gate_passed:
        return "CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING"
    if int(entry["chapter"]) == 1 and i1_post_technical_passed:
        return "TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING"
    if int(entry["chapter"]) == 2 and i2_post_technical_passed:
        return "TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING"
    if int(entry["chapter"]) == 3 and i3_post_technical_passed:
        return "TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING"
    if int(entry["chapter"]) == 4 and i4_post_technical_passed:
        return "TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING"
    if int(entry["chapter"]) == 5 and i5_post_technical_passed:
        return "TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING"
    if int(entry["chapter"]) == 6 and i6_post_technical_passed:
        return "TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING"
    if int(entry["chapter"]) == 7 and i7_post_technical_passed:
        return "TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING"
    if int(entry["chapter"]) == 1 and i1_review_passed:
        return "REVIEW_PASS__TECHNICAL_RECHECK_PENDING"
    if int(entry["chapter"]) == 2 and i2_review_passed:
        return "REVIEW_PASS__TECHNICAL_RECHECK_PENDING"
    if int(entry["chapter"]) == 3 and i3_review_passed:
        return "REVIEW_PASS__TECHNICAL_RECHECK_PENDING"
    if int(entry["chapter"]) == 4 and i4_review_passed:
        return "REVIEW_PASS__TECHNICAL_RECHECK_PENDING"
    if int(entry["chapter"]) == 5 and i5_review_passed:
        return "REVIEW_PASS__TECHNICAL_RECHECK_PENDING"
    if int(entry["chapter"]) == 6 and i6_review_passed:
        return "REVIEW_PASS__TECHNICAL_RECHECK_PENDING"
    if int(entry["chapter"]) == 7 and i7_review_passed:
        return "REVIEW_PASS__TECHNICAL_RECHECK_PENDING"
    if int(entry["chapter"]) == 1 and i1_translation_passed:
        return "TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING"
    if int(entry["chapter"]) == 2 and i2_translation_passed:
        return "TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING"
    if int(entry["chapter"]) == 3 and i3_translation_passed:
        return "TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING"
    if int(entry["chapter"]) == 4 and i4_translation_passed:
        return "TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING"
    if int(entry["chapter"]) == 5 and i5_translation_passed:
        return "TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING"
    if int(entry["chapter"]) == 6 and i6_translation_passed:
        return "TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING"
    if int(entry["chapter"]) == 7 and i7_translation_passed:
        return "TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING"
    if int(entry["chapter"]) == 1 and i1_control_passed:
        return "CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED"
    if int(entry["chapter"]) == 2 and i2_control_passed:
        return "CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED"
    if int(entry["chapter"]) == 3 and i3_control_passed:
        return "CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED"
    if int(entry["chapter"]) == 4 and i4_control_passed:
        return "CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED"
    if int(entry["chapter"]) == 5 and i5_control_passed:
        return "CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED"
    if int(entry["chapter"]) == 6 and i6_control_passed:
        return "CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED"
    if int(entry["chapter"]) == 7 and i7_control_passed:
        return "CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED"
    if int(entry["chapter"]) == 1 and i1_recheck_passed:
        return "FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING"
    if int(entry["chapter"]) == 2 and i2_recheck_passed:
        return "FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING"
    if int(entry["chapter"]) == 3 and i3_recheck_passed:
        return "FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING"
    if int(entry["chapter"]) == 4 and i4_recheck_passed:
        return "FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING"
    if int(entry["chapter"]) == 5 and i5_recheck_passed:
        return "FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING"
    if int(entry["chapter"]) == 6 and i6_recheck_passed:
        return "FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING"
    if int(entry["chapter"]) == 7 and i7_recheck_passed:
        return "FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING"
    if int(entry["chapter"]) == 1 and i1_source_passed:
        return "SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"
    if int(entry["chapter"]) == 2 and i2_source_passed:
        return "SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"
    if int(entry["chapter"]) == 3 and i3_source_passed:
        return "SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"
    if int(entry["chapter"]) == 4 and i4_source_passed:
        return "SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"
    if int(entry["chapter"]) == 5 and i5_source_passed:
        return "SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"
    if int(entry["chapter"]) == 6 and i6_source_passed:
        return "SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"
    if int(entry["chapter"]) == 7 and i7_source_passed:
        return "SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"
    if int(entry["chapter"]) == 10 and i10_recheck_passed:
        return "FORMAL_SOURCE_RECHECK_PASS__CHAPTER_TRANSLATION_STILL_GATED"
    if int(entry["chapter"]) == 11 and gate_status(I11_TABLE_REGION_CHECK, "PASS_TABLE_REGIONS_CROPPED__ROW_TRANSCRIPTION_PENDING"):
        return "TABLE_REGIONS_CROPPED__ROW_TRANSCRIPTION_PENDING"
    if int(entry["chapter"]) == 11 and i11_strategy_passed:
        return "TABLE_STRATEGY_PASS__SOURCE_EXTRACTION_PENDING"
    later_source_checks = {
        12: I12_SOURCE_CHECK,
        13: I13_SOURCE_CHECK,
        14: I14_SOURCE_CHECK,
        15: I15_SOURCE_CHECK,
        16: I16_SOURCE_CHECK,
    }
    if chapter in later_source_checks and gate_status(
        later_source_checks[chapter], "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"
    ):
        return "SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"
    if entry["source_split_status"] == "TRIAL_SOURCE_EXISTS__FORMAL_SPLIT_RECHECK_REQUIRED":
        return "READY_FOR_FORMAL_RECHECK_NOT_FINAL"
    return "NOT_READY_SOURCE_EXTRACTION_PENDING"


def blockers_for(
    entry: dict[str, object],
    i1_source_passed: bool,
    i2_source_passed: bool,
    i3_source_passed: bool,
    i4_source_passed: bool,
    i5_source_passed: bool,
    i6_source_passed: bool,
    i7_source_passed: bool,
    i1_recheck_passed: bool,
    i2_recheck_passed: bool,
    i3_recheck_passed: bool,
    i4_recheck_passed: bool,
    i5_recheck_passed: bool,
    i6_recheck_passed: bool,
    i7_recheck_passed: bool,
    i1_control_passed: bool,
    i2_control_passed: bool,
    i3_control_passed: bool,
    i4_control_passed: bool,
    i5_control_passed: bool,
    i6_control_passed: bool,
    i7_control_passed: bool,
    i1_translation_passed: bool,
    i2_translation_passed: bool,
    i3_translation_passed: bool,
    i4_translation_passed: bool,
    i5_translation_passed: bool,
    i6_translation_passed: bool,
    i7_translation_passed: bool,
    i1_review_passed: bool,
    i2_review_passed: bool,
    i3_review_passed: bool,
    i4_review_passed: bool,
    i5_review_passed: bool,
    i6_review_passed: bool,
    i7_review_passed: bool,
    i1_post_technical_passed: bool,
    i2_post_technical_passed: bool,
    i3_post_technical_passed: bool,
    i4_post_technical_passed: bool,
    i5_post_technical_passed: bool,
    i6_post_technical_passed: bool,
    i7_post_technical_passed: bool,
    i1_chapter_gate_passed: bool,
    i2_chapter_gate_passed: bool,
    i3_chapter_gate_passed: bool,
    i4_chapter_gate_passed: bool,
    i5_chapter_gate_passed: bool,
    i6_chapter_gate_passed: bool,
    i7_chapter_gate_passed: bool,
    i10_recheck_passed: bool,
    i11_strategy_passed: bool,
) -> list[str]:
    blockers: list[str] = []
    if int(entry["chapter"]) == 8 and gate_status(I8_CHAPTER_QUALITY_GATE, "PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING"):
        return [
            "chapter quality gate passed",
            "final promotion and full-book consistency review remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 8 and gate_status(
        I8_POST_TECHNICAL_RECHECK,
        "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING",
    ):
        return [
            "post-translation technical recheck passed",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 8 and gate_status(I8_REVIEW_CHECK, "PASS_REVIEW__TECHNICAL_RECHECK_PENDING"):
        return [
            "draft review passed; post-translation technical recheck is still pending",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 8 and gate_status(I8_TRANSLATION_CHECK, "PASS_TRANSLATION_DRAFT__REVIEW_PENDING"):
        return [
            "translation draft exists and passed mechanical checks",
            "fidelity/readability/terminology review and technical recheck are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 8 and gate_status(
        I8_CONTROL_CHECK,
        "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED",
    ):
        return [
            "chapter control passed; controlled translation file may be prepared next",
            "post-translation review, technical recheck, and final gates remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 8 and gate_status(I8_FORMAL_RECHECK, "PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING"):
        return [
            "formal source recheck passed, but chapter control is still required before translation",
            "translation, review, and technical post-checks are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 8 and gate_status(
        I8_SOURCE_CHECK,
        "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING",
    ):
        return [
            "source extraction candidate exists, but formal PDF recheck is still required",
            "chapter control and technical audit must pass before translation",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 9 and gate_status(I9_CHAPTER_QUALITY_GATE, "PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING"):
        return [
            "chapter quality gate passed",
            "final promotion and full-book consistency review remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 9 and gate_status(
        I9_POST_TECHNICAL_RECHECK,
        "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING",
    ):
        return [
            "post-translation technical recheck passed",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 9 and gate_status(I9_REVIEW_CHECK, "PASS_REVIEW__TECHNICAL_RECHECK_PENDING"):
        return [
            "draft review passed; post-translation technical recheck is still pending",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 9 and gate_status(I9_TRANSLATION_CHECK, "PASS_TRANSLATION_DRAFT__REVIEW_PENDING"):
        return [
            "translation draft exists and passed mechanical checks",
            "fidelity/readability/terminology review and technical recheck are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 9 and gate_status(
        I9_CONTROL_CHECK,
        "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED",
    ):
        return [
            "chapter control passed; controlled translation file may be prepared next",
            "post-translation review, technical recheck, and final gates remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 9 and gate_status(I9_FORMAL_RECHECK, "PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING"):
        return [
            "formal source recheck passed, but chapter control is still required before translation",
            "translation, review, and technical post-checks are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 9 and gate_status(
        I9_SOURCE_CHECK,
        "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING",
    ):
        return [
            "source extraction candidate exists, but formal PDF recheck is still required",
            "chapter control and technical audit must pass before translation",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 10 and gate_status(I10_CHAPTER_QUALITY_GATE, "PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING"):
        return [
            "chapter quality gate passed",
            "final promotion and full-book consistency review remain pending",
            "Book I.11 chord table remains excluded",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 10 and gate_status(
        I10_POST_TECHNICAL_RECHECK,
        "PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING",
    ):
        return [
            "post-translation technical recheck passed",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 10 and gate_status(I10_REVIEW_CHECK, "PASS_REVIEW__TECHNICAL_RECHECK_PENDING"):
        return [
            "draft review passed; post-translation technical recheck is still pending",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 10 and gate_status(I10_TRANSLATION_CHECK, "PASS_TRANSLATION_DRAFT__REVIEW_PENDING"):
        return [
            "translation draft exists and passed mechanical checks",
            "fidelity/readability/terminology review and technical recheck are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 10 and gate_status(
        I10_CONTROL_CHECK,
        "PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED",
    ):
        return [
            "chapter control passed; controlled translation file may be prepared next",
            "post-translation review, technical recheck, and final gates remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 10 and gate_status(
        I10_SOURCE_CHECK,
        "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING",
    ):
        return [
            "source extraction candidate exists, but formal PDF recheck is still required",
            "chapter control and technical audit must pass before translation",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 1 and i1_chapter_gate_passed:
        return [
            "chapter quality gate passed",
            "final promotion and full-book consistency review remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 2 and i2_chapter_gate_passed:
        return [
            "chapter quality gate passed",
            "final promotion and full-book consistency review remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 3 and i3_chapter_gate_passed:
        return [
            "chapter quality gate passed",
            "final promotion and full-book consistency review remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 4 and i4_chapter_gate_passed:
        return [
            "chapter quality gate passed",
            "final promotion and full-book consistency review remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 5 and i5_chapter_gate_passed:
        return [
            "chapter quality gate passed",
            "final promotion and full-book consistency review remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 6 and i6_chapter_gate_passed:
        return [
            "chapter quality gate passed",
            "final promotion and full-book consistency review remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 7 and i7_chapter_gate_passed:
        return [
            "chapter quality gate passed",
            "final promotion and full-book consistency review remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 1 and i1_post_technical_passed:
        return [
            "post-translation technical recheck passed",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 2 and i2_post_technical_passed:
        return [
            "post-translation technical recheck passed",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 3 and i3_post_technical_passed:
        return [
            "post-translation technical recheck passed",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 4 and i4_post_technical_passed:
        return [
            "post-translation technical recheck passed",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 5 and i5_post_technical_passed:
        return [
            "post-translation technical recheck passed",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 6 and i6_post_technical_passed:
        return [
            "post-translation technical recheck passed",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 7 and i7_post_technical_passed:
        return [
            "post-translation technical recheck passed",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 1 and i1_review_passed:
        return [
            "draft review passed; post-translation technical recheck is still pending",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 2 and i2_review_passed:
        return [
            "draft review passed; post-translation technical recheck is still pending",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 3 and i3_review_passed:
        return [
            "draft review passed; post-translation technical recheck is still pending",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 4 and i4_review_passed:
        return [
            "draft review passed; post-translation technical recheck is still pending",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 5 and i5_review_passed:
        return [
            "draft review passed; post-translation technical recheck is still pending",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 6 and i6_review_passed:
        return [
            "draft review passed; post-translation technical recheck is still pending",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 7 and i7_review_passed:
        return [
            "draft review passed; post-translation technical recheck is still pending",
            "chapter quality gate and final promotion remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 1 and i1_translation_passed:
        return [
            "translation draft exists and passed mechanical checks",
            "fidelity/readability/terminology review and technical recheck are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 2 and i2_translation_passed:
        return [
            "translation draft exists and passed mechanical checks",
            "fidelity/readability/terminology review and technical recheck are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 3 and i3_translation_passed:
        return [
            "translation draft exists and passed mechanical checks",
            "fidelity/readability/terminology review and technical recheck are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 4 and i4_translation_passed:
        return [
            "translation draft exists and passed mechanical checks",
            "fidelity/readability/terminology review and technical recheck are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 5 and i5_translation_passed:
        return [
            "translation draft exists and passed mechanical checks",
            "fidelity/readability/terminology review and technical recheck are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 6 and i6_translation_passed:
        return [
            "translation draft exists and passed mechanical checks",
            "fidelity/readability/terminology review and technical recheck are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 7 and i7_translation_passed:
        return [
            "translation draft exists and passed mechanical checks",
            "fidelity/readability/terminology review and technical recheck are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 1 and i1_control_passed:
        return [
            "chapter control passed; controlled translation file may be prepared next",
            "post-translation review, technical recheck, and final gates remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 2 and i2_control_passed:
        return [
            "chapter control passed; controlled translation file may be prepared next",
            "post-translation review, technical recheck, and final gates remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 3 and i3_control_passed:
        return [
            "chapter control passed; controlled translation file may be prepared next",
            "post-translation review, technical recheck, and final gates remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 4 and i4_control_passed:
        return [
            "chapter control passed; controlled translation file may be prepared next",
            "post-translation review, technical recheck, and final gates remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 5 and i5_control_passed:
        return [
            "chapter control passed; controlled translation file may be prepared next",
            "post-translation review, technical recheck, and final gates remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 6 and i6_control_passed:
        return [
            "chapter control passed; controlled translation file may be prepared next",
            "post-translation review, technical recheck, and final gates remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 7 and i7_control_passed:
        return [
            "chapter control passed; controlled translation file may be prepared next",
            "post-translation review, technical recheck, and final gates remain pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 1 and i1_recheck_passed:
        return [
            "formal source recheck passed, but chapter control is still required before translation",
            "translation, review, and technical post-checks are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 2 and i2_recheck_passed:
        return [
            "formal source recheck passed, but chapter control is still required before translation",
            "translation, review, and technical post-checks are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 3 and i3_recheck_passed:
        return [
            "formal source recheck passed, but chapter control is still required before translation",
            "translation, review, and technical post-checks are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 4 and i4_recheck_passed:
        return [
            "formal source recheck passed, but chapter control is still required before translation",
            "translation, review, and technical post-checks are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 5 and i5_recheck_passed:
        return [
            "formal source recheck passed, but chapter control is still required before translation",
            "translation, review, and technical post-checks are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 6 and i6_recheck_passed:
        return [
            "formal source recheck passed, but chapter control is still required before translation",
            "translation, review, and technical post-checks are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 7 and i7_recheck_passed:
        return [
            "formal source recheck passed, but chapter control is still required before translation",
            "translation, review, and technical post-checks are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 1 and i1_source_passed:
        return [
            "source extraction candidate exists, but formal PDF recheck is still required",
            "chapter control and technical audit must pass before translation",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 2 and i2_source_passed:
        return [
            "source extraction candidate exists, but formal PDF recheck is still required",
            "chapter control and technical audit must pass before translation",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 3 and i3_source_passed:
        return [
            "source extraction candidate exists, but formal PDF recheck is still required",
            "chapter control and technical audit must pass before translation",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 4 and i4_source_passed:
        return [
            "source extraction candidate exists, but formal PDF recheck is still required",
            "chapter control and technical audit must pass before translation",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 5 and i5_source_passed:
        return [
            "source extraction candidate exists, but formal PDF recheck is still required",
            "chapter control and technical audit must pass before translation",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 6 and i6_source_passed:
        return [
            "source extraction candidate exists, but formal PDF recheck is still required",
            "chapter control and technical audit must pass before translation",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 7 and i7_source_passed:
        return [
            "source extraction candidate exists, but formal PDF recheck is still required",
            "chapter control and technical audit must pass before translation",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 10 and i10_recheck_passed:
        return [
            "formal source recheck passed, but this is not a final-output gate",
            "chapter control, technical re-audit, and full-book pretranslation PASS are still required",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 11 and gate_status(I11_TABLE_REGION_CHECK, "PASS_TABLE_REGIONS_CROPPED__ROW_TRANSCRIPTION_PENDING"):
        return [
            "chord-table page regions are cropped from Heiberg PDF",
            "row-level source transcription and numeric validation are still pending",
            "chapters/final and output/book.epub remain forbidden",
        ]
    if int(entry["chapter"]) == 11 and i11_strategy_passed:
        return [
            "chord-table strategy passed, but row-level source extraction is still pending",
            "structured raw table and numeric validation must pass before translation",
            "chapters/final and output/book.epub remain forbidden",
        ]
    later_source_checks = {
        12: I12_SOURCE_CHECK,
        13: I13_SOURCE_CHECK,
        14: I14_SOURCE_CHECK,
        15: I15_SOURCE_CHECK,
        16: I16_SOURCE_CHECK,
    }
    chapter = int(entry["chapter"])
    if chapter in later_source_checks and gate_status(
        later_source_checks[chapter], "PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"
    ):
        return [
            "source extraction candidate exists, but formal PDF recheck is still required",
            "chapter control and technical audit must pass before translation",
            "chapters/final and output/book.epub remain forbidden",
        ]
    pdf_status = str(entry["pdf_page_mapping_status"])
    if pdf_status.startswith("PASS_FOR_BOOK_I_PRE_RESEARCH_SAMPLE"):
        blockers.append("pre-research PDF sampling must be promoted to formal chapter evidence")
    elif pdf_status == "PASS_FOR_BOOK_I10_TRIAL__FORMAL_RECHECK_REQUIRED":
        blockers.append("trial PDF evidence must be promoted to formal chapter evidence")
    else:
        blockers.append("chapter-specific PDF page verification pending")
    if entry["source_split_status"] != "TRIAL_SOURCE_EXISTS__FORMAL_SPLIT_RECHECK_REQUIRED":
        blockers.append("chapters/src source file not extracted")
    else:
        blockers.append("existing trial source must be rechecked before final source split")
    risk = str(entry["initial_risk"])
    if risk == "TABLE_NUMERIC_HIGH":
        blockers.append("structured table and numeric validation strategy pending")
    if risk == "FOUNDATION_GEOMETRY_HIGH":
        blockers.append("proof/model terminology audit pending")
    return blockers


def load_matrix() -> list[dict[str, object]]:
    data = json.loads(SEGMENTATION.read_text(encoding="utf-8"))
    i1_source_passed = i1_source_extraction_passed()
    i2_source_passed = i2_source_extraction_passed()
    i3_source_passed = i3_source_extraction_passed()
    i4_source_passed = i4_source_extraction_passed()
    i5_source_passed = i5_source_extraction_passed()
    i6_source_passed = i6_source_extraction_passed()
    i7_source_passed = i7_source_extraction_passed()
    i1_recheck_passed = i1_formal_recheck_passed()
    i2_recheck_passed = i2_formal_recheck_passed()
    i3_recheck_passed = i3_formal_recheck_passed()
    i4_recheck_passed = i4_formal_recheck_passed()
    i5_recheck_passed = i5_formal_recheck_passed()
    i6_recheck_passed = i6_formal_recheck_passed()
    i7_recheck_passed = i7_formal_recheck_passed()
    i1_control_passed = i1_chapter_control_passed()
    i2_control_passed = i2_chapter_control_passed()
    i3_control_passed = i3_chapter_control_passed()
    i4_control_passed = i4_chapter_control_passed()
    i5_control_passed = i5_chapter_control_passed()
    i6_control_passed = i6_chapter_control_passed()
    i7_control_passed = i7_chapter_control_passed()
    i1_translation_passed = i1_translation_check_passed()
    i2_translation_passed = i2_translation_check_passed()
    i3_translation_passed = i3_translation_check_passed()
    i4_translation_passed = i4_translation_check_passed()
    i5_translation_passed = i5_translation_check_passed()
    i6_translation_passed = i6_translation_check_passed()
    i7_translation_passed = i7_translation_check_passed()
    i1_review_passed = i1_review_check_passed()
    i2_review_passed = i2_review_check_passed()
    i3_review_passed = i3_review_check_passed()
    i4_review_passed = i4_review_check_passed()
    i5_review_passed = i5_review_check_passed()
    i6_review_passed = i6_review_check_passed()
    i7_review_passed = i7_review_check_passed()
    i1_post_technical_passed = i1_post_technical_recheck_passed()
    i2_post_technical_passed = i2_post_technical_recheck_passed()
    i3_post_technical_passed = i3_post_technical_recheck_passed()
    i4_post_technical_passed = i4_post_technical_recheck_passed()
    i5_post_technical_passed = i5_post_technical_recheck_passed()
    i6_post_technical_passed = i6_post_technical_recheck_passed()
    i7_post_technical_passed = i7_post_technical_recheck_passed()
    i1_chapter_gate_passed = i1_chapter_quality_gate_passed()
    i2_chapter_gate_passed = i2_chapter_quality_gate_passed()
    i3_chapter_gate_passed = i3_chapter_quality_gate_passed()
    i4_chapter_gate_passed = i4_chapter_quality_gate_passed()
    i5_chapter_gate_passed = i5_chapter_quality_gate_passed()
    i6_chapter_gate_passed = i6_chapter_quality_gate_passed()
    i7_chapter_gate_passed = i7_chapter_quality_gate_passed()
    i10_recheck_passed = i10_formal_recheck_passed()
    i11_strategy_passed = i11_table_strategy_passed()
    rows: list[dict[str, object]] = []
    for entry in data["entries"]:
        chapter = int(entry["chapter"])
        rows.append(
            {
                "chapter": chapter,
                "anchor": entry["anchor"],
                "pal_title": entry["pal_title"],
                "initial_risk": entry["initial_risk"],
                "estimated_pdf_viewer_pages": entry["pdf_viewer_pages_estimated"],
                "source_split_status": entry["source_split_status"],
                "pdf_page_mapping_status": entry["pdf_page_mapping_status"],
                "readiness": readiness_for(
                    entry,
                    i1_source_passed,
                    i2_source_passed,
                    i3_source_passed,
                    i4_source_passed,
                    i5_source_passed,
                    i6_source_passed,
                    i7_source_passed,
                    i1_recheck_passed,
                    i2_recheck_passed,
                    i3_recheck_passed,
                    i4_recheck_passed,
                    i5_recheck_passed,
                    i6_recheck_passed,
                    i7_recheck_passed,
                    i1_control_passed,
                    i2_control_passed,
                    i3_control_passed,
                    i4_control_passed,
                    i5_control_passed,
                    i6_control_passed,
                    i7_control_passed,
                    i1_translation_passed,
                    i2_translation_passed,
                    i3_translation_passed,
                    i4_translation_passed,
                    i5_translation_passed,
                    i6_translation_passed,
                    i7_translation_passed,
                    i1_review_passed,
                    i2_review_passed,
                    i3_review_passed,
                    i4_review_passed,
                    i5_review_passed,
                    i6_review_passed,
                    i7_review_passed,
                    i1_post_technical_passed,
                    i2_post_technical_passed,
                    i3_post_technical_passed,
                    i4_post_technical_passed,
                    i5_post_technical_passed,
                    i6_post_technical_passed,
                    i7_post_technical_passed,
                    i1_chapter_gate_passed,
                    i2_chapter_gate_passed,
                    i3_chapter_gate_passed,
                    i4_chapter_gate_passed,
                    i5_chapter_gate_passed,
                    i6_chapter_gate_passed,
                    i7_chapter_gate_passed,
                    i10_recheck_passed,
                    i11_strategy_passed,
                ),
                "required_controls": SPECIAL_REQUIREMENTS.get(chapter, ["chapter-specific technical audit"]),
                "blockers": blockers_for(
                    entry,
                    i1_source_passed,
                    i2_source_passed,
                    i3_source_passed,
                    i4_source_passed,
                    i5_source_passed,
                    i6_source_passed,
                    i7_source_passed,
                    i1_recheck_passed,
                    i2_recheck_passed,
                    i3_recheck_passed,
                    i4_recheck_passed,
                    i5_recheck_passed,
                    i6_recheck_passed,
                    i7_recheck_passed,
                    i1_control_passed,
                    i2_control_passed,
                    i3_control_passed,
                    i4_control_passed,
                    i5_control_passed,
                    i6_control_passed,
                    i7_control_passed,
                    i1_translation_passed,
                    i2_translation_passed,
                    i3_translation_passed,
                    i4_translation_passed,
                    i5_translation_passed,
                    i6_translation_passed,
                    i7_translation_passed,
                    i1_review_passed,
                    i2_review_passed,
                    i3_review_passed,
                    i4_review_passed,
                    i5_review_passed,
                    i6_review_passed,
                    i7_review_passed,
                    i1_post_technical_passed,
                    i2_post_technical_passed,
                    i3_post_technical_passed,
                    i4_post_technical_passed,
                    i5_post_technical_passed,
                    i6_post_technical_passed,
                    i7_post_technical_passed,
                    i1_chapter_gate_passed,
                    i2_chapter_gate_passed,
                    i3_chapter_gate_passed,
                    i4_chapter_gate_passed,
                    i5_chapter_gate_passed,
                    i6_chapter_gate_passed,
                    i7_chapter_gate_passed,
                    i10_recheck_passed,
                    i11_strategy_passed,
                ),
            }
        )
    return rows


def write_markdown(rows: list[dict[str, object]], created: str) -> None:
    ready = [row for row in rows if row["readiness"] == "READY_FOR_FORMAL_RECHECK_NOT_FINAL"]
    recheck_pass = [
        row
        for row in rows
        if row["readiness"] == "FORMAL_SOURCE_RECHECK_PASS__CHAPTER_TRANSLATION_STILL_GATED"
    ]
    source_extracted = [
        row
        for row in rows
        if row["readiness"] == "SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING"
    ]
    source_recheck_pass = [
        row
        for row in rows
        if row["readiness"] == "FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING"
    ]
    control_pass = [
        row
        for row in rows
        if row["readiness"] == "CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED"
    ]
    translation_pass = [
        row
        for row in rows
        if row["readiness"] == "TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING"
    ]
    review_pass = [
        row for row in rows if row["readiness"] == "REVIEW_PASS__TECHNICAL_RECHECK_PENDING"
    ]
    technical_recheck_pass = [
        row
        for row in rows
        if row["readiness"] == "TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING"
    ]
    chapter_gate_pass = [
        row
        for row in rows
        if row["readiness"] == "CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING"
    ]
    table_strategy_pass = [
        row
        for row in rows
        if row["readiness"] == "TABLE_STRATEGY_PASS__SOURCE_EXTRACTION_PENDING"
    ]
    table_regions_cropped = [
        row
        for row in rows
        if row["readiness"] == "TABLE_REGIONS_CROPPED__ROW_TRANSCRIPTION_PENDING"
    ]
    lines = [
        "# Book I 正式 source split 就绪矩阵 / Book I Source Split Readiness Matrix",
        "",
        "readiness_status: `BOOK_I_PRE_RESEARCH_MATRIX_CREATED__SOURCE_SPLIT_PENDING`",
        f"created_at_utc: `{created}`",
        "",
        "## 控制结论",
        "",
        "- 本矩阵用于决定 Book I 每章是否可以从 PAL 辅助转写推进到正式 `chapters/src/*.md`。",
        "- 当前没有任何章节可直接进入 `chapters/final/` 或批量翻译。",
        "- Book I.1-I.10 已通过章节质量门禁；下一步是终稿前全书一致性审校，不得直接进终稿。",
        "- Book I.10 已通过章节质量门禁，但这不是终稿、正式 EPUB 或 Book I.11 弦表门禁。",
        "- Book I.11 已完成弦表区域裁图，但逐行 source extraction 和数值校验仍未完成。",
        "- Book I.15 仍是表格/数值高风险章节，必须先完成结构化表格策略和数值校验。",
        "",
        "## 统计",
        "",
        f"- chapters: `{len(rows)}`",
        f"- source_extracted_pdf_recheck_pending: `{len(source_extracted)}`",
        f"- formal_source_recheck_pass_chapter_control_pending: `{len(source_recheck_pass)}`",
        f"- chapter_control_pass_translation_prep_allowed: `{len(control_pass)}`",
        f"- translation_draft_pass_review_pending: `{len(translation_pass)}`",
        f"- review_pass_technical_recheck_pending: `{len(review_pass)}`",
        f"- technical_recheck_pass_chapter_gate_pending: `{len(technical_recheck_pass)}`",
        f"- chapter_quality_gate_pass_final_promotion_pending: `{len(chapter_gate_pass)}`",
        f"- ready_for_formal_recheck_not_final: `{len(ready)}`",
        f"- formal_source_recheck_pass_not_translation: `{len(recheck_pass)}`",
        f"- table_strategy_pass_source_extraction_pending: `{len(table_strategy_pass)}`",
        f"- table_regions_cropped_row_transcription_pending: `{len(table_regions_cropped)}`",
        f"- source_extraction_pending: `{len(rows) - len(source_extracted) - len(source_recheck_pass) - len(control_pass) - len(translation_pass) - len(review_pass) - len(technical_recheck_pass) - len(chapter_gate_pass) - len(ready) - len(recheck_pass) - len(table_strategy_pass) - len(table_regions_cropped)}`",
        "",
        "## 矩阵",
        "",
        "| chapter | anchor | risk | PDF viewer pages | readiness | required controls | blockers |",
        "|---:|---|---|---|---|---|---|",
    ]
    for row in rows:
        controls = "<br/>".join(str(item) for item in row["required_controls"])
        blockers = "<br/>".join(str(item) for item in row["blockers"])
        lines.append(
            "| {chapter} | {anchor} | {risk} | {pages} | {readiness} | {controls} | {blockers} |".format(
                chapter=row["chapter"],
                anchor=row["anchor"],
                risk=row["initial_risk"],
                pages=row["estimated_pdf_viewer_pages"],
                readiness=row["readiness"],
                controls=controls,
                blockers=blockers,
            )
        )
    lines.extend(
        [
            "",
            "## 下一步",
            "",
            "1. I.1-I.10 进入终稿前全书一致性审校队列；正式预研究 PASS 前不得进终稿。",
            "2. I.11 已有表格区域裁图；下一步是逐页/逐行 raw table source extraction 和数值校验，不是直接翻译。",
            "3. 对 I.12-I.16 建立球面天文学、图表和数值控制，再进入 source extraction。",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = load_matrix()
    created = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(
            {
                "readiness_status": "BOOK_I_PRE_RESEARCH_MATRIX_CREATED__SOURCE_SPLIT_PENDING",
                "created_at_utc": created,
                "source": "source/book_i_segmentation.json",
                "chapter_count": len(rows),
                "rows": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    write_markdown(rows, created)
    print(f"wrote {OUT_JSON.relative_to(PROJECT_ROOT)}")
    print(f"wrote {OUT_MD.relative_to(PROJECT_ROOT)}")
    print(f"chapters={len(rows)}")


if __name__ == "__main__":
    main()
