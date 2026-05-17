# Book I.8 技术审计 / Technical Audit

chapter_id: `008_book_i_08_two_primary_motions`
audit_status: `PASS_FOR_TRANSLATION_PREP__NOT_TRANSLATED`

## 输入

- 原文章节：`chapters/src/008_book_i_08_two_primary_motions.md`
- source extraction 检查：`qa/pretranslation/008_book_i_08_source_extraction_check.md`
- PDF 页图证据：`qa/technical/page_screenshots/book_i08_pages_017_019_contact_sheet.jpg`
- 分章矩阵：`source/book_i_segmentation.md`
- 术语表：`qa/technical/mathematical_term_lock.md`
- 参考边界：`metadata/source_witness_manifest.md`、`metadata/reference_witness_policy.md`

## 控制结论

- 本章论证天上最初运动有两类：第一运动带动全天自东向西绕赤道极旋转；第二运动使日、月、行星沿相对于赤道倾斜的大圈作相反方向的迁移。
- 本章无几何图形、无正式表格、无六十进制数值；风险集中在球面天文学术语、方向关系、黄道与赤道的几何关系，以及古代模型边界。
- 允许进入 Book I.8 章节控制准备；仍不允许直接写 `chapters/final/`，不允许生成正式 EPUB。
- 英译本只能作 reference witness；不得把本章改写成现代天体物理、公转轨道力学、地球真实自转或现代黄赤交角说明。

## 审计项

| 项目 | PASS/FAIL | 证据位置 | 问题与处理 |
|---|---|---|---|
| source 文件存在且未翻译 | PASS | `chapters/src/008_book_i_08_two_primary_motions.md` | `translation_status=NOT_TRANSLATED` |
| PAL marker 与 segmentation 一致 | PASS | `qa/pretranslation/008_book_i_08_source_extraction_check.md` | marker count `109` |
| PDF 页图范围已定位 | PASS_FOR_PREP | viewer pages `17-19` | 已生成 contact sheet；正式终稿前仍需逐页视觉复核 |
| 图表/表格风险 | PASS | source/PDF range | 本章无几何图形和正式表格 |
| 数值、角度、单位风险 | PASS | source/PDF range | 本章不含数学计算或六十进制值 |
| 第一运动 | PASS_WITH_TRANSLATION_RULE | `μία μὲν ... ἀπὸ ἀνατολῶν ἐπὶ δυσμὰς` | 译为“第一运动/第一载动”，说明其为全天日周运动，不现代化为地球自转 |
| 第二运动 | PASS_WITH_TRANSLATION_RULE | `ἡ δὲ ἑτέρα ... περὶ πόλους ἑτέρους` | 译为“第二运动/第二类运动”，保持与第一运动相反、绕另一些极的结构 |
| 赤道圈 | PASS_WITH_TRANSLATION_RULE | `ἰσημερινὸς` | 正文优先“赤道圈”，注释说明原意关联昼夜平分 |
| 黄道斜圈 | PASS_WITH_TRANSLATION_RULE | `κύκλος λοξὸς πρὸς τὸν ἰσημερινὸν` | 可译“黄道斜圈/相对于赤道倾斜的大圈”；不得写成现代轨道平面力学 |
| 子午圈 | PASS_WITH_TRANSLATION_RULE | `μεσημβρινός` | 译为“子午圈”，说明不同于“通过两组极的大圈” |
| 日月五星 | PASS_WITH_TRANSLATION_RULE | `ἥλιος`、`σελήνη`、`πλανώμενοι ἀστέρες` | 保留古代行星体系语境；不得改写为现代太阳系行星清单 |
| 二分点 | PASS_WITH_TRANSLATION_RULE | `ἰσημερινά`、`ἐαρινόν`、`μετοπωρινόν` | 译为“二分点/春分点/秋分点”，注释说明原文按黄道与赤道交点定义 |
| 二至点 | PASS_WITH_TRANSLATION_RULE | `τροπικά`、`χειμερινόν`、`θερινόν` | 译为“二至点/冬至点/夏至点”，注释说明按通过两组极的大圈与黄道交点定义 |
| 方向关系 | PASS_WITH_TRANSLATION_RULE | `ἀνατολαί`、`δυσμαί`、`ἄρκτοι`、`μεσημβρία` | 译文需区分“升起/东方”“落下/西方”“北方”“南方/正午方位” |
| 古今概念边界 | PASS | technical audit | 不得引入现代天体动力学、真实地球自转或现代黄赤交角数值 |
| 参考译本边界 | PASS | source-control rules | 英译本只作 witness，不作为底稿 |

