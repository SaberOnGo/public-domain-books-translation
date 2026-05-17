# 《Almagest》Book I 预研究与执行总纲

plan_status: `BOOK_I_TRANSLATION_SCOPE_STARTED__FINAL_GATED`
created_at: `2026-05-17`

## 2026-05-17 范围修订

用户已明确收窄本轮范围：只完成 Book I，不完成 13 卷全书。既有全书目录、全书风险图和跨卷术语/模型材料保留为背景参考；本轮执行、EPUB、随机抽检和退出条件均只覆盖 Book I 的 16 章。

## 目标

在正式推进 Book I 终稿前，把 Book I 从“Book I.10 试译样本可行”推进到“Book I source split、术语、图表/表格、数值和技术 QA 路线清楚”。本文件是 Book I 阶段的预研究执行总纲，不是译文。

## 已确认事实

- Heiberg PDF 扫描已保存并哈希记录，是主底本影像。
- PAL Heiberg 古希腊文转写 XML 已保存并记录许可，是辅助古希腊转写和 source split 控制来源。
- 英译本只能作 reference witness。
- Book I.10 已完成试译、评审、facsimile 图样书和样书 EPUB。
- PAL 目录已抽取为 `source/full_toc_draft.json` 和 `source/full_book_translation_outline.md`。
- PAL 目录草案显示全书 `13` 卷、`146` 章；本轮只执行 Book I 的 `16` 章。
- 全书风险图已生成到 `qa/pretranslation/full_book_risk_map.md` 和 `.json`，作为后续章节 QA 路由草案。
- 全书预翻译门禁已生成到 `qa/pretranslation/full_book_pretranslation_gate.md` 和 `.json`，并接入 `quality:all`。
- Book I.11 弦表结构化策略已生成到 `qa/technical/011_book_i_11_chord_table_strategy.md`，并由 `qa/pretranslation/011_book_i_11_table_strategy_check.md` 检查。
- Book I.1、I.2、I.3、I.4、I.5、I.6 和 I.7 已通过章节质量门禁；下一步是终稿前 Book I 一致性审校，不得直接终稿。
- Book I 的 PAL 分章边界已生成到 `source/book_i_segmentation.md` 和 `source/book_i_segmentation.json`，共 `16` 章；PDF 页图核验仍未完成，因此还不是正式 source split PASS。
- Book I 页图抽样已生成接触表，覆盖 PDF viewer pages `4`-`50`，包括 Book I 目录、I.10、I.11 弦表、I.15/I.16 和 Book II 边界；见 `qa/technical/book_i_page_verification.md`。
- Book I source split 就绪矩阵已生成到 `qa/pretranslation/book_i_source_split_readiness.md` 和 `.json`：16 章中只有 I.10 达到 `READY_FOR_FORMAL_RECHECK_NOT_FINAL`，其余章节仍为 source extraction pending。

## 尚未允许直接批量翻译的原因

- 全书正式 `chapters/src/*.md` 尚未生成。
- PDF 页图范围尚未逐卷抽样核验。
- Book I 以外的图表、表格、星表、数值表和模型风险尚未建立完整清单。
- 术语目前仍是 Book I.10 pilot 层级，未达到全书 `LOCKED_WITH_SCOPE`。
- 弦表、星表、行星模型、月球/太阳模型、食限、视差等高风险内容尚未有逐章 QA 路由。
- `qa/pretranslation/pretranslation_report.md` 仍需升级为全书 PASS 报告后，才能启动正式批量章节翻译。

## 第一轮预研究任务

1. 从 `source/full_toc_draft.json` 生成逐卷分章计划。Book I 已完成 PAL 边界识别。
2. 为每卷建立或更新 `source/book_{roman}_segmentation.md`。Book I 已完成，Book II-XIII 待执行。
3. 对每章标记风险类型：基础几何、天球几何、数值表、星表、行星模型、仪器、观测、文字论述。
4. 抽样核对 Heiberg PDF 页图，确认每卷起止、重要图表页、表格页和边界页。
5. 把 `qa/technical/diagram_table_inventory.md` 从 Book I 草案扩展为全书清单。
6. 把 `qa/technical/mathematical_term_lock.md` 从 Book I.10 pilot 升级为全书作用域术语锁定。
7. 建立弦表、星表、黄道/赤道表、行星模型表、食限表、视差表的结构化表格策略。
8. 复核 `metadata/rights_checklist.md` 中 Heiberg PDF 精确版本和 Wikimedia hash 差异，确认正式翻译的权利证据状态。
9. 更新 `qa/pretranslation/pretranslation_report.md`。只有它明确全书预研究 PASS，才进入 `prompts/07_translate_chapters_zh_grc.md`。

## 翻译阶段路线

每章必须按固定路线推进：

1. `chapters/src/{chapter}.md`
2. `chapters/translated/{chapter}.md`
3. `qa/chapter_controls/{chapter}.control.md`
4. `qa/technical/{chapter}.technical_audit.md`
5. `qa/technical/{chapter}.diagram_table_audit.md`
6. `reviews/` 中必要评审记录
7. `chapters/final/{chapter}.md`

任何涉及数学、天文学、表格、图表、数值、模型或古今概念边界的章节，未通过技术审计不得进入 `chapters/final/`。

## 第一轮执行顺序

1. 完成全书 TOC 草案和风险分级。
2. 完成 Book I 正式分章，因为 Book I 包含后续全书术语和弦表基础。
3. 优先处理 Book I.11 弦表的结构化表格策略，但不得在 source split 和数值策略未通过前翻译。
4. 完成 Book II 的天球/地理/黄道关系分章和图表风险识别。
5. 再进入太阳、月球、食、恒星、行星各大模块。

## 退出本预研究阶段的 PASS 条件

- `source/full_toc_draft.json` 可解析。
- 每卷分章计划存在或明确排队。
- 全书高风险章节已分类。
- PDF 页图抽样策略明确。
- 术语、图表/表格、数值和技术审计路线明确。
- `qa/pretranslation/pretranslation_report.md` 不再只描述 Book I.10 试译，而是记录全书预研究是否 PASS。

当前状态：`STARTED`。

## 2026-05-17 进展

