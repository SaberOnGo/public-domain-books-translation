# 日语到简体中文 EPUB 公版书翻译制作模板 / Japanese to Simplified Chinese EPUB Translation Pipeline

## 目标 / Goal

给 AI 这个语言模板目录 `TEMPLATE_ROOT`、共享模板目录 `COMMON_TEMPLATE_ROOT`、目标工程目录 `PROJECT_ROOT` 和原书来源 `SOURCE_URL` 或私人本地书源，AI 应能自动完成：

1. 下载/读取日语公版或授权原文，优先使用可审计的纯文本、HTML 或扫描来源；若是非公版私人自用模式，则读取用户提供的本地书源。
2. 核查来源、版权、底本文字形态、现代校订成分、站点版权口径和使用边界。
3. 记录日语底本的旧字体/新字体、历史假名遣、振假名、注记、分段、异体字和 OCR 状态。
4. 清洗、分章，并保留可追溯的原文证据。
5. 完成通用翻译研究、日语专项研究、本书专项研究、文体画像和预翻译试译。
6. 生成术语表、专名表、称谓/敬语策略、官能或心理描写边界和译注策略。
7. 分章翻译、每章节译后控制、忠实度审校、可读性审校、术语审校、意象词审计和章节门禁。
8. 预制作阶段 1：封面、书籍信息、作者信息、字体、排版、标题、metadata、版本说明等规格。
9. 预制作阶段 2：先生成样章 EPUB，检查通过后再制作全书。
10. 生成 `output/book.epub`。
11. 通过 EPUB 校验和出版文本 lint。
12. 第一版全书 EPUB 后强制执行分层随机抽检模块，抽样正文段落、表格、图片、公式/证明块、图注和注释。
13. 派生 2 个独立 Agent 做严格评审并评分。
14. 根据评审和分层随机抽检结果回退到任意前置阶段返工；返工后必须定点关闭旧问题并使用新 seed 复抽。
15. 随机抽检闭环通过后，公版或授权项目生成 `output/release/book_vX.X.X.epub`、`release_notes.md`、`release_state.json` 和 `release_index.md`；`private_use` 项目生成 `output/private_artifacts/{title}_private_vX.X.X.epub` 和私人产物记录。
16. 全阶段复审，总结经验教训，必要时递增模板版本。

目标不是“把日文换成中文”，而是产出来源清楚、文体判断明确、中文可读、有文学质感、EPUB 制作质量合格的简体中文正本书。

This template handles Japanese source-language issues for Simplified Chinese EPUB production. It complements the target-language framework under `template/epub_pipeline/targets/zh-Hans/quality_framework/`.

## 唯一必须输入 / Required Inputs

- `TEMPLATE_ROOT`：语言方向模板目录，即 `template/epub_pipeline/Japanese-to-Simplified-Chinese`。
- `COMMON_TEMPLATE_ROOT`：共享 EPUB 流水线目录，即 `template/epub_pipeline/common`。
- `PROJECT_ROOT`：复制模板后的具体书籍工程目录；如未提供，AI 必须用 `books/scripts/create_book_project.py` 自动创建。
- `SOURCE_URL`：日语公版或授权来源 URL，例如青空文库、国立国会图书馆数字馆藏、Wikisource、Internet Archive 或其他可核查来源。
- `LOCAL_SOURCE_FILE`：可选，仅用于 `publication_mode=private_use` 的用户本地书源文件。

可选输入：

- `REFERENCE_URLS`：可核查的公版参考资料、作者年谱、初出信息或现代研究目录。现代中文译本不得作为翻译底本或隐藏参考材料。
- `TEXT_FORM_POLICY`：用户对旧字体、历史假名遣、振假名、专名译名或译注密度的明确要求。

## 模板保护 / Template Protection

严禁直接在模板原目录中制作具体书籍。执行任何书籍项目前，AI 必须先把 `template/epub_pipeline/common` 与 `template/epub_pipeline/Japanese-to-Simplified-Chinese` 合并复制到独立书籍工程目录，例如：

