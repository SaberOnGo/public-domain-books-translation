# Book I.2 技术审计 / Technical Audit

chapter_id: `002_book_i_02_order_of_the_theorems`
audit_status: `PASS_FOR_TRANSLATION_PREP__NOT_TRANSLATED`

## 输入

- 原文章节：`chapters/src/002_book_i_02_order_of_the_theorems.md`
- source extraction 检查：`qa/pretranslation/002_book_i_02_source_extraction_check.md`
- PDF 页图证据：`qa/technical/page_screenshots/book_i02_pages_008_009_contact_sheet.jpg`
- 分章矩阵：`source/book_i_segmentation.md`
- 术语表：`qa/technical/mathematical_term_lock.md`
- 专名/术语边界：`metadata/source_witness_manifest.md`、`metadata/reference_witness_policy.md`

## 控制结论

- 本章说明整部论著的论证次序：先总论地球与天、黄道和居住世界，再论太阳/月亮及其现象，最后论恒星天球和五行星。
- 本章无几何图、无表格、无六十进制数值；但包含后续全书模型、观测和几何证明路线的术语入口。
- 允许进入 Book I.2 章节控制准备；仍不允许写 `chapters/final/`，不允许生成正式 EPUB。
- 英译本只能作 reference witness；不得把英译的现代天文学术语体系作为中文底稿。

## 审计项

| 项目 | PASS/FAIL | 证据位置 | 问题与处理 |
|---|---|---|---|
| source 文件存在且未翻译 | PASS | `chapters/src/002_book_i_02_order_of_the_theorems.md` | `translation_status=NOT_TRANSLATED` |
| PAL marker 与 segmentation 一致 | PASS | `qa/pretranslation/002_book_i_02_source_extraction_check.md` | marker count `34` |
| PDF 页图范围已定位 | PASS_FOR_PREP | viewer pages `8`-`9` | 已生成 contact sheet；正式终稿前仍需逐页视觉复核 |
| 图表/表格风险 | PASS | source/PDF range | 本章无图表、无表格 |
| 数值、角度、单位风险 | PASS | source/PDF range | 本章不含数学计算或六十进制值 |
| 全书次序风险 | PASS_WITH_TRANSLATION_RULE | `τάξις`, `προηγεῖται`, `πρῶτον`, `δεύτερον`, `τελευταίου` | 翻译必须保留全书论证顺序，不改写成现代目录简介 |
| 天文学对象风险 | PASS_WITH_TRANSLATION_RULE | `λοξὸς κύκλος`, `οἰκουμένη`, `ὁρίζων`, `ἀπλανῶν σφαῖρα`, `πέντε πλανῆται` | 需与后续黄道、地理、恒星和五行星章节统一 |
| 观测与证明关系 | PASS_WITH_TRANSLATION_RULE | `φαινόμενα`, `τηρήσεις`, `γραμμικαῖς ἐφόδοις ἀποδείξεων` | 保留“现象/观测为基础，几何证明推进”的方法链 |
| 参考译本边界 | PASS | source-control rules | 英译本只作 witness，不作为底稿 |

## 译前术语控制

| Greek | Chinese working term | status | note |
|---|---|---|---|
| τάξις / τάξεως | 次序 / 安排次序 | PRELOCK_FOR_BOOK_I2 | 论证和写作安排，不是现代教材目录 |
| λοξὸς κύκλος | 黄道斜圈 / 倾斜圆 | PRELOCK_FOR_BOOK_I2 | 后续需与 Book I.12-I.15 统一 |
| οἰκουμένη | 居住世界 / 我们所居之地 | PRELOCK_FOR_BOOK_I2 | 古代地理-天文学术语 |
| ὁρίζων | 地平圈 / 地平线 | PRELOCK_FOR_BOOK_I2 | 视球面语境决定 |
| ἐγκλίσεις | 倾斜 / 纬度差异相关倾角 | PRELOCK_FOR_BOOK_I2 | 暂不现代化为单一数理术语 |
| ἀπλανῶν σφαῖρα | 恒星天球 / 固定星天球 | PRELOCK_FOR_BOOK_I2 | 后续星表、恒星球章节需统一 |
| πέντε πλανῆται | 五个行星 | PRELOCK_FOR_BOOK_I2 | 指古代五行星模块 |
| φαινόμενα / τηρήσεις | 显见现象 / 观测 | PRELOCK_FOR_BOOK_I2 | 本章方法论核心 |
| γραμμικαὶ ἔφοδοι | 几何路线 / 线性几何方法 | PRELOCK_FOR_BOOK_I2 | 终稿前需与证明术语统一 |

## 下一步

1. 若开始 Book I.2 翻译准备，先建立 `qa/chapter_controls/002_book_i_02_order_of_the_theorems.control.md`。
2. 翻译时必须保留“全书论证顺序”和“观测加几何证明”的方法链。
3. 翻译后需要忠实度、中文可读性、术语一致性和古今概念边界审校。
