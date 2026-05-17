# Book I.3 译文检查 / Translation Check

check_status: `PASS_TRANSLATION_DRAFT__REVIEW_PENDING`
created_at_utc: `2026-05-17T22:13:23+00:00`

## 控制结论

- 本检查确认 Book I.3 受控译文草稿已建立。
- 本检查不允许进入 `chapters/final/`，不允许生成正式 EPUB。
- 下一步必须进行忠实度、中文可读性、术语一致性和古今概念边界审校。

## 检查项

| id | status | path/detail | missing/hits | sha256 |
|---|---|---|---|---|
| translation_file_exists | PASS | `chapters/translated/003_book_i_03_heaven_moves_spherically.md` | `[]` | `4a95a1e6d89e117ab346e50ceb5be8463cb48518f757ade19568767c3f19cb11` |
| chapter_control_exists | PASS | `qa/chapter_controls/003_book_i_03_heaven_moves_spherically.control.md` | `[]` | `08a1f634c5b83274ffffc2b3c4ec20f91e17203f65839a5cc37c758d194c246e` |
| technical_audit_exists | PASS | `qa/technical/003_book_i_03_heaven_moves_spherically.technical_audit.md` | `[]` | `e67bea80f6fdd3268ebdea37fafcc110d04d6e06f4f128b0e75f69048fe465f8` |
| forbidden_modernizing_wording_absent | PASS | `` | `[]` | `` |
| chapter_notes_present | PASS | `6` | `` | `` |
| proof_chain_not_overcompressed | PASS | `10` | `` | `` |
| forbidden_file_absent | PASS | `chapters/final/003_book_i_03_heaven_moves_spherically.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
