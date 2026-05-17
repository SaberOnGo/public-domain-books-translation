# Book I.7 技术审计 / Technical Audit

chapter_id: `007_book_i_07_earth_has_no_translational_motion`
audit_status: `PASS_FOR_TRANSLATION_PREP__NOT_TRANSLATED`

## 输入

- 原文章节：`chapters/src/007_book_i_07_earth_has_no_translational_motion.md`
- source extraction 检查：`qa/pretranslation/007_book_i_07_source_extraction_check.md`
- PDF 页图证据：`qa/technical/page_screenshots/book_i07_pages_015_017_contact_sheet.jpg`
- 分章矩阵：`source/book_i_segmentation.md`
- 术语表：`qa/technical/mathematical_term_lock.md`
- 参考边界：`metadata/source_witness_manifest.md`、`metadata/reference_witness_policy.md`

## 控制结论

- 本章论证“地球没有平移运动”，并附带反驳“天不动而地球每日自转”或天地共同转动的解释。
- 本章无几何图形、无表格、无六十进制数值；风险集中在古代自然学与天文学概念边界。
- 允许进入 Book I.7 章节控制准备；仍不允许直接翻译，不允许写 `chapters/final/`，不允许生成正式 EPUB。
- 英译本只能作 reference witness；不得把本章改写成近代惯性、相对运动、科里奥利力、重力场或现代地球自转争论。

## 审计项

| 项目 | PASS/FAIL | 证据位置 | 问题与处理 |
|---|---|---|---|
| source 文件存在且未翻译 | PASS | `chapters/src/007_book_i_07_earth_has_no_translational_motion.md` | `translation_status=NOT_TRANSLATED` |
| PAL marker 与 segmentation 一致 | PASS | `qa/pretranslation/007_book_i_07_source_extraction_check.md` | marker count `109` |
| PDF 页图范围已定位 | PASS_FOR_PREP | viewer pages `15-17` | 已生成 contact sheet；正式终稿前仍需逐页视觉复核 |
| 图表/表格风险 | PASS | source/PDF range | 本章无几何图形和正式表格 |
| 数值、角度、单位风险 | PASS | source/PDF range | 本章不含数学计算或六十进制值 |
| 主命题术语 | PASS_WITH_TRANSLATION_RULE | `κίνησιν ... μεταβατικήν` | 正文译作“平移运动/位置迁移”，注释说明区别于围绕轴的旋转 |
| 地心处所延续 | PASS_WITH_TRANSLATION_RULE | `τοῦ κατὰ τὸ κέντρον τόπου` | 与 Book I.5、I.6 的“中央/点的比例”论证连续处理 |
| 重物趋向中心 | PASS_WITH_TRANSLATION_RULE | `τὰ βάρη ... φέρεται`、`ἐπὶ τὸ κέντρον` | 按古代自然运动表达，不改写成现代万有引力 |
| 切平面/垂直关系 | PASS_WITH_TRANSLATION_RULE | `πρὸς ὁρθὰς γωνίας`、`ἐφαπτομένῳ ... ἐπιπέδῳ` | 可用现代几何中文说明“垂直于切平面”，但不得引入新证明 |
| 上下方向相对性 | PASS_WITH_TRANSLATION_RULE | `ἄνω`、`κάτω`、`περιέχουσαν ἐπιφάνειαν` | 说明“上”朝外、“下”向中心，是古代球形宇宙中的方向定义 |
| 地球静止论证 | PASS_WITH_TRANSLATION_RULE | `ἀτρεμοῦσα`、`μήτε βεβηκέναι ... μήτε φέρεσθαι` | 保留“静止/不被载动”的论证语气，不现代化 |
| 地球每日自转设想 | PASS_WITH_TRANSLATION_RULE | `περὶ τὸν αὐτὸν ἄξονα στρεφομένην ... ἀπὸ δυσμῶν ἐπʼ ἀνατολὰς` | 明确这是托勒密列举并反驳的设想，不得写成作者接受自转 |
| 空气与飞行/抛射现象 | PASS_WITH_TRANSLATION_RULE | `ἀέρα`、`ἱπταμένων`、`βαλλομένων` | 译文应清楚表达云、飞行物、抛射物没有表现出地球运动导致的滞后 |
| 古今概念边界 | PASS | technical audit | 不得引入现代惯性、参照系、角速度或真实地球自转知识来替代原论证 |
| 参考译本边界 | PASS | source-control rules | 英译本只作 witness，不作为底稿 |

## 译前术语控制

| Greek | Chinese working term | status | note |
|---|---|---|---|
| κίνησις μεταβατική | 平移运动 / 位置迁移 | PRELOCK_FOR_BOOK_I7 | 题名主术语；区别于 `στροφή` 旋转 |
| μεθίστασθαι | 离开原处 / 改换位置 | PRELOCK_FOR_BOOK_I7 | 指离开世界中心处所 |
| τὸ κατὰ τὸ κέντρον τόπος | 位于中心的处所 | PRELOCK_FOR_BOOK_I7 | 与 Book I.5 的地球居中命题连续 |
| φορά | 运动 / 载动 / 趋向运动 | PRELOCK_FOR_BOOK_I7 | 按上下文区分自然运动和整体运动，不统一硬译 |
| τὰ βάρη | 重物 / 有重量的物体 | PRELOCK_FOR_BOOK_I7 | 古代重轻自然学术语，不等同现代质量 |
| ἐφαπτομένον ἐπίπεδον | 切平面 | PRELOCK_FOR_BOOK_I7 | 可用现代几何术语帮助中文可读性 |
| ἄνω / κάτω | 上 / 下 | PRELOCK_FOR_BOOK_I7 | 本章需说明“上”朝宇宙外围、“下”向地心 |
| ὁμοιομερής | 同质 / 各部分同类 | PRELOCK_FOR_BOOK_I7 | 与 Book I.3 同质性术语保持一致 |
| ἀτρεμοῦσα | 静止着 / 不动 | PRELOCK_FOR_BOOK_I7 | 描述地球整体静止 |
| στροφή / περιστροφή | 旋转 / 回转一周 | PRELOCK_FOR_BOOK_I7 | 用于被反驳的地球每日自转设想 |
| ἄξων | 轴 / 天轴 | PRELOCK_FOR_BOOK_I7 | 与 Book I.5 术语统一 |
| ἀπὸ δυσμῶν ἐπʼ ἀνατολάς | 从西向东 | PRELOCK_FOR_BOOK_I7 | 地球自转设想的方向 |
| ἀήρ | 空气 | PRELOCK_FOR_BOOK_I7 | 不展开成现代大气层物理 |
| ἱπτάμενα / βαλλόμενα | 飞行物 / 抛射物 | PRELOCK_FOR_BOOK_I7 | 云、飞行物、抛射物现象链的一部分 |
| ὑπολείπεσθαι | 滞后 / 落在后面 | PRELOCK_FOR_BOOK_I7 | 反驳地球自转时的关键现象词 |

## 下一步

1. 若开始 Book I.7 翻译准备，先建立 `qa/chapter_controls/007_book_i_07_earth_has_no_translational_motion.control.md`。
2. 翻译时必须保留“地球居中与重物趋心 → 上下方向相对定义 → 地球若整体运动将荒谬 → 自转设想与空气现象反驳”的证明链。
3. 翻译后需要忠实度、中文可读性、术语一致性、古代自然学边界和天文学模型边界审校。
