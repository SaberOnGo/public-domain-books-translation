# Book I.5 译文检查 / Translation Check

check_status: `PASS_TRANSLATION_DRAFT__REVIEW_PENDING`
created_at_utc: `2026-05-17T22:13:24+00:00`

## 控制结论

- 本检查确认 Book I.5 受控译文草稿已建立。
- 本检查不允许进入 `chapters/final/`，不允许生成正式 EPUB。
- 下一步必须进行忠实度、中文可读性、术语一致性、天文学证明链和古今概念边界审校。

## 检查项

| id | status | path/detail | missing/hits | sha256 |
|---|---|---|---|---|
| translation_file_exists | PASS | `chapters/translated/005_book_i_05_earth_is_central.md` | `[]` | `5bf43979605de77bf717b4231fcefee787491969e7de5c616da1ddc5f2c40c2f` |
| chapter_control_exists | PASS | `qa/chapter_controls/005_book_i_05_earth_is_central.control.md` | `[]` | `d33bf57c7fb0abe3200e29124d456a7991dfb0f63bd32bc2af711fb8627a7bca` |
| technical_audit_exists | PASS | `qa/technical/005_book_i_05_earth_is_central.technical_audit.md` | `[]` | `7edeadfda2265230cc88f33074990ac3eae268cfb91f7b0fa6fa9d42d8ca303f` |
| forbidden_modernizing_wording_absent | PASS | `` | `[]` | `` |
| chapter_notes_present | PASS | `6` | `` | `` |
| forbidden_file_absent | PASS | `chapters/final/005_book_i_05_earth_is_central.md` | `` | `` |
| forbidden_file_absent | PASS | `output/book.epub` | `` | `` |
