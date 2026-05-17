# Book I.5 章节质量门禁 / Chapter Quality Gate

chapter_id: `005_book_i_05_earth_is_central`
gate_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
translation: `chapters/translated/005_book_i_05_earth_is_central.md`

## 控制结论

- Book I.5 已完成 source extraction、formal source recheck、章节控制、受控译文草稿、草稿级评审和译后技术复核。
- 本门禁确认 Book I.5 可排队进入终稿前全书一致性审校；但在 `formal_translation_allowed=false` 时，仍不允许写 `chapters/final/005_book_i_05_earth_is_central.md`。
- 本门禁不允许生成正式 `output/book.epub`，也不允许把 Book I.5 的通过状态外推为全书批量翻译许可。

## 聚合输入

| gate | file | required status |
|---|---|---|
| source extraction | `qa/pretranslation/005_book_i_05_source_extraction_check.json` | `PASS_SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING` |
| formal source recheck | `qa/pretranslation/005_book_i_05_formal_source_recheck.json` | `PASS_FOR_SOURCE_PREP__CHAPTER_CONTROL_PENDING` |
| chapter control | `qa/pretranslation/005_book_i_05_chapter_control_check.json` | `PASS_CHAPTER_CONTROL__CONTROLLED_TRANSLATION_PREP_ALLOWED` |
| translation draft | `qa/pretranslation/005_book_i_05_translation_check.json` | `PASS_TRANSLATION_DRAFT__REVIEW_PENDING` |
| draft review | `qa/pretranslation/005_book_i_05_review_check.json` | `PASS_REVIEW__TECHNICAL_RECHECK_PENDING` |
| post-translation technical recheck | `qa/pretranslation/005_book_i_05_post_translation_technical_recheck.json` | `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING` |

## 质量结论

| dimension | result | note |
|---|---|---|
| 底本忠实度 | PASS | 翻译基础为古希腊文 source；英译本只作 reference witness。 |
| 中文可读性 | PASS_WITH_FINAL_REVIEW_NOTE | 三种反证结构已分段；终稿可继续微调黄道十二分宫段落。 |
| 术语一致性 | PASS | `天球中央`、`球心`、`天轴`、`地平圈`、`中天`、`气候带` 与术语预锁一致。 |
| 数学/天文学专项 | PASS | 地球居中命题、地平圈等分、二分/昼夜证据、东西地平与中天时间和月食反证已复核。 |
| 图表与数值 | PASS_NOT_APPLICABLE | 本章无图表、六十进制数值、Euclid 依赖或数学计算；`六个`黄道十二分宫只是分段计数。 |
| 古今概念边界 | PASS | 章末注已说明天球中央、正球/斜球、中天、气候带和月食反证的古代模型边界。 |
| 后续一致性 | PASS_WITH_FINAL_REVIEW_NOTE | `正球/斜球`、`黄道十二分宫`、`气候带` 需在 Book I.12-I.16 统一。 |

## 仍然禁止

- 不得写 `chapters/final/005_book_i_05_earth_is_central.md`。
- 不得生成正式 `output/book.epub`。
- 不得把 Book I.5 的章节级通过状态解释为 Book I.6-I.16 或全书已经可批量翻译。

## 下一步

1. 继续推进 Book I.6 source extraction 与 PDF formal recheck。
2. 等全书预研究和章节级门禁满足后，再统一处理终稿提升。
