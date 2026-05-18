# 英文到简体中文 EPUB 公版书翻译制作模板 / English to Simplified Chinese EPUB Translation Pipeline

## 目标 / Goal

给 AI 这个语言模板目录 `TEMPLATE_ROOT`、共享模板目录 `COMMON_TEMPLATE_ROOT`、目标工程目录 `PROJECT_ROOT` 和原书来源 `SOURCE_URL`，AI 应能自动完成：

1. 下载/读取公版英文原文。
2. 核查来源与版权风险。
3. 清洗、分章。
4. 完成通用翻译研究、本书专项翻译研究、预翻译试译。
5. 生成术语表、文体画像、翻译规则。
6. 分章翻译、每章节译后控制、审校、意象词审计、章节门禁。
7. 预制作阶段 1：封面、书籍信息、作者信息、字体、排版、标题、metadata 等规格。
8. 预制作阶段 2：先生成样章 EPUB，检查通过后再制作全书。
9. 生成 `output/book.epub`。
10. 通过 EPUB 校验。
11. 第一版全书 EPUB 后强制执行分层随机抽检模块，抽样正文段落、表格、图片、公式/证明块、图注和注释。
12. 派生 2 个独立 Agent 做严格评审并评分。
13. 根据评审和分层随机抽检结果回退到任意前置阶段返工；返工后必须定点关闭旧问题并使用新 seed 复抽。
14. 随机抽检闭环通过后，生成 `output/release/book_vX.X.X.epub` 和中英文 `release_note_vX.X.X.md`。
15. 最终输出 EPUB。
16. 全阶段复审，总结经验教训，必要时递增模板版本。

目标不是“能翻出来”，而是产出优秀、可读、有中文生命力、EPUB 制作质量合格的正本书。

英文到简体中文的文学精修规则见 `references/english_to_chinese_literary_refinement.md`。如果某一本书发现系统性标题、段落、术语、译注、排版或文学精修问题，目标文档应放在该书工程的 `goal/` 目录下；可复用经验再分别回填到 common、zh-Hans 目标语言框架和 en-zh-Hans 语言方向模板。

Node.js 工具依赖不随每本书重复安装。先在 `books/` 目录运行 `npm install`，再进入具体书籍目录运行 `npm run lint:publication`、`npm run build:epub`、`npm run check:epub`。本模板的 `package.json` 只提供本书脚本，依赖统一来自共享的 `books/node_modules/`，脚本必须向上查找共享依赖，不能假定书籍目录直接位于 `books/` 下。

## 唯一必须输入 / Required Inputs

- `TEMPLATE_ROOT`：语言方向模板目录，即 `template/epub_pipeline/en-zh-Hans`。
- `COMMON_TEMPLATE_ROOT`：共享 EPUB 流水线目录，即 `template/epub_pipeline/common`。
- `PROJECT_ROOT`：复制模板后的具体书籍工程目录；如未提供，AI 必须用 `books/scripts/create_book_project.py` 自动创建。
- `SOURCE_URL`：原书来源 URL，例如 Project Gutenberg 页面或原文文本链接。

## 模板保护 / Template Protection

严禁直接在模板原目录中制作具体书籍。执行任何书籍项目前，AI 必须先把 `template/epub_pipeline/common` 与 `template/epub_pipeline/en-zh-Hans` 合并复制到独立书籍工程目录，例如：

`books/zh-Hans/{number}_{book_id_slug}/`

复制时若同名文件冲突，以语言方向模板为准。之后所有抓取、研究、翻译、QA、EPUB 输出都只能写入这个新目录。

如果用户只给了语言模板目录和 `SOURCE_URL`，AI 的第一步必须是定位对应的 `COMMON_TEMPLATE_ROOT`，然后用 `books/scripts/create_book_project.py` 创建独立工程目录并自动分配数字前缀；不得把某本书的数据写回模板目录。

## 人类可选干预点 / Optional Human Checkpoints

原则上 AI 自动执行。复制到书籍工程后的 `state/human_feedback_control.md` 的 `human_required` 决定是否必须停下等人类检查。

