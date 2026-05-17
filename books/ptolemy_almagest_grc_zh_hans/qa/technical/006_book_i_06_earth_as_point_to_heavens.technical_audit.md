# Book I.6 技术审计 / Technical Audit

chapter_id: `006_book_i_06_earth_as_point_to_heavens`
audit_status: `PASS_FOR_TRANSLATION_PREP__NOT_TRANSLATED`

## 输入

- 原文章节：`chapters/src/006_book_i_06_earth_as_point_to_heavens.md`
- source extraction 检查：`qa/pretranslation/006_book_i_06_source_extraction_check.md`
- PDF 页图证据：`qa/technical/page_screenshots/book_i06_page_014_contact_sheet.jpg`
- 分章矩阵：`source/book_i_segmentation.md`
- 术语表：`qa/technical/mathematical_term_lock.md`
- 参考边界：`metadata/source_witness_manifest.md`、`metadata/reference_witness_policy.md`

## 控制结论

- 本章论证“地球相对于天体距离只相当于一点”，是 Book I 从地球居中命题转入观测尺度论证的短章。
- 本章无图形、无表格、无六十进制数值；但包含恒星天球距离、各地观测无差异、日晷与环仪中心、视线平面即地平圈、以及地平平面二分整全天球的证明链。
- 允许进入 Book I.6 章节控制准备；仍不允许直接翻译，不允许写 `chapters/final/`，不允许生成正式 EPUB。
- 英译本只能作 reference witness；不得把“点的比例”现代化为真实天文半径、视差数值、近代测距或现代宇宙尺度说明。

## 审计项

| 项目 | PASS/FAIL | 证据位置 | 问题与处理 |
|---|---|---|---|
| source 文件存在且未翻译 | PASS | `chapters/src/006_book_i_06_earth_as_point_to_heavens.md` | `translation_status=NOT_TRANSLATED` |
| PAL marker 与 segmentation 一致 | PASS | `qa/pretranslation/006_book_i_06_source_extraction_check.md` | marker count `27` |
| PDF 页图范围已定位 | PASS_FOR_PREP | viewer page `14` | 已生成 contact sheet；正式终稿前仍需逐页视觉复核 |
| 图表/表格风险 | PASS | source/PDF range | 本章无几何图形和正式表格 |
| 数值、角度、单位风险 | PASS | source/PDF range | 本章不含数学计算或六十进制值 |
| 点的比例命题 | PASS_WITH_TRANSLATION_RULE | `σημείου λόγον ἔχει` | 应译成“只相当于一点/具有点的比例”，并说明这是相对于天体距离的可感尺度命题 |
| 恒星天球距离 | PASS_WITH_TRANSLATION_RULE | `τῆς τῶν ἀπλανῶν ... σφαίρας ἀπόστημα` | 可译为“到所谓恒星天球的距离”，不得解释成现代恒星距离 |
| 各地观测无差异 | PASS_WITH_TRANSLATION_RULE | `ἀπὸ πάντων ... τῶν μερῶν`、`διαφόρων κλιμάτων` | 保留各地观测星体大小、距离相同的经验论证 |
| 日晷与环仪中心 | PASS_WITH_TRANSLATION_RULE | `γνώμονας`、`κρικωτῶν σφαιρῶν κέντρα` | `γνώμων` 暂译“日晷表针/晷针”；`κρικωταὶ σφαῖραι` 暂按观测用环仪/环形球处理 |
| 视线平面与地平圈 | PASS_WITH_TRANSLATION_RULE | `διὰ τῶν ὄψεων ... ἐπίπεδα`、`ὁρίζοντας` | 保留“由视线引出的平面，即所谓地平圈”的几何关系 |
| 天球二分论证 | PASS_WITH_TRANSLATION_RULE | `διχοτομεῖν ... τὴν ὅλην σφαῖραν τοῦ οὐρανοῦ` | 译文应明确地平平面总是二分整个天球 |
| 古今概念边界 | PASS | technical audit | 不得引入现代地球半径、恒星距离、视差、折射或仪器史外插 |
| 参考译本边界 | PASS | source-control rules | 英译本只作 witness，不作为底稿 |

## 译前术语控制

| Greek | Chinese working term | status | note |
|---|---|---|---|
| σημείου λόγον ἔχει | 具有点的比例 / 只相当于一点 | PRELOCK_FOR_BOOK_I6 | 本章主命题；正文优先用读者可懂的“只相当于一点”，注释保留“点的比例” |
| πρὸς αἴσθησιν | 就感官观察而言 / 就可见现象而言 | PRELOCK_FOR_BOOK_I6 | 与 Book I.4 一致，限定观测尺度 |
| ἀπλανῶν σφαῖρα | 恒星天球 / 固定星天球 | PRELOCK_FOR_BOOK_I6 | 与 Book I.2 术语保持一致 |
| ἀπόστημα / ἀπόστασις | 距离 / 相距 | PRELOCK_FOR_BOOK_I6 | 不现代化为精确天文距离 |
| μεγέθη καὶ διαστήματα τῶν ἄστρων | 星体的大小和间距 | PRELOCK_FOR_BOOK_I6 | 依上下文指可见大小和相互间距 |
| κλίματα | 气候带 / 纬度带 | PRELOCK_FOR_BOOK_I6 | 与 Book I.5 一致，古代地理天文学术语 |
| γνώμων | 晷针 / 日晷表针 | PRELOCK_FOR_BOOK_I6 | 用于影子转动和观测设置 |
| κρικωταὶ σφαῖραι | 环仪 / 环形球仪 | PRELOCK_FOR_BOOK_I6 | 终稿前需与仪器术语统一 |
| διοπτεύσεις | 瞄准观测 / 观测视准 | PRELOCK_FOR_BOOK_I6 | 不泛化为现代望远镜观测 |
| περιαγωγαὶ τῶν σκιῶν | 影子的转动轨迹 | PRELOCK_FOR_BOOK_I6 | 与晷针观测相关 |
| ὁρίζοντες | 地平圈 / 地平平面 | PRELOCK_FOR_BOOK_I6 | 本章重点是由视线平面产生的地平 |
| διχοτομεῖν | 二分 / 分成相等两半 | PRELOCK_FOR_BOOK_I6 | 用于地平平面二分天球 |

## 下一步

1. 若开始 Book I.6 翻译准备，先建立 `qa/chapter_controls/006_book_i_06_earth_as_point_to_heavens.control.md`。
2. 翻译时必须保留“观测无差异 → 仪器中心等同地心 → 地平平面二分天球 → 地球大小不可感”的证明链。
3. 翻译后需要忠实度、中文可读性、术语一致性、天文学模型边界和古今概念边界审校。
