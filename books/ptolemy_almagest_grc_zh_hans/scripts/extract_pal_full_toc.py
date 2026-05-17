from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PAL_XML = PROJECT_ROOT / "source" / "transcriptions" / "pal_heiberg" / "pal_heiberg_mathematike_syntaxis_1.xml"
OUT_JSON = PROJECT_ROOT / "source" / "full_toc_draft.json"
OUT_MD = PROJECT_ROOT / "source" / "full_book_translation_outline.md"


ROMAN_ORDER = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
    "IX": 9,
    "X": 10,
    "XI": 11,
    "XII": 12,
    "XIII": 13,
}


def clean_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value


def iter_toc_entries(root: ET.Element) -> list[dict[str, object]]:
    nav = root.find(".//nav")
    if nav is None:
        raise RuntimeError("PAL XML does not contain a nav table of contents")

    entries: list[dict[str, object]] = []
    current_book: str | None = None
    for p in nav.findall("./p"):
        klass = p.attrib.get("class", "")
        a = p.find("./a")
        if a is None:
            continue
        href = a.attrib.get("href", "")
        if not href.startswith("#"):
            continue
        anchor = href[1:]
        title = clean_text("".join(a.itertext()))
        if klass == "toc_entry_main":
            current_book = anchor
            entries.append(
                {
                    "type": "book",
                    "book": current_book,
                    "book_number": ROMAN_ORDER.get(current_book),
                    "anchor": anchor,
                    "pal_title": title,
                }
            )
            continue
        if klass == "toc_entry_minor":
            match = re.match(r"^([IVX]+)\.(\d+)$", anchor)
            if not match:
                entries.append(
                    {
                        "type": "chapter",
                        "book": current_book,
                        "chapter": None,
                        "anchor": anchor,
                        "pal_title": title,
                        "status": "ANCHOR_REQUIRES_REVIEW",
                    }
                )
                continue
            book, chapter = match.groups()
            entries.append(
                {
                    "type": "chapter",
                    "book": book,
                    "book_number": ROMAN_ORDER.get(book),
                    "chapter": int(chapter),
                    "anchor": anchor,
                    "pal_title": title,
                    "status": "DRAFT_FROM_PAL_TOC_NOT_FORMAL_SOURCE_SPLIT",
                }
            )
    return entries


def risk_for(book: str, title: str) -> str:
    lower = title.lower()
    table_markers = ["κανόν", "κανὼν", "κανόνιον", "ἔκθεσις κανονικὴ"]
    if any(marker in lower for marker in table_markers):
        return "TABLE_NUMERIC_HIGH"
    if book in {"III", "IV", "V", "VI", "IX", "X", "XI", "XII", "XIII"}:
        return "MODEL_NUMERIC_HIGH"
    if book in {"VII", "VIII"}:
        return "STAR_CATALOG_HIGH"
    if book in {"I", "II"}:
        return "FOUNDATION_GEOMETRY_HIGH"
    return "HIGH_REVIEW_REQUIRED"


def write_markdown(entries: list[dict[str, object]], created: str) -> None:
    chapters = [entry for entry in entries if entry["type"] == "chapter"]
    lines = [
        "# 《Almagest》全书翻译总纲目录草案 / Full-Book Translation Outline Draft",
        "",
        "outline_status: `DRAFT_FROM_PAL_TOC_NOT_FORMAL_SOURCE_SPLIT`",
        f"created_at_utc: `{created}`",
        "",
        "## 控制说明",
        "",
        "- 本文件由 PAL Heiberg 古希腊转写目录自动抽取，只作为全书预研究和正式分章计划骨架。",
        "- 本文件不是正式 `chapters/src/*.md` 底稿；正式分章仍必须回到 Heiberg PDF 页图和 PAL 标记核验。",
        "- 英译本只能作为 reference witness，不得用于生成本目录或章节译文。",
        "- 每章进入翻译前必须有 source 文件、章节控制、技术审计路径和图表/表格/数值风险判定。",
        "",
        "## 统计",
        "",
        f"- books: `{len([entry for entry in entries if entry['type'] == 'book'])}`",
        f"- chapters: `{len(chapters)}`",
        "",
        "## 全书目录与风险分级",
        "",
        "| book | chapter | PAL title | initial risk | source split status |",
        "|---|---:|---|---|---|",
    ]
    for entry in chapters:
        book = str(entry["book"])
        title = str(entry["pal_title"])
        lines.append(
            f"| {book} | {entry['chapter']} | {title} | {risk_for(book, title)} | {entry['status']} |"
        )
    lines.extend(
        [
            "",
            "## 下一步",
            "",
            "1. 逐 Book 建立 `source/book_{roman}_segmentation.md`，确认 PAL anchor、Heiberg 页码和 PDF viewer page 范围。",
            "2. 按风险分级优先处理 Book I、Book II、弦表、星表、行星模型和所有 `TABLE_NUMERIC_HIGH` 章节。",
            "3. 每章正式抽取到 `chapters/src/` 前，必须记录来源角色、PAL 起止标记、PDF 页图核验状态和图表/表格风险。",
            "4. 每章翻译后必须完成 `qa/chapter_controls/`、技术审计、图表/表格审计和章节门禁，PASS 后才可进入 `chapters/final/`。",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    root = ET.fromstring(PAL_XML.read_text(encoding="utf-8"))
    created = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    entries = iter_toc_entries(root)
    chapters = [entry for entry in entries if entry["type"] == "chapter"]
    for entry in chapters:
        entry["initial_risk"] = risk_for(str(entry["book"]), str(entry["pal_title"]))
    OUT_JSON.write_text(
        json.dumps(
            {
                "toc_status": "DRAFT_FROM_PAL_TOC_NOT_FORMAL_SOURCE_SPLIT",
                "created_at_utc": created,
                "source": "PAL Heiberg auxiliary Greek transcription",
                "primary_facsimile_required_for_formal_split": True,
                "reference_translation_role": "reference witness only, not source for TOC or translation",
                "book_count": len([entry for entry in entries if entry["type"] == "book"]),
                "chapter_count": len(chapters),
                "entries": entries,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    write_markdown(entries, created)
    print(f"wrote {OUT_JSON.relative_to(PROJECT_ROOT)}")
    print(f"wrote {OUT_MD.relative_to(PROJECT_ROOT)}")
    print(f"books={len([entry for entry in entries if entry['type'] == 'book'])} chapters={len(chapters)}")


if __name__ == "__main__":
    main()
