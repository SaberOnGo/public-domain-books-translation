# Book I.7 章节控制检查 / Chapter Control Check

check_status: `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED`
created_at_utc: `2026-05-17T22:13:21+00:00`

## 控制结论

- 本检查确认 Book I.7 章节控制文件已建立。
- 若本检查 PASS，下一步只允许写受控译文 `chapters/translated/007_book_i_07_earth_has_no_translational_motion.md`。
- 本检查不允许写 `chapters/final/`，不允许生成正式 EPUB。

## 检查项

| id | status | path | missing | sha256 |
|---|---|---|---|---|
| control_exists | PASS | `qa/chapter_controls/007_book_i_07_earth_has_no_translational_motion.control.md` |  | `6828368e374bf157c6c03c43664f9e64d92327ba219be56c731b2257ba5fa203` |
| source_recheck_exists | PASS | `qa/pretranslation/007_book_i_07_formal_source_recheck.md` |  | `477c43fa0d440cd38dd98575ee900e829d9ea13470baf93a60856266e9bd7073` |
| technical_audit_exists | PASS | `qa/technical/007_book_i_07_earth_has_no_translational_motion.technical_audit.md` |  | `0ca6663d4ca6a716234fc6ef59b10fd18de8b8b39f3c867d30b6be06076a3fd1` |
| forbidden_absent | PASS | `chapters/final/007_book_i_07_earth_has_no_translational_motion.md` |  | `` |
| forbidden_absent | PASS | `output/book.epub` |  | `` |
