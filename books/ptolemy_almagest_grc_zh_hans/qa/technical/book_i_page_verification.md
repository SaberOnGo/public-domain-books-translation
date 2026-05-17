# Book I 核页记录 / Book I Page Verification

verification_status: `BOOK_I_PAL_BOUNDARIES_AND_PDF_SAMPLING_DRAFT__SOURCE_SPLIT_OPEN`

## 已完成 / Completed

| check | result | evidence |
|---|---|---|
| PDF downloaded | PASS | `source/facsimile/Almagest_Complete_Heiberg_1898.pdf` |
| SHA256 recorded | PASS | `b5115c91265e7997236d54bb6e421eff6308ef3639681e4a6ab6bcfc37a1c32b` |
| page count control | PASS_FOR_RESEARCH | PDF internal page tree maximum `/Count` = `589` |
| Book I chapter structure | PASS_FOR_RESEARCH | PAL Heiberg transcription page shows Book I chapter sequence; use as segmentation reference only |
| Browser PDF rendering | PASS_FOR_RESEARCH | User-provided screenshot and tool screenshot show Chrome PDF viewer rendering local PDF at `127.0.0.1:8765`; page indicator visible as `3 / 589` |
| PAL Book I.10 range | PASS_FOR_SOURCE_PREP | `<h3 id="I.10">` starts at PAL XML line 738, Heiberg/PAL marker `I_31_7`; `<h3 id="I.11">` starts at line 1043, marker `I_48` |
| Book I.10 trial source extraction | PASS_FOR_TRIAL_SOURCE | `chapters/src/010_book_i_10_chords.md` generated from PAL XML; trial toc recorded at `source/trial_toc.json` |
| Book I.10 figure label audit | PASS_FOR_TRIAL | `qa/technical/010_book_i_10_chords.diagram_table_audit.md` maps 7 figures to labels and Greek source lines |
| Book I PAL segmentation | PASS_FOR_PRE_RESEARCH | `source/book_i_segmentation.md` records 16 Book I chapter boundaries from PAL anchors and page markers |
| Book I PDF contact sheets | PASS_FOR_PRE_RESEARCH_SAMPLE | Contact sheets cover viewer pages `4`-`50`, including Book I title/TOC, I.10, I.11 chord table, I.15, I.16, and Book II boundary |

## 未完成 / Open

| check | status | required action |
|---|---|---|
| Wikimedia file-history hash reconciliation | OPEN | Confirm whether current file history lists the same SHA1/SHA256 or a revised file. |
| PDF page-image offset | PASS_FOR_BOOK_I10_TRIAL | Book I.10 maps to PDF viewer pages `19` through `27`; viewer page `28` starts Book I.11. Screenshots saved under `qa/technical/page_screenshots/`. |
| Missing/damaged page scan | OPEN | Visual sample around Book I title, I.10, I.11, I.15, and Book II title. |
| OCR confidence | OPEN | Decide OCR/manual/PAL transcription path; record rights policy before bulk import. |

## 2026-05-16 Tooling Attempt

| attempt | result | implication |
|---|---|---|
| Browser via `file://` | blocked | cannot use direct file URL for PDF inspection in this environment |
| Browser via local `http.server` | PDF fetched, viewer did not expose rendered page content | insufficient for page-image verification |
| Python package check | `PIL` available; `pypdf` and `PyMuPDF` unavailable | cannot render or inspect PDF pages programmatically yet |
| `pip install pypdf pymupdf` | stopped after long PyMuPDF download stall | no local rendering tool installed this round |

## 2026-05-17 Browser/PAL Update

The PDF viewer is visually usable in the browser even though DOM extraction is not useful. Use browser screenshots and manual/page-number navigation for page-image checks. The PAL transcription provides exact Heiberg/PAL markers for Book I.10: `I_31_7` through before `I_48`.

## 2026-05-17 Trial Extraction Update

Book I.10 trial source now exists in `chapters/src/010_book_i_10_chords.md`. The extracted source preserves PAL line/page markers and records PAL page markers `I_32` through `I_47`.

This does not complete PDF page verification. The next PDF check must map the PAL/Heiberg markers around `I_31_7` to actual PDF viewer page numbers and capture or record the pages containing the Book I.10 diagrams before the trial translation can pass.

## 2026-05-17 Book I.10 PDF Range Mapping

Evidence screenshots:

