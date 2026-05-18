# 古希腊文到简体中文 EPUB 公版书翻译制作模板 / Ancient Greek to Simplified Chinese EPUB Translation Pipeline

## 目标 / Goal

给 AI 这个语言模板目录 `TEMPLATE_ROOT`、共享模板目录 `COMMON_TEMPLATE_ROOT`、目标工程目录 `PROJECT_ROOT` 和原书来源 `SOURCE_URL`，AI 应能自动完成：

1. 下载/读取古希腊文公版底本。
2. 核查来源、版权、版本、编辑者、扫描/OCR/转写状态。
3. 记录 source witnesses、章节编号、页码/行号体系和文本不确定性。
4. 清洗、分章，并保留可追溯的原文证据。
5. 完成通用翻译研究、古希腊文专项研究、本书专项研究和预翻译试译。
6. 生成术语表、专名转写表、文体画像、译注策略和参考译本使用边界。
7. 分章翻译、每章节译后控制、忠实度审校、可读性审校、术语审校和章节门禁。
8. 预制作阶段 1：封面、书籍信息、作者信息、字体、排版、标题、metadata、版本说明等规格。
9. 预制作阶段 2：先生成样章 EPUB，检查通过后再制作全书。
10. 生成 `output/book.epub`。
11. 通过 EPUB 校验和出版文本 lint。
12. 第一版全书 EPUB 后强制执行分层随机抽检模块，抽样正文段落、表格、图片、公式/证明块、图注和注释。
13. 派生 2 个独立 Agent 做严格评审并评分。
14. 根据评审和分层随机抽检结果回退到任意前置阶段返工；返工后必须定点关闭旧问题并使用新 seed 复抽。
15. 随机抽检闭环通过后，生成 `output/release/book_vX.X.X.epub` 和中英文 `release_note_vX.X.X.md`。
16. 全阶段复审，总结经验教训，必要时递增模板版本。

目标不是“从希腊文大概翻出来”，而是产出来源清楚、版本可追溯、译文可读、术语稳定、EPUB 制作质量合格的简体中文正本书。

This template handles Ancient Greek source-language issues for Simplified Chinese EPUB production. It does not replace book-type profiles such as `profiles/classical-science-zh-Hans`; use that profile in addition when the work is mathematical, astronomical, diagram-heavy, table-heavy, proof-heavy, or technically dense.

## 唯一必须输入 / Required Inputs

- `TEMPLATE_ROOT`：语言方向模板目录，即 `template/epub_pipeline/grc-zh-Hans`。
- `COMMON_TEMPLATE_ROOT`：共享 EPUB 流水线目录，即 `template/epub_pipeline/common`。
- `PROJECT_ROOT`：复制模板后的具体书籍工程目录；如未提供，AI 必须用 `books/scripts/create_book_project.py` 自动创建。
- `SOURCE_URL`：古希腊文公版来源 URL，例如校勘版扫描、TEI/XML、Perseus、Wikisource、Internet Archive 或其他可核查来源。

可选输入：

- `PROFILE_ROOT`：特殊书型控制模板，例如 `template/epub_pipeline/profiles/classical-science-zh-Hans`。
- `REFERENCE_TRANSLATION_URLS`：第二语言参考译本来源，只能用于理解、差异校对和技术核验，不能直接转译。

## 模板保护 / Template Protection

严禁直接在模板原目录中制作具体书籍。执行任何书籍项目前，AI 必须先把 `template/epub_pipeline/common` 与 `template/epub_pipeline/grc-zh-Hans` 合并复制到独立书籍工程目录，例如：

`books/zh-Hans/{number}_{book_id_slug}/`

如果启用 profile，则在语言方向模板之后再覆盖复制 profile：

`common -> grc-zh-Hans -> profiles/{profile-target} -> books/zh-Hans/{number}_{book_id_slug}/`

之后所有抓取、研究、翻译、QA、EPUB 输出都只能写入新书籍工程目录。

如果用户只给了语言模板目录和 `SOURCE_URL`，AI 的第一步必须是定位对应的 `COMMON_TEMPLATE_ROOT`，然后用 `books/scripts/create_book_project.py` 创建独立工程目录并自动分配数字前缀；不得把某本书的数据写回模板目录。

Node.js 工具依赖不随每本书重复安装。先在 `books/` 目录运行 `npm install`，再进入具体书籍目录运行 `npm run lint:publication`、`npm run build:epub`、`npm run check:epub`。本模板的 `package.json` 只提供本书脚本，依赖统一来自共享的 `books/node_modules/`，脚本必须向上查找共享依赖，不能假定书籍目录直接位于 `books/` 下。

## 古希腊文专项规则 / Ancient Greek Rules

- 原书语言文本是底本；现代英译、法译、德译等只能作参考译本。
- 必须记录所用希腊文版本、编辑者、卷册、页码/行号或章节编号。
- 如果来源是扫描件，必须记录 OCR 或人工转写状态；不能把未校 OCR 当成可靠底本。
- 若同时使用 PDF 扫描、古希腊文转写和第二语言译本，必须写明三者分工：PDF/校勘本影像用于底本页图和最终核验；古希腊转写用于检索、切分、分词链和细节校正；第二语言译本只作参考证据。
- 若存在校勘异文，必须记录采用哪个读法；疑难处不得静默选择。
- 人名、地名、神名、技术术语应建立转写/意译/通行译名策略。
- 古典作品中的语法省略、长周期句、分词链、引语和嵌套从句，必须转成自然中文，同时保留逻辑关系。
- 不得把第二语言参考译本的表达、注释或结构当作中文译文来源。