默认：`human_required=false`，AI 自动执行。

建议人类可选查看：

- `metadata/book_specific_translation_research.md`：本书专项翻译研究。
- `qa/pretranslation/pretranslation_report.md`：预翻译试译报告。
- `qa/chapter_controls/{NNN_slug}.control.md`：某章译后控制。
- `preproduction/stage1/production_spec.md`：全书制作规格。
- `preproduction/stage2_sample/sample_book.epub`：样章 EPUB。
- `reviews/random_spotcheck/round_XXX/`：分层随机抽检样本、证据、评审、修复和闭环记录。
- `output/release/`：带版本号的 EPUB、release note、release state 和发布索引。
- `reviews/scorecards/final_quality_score.md`：最终质量评分。

如果无人干预，AI 只有在报告明确 `PASS` 时才可继续；若 `FAIL`，必须按回溯规则自行修正，不能跳过。

## 新版执行顺序 / Execution Order

1. `prompts/00_orchestrator_zh_en.md`
2. `prompts/01_ingest_clean_zh_en.md`
3. `prompts/02_split_zh_en.md`
4. `prompts/03_global_translation_research_zh_en.md`
5. `prompts/04_book_specific_research_zh_en.md`
6. `prompts/05_pretranslation_trials_zh_en.md`
7. `prompts/06_glossary_style_zh_en.md`
8. `prompts/07_translate_chapters_zh_en.md`
9. `prompts/08a_chapter_post_translation_control_zh_en.md`
10. `prompts/08_review_fidelity_zh_en.md`
11. `prompts/09_review_readability_imagery_zh_en.md`
12. `prompts/10_review_terminology_zh_en.md`
13. `prompts/11_chapter_quality_gate_zh_en.md`
14. `prompts/13_preproduction_stage1_spec_zh_en.md`
15. `prompts/14_preproduction_stage2_sample_zh_en.md`
16. `prompts/15_full_book_production_zh_en.md`
17. `prompts/16a_stratified_random_spotcheck.md`
18. `prompts/16_independent_review_agents_zh_en.md`
19. `prompts/17_revision_routing_zh_en.md`
20. `prompts/18a_release_versioning.md`
21. `prompts/18_final_output_zh_en.md`
22. `prompts/19_retrospective_template_update_zh_en.md`

## 硬门禁 / Hard Gates

- 没有版权/公版来源核查，不得翻译。
- 未复制模板到独立书籍工程目录，不得开始抓取原文。
- 没有本书专项翻译研究，不得预翻译。
- 预翻译未 `PASS`，不得批量分章翻译。
- 每章译后控制未 `PASS`，不得进入章节审校。
- 章节没有意象词审计，不得进入 `chapters/final/`。
- 章节没有质量门禁 `PASS`，不得进入 `chapters/final/`。
- 未完成预制作阶段 1，不得制作样章。
- 样章未 `PASS`，不得制作全书 EPUB。
- EPUB 校验有 fatal/error，不得进入最终输出。
- 第一版全书 EPUB 后未完成分层随机抽检，不得进入最终输出。
- 表格、图片、公式、图注或注释实际存在时，不得只抽正文段落后宣布抽检通过。
- `npm run review:random-validate:pass` 未通过，不得标记 `DONE`。
- 未创建 `output/release/book_vX.X.X.epub`，或 `output/release/release_state.json.latest_status` 不是 `PASS`，不得标记 `DONE`。
- 未完成双 Agent 独立评审，不得宣布完成。
- 每轮精校后未完成双 Agent 分层随机抽检，不得宣布精校完成。
- 随机抽检中任一 Agent 平均分 < 75、任一单项 < 70，或指出读不懂、事实误解、英文句法硬搬、无依据润饰、术语/专名/译注/表格/图片/公式错误，必须回退精校或更早阶段。
- 评审未通过，必须回退返工。
- 未完成复盘和经验沉淀，不得标记 `DONE`。
- 已发现系统性精修问题但没有书籍专属 `goal/` 目标文档，不得标记 `DONE`。
- 已发现可复用经验但没有回填模板，不得标记 `DONE`。
