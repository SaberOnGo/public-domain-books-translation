# Book I.11 弦表区域抽取检查 / Table Region Extraction Check

check_status: `FAIL`
created_at_utc: `2026-05-17T22:21:27+00:00`

## 控制结论

- 本检查只确认 Heiberg PDF 弦表区域已经稳定裁出。
- 区域裁图不是弦表行列转录，不允许把本检查解释为 Book I.11 已翻译或可进入终稿。
- 下一步必须逐行转录 `48`-`63` 页弦表，形成结构化 CSV/JSON 后再进入表格数值校验。

## 检查项

| id | status | detail |
|---|---|---|
| region_csv_exists | PASS | `source/tables/book_i_11_chord_table_regions.csv` |
| printed_page_coverage | PASS | `[48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]` |
| viewer_page_coverage | PASS | `[28, 29, 30, 31, 32, 33, 34, 35]` |
| region_images_exist | PASS | `[]` |
| region_images_not_tiny | PASS | `` |
| region_images_have_edge_margin | FAIL | `` |
| row_transcription_not_claimed | PASS | `0` |
| strategy_mentions_region_stage | PASS | `[]` |
| book_i11_final_absent | PASS | `` |

## Failures

- region images have too much ink on crop edge; likely clipped or too tight: ['source/tables/book_i_11_chord_table_regions/book_i11_p049_right_table_region.png', 'source/tables/book_i_11_chord_table_regions/book_i11_p053_right_table_region.png']
