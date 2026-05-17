# Book I.8 评审检查 / Review Check

check_status: `PASS_REVIEW__TECHNICAL_RECHECK_PENDING`
created_at_utc: `2026-05-17T22:13:29+00:00`

## 控制结论

- 本检查确认 Book I.8 译后评审记录存在并通过草稿级评审。
- 本检查不允许进入 `chapters/final/`，不允许生成正式 EPUB。
- 下一步仍需译后技术复核和章节质量门禁。

## 检查项

| id | status | path | missing | sha256 |
|---|---|---|---|---|
| review_exists | PASS | `reviews/chapters/008_book_i_08_two_primary_motions.review.md` |  | `04c8d3fcc57c0646ddebedf4a2d9bc2cb5423f985c904d5935b6530d21540c20` |
| translation_check_exists | PASS | `qa/pretranslation/008_book_i_08_translation_check.md` |  | `1bb020199172fd259decd177ef232cd42a684e507559571ceea81083af727b4e` |
| translation_exists | PASS | `chapters/translated/008_book_i_08_two_primary_motions.md` |  | `21d66a0dac69e5202cdee04c2d930734a2a29334b82cbc14f7bcde8d2472404e` |
| forbidden_absent | PASS | `chapters/final/008_book_i_08_two_primary_motions.md` |  | `` |
| forbidden_absent | PASS | `output/book.epub` |  | `` |
