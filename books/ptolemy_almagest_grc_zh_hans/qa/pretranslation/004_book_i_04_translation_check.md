# Book I.4 译文检查 / Translation Check

check_status: `PASS_TRANSLATION_DRAFT__REVIEW_PENDING`
created_at_utc: `2026-05-17T22:13:23+00:00`

## 控制结论

- 本检查确认 Book I.4 受控译文草稿已建立。
- 本检查不允许进入 `chapters/final/`，不允许生成正式 EPUB。
- 下一步必须进行忠实度、中文可读性、术语一致性、观测证明链和古今概念边界审校。

## 检查项

| id | status | path/detail | missing/hits | sha256 |
|---|---|---|---|---|
| translation_file_exists | PASS | `chapters/translated/004_book_i_04_earth_is_spherical.md` | `[]` | `6ac3e482ad43bf2df9777301c57402ff00ee70fc723af3ae4f5da9bc1405473b` |
| chapter_control_exists | PASS | `qa/chapter_controls/004_book_i_04_earth_is_spherical.control.md` | `[]` | `b5b31c2a93ca81267b140f614da2eacb7f2f086d62af8414257842d8f40a4f41` |
| technical_audit_exists | PASS | `qa/technical/004_book_i_04_earth_is_spherical.technical_audit.md` | `[]` | `e886e3451949675035bbfffe19e9ab8bd6d03ee66fa4adca617612a1c4831ba4` |
| forbidden_modernizing_wording_absent | PASS | `` | `[]` | `` |
| chapter_notes_present | PASS | `5` | `` | `` |
| forbidden_file_absent | PASS | `chapters/final/004_book_i_04_earth_is_spherical.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
