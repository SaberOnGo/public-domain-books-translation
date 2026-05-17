# 《Almagest》图表与表格清单 / Diagram and Table Inventory

inventory_status: `BOOK_I10_FIGURE_LABEL_AUDIT_PASS_FOR_TRIAL__FULL_BOOK_OPEN`

| id | chapter | source_location | type | source_caption_or_label | target_caption_or_label | redraw_required | numeric_check_required | status | notes |
|---|---|---|---|---|---|---|---|---|---|
| I.10-geometry-chords | Book I.10 | PDF viewer pages `19`-`27`; printed pages `31`-`47`; PAL `I_31_7` through before `I_48` | geometry_figure_series | chord construction figures visible on PDF viewer pages `20`, `22`, `23`, `24`, `25`, `26` | 弦定理几何图 candidate | yes | yes | PASS_FOR_BOOK_I10_TRIAL | screenshots saved under `qa/technical/page_screenshots/`; 7 figure labels and source references audited in `qa/technical/010_book_i_10_chords.diagram_table_audit.md`; final redraw still requires structured vector work |
| I.11-chord-table | Book I.11 | PDF viewer pages `28`-`35`; printed pages `48`-`63`; PAL heading `I_48`, table body absent in PAL transcription; region crops under `source/tables/book_i_11_chord_table_regions/` | numeric_table | chord table | 弦表 candidate | structured_table_required plus optional facsimile evidence | yes | REGION_CROPPED__ROW_TRANSCRIPTION_PENDING | preserve sexagesimal values; no AI freehand table reconstruction; prior strategy stage `STRATEGY_PASS_SOURCE_EXTRACTION_PENDING`; region CSV is `source/tables/book_i_11_chord_table_regions.csv`; row transcription still pending |
| I.12-ecliptic-equator | Book I.12 | PDF page-image offset TBD | spherical_astronomy_diagram | ecliptic/equator relation figure to verify | 黄道-赤道关系图 candidate | yes | yes | DRAFT | spherical-geometry labels must match text |
| I.13-ecliptic-arc-table | Book I.13 | PDF page-image offset TBD | numeric_table | ecliptic/equator arc relation table to verify | 黄道弧表 candidate | structured_table_preferred | yes | DRAFT | table checksum required |
| I.14-rising-difference | Book I.14 | PDF page-image offset TBD | spherical_astronomy_diagram/table | rising-time difference material to verify | 升起差图/表 candidate | yes_if_diagram_present | yes | DRAFT | terminology must distinguish rising, arc, and time-degree relation |
| I.15-obliquity | Book I.15 | PDF page-image offset TBD | observation_numeric_claim/table | obliquity of the ecliptic material to verify | 黄道倾角 candidate | yes_if_diagram_present | yes | DRAFT | record ancient value and modern explanatory note separately |
| whole-work-star-tables | later books | out of current scope | star_catalog/table | TBD | TBD | TBD | yes | OUT_OF_SCOPE_CURRENTLY | record later, do not translate now |

## 当前结论

Book I 已有研究级图表清单。Book I.10 的 PDF 页图范围、图中点名、线段、弧、比例关系和正文引用已完成逐图审计；Book I.11 已完成弦表区域裁图，但逐行转录和数值校验仍未完成。最终出版重绘、Book I.11 raw table 和 Book I.15 表格/数值控制仍阻断 Book I 终稿与 EPUB。

## Book I.11 弦表区域证据 / Chord Table Region Evidence

| evidence | path |
|---|---|
| region manifest | `source/tables/book_i_11_chord_table_regions.csv` |
| region crop directory | `source/tables/book_i_11_chord_table_regions/` |
| crop contact sheet | `qa/technical/page_screenshots/book_i11_table_region_crops_contact_sheet.jpg` |

## Book I.10 截图证据 / Screenshot Evidence

| evidence | path |
|---|---|
| contact sheet | `qa/technical/page_screenshots/book_i10_pdf_pages_019_028_contact_sheet.jpg` |
| viewer page 19 | `qa/technical/page_screenshots/almagest-pdf-page-019.png` |
| viewer page 20 | `qa/technical/page_screenshots/almagest-pdf-page-020.png` |
| viewer page 21 | `qa/technical/page_screenshots/almagest-pdf-page-021.png` |
| viewer page 22 | `qa/technical/page_screenshots/almagest-pdf-page-022.png` |
| viewer page 23 | `qa/technical/page_screenshots/almagest-pdf-page-023.png` |
| viewer page 24 | `qa/technical/page_screenshots/almagest-pdf-page-024.png` |
| viewer page 25 | `qa/technical/page_screenshots/almagest-pdf-page-025.png` |
| viewer page 26 | `qa/technical/page_screenshots/almagest-pdf-page-026.png` |
| viewer page 27 | `qa/technical/page_screenshots/almagest-pdf-page-027.png` |
| viewer page 28 boundary check | `qa/technical/page_screenshots/almagest-pdf-page-028.png` |
