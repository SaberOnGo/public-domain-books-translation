# Book I.6 章节质量门禁 / Chapter Quality Gate

chapter_id: `006_book_i_06_earth_as_point_to_heavens`
gate_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
translation: `chapters/translated/006_book_i_06_earth_as_point_to_heavens.md`

## 控制结论

- Book I.6 已完成 source extraction、formal source recheck、章节控制、受控译文草稿、草稿级评审和译后技术复核。
- 本门禁确认 Book I.6 可排队进入终稿前全书一致性审校；但在 `formal_translation_allowed=false` 时，仍不允许写 `chapters/final/006_book_i_06_earth_as_point_to_heavens.md`。
- 本门禁不允许生成正式 `output/book.epub`，也不允许把 Book I.6 的通过状态外推为全书批量翻译许可。

## 聚合输入

| gate | file | required status |
|---|---|---|
| source extraction | `qa/pretranslation/006_book_i_06_source_extraction_check.json` | `PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING` |
| formal source recheck | `qa/pretranslation/006_book_i_06_formal_source_recheck.json` | `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING` |
| chapter control | `qa/pretranslation/006_book_i_06_chapter_control_check.json` | `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED` |
| translation draft | `qa/pretranslation/006_book_i_06_translation_check.json` | `PASS_TRANSLATION_DRAFT__REVIEW_PENDING` |
| draft review | `qa/pretranslation/006_book_i_06_review_check.json` | `PASS_REVIEW__TECHNICAL_RECHECK_PENDING` |
| post-translation technical recheck | `qa/pretranslation/006_book_i_06_post_translation_technical_recheck.json` | `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING` |

## 质量结论

| dimension | result | note |
|---|---|---|
| 底本忠实度 | PASS | 翻译基础为古希腊文 source；英译本只作 reference witness。 |
| 中文可读性 | PASS | 原文短章已拆为五个推理段落；证明链清楚。 |
| 术语一致性 | PASS_WITH_FINAL_REVIEW_NOTE | `恒星天球`、`气候带`、`晷针`、`环仪`、`地平圈`、`二分` 与术语预锁一致；`环仪` 终稿前需全书统一。 |
| 数学/天文学专项 | PASS | 点的比例命题、恒星天球距离、各地观测无差异、晷针与环仪中心、地平平面二分天球已复核。 |
| 图表与数值 | PASS_NOT_APPLICABLE | 本章无图表、六十进制数值、Euclid 依赖或数学计算。 |
| 古今概念边界 | PASS | 章末注已说明点的比例、恒星天球、气候带、晷针/环仪和地平圈的古代模型边界。 |
| 后续一致性 | PASS_WITH_FINAL_REVIEW_NOTE | `环仪/环形球仪` 需在后续仪器或观测章节中统一。 |

## 仍然禁止

- 不得写 `chapters/final/006_book_i_06_earth_as_point_to_heavens.md`。
- 不得生成正式 `output/book.epub`。
- 不得把 Book I.6 的章节级通过状态解释为 Book I.7-I.16 或全书已经可批量翻译。

## 下一步

1. 继续推进 Book I.7 source extraction 与 PDF formal recheck。
2. 等全书预研究和章节级门禁满足后，再统一处理终稿提升。
