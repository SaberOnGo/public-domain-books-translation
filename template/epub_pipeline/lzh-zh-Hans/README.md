# 文言文到现代简体中文 EPUB 翻译制作模板 / Literary Chinese to Modern Simplified Chinese EPUB Translation Pipeline

## 目标 / Goal

给 AI 这个语言模板目录 `TEMPLATE_ROOT`、共享模板目录 `COMMON_TEMPLATE_ROOT`、目标工程目录 `PROJECT_ROOT` 和原书来源 `SOURCE_URL` 或私人本地书源，AI 应能自动完成：

1. 下载/读取文言文公版或授权底本；若是非公版私人自用模式，则读取用户提供的本地书源。
2. 核查来源、版权、版本、标点、断句、校注成分、OCR/转写状态和使用边界。
3. 记录底本、witness、章节/篇章编号、断句标点策略、异文、疑难读法和现代整理成分。
4. 清洗、分章，并保留可追溯的原文证据。
5. 完成文言文专项研究、本书历史/文化/制度背景研究、文体画像和预翻译试译。
6. 生成术语表、专名表、古今词义策略、译注策略和对照正文策略。
7. 分章翻译，每段默认输出“古文原文一段 + 现代中文今译一段”。
8. 完成章节译后控制、忠实度审校、可读性审校、术语/专名审校、注释审校和章节门禁。
9. 预制作阶段 1：封面、书籍信息、字体、排版、标题、metadata、版本说明等规格。
10. 预制作阶段 2：先生成样章 EPUB，检查通过后再制作全书。
11. 生成 `output/book.epub`。
12. 通过 EPUB 校验、出版文本 lint、读者可见内容门禁和资产门禁。
13. 第一版全书 EPUB 后执行分层随机抽检，抽样古文段、今译段、注释、表格、图片、图注和附录等读者可见审计单元。
14. 派生 2 个独立 Agent 严格评审；若发现 P0/P1/P2，必须修复、重建并用新 seed 复抽。
15. 随机抽检闭环通过后，公开项目生成 `output/release/` 版本化 EPUB；私人自用项目生成 `output/private_artifacts/` 本地产物。
16. 全阶段复盘，将试译和成书过程中发现的可复用规则回填到 common、`targets/zh-Hans`、`lzh-zh-Hans` 或相关 profile。

目标不是“把古文翻成白话大意”，而是产出底本清楚、今译可信、注释有用、能对照原文阅读、EPUB 制作质量合格的现代中文读者版。

This template handles Literary Chinese source-language issues for modern Simplified Chinese EPUB production. It complements the target-language framework under `template/epub_pipeline/targets/zh-Hans/quality_framework/`.

## 默认读者版形态 / Default Reader-Facing Form

文言文项目的默认 EPUB 正文不是只给现代译文，而是平行对照：

```html
<section class="parallel-passage" id="p001">
  <p class="source-text" lang="lzh">古文原文一段。</p>
  <p class="modern-text" lang="zh-Hans">现代中文译文一段。</p>
</section>
```

只有在索引、附录、纯表格、书籍信息页或经过记录的特殊编辑场景下，才允许例外。例外必须写入 `metadata/classical_chinese_source_profile.md` 或 `preproduction/stage1/production_spec.md`。

## 唯一必须输入 / Required Inputs

- `TEMPLATE_ROOT`：语言方向模板目录，即 `template/epub_pipeline/lzh-zh-Hans`。
- `COMMON_TEMPLATE_ROOT`：共享 EPUB 流水线目录，即 `template/epub_pipeline/common`。
- `PROJECT_ROOT`：复制模板后的具体书籍工程目录；如未提供，AI 必须用 `books/scripts/create_book_project.py` 自动创建。
- `SOURCE_URL`：文言文公版或授权来源 URL，例如 Wikisource、Project Gutenberg、Internet Archive、国家/大学图书馆公开馆藏或其他可核查来源。
- `LOCAL_SOURCE_FILE`：可选，仅用于 `publication_mode=private_use` 的用户本地书源文件。

可选输入：

- `PROFILE_ROOT`：特殊书型控制模板，例如 `template/epub_pipeline/profiles/classical-history-zh-Hans`。
- `REFERENCE_URLS`：可核查的公版注疏、异文资料、人物年表、历史地图或现代研究目录。现代版权校注本不得作为隐藏底本。

