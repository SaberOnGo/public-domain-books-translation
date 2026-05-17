# Book I.9 章节质量门禁检查 / Chapter Quality Gate Check

check_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
created_at_utc: `2026-05-17T22:13:37+00:00`

## 控制结论

- Book I.9 章节级质量门禁通过，可进入终稿前全书一致性审校队列。
- 本检查不允许写 `chapters/final/009_book_i_09_on_individual_preliminaries.md`，不允许生成正式 EPUB。
- 本检查不放开 Book II-XIII；当前目标仍只覆盖 Book I。

## 检查项

| id | status | path | expected/actual/missing | sha256 |
|---|---|---|---|---|
| source_extraction | PASS | `qa/pretranslation/009_book_i_09_source_extraction_check.json` | `PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING / PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING` | `36e0e5b01a61147f3bbc9262ec235ca3ab61cada9bdb7017696b2fb81042896e` |
| formal_source_recheck | PASS | `qa/pretranslation/009_book_i_09_formal_source_recheck.json` | `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING / PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING` | `854762bd5803acfbb09c815e606af447b81256f71f1eb74dd23963052cab1330` |
| chapter_control | PASS | `qa/pretranslation/009_book_i_09_chapter_control_check.json` | `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED / PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED` | `01a568810ac6993fcc36bed7962e48cb0506c1f087f46389cdce8ffdd0d45c5d` |
| translation_draft | PASS | `qa/pretranslation/009_book_i_09_translation_check.json` | `PASS_TRANSLATION_DRAFT__REVIEW_PENDING / PASS_TRANSLATION_DRAFT__REVIEW_PENDING` | `feb1ce323e1a4c566b47d352b80d5ba2bd6ef5eb2979b0f64e04cc470b6e42da` |
| draft_review | PASS | `qa/pretranslation/009_book_i_09_review_check.json` | `PASS_REVIEW__TECHNICAL_RECHECK_PENDING / PASS_REVIEW__TECHNICAL_RECHECK_PENDING` | `01fd57a114cba4d3319c3344b796916aef7a753553a9ac14aafd964e63213e4b` |
| post_translation_technical_recheck | PASS | `qa/pretranslation/009_book_i_09_post_translation_technical_recheck.json` | `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING / PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING` | `d8a298b5c8520942197c29165d72278bd721322c927f06d9622a33066a972a3b` |
| chapter_quality_gate_record | PASS | `qa/chapter_controls/009_book_i_09_on_individual_preliminaries.quality_gate.md` | `[]` | `19644dc00aa8dd6ff0c043a4b04db7e7ccc8a76563f499eeb85fea0a050a88b0` |
| translation_file | PASS | `chapters/translated/009_book_i_09_on_individual_preliminaries.md` | `[]` | `7c270fdda053c3693781e8f1cb20f607d36bc00dec986f8f38802c052f2c44c1` |
| forbidden_file_absent | PASS | `chapters/final/009_book_i_09_on_individual_preliminaries.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
