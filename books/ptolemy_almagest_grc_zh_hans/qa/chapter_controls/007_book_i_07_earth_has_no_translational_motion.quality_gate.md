# Book I.7 章节质量门禁 / Chapter Quality Gate

chapter_id: `007_book_i_07_earth_has_no_translational_motion`
gate_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
translation: `chapters/translated/007_book_i_07_earth_has_no_translational_motion.md`

## 控制结论

- Book I.7 已完成 source extraction、formal source recheck、章节控制、受控译文草稿、草稿级评审和译后技术复核。
- 本门禁确认 Book I.7 可排队进入终稿前全书一致性审校；但在 `formal_translation_allowed=false` 时，仍不允许写 `chapters/final/007_book_i_07_earth_has_no_translational_motion.md`。
- 本门禁不允许生成正式 `output/book.epub`，也不允许把 Book I.7 的通过状态外推为全书批量翻译许可。

## 聚合输入

| gate | file | required status |
|---|---|---|
| source extraction | `qa/pretranslation/007_book_i_07_source_extraction_check.json` | `PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING` |
| formal source recheck | `qa/pretranslation/007_book_i_07_formal_source_recheck.json` | `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING` |
| chapter control | `qa/pretranslation/007_book_i_07_chapter_control_check.json` | `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED` |
| translation draft | `qa/pretranslation/007_book_i_07_translation_check.json` | `PASS_TRANSLATION_DRAFT__REVIEW_PENDING` |
| draft review | `qa/pretranslation/007_book_i_07_review_check.json` | `PASS_REVIEW__TECHNICAL_RECHECK_PENDING` |
| post-translation technical recheck | `qa/pretranslation/007_book_i_07_post_translation_technical_recheck.json` | `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING` |

## 质量结论

| dimension | result | note |
|---|---|---|
| 底本忠实度 | PASS | 翻译基础为古希腊文 source；英译本只作 reference witness。 |
| 中文可读性 | PASS_WITH_FINAL_REVIEW_NOTE | 原文长周期句已拆分；“违反自然的设想”一段终稿可再润色。 |
| 术语一致性 | PASS_WITH_FINAL_REVIEW_NOTE | `平移运动`、`切平面`、`上/下`、`旋转`、`飞行物/抛射物` 与术语预锁一致；`φορά` 终稿前需全书统一。 |
| 数学/天文学专项 | PASS | 地球无平移运动、重物趋向中心、地球每日自转设想和空气现象反驳已复核。 |
| 图表与数值 | PASS_NOT_APPLICABLE | 本章无图表、六十进制数值、Euclid 依赖或数学计算。 |
| 古今概念边界 | PASS | 章末注已说明平移/旋转区别、切平面、上/下方向和自转设想；正文未改写成现代物理。 |
| 后续一致性 | PASS_WITH_FINAL_REVIEW_NOTE | `φορά`、`重物`、`空气` 等自然学术语需在后续章节中统一。 |

## 仍然禁止

- 不得写 `chapters/final/007_book_i_07_earth_has_no_translational_motion.md`。
- 不得生成正式 `output/book.epub`。
- 不得把 Book I.7 的章节级通过状态解释为 Book I.8-I.16 或全书已经可批量翻译。

## 下一步

1. 继续推进 Book I.8 source extraction 与 PDF formal recheck。
2. 等全书预研究和章节级门禁满足后，再统一处理终稿提升。
