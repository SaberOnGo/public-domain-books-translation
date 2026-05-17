# Book I.2 章节质量门禁 / Chapter Quality Gate

chapter_id: `002_book_i_02_order_of_the_theorems`
gate_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
translation: `chapters/translated/002_book_i_02_order_of_the_theorems.md`

## 控制结论

- Book I.2 已完成 source extraction、formal source recheck、章节控制、受控译文草稿、草稿级评审和译后技术复核。
- 本门禁确认 Book I.2 可排队进入终稿前全书一致性审校；但在 `formal_translation_allowed=false` 时，仍不允许写 `chapters/final/002_book_i_02_order_of_the_theorems.md`。
- 本门禁不允许生成正式 `output/book.epub`，也不允许把 Book I.2 的通过状态外推为全书批量翻译许可。

## 聚合输入

| gate | file | required status |
|---|---|---|
| source extraction | `qa/pretranslation/002_book_i_02_source_extraction_check.json` | `PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING` |
| formal source recheck | `qa/pretranslation/002_book_i_02_formal_source_recheck.json` | `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING` |
| chapter control | `qa/pretranslation/002_book_i_02_chapter_control_check.json` | `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED` |
| translation draft | `qa/pretranslation/002_book_i_02_translation_check.json` | `PASS_TRANSLATION_DRAFT__REVIEW_PENDING` |
| draft review | `qa/pretranslation/002_book_i_02_review_check.json` | `PASS_REVIEW__TECHNICAL_RECHECK_PENDING` |
| post-translation technical recheck | `qa/pretranslation/002_book_i_02_post_translation_technical_recheck.json` | `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING` |

## 质量结论

| dimension | result | note |
|---|---|---|
| 底本忠实度 | PASS | 翻译基础为古希腊文 source；英译本只作 reference witness。 |
| 中文可读性 | PASS_WITH_FINAL_REVIEW_NOTE | 已将长周期总纲句拆分；终稿可进一步微调第一段节奏。 |
| 术语一致性 | PASS | `黄道斜圈`、`我们所居世界`、`地平圈`、`恒星天球`、`五个行星` 与术语预锁一致。 |
| 数学/天文学专项 | PASS_NOT_APPLICABLE | 本章无图表、数值、Euclid 依赖或天文计算；方法论和对象术语已复核。 |
| 古今概念边界 | PASS | 章末注已说明古代数学天文学语境，不现代化为物理轨道或现代宇宙论。 |
| 后续一致性 | PASS_WITH_FINAL_REVIEW_NOTE | `黄道斜圈`、`地平圈`、`恒星天球` 需在后续章节统一。 |

## 仍然禁止

- 不得写 `chapters/final/002_book_i_02_order_of_the_theorems.md`。
- 不得生成正式 `output/book.epub`。
- 不得把 Book I.2 的章节级通过状态解释为 Book I.3-I.16 或全书已经可批量翻译。

## 下一步

1. 继续推进 Book I.3 source extraction 与 PDF formal recheck。
2. 等全书预研究和章节级门禁满足后，再统一处理终稿提升。
