# /goal: 《Almagest》Book I 翻译阶段、第一版 EPUB 与双 Agent 评审闭环

日期：2026-05-17

本 `/goal` 是 `books/ptolemy_almagest_grc_zh_hans/` 进入 Book I 翻译阶段的执行合约。它必须遵守仓库根目录 `AGENTS.md`、本书 `AGENTS.md`、`PIPELINE_SPEC.md`、`MASTER_PROMPT.md`、`prompts/00_orchestrator_zh_grc.md`、`template/epub_pipeline/grc-zh-Hans`、`template/epub_pipeline/profiles/classical-science-zh-Hans`、`template/epub_pipeline/targets/zh-Hans`，以及本书已有 `metadata/`、`source/`、`qa/`、`references/`、`prompts/`、`state/` 文件。

## 2026-05-17 范围修订

用户已明确收窄本轮执行范围：只完成 Book I，不完成 13 卷全书。既有 PAL 全书目录、全书风险图和跨卷术语/模型记录只作为 Book I 的背景参考，不再作为本轮退出条件。

本轮退出条件改为：Book I 共 16 章完成 `src`、`translated`、`final` 和必要 QA；完成 Book I 第一版 EPUB；经数学/天文学/图表/表格/数值/中文可读性精校；至少 2 个独立 Agent 依据模板对 Book I 随机抽检和整体评审通过。Book II-XIII 不进入本轮翻译、终稿或 EPUB 生产。

## /goal 目标

进入《Almagest / 天文学大成》Book I 翻译阶段：在 `D:\project\49_public-domain-books-translation` 中，严格依据 `books/ptolemy_almagest_grc_zh_hans` 与模板流程，完成 Book I 预研究与总纲，再按 Book I 章节推进古希腊文底本翻译、数学/天文学专项校核、Book I 第一版 EPUB 制作、迭代评审与精校。只有完成 Book I 第一版 EPUB，且至少 2 个独立 Agent 按模板随机抽检和整体评审通过后，才可退出任务。

## 当前启动状态

- Book I.10 受控试译、试译评审和样书 EPUB 预制作已完成，作为全书阶段的工程样本。
- 现在进入 Book I 阶段：Book I 预研究、目录总纲、正式分章策略、风险分级、门禁路线设计。
- 本轮已生成 PAL 全书目录草案：
  - `source/full_toc_draft.json`
  - `source/full_book_translation_outline.md`
- PAL 目录草案显示全书 `13` 卷、`146` 章；本轮只取 Book I 的 `16` 章作为执行范围。全书目录只是背景索引，不是本轮完成目标。

## 来源角色硬规则

1. Heiberg PDF 扫描：主底本影像。负责古希腊正文核验、页图、版面、图表、表格、校勘/脚注区和最终出版 facsimile 图来源。
2. PAL Heiberg 古希腊文转写 XML：辅助古希腊文转写。负责可复制文本、章节切分、PAL/Heiberg 页标、分词链、长周期句分析、OCR/人工转写疑点校正和 source text 抽取。
3. 英译本：reference witness only。只可用于疑难理解、术语对照、技术差异提示和差异摘要；不得作为中文转译底稿，不得复制现代译本表达、注释、图表、表格或编辑结构，也不得作为 OCR/转写修正 authority。

冲突处理顺序：先回查 Heiberg PDF 和 PAL 古希腊转写；必要时查 Heiberg 校勘语境和 `qa/textual/`、`qa/technical/` 记录；英译本只能提示疑点，不能覆盖古希腊文证据。

## 阶段 0：全书预研究与总纲

本阶段必须完成后，才能正式批量分章翻译。

必须输出或更新：

