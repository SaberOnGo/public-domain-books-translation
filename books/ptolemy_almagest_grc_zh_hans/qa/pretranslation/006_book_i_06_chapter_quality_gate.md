# Book I.6 章节质量门禁检查 / Chapter Quality Gate Check

check_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
created_at_utc: `2026-05-17T22:13:36+00:00`

## 控制结论

- Book I.6 章节级质量门禁通过，可进入终稿前全书一致性审校队列。
- 本检查不允许写 `chapters/final/006_book_i_06_earth_as_point_to_heavens.md`，不允许生成正式 EPUB。
- 本检查不放开 Book I.7-I.16 或全书批量翻译。

## 检查项

| id | status | path | expected/actual/missing | sha256 |
|---|---|---|---|---|
| source_extraction | PASS | `qa/pretranslation/006_book_i_06_source_extraction_check.json` | `PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING / PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING` | `2d48d1af935a32c82aa41f1979131eda8d883596b65cf12910f8909fb65f6b32` |
| formal_source_recheck | PASS | `qa/pretranslation/006_book_i_06_formal_source_recheck.json` | `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING / PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING` | `205b829764155741613464fcbd956377c0cfd5200322cba2782e8598656e5478` |
| chapter_control | PASS | `qa/pretranslation/006_book_i_06_chapter_control_check.json` | `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED / PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED` | `e68b523e67e4493015ee64fa9282dd8e8e6bebfa030d59c962bde6547cef6264` |
| translation_draft | PASS | `qa/pretranslation/006_book_i_06_translation_check.json` | `PASS_TRANSLATION_DRAFT__REVIEW_PENDING / PASS_TRANSLATION_DRAFT__REVIEW_PENDING` | `7032114914efe44acda0eb9044f905616d0e72161a032ce9b5055bfd922f58ea` |
| draft_review | PASS | `qa/pretranslation/006_book_i_06_review_check.json` | `PASS_REVIEW__TECHNICAL_RECHECK_PENDING / PASS_REVIEW__TECHNICAL_RECHECK_PENDING` | `6dcf800d9672212e15869524a5c51760c0e23cfd534a9fb428c99853ea40779c` |
| post_translation_technical_recheck | PASS | `qa/pretranslation/006_book_i_06_post_translation_technical_recheck.json` | `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING / PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING` | `72ca40f93eb1ca3c32eb68cada713316d6ea8783a54fe9b3b54e7df3402a8127` |
| chapter_quality_gate_record | PASS | `qa/chapter_controls/006_book_i_06_earth_as_point_to_heavens.quality_gate.md` | `[]` | `d6b95cfc54610ba11d264f2c42fe0df96df5c89aa6c26421f7caae41cb46c600` |
| translation_file | PASS | `chapters/translated/006_book_i_06_earth_as_point_to_heavens.md` | `[]` | `f119dadf12ae458af97d6271f775872d2c63b6bc4587b5230c52f4b50e6eb5fb` |
| forbidden_file_absent | PASS | `chapters/final/006_book_i_06_earth_as_point_to_heavens.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
