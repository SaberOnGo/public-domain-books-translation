# Book I.2 章节质量门禁检查 / Chapter Quality Gate Check

check_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
created_at_utc: `2026-05-17T22:13:34+00:00`

## 控制结论

- Book I.2 章节级质量门禁通过，可进入终稿前全书一致性审校队列。
- 本检查不允许写 `chapters/final/002_book_i_02_order_of_the_theorems.md`，不允许生成正式 EPUB。
- 本检查不放开 Book I.3-I.16 或全书批量翻译。

## 检查项

| id | status | path | expected/actual/missing | sha256 |
|---|---|---|---|---|
| source_extraction | PASS | `qa/pretranslation/002_book_i_02_source_extraction_check.json` | `PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING / PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING` | `e4b19229e4d88b9969f7cff37f0db627c4600e7f8269a492f238599bf215011f` |
| formal_source_recheck | PASS | `qa/pretranslation/002_book_i_02_formal_source_recheck.json` | `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING / PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING` | `82d2c9c7f486a6948f45e217c8cc7b2a597bc5bb361a21a8c0d4071694296918` |
| chapter_control | PASS | `qa/pretranslation/002_book_i_02_chapter_control_check.json` | `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED / PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED` | `39ae97a0799734696dc9bfc1077391e9977e3363b2fe29fe4652ca107b223ead` |
| translation_draft | PASS | `qa/pretranslation/002_book_i_02_translation_check.json` | `PASS_TRANSLATION_DRAFT__REVIEW_PENDING / PASS_TRANSLATION_DRAFT__REVIEW_PENDING` | `de2e97e8782571c138932ce79d4cc2be49b0d40dc1d13863266fc3a189715dea` |
| draft_review | PASS | `qa/pretranslation/002_book_i_02_review_check.json` | `PASS_REVIEW__TECHNICAL_RECHECK_PENDING / PASS_REVIEW__TECHNICAL_RECHECK_PENDING` | `95b7030c898e9871bca9a5db36ba096077090e50521807871f3f7976680c88f7` |
| post_translation_technical_recheck | PASS | `qa/pretranslation/002_book_i_02_post_translation_technical_recheck.json` | `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING / PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING` | `58f9f81e78bd4c3d60a5801387533d6448495bbb2d54c94ad27f60cc559fb32c` |
| chapter_quality_gate_record | PASS | `qa/chapter_controls/002_book_i_02_order_of_the_theorems.quality_gate.md` | `[]` | `68a521a59c3f075b7f7c92f777c2a78cbc1657e584f15bf8c39cc010dee79569` |
| translation_file | PASS | `chapters/translated/002_book_i_02_order_of_the_theorems.md` | `[]` | `2cc9ab0f7adb05a3c56a58dea6f78678850ad3cc0115f8b7c36fb29afa1efe96` |
| forbidden_file_absent | PASS | `chapters/final/002_book_i_02_order_of_the_theorems.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
