# Book I.4 章节控制检查 / Chapter Control Check

check_status: `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED`
created_at_utc: `2026-05-17T22:13:19+00:00`

## 控制结论

- 本检查确认 Book I.4 章节控制文件已建立。
- 若本检查 PASS，下一步只允许写受控译文 `chapters/translated/004_book_i_04_earth_is_spherical.md`。
- 本检查不允许写 `chapters/final/`，不允许生成正式 EPUB。

## 检查项

| id | status | path | missing | sha256 |
|---|---|---|---|---|
| control_exists | PASS | `qa/chapter_controls/004_book_i_04_earth_is_spherical.control.md` |  | `b5b31c2a93ca81267b140f614da2eacb7f2f086d62af8414257842d8f40a4f41` |
| source_recheck_exists | PASS | `qa/pretranslation/004_book_i_04_formal_source_recheck.md` |  | `e0d82033dd04f7dcdd3bde1be685104bcf499e5e7bb984865a5906b9862d64e5` |
| technical_audit_exists | PASS | `qa/technical/004_book_i_04_earth_is_spherical.technical_audit.md` |  | `e886e3451949675035bbfffe19e9ab8bd6d03ee66fa4adca617612a1c4831ba4` |
| forbidden_absent | PASS | `chapters/final/004_book_i_04_earth_is_spherical.md` |  | `` |
| forbidden_absent | PASS | `output/book.epub` |  | `` |
