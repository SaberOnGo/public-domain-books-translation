# Book I.3 章节控制检查 / Chapter Control Check

check_status: `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED`
created_at_utc: `2026-05-17T22:13:19+00:00`

## 控制结论

- 本检查确认 Book I.3 章节控制文件已建立。
- 若本检查 PASS，下一步只允许写受控译文 `chapters/translated/003_book_i_03_heaven_moves_spherically.md`。
- 本检查不允许写 `chapters/final/`，不允许生成正式 EPUB。

## 检查项

| id | status | path | missing | sha256 |
|---|---|---|---|---|
| control_exists | PASS | `qa/chapter_controls/003_book_i_03_heaven_moves_spherically.control.md` |  | `08a1f634c5b83274ffffc2b3c4ec20f91e17203f65839a5cc37c758d194c246e` |
| source_recheck_exists | PASS | `qa/pretranslation/003_book_i_03_formal_source_recheck.md` |  | `3a86e363e4c28811d29cb413cd481931a93a4554f66c53b90339eaaa1aeaab4c` |
| technical_audit_exists | PASS | `qa/technical/003_book_i_03_heaven_moves_spherically.technical_audit.md` |  | `e67bea80f6fdd3268ebdea37fafcc110d04d6e06f4f128b0e75f69048fe465f8` |
| forbidden_absent | PASS | `chapters/final/003_book_i_03_heaven_moves_spherically.md` |  | `` |
| forbidden_absent | PASS | `output/book.epub` |  | `` |
