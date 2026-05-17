# Book I.6 译文检查 / Translation Check

check_status: `PASS_TRANSLATION_DRAFT__REVIEW_PENDING`
created_at_utc: `2026-05-17T22:13:24+00:00`

## 控制结论

- 本检查确认 Book I.6 受控译文草稿已建立。
- 本检查不允许进入 `chapters/final/`，不允许生成正式 EPUB。
- 下一步必须进行忠实度、中文可读性、术语一致性、天文学证明链和古今概念边界审校。

## 检查项

| id | status | path/detail | missing/hits | sha256 |
|---|---|---|---|---|
| translation_file_exists | PASS | `chapters/translated/006_book_i_06_earth_as_point_to_heavens.md` | `[]` | `f119dadf12ae458af97d6271f775872d2c63b6bc4587b5230c52f4b50e6eb5fb` |
| chapter_control_exists | PASS | `qa/chapter_controls/006_book_i_06_earth_as_point_to_heavens.control.md` | `[]` | `121f43f6f8458f73a05abe66d1dde5e76702f06a18cae1ab2d5f453be8ea5935` |
| technical_audit_exists | PASS | `qa/technical/006_book_i_06_earth_as_point_to_heavens.technical_audit.md` | `[]` | `3b242c358c99f55d86f0a8391eb07f734b267b16b30978288a7705be42b8d199` |
| forbidden_modernizing_wording_absent | PASS | `` | `[]` | `` |
| chapter_notes_present | PASS | `5` | `` | `` |
| forbidden_file_absent | PASS | `chapters/final/006_book_i_06_earth_as_point_to_heavens.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
