# 德语到简体中文 EPUB 公版书翻译制作模板 / German to Simplified Chinese EPUB Translation Pipeline

## 目标

给 AI 这个语言模板目录 `TEMPLATE_ROOT`、共享模板目录 `COMMON_TEMPLATE_ROOT`、目标工程目录 `PROJECT_ROOT` 和德语公版或授权来源 `SOURCE_URL` 后，AI 应能自动完成：

1. 下载或读取德语公版/授权原文。
2. 核查来源、版权、版本、OCR/转写状态和使用边界。
3. 记录德语底本形态、初版/所用版本、章节结构、注释和可能的现代编辑成分。
4. 清洗、分章，并保留可追溯的原文证据。
5. 完成通用翻译研究、德语专项研究、本书专项研究、文体画像和预翻译试译。
6. 生成术语表、专名表、译注策略和德语源语言干扰清单。
7. 分章翻译、每章节译后控制、忠实度审校、可读性审校、术语审校、意象词审计和章节门禁。
8. 按公共模板完成预制作、封面、书籍信息页、EPUB 构建、EPUBCheck、分层随机抽检、独立评审和版本化 release。
9. 将制作过程中发现的可复用德语经验回填到本模板。

目标不是“把德语换成中文”，而是产出来源清楚、中文自然、有文学/知识质感、术语稳定、EPUB 制作质量合格的简体中文正本书。

## 唯一必须输入

- `TEMPLATE_ROOT`：`template/epub_pipeline/German-to-Simplified-Chinese`
- `COMMON_TEMPLATE_ROOT`：`template/epub_pipeline/common`
- `PROJECT_ROOT`：复制模板后的具体书籍工程目录；如未提供，AI 必须用 `books/scripts/create_book_project.py` 自动创建。
- `SOURCE_URL`：德语公版或授权来源 URL，例如 Gutenberg-DE、Deutsches Textarchiv、Deutsche Digitale Bibliothek、Wikisource、Internet Archive 或其他可核查来源。
- `LOCAL_SOURCE_FILE`：仅用于 `publication_mode=private_use` 的用户本地书源。

## 模板保护

严禁直接在模板原目录中制作具体书籍。执行任何书籍项目前，必须先把 `template/epub_pipeline/common` 与 `template/epub_pipeline/German-to-Simplified-Chinese` 合并复制到独立书籍工程目录：

`books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`

如果启用 profile，则在语言方向模板之后叠加：

`common -> German-to-Simplified-Chinese -> profiles/{profile-target} -> books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`

之后所有抓取、研究、翻译、QA、EPUB 输出都只能写入新书籍工程目录。

## 德语专项规则

- 原文以德语底本为准；现代英译、中文译本、百科介绍只能用于背景理解和事实核验。
- 必须记录作者生卒年、原书出版年份、所用来源页面权利口径，以及中国、美国和常见 life+70 地区初步版权风险。
- 必须说明来源是人工校对文本、TEI/HTML、纯文本、扫描 OCR，还是 PDF 影印；未校 OCR 不能直接作为可靠底本。
- 德语长句必须先拆逻辑：谓语骨架、框架结构、插入语、关系从句、分词结构、递进/让步/因果，再转为中文句群。
- 德语复合词、长前置定语、可分动词、情态动词、否定作用域、虚拟式和被动态度必须按中文表达习惯重组。
- 科学技术、天文学、社会制度、殖民语境、身份称谓、专名和虚构文明设定必须建术语表和译注边界。

## 执行顺序

1. `prompts/00_orchestrator_zh_de.md`
2. `prompts/01_ingest_clean_zh_de.md`
3. `prompts/02_split_zh_de.md`
4. `prompts/03_global_translation_research_zh_de.md`
5. `prompts/04_book_specific_research_zh_de.md`
6. `prompts/05_pretranslation_trials_zh_de.md`
7. `prompts/06_glossary_style_zh_de.md`
8. `prompts/07_translate_chapters_zh_de.md`
9. `prompts/08a_chapter_post_translation_control_zh_de.md`
10. `prompts/08_review_fidelity_zh_de.md`
11. `prompts/09_review_readability_imagery_zh_de.md`
12. `prompts/10_review_terminology_zh_de.md`
13. `prompts/11_chapter_quality_gate_zh_de.md`
14. `prompts/13_preproduction_stage1_spec_zh_de.md`
15. `prompts/14_preproduction_stage2_sample_zh_de.md`
16. `prompts/15_full_book_production_zh_de.md`
17. `prompts/16a_stratified_random_spotcheck.md`
18. `prompts/16_independent_review_agents_zh_de.md`
19. `prompts/17_revision_routing_zh_de.md`
20. `prompts/18a_release_versioning.md`
21. `prompts/18_final_output_zh_de.md`
22. `prompts/19_retrospective_template_update_zh_de.md`

## 硬门禁

- 公开项目没有德语公版或授权来源证据，不得翻译。
- 未记录底本版本、来源形态和版权风险，不得预翻译。
- OCR/转写未经说明，不得作为可靠正文批量翻译。
- 未完成德语源语言干扰研究、术语策略和预翻译试译，不得批量分章翻译。
- 每章译后 control 最近一轮不是全章零问题 PASS 时，不得进入下一章或 `chapters/final/`。最近一轮必须记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true`；发现并修复问题的轮次只能记为 `FIXED_RECHECK_REQUIRED`，必须追加新的整章复查。
- 第一版全书 EPUB 后未完成分层随机抽检，不得进入最终输出。
- `npm run review:random-validate:pass` 未通过，不得标记 `DONE`。
- 公版或授权项目未创建 `output/release/{目标语言书名}_vX.X.X.epub`，或 `release_state.json.latest_status` 不是 `PASS`，不得标记 `DONE`。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.