- 已新增 `scripts/extract_pal_book_segmentation.py`。
- 已新增 npm 脚本 `source:book-i`。
- 已生成 `source/book_i_segmentation.json`。
- 已重写 `source/book_i_segmentation.md` 为 PAL 边界控制表。
- Book I.11 和 I.15 被标记为 `TABLE_NUMERIC_HIGH`，进入正式翻译前必须先做结构化表格和数值校验策略。
- 下一步：对 Book I 执行 PDF 页图抽样，确认每章 viewer page 起止、I.11 弦表起止页、I.15 黄道倾角表/数值页和 Book II 边界页。

## 2026-05-17 Book I PDF 抽样进展

- 已新增 `scripts/render_pdf_contact_sheet.py`。
- 已生成：
  - `qa/technical/page_screenshots/book_i_pages_004_018_contact_sheet.jpg`
  - `qa/technical/page_screenshots/book_i_pages_019_029_contact_sheet.jpg`
  - `qa/technical/page_screenshots/book_i_pages_030_047_contact_sheet.jpg`
  - `qa/technical/page_screenshots/book_i_pages_048_050_boundary_contact_sheet.jpg`
- `qa/technical/book_i_page_verification.md` 已记录 Book I 页图抽样和工作页码公式。
- 下一步仍不是翻译，而是把 Book I 的 `PENDING_PDF_PAGE_VERIFICATION` 逐章关闭，并决定哪些章节可以生成正式 `chapters/src/*.md`。

## 2026-05-17 Book I source split 就绪矩阵

- 已新增 `scripts/build_book_i_readiness_matrix.py`。
- 已新增 npm 脚本 `source:book-i-readiness`。
- 已生成：
  - `qa/pretranslation/book_i_source_split_readiness.json`
  - `qa/pretranslation/book_i_source_split_readiness.md`
- 矩阵结论：当前没有任何章节可直接进入 `chapters/final/` 或批量翻译；I.10 仅可进入 formal recheck；I.11 和 I.15 必须先完成结构化表格与数值校验策略。

## 2026-05-17 PDF 抽样状态升级

- `source/book_i_segmentation.md` 已从笼统 `PENDING_PDF_PAGE_VERIFICATION` 升级为 `PASS_FOR_BOOK_I_PRE_RESEARCH_SAMPLE__FORMAL_RECHECK_REQUIRED`。
- 这只表示 Book I 已有预研究页图抽样证据，不代表章节级正式 source extraction 已通过。
- `qa/pretranslation/book_i_source_split_readiness.md` 已同步 blockers：每章仍需把预研究 PDF 抽样升级为正式章节证据。

## 2026-05-17 Book I.10 formal source recheck

- 已新增 `scripts/check_book_i10_formal_source_recheck.py`。
- 已新增 npm 脚本 `source:i10-formal-recheck`。
- 已生成：
  - `qa/pretranslation/010_book_i_10_formal_source_recheck.json`
  - `qa/pretranslation/010_book_i_10_formal_source_recheck.md`
- Book I.10 recheck 结论为 `PASS_FOR_FORMAL_SOURCE_RECHECK__NOT_FINAL_GATE`。
- `qa/pretranslation/book_i_source_split_readiness.md` 已改为读取该 recheck JSON：Book I.10 现在记录为 `FORMAL_SOURCE_RECHECK_PASS__CHAPTER_TRANSLATION_STILL_GATED`。
- 这仍不允许写 `chapters/final/`，不允许生成正式 `output/book.epub`，也不允许把 Book I.10 的 trial 译文直接当成终稿。

## 2026-05-17 全书风险图

- 已新增 `scripts/build_full_book_risk_map.py`。
- 已新增 npm 脚本 `source:risk-map` 和 `source:full-prep`。
- 已生成：
  - `qa/pretranslation/full_book_risk_map.json`
  - `qa/pretranslation/full_book_risk_map.md`
- 当前风险统计：`FOUNDATION_GEOMETRY_HIGH=26`，`MODEL_NUMERIC_HIGH=95`，`STAR_CATALOG_HIGH=9`，`TABLE_NUMERIC_HIGH=16`。
- 风险图明确三类来源分工：Heiberg PDF 是正式切分主影像依据，PAL Greek XML 是古希腊辅助转写，英译本只作 reference witness。
- 风险图只是全书预研究 QA 路由，不替代 PDF 页图核验、正式 `chapters/src`、章节控制或技术审计。

## 2026-05-17 全书预翻译门禁