`books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`

之后所有抓取、研究、翻译、QA、EPUB 输出都只能写入新书籍工程目录。

如果用户只给了语言模板目录和 `SOURCE_URL`，AI 的第一步必须定位对应的 `COMMON_TEMPLATE_ROOT`，然后用 `books/scripts/create_book_project.py` 创建独立工程目录并自动分配数字前缀；不得把某本书的数据写回模板目录。若用户提供本地书源并声明个人自用、不传播、不商业使用，必须使用 `--mode private-use` 创建到被 Git 忽略的 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/`，并最后叠加 `template/epub_pipeline/modes/private_use/` 覆盖层。

Node.js 工具依赖不随每本书重复安装。先在 `books/` 目录运行 `npm install`，再进入具体书籍目录运行 `npm run lint:publication`、`npm run build:epub`、`npm run check:epub`。本模板的 `package.json` 只提供本书脚本，依赖统一来自共享的 `books/node_modules/`。

## 日语专项规则 / Japanese Rules

- 原文必须以日语公版底本为准；现代中文译本、出版社校注本、现代注释和现代译文不能作为翻译来源。
- 必须记录作者生卒年、初出/出版年份、来源站点版权口径，以及中国、日本、美国和常见 life+70 地区的初步版权风险。
- 必须说明所用文本是旧字体、现代字体、历史假名遣、现代假名遣、带振假名文本、扫描 OCR，还是人工校订文本。
- 振假名、旁注、编者注、底本注、校订者说明必须分清；不得把现代校订说明误当作者正文。
- 日语省主语、省宾语、敬语、称谓、视角转换、句末语气和暧昧心理描写，必须转成自然中文，同时保留叙述的不确定性。
- 官能、暴力、病态心理、权力关系或性别压迫题材不得被色情化、猎奇化或道德说教化；译文只呈现原作的叙述力度和文学判断。
- 人名、地名、作品名、时代词、衣物器物、佛教/艺道/江户或明治大正语境词必须建立统一译名和译注边界。
- 日语汉字词不能因为“看得懂”就照搬；必须判断现代中文语义是否漂移。

## 必读参考文件 / Required References

- `references/translation_research_universal.md`
- `references/quality_standard.md`
- `references/japanese_source_notes.md`
- `references/japanese_title_strategy.md`
- `references/japanese_to_chinese_literary_refinement.md`
- `template/epub_pipeline/targets/zh-Hans/quality_framework/README.md`
- `template/epub_pipeline/common/references/quality_gate_framework.md`
- `template/epub_pipeline/common/references/cover_design_policy.md`
- `template/epub_pipeline/common/references/book_info_frontmatter_policy.md`
- `template/epub_pipeline/common/references/epub_assets_figures_tables.md`
- `template/epub_pipeline/common/references/release_versioning.md`

## 关键产物 / Key Records

- `metadata/source_evidence.md`：公版来源、获取日期、来源版本、文本权利证据。
- `metadata/rights_checklist.md`：作者生卒年、初出/出版年份、来源站点口径、地域版权风险。
- `metadata/japanese_source_profile.md`：底本文字形态、假名遣、振假名、注记、OCR/校订状态。
- `metadata/book_specific_translation_research.md`：本书作者、时代、题材、文体、叙述策略和敏感题材边界。
- `metadata/style_profile.md`：中文文体画像。
- `glossary/terms.csv`：日语原词、假名/罗马字（必要时）、中文译名、说明、首次出现策略。
- `qa/textual/japanese_textual_notes.md`：旧字、异体字、振假名、注记、OCR 或版本疑难。
- `qa/pretranslation/pretranslation_report.md`：预翻译试译报告。
- `qa/chapter_controls/{NNN_slug}.control.md`：每章译后控制。
- `qa/gates/{NNN_slug}.gate.md`：章节最终门禁。

## 人类可选干预点 / Optional Human Checkpoints

原则上 AI 自动执行。复制到书籍工程后的 `state/human_feedback_control.md` 的 `human_required` 决定是否必须停下等人类检查。

建议人类可选查看：

- `metadata/source_evidence.md`
- `metadata/rights_checklist.md`
- `metadata/japanese_source_profile.md`
- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `glossary/terms.csv`
- `qa/textual/japanese_textual_notes.md`
- `qa/pretranslation/pretranslation_report.md`
- `qa/chapter_controls/{NNN_slug}.control.md`
- `preproduction/stage1/production_spec.md`
- `preproduction/stage2_sample/sample_book.epub`
- `reviews/random_spotcheck/round_XXX/`
- `output/release/`：公版或授权项目的版本化发布目录。
- `output/private_artifacts/`：`private_use` 项目的本地私人产物目录。
- `reviews/scorecards/final_quality_score.md`

如果无人干预，AI 只有在报告明确 `PASS` 时才可继续；若 `FAIL`，必须按回溯规则自行修正，不能跳过。

## 执行顺序 / Execution Order

1. `prompts/00_orchestrator_zh_ja.md`
2. `prompts/01_ingest_clean_zh_ja.md`
3. `prompts/02_split_zh_ja.md`
4. `prompts/03_global_translation_research_zh_ja.md`
5. `prompts/04_book_specific_research_zh_ja.md`
6. `prompts/05_pretranslation_trials_zh_ja.md`
7. `prompts/06_glossary_style_zh_ja.md`
8. `prompts/07_translate_chapters_zh_ja.md`
9. `prompts/08a_chapter_post_translation_control_zh_ja.md`
10. `prompts/08_review_fidelity_zh_ja.md`
11. `prompts/09_review_readability_imagery_zh_ja.md`
12. `prompts/10_review_terminology_zh_ja.md`
13. `prompts/11_chapter_quality_gate_zh_ja.md`
14. `prompts/13_preproduction_stage1_spec_zh_ja.md`
15. `prompts/14_preproduction_stage2_sample_zh_ja.md`
16. `prompts/15_full_book_production_zh_ja.md`
17. `prompts/16a_stratified_random_spotcheck.md`
18. `prompts/16_independent_review_agents_zh_ja.md`
19. `prompts/17_revision_routing_zh_ja.md`
20. `prompts/18a_release_versioning.md`
21. `prompts/18_final_output_zh_ja.md`
22. `prompts/19_retrospective_template_update_zh_ja.md`

## 硬门禁 / Hard Gates

- 公开项目没有日语公版或授权来源证据，不得翻译；私人自用项目没有本地书源文件和 `metadata/private_use_declaration.md`，不得翻译。
- 未记录底本文字形态、来源版本和版权风险，不得预翻译。
- 现代中文译本或现代出版社校注材料的版权和使用边界不清楚，不得使用。
- 未建立 `metadata/japanese_source_profile.md`，不得批量分章翻译。
- 未建立 `qa/textual/japanese_textual_notes.md` 或明确说明无文本疑难，不得进入最终输出。
- 未完成日语源语言干扰研究、术语策略和称谓/敬语策略，不得批量翻译。
- 涉及官能、暴力、病态心理或权力关系时，未写明文学处理边界，不得批量翻译。
- 第一版全书 EPUB 后未完成分层随机抽检，不得进入最终输出。
- `npm run review:random-validate:pass` 未通过，不得标记 `DONE`。
- 公版或授权项目未创建 `output/release/book_vX.X.X.epub`，或 `output/release/release_state.json.latest_status` 不是 `PASS`，不得标记 `DONE`。
- `private_use` 项目未创建 `output/private_artifacts/{title}_private_vX.X.X.epub`，或 `output/private_artifacts/private_artifact_state.json.latest_status` 不是 `PASS`，不得标记 `DONE`。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.
