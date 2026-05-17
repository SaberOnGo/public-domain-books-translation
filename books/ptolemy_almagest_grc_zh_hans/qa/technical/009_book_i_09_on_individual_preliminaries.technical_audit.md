# Book I.9 技术审计 / Technical Audit

chapter_id: `009_book_i_09_on_individual_preliminaries`
audit_status: `PASS_FOR_TRANSLATION_PREP__NOT_TRANSLATED`

## 输入

- 原文章节：`chapters/src/009_book_i_09_on_individual_preliminaries.md`
- source extraction 检查：`qa/pretranslation/009_book_i_09_source_extraction_check.md`
- PDF 页图证据：`qa/technical/page_screenshots/book_i09_page_019_contact_sheet.jpg`
- 分章矩阵：`source/book_i_segmentation.md`
- 术语表：`qa/technical/mathematical_term_lock.md`
- 参考边界：`metadata/source_witness_manifest.md`、`metadata/reference_witness_policy.md`

## 控制结论

- 本章是从 Book I.1-I.8 的总括预设，转入 Book I.10 几何弦论的过渡章。
- 本章无几何图形、无表格、无六十进制数值；风险集中在“具体测定”“逐项证明”“前述两极之间的弧”“圆内直线大小”和“几何证明”的术语衔接。
- 允许进入 Book I.9 章节控制准备；仍不允许直接写 `chapters/final/`，不允许生成正式 EPUB。
- 英译本只能作 reference witness；不得把本章简化成现代章节目录说明，也不得提前翻译 Book I.10 的证明内容。

## 审计项

| 项目 | PASS/FAIL | 证据位置 | 问题与处理 |
|---|---|---|---|
| source 文件存在且未翻译 | PASS | `chapters/src/009_book_i_09_on_individual_preliminaries.md` | `translation_status=NOT_TRANSLATED` |
| PAL marker 与 segmentation 一致 | PASS | `qa/pretranslation/009_book_i_09_source_extraction_check.md` | marker count `11` |
| PDF 页图范围已定位 | PASS_FOR_PREP | viewer page `19` | 已生成 contact sheet；正式终稿前仍需逐页视觉复核 |
| 图表/表格风险 | PASS | source/PDF range | 本章无几何图形和正式表格 |
| 数值、角度、单位风险 | PASS | source/PDF range | 本章不含数学计算或六十进制值 |
| 过渡章功能 | PASS_WITH_TRANSLATION_RULE | `μέλλοντες δὲ ἄρχεσθαι` | 译文须说明这是进入逐项证明前的安排 |
| 具体测定 | PASS_WITH_TRANSLATION_RULE | `κατὰ μέρος καταλήψεις` | 译为“各项具体测定/逐项测定”，不硬译成“把握” |
| 前述两极之间的弧 | PASS_WITH_TRANSLATION_RULE | `μεταξύ τῶν προειρημένων πόλων περιφέρεια` | 与 I.8 的赤道极/黄道极关系相衔接 |
| 圆内直线大小 | PASS_WITH_TRANSLATION_RULE | `πηλικότητος τῶν ἐν τῷ κύκλῳ εὐθειῶν` | 指 I.10 的圆内直线/弦长理论；不得提前展开弦表 |
| 几何证明 | PASS_WITH_TRANSLATION_RULE | `γραμμικῶς ἀποδεικνύειν` | 译为“用几何线图方式证明/按几何作图证明” |
| 参考译本边界 | PASS | source-control rules | 英译本只作 witness，不作为底稿 |

## 译前术语控制

| Greek | Chinese working term | status | note |
|---|---|---|---|
| κατὰ μέρος καταλήψεις | 各项具体测定 / 逐项测定 | PRELOCK_FOR_BOOK_I9 | 题名主术语；连接后续各项证明 |
| ὁλοσχερὴς προδιάληψις | 总括性的预先说明 | PRELOCK_FOR_BOOK_I9 | 回指 I.1-I.8 的总论 |
| κατὰ μέρος ἀποδείξεις | 逐项证明 / 各项具体证明 | PRELOCK_FOR_BOOK_I9 | 进入后续数学证明 |
| προειρημένοι πόλοι | 前述两极 | PRELOCK_FOR_BOOK_I9 | 回指 I.8 的两组极关系 |
| περιφέρεια | 弧 / 圆周弧 | PRELOCK_FOR_BOOK_I9 | 与 I.10 弧/弦术语保持一致 |
| διʼ αὐτῶν γραφόμενος μέγιστος κύκλος | 通过这些极画出的大圈 | PRELOCK_FOR_BOOK_I9 | 连接 I.8 的大圈结构 |
| πηλικότης τῶν ἐν τῷ κύκλῳ εὐθειῶν | 圆内直线的大小 / 弦长问题 | PRELOCK_FOR_BOOK_I9 | 正文可说“圆内直线的大小”，注释说明即后续弦长理论 |
| γραμμικῶς ἀποδεικνύειν | 按几何线图证明 / 用几何方法证明 | PRELOCK_FOR_BOOK_I9 | 不改写成代数推导 |

## 下一步

1. 若开始 Book I.9 翻译准备，先建立 `qa/chapter_controls/009_book_i_09_on_individual_preliminaries.control.md`。
2. 翻译时必须保留“总括预设已经列明 → 即将进入逐项证明 → 第一项需要测定前述两极间大圈弧的大小 → 因而先讲圆内直线大小”的过渡链。
3. 翻译后需要忠实度、中文可读性、术语一致性、Book I.8-I.10 衔接和古今概念边界审校。