- `source/full_toc_draft.json`
- `source/full_book_translation_outline.md`
- `source/book_{roman}_segmentation.md` 或等效逐卷分章控制文件
- `qa/pretranslation/full_book_pre_research_plan.md` 或等效全书预研究计划
- `qa/technical/diagram_table_inventory.md`
- `qa/technical/proof_dependency_map.md`
- `qa/technical/numeric_validation_log.md`
- `qa/technical/table_validation_log.md`
- `qa/technical/equation_notation_registry.csv`
- `qa/technical/claim_traceability_matrix.csv`
- `qa/technical/astronomical_model_registry.csv`
- `qa/technical/mathematical_term_lock.md`
- `metadata/rights_checklist.md`
- `metadata/source_witness_manifest.md`
- `metadata/reference_witness_policy.md`
- `qa/pretranslation/pretranslation_report.md`
- `state/pipeline_state.json`

全书预研究 PASS 条件：

- Heiberg PDF、PAL XML、英译本参考边界三者分工清楚，并通过 `npm run quality:source-roles`。
- 全书目录来自 PAL 古希腊转写并回到 PDF 页图抽样核验；不得从英译本目录生成正式目录。
- 全书正式 source split 策略明确，每章都有 PAL anchor、Heiberg 页码、PDF viewer page 范围或待核验状态。
- Book I 到 Book XIII 的数学、天文学、表格、图表、星表和数值风险分级明确。
- 术语锁定至少达到 `LOCKED_WITH_SCOPE`：正文译法、章末注释、六十进制、角度、非角度弦长、Euclid 依据说明规则稳定。
- 图表/表格策略明确：EPUB 初版优先使用 Heiberg PDF 裁图 facsimile；可结构化表格必须输出为 XHTML table，不得只用图片替代表格。
- 对弦表、星表、行星模型、黄道/赤道关系、食限、视差、恒星目录等高风险章节有专门 QA 路由。

## 阶段 1：正式分章 source split

只允许从古希腊文底本链路生成 `chapters/src/*.md`。

每章 source 文件必须记录：

- book/chapter 编号。
- PAL anchor 起止点。
- PAL page markers。
- Heiberg PDF 页图范围。
- 是否涉及图表、表格、数值、证明、天文学模型、星表。
- 参考译本是否只作为 reference witness。
- 未决 OCR/转写/异文/残损/拟补问题。

本阶段禁止：

- 从英译本复制目录、段落或译文。
- 把 PAL XML 当作最终图表/页图 authority。
- 未核 PDF 页图就把章节推进到翻译 PASS。

## 阶段 2：逐章翻译

每章按 `prompts/07_translate_chapters_zh_grc.md` 输出到：

- `chapters/translated/{same_filename}.md`

翻译规则：

- 必须从古希腊文底稿翻译。
- 英译本只能用于疑难校读和差异提示。
- 中文必须现代、清楚、可读；古代术语直译影响理解时，正文采用现代可读表达，章末集中注释说明原文表达和古今概念边界。
- Euclid、Hipparchus、古代天文学依据不得裸写缩写；正文用“依据《几何原本》……〔n〕”，章末说明对应命题、定义或系的大意。
- 六十进制数值：角度用 `°′″`，非角度弦长/平方量等用 `37p04′55″` 这类 `p` 加六十进制小分格式。不得裸用内部 `;`/`,` 记法，不得写成“份”，不得统一转成十进制小数。
- 图表标签、弧/角/弦、点名、线段、表格字段必须与源图、正文和 QA 记录一致。

## 阶段 3：章节译后控制、技术审计和终稿门禁

每章翻译后必须立即进入：

- `prompts/08a_chapter_post_translation_control_zh_grc.md`
- `prompts/08_review_fidelity_zh_grc.md`
- `prompts/08b_chapter_technical_audit_zh_Hans.md`
- `prompts/08c_diagram_table_audit_zh_Hans.md`
- `prompts/09_review_readability_imagery_zh_grc.md`
- `prompts/10_review_terminology_zh_grc.md`
- `prompts/11_chapter_quality_gate_zh_grc.md`

每章至少输出：

- `qa/chapter_controls/{same_filename}.control.md`
- `qa/technical/{same_filename}.technical_audit.md`
- `qa/technical/{same_filename}.diagram_table_audit.md`，若本章无图表也要明确记录。
- 必要的 proof、notation、numeric、table、claim traceability 更新。

