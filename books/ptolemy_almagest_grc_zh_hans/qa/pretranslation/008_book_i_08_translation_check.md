# Book I.8 译文检查 / Translation Check

check_status: `PASS_TRANSLATION_DRAFT__REVIEW_PENDING`
created_at_utc: `2026-05-17T22:13:25+00:00`

## 控制结论

- 本检查确认 Book I.8 受控译文草稿已建立。
- 本检查不允许进入 `chapters/final/`，不允许生成正式 EPUB。
- 下一步必须进行忠实度、中文可读性、术语一致性、天文学证明链和古今概念边界审校。

## 检查项

| id | status | path/detail | missing/hits | sha256 |
|---|---|---|---|---|
| translation_file_exists | PASS | `chapters/translated/008_book_i_08_two_primary_motions.md` | `[]` | `21d66a0dac69e5202cdee04c2d930734a2a29334b82cbc14f7bcde8d2472404e` |
| chapter_control_exists | PASS | `qa/chapter_controls/008_book_i_08_two_primary_motions.control.md` | `[]` | `03a7ef3f3031049b52c51f76fc1ec47848382d9f1a67326859e4a3f87c9be717` |
| technical_audit_exists | PASS | `qa/technical/008_book_i_08_two_primary_motions.technical_audit.md` | `[]` | `649ab7caa0c4097a0d33496ac0270b5cf33b80542bfd292082233a41efa4ffc4` |
| forbidden_modernizing_wording_absent | PASS | `` | `[]` | `` |
| chapter_notes_present | PASS | `5` | `` | `` |
| forbidden_file_absent | PASS | `chapters/final/008_book_i_08_two_primary_motions.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
