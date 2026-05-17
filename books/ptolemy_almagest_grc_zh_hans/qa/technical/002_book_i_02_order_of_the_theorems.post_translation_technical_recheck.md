# Book I.2 译后技术复核 / Post-Translation Technical Recheck

chapter_id: `002_book_i_02_order_of_the_theorems`
recheck_status: `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING`
translation: `chapters/translated/002_book_i_02_order_of_the_theorems.md`
review: `reviews/chapters/002_book_i_02_order_of_the_theorems.review.md`

## 控制结论

- Book I.2 译文草稿已按古希腊文 source 文件和译前技术审计复核；未发现会阻断章节质量门禁的技术问题。
- 本章不含几何图、表格、六十进制数值、角度或天文学计算；无需图表标签审计或数值表抽取。
- 关键风险集中在全书论证次序、黄道/地理术语、恒星/行星模块，以及“显见现象、观测、几何证明”的方法链；译文已保留这些关系并在章末注说明。
- 本复核只允许进入后续章节质量门禁；仍不允许写 `chapters/final/002_book_i_02_order_of_the_theorems.md`，不允许生成正式 `output/book.epub`。

## Source Witness 边界

| 项目 | PASS/FAIL | 说明 |
|---|---|---|
| 古希腊文底稿为翻译基础 | PASS | 译文说明明确依据 `chapters/src/002_book_i_02_order_of_the_theorems.md`。 |
| 英译本只作 reference witness | PASS | 译文说明和评审均记录英文译本不得作为转译底稿。 |
| PDF/PAL 角色未混淆 | PASS | 本章 source extraction 与 formal recheck 已通过；PAL 转写作为古希腊辅助文本，Heiberg PDF 仍是正式影像依据。 |

## 术语复核

| Greek | locked Chinese | result | note |
|---|---|---|---|
| `τάξις / τάξεως` | 次序 / 安排次序 | PASS | 译文保留全书论证顺序功能。 |
| `λοξὸς κύκλος` | 黄道斜圈 / 倾斜圆 | PASS_WITH_FINAL_REVIEW_NOTE | 暂定译法；终稿需与 Book I.12-I.15 统一。 |
| `οἰκουμένη` | 居住世界 / 我们所居之地 | PASS | 译为“我们所居世界”，避免现代全球地理化。 |
| `ὁρίζων` | 地平圈 / 地平线 | PASS | 本章用“地平圈”保留球面语境。 |
| `ἠλιακὴ κίνησις / σεληνιακὴ κίνησις` | 太阳运动 / 月亮运动 | PASS | 未现代化为物理轨道。 |
| `ἀπλανῶν σφαῖρα` | 恒星天球 / 固定星天球 | PASS | 与后续恒星模块相容。 |
| `πέντε πλανῆται` | 五个行星 | PASS | 章末注已说明古代五行星模块。 |
| `φαινόμενα / τηρήσεις` | 显见现象 / 观测 | PASS | 方法链保留。 |
| `γραμμικαὶ ἔφοδοι` | 几何路线 / 线性几何方法 | PASS | 译为“几何方法中的证明”，可读且保留证明路径。 |

## 论证链复核

| source chain | translation result | status |
|---|---|---|
| 总体关系优先 | “整个地球同整个天的总体关系”已保留 | PASS |
| 黄道/居住世界/地平圈/倾斜差异 | 第一段完整保留 | PASS |
| 太阳与月亮先于诸星 | 第二段保留先后关系 | PASS |
| 恒星天球先于五行星 | 第二段保留模块顺序 | PASS |
| 显见现象与可靠观测作为基础 | 第三段保留 | PASS |
| 几何证明推进认识 | 第三段保留 | PASS |
| 总论命题链 | 天球形、地球形、地球居中、点的比例、无平移运动均保留 | PASS |

## 图表与数值

- 图形：本章无图形。
- 表格：本章无表格。
- 六十进制数值：本章无数值。
- 弧、角、弦关系：本章未进入几何弦论证。
- Euclid 依赖：本章未引用《几何原本》命题。

## 残留事项

- `黄道斜圈`、`地平圈`、`恒星天球` 需在 Book I.12-I.15 和后续恒星/行星章节中统一。
- 终稿阶段仍需检查第一段长句可读性；不得借润色删减章节次序关系。

## 下一步

1. 建立 Book I.2 章节质量门禁，聚合 source、formal recheck、chapter control、translation、review 和本技术复核。
2. 通过章节质量门禁前，不得写 `chapters/final/002_book_i_02_order_of_the_theorems.md`。
3. 继续推进 Book I.3 的 source extraction / PDF formal recheck，避免只在已译章节上局部循环。
