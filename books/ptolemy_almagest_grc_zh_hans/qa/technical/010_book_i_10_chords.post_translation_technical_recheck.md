# Book I.10 译后技术复核 / Post-Translation Technical Recheck

recheck_status: `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING`
chapter_id: `010_book_i_10_chords`

## 控制结论

- 本章含几何图、Euclid 依赖、六十进制数值和近似说明；所有这些都已在受控草稿中保留。
- 英译本只作 reference witness；译文依据古希腊文 source 文件。
- 本章只到 Book I.10 弦长论和弦表引出为止，不翻译 Book I.11 弦表本体。
- 不得写 `chapters/final/010_book_i_10_chords.md`；不允许生成正式 `output/book.epub`。

## 技术复核项

| item | result | evidence |
|---|---|---|
| 图表风险 | PASS_FOR_DRAFT | 译文引用 7 张试译图；正式 Book I EPUB 阶段需统一 facsimile/SVG 策略 |
| 图中点名 | PASS | 希腊大写点名保留 |
| 数值风险 | PASS | `p` 六十进制显示保留整数部和小分；未转十进制小数 |
| 角度表示 | PASS | 弧和角仍用 `°′″` |
| Euclid 依赖 | PASS | 正文有依据标记，章末注列出各条大意 |
| 证明链 | PASS | 十边形/五边形、圆内四边形引理、弧差、半弧、弧和、弦弧比引理和一度近似均保留 |
| Book I.11 排除 | PASS | 范围注说明弦表本体不在本章范围 |
| 古今边界 | PASS | 未把原证明改写为三角函数、现代圆函数或现代天文学 |

## 章节质量门禁输入

- 译文：`chapters/translated/010_book_i_10_chords.md`
- 评审：`reviews/chapters/010_book_i_10_chords.review.md`
- 技术审计：`qa/technical/010_book_i_10_chords.technical_audit.md`
- 图表审计：`qa/technical/010_book_i_10_chords.diagram_table_audit.md`
- proof dependency map：`qa/technical/proof_dependency_map.md`
- numeric validation log：`qa/technical/numeric_validation_log.md`
- source recheck：`qa/pretranslation/010_book_i_10_formal_source_recheck.md`

下一步只能进入 Book I.10 章节质量门禁；仍不得进入终稿、正式 EPUB 或 Book II-XIII。
