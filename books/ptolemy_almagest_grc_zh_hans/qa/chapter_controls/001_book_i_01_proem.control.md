# Book I.1 章节控制 / Chapter Control

chapter_file: `001_book_i_01_proem.md`
source_path: `chapters/src/001_book_i_01_proem.md`
translated_path: `chapters/translated/001_book_i_01_proem.md`
human_required: false
human_feedback_status: `none`
control_status: `PASS_FOR_CONTROLLED_TRANSLATION_PREP__NOT_TRANSLATED`
return_to_stage: `07_translate_chapters`

## 范围

本控制只覆盖 Book I.1 的受控翻译准备。它不允许写 `chapters/final/`，不允许生成正式 EPUB，也不允许绕过后续忠实度、可读性、术语和技术审校。

## 已满足的前置条件

| check | result | evidence |
|---|---|---|
| source candidate exists | PASS | `chapters/src/001_book_i_01_proem.md` |
| source extraction check | PASS | `qa/pretranslation/001_book_i_01_source_extraction_check.md` |
| formal source recheck | PASS | `qa/pretranslation/001_book_i_01_formal_source_recheck.md` |
| PDF page evidence | PASS_FOR_PREP | `qa/technical/page_screenshots/book_i01_pages_006_008_contact_sheet.jpg` |
| technical audit | PASS_FOR_PREP | `qa/technical/001_book_i_01_proem.technical_audit.md` |
| term prelock | PASS_FOR_PREP | `qa/technical/mathematical_term_lock.md` |

## 翻译控制要求

| risk | required handling |
|---|---|
| 古代学科分类 | 保留 `理论/实践/自然学/数学/神学性研究` 的古代哲学分类链条，不改写成现代大学学科介绍。 |
| 数学与天文学关系 | 体现数学诸学通向天体研究的论证关系，不把本章写成现代天文学导论。 |
| 专名 `Σύρε` | 按本书专名规则采用稳定译名，并在必要时注释；不得随意音译漂移。 |
| 英译本参考 | 英译本只作 reference witness，不得作为中文句子的转译底稿。 |
| 中文可读性 | 避免古希腊长周期句硬搬；允许拆句，但不得省略论证层级。 |
| 注释策略 | 如古代学科分类可能使读者误解，可在章末集中注释，不在正文中堆大段解释。 |

## 禁止项

- 不得写 `chapters/final/001_book_i_01_proem.md`。
- 不得生成正式 `output/book.epub`。
- 不得把英译本句式当作底稿。
- 不得把 `φυσικόν` 直接现代化成“物理学”而不加边界处理。
- 不得把 `θεολογικόν` 写成现代宗教教义意义。
- 不得省略 Ptolemy 说明数学诸学价值的论证链。

## 自动结论

Book I.1 可以进入受控翻译准备；翻译完成后必须继续执行章节控制复核、技术审计复核、忠实度审校、可读性审校、术语审校和章节质量门禁。当前仍未翻译，不能进入终稿。
