# Book I.6 译后技术复核 / Post-Translation Technical Recheck

chapter_id: `006_book_i_06_earth_as_point_to_heavens`
recheck_status: `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING`
translation: `chapters/translated/006_book_i_06_earth_as_point_to_heavens.md`
review: `reviews/chapters/006_book_i_06_earth_as_point_to_heavens.review.md`

## 控制结论

- Book I.6 译文草稿已按古希腊文 source 文件和译前技术审计复核；未发现会阻断章节质量门禁的技术问题。
- 本章不含几何图、表格、六十进制数值、角度或数学计算。
- 关键风险集中在点的比例命题、恒星天球距离、各地观测无差异、晷针与环仪中心、视线平面与地平圈、以及地平平面二分天球；译文已保留这些关系并在章末注说明。
- 本复核只允许进入后续章节质量门禁；仍不允许写 `chapters/final/006_book_i_06_earth_as_point_to_heavens.md`，不允许生成正式 `output/book.epub`。

## Source Witness 边界

| 项目 | PASS/FAIL | 说明 |
|---|---|---|
| 古希腊文底稿为翻译基础 | PASS | 译文说明明确依据 `chapters/src/006_book_i_06_earth_as_point_to_heavens.md`。 |
| 英译本只作 reference witness | PASS | 译文说明和评审均记录英文译本不得作为转译底稿。 |
| PDF/PAL 角色未混淆 | PASS | 本章 source extraction 与 formal recheck 已通过；PAL 转写作为古希腊辅助文本，Heiberg PDF 仍是正式影像依据。 |

## 术语复核

| Greek | locked Chinese | result | note |
|---|---|---|---|
| `σημείου λόγον ἔχει` | 具有点的比例 / 只相当于一点 | PASS | 正文用“只相当于一点”，注释保留字面比例语。 |
| `πρὸς αἴσθησιν` | 就感官观察而言 / 就可见现象而言 | PASS | 正文保留“就感官观察而言”。 |
| `ἀπλανῶν σφαῖρα` | 恒星天球 / 固定星天球 | PASS | 正文用“恒星天球”。 |
| `ἀπόστημα / ἀπόστασις` | 距离 / 相距 | PASS | 正文保留相对于天体距离的尺度关系。 |
| `μεγέθη καὶ διαστήματα τῶν ἄστρων` | 星体的大小和间距 | PASS | 正文保留可见大小和间距。 |
| `κλίματα` | 气候带 / 纬度带 | PASS_WITH_FINAL_REVIEW_NOTE | 正文用“气候带”；注释说明古代地理天文学语境。 |
| `γνώμων` | 晷针 / 日晷表针 | PASS | 正文用“晷针”。 |
| `κρικωταὶ σφαῖραι` | 环仪 / 环形球仪 | PASS_WITH_FINAL_REVIEW_NOTE | 正文用“环仪”；终稿前需同全书仪器术语统一。 |
| `διοπτεύσεις` | 瞄准观测 / 观测视准 | PASS | 正文用“瞄准观测”。 |
| `περιαγωγαὶ τῶν σκιῶν` | 影子的转动轨迹 | PASS | 正文保留影子转动轨迹。 |
| `ὁρίζοντες` | 地平圈 / 地平平面 | PASS | 正文用“地平圈”，注释说明几何平面含义。 |
| `διχοτομεῖν` | 二分 / 分成相等两半 | PASS | 正文保留二分整全天球。 |

## 论证链复核

| source chain | translation result | status |
|---|---|---|
| 地球相对于恒星天球距离具有点的比例 | 第一段保留主命题和可感尺度限定 | PASS |
| 各地观测星体大小和间距无差异 | 第二段保留同一时刻、不同气候带的观测证据 | PASS |
| 晷针与环仪中心可视同地心 | 第三段保留仪器中心、瞄准观测和影子转动轨迹 | PASS |
| 视线平面即地平圈并二分天球 | 第四段保留定义关系和二分结果 | PASS |
| 地球大小若可感则地表平面不能二分 | 末段保留地下部分大于地上部分的反证 | PASS |

## 图表与数值

- 图形：本章无图形。
- 表格：本章无表格。
- 六十进制数值：本章无六十进制值。
- 弧、角、弦关系：本章未进入几何弦论证。
- Euclid 依赖：本章未引用《几何原本》命题。

## 古今概念边界

- 正文未使用现代视差、现代恒星测距、现代地球半径比例或望远镜观测替换原论证。
- “恒星天球”“地平圈”“晷针”“环仪”均作为古代几何天文学/观测仪器语境处理。
- “点的比例”仅说明可感尺度，不给出现代数值化比例。

## 残留事项

- `环仪/环形球仪` 需在后续仪器或观测术语统一时复核。
- 终稿阶段可继续润色第三段仪器论证；不得借润色删掉“仪器中心可视同地心”的逻辑。

## 下一步

1. 建立 Book I.6 章节质量门禁，聚合 source、formal recheck、chapter control、translation、review 和本技术复核。
2. 通过章节质量门禁前，不得写 `chapters/final/006_book_i_06_earth_as_point_to_heavens.md`。
3. 继续推进 Book I.7 的 source extraction / PDF formal recheck，避免只在已译章节上局部循环。