只有章节门禁 PASS 后，才可写入：

- `chapters/final/{same_filename}.md`

## 阶段 4：第一版 EPUB

所有章节终稿 PASS 后，执行：

- `prompts/13_preproduction_stage1_spec_zh_grc.md`
- `prompts/14_preproduction_stage2_sample_zh_grc.md`
- `prompts/15_full_book_production_zh_grc.md`
- `prompts/12_build_validate_zh_grc.md`

必须输出：

- `preproduction/stage1/production_spec.md`
- `preproduction/stage2_sample/sample_book.epub`
- `preproduction/stage2_sample/sample_review.md`
- `output/book.epub`
- `output/publication_lint.json`
- `output/asset_manifest_check.json`
- `output/epubcheck.json` 或 `output/epubcheck.log`

EPUBCheck 必须 fatal=0、error=0。`npm run quality:all`、`npm run build:epub` 和资源 manifest 检查必须通过。

## 阶段 5：EPUB 后再评审、精校和迭代

第一版 EPUB 完成后，必须多轮精校，重点检查：

- 古希腊文忠实度。
- 中文可读性。
- 数学证明链。
- 天文学模型与古今概念边界。
- 图表标签、正文引用、点线关系。
- 弦表、星表、角度、六十进制、近似说明。
- 术语一致性。
- EPUB 手机阅读体验、图表缩放、章末注释、目录、metadata、封面。

发现 P0/P1/P2 必修问题时，必须写入 `reviews/revision_route.md`，回到相应阶段修复。不得只在 EPUB 成品上表面修补。

## 阶段 6：双独立 Agent 随机抽检与最终评审

每轮精校后必须执行：

```powershell
npm run review:random-samples
```

要求：

- 至少 2 个独立 Agent。
- 每个 Agent 至少 10 个随机读者可见段落。
- 样本必须来自 `chapters/final`，不得由主执行 AI 人工挑选。
- `reviews/random_spotcheck/random_sample_manifest.json` 必须记录 seed、候选段落数和 Agent 样本编号。
- 每个 Agent 假设自己是认真阅读本书的中文读者，逐段检查是否读得懂、是否忠实、数学/天文学链条是否成立、术语/数值/图表/注释是否清楚。
- 每段 0-100 分。每个 Agent 平均分必须 >= 75，且无单段 < 70。
- 任一段出现读不懂、数学证明链断裂、天文学概念误导、术语/数值/图表关系错误，必须判为失败。

最终独立评审至少需要：

- Agent A：内容、古希腊文忠实度、中文可读性、术语、数学/天文学。
- Agent B：EPUB 工程、排版、metadata、封面、移动端可读性、lint、EPUBCheck。
- 若 A/B 未充分覆盖数学/天文学，则增加 Agent C：数学/天文学专项评审。

退出条件：

- `output/book.epub` 存在并通过校验。
- 所有章节存在 src、translated、final 和 QA 记录。
- 所有数学、天文学、图表、表格、数值检查 PASS。
- 随机段落抽检通过：至少 2 个独立 Agent，各不少于 10 段，平均分均 >= 75，且无单段 < 70。
- 至少 2 个独立 Agent 总评 PASS，且每个 PASS Agent 总分 >= 85。
- 无 P0/P1。
- P2 必修项全部关闭。
- `reviews/revision_route.md` 无未关闭阻断项。
- 复盘和模板经验回填完成或明确记录为不需要。

## 当前立刻执行项

本轮先执行：

1. 生成 PAL 全书目录草案和风险总纲。
2. 写入本 `/goal` 文件。
3. 更新 `state/pipeline_state.json`，将状态推进到全书预研究启动，但不直接解除章节翻译门禁。
4. 建立全书预研究计划，明确下一步先做正式分章、权利复核、图表/表格总清单和术语锁定升级。

本轮不直接批量翻译，不写 `chapters/final/`，不生成正式 `output/book.epub`。
