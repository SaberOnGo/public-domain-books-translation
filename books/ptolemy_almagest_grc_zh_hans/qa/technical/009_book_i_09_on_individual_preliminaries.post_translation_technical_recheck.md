# Book I.9 译后技术复核 / Post-Translation Technical Recheck

recheck_status: `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING`
chapter_id: `009_book_i_09_on_individual_preliminaries`

## 控制结论

- 本章不含几何图、表格、六十进制数值、角度或数学计算。
- 英译本只作 reference witness；译文依据古希腊文 source 文件。
- 译文保留总括预设、逐项证明、前述两极间大圈弧、圆内直线大小和几何证明的衔接关系。
- 不得写 `chapters/final/009_book_i_09_on_individual_preliminaries.md`；不允许生成正式 `output/book.epub`。

## 技术复核项

| item | result | evidence |
|---|---|---|
| 图表风险 | PASS | 本章无图表；无需 facsimile figure |
| 数值风险 | PASS | 本章无六十进制数值、角度和计算 |
| Euclid 依赖 | PASS | 本章无显式 Euclid 依赖 |
| 具体测定 | PASS | 译文使用“各项具体测定/具体证明”语义 |
| I.8 衔接 | PASS | 保留前述两极之间的大圈弧 |
| I.10 衔接 | PASS | “圆内直线大小”指向弦长理论但未提前展开 |
| 古今边界 | PASS | 未出现现代代数化或教材目录化改写 |

## 章节质量门禁输入

- 译文：`chapters/translated/009_book_i_09_on_individual_preliminaries.md`
- 评审：`reviews/chapters/009_book_i_09_on_individual_preliminaries.review.md`
- 术语锁：`qa/technical/mathematical_term_lock.md`
- source recheck：`qa/pretranslation/009_book_i_09_formal_source_recheck.md`

下一步只能进入 Book I.9 章节质量门禁；仍不得进入终稿、正式 EPUB 或 Book II-XIII。
