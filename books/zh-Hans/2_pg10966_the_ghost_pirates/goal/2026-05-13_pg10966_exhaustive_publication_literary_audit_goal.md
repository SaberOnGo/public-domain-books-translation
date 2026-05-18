# /goal: 《幽灵海盗》出版级二次总审与查漏补缺

created_at: 2026-05-13
status: IN_PROGRESS

## 目标

参考 `books/zh-Hans/1_pg20923_a_negro_explorer_at_the_north_pole` 的 EPUB 制作经验，以及 `template/epub_pipeline`、本书 `books/zh-Hans/2_pg10966_the_ghost_pirates` 的规则，对《幽灵海盗》做二次出版级总审。不得只因 EPUBCheck 通过就结束；必须覆盖标题工程、章节精修、术语/译注统一、长段落处理、重要段落与高潮段落的文学性、“信达雅”与专业细节。

## 必须读取或对照

- `AGENTS.md`
- `skills/public-domain-epub-pipeline/SKILL.md`
- `template/epub_pipeline/README.md`
- `template/epub_pipeline/common/references/chapter_title_policy.md`
- `template/epub_pipeline/en-zh-Hans/references/english_chapter_title_strategy.md`
- `template/epub_pipeline/en-zh-Hans/references/english_to_chinese_literary_refinement.md`
- `template/epub_pipeline/targets/zh-Hans/quality_framework/references/quality_standard.md`
- `books/zh-Hans/1_pg20923_a_negro_explorer_at_the_north_pole` 中标题工程、出版复核、EPUB 质量整改和精修 QA 记录
- 本书 `AGENTS.md`、`SKILL.md`、`metadata/`、`glossary/`、`qa/refinement/`、`output/final_manifest.md`

## 检查范围

1. 标题工程：目录题名、页面标题、源文标题是否一致；不得有英文原名括注、旧纸书标题链或 AI 自拟小题误入成书。
2. 章节首尾：不得有 Project Gutenberg 副文本、running title、重复标题、下一章标题残留。
3. 长段落：普通叙事段超过 300 字需复核，超过 500 字需判断是否拆分；诗歌/号子/名单等格式例外需说明。
4. 术语与译注：人名、船名、职务、航海索具、帆名、方位词和签名缩写需统一；普通名词不得随意正文括注英文。
5. 重要段落：首现黑影、测程绳盘、汤姆事故、威廉斯坠落、雾中绿光、雅各布斯高空崩溃、蓝火搜桅、雾船与海下船影、最终登船沉没、附录《寂静之船》。
6. 文学性与“信达雅”：准确不越界，中文可读有呼吸，恐怖感来自观察、迟疑和现场动作，不来自外加惊悚词。
7. EPUB 成品：重新运行 publication lint、refinement check、build、EPUBCheck、残留扫描和解包扫描。

## 交付物

- 新增 QA 报告：`qa/refinement/exhaustive_publication_literary_audit.md`
- 如发现实质缺口，修复 `chapters/final/`、`chapters/translated/`、`glossary/`、`metadata/` 或 QA 记录。
- 更新 `state/pipeline_state.json`、`output/final_manifest.md`。
- 重新输出 `output/book.epub` 与 `output/幽灵海盗.epub`。

## 退出条件

- 所有检查项有明确 PASS/修复记录。
- 旧残留和高风险词扫描为 0，或仅在 QA 报告中作为已修复项被列出并说明。
- EPUBCheck `fatal=0`、`error=0`、`warning=0`。
- `git diff --check` 通过。