- `qa/technical/page_screenshots/almagest-pdf-page-019.png`
- `qa/technical/page_screenshots/almagest-pdf-page-020.png`
- `qa/technical/page_screenshots/almagest-pdf-page-021.png`
- `qa/technical/page_screenshots/almagest-pdf-page-022.png`
- `qa/technical/page_screenshots/almagest-pdf-page-023.png`
- `qa/technical/page_screenshots/almagest-pdf-page-024.png`
- `qa/technical/page_screenshots/almagest-pdf-page-025.png`
- `qa/technical/page_screenshots/almagest-pdf-page-026.png`
- `qa/technical/page_screenshots/almagest-pdf-page-027.png`
- `qa/technical/page_screenshots/almagest-pdf-page-028.png`
- `qa/technical/page_screenshots/book_i10_pdf_pages_019_028_contact_sheet.jpg`

| PDF viewer page | visible printed pages | Book I.10 role | diagram/table observation |
|---:|---|---|---|
| 19 | 30-31 | Book I.10 starts on printed page 31, right column/page | no figure in visible start section |
| 20 | 32-33 | Book I.10 continuation | geometry figure visible on printed page 32 |
| 21 | 34-35 | Book I.10 continuation | no obvious large diagram in screenshot |
| 22 | 36-37 | Book I.10 continuation | geometry figure visible on printed page 37 |
| 23 | 38-39 | Book I.10 continuation | geometry figures visible on printed pages 38 and 39 |
| 24 | 40-41 | Book I.10 continuation | geometry figure visible on printed page 41 |
| 25 | 42-43 | Book I.10 continuation | geometry figure visible on printed page 43 |
| 26 | 44-45 | Book I.10 continuation | geometry figure visible on printed page 45 |
| 27 | 46-47 | Book I.10 ending range | no obvious large diagram in screenshot |
| 28 | 48-49 | Book I.11 starts; outside Book I.10 except boundary check | chord table visible on printed page 48 |

Conclusion: Book I.10 page range is sufficiently located for trial-page control, and the figures on viewer pages `20`, `22`, `23`, `24`, `25`, and `26` have a chapter-level diagram audit in `qa/technical/010_book_i_10_chords.diagram_table_audit.md`. This allows only Book I.10 single-chapter controlled trial translation. Full Book I source splitting and publication still require the open checks above.

## 2026-05-17 Book I PDF Sampling Update

PyMuPDF rendering is now available locally through `scripts/render_pdf_contact_sheet.py`. The following contact sheets were generated:

- `qa/technical/page_screenshots/book_i_pages_004_018_contact_sheet.jpg`
- `qa/technical/page_screenshots/book_i_pages_019_029_contact_sheet.jpg`
- `qa/technical/page_screenshots/book_i_pages_030_047_contact_sheet.jpg`
- `qa/technical/page_screenshots/book_i_pages_048_050_boundary_contact_sheet.jpg`

Observed page-image mapping for Book I:

| PDF viewer page | visible printed pages / role |
|---:|---|
| 4 | front matter and Greek title opening |
| 5 | Book I table of contents opening, printed page around `I_3` |
| 6 | printed pages `4`-`5`, Book I.1 begins |
| 19 | printed pages `30`-`31`, Book I.9 and Book I.10 boundary |
| 20-27 | printed pages `32`-`47`, Book I.10 body and figures |
| 28-35 | printed pages `48`-`63`, Book I.11 chord table |
| 36-38 | printed pages `64`-`68`, Book I.12 and transition to I.13 |
| 38-42 | printed pages `67`-`76`, Book I.13 diagram/proof material |
| 42-43 | printed pages `74`-`79`, Book I.14 material |
| 44 | printed pages `74`-`75`, Book I.14 material |
| 45 | printed pages `76`-`77`, Book I.14/I.15 boundary vicinity |
| 46 | printed pages `78`-`79`, Book I.15/I.16 vicinity |
| 47 | printed pages `80`-`81`, obliquity table material |
| 48-49 | printed pages `82`-`85`, Book I.16 ending |
| 50 | Book II table of contents and beginning, boundary after Book I |

Working page formula for Book I sampled pages: `PDF viewer page = floor((Heiberg printed page + 8) / 2)`. This formula is recorded only as a Book I page-image sampling aid. Formal chapter source extraction must still cite the screenshot evidence and preserve `PENDING_PDF_PAGE_VERIFICATION` until chapter-specific checks are complete.

`source/book_i_segmentation.md` now includes estimated PDF viewer page ranges for the 16 Book I chapters. These ranges are suitable for pre-research planning and page sampling, not yet for final chapter gate PASS.

## Publication Gate

This file must become `PASS` before Book I can move from pretranslation research into formal source splitting.
