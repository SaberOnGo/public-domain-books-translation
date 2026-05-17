# Book I.11 弦表 raw table 检查 / Raw Chord Table Check

check_status: `FAIL_RAW_TABLE_INCOMPLETE`
created_at_utc: `2026-05-17T22:12:24+00:00`

## 控制结论

- 本检查确认 `book_i_11_chord_table_raw.csv` 是否已完成 PDF 逐行转录和数值校验。
- `book_i_11_chord_table_modern_check.csv` 只作现代数值 QA 旁证，不是底稿，也不是 Ptolemy 表的 expected source value。
- 只有 360 行全部 `RAW_TRANSCRIBED_FROM_HEIBERG_PDF` 且数值检查通过，Book I.11 才能进入翻译/EPUB 表格生成。

## 统计

- raw_count: `360`
- modern_check_count: `360`
- pending_pdf_transcription: `360`
- pdf_transcribed: `0`
- numeric_pass: `0`
- numeric_disputed: `0`

## 检查项

| id | status | detail |
|---|---|---|
| raw_csv_exists | PASS | `source/tables/book_i_11_chord_table_raw.csv` |
| modern_check_csv_exists | PASS | `source/tables/book_i_11_chord_table_modern_check.csv` |
| raw_row_count_360 | PASS | `360` |
| modern_check_row_count_360 | PASS | `360` |
| some_rows_pdf_transcribed | FAIL | `0` |
| all_rows_numeric_checked | FAIL | `0` |
| disputed_rows_recorded | PASS | `0` |
| arc_coverage_half_degree_to_180 | PASS | `0°30′` |

## Failures

- no rows have been transcribed from Heiberg PDF yet
- numeric checks incomplete: 0/360 PASS
