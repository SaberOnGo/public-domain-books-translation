# Book I.1 译文检查 / Translation Check

check_status: `PASS_TRANSLATION_DRAFT__REVIEW_PENDING`
created_at_utc: `2026-05-17T22:13:22+00:00`

## 控制结论

- 本检查确认 Book I.1 受控译文草稿已建立。
- 本检查不允许进入 `chapters/final/`，不允许生成正式 EPUB。
- 下一步必须进行忠实度、中文可读性、术语一致性和概念边界审校。

## 检查项

| id | status | path/detail | missing/hits | sha256 |
|---|---|---|---|---|
| translation_file_exists | PASS | `chapters/translated/001_book_i_01_proem.md` | `[]` | `229acd645e25e8d341dcce5cfb15dfa6604363b0e46a961b498a55250c959c84` |
| chapter_control_exists | PASS | `qa/chapter_controls/001_book_i_01_proem.control.md` | `[]` | `f96fc5f6217aad3e8406a9236b0cd445dcda7751139a3e799541b539cbd91a54` |
| technical_audit_exists | PASS | `qa/technical/001_book_i_01_proem.technical_audit.md` | `[]` | `2cf157e9103529714fa68d0a16d2fc72c099cf034cbfe902724c46a5e28d5aeb` |
| forbidden_modernizing_wording_absent | PASS | `` | `[]` | `` |
| chapter_notes_present | PASS | `4` | `` | `` |
| forbidden_file_absent | PASS | `chapters/final/001_book_i_01_proem.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
