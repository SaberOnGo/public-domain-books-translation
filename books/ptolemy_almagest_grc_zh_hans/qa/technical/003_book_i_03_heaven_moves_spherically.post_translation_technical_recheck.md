# Book I.3 译后技术复核 / Post-Translation Technical Recheck

chapter_id: `003_book_i_03_heaven_moves_spherically`
recheck_status: `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING`
translation: `chapters/translated/003_book_i_03_heaven_moves_spherically.md`
review: `reviews/chapters/003_book_i_03_heaven_moves_spherically.review.md`

## 控制结论

- Book I.3 译文草稿已按古希腊文 source 文件和译前技术审计复核；未发现会阻断章节质量门禁的技术问题。
- 本章不含几何图、表格、六十进制数值、角度或天文学计算；无需图表标签审计或数值表抽取。
- 关键风险集中在观测链、恒显星绕极、直线无穷运动反证、球形/圆形几何比较、湿气蒸腾，以及以太/同质性自然学论证；译文已保留这些关系并在章末注说明。
- 本复核只允许进入后续章节质量门禁；仍不允许写 `chapters/final/003_book_i_03_heaven_moves_spherically.md`，不允许生成正式 `output/book.epub`。

## Source Witness 边界

| 项目 | PASS/FAIL | 说明 |
|---|---|---|
| 古希腊文底稿为翻译基础 | PASS | 译文说明明确依据 `chapters/src/003_book_i_03_heaven_moves_spherically.md`。 |
| 英译本只作 reference witness | PASS | 译文说明和评审均记录英文译本不得作为转译底稿。 |
| PDF/PAL 角色未混淆 | PASS | 本章 source extraction 与 formal recheck 已通过；PAL 转写作为古希腊辅助文本，Heiberg PDF 仍是正式影像依据。 |

## 术语复核

| Greek | locked Chinese | result | note |
|---|---|---|---|
| `σφαιροειδῶς φέρεται` | 以球形方式运动 / 作球形运动 | PASS | 正文保留章节主命题，章末注说明不是现代动力学改写。 |
| `παράλληλοι κύκλοι` | 平行圆 | PASS | 译文保留日月星从东到西沿平行圆升落的观测链。 |
| `αἰεὶ φανεροὶ ἀστέρες` | 恒显星 / 常显星 | PASS | 正文用“恒显星”，注释解释为特定地点始终不落的星。 |
| `πόλος` | 极 / 天球的极 | PASS | 译为“天球的极”，保留绕同一中心旋转的模型功能。 |
| `οὐρανία σφαῖρα` | 天球 | PASS | 与 Book I.2 的天球术语相容。 |
| `ἐπʼ εὐθείας ... ἐπʼ ἄπειρον` | 沿直线向无穷远处运动 | PASS | 反证对象完整保留。 |
| `ἀναθυμίασις` | 湿气蒸腾 / 蒸腾气 | PASS | 未在正文中现代化为大气折射。 |
| `ὡροσκοπίων κατασκευαί` | 升度构造 | PASS_WITH_FINAL_REVIEW_NOTE | 暂定译法；需与后续球面天文学章节统一。 |
| `αἰθήρ` | 以太 | PASS | 注释明确古代自然学边界。 |
| `ὁμοιομέρεια` | 同质性 / 同质 | PASS | 保留同质物体与同质表面的自然学论证。 |

## 论证链复核

| source chain | translation result | status |
|---|---|---|
| 古人从观察形成最初观念 | 第一段完整保留日月星升起、升高、下降、隐没和再次出现 | PASS |
| 恒显星绕同一中心旋转 | 第二段保留恒显星、天球的极、大小圆和隐没时长差异 | PASS |
| 一切现象反证异说 | 第二段末尾保留“现象反证不同设想”的过渡 | PASS |
| 反证直线无穷运动 | 第三至四段保留每日同起点、返回不可见、大小变化、地面截断、点燃/熄灭和恒显星问题 | PASS |
| 非球形导致距离不等 | 第五段保留距离不等会导致大小和星间距变化，而观测不支持 | PASS |
| 地平处视大小 | 第六段保留湿气蒸腾解释和水中物体类比 | PASS |
| 升度构造与几何比较 | 第七段保留升度构造只与球形假设相合、圆/球最易动、同周长形状最大比较 | PASS |
| 以太和同质性自然学论证 | 第八至九段保留以太、同质表面、平面/立体、神圣天体与球形关系 | PASS |

## 图表与数值

- 图形：本章无图形。
- 表格：本章无表格。
- 六十进制数值：本章无数值。
- 弧、角、弦关系：本章未进入几何弦论证。
- Euclid 依赖：本章未引用《几何原本》命题。

## 古今概念边界

- 正文未使用现代物理轨道、现代天体物理或现代大气光学术语替换原论证。
- “湿气蒸腾”只作为原文古代视觉解释保留；后续可在注释或术语表中说明它不同于现代大气折射。
- “以太”和“同质性”只作为古代自然学论证术语保留，不作为现代物理实体或材料科学术语处理。

## 残留事项

- `升度构造` 需在 Book I.12-I.16 的黄道、地平和升降章节中统一。
- 终稿阶段可继续润色自然学段句式；不得借润色删除“观测 → 反证 → 几何比较 → 自然学论证”的链条。

## 下一步

1. 建立 Book I.3 章节质量门禁，聚合 source、formal recheck、chapter control、translation、review 和本技术复核。
2. 通过章节质量门禁前，不得写 `chapters/final/003_book_i_03_heaven_moves_spherically.md`。
3. 继续推进 Book I.4 的 source extraction / PDF formal recheck，避免只在已译章节上局部循环。