- 已新增 `scripts/check_full_book_pretranslation_gate.py`。
- 已新增 npm 脚本 `quality:pretranslation-gate`，并将其接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/full_book_pretranslation_gate.json`
  - `qa/pretranslation/full_book_pretranslation_gate.md`
- 当前门禁结论为 `PASS_PRE_RESEARCH_ACTIVE__FORMAL_TRANSLATION_GATED`。
- 该门禁允许继续预研究和 source split 准备，但在 `formal_translation_allowed=false` 时检查并阻止 `chapters/final/*.md` 与正式 `output/book.epub`。

## 2026-05-17 Book I.11 弦表策略

- 已确认 PAL XML 在 Book I.11 到 I.12 之间只保留题名和页标：`I_48` 到 `I_63`，没有表格行列转写。
- 已生成 Book I.11 弦表页图接触表：`qa/technical/page_screenshots/book_i11_chord_table_pages_028_035_contact_sheet.jpg`。
- 已新增 `qa/technical/011_book_i_11_chord_table_strategy.md`。
- 已新增 `scripts/check_book_i11_table_strategy.py`。
- 已新增 npm 脚本 `source:i11-table-strategy` 和 `quality:i11-table-strategy`，并将后者接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/011_book_i_11_table_strategy_check.json`
  - `qa/pretranslation/011_book_i_11_table_strategy_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.11 为 `TABLE_STRATEGY_PASS__SOURCE_EXTRACTION_PENDING`。
- 下一步是逐页/逐行 raw table source extraction 和数值校验；仍不得直接翻译 Book I.11。

## 2026-05-17 Book I.1 source extraction candidate

- 已新增通用 PAL 章节 source extractor：`scripts/extract_pal_chapter_source.py`。
- 已新增 source extraction 检查脚本：`scripts/check_chapter_source_extraction.py`。
- 已新增 npm 脚本：
  - `source:i1-extract`
  - `quality:i1-source`
- 已将 `quality:i1-source` 接入 `quality:all`。
- 已生成：
  - `chapters/src/001_book_i_01_proem.md`
  - `qa/pretranslation/001_book_i_01_source_extraction_check.json`
  - `qa/pretranslation/001_book_i_01_source_extraction_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.1 为 `SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING`。
- 这只是 source extraction candidate；Book I.1 仍需 formal PDF recheck、章节控制和技术审计后，才可进入翻译。

## 2026-05-17 Book I.1 formal source recheck

- 已生成 Book I.1 PDF 页图证据：`qa/technical/page_screenshots/book_i01_pages_006_008_contact_sheet.jpg`。
- 已新增 Book I.1 技术审计：`qa/technical/001_book_i_01_proem.technical_audit.md`。
- 已更新 `qa/technical/mathematical_term_lock.md`，加入 Book I.1 学科分类术语预锁。
- 已新增 `scripts/check_book_i1_formal_source_recheck.py`。
- 已新增 npm 脚本：
  - `source:i1-formal-recheck`
  - `quality:i1-formal-recheck`
- 已将 `quality:i1-formal-recheck` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/001_book_i_01_formal_source_recheck.json`
  - `qa/pretranslation/001_book_i_01_formal_source_recheck.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.1 为 `FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING`。
- 下一步只能先创建章节控制文件；不得直接进入终稿或正式 EPUB。

## 2026-05-17 Book I.1 chapter control

- 已新增章节控制文件：`qa/chapter_controls/001_book_i_01_proem.control.md`。
- 已新增章节控制检查脚本：`scripts/check_book_i1_chapter_control.py`。
- 已新增 npm 脚本：
  - `source:i1-control`
  - `quality:i1-control`
- 已将 `quality:i1-control` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/001_book_i_01_chapter_control_check.json`
  - `qa/pretranslation/001_book_i_01_chapter_control_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.1 为 `CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED`。
- 下一步只允许写受控译文 `chapters/translated/001_book_i_01_proem.md`；译后仍需复核、审校和质量门禁，不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.1 controlled translation draft

- 已新增受控译文草稿：`chapters/translated/001_book_i_01_proem.md`。
- 已新增译文检查脚本：`scripts/check_book_i1_translation.py`。
- 已新增 npm 脚本：
  - `source:i1-translation-check`
  - `quality:i1-translation`
- 已将 `quality:i1-translation` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/001_book_i_01_translation_check.json`
  - `qa/pretranslation/001_book_i_01_translation_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.1 为 `TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING`。
- 下一步必须进行忠实度、可读性、术语一致性、概念边界和技术复核；不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.1 draft review

- 已新增评审记录：`reviews/chapters/001_book_i_01_proem.review.md`。
- 已新增评审检查脚本：`scripts/check_book_i1_review.py`。
- 已新增 npm 脚本：
  - `source:i1-review`
  - `quality:i1-review`
- 已将 `quality:i1-review` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/001_book_i_01_review_check.json`
  - `qa/pretranslation/001_book_i_01_review_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.1 为 `REVIEW_PASS__TECHNICAL_RECHECK_PENDING`。
- 下一步必须进行译后技术复核；不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.1 post-translation technical recheck

- 已新增译后技术复核记录：`qa/technical/001_book_i_01_proem.post_translation_technical_recheck.md`。
- 已新增译后技术复核检查脚本：`scripts/check_book_i1_post_translation_technical_recheck.py`。
- 已新增 npm 脚本：
  - `source:i1-post-technical-recheck`
  - `quality:i1-post-technical-recheck`
- 已将 `quality:i1-post-technical-recheck` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/001_book_i_01_post_translation_technical_recheck.json`
  - `qa/pretranslation/001_book_i_01_post_translation_technical_recheck.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.1 为 `TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING`。
- 下一步必须建立章节质量门禁，聚合 source、formal recheck、chapter control、translation、review 和技术复核结果；不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.1 chapter quality gate

- 已新增章节质量门禁记录：`qa/chapter_controls/001_book_i_01_proem.quality_gate.md`。
- 已新增章节质量门禁检查脚本：`scripts/check_book_i1_chapter_quality_gate.py`。
- 已新增 npm 脚本：
  - `source:i1-chapter-gate`
  - `quality:i1-chapter-gate`
- 已将 `quality:i1-chapter-gate` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/001_book_i_01_chapter_quality_gate.json`
  - `qa/pretranslation/001_book_i_01_chapter_quality_gate.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.1 为 `CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING`。
- 这只表示 Book I.1 可以排队进入终稿前全书一致性审校；在全书预研究 PASS 前，仍不得写 `chapters/final/` 或正式 `output/book.epub`。

## 2026-05-17 Book I.2 source extraction candidate

- 已扩展通用 PAL 章节 source extractor：`scripts/extract_pal_chapter_source.py` 支持 `I.2`。
- 已扩展 source extraction 检查脚本：`scripts/check_chapter_source_extraction.py` 支持 `I.2`。
- 已新增 npm 脚本：
  - `source:i2-extract`
  - `source:i2-check`
  - `quality:i2-source`
- 已将 `quality:i2-source` 接入 `quality:all`。
- 已生成：
  - `chapters/src/002_book_i_02_order_of_the_theorems.md`
  - `qa/pretranslation/002_book_i_02_source_extraction_check.json`
  - `qa/pretranslation/002_book_i_02_source_extraction_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.2 为 `SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING`。
- 这只是 source extraction candidate；Book I.2 仍需 formal PDF recheck、章节控制和技术审计后，才可进入翻译。

## 2026-05-17 Book I.2 formal source recheck

- 已生成 Book I.2 PDF 页图证据：`qa/technical/page_screenshots/book_i02_pages_008_009_contact_sheet.jpg`。
- 已新增 Book I.2 技术审计：`qa/technical/002_book_i_02_order_of_the_theorems.technical_audit.md`。
- 已更新 `qa/technical/mathematical_term_lock.md`，加入 Book I.2 全书次序与天文学对象术语预锁。
- 已新增 `scripts/check_book_i2_formal_source_recheck.py`。
- 已新增 npm 脚本：
  - `source:i2-formal-recheck`
  - `quality:i2-formal-recheck`
- 已将 `quality:i2-formal-recheck` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/002_book_i_02_formal_source_recheck.json`
  - `qa/pretranslation/002_book_i_02_formal_source_recheck.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.2 为 `FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING`。
- 下一步只能先创建章节控制文件；不得直接翻译、不得进终稿或正式 EPUB。

## 2026-05-17 Book I.2 chapter control

- 已新增章节控制文件：`qa/chapter_controls/002_book_i_02_order_of_the_theorems.control.md`。
- 已新增章节控制检查脚本：`scripts/check_book_i2_chapter_control.py`。
- 已新增 npm 脚本：
  - `source:i2-control`
  - `quality:i2-control`
- 已将 `quality:i2-control` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/002_book_i_02_chapter_control_check.json`
  - `qa/pretranslation/002_book_i_02_chapter_control_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.2 为 `CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED`。
- 下一步只允许写受控译文 `chapters/translated/002_book_i_02_order_of_the_theorems.md`；译后仍需复核、审校和质量门禁，不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.2 controlled translation draft

- 已新增受控译文草稿：`chapters/translated/002_book_i_02_order_of_the_theorems.md`。
- 已新增译文检查脚本：`scripts/check_book_i2_translation.py`。
- 已新增 npm 脚本：
  - `source:i2-translation-check`
  - `quality:i2-translation`
- 已将 `quality:i2-translation` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/002_book_i_02_translation_check.json`
  - `qa/pretranslation/002_book_i_02_translation_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.2 为 `TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING`。
- 下一步必须进行忠实度、可读性、术语一致性、概念边界和技术复核；不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.2 draft review

- 已新增评审记录：`reviews/chapters/002_book_i_02_order_of_the_theorems.review.md`。
- 已新增评审检查脚本：`scripts/check_book_i2_review.py`。
- 已新增 npm 脚本：
  - `source:i2-review`
  - `quality:i2-review`
- 已将 `quality:i2-review` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/002_book_i_02_review_check.json`
  - `qa/pretranslation/002_book_i_02_review_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.2 为 `REVIEW_PASS__TECHNICAL_RECHECK_PENDING`。
- 下一步必须进行译后技术复核；不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.2 post-translation technical recheck

- 已新增译后技术复核记录：`qa/technical/002_book_i_02_order_of_the_theorems.post_translation_technical_recheck.md`。
- 已新增译后技术复核检查脚本：`scripts/check_book_i2_post_translation_technical_recheck.py`。
- 已新增 npm 脚本：
  - `source:i2-post-technical-recheck`
  - `quality:i2-post-technical-recheck`
- 已将 `quality:i2-post-technical-recheck` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/002_book_i_02_post_translation_technical_recheck.json`
  - `qa/pretranslation/002_book_i_02_post_translation_technical_recheck.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.2 为 `TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING`。
- 下一步必须建立章节质量门禁，聚合 source、formal recheck、chapter control、translation、review 和技术复核结果；不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.2 chapter quality gate

- 已新增章节质量门禁记录：`qa/chapter_controls/002_book_i_02_order_of_the_theorems.quality_gate.md`。
- 已新增章节质量门禁检查脚本：`scripts/check_book_i2_chapter_quality_gate.py`。
- 已新增 npm 脚本：
  - `source:i2-chapter-gate`
  - `quality:i2-chapter-gate`
- 已将 `quality:i2-chapter-gate` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/002_book_i_02_chapter_quality_gate.json`
  - `qa/pretranslation/002_book_i_02_chapter_quality_gate.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.2 为 `CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING`。
- 这只表示 Book I.2 可以排队进入终稿前全书一致性审校；在全书预研究 PASS 前，仍不得写 `chapters/final/` 或正式 `output/book.epub`。

## 2026-05-17 Book I.3 source extraction and formal source recheck

- 已扩展通用 PAL 章节 source extractor：`scripts/extract_pal_chapter_source.py` 支持 `I.3`。
- 已扩展 source extraction 检查脚本：`scripts/check_chapter_source_extraction.py` 支持 `I.3`。
- 已新增 npm 脚本：
  - `source:i3-extract`
  - `source:i3-check`
  - `quality:i3-source`
  - `source:i3-formal-recheck`
  - `quality:i3-formal-recheck`
- 已生成：
  - `chapters/src/003_book_i_03_heaven_moves_spherically.md`
  - `qa/pretranslation/003_book_i_03_source_extraction_check.json`
  - `qa/pretranslation/003_book_i_03_source_extraction_check.md`
  - `qa/technical/page_screenshots/book_i03_pages_009_011_contact_sheet.jpg`
  - `qa/technical/003_book_i_03_heaven_moves_spherically.technical_audit.md`
  - `qa/pretranslation/003_book_i_03_formal_source_recheck.json`
  - `qa/pretranslation/003_book_i_03_formal_source_recheck.md`
- 已更新 `qa/technical/mathematical_term_lock.md`，加入 Book I.3 天球运动与观测反证术语预锁。
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.3 为 `FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING`。
- 下一步只能先创建章节控制文件；不得直接翻译、不得进终稿或正式 EPUB。

## 2026-05-17 Book I.3 chapter control

- 已新增章节控制文件：`qa/chapter_controls/003_book_i_03_heaven_moves_spherically.control.md`。
- 已新增章节控制检查脚本：`scripts/check_book_i3_chapter_control.py`。
- 已新增 npm 脚本：
  - `source:i3-control`
  - `quality:i3-control`
- 已将 `quality:i3-control` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/003_book_i_03_chapter_control_check.json`
  - `qa/pretranslation/003_book_i_03_chapter_control_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.3 为 `CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED`。
- 下一步只允许写受控译文 `chapters/translated/003_book_i_03_heaven_moves_spherically.md`；译后仍需复核、审校和质量门禁，不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.3 controlled translation draft

- 已新增受控译文草稿：`chapters/translated/003_book_i_03_heaven_moves_spherically.md`。
- 已新增译文检查脚本：`scripts/check_book_i3_translation.py`。
- 已新增 npm 脚本：
  - `source:i3-translation-check`
  - `quality:i3-translation`
- 已将 `quality:i3-translation` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/003_book_i_03_translation_check.json`
  - `qa/pretranslation/003_book_i_03_translation_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.3 为 `TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING`。
- 下一步必须进行忠实度、可读性、术语一致性、观测/反证链和古今概念边界审校；不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.3 draft review

- 已新增评审记录：`reviews/chapters/003_book_i_03_heaven_moves_spherically.review.md`。
- 已新增评审检查脚本：`scripts/check_book_i3_review.py`。
- 已新增 npm 脚本：
  - `source:i3-review`
  - `quality:i3-review`
- 已将 `quality:i3-review` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/003_book_i_03_review_check.json`
  - `qa/pretranslation/003_book_i_03_review_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.3 为 `REVIEW_PASS__TECHNICAL_RECHECK_PENDING`。
- 下一步必须进行译后技术复核；不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.3 post-translation technical recheck

- 已新增译后技术复核记录：`qa/technical/003_book_i_03_heaven_moves_spherically.post_translation_technical_recheck.md`。
- 已新增译后技术复核检查脚本：`scripts/check_book_i3_post_translation_technical_recheck.py`。
- 已新增 npm 脚本：
  - `source:i3-post-technical-recheck`
  - `quality:i3-post-technical-recheck`
- 已将 `quality:i3-post-technical-recheck` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/003_book_i_03_post_translation_technical_recheck.json`
  - `qa/pretranslation/003_book_i_03_post_translation_technical_recheck.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.3 为 `TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING`。
- 下一步必须建立章节质量门禁，聚合 source、formal recheck、chapter control、translation、review 和技术复核结果；不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.3 chapter quality gate

- 已新增章节质量门禁记录：`qa/chapter_controls/003_book_i_03_heaven_moves_spherically.quality_gate.md`。
- 已新增章节质量门禁检查脚本：`scripts/check_book_i3_chapter_quality_gate.py`。
- 已新增 npm 脚本：
  - `source:i3-chapter-gate`
  - `quality:i3-chapter-gate`
- 已将 `quality:i3-chapter-gate` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/003_book_i_03_chapter_quality_gate.json`
  - `qa/pretranslation/003_book_i_03_chapter_quality_gate.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.3 为 `CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING`。
- 这只表示 Book I.3 可以排队进入终稿前全书一致性审校；在全书预研究 PASS 前，仍不得写 `chapters/final/` 或正式 `output/book.epub`。

## 2026-05-17 Book I.4 source extraction candidate

- 已扩展通用 PAL 章节 source extractor 支持 I.4。
- 已扩展 source extraction 检查脚本支持 I.4。
- 已新增 npm 脚本：
  - `source:i4-extract`
  - `source:i4-check`
  - `quality:i4-source`
- 已将 `quality:i4-source` 接入 `quality:all`。
- 已生成：
  - `chapters/src/004_book_i_04_earth_is_spherical.md`
  - `qa/pretranslation/004_book_i_04_source_extraction_check.json`
  - `qa/pretranslation/004_book_i_04_source_extraction_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.4 为 `SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING`。
- 这只是 source extraction candidate；Book I.4 仍需 formal PDF recheck、章节控制和技术审计后，才可进入翻译。

## 2026-05-17 Book I.4 formal source recheck

- 已生成 Book I.4 PDF 页图证据：`qa/technical/page_screenshots/book_i04_pages_011_012_contact_sheet.jpg`。
- 已新增 Book I.4 技术审计：`qa/technical/004_book_i_04_earth_is_spherical.technical_audit.md`。
- 已更新 `qa/technical/mathematical_term_lock.md`，加入 Book I.4 地球球形与观测证据术语预锁。
- 已新增 `scripts/check_book_i4_formal_source_recheck.py`。
- 已新增 npm 脚本：
  - `source:i4-formal-recheck`
  - `quality:i4-formal-recheck`
- 已将 `quality:i4-formal-recheck` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/004_book_i_04_formal_source_recheck.json`
  - `qa/pretranslation/004_book_i_04_formal_source_recheck.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.4 为 `FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING`。
- 下一步只能先创建章节控制文件；不得直接翻译、不得进终稿或正式 EPUB。

## 2026-05-17 Book I.4 chapter control

- 已新增章节控制文件：`qa/chapter_controls/004_book_i_04_earth_is_spherical.control.md`。
- 已新增章节控制检查脚本：`scripts/check_book_i4_chapter_control.py`。
- 已新增 npm 脚本：
  - `source:i4-control`
  - `quality:i4-control`
- 已将 `quality:i4-control` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/004_book_i_04_chapter_control_check.json`
  - `qa/pretranslation/004_book_i_04_chapter_control_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.4 为 `CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED`。
- 下一步只允许写受控译文 `chapters/translated/004_book_i_04_earth_is_spherical.md`；译后仍需复核、审校和质量门禁，不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.4 controlled translation draft

- 已新增受控译文草稿：`chapters/translated/004_book_i_04_earth_is_spherical.md`。
- 已新增译文检查脚本：`scripts/check_book_i4_translation.py`。
- 已新增 npm 脚本：
  - `source:i4-translation-check`
  - `quality:i4-translation`
- 已将 `quality:i4-translation` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/004_book_i_04_translation_check.json`
  - `qa/pretranslation/004_book_i_04_translation_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.4 为 `TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING`。
- 下一步必须进行忠实度、可读性、术语一致性、观测证明链和古今概念边界审校；不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.4 draft review

- 已新增评审记录：`reviews/chapters/004_book_i_04_earth_is_spherical.review.md`。
- 已新增评审检查脚本：`scripts/check_book_i4_review.py`。
- 已新增 npm 脚本：
  - `source:i4-review`
  - `quality:i4-review`
- 已将 `quality:i4-review` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/004_book_i_04_review_check.json`
  - `qa/pretranslation/004_book_i_04_review_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.4 为 `REVIEW_PASS__TECHNICAL_RECHECK_PENDING`。
- 下一步必须进行译后技术复核；不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.4 post-translation technical recheck

- 已新增译后技术复核记录：`qa/technical/004_book_i_04_earth_is_spherical.post_translation_technical_recheck.md`。
- 已新增译后技术复核检查脚本：`scripts/check_book_i4_post_translation_technical_recheck.py`。
- 已新增 npm 脚本：
  - `source:i4-post-technical-recheck`
  - `quality:i4-post-technical-recheck`
- 已将 `quality:i4-post-technical-recheck` 接入 `quality:all`。
- 已生成：
  - `qa/pretranslation/004_book_i_04_post_translation_technical_recheck.json`
  - `qa/pretranslation/004_book_i_04_post_translation_technical_recheck.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.4 为 `TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING`。
- 下一步必须建立章节质量门禁，聚合 source、formal recheck、chapter control、translation、review 和技术复核结果；不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.4 chapter quality gate

- 已新增章节质量门禁记录：`qa/chapter_controls/004_book_i_04_earth_is_spherical.quality_gate.md`。
- 已新增章节质量门禁检查脚本：`scripts/check_book_i4_chapter_quality_gate.py`。
- 已新增 npm 脚本：
  - `source:i4-chapter-gate`
  - `quality:i4-chapter-gate`
- 已将 `quality:i4-chapter-gate` 接入 `quality:all` 和全书预翻译门禁 required files。
- 已生成：
  - `qa/pretranslation/004_book_i_04_chapter_quality_gate.json`
  - `qa/pretranslation/004_book_i_04_chapter_quality_gate.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.4 为 `CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING`。
- 这仍不是终稿门禁；Book I.4 只能进入终稿前全书一致性审校队列，仍不得写 `chapters/final/` 或生成正式 `output/book.epub`。

## 2026-05-17 Book I.5 source extraction candidate

- 已扩展通用 PAL 章节 source extractor 支持 I.5。
- 已扩展 source extraction 检查脚本支持 I.5。
- 已新增 npm 脚本：
  - `source:i5-extract`
  - `source:i5-check`
  - `quality:i5-source`
- 已将 `quality:i5-source` 接入 `quality:all` 和全书预翻译门禁 required files。
- 已生成：
  - `chapters/src/005_book_i_05_earth_is_central.md`
  - `qa/pretranslation/005_book_i_05_source_extraction_check.json`
  - `qa/pretranslation/005_book_i_05_source_extraction_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.5 为 `SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING`。
- 这只是 source extraction candidate；Book I.5 仍需 formal PDF recheck、章节控制和技术审计后，才可进入翻译。

## 2026-05-17 Book I.5 formal source recheck

- 已生成 Book I.5 PDF 页图证据：`qa/technical/page_screenshots/book_i05_pages_012_014_contact_sheet.jpg`。
- 已新增 Book I.5 技术审计：`qa/technical/005_book_i_05_earth_is_central.technical_audit.md`。
- 已更新 `qa/technical/mathematical_term_lock.md`，加入 Book I.5 地球居中与观测反证术语预锁。
- 已新增 `scripts/check_book_i5_formal_source_recheck.py`。
- 已新增 npm 脚本：
  - `source:i5-formal-recheck`
  - `quality:i5-formal-recheck`
- 已将 `quality:i5-formal-recheck` 接入 `quality:all` 和全书预翻译门禁 required files。
- 已生成：
  - `qa/pretranslation/005_book_i_05_formal_source_recheck.json`
  - `qa/pretranslation/005_book_i_05_formal_source_recheck.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.5 为 `FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING`。
- 下一步必须建立章节控制文件；不得直接进入翻译、`chapters/final/` 或正式 EPUB。

## 2026-05-17 Book I.5 chapter control

- 已新增章节控制文件：`qa/chapter_controls/005_book_i_05_earth_is_central.control.md`。
- 已新增章节控制检查脚本：`scripts/check_book_i5_chapter_control.py`。
- 已新增 npm 脚本：
  - `source:i5-control`
  - `quality:i5-control`
- 已将 `quality:i5-control` 接入 `quality:all` 和全书预翻译门禁 required files。
- 已生成：
  - `qa/pretranslation/005_book_i_05_chapter_control_check.json`
  - `qa/pretranslation/005_book_i_05_chapter_control_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.5 为 `CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED`。
- 下一步只允许写受控译文 `chapters/translated/005_book_i_05_earth_is_central.md`；译后仍需复核、审校和质量门禁，不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.5 controlled translation draft

- 已新增受控译文草稿：`chapters/translated/005_book_i_05_earth_is_central.md`。
- 已新增译文检查脚本：`scripts/check_book_i5_translation.py`。
- 已新增 npm 脚本：
  - `source:i5-translation-check`
  - `quality:i5-translation`
- 已将 `quality:i5-translation` 接入 `quality:all` 和全书预翻译门禁 required files。
- 已生成：
  - `qa/pretranslation/005_book_i_05_translation_check.json`
  - `qa/pretranslation/005_book_i_05_translation_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.5 为 `TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING`。
- 下一步必须进行忠实度、中文可读性、术语一致性、天文学证明链和古今概念边界审校；仍不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.5 draft review

- 已新增评审记录：`reviews/chapters/005_book_i_05_earth_is_central.review.md`。
- 已新增评审检查脚本：`scripts/check_book_i5_review.py`。
- 已新增 npm 脚本：
  - `source:i5-review`
  - `quality:i5-review`
- 已将 `quality:i5-review` 接入 `quality:all` 和全书预翻译门禁 required files。
- 已生成：
  - `qa/pretranslation/005_book_i_05_review_check.json`
  - `qa/pretranslation/005_book_i_05_review_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.5 为 `REVIEW_PASS__TECHNICAL_RECHECK_PENDING`。
- 下一步必须执行译后技术复核和章节质量门禁；仍不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.5 post-translation technical recheck

- 已新增译后技术复核记录：`qa/technical/005_book_i_05_earth_is_central.post_translation_technical_recheck.md`。
- 已新增译后技术复核检查脚本：`scripts/check_book_i5_post_translation_technical_recheck.py`。
- 已新增 npm 脚本：
  - `source:i5-post-technical-recheck`
  - `quality:i5-post-technical-recheck`
- 已将 `quality:i5-post-technical-recheck` 接入 `quality:all` 和全书预翻译门禁 required files。
- 已生成：
  - `qa/pretranslation/005_book_i_05_post_translation_technical_recheck.json`
  - `qa/pretranslation/005_book_i_05_post_translation_technical_recheck.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.5 为 `TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING`。
- 下一步必须建立章节质量门禁，聚合 source、formal recheck、chapter control、translation、review 和技术复核结果；不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.5 chapter quality gate

- 已新增章节质量门禁记录：`qa/chapter_controls/005_book_i_05_earth_is_central.quality_gate.md`。
- 已新增章节质量门禁检查脚本：`scripts/check_book_i5_chapter_quality_gate.py`。
- 已新增 npm 脚本：
  - `source:i5-chapter-gate`
  - `quality:i5-chapter-gate`
- 已将 `quality:i5-chapter-gate` 接入 `quality:all` 和全书预翻译门禁 required files。
- 已生成：
  - `qa/pretranslation/005_book_i_05_chapter_quality_gate.json`
  - `qa/pretranslation/005_book_i_05_chapter_quality_gate.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.5 为 `CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING`。
- 下一步是终稿前全书一致性审校；在 `formal_translation_allowed=false` 时，仍不得进入 `chapters/final/` 或生成正式 EPUB。

## 2026-05-17 Book I.6 source extraction candidate

- 已新增 Book I.6 source extraction candidate：`chapters/src/006_book_i_06_earth_as_point_to_heavens.md`。
- 已将 Book I.6 加入 PAL 章节抽取脚本和 source extraction 检查脚本。
- 已新增 npm 脚本：
  - `source:i6-extract`
  - `source:i6-check`
  - `quality:i6-source`
- 已将 `quality:i6-source` 接入 `quality:all` 和全书预翻译门禁 required files。
- 已生成：
  - `qa/pretranslation/006_book_i_06_source_extraction_check.json`
  - `qa/pretranslation/006_book_i_06_source_extraction_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.6 为 `SOURCE_EXTRACTED__PDF_RECHECK_AND_TECHNICAL_QA_PENDING`。
- 这只是 source extraction candidate；Book I.6 仍需 formal PDF recheck、章节控制和技术审计后，才可进入翻译。

## 2026-05-17 Book I.6 formal source recheck

- 已生成 Book I.6 PDF 页图证据：`qa/technical/page_screenshots/book_i06_page_014_contact_sheet.jpg`。
- 已新增 Book I.6 技术审计：`qa/technical/006_book_i_06_earth_as_point_to_heavens.technical_audit.md`。
- 已更新 `qa/technical/mathematical_term_lock.md`，加入 Book I.6 地球尺度与观测平面术语预锁。
- 已新增 `scripts/check_book_i6_formal_source_recheck.py`。
- 已新增 npm 脚本：
  - `source:i6-formal-recheck`
  - `quality:i6-formal-recheck`
- 已将 `quality:i6-formal-recheck` 接入 `quality:all` 和全书预翻译门禁 required files。
- 已生成：
  - `qa/pretranslation/006_book_i_06_formal_source_recheck.json`
  - `qa/pretranslation/006_book_i_06_formal_source_recheck.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.6 为 `FORMAL_SOURCE_RECHECK_PASS__CHAPTER_CONTROL_PENDING`。
- 下一步必须建立章节控制文件；不得直接进入翻译、`chapters/final/` 或正式 EPUB。

## 2026-05-17 Book I.6 chapter control

- 已新增章节控制文件：`qa/chapter_controls/006_book_i_06_earth_as_point_to_heavens.control.md`。
- 已新增章节控制检查脚本：`scripts/check_book_i6_chapter_control.py`。
- 已新增 npm 脚本：
  - `source:i6-control`
  - `quality:i6-control`
- 已将 `quality:i6-control` 接入 `quality:all` 和全书预翻译门禁 required files。
- 已生成：
  - `qa/pretranslation/006_book_i_06_chapter_control_check.json`
  - `qa/pretranslation/006_book_i_06_chapter_control_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.6 为 `CHAPTER_CONTROL_PASS__CONTROLLED_TRANSLATION_PREP_ALLOWED`。
- 下一步只允许写受控译文 `chapters/translated/006_book_i_06_earth_as_point_to_heavens.md`；译后仍需复核、审校和质量门禁，不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.6 controlled translation draft

- 已新增受控译文草稿：`chapters/translated/006_book_i_06_earth_as_point_to_heavens.md`。
- 已新增译文检查脚本：`scripts/check_book_i6_translation.py`。
- 已新增 npm 脚本：
  - `source:i6-translation-check`
  - `quality:i6-translation`
- 已将 `quality:i6-translation` 接入 `quality:all` 和全书预翻译门禁 required files。
- 已生成：
  - `qa/pretranslation/006_book_i_06_translation_check.json`
  - `qa/pretranslation/006_book_i_06_translation_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.6 为 `TRANSLATION_DRAFT_PASS__REVIEW_AND_TECHNICAL_RECHECK_PENDING`。
- 下一步必须进行忠实度、中文可读性、术语一致性、天文学证明链和古今概念边界审校；仍不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.6 draft review

- 已新增评审记录：`reviews/chapters/006_book_i_06_earth_as_point_to_heavens.review.md`。
- 已新增评审检查脚本：`scripts/check_book_i6_review.py`。
- 已新增 npm 脚本：
  - `source:i6-review`
  - `quality:i6-review`
- 已将 `quality:i6-review` 接入 `quality:all` 和全书预翻译门禁 required files。
- 已生成：
  - `qa/pretranslation/006_book_i_06_review_check.json`
  - `qa/pretranslation/006_book_i_06_review_check.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.6 为 `REVIEW_PASS__TECHNICAL_RECHECK_PENDING`。
- 下一步必须执行译后技术复核和章节质量门禁；仍不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.6 post-translation technical recheck

- 已新增译后技术复核记录：`qa/technical/006_book_i_06_earth_as_point_to_heavens.post_translation_technical_recheck.md`。
- 已新增译后技术复核检查脚本：`scripts/check_book_i6_post_translation_technical_recheck.py`。
- 已新增 npm 脚本：
  - `source:i6-post-technical-recheck`
  - `quality:i6-post-technical-recheck`
- 已将 `quality:i6-post-technical-recheck` 接入 `quality:all` 和全书预翻译门禁 required files。
- 已生成：
  - `qa/pretranslation/006_book_i_06_post_translation_technical_recheck.json`
  - `qa/pretranslation/006_book_i_06_post_translation_technical_recheck.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.6 为 `TECHNICAL_RECHECK_PASS__CHAPTER_QUALITY_GATE_PENDING`。
- 下一步必须建立章节质量门禁，聚合 source、formal recheck、chapter control、translation、review 和技术复核结果；不得直接进入 `chapters/final/`。

## 2026-05-17 Book I.6 chapter quality gate

- 已新增章节质量门禁记录：`qa/chapter_controls/006_book_i_06_earth_as_point_to_heavens.quality_gate.md`。
- 已新增章节质量门禁检查脚本：`scripts/check_book_i6_chapter_quality_gate.py`。
- 已新增 npm 脚本：
  - `source:i6-chapter-gate`
  - `quality:i6-chapter-gate`
- 已将 `quality:i6-chapter-gate` 接入 `quality:all` 和全书预翻译门禁 required files。
- 已生成：
  - `qa/pretranslation/006_book_i_06_chapter_quality_gate.json`
  - `qa/pretranslation/006_book_i_06_chapter_quality_gate.md`
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.6 为 `CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING`。
- 下一步是终稿前全书一致性审校；在 `formal_translation_allowed=false` 时，仍不得进入 `chapters/final/` 或生成正式 EPUB。

## 2026-05-17 Book I.7 controlled chapter pass

- 已新增 Book I.7 source extraction candidate：`chapters/src/007_book_i_07_earth_has_no_translational_motion.md`。
- 已生成 Book I.7 PDF 页图证据：`qa/technical/page_screenshots/book_i07_pages_015_017_contact_sheet.jpg`。
- 已新增译前技术审计：`qa/technical/007_book_i_07_earth_has_no_translational_motion.technical_audit.md`。
- 已新增章节控制、受控译文草稿、草稿级评审、译后技术复核和章节质量门禁：
  - `qa/chapter_controls/007_book_i_07_earth_has_no_translational_motion.control.md`
  - `chapters/translated/007_book_i_07_earth_has_no_translational_motion.md`
  - `reviews/chapters/007_book_i_07_earth_has_no_translational_motion.review.md`
  - `qa/technical/007_book_i_07_earth_has_no_translational_motion.post_translation_technical_recheck.md`
  - `qa/chapter_controls/007_book_i_07_earth_has_no_translational_motion.quality_gate.md`
- 已新增并运行 Book I.7 全套检查脚本：source extraction、formal source recheck、chapter control、translation、review、post-technical-recheck、chapter-gate。
- 已新增 npm 脚本：`source:i7-*` 与 `quality:i7-*`，并接入 `quality:all`。
- 已将 Book I.7 全套控制文件纳入全书预翻译门禁 required files。
- `qa/pretranslation/book_i_source_split_readiness.md` 已记录 Book I.7 为 `CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING`。
- 下一步继续推进 Book I.8 source extraction 与 PDF formal recheck；仍不得进入 `chapters/final/` 或生成正式 EPUB。

## 2026-05-17 Book I.8 controlled chapter pass

- 已新增 Book I.8 source extraction candidate：`chapters/src/008_book_i_08_two_primary_motions.md`。
- 已生成 Book I.8 PDF 页图证据：`qa/technical/page_screenshots/book_i08_pages_017_019_contact_sheet.jpg`。
- 已新增译前技术审计：`qa/technical/008_book_i_08_two_primary_motions.technical_audit.md`。
- 已更新 `qa/technical/mathematical_term_lock.md`，加入 Book I.8 天球两种基本运动术语预锁。
- 已新增章节控制、受控译文草稿、草稿级评审、译后技术复核和章节质量门禁：
  - `qa/chapter_controls/008_book_i_08_two_primary_motions.control.md`
  - `chapters/translated/008_book_i_08_two_primary_motions.md`
  - `reviews/chapters/008_book_i_08_two_primary_motions.review.md`
  - `qa/technical/008_book_i_08_two_primary_motions.post_translation_technical_recheck.md`
  - `qa/chapter_controls/008_book_i_08_two_primary_motions.quality_gate.md`
- 已新增并运行 Book I.8 全套检查脚本：source extraction、formal source recheck、chapter control、translation、review、post-technical-recheck、chapter-gate。
- 已新增 npm 脚本：`source:i8-*` 与 `quality:i8-*`，并接入 `quality:all`。
- 已将 Book I.8 全套控制文件纳入全书预翻译门禁 required files。
- `qa/pretranslation/book_i_source_split_readiness.md` 将记录 Book I.8 为 `CHAPTER_QUALITY_GATE_PASS__FINAL_PROMOTION_PENDING`。
- 下一步继续推进 Book I.9；仍不得进入 `chapters/final/` 或生成正式 EPUB。

## 2026-05-17 Book I.9 controlled chapter pass

- 已新增 Book I.9 source extraction candidate：`chapters/src/009_book_i_09_on_individual_preliminaries.md`。
- 已生成 Book I.9 PDF 页图证据：`qa/technical/page_screenshots/book_i09_page_019_contact_sheet.jpg`。
- 已新增译前技术审计：`qa/technical/009_book_i_09_on_individual_preliminaries.technical_audit.md`。
- 已更新 `qa/technical/mathematical_term_lock.md`，加入 Book I.9 具体测定与弦论引入术语预锁。
- 已新增章节控制、受控译文草稿、草稿级评审、译后技术复核和章节质量门禁：
  - `qa/chapter_controls/009_book_i_09_on_individual_preliminaries.control.md`
  - `chapters/translated/009_book_i_09_on_individual_preliminaries.md`
  - `reviews/chapters/009_book_i_09_on_individual_preliminaries.review.md`
  - `qa/technical/009_book_i_09_on_individual_preliminaries.post_translation_technical_recheck.md`
  - `qa/chapter_controls/009_book_i_09_on_individual_preliminaries.quality_gate.md`
- 已新增并运行 Book I.9 全套检查脚本：source extraction、formal source recheck、chapter control、translation、review、post-technical-recheck、chapter-gate。
- 已新增 npm 脚本：`source:i9-*` 与 `quality:i9-*`，并接入 `quality:all`。
- 已将 Book I.9 全套控制文件纳入全书预翻译门禁 required files。
- 下一步转入 Book I.10 的正式章节控制复核；仍不得进入 `chapters/final/` 或生成正式 EPUB。

## 2026-05-17 Book I.10 controlled chapter pass

- 已将 Book I.10 从试译通过状态升级为 Book I 章节级受控草稿队列；这不是终稿许可。
- 已调整 `chapters/src/010_book_i_10_chords.md` 的 source-control 状态，使其作为 formal source extraction candidate 接受 source 检查。
- 已调整 `chapters/translated/010_book_i_10_chords.md` 的章节状态为受控草稿；仍保留 Book I.11 弦表本体排除。
- 已新增 Book I.10 章节级评审、译后技术复核和章节质量门禁：
  - `reviews/chapters/010_book_i_10_chords.review.md`
  - `qa/technical/010_book_i_10_chords.post_translation_technical_recheck.md`
  - `qa/chapter_controls/010_book_i_10_chords.quality_gate.md`
- 已新增并运行 Book I.10 全套检查脚本：source extraction、formal source recheck、chapter control、translation、review、post-technical-recheck、chapter-gate。
- 已新增 npm 脚本：`source:i10-*` 与 `quality:i10-*`，并接入 `quality:all`。
- 已将 Book I.10 全套控制文件纳入全书预翻译门禁 required files。
- 下一步是 Book I.11 弦表的结构化 source extraction 与数值校验；不得直接翻译弦表正文，仍不得进入 `chapters/final/` 或生成正式 EPUB。
