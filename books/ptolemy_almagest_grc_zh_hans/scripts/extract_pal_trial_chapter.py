from __future__ import annotations

import hashlib
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PAL_XML = PROJECT_ROOT / "source" / "transcriptions" / "pal_heiberg" / "pal_heiberg_mathematike_syntaxis_1.xml"
OUT = PROJECT_ROOT / "chapters" / "src" / "010_book_i_10_chords.md"
TRIAL_TOC = PROJECT_ROOT / "source" / "trial_toc.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def extract_between(text: str, start_id: str, next_id: str) -> str:
    start = re.search(rf'<h3\s+id="{re.escape(start_id)}"', text)
    end = re.search(rf'<h3\s+id="{re.escape(next_id)}"', text)
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


def main() -> None:
    raw = PAL_XML.read_text(encoding="utf-8")
    chunk = extract_between(raw, "I.10", "I.11")
    marked = clean_pal_html(chunk)
    plain = remove_markers(marked)
    markers = re.findall(r"\[I_[^\]]+\]", marked)
    pages = re.findall(r"\[PAL_PAGE ([^\]]+)\]", marked)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    TRIAL_TOC.parent.mkdir(parents=True, exist_ok=True)

    out_text = f"""# Book I.10: On the Lengths of Straight Lines in the Circle

source_status: `TRIAL_SOURCE_EXTRACTED_FROM_PAL_AUXILIARY_TRANSCRIPTION`
translation_status: `NOT_TRANSLATED`
formal_translation_scope: `TRIAL_CHAPTER_ONLY`

## Source Control

| field | value |
|---|---|
| work | Ptolemy, Mathematical Syntaxis / Almagest |
| book_chapter | Book I.10 |
| Greek_title | ιʹ. Περὶ τῆς πηλικότητος τῶν ἐν τῷ κύκλῳ εὐθειῶν. |
| working_Chinese_title | 圆内直线大小之论 / 弦长论 |
| primary_facsimile | `source/facsimile/Almagest_Complete_Heiberg_1898.pdf` |
| auxiliary_transcription | `source/transcriptions/pal_heiberg/pal_heiberg_mathematike_syntaxis_1.xml` |
| auxiliary_license | PAL transcription license recorded as CC BY 4.0, see `source/transcriptions/pal_heiberg/LICENSE.md` |
| pal_xml_sha256 | `{sha256(PAL_XML)}` |
| extracted_at_utc | `{datetime.now(timezone.utc).replace(microsecond=0).isoformat()}` |
| start_marker | `I_31_7` |
| end_before | `I_48` / `<h3 id="I.11">` |
| marker_count | `{len(markers)}` |
| pal_page_markers_seen | `{", ".join(pages) if pages else "none in extracted range"}` |
| pdf_page_mapping_status | `PENDING_VISUAL_VERIFICATION` |

## Use Rules

- This file is a trial source file, not a final source split for the whole book.
- Translate from the Greek text below, not from a modern reference translation.
- Use any English translation only as a reference witness for difficult readings and technical checking.
- Do not move this chapter to `chapters/final/` until the trial chapter gate, math/astronomy audit, and figure/table audit pass.
- PDF facsimile page and diagram checks remain required before this chapter can pass review.

## PAL Source With Markers

```grc
{marked}
```

## Plain Greek Working Text

```grc
{plain}
```
"""
    OUT.write_text(out_text, encoding="utf-8")

    toc = {
        "toc_status": "TRIAL_ONLY_NOT_FULL_SOURCE_SPLIT",
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source": "PAL Heiberg transcription, auxiliary source control",
        "full_book_split_allowed": False,
        "chapters": [
            {
                "id": "010_book_i_10_chords",
                "book": "I",
                "chapter": "10",
                "source_file": "chapters/src/010_book_i_10_chords.md",
                "pal_start_marker": "I_31_7",
                "pal_end_before": "I_48",
                "pdf_page_mapping_status": "PENDING_VISUAL_VERIFICATION",
                "translation_status": "NOT_TRANSLATED",
                "review_status": "NOT_STARTED",
            }
        ],
    }
    TRIAL_TOC.write_text(json.dumps(toc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
