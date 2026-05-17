# Book I.8 正式 source recheck / Formal Source Recheck

recheck_status: `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING`
created_at_utc: `2026-05-17T22:13:17+00:00`

## 控制结论

- 本报告确认 Book I.8 source extraction candidate、PDF 页图证据和译前技术审计已建立。
- 本报告不允许直接翻译；下一步必须先创建章节控制文件，再进入受控翻译。
- 本报告不允许写 `chapters/final/`，不允许生成正式 EPUB。

## 检查项

| id | status | path | missing | sha256 |
|---|---|---|---|---|
| source_file_exists | PASS | `chapters/src/008_book_i_08_two_primary_motions.md` |  | `d0331ea61ae7357ab4362ae9a5335c9798ff18f87e7460a3ea0270e23de6d0a0` |
| source_extraction_check_exists | PASS | `qa/pretranslation/008_book_i_08_source_extraction_check.md` |  | `1ea164b295963da4a50784f8bd16405fb52537cf3ae97dd26af39bb7cdaa66ca` |
| pdf_contact_sheet_exists | PASS | `qa/technical/page_screenshots/book_i08_pages_017_019_contact_sheet.jpg` |  | `a005f3f0920b0906e380f3eaf6fc936d225199712e955030444089e450d9d19e` |
| technical_audit_exists | PASS | `qa/technical/008_book_i_08_two_primary_motions.technical_audit.md` |  | `649ab7caa0c4097a0d33496ac0270b5cf33b80542bfd292082233a41efa4ffc4` |
| term_lock_updated | PASS | `qa/technical/mathematical_term_lock.md` |  | `1066e99caad25386984337d6db996609a52f9dfba28fbccc2e08a570982e42a0` |
| forbidden_absent | PASS | `chapters/final/008_book_i_08_two_primary_motions.md` |  | `` |
| forbidden_absent | PASS | `output/book.epub` |  | `` |
