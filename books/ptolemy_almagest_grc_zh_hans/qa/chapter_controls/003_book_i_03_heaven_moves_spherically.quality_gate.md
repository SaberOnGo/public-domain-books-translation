# Book I.3 章节质量门禁 / Chapter Quality Gate

chapter_id: `003_book_i_03_heaven_moves_spherically`
gate_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
translation: `chapters/translated/003_book_i_03_heaven_moves_spherically.md`

## 控制结论

- Book I.3 已完成 source extraction、formal source recheck、章节控制、受控译文草稿、草稿级评审和译后技术复核。
- 本门禁确认 Book I.3 可排队进入终稿前全书一致性审校；但在 `formal_translation_allowed=false` 时，仍不允许写 `chapters/final/003_book_i_03_heaven_moves_spherically.md`。
- 本门禁不允许生成正式 `output/book.epub`，也不允许把 Book I.3 的通过状态外推为全书批量翻译许可。

## 聚合输入

| gate | file | required status |
|---|---|---|
| source extraction | `qa/pretranslation/003_book_i_03_source_extraction_check.json` | `PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING` |
| formal source recheck | `qa/pretranslation/003_book_i_03_formal_source_recheck.json` | `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING` |
| chapter control | `qa/pretranslation/003_book_i_03_chapter_control_check.json` | `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED` |
| translation draft | `qa/pretranslation/003_book_i_03_translation_check.json` | `PASS_TRANSLATION_DRAFT__REVIEW_PENDING` |
| draft review | `qa/pretranslation/003_book_i_03_review_check.json` | `PASS_REVIEW__TECHNICAL_RECHECK_PENDING` |
| post-translation technical recheck | `qa/pretranslation/003_book_i_03_post_translation_technical_recheck.json` | `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING` |

## 质量结论

| dimension | result | note |
|---|---|---|
| 底本忠实度 | PASS | 翻译基础为古希腊文 source；英译本只作 reference witness。 |
| 中文可读性 | PASS_WITH_FINAL_REVIEW_NOTE | 长周期句已分段；终稿可继续润色自然学段句式。 |
| 术语一致性 | PASS | `恒显星`、`天球的极`、`湿气蒸腾`、`升度构造`、`以太`、`同质` 与术语预锁一致。 |
| 数学/天文学专项 | PASS | 观测链、直线无穷运动反证、球形/圆形几何比较和古代自然学边界已复核。 |
| 图表与数值 | PASS_NOT_APPLICABLE | 本章无图表、数值、Euclid 依赖或天文计算。 |
| 古今概念边界 | PASS | 章末注已说明球形运动、湿气蒸腾、以太和同质性等古代概念边界。 |
| 后续一致性 | PASS_WITH_FINAL_REVIEW_NOTE | `升度构造` 需在 Book I.12-I.16 的球面天文学章节统一。 |

## 仍然禁止

- 不得写 `chapters/final/003_book_i_03_heaven_moves_spherically.md`。
- 不得生成正式 `output/book.epub`。
- 不得把 Book I.3 的章节级通过状态解释为 Book I.4-I.16 或全书已经可批量翻译。

## 下一步

1. 继续推进 Book I.4 source extraction 与 PDF formal recheck。
2. 等全书预研究和章节级门禁满足后，再统一处理终稿提升。
