# Book I.1 章节质量门禁检查 / Chapter Quality Gate Check

check_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
created_at_utc: `2026-05-17T22:13:34+00:00`

## 控制结论

- Book I.1 章节级质量门禁通过，可进入终稿前全书一致性审校队列。
- 本检查不允许写 `chapters/final/001_book_i_01_proem.md`，不允许生成正式 EPUB。
- 本检查不放开 Book I.2-I.16 或全书批量翻译。

## 检查项

| id | status | path | expected/actual/missing | sha256 |
|---|---|---|---|---|
| source_extraction | PASS | `qa/pretranslation/001_book_i_01_source_extraction_check.json` | `PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING / PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING` | `5d1b444fa2057ff85705cec104f7e7fae8de311eaee6da6c3cda7699f8355dae` |
| formal_source_recheck | PASS | `qa/pretranslation/001_book_i_01_formal_source_recheck.json` | `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING / PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING` | `60e1b0706d6890f8bb4f6231cb76d7c08d39b5430c5a1667555b13875061cacd` |
| chapter_control | PASS | `qa/pretranslation/001_book_i_01_chapter_control_check.json` | `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED / PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED` | `90fcd7e85afa7c4a0233b103fa58f6677611ee69261508a9d0b40a0c29f23ee4` |
| translation_draft | PASS | `qa/pretranslation/001_book_i_01_translation_check.json` | `PASS_TRANSLATION_DRAFT__REVIEW_PENDING / PASS_TRANSLATION_DRAFT__REVIEW_PENDING` | `55b16743253a8d3a1150a555af3c2c39e3c18f7946635cea2fef0c8a3db5cee0` |
| draft_review | PASS | `qa/pretranslation/001_book_i_01_review_check.json` | `PASS_REVIEW__TECHNICAL_RECHECK_PENDING / PASS_REVIEW__TECHNICAL_RECHECK_PENDING` | `a0a6bf8a479a5d796527f0076ebc71a0062f3f73cdf6f5812c90fb98c9398397` |
| post_translation_technical_recheck | PASS | `qa/pretranslation/001_book_i_01_post_translation_technical_recheck.json` | `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING / PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING` | `db4d2934548ad5afa4f02e70542e841c030c05349f67480a2c29a31960b14392` |
| chapter_quality_gate_record | PASS | `qa/chapter_controls/001_book_i_01_proem.quality_gate.md` | `[]` | `a5fc758362744aebffbd80c9d6192116e57beecadc1b82811833efb40e3e1fef` |
| translation_file | PASS | `chapters/translated/001_book_i_01_proem.md` | `[]` | `229acd645e25e8d341dcce5cfb15dfa6604363b0e46a961b498a55250c959c84` |
| forbidden_file_absent | PASS | `chapters/final/001_book_i_01_proem.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
