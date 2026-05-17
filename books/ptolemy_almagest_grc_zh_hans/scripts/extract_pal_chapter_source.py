from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PAL_XML = PROJECT_ROOT / "source" / "transcriptions" / "pal_heiberg" / "pal_heiberg_mathematike_syntaxis_1.xml"
FULL_TOC = PROJECT_ROOT / "source" / "full_toc_draft.json"
BOOK_I_SEGMENTATION = PROJECT_ROOT / "source" / "book_i_segmentation.json"


CHAPTER_OUTPUTS = {
    "I.1": {
        "path": "chapters/src/001_book_i_01_proem.md",
        "english_title": "Book I.1: Proem",
        "working_Chinese_title": "序言",
    },
    "I.2": {
        "path": "chapters/src/002_book_i_02_order_of_the_theorems.md",
        "english_title": "Book I.2: On the Order of the Theorems",
        "working_Chinese_title": "论诸定理的次序",
    },
    "I.3": {
        "path": "chapters/src/003_book_i_03_heaven_moves_spherically.md",
        "english_title": "Book I.3: That the Heaven Moves Spherically",
        "working_Chinese_title": "论天以球形方式运动",
    },
    "I.4": {
        "path": "chapters/src/004_book_i_04_earth_is_spherical.md",
        "english_title": "Book I.4: That the Earth Also Is Spherical to Sense, as to Its Whole Parts",
        "working_Chinese_title": "论地球按整体各部分看也是球形的",
    },
    "I.5": {
        "path": "chapters/src/005_book_i_05_earth_is_central.md",
        "english_title": "Book I.5: That the Earth Is in the Middle of the Heaven",
        "working_Chinese_title": "论地球位于天的中央",
    },
    "I.6": {
        "path": "chapters/src/006_book_i_06_earth_as_point_to_heavens.md",
        "english_title": "Book I.6: That the Earth Has the Ratio of a Point to the Heavenly Bodies",
        "working_Chinese_title": "论地球相对于天体只相当于一点",
    },
    "I.7": {
        "path": "chapters/src/007_book_i_07_earth_has_no_translational_motion.md",
        "english_title": "Book I.7: That the Earth Makes No Translational Motion",
        "working_Chinese_title": "论地球没有平移运动",
    },
    "I.8": {
        "path": "chapters/src/008_book_i_08_two_primary_motions.md",
        "english_title": "Book I.8: That There Are Two Differences of the Primary Motions",
        "working_Chinese_title": "论最初运动有两种差别",
    },
    "I.9": {
        "path": "chapters/src/009_book_i_09_on_individual_preliminaries.md",
        "english_title": "Book I.9: On the Individual Preliminaries",
        "working_Chinese_title": "论各项具体测定",
    },
    "I.10": {
        "path": "chapters/src/010_book_i_10_chords.md",
        "english_title": "Book I.10: On the Magnitudes of the Straight Lines in the Circle",
        "working_Chinese_title": "论圆内直线的量",
    },
    "I.11": {
        "path": "chapters/src/011_book_i_11_chord_table.md",
        "english_title": "Book I.11: Table of the Straight Lines in the Circle",
        "working_Chinese_title": "圆内直线表",
    },
    "I.12": {
        "path": "chapters/src/012_book_i_12_arc_between_tropics.md",
        "english_title": "Book I.12: On the Arc between the Tropics",
        "working_Chinese_title": "论二至圈之间的弧",
    },
    "I.13": {
        "path": "chapters/src/013_book_i_13_preliminaries_for_spherical_proofs.md",
        "english_title": "Book I.13: Preliminaries for the Spherical Proofs",
        "working_Chinese_title": "球面证明的预备",
    },
    "I.14": {
        "path": "chapters/src/014_book_i_14_arcs_between_equator_and_ecliptic.md",
        "english_title": "Book I.14: On the Arcs between the Equator and the Oblique Circle",
        "working_Chinese_title": "论赤道圈与黄道斜圈之间的弧",
    },
    "I.15": {
        "path": "chapters/src/015_book_i_15_obliquity_table.md",
        "english_title": "Book I.15: Table of Obliquity",
        "working_Chinese_title": "黄道倾斜表",
    },
    "I.16": {
        "path": "chapters/src/016_book_i_16_risings_on_right_sphere.md",
        "english_title": "Book I.16: On Risings on the Right Sphere",
        "working_Chinese_title": "论正球上的升起",
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_toc_entry(anchor: str) -> dict[str, object]:
    data = json.loads(FULL_TOC.read_text(encoding="utf-8"))
    for entry in data["entries"]:
        if entry.get("type") == "chapter" and entry.get("anchor") == anchor:
            return entry
    raise RuntimeError(f"Cannot locate TOC entry for {anchor}")


def load_segmentation_entry(anchor: str) -> dict[str, object]:
    if anchor.startswith("I."):
        data = json.loads(BOOK_I_SEGMENTATION.read_text(encoding="utf-8"))
        for entry in data["entries"]:
            if entry.get("anchor") == anchor:
                return entry
    raise RuntimeError(f"Cannot locate segmentation entry for {anchor}")


def extract_between(text: str, start_id: str, next_id: str) -> str:
    start = re.search(rf'<h3\s+id="{re.escape(start_id)}"', text)
    end = re.search(rf'<h[23]\s+id="{re.escape(next_id)}"', text)
    if not start or not end or end.start() <= start.start():
        raise RuntimeError(f"Cannot locate chapter range {start_id} -> {next_id}")
    return text[start.start() : end.start()]


def clean_pal_html(chunk: str) -> str:
    chunk = re.sub(
        r'<span\s+class="pagina"\s+data-prae="/([^"]+)/"\s+id="[^"]+">\s*</span>',
        r"\n\n[PAL_PAGE \1]\n\n",
        chunk,
    )
    chunk = re.sub(r'<span\s+data-reserve="\|([^|]+)\|">\s*</span>', r"[\1] ", chunk)
    chunk = re.sub(r'<a\s+[^>]*>\s*</a>', "", chunk)
    chunk = re.sub(r'<u\s+class="num">([^<]+)</u>', r"\1", chunk)
    chunk = re.sub(r"</h3\s*>", "\n\n", chunk)
    chunk = re.sub(r'<h3\s+id="[^"]*">', "## ", chunk)
    chunk = re.sub(r"</p\s*>", "\n\n", chunk)
    chunk = re.sub(r"<p\s*>", "", chunk)
    chunk = re.sub(r"<[^>]+>", "", chunk)
    chunk = html.unescape(chunk)
    chunk = re.sub(r"[ \t]+", " ", chunk)
    chunk = re.sub(r" *\n *", "\n", chunk)
    chunk = re.sub(r"\n{3,}", "\n\n", chunk)
    return chunk.strip()


def remove_markers(marked: str) -> str:
    plain = re.sub(r"\[PAL_PAGE [^\]]+\]\s*", "", marked)
    plain = re.sub(r"\[I_[^\]]+\]\s*", "", plain)
    plain = re.sub(r"\n{3,}", "\n\n", plain)
    return plain.strip()


def output_path(anchor: str, explicit_out: str | None) -> Path:
    if explicit_out:
        return PROJECT_ROOT / explicit_out
    config = CHAPTER_OUTPUTS.get(anchor)
    if not config:
        raise RuntimeError(f"No default output mapping for {anchor}; pass --out")
    return PROJECT_ROOT / str(config["path"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract one PAL Greek chapter source file.")
    parser.add_argument("--anchor", required=True, help="Chapter anchor such as I.1")
    parser.add_argument("--out", help="Output path relative to the book project root")
    args = parser.parse_args()

    toc_entry = load_toc_entry(args.anchor)
    segmentation = load_segmentation_entry(args.anchor)
    next_anchor = str(segmentation["next_anchor_or_book"])
    if next_anchor == "NEXT_BOOK_OR_EOF":
        next_anchor = "II"

    raw = PAL_XML.read_text(encoding="utf-8")
    chunk = extract_between(raw, args.anchor, next_anchor)
    marked = clean_pal_html(chunk)
    plain = remove_markers(marked)
    markers = re.findall(r"\[I_[^\]]+\]", marked)
    pages = re.findall(r"\[PAL_PAGE ([^\]]+)\]", marked)
    out = output_path(args.anchor, args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    config = CHAPTER_OUTPUTS.get(args.anchor, {})
    english_title = str(config.get("english_title", f"Book {args.anchor}"))
    chinese_title = str(config.get("working_Chinese_title", "中文题名待定"))
    created = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    out_text = f"""# {english_title}

source_status: `FORMAL_SOURCE_EXTRACTED_FROM_PAL_AUXILIARY_TRANSCRIPTION__PDF_RECHECK_REQUIRED`
translation_status: `NOT_TRANSLATED`
formal_translation_scope: `SOURCE_ONLY_NOT_TRANSLATION`

## Source Control

| field | value |
|---|---|
| work | Ptolemy, Mathematical Syntaxis / Almagest |
| book_chapter | Book {args.anchor} |
| Greek_title | {toc_entry["pal_title"]} |
| working_Chinese_title | {chinese_title} |
| primary_facsimile | `source/facsimile/Almagest_Complete_Heiberg_1898.pdf` |
| auxiliary_transcription | `source/transcriptions/pal_heiberg/pal_heiberg_mathematike_syntaxis_1.xml` |
| auxiliary_license | PAL transcription license recorded as CC BY 4.0, see `source/transcriptions/pal_heiberg/LICENSE.md` |
| pal_xml_sha256 | `{sha256(PAL_XML)}` |
| extracted_at_utc | `{created}` |
| start_marker | `{segmentation["reserve_marker_first"]}` |
| end_before | `{next_anchor}` |
| marker_count | `{len(markers)}` |
| pal_page_markers_seen | `{", ".join(pages) if pages else "none in extracted range"}` |
| estimated_pdf_viewer_pages | `{segmentation["pdf_viewer_pages_estimated"]}` |
| pdf_page_mapping_status | `{segmentation["pdf_page_mapping_status"]}` |
| source_split_status_before_extraction | `{segmentation["source_split_status"]}` |

## Use Rules

- This file is a formal source-extraction candidate, not a translation and not a final chapter.
- Translate only from the Greek text below after chapter controls and technical QA are created.
- Use English translations only as reference witnesses for difficult readings and technical checking.
- Do not move this chapter to `chapters/final/` until translation, chapter control, reviews, and technical audits pass.
- Heiberg PDF facsimile page checks remain required before this chapter can be promoted beyond source extraction.

## PAL Source With Markers

```grc
{marked}
```

## Plain Greek Working Text

```grc
{plain}
```
"""
    out.write_text(out_text, encoding="utf-8")
    print(f"wrote {out.relative_to(PROJECT_ROOT)} anchor={args.anchor} markers={len(markers)}")


if __name__ == "__main__":
    main()
