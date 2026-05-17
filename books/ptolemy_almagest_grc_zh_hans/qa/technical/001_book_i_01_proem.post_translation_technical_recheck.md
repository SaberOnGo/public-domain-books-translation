# Book I.1 译后技术复核 / Post-Translation Technical Recheck

chapter_id: `001_book_i_01_proem`
recheck_status: `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING`
translation: `chapters/translated/001_book_i_01_proem.md`
review: `reviews/chapters/001_book_i_01_proem.review.md`

## 控制结论

- Book I.1 译文草稿已按古希腊文 source 文件和译前技术审计复核；未发现会阻断章节质量门禁的技术问题。
- 本章不含几何图、表格、六十进制数值、角度或天文学计算；无需图表标签审计或数值表抽取。
- 关键风险集中在古代学科分类和概念边界；译文已通过章末注说明，不把 `自然学` 现代化为物理学，也不把 `实践部分` 现代化为应用科学。
- 本复核只允许进入后续章节质量门禁；仍不允许写 `chapters/final/001_book_i_01_proem.md`，不允许生成正式 `output/book.epub`。

## Source Witness 边界

| 项目 | PASS/FAIL | 说明 |
|---|---|---|
| 古希腊文底稿为翻译基础 | PASS | 译文说明明确依据 `chapters/src/001_book_i_01_proem.md`。 |
| 英译本只作 reference witness | PASS | 译文说明和评审均记录英文译本不得作为转译底稿。 |
| PDF/PAL 角色未混淆 | PASS | 本章 source extraction 与 formal recheck 已通过；PAL 转写作为古希腊辅助文本，Heiberg PDF 仍是正式影像依据。 |

## 术语复核

| Greek | locked Chinese | result | note |
|---|---|---|---|
| `θεωρητικόν` | 理论部分 / 理论的 | PASS | 与 `实践部分` 对举保留。 |
| `πρακτικόν` | 实践部分 / 实践的 | PASS | 未译作现代“应用科学”。 |
| `φυσικόν` | 自然学 | PASS | 正文未译作现代“物理学”。 |
| `μαθηματικόν / μαθηματικά` | 数学 / 数学诸学 | PASS | 保留其通向天文学理论的古代学科范围。 |
| `θεολογικόν` | 神学性研究 / 神学部分 | PASS | 章末注已说明不是现代宗教教义意义。 |
| `οὐράνια` | 天体 / 天上事物 | PASS | 与天体理论研究语境一致。 |

## 论证链复核

| source chain | translation result | status |
|---|---|---|
| 理论部分与实践部分区分 | 开篇已保留理论/实践差异和二者获益方式 | PASS |
| 亚里士多德理论哲学三分 | 自然学、数学、神学性研究三分完整 | PASS |
| 数学的确定性 | 通过算术和几何获得稳固知识的论证保留 | PASS |
| 天上/神圣事物作为研究对象 | 对永远如此、同一状态之事物的研究保留 | PASS |
| 数学对神学性研究、自然学和伦理实践的助益 | 三段助益关系均保留 | PASS |
| 本书写作计划 | 简明列出天体理论所需内容、详略处理前人工作的计划保留 | PASS |

## 图表与数值

- 图形：本章无图形。
- 表格：本章无表格。
- 六十进制数值：本章无数值。
- 弧、角、弦关系：本章未进入几何弦论证。
- Euclid 依赖：本章未引用《几何原本》命题。

## 残留事项

- `叙鲁斯` 需在全书专名表进入终稿前统一锁定。
- 终稿阶段仍需按全书风格检查中文节奏；不得借润色删减古代学科分类链条。

## 下一步

1. 建立 Book I.1 章节质量门禁，聚合 source、formal recheck、chapter control、translation、review 和本技术复核。
2. 通过章节质量门禁前，不得写 `chapters/final/001_book_i_01_proem.md`。
3. 继续推进 Book I.2 的 source extraction / PDF formal recheck，避免只在 I.1/I.10 上局部循环。
