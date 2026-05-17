# Book I.4 技术审计 / Technical Audit

chapter_id: `004_book_i_04_earth_is_spherical`
audit_status: `PASS_FOR_TRANSLATION_PREP__NOT_TRANSLATED`

## 输入

- 原文章节：`chapters/src/004_book_i_04_earth_is_spherical.md`
- source extraction 检查：`qa/pretranslation/004_book_i_04_source_extraction_check.md`
- PDF 页图证据：`qa/technical/page_screenshots/book_i04_pages_011_012_contact_sheet.jpg`
- 分章矩阵：`source/book_i_segmentation.md`
- 术语表：`qa/technical/mathematical_term_lock.md`
- 参考边界：`metadata/source_witness_manifest.md`、`metadata/reference_witness_policy.md`

## 控制结论

- 本章证明“地球就感官观察所及、按整体各部分看也是球形的”，是 Book I 地球形状基础论证。
- 本章无图形、无表格、无六十进制数值；但包含月食时刻差异、东西向升落差异、反证凹面/平面/多边形/圆柱形地球，以及航近山地逐渐显现的观测证据。
- 允许进入 Book I.4 章节控制准备；仍不允许写 `chapters/final/`，不允许生成正式 EPUB。
- 英译本只能作 reference witness；不得把本章现代化为现代地球椭球、经度时区制度或现代测地学说明。

## 审计项

| 项目 | PASS/FAIL | 证据位置 | 问题与处理 |
|---|---|---|---|
| source 文件存在且未翻译 | PASS | `chapters/src/004_book_i_04_earth_is_spherical.md` | `translation_status=NOT_TRANSLATED` |
| PAL marker 与 segmentation 一致 | PASS | `qa/pretranslation/004_book_i_04_source_extraction_check.md` | marker count `50` |
| PDF 页图范围已定位 | PASS_FOR_PREP | viewer pages `11`-`12` | 已生成 contact sheet；正式终稿前仍需逐页视觉复核 |
| 图表/表格风险 | PASS | source/PDF range | 本章无图形、无表格 |
| 数值、角度、单位风险 | PASS | source/PDF range | 本章不含数学计算或六十进制值 |
| 月食时刻证据 | PASS_WITH_TRANSLATION_RULE | `ἐκλειπτικὰς φαντασίας`、`σεληνιακὰς` | 必须保留同一食象在各地记录时刻不同，不现代化为时区 |
| 东西向升落差异 | PASS_WITH_TRANSLATION_RULE | 东方居住者较早、西方较晚 | 保留观测相对关系和地表曲率推论 |
| 形状反证链 | PASS_WITH_TRANSLATION_RULE | 凹面、平面、多边形、圆柱形 | 翻译不得省略备选形状及其反证结果 |
| 恒显星/南北移动证据 | PASS_WITH_TRANSLATION_RULE | 北行时南星隐没、北星显现 | 与 I.3 恒显星术语保持一致 |
| 航近高地证据 | PASS_WITH_TRANSLATION_RULE | 山和高地从海面逐渐显现 | 保留“因水面凸曲先前被遮没”的观察解释 |
| 参考译本边界 | PASS | source-control rules | 英译本只作 witness，不作为底稿 |

## 译前术语控制

| Greek | Chinese working term | status | note |
|---|---|---|---|
| σφαιροειδής | 球形的 / 近似球形的 | PRELOCK_FOR_BOOK_I4 | 主命题，不改写为现代地球椭球 |
| πρὸς αἴσθησιν | 就感官观察而言 / 就可见现象而言 | PRELOCK_FOR_BOOK_I4 | 限定证明范围 |
| καθʼ ὅλα μέρη | 按整体各部分看 | PRELOCK_FOR_BOOK_I4 | 保留整体限定 |
| ἐκλειπτικὰς φαντασίας | 食的现象 / 食象 | PRELOCK_FOR_BOOK_I4 | 尤其指月食记录 |
| μεσημβρία | 正午 / 子午 | PRELOCK_FOR_BOOK_I4 | 与时刻记录有关 |
| ἀνατολικώτεροι / δυτικώτεροι | 较东者 / 较西者 | PRELOCK_FOR_BOOK_I4 | 不现代化为时区 |
| κυρτότης | 凸曲 / 曲率 | PRELOCK_FOR_BOOK_I4 | 地表/水面形状证据 |
| ἐπιπροσθήσεις | 遮蔽 / 遮挡 | PRELOCK_FOR_BOOK_I4 | 地球凸曲造成的遮挡 |
| κοίλη / ἐπίπεδος | 凹面 / 平面 | PRELOCK_FOR_BOOK_I4 | 反证备选形状 |
| κυλινδροειδής | 圆柱形的 | PRELOCK_FOR_BOOK_I4 | 反证备选形状 |
| τοῦ κόσμου πόλοι | 世界的极 / 天极 | PRELOCK_FOR_BOOK_I4 | 与圆柱形反证相关 |
| ἄρκτοι | 北方 / 北极一带 | PRELOCK_FOR_BOOK_I4 | 后续需统一方位译法 |
| προσπλέωμεν | 航近 / 船行接近 | PRELOCK_FOR_BOOK_I4 | 海上观测证据 |

## 下一步

1. 若开始 Book I.4 翻译准备，先建立 `qa/chapter_controls/004_book_i_04_earth_is_spherical.control.md`。
2. 翻译时必须保留“月食/升落时刻 → 形状反证 → 南北星象变化 → 航近高地”的证明链。
3. 翻译后需要忠实度、中文可读性、术语一致性、数学/天文学证明链和古今概念边界审校。
