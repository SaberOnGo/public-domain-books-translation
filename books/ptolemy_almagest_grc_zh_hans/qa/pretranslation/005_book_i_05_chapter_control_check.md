# Book I.5 章节控制检查 / Chapter Control Check

check_status: `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED`
created_at_utc: `2026-05-17T22:13:20+00:00`

## 控制结论

- 本检查确认 Book I.5 章节控制文件已建立。
- 若本检查 PASS，下一步只允许写受控译文 `chapters/translated/005_book_i_05_earth_is_central.md`。
- 本检查不允许写 `chapters/final/`，不允许生成正式 EPUB。

## 检查项

| id | status | path | missing | sha256 |
|---|---|---|---|---|
| control_exists | PASS | `qa/chapter_controls/005_book_i_05_earth_is_central.control.md` |  | `d33bf57c7fb0abe3200e29124d456a7991dfb0f63bd32bc2af711fb8627a7bca` |
| source_recheck_exists | PASS | `qa/pretranslation/005_book_i_05_formal_source_recheck.md` |  | `f56ba31d615b35b183203ee492ca8f021daf67bccd330f1ac43db19fc9687f0b` |
| technical_audit_exists | PASS | `qa/technical/005_book_i_05_earth_is_central.technical_audit.md` |  | `7edeadfda2265230cc88f33074990ac3eae268cfb91f7b0fa6fa9d42d8ca303f` |
| forbidden_absent | PASS | `chapters/final/005_book_i_05_earth_is_central.md` |  | `` |
| forbidden_absent | PASS | `output/book.epub` |  | `` |
