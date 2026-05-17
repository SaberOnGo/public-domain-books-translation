# Book I.6 章节控制检查 / Chapter Control Check

check_status: `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED`
created_at_utc: `2026-05-17T22:13:20+00:00`

## 控制结论

- 本检查确认 Book I.6 章节控制文件已建立。
- 若本检查 PASS，下一步只允许写受控译文 `chapters/translated/006_book_i_06_earth_as_point_to_heavens.md`。
- 本检查不允许写 `chapters/final/`，不允许生成正式 EPUB。

## 检查项

| id | status | path | missing | sha256 |
|---|---|---|---|---|
| control_exists | PASS | `qa/chapter_controls/006_book_i_06_earth_as_point_to_heavens.control.md` |  | `121f43f6f8458f73a05abe66d1dde5e76702f06a18cae1ab2d5f453be8ea5935` |
| source_recheck_exists | PASS | `qa/pretranslation/006_book_i_06_formal_source_recheck.md` |  | `0c511614c8c825af769bfb0451425b731c73d7911a8bce96561f74172cb99c7d` |
| technical_audit_exists | PASS | `qa/technical/006_book_i_06_earth_as_point_to_heavens.technical_audit.md` |  | `3b242c358c99f55d86f0a8391eb07f734b267b16b30978288a7705be42b8d199` |
| forbidden_absent | PASS | `chapters/final/006_book_i_06_earth_as_point_to_heavens.md` |  | `` |
| forbidden_absent | PASS | `output/book.epub` |  | `` |
