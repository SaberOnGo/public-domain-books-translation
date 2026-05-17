# Source Witness Manifest / 《Almagest》底本与见证清单

manifest_status: `FACSIMILE_AND_PAL_TRANSCRIPTION_AVAILABLE__BOOK_I_MAPPING_DRAFT`

## Base Text / 主底本影像

- source_language: Ancient Greek
- edition_title: Almagest / Mathematike Syntaxis, Heiberg Greek edition
- editor_or_transcriber: J. L. Heiberg
- publication_year: 1898 candidate, exact scan metadata to verify
- source_url: https://commons.wikimedia.org/wiki/File:Almagest_Complete,_Heiberg.pdf
- local_facsimile: `source/facsimile/Almagest_Complete_Heiberg_1898.pdf`
- local_sha1: `e7c2a35f90202e8f23103e54a8fb3c90fd303b0b`
- local_sha256: `b5115c91265e7997236d54bb6e421eff6308ef3639681e4a6ab6bcfc37a1c32b`
- bytes: `18277108`
- pdf_page_count_control: `589`
- public_domain_evidence: Wikimedia Commons public-domain file page plus local preservation hash； file history/hash discrepancy must be rechecked before publication
- volume_or_book_range: Books I-XIII expected； Book I pilot mapped from Heiberg/PAL chapter structure, PDF page-image offset still to verify
- page_line_section_system: Heiberg book/chapter/page system； PAL Heiberg transcription preserves Heiberg page markers between slash delimiters
- scan_or_text_type: PDF scan facsimile
- ocr_status: no independent OCR selected； PAL Greek transcription is used as auxiliary transcription control, not as a replacement for facsimile checks
- missing_or_damaged_pages: unknown
- reason_for_selection: standard Greek scholarly base； full Greek work preserved as public-domain facsimile candidate and locally hashed

## 三源分工 / Source Role Hierarchy

本书必须同时保留 PDF 扫描、PAL 古希腊文转写和英译本参考，但三者职责不同：

1. **Heiberg PDF 扫描**：主底本影像。用于核对古希腊正文、页码、版面、图表、表格、校勘/脚注区域、几何图标签和最终出版图来源。
2. **PAL Heiberg 古希腊文转写 XML**：辅助古希腊文转写。用于可复制文本、章节切分、PAL/Heiberg 页标、分词链、长周期句分析、OCR/人工转写疑点校正和试译 source text 抽取；不得跳过 PDF 页图核验。
3. **英译本**：reference witness only。只能用于理解疑难数学/天文学段落、比较术语、发现差异和写差异摘要；不得作为中文转译底稿，不得复制现代译本的措辞、注释、图表、表格或编辑结构，也不得单独修正古希腊文底稿。

冲突处理顺序：先回查 Heiberg PDF 扫描和 PAL 古希腊转写；必要时查 Heiberg 校勘语境和 `qa/textual/`、`qa/technical/` 记录；英译本只能提示疑点，不能覆盖古希腊文证据。

## Witnesses / 文本见证

| id | witness_type | language | title_or_source | editor_translator | date | rights_status | allowed_use | notes |
|---|---|---|---|---|---|---|---|---|
| base-heiberg | primary_facsimile_critical_edition_scan | Ancient Greek | Heiberg Greek edition PDF | J. L. Heiberg | 1898 candidate | public-domain candidate | primary facsimile for Greek base text, page/figure/table/final checks | downloaded； local SHA256 `b5115c91265e7997236d54bb6e421eff6308ef3639681e4a6ab6bcfc37a1c32b` |
| aux-pal-heiberg | auxiliary_greek_transcription | Ancient Greek | PAL Heiberg transcription | Ptolemaeus Arabus et Latinus | modern digital transcription of Heiberg | CC BY 4.0 except listed Quadripartitum exception； Almagest not the exception | searchable Greek source control, extraction, segmentation, OCR/transcription discrepancy checks | local XML saved； commit `368c5f1f6555679f2d7ab84062839e921a6293cb`； SHA256 `3f4dd5e0bf3a52255ac7cd1c719cffe4b26a706b75ae4100b23e74fc729a300d`； not a second-language translation |
| ref-toomer | reference_translation | English | Ptolemy's Almagest | G. J. Toomer | 1984/1998 | copyrighted | reference witness only | no direct translation, no copied notes |
| ref-taliaferro | reference_translation_candidate | English | Mathematical Composition (Almagest) | R. Catesby Taliaferro | 1939 | public-domain candidate, but HathiTrust item currently `Limited (search-only)` | candidate reference witness after rights/full-view verification | HathiTrust record `001475750`, item `mdp.39015036048588`； not downloaded |
| ref-ia | historical_scan_search | Greek/Latin/other | Internet Archive Almagest search | various | varies | must verify item by item | source discovery only | not a base until exact item verified |

## Numbering System / 编号体系

- book_or_volume: Books I-XIII expected.
- chapter_or_section: to be mapped from Heiberg.
- page: Heiberg page numbers to preserve.
- line: line-level reference not yet established.
- figure_or_table: all figures, chord tables, astronomical tables must be inventoried.
- notes: Book I pilot is the only planned pretranslation scope.

## Blockers

- `manifest_status` cannot become `PASS` until PDF page-image verification, Book I structure map review, figure/table inventory, and trial chapter extraction policy are complete.
- PAL transcription can be used for auxiliary Greek source text control with attribution, but every final source decision must remain traceable to Heiberg PDF/PAL Greek evidence.
- English translations remain `reference_translation` witnesses only and cannot unlock formal translation by themselves.
