# 意大利语到简体中文 EPUB 公版书翻译制作模板 / Italian to Simplified Chinese EPUB Translation Pipeline

## 目标

给 AI 这个语言模板目录 `TEMPLATE_ROOT`、共享模板目录 `COMMON_TEMPLATE_ROOT`、目标工程目录 `PROJECT_ROOT` 和意大利语公版或授权来源 `SOURCE_URL` 后，AI 应能自动完成：

1. 下载或读取意大利语公版/授权原文。
2. 核查来源、版权、版本、OCR/转写状态和使用边界。
3. 记录意大利语底本形态、初版/所用版本、章节结构、注释和可能的现代编辑成分。
4. 清洗、分章，并保留可追溯的原文证据。
5. 完成通用翻译研究、意大利语专项研究、本书专项研究、文体画像和预翻译试译。
6. 生成术语表、专名表、译注策略和意大利语源语言干扰清单。
7. 分章翻译、每章译后控制、忠实度审校、可读性审校、术语审校、意象词审计和章节门禁。
8. 按公共模板完成预制作、封面、书籍信息页、EPUB 构建、EPUBCheck、分层随机抽检、独立评审和版本化 release。
9. 将制作过程中发现的可复用意大利语经验回填到本模板。

目标不是“把意大利语换成中文”，而是产出来源清楚、中文自然、有文学/叙事质感、术语稳定、EPUB 制作质量合格的简体中文正本书。

## 唯一必须输入

- `TEMPLATE_ROOT`：`template/epub_pipeline/it-zh-Hans`
- `COMMON_TEMPLATE_ROOT`：`template/epub_pipeline/common`
- `PROJECT_ROOT`：复制模板后的具体书籍工程目录；如未提供，AI 必须用 `books/scripts/create_book_project.py` 自动创建。
- `SOURCE_URL`：意大利语公版或授权来源 URL，例如 Wikisource、Internet Archive、Project Gutenberg、Liber Liber 或其他可核查来源。
- `LOCAL_SOURCE_FILE`：仅用于 `publication_mode=private_use` 的用户本地书源。

## 模板保护

严禁直接在模板原目录中制作具体书籍。执行任何书籍项目前，必须先把 `template/epub_pipeline/common` 与 `template/epub_pipeline/it-zh-Hans` 合并复制到独立书籍工程目录：

`books/zh-Hans/{number}_{book_id_slug}/`

如果启用 profile，则在语言方向模板之后叠加：

`common -> it-zh-Hans -> profiles/{profile-target} -> books/zh-Hans/{number}_{book_id_slug}/`

之后所有抓取、研究、翻译、QA、EPUB 输出都只能写入新书籍工程目录。

## 意大利语专项规则

- 原文以意大利语底本为准；现代英译、中文译本、百科介绍只能用于背景理解和事实核验。
- 必须记录作者生卒年、原书出版年份、所用来源页面权利口径，以及中国、美国和常见 life+70 地区初步版权风险。
- 必须说明来源是人工校对文本、HTML、纯文本、扫描 OCR、TEI/XML 还是影印；未校 OCR 不能直接作为可靠底本。
- 冒险小说、殖民时代小说和海事文本必须建立地名、人名、船名、头衔、民族称谓、宗教称谓、殖民机构和武器/航海词表。
- 意大利语长句必须先拆逻辑：主句、插入语、关系从句、分词结构、递进/让步/因果，再转为中文句群。
- 感叹、排比、动作连串和对话称谓必须按中文读者节奏重组，不得变成流水账。

## 执行顺序

1. `prompts/00_orchestrator_zh_it.md`
2. `prompts/01_ingest_clean_zh_it.md`
3. `prompts/02_split_zh_it.md`
4. `prompts/03_global_translation_research_zh_it.md`
5. `prompts/04_book_specific_research_zh_it.md`
6. `prompts/05_pretranslation_trials_zh_it.md`
7. `prompts/06_glossary_style_zh_it.md`
8. `prompts/07_translate_chapters_zh_it.md`
9. `prompts/08a_chapter_post_translation_control_zh_it.md`
10. `prompts/08_review_fidelity_zh_it.md`
11. `prompts/09_review_readability_imagery_zh_it.md`
12. `prompts/10_review_terminology_zh_it.md`
13. `prompts/11_chapter_quality_gate_zh_it.md`
14. `prompts/13_preproduction_stage1_spec_zh_it.md`
15. `prompts/14_preproduction_stage2_sample_zh_it.md`
16. `prompts/15_full_book_production_zh_it.md`
17. `prompts/16a_stratified_random_spotcheck.md`
18. `prompts/16_independent_review_agents_zh_it.md`
19. `prompts/17_revision_routing_zh_it.md`
20. `prompts/18a_release_versioning.md`
21. `prompts/18_final_output_zh_it.md`
22. `prompts/19_retrospective_template_update_zh_it.md`

## 硬门禁

- 公开项目没有意大利语公版或授权来源证据，不得翻译。
- 未记录底本版本、来源形态和版权风险，不得预翻译。
- OCR/转写未经说明，不得作为可靠正文批量翻译。
- 未完成意大利语源语言干扰研究、术语策略和预翻译试译，不得批量分章翻译。
- 每章译后 control 最近一轮不是全章零问题 PASS 时，不得进入下一章或 `chapters/final/`。
- 第一版全书 EPUB 后未完成分层随机抽检，不得进入最终输出。
- `npm run review:random-validate:pass` 未通过，不得标记 `DONE`。
- 公版或授权项目未创建 `output/release/{目标语言书名}_vX.X.X.epub`，或 `release_state.json.latest_status` 不是 `PASS`，不得标记 `DONE`。
