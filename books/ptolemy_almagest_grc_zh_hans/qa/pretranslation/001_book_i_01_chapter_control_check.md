# Book I.1 章节控制检查 / Chapter Control Check

check_status: `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED`
created_at_utc: `2026-05-17T22:13:18+00:00`

## 控制结论

- 本检查确认 Book I.1 章节控制文件已建立。
- 若本检查 PASS，下一步只允许写受控译文 `chapters/translated/001_book_i_01_proem.md`。
- 本检查不允许写 `chapters/final/`，不允许生成正式 EPUB。

## 检查项

| id | status | path | missing | sha256 |
|---|---|---|---|---|
| control_exists | PASS | `qa/chapter_controls/001_book_i_01_proem.control.md` |  | `f96fc5f6217aad3e8406a9236b0cd445dcda7751139a3e799541b539cbd91a54` |
| source_recheck_exists | PASS | `qa/pretranslation/001_book_i_01_formal_source_recheck.md` |  | `9139bd4394a77a0431d12d6a82e63f149904bb62eaf6f6967e557504f7fb35a2` |
| technical_audit_exists | PASS | `qa/technical/001_book_i_01_proem.technical_audit.md` |  | `2cf157e9103529714fa68d0a16d2fc72c099cf034cbfe902724c46a5e28d5aeb` |
| forbidden_absent | PASS | `chapters/final/001_book_i_01_proem.md` |  | `` |
| forbidden_absent | PASS | `output/book.epub` |  | `` |
