# Book I.4 章节质量门禁检查 / Chapter Quality Gate Check

check_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
created_at_utc: `2026-05-17T22:13:35+00:00`

## 控制结论

- Book I.4 章节级质量门禁通过，可进入终稿前全书一致性审校队列。
- 本检查不允许写 `chapters/final/004_book_i_04_earth_is_spherical.md`，不允许生成正式 EPUB。
- 本检查不放开 Book I.5-I.16 或全书批量翻译。

## 检查项

| id | status | path | expected/actual/missing | sha256 |
|---|---|---|---|---|
| source_extraction | PASS | `qa/pretranslation/004_book_i_04_source_extraction_check.json` | `PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING / PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING` | `78ec7d950c23700be7c7ed2b978fa9251f7798937525270fb17d535dff13859a` |
| formal_source_recheck | PASS | `qa/pretranslation/004_book_i_04_formal_source_recheck.json` | `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING / PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING` | `b969fa3ab9bb0045f3fa1f5245c7171e3575c4f01d80b606d0ddc4785dea018d` |
| chapter_control | PASS | `qa/pretranslation/004_book_i_04_chapter_control_check.json` | `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED / PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED` | `b9d3e8d53119623658c3c68eb591182b9dd85bc28e0b09102e869838c46dac80` |
| translation_draft | PASS | `qa/pretranslation/004_book_i_04_translation_check.json` | `PASS_TRANSLATION_DRAFT__REVIEW_PENDING / PASS_TRANSLATION_DRAFT__REVIEW_PENDING` | `fea73d718385a1d05e4b98a241233be00f96c9e063262f63d48bc8e1fe55ec96` |
| draft_review | PASS | `qa/pretranslation/004_book_i_04_review_check.json` | `PASS_REVIEW__TECHNICAL_RECHECK_PENDING / PASS_REVIEW__TECHNICAL_RECHECK_PENDING` | `9ac27dad47abd3d6f772d23549452f61948261145ca3a48157ad1b3542d9234f` |
| post_translation_technical_recheck | PASS | `qa/pretranslation/004_book_i_04_post_translation_technical_recheck.json` | `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING / PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING` | `2157e16aa7eeba80c6f8cc14a2f444bae3ae5e7155bd58a796afeffe83873961` |
| chapter_quality_gate_record | PASS | `qa/chapter_controls/004_book_i_04_earth_is_spherical.quality_gate.md` | `[]` | `6ffb3523d78b218fb8e39a765bf29d6b4f8f072fd9bcb2ad567721c625b635e7` |
| translation_file | PASS | `chapters/translated/004_book_i_04_earth_is_spherical.md` | `[]` | `6ac3e482ad43bf2df9777301c57402ff00ee70fc723af3ae4f5da9bc1405473b` |
| forbidden_file_absent | PASS | `chapters/final/004_book_i_04_earth_is_spherical.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
