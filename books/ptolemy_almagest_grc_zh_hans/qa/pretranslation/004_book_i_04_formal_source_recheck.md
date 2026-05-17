# Book I.4 正式 source recheck / Formal Source Recheck

recheck_status: `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING`
created_at_utc: `2026-05-17T22:13:15+00:00`

## 控制结论

- 本报告确认 Book I.4 source extraction candidate、PDF 页图证据和译前技术审计已建立。
- 本报告不允许直接翻译；下一步必须先创建章节控制文件，再进入受控翻译。
- 本报告不允许写 `chapters/final/`，不允许生成正式 EPUB。

## 检查项

| id | status | path | missing | sha256 |
|---|---|---|---|---|
| source_file_exists | PASS | `chapters/src/004_book_i_04_earth_is_spherical.md` |  | `4cac906c317c09226ad6b5bdd656b446e30dc1a6e89b0675bd070e7382a87bf7` |
| source_extraction_check_exists | PASS | `qa/pretranslation/004_book_i_04_source_extraction_check.md` |  | `80f1baab006d5d382afddc2d15d755c6b52fbdc87ea8615fac9154b64c3dccf7` |
| pdf_contact_sheet_exists | PASS | `qa/technical/page_screenshots/book_i04_pages_011_012_contact_sheet.jpg` |  | `42c0e3e90de09daf3265e6e677518ccc13a97c01c2b3930b9f6433a8dbfc05ac` |
| technical_audit_exists | PASS | `qa/technical/004_book_i_04_earth_is_spherical.technical_audit.md` |  | `e886e3451949675035bbfffe19e9ab8bd6d03ee66fa4adca617612a1c4831ba4` |
| term_lock_updated | PASS | `qa/technical/mathematical_term_lock.md` |  | `1066e99caad25386984337d6db996609a52f9dfba28fbccc2e08a570982e42a0` |
| forbidden_absent | PASS | `chapters/final/004_book_i_04_earth_is_spherical.md` |  | `` |
| forbidden_absent | PASS | `output/book.epub` |  | `` |