## 必读参考文件 / Required References

- `references/ancient_greek_source_notes.md`
- `references/ancient_greek_source_types.md`
- `references/ancient_greek_textual_criticism_policy.md`
- `references/ancient_greek_reference_translation_policy.md`
- `references/ancient_greek_names_transliteration_policy.md`
- `references/ancient_greek_title_strategy.md`
- `references/ancient_greek_to_chinese_translation_notes.md`
- `references/quality_standard.md`

## 关键产物 / Key Records

- `metadata/source_witness_manifest.md`：底本、版本、扫描/OCR/转写、witness 和编号体系。
- `source/triangulated_source_control.md` 或等效文件：当一本书同时使用扫描、古希腊转写和第二语言译本时，记录三者分工和冲突处理顺序。
- `qa/textual/textual_uncertainty_log.md`：异文、残损、拟补、OCR 不确定和语法歧义记录。
- `glossary/terms.csv`：古希腊文原词、必要转写、中文译名和说明。
- `metadata/chapter_title_map.yaml`：需要时记录原题、导航短题名、页面主标题、副标题和说明。

## 人类可选干预点 / Optional Human Checkpoints

原则上 AI 自动执行。复制到书籍工程后的 `state/human_feedback_control.md` 的 `human_required` 决定是否必须停下等人类检查。

默认：`human_required=false`，AI 自动执行。

建议人类可选查看：

- `metadata/source_witness_manifest.md`：底本、witness、编号体系和来源风险。
- `qa/textual/textual_uncertainty_log.md`：异文、残损、拟补、OCR 不确定和语法歧义。
- `metadata/book_specific_translation_research.md`：本书专项翻译研究。
- `qa/pretranslation/pretranslation_report.md`：预翻译试译报告。
- `glossary/terms.csv`：专名、术语和转写策略。
- `qa/chapter_controls/{NNN_slug}.control.md`：某章译后控制。
- `preproduction/stage1/production_spec.md`：全书制作规格。
- `preproduction/stage2_sample/sample_book.epub`：样章 EPUB。
- `reviews/random_spotcheck/round_XXX/`：分层随机抽检样本、证据、评审、修复和闭环记录。
- `output/release/`：带版本号的 EPUB、release note、release state 和发布索引。
- `reviews/scorecards/final_quality_score.md`：最终质量评分。

如果无人干预，AI 只有在报告明确 `PASS` 时才可继续；若 `FAIL`，必须按回溯规则自行修正，不能跳过。

## 执行顺序 / Execution Order

1. `prompts/00_orchestrator_zh_grc.md`
2. `prompts/01_ingest_clean_zh_grc.md`
3. `prompts/02_split_zh_grc.md`
4. `prompts/03_global_translation_research_zh_grc.md`
5. `prompts/04_book_specific_research_zh_grc.md`
6. `prompts/05_pretranslation_trials_zh_grc.md`
7. `prompts/06_glossary_style_zh_grc.md`
8. `prompts/07_translate_chapters_zh_grc.md`
9. `prompts/08a_chapter_post_translation_control_zh_grc.md`
10. `prompts/08_review_fidelity_zh_grc.md`
11. `prompts/09_review_readability_imagery_zh_grc.md`
12. `prompts/10_review_terminology_zh_grc.md`
13. `prompts/11_chapter_quality_gate_zh_grc.md`
14. `prompts/13_preproduction_stage1_spec_zh_grc.md`
15. `prompts/14_preproduction_stage2_sample_zh_grc.md`
16. `prompts/15_full_book_production_zh_grc.md`
17. `prompts/16a_stratified_random_spotcheck.md`
18. `prompts/16_independent_review_agents_zh_grc.md`
19. `prompts/17_revision_routing_zh_grc.md`
20. `prompts/18a_release_versioning.md`
21. `prompts/18_final_output_zh_grc.md`
22. `prompts/19_retrospective_template_update_zh_grc.md`

若启用 `classical-science-zh-Hans` profile，则在本书专项研究、术语、图表、章节译后控制和最终评审阶段插入 profile 的额外门禁。

## 硬门禁 / Hard Gates

- 没有古希腊文公版来源证据，不得翻译。
- 未记录底本版本、编辑者或来源状态，不得预翻译。
- OCR/转写未经说明，不得作为可靠正文批量翻译。
- 未建立 `metadata/source_witness_manifest.md`，不得批量分章翻译。
- 未建立 `qa/textual/textual_uncertainty_log.md` 或明确说明无文本不确定项，不得进入最终输出。
- 未完成古希腊文源语言干扰研究和术语策略，不得批量翻译。
- 第二语言参考译本版权和使用边界不清楚，不得使用。
- 如果启用古典科学 profile，未通过术语锁定、技术审计和图表/表格审计，不得进入最终输出。
- 第一版全书 EPUB 后未完成分层随机抽检，不得进入最终输出。
- 表格、图片、公式、图注或注释实际存在时，不得只抽正文段落后宣布抽检通过。
- `npm run review:random-validate:pass` 未通过，不得标记 `DONE`。
- 未创建 `output/release/book_vX.X.X.epub`，或 `output/release/release_state.json.latest_status` 不是 `PASS`，不得标记 `DONE`。
