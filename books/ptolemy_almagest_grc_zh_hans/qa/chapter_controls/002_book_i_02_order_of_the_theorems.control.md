# Book I.2 章节控制 / Chapter Control

chapter_file: `002_book_i_02_order_of_the_theorems.md`
source_path: `chapters/src/002_book_i_02_order_of_the_theorems.md`
translated_path: `chapters/translated/002_book_i_02_order_of_the_theorems.md`
human_required: false
human_feedback_status: `none`
control_status: `PASS_FOR_CONTROLLED_TRANSLATION_PREP__NOT_TRANSLATED`
return_to_stage: `07_translate_chapters`

## 范围

本控制只覆盖 Book I.2 的受控翻译准备。它不允许写 `chapters/final/`，不允许生成正式 EPUB，也不允许把本章的 source recheck 通过状态解释为全书可批量翻译。

## 已满足的前置条件

| check | result | evidence |
|---|---|---|
| source candidate exists | PASS | `chapters/src/002_book_i_02_order_of_the_theorems.md` |
| source extraction check | PASS | `qa/pretranslation/002_book_i_02_source_extraction_check.md` |
| formal source recheck | PASS | `qa/pretranslation/002_book_i_02_formal_source_recheck.md` |
| PDF page evidence | PASS_FOR_PREP | `qa/technical/page_screenshots/book_i02_pages_008_009_contact_sheet.jpg` |
| technical audit | PASS_FOR_PREP | `qa/technical/002_book_i_02_order_of_the_theorems.technical_audit.md` |
| term prelock | PASS_FOR_PREP | `qa/technical/mathematical_term_lock.md` |

## 翻译控制要求

| risk | required handling |
|---|---|
| 全书论证次序 | 保留先总论天地关系、再论黄道/居住世界、再论太阳/月亮、最后论恒星和五行星的次序，不改写成现代目录摘要。 |
| 黄道与地理术语 | `λοξὸς κύκλος`、`οἰκουμένη`、`ὁρίζων`、`ἐγκλίσεις` 必须按古代天文学语境处理，并为后续 Book I.12-I.15 统一预留空间。 |
| 太阳/月亮与恒星/行星模块 | 不把古代“运动”现代化为真实物理轨道；需保留本书作为数学天文学模型的表达。 |
| 观测与证明方法 | 保留“显见现象/可靠观测作为基础，几何证明路线推进”的方法链。 |
| 英译本参考 | 英译本只作 reference witness，不得作为中文句子的转译底稿。 |
| 中文可读性 | 允许拆分长周期句；但不得删掉章节列出的先后关系和方法论层级。 |
| 注释策略 | 如“居住世界”“恒星天球”“五行星”等术语可能误导现代读者，可在章末集中注释。 |

## 禁止项

- 不得写 `chapters/final/002_book_i_02_order_of_the_theorems.md`。
- 不得生成正式 `output/book.epub`。
- 不得把英译本句式当作底稿。
- 不得把本章写成现代天文学教材目录。
- 不得省略显见现象、观测和几何证明之间的方法链。
- 不得提前翻译 Book I.11 弦表或进入全书批量翻译。

## 自动结论

Book I.2 可以进入受控翻译准备；翻译完成后必须继续执行章节控制复核、技术审计复核、忠实度审校、可读性审校、术语审校和章节质量门禁。当前仍未翻译，不能进入终稿。
