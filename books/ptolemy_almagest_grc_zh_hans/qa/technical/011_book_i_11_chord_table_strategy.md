# Book I.11 弦表结构化策略 / Chord Table Strategy

strategy_status: `BOOK_I11_TABLE_STRATEGY_PASS__SOURCE_EXTRACTION_PENDING`

region_extraction_status: `REGION_CROPPED__ROW_TRANSCRIPTION_PENDING`

## 控制结论

- Book I.11 是弦表本体，不得散文化翻译，也不得先用现代三角函数表重建。
- Heiberg PDF viewer pages `28`-`35`、printed pages `48`-`63` 是表格转录的主影像依据。
- PAL XML 在 `I.11` 到 `I.12` 之间只保留题名、`I_48`、`I_63` 页标和空段落，不含表格行列数据。
- 英译本只能用于理解表头或疑难项的 reference witness，不得作为表格底稿。
- 当前允许继续表格 source extraction 准备；仍不允许翻译 Book I.11 正文、写 `chapters/final/` 或生成正式 `output/book.epub`。

## 已有证据

| item | status | evidence |
|---|---|---|
| PDF page range | PASS_FOR_PRE_RESEARCH | `qa/technical/book_i_page_verification.md` records viewer pages `28`-`35` / printed pages `48`-`63` |
| PDF contact sheet | PASS_FOR_PRE_RESEARCH | `qa/technical/page_screenshots/book_i11_chord_table_pages_028_035_contact_sheet.jpg` |
| PAL heading boundary | PASS_FOR_PRE_RESEARCH | `<h3 id="I.11">` starts at `I_48`; `<h3 id="I.12">` starts at `I_64` |
| PAL table body | ABSENT_IN_PAL_TRANSCRIPTION | PAL has no transcribed rows between `I_48_2` and `I_63` |
| translation permission | BLOCKED | source extraction and table QA must happen first |
| table region crops | PASS_FOR_ROW_TRANSCRIPTION_PREP | `source/tables/book_i_11_chord_table_regions.csv` and `source/tables/book_i_11_chord_table_regions/*.png` |
| modern numeric QA table | PASS_FOR_TRANSCRIPTION_AID_ONLY | `source/tables/book_i_11_chord_table_modern_check.csv`; not a source transcription and not an expected source value |
| raw transcription worksheet | CREATED_NOT_TRANSCRIBED | `source/tables/book_i_11_chord_table_raw.csv`; 360 rows initialized, PDF row transcription pending |

## 表格字段草案

正式 source extraction 时先生成结构化 CSV/JSON，再生成 Markdown/XHTML。初始字段如下，后续可按 PDF 实际列宽微调：

| field | purpose | rule |
|---|---|---|
| `row_id` | stable row key | `I.11.p{printed_page}.r{n}` |
| `pdf_viewer_page` | PDF viewer page | integer, expected `28`-`35` |
| `printed_page` | Heiberg printed page | integer, expected `48`-`63` |
| `column_block` | page-local table block | left/right or numbered block, as seen in PDF |
| `arc_raw` | Greek table arc entry | preserve source glyphs and half-degree marks |
| `arc_normalized` | reader-facing arc | use `度/′/″` style such as `0°30′`; no decimal-only conversion |
| `chord_raw_columns` | chord value columns under `εὐθειῶν` | preserve Greek numeral columns before normalization |
| `chord_normalized` | chord value in radius/diameter scale used by the table | preserve sexagesimal components; no decimal-only conversion |
| `difference_raw_columns` | columns under `ἑξηκοστῶν` | preserve source columns; semantic label remains provisional until table header review |
| `facsimile_region` | crop or page-region reference | required before publication table QA |
| `verification_status` | extraction/validation state | `RAW_TRANSCRIBED`, `NORMALIZED`, `CHECKED`, `DISPUTED` |
| `notes` | variant/OCR/reading notes | record uncertain glyphs, corrections, and witness differences |

## Raw table 文件状态

- `source/tables/book_i_11_chord_table_modern_check.csv` 由 `scripts/generate_book_i11_chord_table_modern_check.py` 生成，只作现代数值 QA 旁证。
- 现代公式值可能与 Ptolemy 原表四舍五入或制表传统相差 `1″` 等小量；不得把它当作 PDF 转录预期值。
- `source/tables/book_i_11_chord_table_raw.csv` 由 `scripts/init_book_i11_chord_table_raw.py` 初始化，共 `360` 行，覆盖 `0°30′` 至 `180°`。
- 当前 raw table 行状态仍是 `PENDING_PDF_ROW_TRANSCRIPTION`；不得把 expected value 当作已转录底稿。
- `scripts/check_book_i11_chord_table_raw.py` 会在所有行完成 PDF 转录和数值校验前失败，这是预期门禁。

## 数值校验路线

1. 先转录表头、首行、末行、每页页首/页末、每 5 度节点和异常视觉项。
2. 如果抽样发现列漂移、页切换漏行或希腊数字识别不稳，立即改为全量双录。
3. 全量转录完成后，按表内相邻弦值差、半度步长、页首页末连续性做结构校验。
4. 现代三角函数只能用于 QA 旁证：`chord = 120 * sin(arc / 2)`；正文不得写成现代三角函数推导。
5. 所有读者版数值保留角度与六十进制表达，不得只给小数。

## EPUB 表格路线

- 正文 EPUB 应使用结构化 XHTML 表格，不把弦表转成普通段落。
- 大表必须允许小屏横向滚动，并按 PDF 页或列组分段，避免手机上缩到不可读。
- 每段表格都保留表题、页码来源和必要说明。
- 读者版 EPUB 不放原图旁证；facsimile crop 只保留在 `source/` 和 `qa/` 中作为转录、复核和争议项证据。
- 可检索表格是 EPUB 正文的唯一弦表正文形式，不得用整页图片替代。

## 区域裁图规则

- `scripts/extract_book_i11_table_regions.py` 按固定 viewer page 和 printed page 映射裁出 `48`-`63` 页弦表区域。
- `source/tables/book_i_11_chord_table_regions.csv` 是逐页区域清单，状态必须是 `REGION_CROPPED__ROW_TRANSCRIPTION_PENDING`。
- 弦表区域裁图不是弦表转录，不能替代 `source/tables/book_i_11_chord_table_raw.csv` 的逐行结构化数据。
- 若后续发现某页裁图切掉表头、行尾或半度标记，必须先调整脚本坐标并重新生成全部区域裁图，再继续转录。

## 下一步

1. 逐页复核 `source/tables/book_i_11_chord_table_regions/*.png` 是否完整包含表头和全部表格行。
2. 在 `source/tables/book_i_11_chord_table_raw.csv` 中逐行填写 PDF 原表读数。
3. 对照 `source/tables/book_i_11_chord_table_modern_check.csv` 和英译 witness 处理疑难项。
4. 完成表头语义、列组和半度步长校验后，再允许 Book I.11 source extraction。
