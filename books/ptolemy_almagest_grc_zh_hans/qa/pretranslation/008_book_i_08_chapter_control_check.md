# Book I.8 章节控制检查 / Chapter Control Check

check_status: `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED`
created_at_utc: `2026-05-17T22:13:21+00:00`

## 控制结论

- 本检查确认 Book I.8 章节控制文件已建立。
- 若本检查 PASS，下一步只允许写受控译文 `chapters/translated/008_book_i_08_two_primary_motions.md`。
- 本检查不允许写 `chapters/final/`，不允许生成正式 EPUB。

## 检查项

| id | status | path | missing | sha256 |
|---|---|---|---|---|
| control_exists | PASS | `qa/chapter_controls/008_book_i_08_two_primary_motions.control.md` |  | `03a7ef3f3031049b52c51f76fc1ec47848382d9f1a67326859e4a3f87c9be717` |
| source_recheck_exists | PASS | `qa/pretranslation/008_book_i_08_formal_source_recheck.md` |  | `dd8dc960c88cfc4c4c6bea6d75ec1a704b66bf95969d187732794f1881ba9364` |
| technical_audit_exists | PASS | `qa/technical/008_book_i_08_two_primary_motions.technical_audit.md` |  | `649ab7caa0c4097a0d33496ac0270b5cf33b80542bfd292082233a41efa4ffc4` |
| forbidden_absent | PASS | `chapters/final/008_book_i_08_two_primary_motions.md` |  | `` |
| forbidden_absent | PASS | `output/book.epub` |  | `` |
