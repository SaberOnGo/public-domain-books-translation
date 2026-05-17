from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PAL_XML = PROJECT_ROOT / "source" / "transcriptions" / "pal_heiberg" / "pal_heiberg_mathematike_syntaxis_1.xml"
FULL_TOC = PROJECT_ROOT / "source" / "full_toc_draft.json"


BOOK_SLUGS = {
    "I": "i",
    "II": "ii",
    "III": "iii",
    "IV": "iv",
    "V": "v",
    "VI": "vi",
    "VII": "vii",
    "VIII": "viii",
    "IX": "ix",
    "X": "x",
    "XI": "xi",
    "XII": "xii",
    "XIII": "xiii",
}


def load_chapters(book: str) -> list[dict[str, object]]:
    data = json.loads(FULL_TOC.read_text(encoding="utf-8"))
    chapters = [
        entry
        for entry in data["entries"]
        if entry.get("type") == "chapter" and entry.get("book") == book
    ]
    if not chapters:
        raise RuntimeError(f"No chapters for book {book} in {FULL_TOC}")
    return chapters


def find_heading_positions(raw: str) -> dict[str, int]:
    positions: dict[str, int] = {}
    for match in re.finditer(r'<h([23])\s+id="([^"]+)"', raw):
        positions[match.group(2)] = match.start()
    return positions


def page_markers(chunk: str) -> list[str]:
    markers = re.findall(r'<span\s+class="pagina"\s+data-prae="/([^"]+)/"', chunk)
    return markers


def reserve_markers(chunk: str) -> list[str]:
    markers = re.findall(r'data-reserve="\|([^|]+)\|"', chunk)
    return markers


def first_or_empty(items: list[str]) -> str:
    return items[0] if items else ""


def last_or_empty(items: list[str]) -> str:
    return items[-1] if items else ""


def heiberg_page_number(marker: str) -> int | None:
    match = re.search(r"_(\d+)$", marker)
    return int(match.group(1)) if match else None


def estimated_viewer_page(marker: str) -> int | None:
    page = heiberg_page_number(marker)
    if page is None:
        return None
    # Book I page-image sampling shows viewer page 6 contains printed pages 4-5,
    # viewer page 19 contains pages 30-31, and viewer page 50 begins Book II.
    return (page + 8) // 2


def format_viewer_range(first_marker: str, last_marker: str) -> str:
    first = estimated_viewer_page(first_marker)
    last = estimated_viewer_page(last_marker)
    if first is None or last is None:
        return "PENDING"
    return str(first) if first == last else f"{first}-{last}"