## 模板保护 / Template Protection

严禁直接在模板原目录中制作具体书籍。执行任何书籍项目前，AI 必须先把 `template/epub_pipeline/common` 与 `template/epub_pipeline/lzh-zh-Hans` 合并复制到独立书籍工程目录，例如：

`books/zh-Hans/{number}_{book_id_slug}/`

如果启用 profile，则在语言方向模板之后再覆盖复制 profile：

`common -> lzh-zh-Hans -> profiles/{profile-target} -> books/zh-Hans/{number}_{book_id_slug}/`

## 文言文专项规则 / Literary Chinese Rules

- 原文底本是翻译依据。现代白话译文、现代商业校注、百科条目和课堂讲义不能作为翻译底本。
- 必须记录底本是否有现代标点、现代分段、校注者说明、异体字整理、繁简转换、OCR 或转写成分。
- 断句和标点是翻译判断的一部分。疑难断句不得静默处理，必须记录。
- 古今词义差异、人称省略、宾语省略、使动/意动、被动、兼语、判断句、互文、借代、典故和外交辞令必须逐项判断。
- 今译应让现代中文读者读懂人物行为、因果、语气和策略，但不得把原文扩写成历史小说。
- 注释应服务阅读：解释必要背景、制度、专名、年代、地理、异文和校勘，不替读者做文学鉴赏结论。
- 章节标题、篇名和目录题名必须按 `references/classical_chinese_title_strategy.md` 处理；不得把长篇题解塞进 EPUB 目录。

## 建议叠加 profile / Recommended Profile

《战国策》《左传》《国语》《史记》列传等历史叙事、人物关系密集或制度背景密集文本，建议叠加：

`template/epub_pipeline/profiles/classical-history-zh-Hans`

该 profile 负责人物、国家、年代、官制、礼制、战争、外交、注释密度和历史关系审计。本模板负责文言文源语言到现代中文的语言转换。

## 执行顺序 / Execution Order

1. `prompts/00_orchestrator_zh_lzh.md`
2. `prompts/01_ingest_clean_zh_lzh.md`
3. `prompts/02_split_zh_lzh.md`
4. `prompts/03_global_translation_research_zh_lzh.md`
5. `prompts/04_book_specific_research_zh_lzh.md`
6. `prompts/05_pretranslation_trials_zh_lzh.md`
7. `prompts/06_glossary_style_zh_lzh.md`
8. `prompts/07_translate_chapters_zh_lzh.md`
9. `prompts/08a_chapter_post_translation_control_zh_lzh.md`
10. `prompts/08_review_fidelity_zh_lzh.md`
11. `prompts/09_review_readability_imagery_zh_lzh.md`
12. `prompts/10_review_terminology_zh_lzh.md`
13. `prompts/11_chapter_quality_gate_zh_lzh.md`
14. `prompts/13_preproduction_stage1_spec_zh_lzh.md`
15. `prompts/14_preproduction_stage2_sample_zh_lzh.md`
16. `prompts/15_full_book_production_zh_lzh.md`
17. `prompts/16a_stratified_random_spotcheck.md`
18. `prompts/16_independent_review_agents_zh_lzh.md`
19. `prompts/17_revision_routing_zh_lzh.md`
20. `prompts/18a_release_versioning.md`
21. `prompts/18_final_output_zh_lzh.md`
22. `prompts/19_retrospective_template_update_zh_lzh.md`

## 硬门禁 / Hard Gates

- 公开项目没有文言文公版或授权来源证据，不得翻译。
- 未记录底本、断句、标点、版本、异文和文本疑难，不得预翻译。
- 试译未覆盖对照正文、注释密度、疑难断句和人物/制度背景，不得批量翻译。
- 章节没有原文-今译对齐记录，不得进入 `chapters/final/`。
- 注释没有分层策略，或必要注释缺失导致现代读者会误解人物、制度、时间、地点、语气或事件，不得进入最终输出。
- 第一版全书 EPUB 后未完成分层随机抽检，不得进入最终输出。
- `npm run review:random-validate:pass` 未通过，不得标记 `DONE`。
