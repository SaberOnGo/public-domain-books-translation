# Book I.3 章节质量门禁检查 / Chapter Quality Gate Check

check_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
created_at_utc: `2026-05-17T22:13:35+00:00`

## 控制结论

- Book I.3 章节级质量门禁通过，可进入终稿前全书一致性审校队列。
- 本检查不允许写 `chapters/final/003_book_i_03_heaven_moves_spherically.md`，不允许生成正式 EPUB。
- 本检查不放开 Book I.4-I.16 或全书批量翻译。

## 检查项

| id | status | path | expected/actual/missing | sha256 |
|---|---|---|---|---|
| source_extraction | PASS | `qa/pretranslation/003_book_i_03_source_extraction_check.json` | `PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING / PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING` | `b96ad6ae722cf423fda58413fa2b178e986805f0b90a29756ad2003484d59cab` |
| formal_source_recheck | PASS | `qa/pretranslation/003_book_i_03_formal_source_recheck.json` | `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING / PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING` | `9cf459f8d3f9b322053e1d5eb68268f3eab5abf245b99ebb7e16cf1d029d6ba4` |
| chapter_control | PASS | `qa/pretranslation/003_book_i_03_chapter_control_check.json` | `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED / PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED` | `c755e434f4c8f16def8b33341f1a75340f6de7481bf155e60b1f1e82897d4b13` |
| translation_draft | PASS | `qa/pretranslation/003_book_i_03_translation_check.json` | `PASS_TRANSLATION_DRAFT__REVIEW_PENDING / PASS_TRANSLATION_DRAFT__REVIEW_PENDING` | `868a24793f4af976b98a47774e79eb76ce4cdcd879df4d8abecb0e65280c7e57` |
| draft_review | PASS | `qa/pretranslation/003_book_i_03_review_check.json` | `PASS_REVIEW__TECHNICAL_RECHECK_PENDING / PASS_REVIEW__TECHNICAL_RECHECK_PENDING` | `95bfa8fd2e1d350a2fd47a95c39721c18aadd330b6e2da2b69c86834f5fd0e09` |
| post_translation_technical_recheck | PASS | `qa/pretranslation/003_book_i_03_post_translation_technical_recheck.json` | `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING / PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING` | `347e294a46f17e809bcee4c03979a66bb74de63572ab650cd51b8b27c4481b7e` |
| chapter_quality_gate_record | PASS | `qa/chapter_controls/003_book_i_03_heaven_moves_spherically.quality_gate.md` | `[]` | `e868d03f0eba1e0ad006cd7c407db78efe2c91c6d96c6dcd74ac1bf1ad9c5ade` |
| translation_file | PASS | `chapters/translated/003_book_i_03_heaven_moves_spherically.md` | `[]` | `4a95a1e6d89e117ab346e50ceb5be8463cb48518f757ade19568767c3f19cb11` |
| forbidden_file_absent | PASS | `chapters/final/003_book_i_03_heaven_moves_spherically.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
