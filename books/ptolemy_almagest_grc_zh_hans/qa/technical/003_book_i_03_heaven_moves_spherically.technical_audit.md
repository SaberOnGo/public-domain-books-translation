# Book I.3 技术审计 / Technical Audit

chapter_id: `003_book_i_03_heaven_moves_spherically`
audit_status: `PASS_FOR_TRANSLATION_PREP__NOT_TRANSLATED`

## 输入

- 原文章节：`chapters/src/003_book_i_03_heaven_moves_spherically.md`
- source extraction 检查：`qa/pretranslation/003_book_i_03_source_extraction_check.md`
- PDF 页图证据：`qa/technical/page_screenshots/book_i03_pages_009_011_contact_sheet.jpg`
- 分章矩阵：`source/book_i_segmentation.md`
- 术语表：`qa/technical/mathematical_term_lock.md`
- 参考边界：`metadata/source_witness_manifest.md`、`metadata/reference_witness_policy.md`

## 控制结论

- 本章证明“天以球形方式运动”，是 Book I 基础天文学论证链的第一章。
- 本章无图形、无表格、无六十进制数值；但包含观测证据、反证链、地平处视大小解释、天球几何与古代自然学论证。
- 允许进入 Book I.3 章节控制准备；仍不允许写 `chapters/final/`，不允许生成正式 EPUB。
- 英译本只能作 reference witness；不得把本章现代化为现代天体物理或大气光学说明。

## 审计项

| 项目 | PASS/FAIL | 证据位置 | 问题与处理 |
|---|---|---|---|
| source 文件存在且未翻译 | PASS | `chapters/src/003_book_i_03_heaven_moves_spherically.md` | `translation_status=NOT_TRANSLATED` |
| PAL marker 与 segmentation 一致 | PASS | `qa/pretranslation/003_book_i_03_source_extraction_check.md` | marker count `109` |
| PDF 页图范围已定位 | PASS_FOR_PREP | viewer pages `9`-`11` | 已生成 contact sheet；正式终稿前仍需逐页视觉复核 |
| 图表/表格风险 | PASS | source/PDF range | 本章无图形、无表格 |
| 数值、角度、单位风险 | PASS | source/PDF range | 本章不含数学计算或六十进制值 |
| 观测链 | PASS_WITH_TRANSLATION_RULE | 日月星从东向西、升起落下、平行圆、恒显星 | 翻译必须保持观测先导，不改写为现代物理机制 |
| 反证链 | PASS_WITH_TRANSLATION_RULE | 直线向无穷远运动、星体大小不应如此呈现 | 必须保留问句/反证推进关系 |
| 地平处视大小解释 | PASS_WITH_TRANSLATION_RULE | `ἀναθυμίασις` 与水中物体类比 | 可译为湿气蒸腾，不得直接写成现代大气折射 |
| 球形/圆形几何论证 | PASS_WITH_TRANSLATION_RULE | 圆、球、同周长多边形、最大形体 | 需保留古代几何比较，不改成现代极值定理 |
| 自然学论证 | PASS_WITH_TRANSLATION_RULE | 以太、同质性、天上/地上形体 | 需保留古代自然学边界，不现代化 |
| 参考译本边界 | PASS | source-control rules | 英译本只作 witness，不作为底稿 |

## 译前术语控制

| Greek | Chinese working term | status | note |
|---|---|---|---|
| σφαιροειδῶς φέρεται | 以球形方式运动 / 作球形运动 | PRELOCK_FOR_BOOK_I3 | 主命题 |
| παράλληλοι κύκλοι | 平行圆 | PRELOCK_FOR_BOOK_I3 | 天体每日视运动圆 |
| αἰεὶ φανεροὶ ἀστέρες | 恒显星 / 常显星 | PRELOCK_FOR_BOOK_I3 | 永远在地平上方的星 |
| πόλος | 极 / 天球极 | PRELOCK_FOR_BOOK_I3 | 天球中心点/极点语境 |
| οὐρανία σφαῖρα | 天球 | PRELOCK_FOR_BOOK_I3 | 几何模型语境 |
| ἐπʼ εὐθείας ... ἐπʼ ἄπειρον | 沿直线向无穷远运动 | PRELOCK_FOR_BOOK_I3 | 反证对象 |
| ἀναθυμίασις | 蒸腾气 / 湿气蒸腾 | PRELOCK_FOR_BOOK_I3 | 地平处视觉解释 |
| ὡροσκοπία | 升度/时刻观测构造 | PRELOCK_FOR_BOOK_I3 | 后续需继续核定 |
| αἰθήρ | 以太 | PRELOCK_FOR_BOOK_I3 | 古代自然学术语 |
| ὁμοιομέρεια | 同质性 | PRELOCK_FOR_BOOK_I3 | 支撑均匀圆形运动 |

## 下一步

1. 若开始 Book I.3 翻译准备，先建立 `qa/chapter_controls/003_book_i_03_heaven_moves_spherically.control.md`。
2. 翻译时必须保留“观测 → 反证 → 几何论证 → 自然学论证”的证明链。
3. 翻译后需要忠实度、中文可读性、术语一致性、数学/天文学证明链和古今概念边界审校。
