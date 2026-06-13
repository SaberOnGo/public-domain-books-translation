# 西班牙语到简体中文 EPUB 公版书翻译制作模板 / Spanish to Simplified Chinese EPUB Translation Pipeline

本模板用于把西班牙语公版或授权原文翻译成简体中文，并制作可发布 EPUB。它覆盖早期近代小说、流浪汉小说、黄金时代文学、旅行散文、戏剧和经典西语叙事。

给 AI 这个语言模板目录 `TEMPLATE_ROOT`、共享模板目录 `COMMON_TEMPLATE_ROOT`、目标工程目录 `PROJECT_ROOT` 和西班牙语公版或授权来源 `SOURCE_URL` 后，AI 应能自动完成：

1. 下载或读取西班牙语公版/授权原文。
2. 记录来源、版权、底本版本和文本形态。
3. 建立 `metadata/spanish_source_profile.md`、术语表、称谓策略、译注策略和章节标题映射。
4. 按 common 流水线完成研究、试译、分章翻译、每章全量复查、EPUB 构建、分层随机抽检和 release。
5. 将制作过程中发现的可复用西班牙语经验回填到本模板或共享 skills。

目标不是“把西班牙语换成中文”，而是产出来源清楚、中文自然、有叙述声音和讽刺质感、术语稳定、EPUB 制作质量合格的简体中文正本书。

## 变量

- `TEMPLATE_ROOT`：`template/epub_pipeline/Spanish-to-Simplified-Chinese`
- `COMMON_TEMPLATE_ROOT`：`template/epub_pipeline/common`
- `TARGET_FRAMEWORK_ROOT`：`template/epub_pipeline/targets/zh-Hans/quality_framework`
- `PROJECT_ROOT`：`books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}`
- `SOURCE_URL`：西班牙语公版或授权来源 URL，例如 Project Gutenberg、Wikisource、Biblioteca Virtual Miguel de Cervantes、Biblioteca Nacional de Espana、Internet Archive 或其他可核查来源。

## 工程创建

严禁直接在模板原目录中制作具体书籍。执行任何书籍项目前，必须先把 `template/epub_pipeline/common` 与 `template/epub_pipeline/Spanish-to-Simplified-Chinese` 合并复制到独立书籍工程目录：

```powershell
python books/scripts/create_book_project.py "{目标语言书名}_{目标语言作者名}" --source-target Spanish-to-Simplified-Chinese --source-url "{SOURCE_URL}"
```

复制顺序：

`common -> Spanish-to-Simplified-Chinese -> profiles/{profile-target} -> books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`

## 西班牙语专项规则

- 原文以西班牙语底本为准；现代英译、中文译本、百科介绍只能用于背景理解和事实核验。
- 早期近代西班牙语长句必须先拆逻辑：主句、插入语、关系从句、递进/让步/因果，再转为中文句群。
- 流浪汉小说和讽刺散文必须保留叙述者声音，不得翻成客观说明或现代心理分析。
- 宗教、法律、阶层、称谓、食物、货币、衣物和地名必须早期入术语表。
- 正文不默认保留西班牙语原词括注；需要原词时优先放入译注或术语表。

## Prompt 顺序

1. `prompts/00_orchestrator_zh_es.md`
2. `prompts/01_ingest_clean_zh_es.md`
3. `prompts/02_split_zh_es.md`
4. `prompts/03_global_translation_research_zh_es.md`
5. `prompts/04_book_specific_research_zh_es.md`
6. `prompts/05_pretranslation_trials_zh_es.md`
7. `prompts/06_glossary_style_zh_es.md`
8. `prompts/07_translate_chapters_zh_es.md`
9. `prompts/08a_chapter_post_translation_control_zh_es.md`
10. `prompts/08_review_fidelity_zh_es.md`
11. `prompts/09_review_readability_imagery_zh_es.md`
12. `prompts/10_review_terminology_zh_es.md`
13. `prompts/11_chapter_quality_gate_zh_es.md`
14. `prompts/13_preproduction_stage1_spec_zh_es.md`
15. `prompts/14_preproduction_stage2_sample_zh_es.md`
16. `prompts/15_full_book_production_zh_es.md`
17. `template/epub_pipeline/common/prompts/16a_stratified_random_spotcheck.md`
18. `prompts/16_independent_review_agents_zh_es.md`
19. `prompts/17_revision_routing_zh_es.md`
20. `template/epub_pipeline/common/prompts/18a_release_versioning.md`
21. `prompts/18_final_output_zh_es.md`
22. `prompts/19_retrospective_template_update_zh_es.md`

## 停止条件

- 公开项目没有西班牙语公版或授权来源证据，不得翻译。
- 只有现代受版权保护译本、盗版站或来源不明 EPUB 时停止。
- 未完成西班牙语源语言干扰研究、术语策略和预翻译试译，不得批量分章翻译。
- 每章译后全量检查未以零问题 PASS 关闭，不得进入下一章或终稿。
- 第一版 EPUB 后未完成分层随机抽检、问题族追杀和 `review:random-validate:pass`，不得 release。
