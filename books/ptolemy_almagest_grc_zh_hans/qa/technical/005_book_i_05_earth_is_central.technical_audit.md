# Book I.5 技术审计 / Technical Audit

chapter_id: `005_book_i_05_earth_is_central`
audit_status: `PASS_FOR_TRANSLATION_PREP__NOT_TRANSLATED`

## 输入

- 原文章节：`chapters/src/005_book_i_05_earth_is_central.md`
- source extraction 检查：`qa/pretranslation/005_book_i_05_source_extraction_check.md`
- PDF 页图证据：`qa/technical/page_screenshots/book_i05_pages_012_014_contact_sheet.jpg`
- 分章矩阵：`source/book_i_segmentation.md`
- 术语表：`qa/technical/mathematical_term_lock.md`
- 参考边界：`metadata/source_witness_manifest.md`、`metadata/reference_witness_policy.md`

## 控制结论

- 本章论证“地球位于天球中央”，是 Book I 地心位置命题的基础章节。
- 本章无图形、无表格、无六十进制数值；但包含三种非居中位置的反证链、地平圈等分论证、昼夜/二分点观测、东方/西方地平与中天时间对称性、以及各地气候带的地平面差异问题。
- 允许进入 Book I.5 章节控制准备；仍不允许直接翻译，不允许写 `chapters/final/`，不允许生成正式 EPUB。
- 英译本只能作 reference witness；不得把本章现代化为牛顿力学、现代地心惯性系、现代坐标系或近代天体力学说明。

## 审计项

| 项目 | PASS/FAIL | 证据位置 | 问题与处理 |
|---|---|---|---|
| source 文件存在且未翻译 | PASS | `chapters/src/005_book_i_05_earth_is_central.md` | `translation_status=NOT_TRANSLATED` |
| PAL marker 与 segmentation 一致 | PASS | `qa/pretranslation/005_book_i_05_source_extraction_check.md` | marker count `78` |
| PDF 页图范围已定位 | PASS_FOR_PREP | viewer pages `12`-`14` | 已生成 contact sheet；正式终稿前仍需逐页视觉复核 |
| 图表/表格风险 | PASS | source/PDF range | 本章无几何图形和正式表格 |
| 数值、角度、单位风险 | PASS | source/PDF range | 本章不含数学计算或六十进制值 |
| 地球居中命题 | PASS_WITH_TRANSLATION_RULE | `μέση τοῦ οὐρανοῦ`、`κέντρον σφαίρας` | 正文应译为“位于天球中央/如球心”，避免现代物理化 |
| 三种非居中位置 | PASS_WITH_TRANSLATION_RULE | 轴外且距两极相等、在轴上偏向一极、不在轴上且距两极不等 | 不得省略三分反证结构 |
| 地平圈等分 | PASS_WITH_TRANSLATION_RULE | `ὁρίζων`、`ὑπὲρ γῆν`、`ὑπὸ γῆν` | 保留地平圈把上/下部分等分或不等分的几何含义 |
| 二分点/昼夜证据 | PASS_WITH_TRANSLATION_RULE | `ἰσημερία`、夏至/冬至最大日长变化 | 不现代化为现代天文学教材叙述 |
| 东西地平和中天时间 | PASS_WITH_TRANSLATION_RULE | `ἀνατολὰς`、`δυσμὰς`、`μεσουράνησις` | 保留从升起到中天、从中天到落下的时间对称性 |
| 气候带与地平面差异 | PASS_WITH_TRANSLATION_RULE | `κλίματα`、`τοῦ ὁρίζοντος ἐπίπεδον` | `κλίματα` 暂按古代天文学“气候带/纬度带”处理 |
| 参考译本边界 | PASS | source-control rules | 英译本只作 witness，不作为底稿 |

## 译前术语控制

| Greek | Chinese working term | status | note |
|---|---|---|---|
| μέση τοῦ οὐρανοῦ | 位于天的中央 / 位于天球中央 | PRELOCK_FOR_BOOK_I5 | 主命题；避免写成现代物理中心 |
| κέντρον σφαίρας | 球心 / 球的中心 | PRELOCK_FOR_BOOK_I5 | 比喻地球相对天球的位置 |
| ἄξων | 轴 / 天轴 | PRELOCK_FOR_BOOK_I5 | 与两极和地球偏置反证相关 |
| πόλοι | 极 / 天极 | PRELOCK_FOR_BOOK_I5 | 与 I.3、I.4 术语保持一致 |
| ὀρθὴ σφαῖρα | 正球 / 正置天球 | PRELOCK_FOR_BOOK_I5 | 终稿前需与球面天文学章节统一 |
| ἐγκεκλιμένη σφαῖρα | 斜球 / 倾斜天球 | PRELOCK_FOR_BOOK_I5 | 终稿前需与 Book I.12-I.16 统一 |
| ἰσημερία | 二分 / 昼夜平分 | PRELOCK_FOR_BOOK_I5 | 视上下文译为“二分点”或“昼夜等分” |
| ὁρίζων | 地平圈 / 地平线 | PRELOCK_FOR_BOOK_I5 | 几何论证中优先“地平圈” |
| ἰσημερινός | 赤道圈 / 昼夜平分圈 | PRELOCK_FOR_BOOK_I5 | 后续需与 Book I.12-I.15 统一 |
| μεσουράνησις | 中天 | PRELOCK_FOR_BOOK_I5 | 升起到中天、从中天到落下的时间关系 |
| κλίματα | 气候带 / 纬度带 | PRELOCK_FOR_BOOK_I5 | 古代地理天文学术语，不作现代气候学解释 |

## 下一步

1. 若开始 Book I.5 翻译准备，先建立 `qa/chapter_controls/005_book_i_05_earth_is_central.control.md`。
2. 翻译时必须保留“三种非居中位置 → 观测反证 → 地球居中”的证明链。
3. 翻译后需要忠实度、中文可读性、术语一致性、天文学模型边界和古今概念边界审校。
