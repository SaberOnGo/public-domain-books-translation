# Book I.5 译后技术复核 / Post-Translation Technical Recheck

chapter_id: `005_book_i_05_earth_is_central`
recheck_status: `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING`
translation: `chapters/translated/005_book_i_05_earth_is_central.md`
review: `reviews/chapters/005_book_i_05_earth_is_central.review.md`

## 控制结论

- Book I.5 译文草稿已按古希腊文 source 文件和译前技术审计复核；未发现会阻断章节质量门禁的技术问题。
- 本章不含几何图、表格、六十进制数值、角度或数学计算；`六个`黄道十二分宫是可见/不可见分段计数，不是数值表。
- 关键风险集中在地球居中命题、三种非居中位置反证、地平圈等分、二分/昼夜长短变化、东西地平与中天时间、以及月食反证；译文已保留这些关系并在章末注说明。
- 本复核只允许进入后续章节质量门禁；仍不允许写 `chapters/final/005_book_i_05_earth_is_central.md`，不允许生成正式 `output/book.epub`。

## Source Witness 边界

| 项目 | PASS/FAIL | 说明 |
|---|---|---|
| 古希腊文底稿为翻译基础 | PASS | 译文说明明确依据 `chapters/src/005_book_i_05_earth_is_central.md`。 |
| 英译本只作 reference witness | PASS | 译文说明和评审均记录英文译本不得作为转译底稿。 |
| PDF/PAL 角色未混淆 | PASS | 本章 source extraction 与 formal recheck 已通过；PAL 转写作为古希腊辅助文本，Heiberg PDF 仍是正式影像依据。 |

## 术语复核

| Greek | locked Chinese | result | note |
|---|---|---|---|
| `μέση τοῦ οὐρανοῦ` | 位于天的中央 / 位于天球中央 | PASS | 正文保留“天球中央”主命题。 |
| `κέντρον σφαίρας` | 球心 / 球的中心 | PASS | 译为“如同球心”，保留模型比拟。 |
| `ἄξων` | 轴 / 天轴 | PASS | 译文保留天轴和两极关系。 |
| `πόλοι` | 极 / 天极 | PASS | 与 I.3、I.4 术语保持一致。 |
| `ὀρθὴ σφαῖρα` | 正球 / 正置天球 | PASS_WITH_FINAL_REVIEW_NOTE | 正文用“正球”；终稿前需与球面天文学章节统一。 |
| `ἐγκεκλιμένη σφαῖρα` | 斜球 / 倾斜天球 | PASS_WITH_FINAL_REVIEW_NOTE | 正文用“斜球”；终稿前需与 Book I.12-I.16 统一。 |
| `ἰσημερία` | 二分 / 昼夜平分 | PASS | 正文按语境用“昼夜平分”和“二分”。 |
| `ὁρίζων` | 地平圈 / 地平线 | PASS | 几何论证中译为“地平圈”。 |
| `ἰσημερινός` | 赤道圈 / 昼夜平分圈 | PASS | 正文用“赤道圈”。 |
| `μεσουράνησις` | 中天 | PASS | 正文保留升起到中天、从中天到落下的对称关系。 |
| `κλίματα` | 气候带 / 纬度带 | PASS_WITH_FINAL_REVIEW_NOTE | 正文用“气候带”；注释说明古代地理天文学语境。 |

## 论证链复核

| source chain | translation result | status |
|---|---|---|
| 地球位于天球中央，如同球心 | 第一段保留主命题和模型限定 | PASS |
| 三种非居中位置 | 第二段保留三分结构 | PASS |
| 轴外且向上/下偏移的反证 | 第三至四段保留正球、斜球、赤道圈和平行圆的反证 | PASS |
| 东/西偏移的反证 | 第五段保留星体大小/距离和中天时间对称性 | PASS |
| 在轴上偏向一极的反证 | 第六至七段保留气候带、地平面和黄道十二分宫平分论证 | PASS |
| 南北偏向与日晷影子 | 第八段保留二分时东西影子成直线的观测证据 | PASS |
| 总结与月食反证 | 末段保留昼夜增减次序和月食径直相对条件 | PASS |

## 图表与数值

- 图形：本章无图形。
- 表格：本章无表格。
- 六十进制数值：本章无六十进制值。
- 数值计数：`六个`黄道十二分宫只是分段可见性计数，不进入数值表控制。
- 弧、角、弦关系：本章未进入几何弦论证。
- Euclid 依赖：本章未引用《几何原本》命题。

## 古今概念边界

- 正文未使用现代物理中心、现代坐标系、牛顿力学、现代天体力学或惯性系替换原论证。
- “天球中央”“球心”“天轴”“地平圈”“中天”均作为古代几何天文学模型术语处理。
- “气候带”仅作古代地理天文学观测带，不作为现代气候学分类。

## 残留事项

- `正球/斜球`、`黄道十二分宫`、`气候带` 需在 Book I.12-I.16 球面天文学章节中统一。
- 终稿阶段可继续润色黄道十二分宫段；不得借润色删掉六个可见、六个不可见的平分论证。

## 下一步

1. 建立 Book I.5 章节质量门禁，聚合 source、formal recheck、chapter control、translation、review 和本技术复核。
2. 通过章节质量门禁前，不得写 `chapters/final/005_book_i_05_earth_is_central.md`。
3. 继续推进 Book I.6 的 source extraction / PDF formal recheck，避免只在已译章节上局部循环。