## 译前术语控制

| Greek | Chinese working term | status | note |
|---|---|---|---|
| πρῶται κινήσεις | 最初运动 / 基本运动 | PRELOCK_FOR_BOOK_I8 | 题名主术语；指天球运动的基本类别 |
| πρώτη φορά / πρώτη περιαγωγή | 第一运动 / 第一载动 / 第一回转 | PRELOCK_FOR_BOOK_I8 | 全天自东向西的日周运动 |
| δευτέρα φορά / δευτέρα διαφορά | 第二运动 / 第二类运动 | PRELOCK_FOR_BOOK_I8 | 与第一运动相反，绕黄道斜圈的极 |
| ἰσημερινός | 赤道圈 / 昼夜平分圈 | PRELOCK_FOR_BOOK_I8 | 正文用“赤道圈”，注释解释昼夜平分语源 |
| ὁρίζων | 地平圈 | PRELOCK_FOR_BOOK_I8 | 本章以大圈二分赤道圈为核心 |
| λοξὸς κύκλος | 黄道斜圈 / 相对于赤道倾斜的大圈 | PRELOCK_FOR_BOOK_I8 | 与 Book I.2 的黄道相关术语保持一致 |
| πλανώμενοι ἀστέρες | 行星 / 游移星 | PRELOCK_FOR_BOOK_I8 | 古代“游移的星”，正文可用“行星” |
| ἀπλανεῖς / λοιπὰ ἄστρα | 恒星 / 其余星体 | PRELOCK_FOR_BOOK_I8 | 与行星区别 |
| μεσουράνησις | 中天 | PRELOCK_FOR_BOOK_I8 | 每日升起、中天、落下现象链 |
| μεσημβρινός | 子午圈 | PRELOCK_FOR_BOOK_I8 | 需说明其与通过赤道极和黄道极的大圈不同 |
| ἰσημερινά | 二分点 | PRELOCK_FOR_BOOK_I8 | 黄道与赤道圈的两个交点 |
| ἐαρινόν / μετοπωρινόν | 春分点 / 秋分点 | PRELOCK_FOR_BOOK_I8 | 以太阳沿黄道由南向北或由北向南通过赤道为准 |
| τροπικά | 二至点 | PRELOCK_FOR_BOOK_I8 | 黄道与通过两组极的大圈的两个交点 |
| χειμερινόν / θερινόν | 冬至点 / 夏至点 | PRELOCK_FOR_BOOK_I8 | 按相对赤道的南北极限命名 |
| πρὸς ἄρκτους / πρὸς μεσημβρίαν | 向北 / 向南 | PRELOCK_FOR_BOOK_I8 | 方向术语，不按字面硬译为“大熊/正午” |

## 下一步

1. 若开始 Book I.8 翻译准备，先建立 `qa/chapter_controls/008_book_i_08_two_primary_motions.control.md`。
2. 翻译时必须保留“第一运动日周带动 → 行星相对恒星向东滞后并南北偏移 → 需设黄道斜圈第二运动 → 定义二分点、二至点、子午圈和两类运动关系”的证明链。
3. 翻译后需要忠实度、中文可读性、术语一致性、球面天文学证明链和古今概念边界审校。
