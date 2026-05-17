# Book I.4 译后技术复核 / Post-Translation Technical Recheck

chapter_id: `004_book_i_04_earth_is_spherical`
recheck_status: `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING`
translation: `chapters/translated/004_book_i_04_earth_is_spherical.md`
review: `reviews/chapters/004_book_i_04_earth_is_spherical.review.md`

## 控制结论

- Book I.4 译文草稿已按古希腊文 source 文件和译前技术审计复核；未发现会阻断章节质量门禁的技术问题。
- 本章不含几何图、表格、六十进制数值、角度或天文学计算；无需图表标签审计或数值表抽取。
- 关键风险集中在月食时刻差异、东西向升落差异、地表形状反证、南北星象变化和航近高地证据；译文已保留这些关系并在章末注说明。
- 本复核只允许进入后续章节质量门禁；仍不允许写 `chapters/final/004_book_i_04_earth_is_spherical.md`，不允许生成正式 `output/book.epub`。

## Source Witness 边界

| 项目 | PASS/FAIL | 说明 |
|---|---|---|
| 古希腊文底稿为翻译基础 | PASS | 译文说明明确依据 `chapters/src/004_book_i_04_earth_is_spherical.md`。 |
| 英译本只作 reference witness | PASS | 译文说明和评审均记录英文译本不得作为转译底稿。 |
| PDF/PAL 角色未混淆 | PASS | 本章 source extraction 与 formal recheck 已通过；PAL 转写作为古希腊辅助文本，Heiberg PDF 仍是正式影像依据。 |

## 术语复核

| Greek | locked Chinese | result | note |
|---|---|---|---|
| `σφαιροειδής` | 球形的 / 近似球形的 | PASS | 正文保留章节主命题，不改写为现代地球椭球。 |
| `πρὸς αἴσθησιν` | 就感官观察而言 / 就可见现象而言 | PASS | 译为“就感官观察所及”，保留证明范围。 |
| `καθʼ ὅλα μέρη` | 按整体各部分看 | PASS | 正文保留整体限定。 |
| `ἐκλειπτικὰς φαντασίας` | 食的现象 / 食象 | PASS | 译为“食象”，并在语境中说明尤其是月食。 |
| `μεσημβρία` | 正午 / 子午 | PASS | 译为“正午”，保留本地计时语境。 |
| `ἀνατολικώτεροι / δυτικώτεροι` | 较东者 / 较西者 | PASS | 译文保持相对位置，不现代化为时区。 |
| `κυρτότης` | 凸曲 / 曲率 | PASS | 译为“凸曲”，用于地表和水面证据。 |
| `ἐπιπροσθήσεις` | 遮蔽 / 遮挡 | PASS | 译文用“遮挡”，说明曲面造成可见差异。 |
| `κοίλη / ἐπίπεδος` | 凹面 / 平面 | PASS | 反证备选形状已保留。 |
| `κυλινδροειδής` | 圆柱形的 | PASS | 圆柱形反证已保留。 |
| `τοῦ κόσμου πόλοι` | 世界的极 / 天极 | PASS_WITH_FINAL_REVIEW_NOTE | 正文用“世界的两极”；终稿可统一为“天极”并注出原文。 |
| `ἄρκτοι` | 北方 / 北极一带 | PASS | 正文用“北方”，注释说明方向语境。 |
| `προσπλέωμεν` | 航近 / 船行接近 | PASS | 航海观察证据已保留。 |

## 论证链复核

| source chain | translation result | status |
|---|---|---|
| 地球就感官观察所及为球形 | 第一段保留主命题和证明范围 | PASS |
| 日月星对不同地点升落时刻不同 | 第一段保留东方较早、西方较晚 | PASS |
| 同一食象在各地记录时刻不同 | 第二段保留月食、正午等距小时和东西向时刻差 | PASS |
| 小时差与地域距离成比例 | 第二段保留比例关系并推向地表球形 | PASS |
| 非球形备选反证 | 第三至四段保留凹面、平面、多边形和圆柱形反证 | PASS |
| 南北移动时星象改变 | 第四段保留北行时南星隐没、北星显现 | PASS |
| 航近高地证据 | 第五段保留高地从海面逐渐显现和水面凸曲解释 | PASS |

## 图表与数值

- 图形：本章无图形。
- 表格：本章无表格。
- 六十进制数值：本章无数值。
- 弧、角、弦关系：本章未进入几何弦论证。
- Euclid 依赖：本章未引用《几何原本》命题。

## 古今概念边界

- 正文未使用现代测地学、现代时区制度、地球椭球、大地水准面或现代光学替换原论证。
- “正午”“小时”只作为古代本地时刻记录语境保留。
- “凸曲”用于原文可见遮挡与水面形状解释，不作为现代精密曲率测量术语处理。

## 残留事项

- `世界的两极`、`北方`、`正午/子午` 需在后续地理、黄道和升降章节中统一。
- 终稿阶段可继续润色第二段关于“较东者记录时刻更晚”的句式；不得借润色改写为现代时区说明。

## 下一步

1. 建立 Book I.4 章节质量门禁，聚合 source、formal recheck、chapter control、translation、review 和本技术复核。
2. 通过章节质量门禁前，不得写 `chapters/final/004_book_i_04_earth_is_spherical.md`。
3. 继续推进 Book I.5 的 source extraction / PDF formal recheck，避免只在已译章节上局部循环。
