# Book I.1 技术审计 / Technical Audit

chapter_id: `001_book_i_01_proem`
audit_status: `PASS_FOR_TRANSLATION_PREP__NOT_TRANSLATED`

## 输入

- 原文章节：`chapters/src/001_book_i_01_proem.md`
- source extraction 检查：`qa/pretranslation/001_book_i_01_source_extraction_check.md`
- PDF 页图证据：`qa/technical/page_screenshots/book_i01_pages_006_008_contact_sheet.jpg`
- 分章矩阵：`source/book_i_segmentation.md`
- 术语表：`qa/technical/mathematical_term_lock.md`
- 专名规则：`references/ancient_greek_names_transliteration_policy.md`

## 控制结论

- 本章是哲学性序言和学科定位章节，不含几何图、数值表或天文模型计算。
- 关键风险不是表格/数值，而是古代学科分类、亚里士多德式术语、献辞对象和“数学/天文学”关系的概念边界。
- 允许进入 Book I.1 受控翻译准备；仍不允许写 `chapters/final/`，不允许生成正式 EPUB。
- 英译本只能作 reference witness；不得把英译的现代哲学术语直接作为中文底稿。

## 审计项

| 项目 | PASS/FAIL | 证据位置 | 问题与处理 |
|---|---|---|---|
| source 文件存在且未翻译 | PASS | `chapters/src/001_book_i_01_proem.md` | `translation_status=NOT_TRANSLATED` |
| PAL marker 与 segmentation 一致 | PASS | `qa/pretranslation/001_book_i_01_source_extraction_check.md` | marker count `105` |
| PDF 页图范围已定位 | PASS_FOR_PREP | viewer pages `6`-`8` | 已生成 contact sheet；正式译前仍建议逐页视觉复核 |
| 图表/表格风险 | PASS | source/PDF range | 本章无图表、无数值表 |
| 数值、角度、单位风险 | PASS | source/PDF range | 本章不含数学计算或六十进制值 |
| 古代学科分类边界 | PASS_WITH_TRANSLATION_RULE | `θεωρητικόν`, `πρακτικόν`, `φυσικόν`, `μαθηματικόν`, `θεολογικόν` | 不得套用现代大学学科分类；需按古代哲学分类解释 |
| 数学与天文学关系 | PASS_WITH_TRANSLATION_RULE | `μαθηματικά`, `θεῖα καὶ οὐράνια` | “数学”包含天文理论的基础语境；不可改写成现代物理学或现代天文学导论 |
| 专名/称呼 | PASS_WITH_TRANSLATION_RULE | `ὦ Σύρε` | 译名前需按本书专名规则记录；正文可保留稳定译名并在注释说明 |
| 参考译本边界 | PASS | source-control rules | 英译本只作 witness，不作为底稿 |

## 译前术语控制

| Greek | Chinese working term | status | note |
|---|---|---|---|
| θεωρητικόν | 理论部分 / 理论的 | PRELOCK_FOR_BOOK_I1 | 与 `πρακτικόν` 对举，避免译成现代“理论科学”而失去古代哲学分类语境 |
| πρακτικόν | 实践部分 / 实践的 | PRELOCK_FOR_BOOK_I1 | 指行动/伦理相关领域，不等同现代“应用科学” |
| φυσικόν | 自然学 | PRELOCK_FOR_BOOK_I1 | 古代 physics/nature study；不可直接现代化为“物理学” |
| μαθηματικόν / μαθηματικά | 数学 / 数学诸学 | PRELOCK_FOR_BOOK_I1 | 在本书中通向天文学理论，不限现代狭义数学 |
| θεολογικόν | 神学性研究 / 神学部分 | PRELOCK_FOR_BOOK_I1 | 亚里士多德式理论哲学分类，不作宗教教义化处理 |
| οὐράνια | 天体 / 天上事物 | PRELOCK_FOR_BOOK_I1 | 结合本书天文学语境处理 |

## 下一步

1. 若开始翻译 Book I.1，先建立 `qa/chapter_controls/001_book_i_01_proem.control.md`。
2. 翻译时必须保留古代学科分类链条，不把序言改写成现代科学史综述。
3. 翻译后需要忠实度、中文可读性、术语一致性和概念边界审校。
