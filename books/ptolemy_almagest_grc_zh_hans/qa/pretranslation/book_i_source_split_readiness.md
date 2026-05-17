# Book I 正式 source split 就绪矩阵 / Book I Source Split Readiness Matrix

readiness_status: `BOOK_I_PRE_RESEARCH_MATRIX_CREATED__SOURCE_SPLIT_PENDING`
created_at_utc: `2026-05-17T15:34:01+00:00`

## 控制结论

- 本矩阵用于决定 Book I 每章是否可以从 PAL 辅助转写推进到正式 `chapters/src/*.md`。
- 当前没有任何章节可直接进入 `chapters/final/` 或批量翻译。
- Book I.1-I.10 已通过章节质量门禁；下一步是终稿前全书一致性审校，不得直接进终稿。
- Book I.10 已通过章节质量门禁，但这不是终稿、正式 EPUB 或 Book I.11 弦表门禁。
- Book I.11 已完成弦表区域裁图，但逐行 source extraction 和数值校验仍未完成。
- Book I.15 仍是表格/数值高风险章节，必须先完成结构化表格策略和数值校验。

## 统计

- chapters: `16`
- source_extracted_pdf_recheck_pending: `5`
- formal_source_recheck_pass_chapter_control_pending: `0`
- chapter_control_pass_translation_prep_allowed: `0`
- translation_draft_pass_review_pending: `0`
- review_pass_technical_recheck_pending: `0`
- technical_recheck_pass_chapter_gate_pending: `0`
- chapter_quality_gate_pass_final_promotion_pending: `10`
- ready_for_formal_recheck_not_final: `0`
- formal_source_recheck_pass_not_translation: `0`
- table_strategy_pass_source_extraction_pending: `0`
- table_regions_cropped_row_transcription_pending: `1`
- source_extraction_pending: `0`

## 矩阵

| chapter | anchor | risk | PDF viewer pages | readiness | required controls | blockers |
|---:|---|---|---|---|---|---|
| 1 | I.1 | FOUNDATION_GEOMETRY_HIGH | 6-8 | CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING | philosophical framing check<br/>title/person-name policy | chapter quality gate passed<br/>final promotion and full-book consistency review remain pending<br/>chapters/final and output/book.epub remain forbidden |
| 2 | I.2 | FOUNDATION_GEOMETRY_HIGH | 8-9 | CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING | whole-work order terminology<br/>astronomical discipline vocabulary | chapter quality gate passed<br/>final promotion and full-book consistency review remain pending<br/>chapters/final and output/book.epub remain forbidden |
| 3 | I.3 | FOUNDATION_GEOMETRY_HIGH | 9-11 | CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING | spherical motion concept boundary<br/>observational argument check | chapter quality gate passed<br/>final promotion and full-book consistency review remain pending<br/>chapters/final and output/book.epub remain forbidden |
| 4 | I.4 | FOUNDATION_GEOMETRY_HIGH | 11-12 | CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING | earth-sphericity proof chain<br/>observation terminology | chapter quality gate passed<br/>final promotion and full-book consistency review remain pending<br/>chapters/final and output/book.epub remain forbidden |
| 5 | I.5 | FOUNDATION_GEOMETRY_HIGH | 12-14 | CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING | geocentric premise check<br/>proof dependency record | chapter quality gate passed<br/>final promotion and full-book consistency review remain pending<br/>chapters/final and output/book.epub remain forbidden |
| 6 | I.6 | FOUNDATION_GEOMETRY_HIGH | 14 | CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING | scale argument check<br/>point/ratio terminology | chapter quality gate passed<br/>final promotion and full-book consistency review remain pending<br/>chapters/final and output/book.epub remain forbidden |
| 7 | I.7 | FOUNDATION_GEOMETRY_HIGH | 15-17 | CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING | ancient physics vocabulary<br/>modern concept boundary note | chapter quality gate passed<br/>final promotion and full-book consistency review remain pending<br/>chapters/final and output/book.epub remain forbidden |
| 8 | I.8 | FOUNDATION_GEOMETRY_HIGH | 17-19 | CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING | celestial motion vocabulary<br/>two-motion distinction | chapter quality gate passed<br/>final promotion and full-book consistency review remain pending<br/>chapters/final and output/book.epub remain forbidden |
| 9 | I.9 | FOUNDATION_GEOMETRY_HIGH | 19 | CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING | geometric prerequisite terminology<br/>Euclidean dependency scan | chapter quality gate passed<br/>final promotion and full-book consistency review remain pending<br/>chapters/final and output/book.epub remain forbidden |
| 10 | I.10 | FOUNDATION_GEOMETRY_HIGH | 20-27 | CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING | trial source formal recheck<br/>figure label audit already exists | chapter quality gate passed<br/>final promotion and full-book consistency review remain pending<br/>Book I.11 chord table remains excluded<br/>chapters/final and output/book.epub remain forbidden |
| 11 | I.11 | TABLE_NUMERIC_HIGH | 28-35 | TABLE_REGIONS_CROPPED__ROW_TRANSCRIPTION_PENDING | structured chord table extraction<br/>sexagesimal numeric validation<br/>XHTML table strategy | chord-table page regions are cropped from Heiberg PDF<br/>row-level source transcription and numeric validation are still pending<br/>chapters/final and output/book.epub remain forbidden |
| 12 | I.12 | FOUNDATION_GEOMETRY_HIGH | 36-38 | SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING | spherical astronomy diagram audit<br/>tropic/ecliptic terminology | source extraction candidate exists, but formal PDF recheck is still required<br/>chapter control and technical audit must pass before translation<br/>chapters/final and output/book.epub remain forbidden |
| 13 | I.13 | FOUNDATION_GEOMETRY_HIGH | 38-42 | SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING | spherical proof dependency map<br/>diagram/table audit | source extraction candidate exists, but formal PDF recheck is still required<br/>chapter control and technical audit must pass before translation<br/>chapters/final and output/book.epub remain forbidden |
| 14 | I.14 | FOUNDATION_GEOMETRY_HIGH | 42-43 | SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING | equator/ecliptic arc relation check<br/>numeric/diagram audit | source extraction candidate exists, but formal PDF recheck is still required<br/>chapter control and technical audit must pass before translation<br/>chapters/final and output/book.epub remain forbidden |
| 15 | I.15 | TABLE_NUMERIC_HIGH | 44 | SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING | obliquity table extraction<br/>ancient value preservation<br/>numeric validation | source extraction candidate exists, but formal PDF recheck is still required<br/>chapter control and technical audit must pass before translation<br/>chapters/final and output/book.epub remain forbidden |
| 16 | I.16 | FOUNDATION_GEOMETRY_HIGH | 45-46 | SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING | right-sphere rising terminology<br/>cross-reference check | source extraction candidate exists, but formal PDF recheck is still required<br/>chapter control and technical audit must pass before translation<br/>chapters/final and output/book.epub remain forbidden |

## 下一步

1. I.1-I.10 进入终稿前全书一致性审校队列；正式预研究 PASS 前不得进终稿。
2. I.11 已有表格区域裁图；下一步是逐页/逐行 raw table source extraction 和数值校验，不是直接翻译。
3. 对 I.12-I.16 建立球面天文学、图表和数值控制，再进入 source extraction。
