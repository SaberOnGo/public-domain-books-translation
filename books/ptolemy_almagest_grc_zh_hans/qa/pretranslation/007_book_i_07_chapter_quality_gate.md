# Book I.7 章节质量门禁检查 / Chapter Quality Gate Check

check_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
created_at_utc: `2026-05-17T22:13:36+00:00`

## 控制结论

- Book I.7 章节级质量门禁通过，可进入终稿前全书一致性审校队列。
- 本检查不允许写 `chapters/final/007_book_i_07_earth_has_no_translational_motion.md`，不允许生成正式 EPUB。
- 本检查不放开 Book I.8-I.16 或全书批量翻译。

## 检查项

| id | status | path | expected/actual/missing | sha256 |
|---|---|---|---|---|
| source_extraction | PASS | `qa/pretranslation/007_book_i_07_source_extraction_check.json` | `PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING / PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING` | `6b09d018a3c4d002d6c404dc4f5b94b98f5c806a2fda3305bdc28af6237e9114` |
| formal_source_recheck | PASS | `qa/pretranslation/007_book_i_07_formal_source_recheck.json` | `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING / PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING` | `af1e9214a8b5740a09043b3ba91d94cdd6148122353d214a0ac4e7f15019b9d6` |
| chapter_control | PASS | `qa/pretranslation/007_book_i_07_chapter_control_check.json` | `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED / PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED` | `279465d0d1feeff1265d5751de3dcaef739125f3c163beee11a6e520f3093bf1` |
| translation_draft | PASS | `qa/pretranslation/007_book_i_07_translation_check.json` | `PASS_TRANSLATION_DRAFT__REVIEW_PENDING / PASS_TRANSLATION_DRAFT__REVIEW_PENDING` | `c4f2c92acbb4578ed02aa4ba2710fdf09618ba805c996960716907c0d1397474` |
| draft_review | PASS | `qa/pretranslation/007_book_i_07_review_check.json` | `PASS_REVIEW__TECHNICAL_RECHECK_PENDING / PASS_REVIEW__TECHNICAL_RECHECK_PENDING` | `a2907a983095541cac8807a2e4c07359fa6020e5225d2a7777b2e7daea60a591` |
| post_translation_technical_recheck | PASS | `qa/pretranslation/007_book_i_07_post_translation_technical_recheck.json` | `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING / PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING` | `4733bff91f6a7723b9d98579e0726697a5d7623cd361abdbdd95f61f142b3b2d` |
| chapter_quality_gate_record | PASS | `qa/chapter_controls/007_book_i_07_earth_has_no_translational_motion.quality_gate.md` | `[]` | `aa54ec5f76ee2c520956831fbfa680defe8ae2b794b2c75b1ad1aedc3bcf0927` |
| translation_file | PASS | `chapters/translated/007_book_i_07_earth_has_no_translational_motion.md` | `[]` | `e98457b9a87c6d933eb5ef8b1392cce2cca76fcc741003d06b9ad6be025ec9f7` |
| forbidden_file_absent | PASS | `chapters/final/007_book_i_07_earth_has_no_translational_motion.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
