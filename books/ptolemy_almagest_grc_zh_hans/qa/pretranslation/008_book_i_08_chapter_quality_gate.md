# Book I.8 章节质量门禁检查 / Chapter Quality Gate Check

check_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
created_at_utc: `2026-05-17T22:13:37+00:00`

## 控制结论

- Book I.8 章节级质量门禁通过，可进入终稿前全书一致性审校队列。
- 本检查不允许写 `chapters/final/008_book_i_08_two_primary_motions.md`，不允许生成正式 EPUB。
- 本检查不放开 Book I.9-I.16 以外的任何卷；Book II-XIII 仍不在当前目标范围内。

## 检查项

| id | status | path | expected/actual/missing | sha256 |
|---|---|---|---|---|
| source_extraction | PASS | `qa/pretranslation/008_book_i_08_source_extraction_check.json` | `PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING / PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING` | `9aae7a00b9089250142c5c2a4e60365a03a3a282d8e0cda30e148eb8d2bbe28f` |
| formal_source_recheck | PASS | `qa/pretranslation/008_book_i_08_formal_source_recheck.json` | `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING / PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING` | `709226534b3f432e3800f98253f25a635e075e901efc76985b286e3194b1530a` |
| chapter_control | PASS | `qa/pretranslation/008_book_i_08_chapter_control_check.json` | `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED / PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED` | `0f62b068246ca972b27c58946babe28bfc5a14e258398695e20bab641cf697b7` |
| translation_draft | PASS | `qa/pretranslation/008_book_i_08_translation_check.json` | `PASS_TRANSLATION_DRAFT__REVIEW_PENDING / PASS_TRANSLATION_DRAFT__REVIEW_PENDING` | `7ecec30bb23be787cee63f11b741695a45821348cd11cce59106d70ed8448afc` |
| draft_review | PASS | `qa/pretranslation/008_book_i_08_review_check.json` | `PASS_REVIEW__TECHNICAL_RECHECK_PENDING / PASS_REVIEW__TECHNICAL_RECHECK_PENDING` | `671758c73bdad4ed4ae253132a53cb0275258f9b59e43525e065d03b443ff4c2` |
| post_translation_technical_recheck | PASS | `qa/pretranslation/008_book_i_08_post_translation_technical_recheck.json` | `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING / PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING` | `00108903ee6fef81eeb2cf2adf8146334ab3fae2ff25504d881ae8ce4c82fc2b` |
| chapter_quality_gate_record | PASS | `qa/chapter_controls/008_book_i_08_two_primary_motions.quality_gate.md` | `[]` | `e5d538ef1f9708435745b1503388c52666433059581527d86016393e0b742bdf` |
| translation_file | PASS | `chapters/translated/008_book_i_08_two_primary_motions.md` | `[]` | `21d66a0dac69e5202cdee04c2d930734a2a29334b82cbc14f7bcde8d2472404e` |
| forbidden_file_absent | PASS | `chapters/final/008_book_i_08_two_primary_motions.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