def escape_table(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def pdf_status(book: str, chapter: int) -> str:
    if book == "I" and chapter == 10:
        return "PASS_FOR_BOOK_I10_TRIAL__FORMAL_RECHECK_REQUIRED"
    if book == "I":
        return "PASS_FOR_BOOK_I_PRE_RESEARCH_SAMPLE__FORMAL_RECHECK_REQUIRED"
    return "PENDING_PDF_PAGE_VERIFICATION"


def source_status(book: str, chapter: int) -> str:
    if book == "I" and chapter == 10:
        return "TRIAL_SOURCE_EXISTS__FORMAL_SPLIT_RECHECK_REQUIRED"
    return "PAL_BOUNDARY_IDENTIFIED__CHAPTER_SOURCE_NOT_EXTRACTED"


def output_paths(book: str) -> tuple[Path, Path]:
    slug = BOOK_SLUGS.get(book)
    if slug is None:
        raise RuntimeError(f"Unsupported book label: {book}")
    return (
        PROJECT_ROOT / "source" / f"book_{slug}_segmentation.json",
        PROJECT_ROOT / "source" / f"book_{slug}_segmentation.md",
    )


def build_segmentation(book: str) -> dict[str, object]:
    raw = PAL_XML.read_text(encoding="utf-8")
    positions = find_heading_positions(raw)
    chapters = load_chapters(book)
    entries: list[dict[str, object]] = []
    for index, chapter in enumerate(chapters):
        anchor = str(chapter["anchor"])
        next_anchor = str(chapters[index + 1]["anchor"]) if index + 1 < len(chapters) else None
        start = positions.get(anchor)
        if start is None:
            raise RuntimeError(f"Cannot locate heading {anchor} in PAL XML")
        if next_anchor:
            end = positions.get(next_anchor)
        else:
            next_book_number = int(chapter["book_number"]) + 1
            next_book = None
            for candidate, number in {
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
            }.items():
                if number == next_book_number:
                    next_book = candidate
                    break
            end = positions.get(str(next_book)) if next_book else len(raw)
        if end is None or end <= start:
            raise RuntimeError(f"Cannot locate end boundary for {anchor}")
        chunk = raw[start:end]
        pages = page_markers(chunk)
        reserves = reserve_markers(chunk)
        entries.append(
            {
                "book": book,
                "chapter": chapter["chapter"],
                "anchor": anchor,
                "next_anchor_or_book": next_anchor or "NEXT_BOOK_OR_EOF",
                "pal_title": chapter["pal_title"],
                "initial_risk": chapter.get("initial_risk", "HIGH_REVIEW_REQUIRED"),
                "pal_page_first": first_or_empty(pages),
                "pal_page_last": last_or_empty(pages),
                "pdf_viewer_pages_estimated": format_viewer_range(first_or_empty(pages), last_or_empty(pages)),
                "reserve_marker_first": first_or_empty(reserves),
                "reserve_marker_last": last_or_empty(reserves),
                "reserve_marker_count": len(reserves),
                "pdf_page_mapping_status": pdf_status(book, int(chapter["chapter"])),
                "source_split_status": source_status(book, int(chapter["chapter"])),
            }
        )
    return {
        "segmentation_status": "PAL_BOUNDARIES_IDENTIFIED__PDF_VERIFICATION_PENDING",
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "book": book,
        "chapter_count": len(entries),
        "primary_facsimile_required": True,
        "auxiliary_transcription": "source/transcriptions/pal_heiberg/pal_heiberg_mathematike_syntaxis_1.xml",
        "reference_translation_role": "reference witness only, not segmentation authority",
        "entries": entries,
    }


def write_markdown(data: dict[str, object], out_md: Path) -> None:
    entries = data["entries"]
    lines = [
        f"# Book {data['book']} 分章控制 / Book {data['book']} Segmentation Control",
        "",
        f"segmentation_status: `{data['segmentation_status']}`",
        f"created_at_utc: `{data['created_at_utc']}`",
        "",
        "## 控制结论",
        "",
        "- 本文件记录 PAL 古希腊转写中的章节边界、页标和 marker 范围。",
        "- 本文件仍不是最终 `chapters/src` 底稿；每章正式 source extraction 前必须回查 Heiberg PDF 页图。",
        "- 英译本不得作为分章 authority，只能在疑难理解阶段作为 reference witness。",
        "- `PASS_FOR_BOOK_I_PRE_RESEARCH_SAMPLE__FORMAL_RECHECK_REQUIRED` 只表示本轮已有页图抽样证据；章节正式 source extraction 前仍必须做章节级复核。",
        "",
        "## 分章表",
        "",
        "| chapter | anchor | PAL title | risk | PAL pages | estimated PDF viewer pages | reserve markers | PDF status | source status |",
        "|---:|---|---|---|---|---|---|---|---|",
    ]
    for entry in entries:
        pages = f"{entry['pal_page_first']}..{entry['pal_page_last']}".strip(".")
        reserves = f"{entry['reserve_marker_first']}..{entry['reserve_marker_last']} ({entry['reserve_marker_count']})"
        lines.append(
            "| {chapter} | {anchor} | {title} | {risk} | {pages} | {viewer_pages} | {reserves} | {pdf} | {source} |".format(
                chapter=entry["chapter"],
                anchor=entry["anchor"],
                title=escape_table(entry["pal_title"]),
                risk=entry["initial_risk"],
                pages=escape_table(pages or "NO_PAGE_MARKER_IN_CHUNK"),
                viewer_pages=entry["pdf_viewer_pages_estimated"],
                reserves=escape_table(reserves),
                pdf=entry["pdf_page_mapping_status"],
                source=entry["source_split_status"],
            )
        )
    lines.extend(
        [
            "",
            "## 下一步",
            "",
            "1. 对每章执行章节级 PDF 复核，把预研究估算页码升级为正式 source extraction 证据。",
            "2. 对涉及图表、表格、证明和数值的章节补齐 `qa/technical/` 对应记录。",
            "3. 章节级 PDF 页图、PAL 边界和 QA 路由都通过后，才可生成正式 `chapters/src/*.md`。",
        ]
    )
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    book = "I"
    data = build_segmentation(book)
    out_json, out_md = output_paths(book)
    out_json.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(data, out_md)
    print(f"wrote {out_json.relative_to(PROJECT_ROOT)}")
    print(f"wrote {out_md.relative_to(PROJECT_ROOT)}")
    print(f"book={book} chapters={data['chapter_count']}")


if __name__ == "__main__":
    main()
