# Book I.5 章节质量门禁检查 / Chapter Quality Gate Check

check_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
created_at_utc: `2026-05-17T22:13:36+00:00`

## 控制结论

- Book I.5 章节级质量门禁通过，可进入终稿前全书一致性审校队列。
- 本检查不允许写 `chapters/final/005_book_i_05_earth_is_central.md`，不允许生成正式 EPUB。
- 本检查不放开 Book I.6-I.16 或全书批量翻译。

## 检查项

| id | status | path | expected/actual/missing | sha256 |
|---|---|---|---|---|
| source_extraction | PASS | `qa/pretranslation/005_book_i_05_source_extraction_check.json` | `PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING / PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING` | `d80215bb788b1222cc7635ff50291c6a2968b8b40cbfa00b615a054f65776a66` |
| formal_source_recheck | PASS | `qa/pretranslation/005_book_i_05_formal_source_recheck.json` | `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING / PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING` | `3064e1e52a862c95d4d5bfc16ebd283a9294ccca829ca4721d3c2b5c5df812ac` |
| chapter_control | PASS | `qa/pretranslation/005_book_i_05_chapter_control_check.json` | `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED / PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED` | `6da29fd1c41582b657c112a9d15f68c95d94b084f1fe16285106d4c31e7490ec` |
| translation_draft | PASS | `qa/pretranslation/005_book_i_05_translation_check.json` | `PASS_TRANSLATION_DRAFT__REVIEW_PENDING / PASS_TRANSLATION_DRAFT__REVIEW_PENDING` | `8363572eceda45cbab31a90220a3e55621b7b31397ef6df416f4dc8d4d43177c` |
| draft_review | PASS | `qa/pretranslation/005_book_i_05_review_check.json` | `PASS_REVIEW__TECHNICAL_RECHECK_PENDING / PASS_REVIEW__TECHNICAL_RECHECK_PENDING` | `51e2aed8f73816ec6e0157ddaec60f64bab9f0f78279a60f4e047ad819ad67f9` |
| post_translation_technical_recheck | PASS | `qa/pretranslation/005_book_i_05_post_translation_technical_recheck.json` | `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING / PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING` | `4452a9f51f47e366c4659eda08c3c50aec6fe3fa54c4f914c99f63145259df52` |
| chapter_quality_gate_record | PASS | `qa/chapter_controls/005_book_i_05_earth_is_central.quality_gate.md` | `[]` | `1f268bf5c30405660c04f1a2beca5959cc67d4ec45ce51aad4da81ef03324cf7` |
| translation_file | PASS | `chapters/translated/005_book_i_05_earth_is_central.md` | `[]` | `5bf43979605de77bf717b4231fcefee787491969e7de5c616da1ddc5f2c40c2f` |
| forbidden_file_absent | PASS | `chapters/final/005_book_i_05_earth_is_central.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
