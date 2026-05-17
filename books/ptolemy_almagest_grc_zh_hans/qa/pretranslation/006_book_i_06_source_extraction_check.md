# Book I.6 Source Extraction Check

check_status: `PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING`
created_at_utc: `2026-05-17T22:13:10+00:00`

## 控制结论

- 本检查只确认章节 source extraction candidate 已生成。
- 本检查不允许翻译本章，不允许写 `chapters/final/`，不允许生成正式 EPUB。
- 章节仍需 PDF formal recheck、章节控制、技术审计和译后评审。

## 检查项

| id | status | detail |
|---|---|---|
| source_file_exists | PASS | `chapters/src/006_book_i_06_earth_as_point_to_heavens.md` |
| source_control_wording | PASS | `[]` |
| marker_count_matches_segmentation | PASS | `27` |
| pdf_viewer_pages_recorded | PASS | `14` |
| translated_absent_or_allowed_by_control | PASS | `chapters/translated/006_book_i_06_earth_as_point_to_heavens.md` |
| final_absent | PASS | `chapters/final/006_book_i_06_earth_as_point_to_heavens.md` |
| formal_translation_still_gated | PASS | `` |
