# Book I.8 译后技术复核检查 / Post-Translation Technical Recheck

check_status: `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING`
created_at_utc: `2026-05-17T22:13:33+00:00`

## 控制结论

- 本检查确认 Book I.8 已通过译后技术复核，可进入章节质量门禁准备。
- 本检查不允许进入 `chapters/final/`，不允许生成正式 EPUB。
- Book I.8 无图表、无六十进制数值、无 Euclid 依赖；技术风险集中在两类天球基本运动和球面天文学术语边界。

## 检查项

| id | status | path/detail | missing/hits | sha256 |
|---|---|---|---|---|
| post_translation_recheck_exists | PASS | `qa/technical/008_book_i_08_two_primary_motions.post_translation_technical_recheck.md` | `[]` | `36b682cabc5a2354b4f4632682c9fe9009e4bd16647e3fa254e2318385c0ea9f` |
| translation_exists | PASS | `chapters/translated/008_book_i_08_two_primary_motions.md` | `[]` | `21d66a0dac69e5202cdee04c2d930734a2a29334b82cbc14f7bcde8d2472404e` |
| review_exists | PASS | `reviews/chapters/008_book_i_08_two_primary_motions.review.md` | `[]` | `04c8d3fcc57c0646ddebedf4a2d9bc2cb5423f985c904d5935b6530d21540c20` |
| term_lock_contains_book_i8_terms | PASS | `qa/technical/mathematical_term_lock.md` | `[]` | `1066e99caad25386984337d6db996609a52f9dfba28fbccc2e08a570982e42a0` |
| translation_body_modernizing_terms_absent | PASS | `` | `[]` | `` |
| geometry_table_numeric_markers_absent_for_i8 | PASS | `` | `[]` | `` |
| forbidden_file_absent | PASS | `chapters/final/008_book_i_08_two_primary_motions.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
