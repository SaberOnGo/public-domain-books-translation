---
name: public-domain-epub-pipeline
description: Use when creating, reviewing, or maintaining public-domain book translation projects and EPUB pipeline templates in this repository. Follow multilingual, language-pair-specific, rights-aware workflow rules.
---

# Public-Domain EPUB Pipeline Skill / 公版书 EPUB 流水线 Skill

Use this skill when an AI agent is asked to create a book project, add or update a language-pair template, revise prompts, review policy documents, or build EPUB output in this repository.

当 AI agent 被要求创建书籍工程、新增或更新语言方向模板、修改 prompt、审查政策文档或构建 EPUB 时，使用本 skill。

## Core Workflow / 核心流程

1. Read `AGENTS.md`.
   先读取 `AGENTS.md`。
2. Before doing any repository task, read the relevant `template/` files. The template is the source of truth; do not rely on memory or prior runs.
   执行任何仓库任务前，必须读取相关 `template/` 文件。模板是规则源，不得依赖记忆或历史执行经验。
3. Read the repository README in the user's preferred language when available.
   优先读取用户偏好语言对应的 README。
4. Read `template/epub_pipeline/README.md`.
   读取 `template/epub_pipeline/README.md`。
5. For EPUB production, cover, book-info/frontmatter, assets, quality gates, random review, or release work, read the applicable common policy files before editing or building:
   - `template/epub_pipeline/common/README.md`
   - `template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md`
   - `template/epub_pipeline/common/references/cover_design_policy.md`
   - `template/epub_pipeline/common/references/book_info_frontmatter_policy.md`
   - `template/epub_pipeline/common/references/epub_assets_figures_tables.md`
   - `template/epub_pipeline/common/references/quality_gate_framework.md`
   - `template/epub_pipeline/common/references/release_versioning.md`
   涉及 EPUB 制作、封面、书籍信息页/前置页、资产、质量门禁、随机评审或发布时，编辑或构建前必须读取适用的 common policy 文件：
   - `template/epub_pipeline/common/README.md`
   - `template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md`
   - `template/epub_pipeline/common/references/cover_design_policy.md`
   - `template/epub_pipeline/common/references/book_info_frontmatter_policy.md`
   - `template/epub_pipeline/common/references/epub_assets_figures_tables.md`
   - `template/epub_pipeline/common/references/quality_gate_framework.md`
   - `template/epub_pipeline/common/references/release_versioning.md`
6. Select the matching language-pair template, for example `fr-en`, `ja-es`, `en-zh-Hans`, or `zh-Hant-de`.
   选择匹配的语言方向模板，例如 `fr-en`、`ja-es`、`en-zh-Hans` 或 `zh-Hant-de`。
7. If a matching target-language framework exists under `template/epub_pipeline/targets/{target}/`, read it before translating.
   如果 `template/epub_pipeline/targets/{target}/` 下存在匹配的目标语言质量框架，翻译前必须读取。
8. Create the book project with `books/scripts/create_book_project.py`; it copies `template/epub_pipeline/common` into `books/{target}/{number}_{book_id_slug}/`, then overlays the matching language-pair template.
   使用 `books/scripts/create_book_project.py` 创建书籍工程；脚本会把 `template/epub_pipeline/common` 复制到 `books/{target}/{number}_{book_id_slug}/`，再覆盖复制匹配的语言方向模板。
9. Write all book-specific source text, translations, QA, EPUB output, and metadata only inside the book project.
   所有具体书籍的原文、译文、QA、EPUB 输出和 metadata 只能写入书籍工程目录。
10. Run the workflow through source evidence, rights checks, research, trial translation, chapter translation, review, gates, EPUB production, validation, mandatory post-EPUB stratified random spot-check, independent review, versioned release, and retrospective.
   按来源证据、版权核查、研究、试译、章节翻译、审校、门禁、EPUB 制作、校验、EPUB 后强制分层随机抽检、独立评审、版本化发布和复盘流程执行。
11. Before EPUB production, run `node scripts/publication_lint.js --target={target-language} --write-report` inside the book project and fix all hard errors.
   EPUB 制作前，必须在书籍工程内运行 `node scripts/publication_lint.js --target={target-language} --write-report`，并修复所有硬错误。
12. Before final EPUB output, check long chapter titles against `references/chapter_title_policy.md` and any matching source-to-target title strategy. EPUB navigation must use concise labels, not printed-TOC title chains.
    最终 EPUB 输出前，必须按 `references/chapter_title_policy.md` 及对应语言方向标题策略检查长章节标题。EPUB 目录应使用短题名，不应塞入纸书目录式标题链。
13. After the first full-book EPUB is built, run the stratified random spot-check module from `references/stratified_random_spotcheck.md` and `prompts/16a_stratified_random_spotcheck.md`. Use deterministic scripts, keep all samples and evidence under `books/{target}/{number}_{book_id_slug}/reviews/random_spotcheck/round_XXX/`, close every discovered P0/P1/P2, and run `npm run review:random-validate:pass` before final output.
    第一版全书 EPUB 生成后，必须执行 `references/stratified_random_spotcheck.md` 和 `prompts/16a_stratified_random_spotcheck.md` 定义的分层随机抽检模块。必须使用确定性脚本，所有样本和证据保存在 `books/{target}/{number}_{book_id_slug}/reviews/random_spotcheck/round_XXX/`，所有发现的 P0/P1/P2 必须关闭，最终输出前必须通过 `npm run review:random-validate:pass`。
    The current executor must generate new random spot-check rounds. Historical PASS rounds from previous agents, previous releases, or previous private artifacts do not count. The user may specify any current-run consecutive PASS requirement of `>=1`; when unspecified, the default validator requires the latest consecutive 2 PASS rounds from the same `review_run_id`.
    当前执行者必须生成新的随机抽检轮次。之前 Agent、之前 release 或之前 private artifact 已经 PASS 的历史轮次不得计入本次执行。用户可以指定任意 `>=1` 的当前运行连续 PASS 轮次要求；未指定时，默认强校验要求同一 `review_run_id` 下最新连续 2 轮 PASS。
14. After random spot-check closure, run the versioned release module from `references/release_versioning.md` and `prompts/18a_release_versioning.md`. Create `output/release/book_vX.X.X.epub`, `release_note_vX.X.X.md`, `release_state.json`, and `release_index.md`; `output/book.epub` alone is not enough for `DONE`.
    随机抽检闭环通过后，必须执行 `references/release_versioning.md` 和 `prompts/18a_release_versioning.md` 定义的版本化发布模块。必须创建 `output/release/book_vX.X.X.epub`、`release_note_vX.X.X.md`、`release_state.json` 和 `release_index.md`；只有 `output/book.epub` 不能标记 `DONE`。
15. For translated titles, title occurrences do not count as first body occurrences for terminology notes. Chapter titles, subtitles, and navigation titles must follow target-language title style; source names or parenthetical original names belong at the first natural body occurrence, in notes, or in the glossary.
    对译文标题而言，标题中的出现不计入术语译注的“正文首次出现”。章节标题、副标题和目录题名必须按目标语言标题习惯处理；原文名或括注原名应放在正文第一次自然出现处、译注或术语表中。
16. If a specific book has systematic refinement issues, place its goal under `books/{target}/{number}_{book_id_slug}/goal/`, then backfill reusable lessons into common, target-language, or source-target templates.
    如果某本书有系统性精修问题，目标文档应放在 `books/{target}/{number}_{book_id_slug}/goal/`，再把可复用经验回填到 common、目标语言或语言方向模板。
17. Put language-pair-specific scripts, datasets, and exploratory research under `research/{source-target}/...` or the matching language-pair template, not in the repository root.
   特定语言方向的脚本、数据集和探索性调研应放在 `research/{source-target}/...` 或对应语言方向模板中，不要放在仓库根目录。
18. Do not hard-code local absolute paths in scripts or prompts. Resolve paths from the script location, the repository root, or explicit user-provided arguments.
    不要在脚本或 prompt 中写死本机绝对路径。路径应基于脚本位置、仓库根目录或用户显式传入的参数解析。

## Policy Boundary Lessons / Policy 边界教训

- Read `cover_design_policy.md` and `book_info_frontmatter_policy.md` separately. Do not merge them from memory.
- 必须分别读取 `cover_design_policy.md` 与 `book_info_frontmatter_policy.md`，不得凭记忆把两者合并。
- Covers use the concise producer line `LifeBook 书坊 译制`. Personal contributor names belong in `book-info.xhtml` and metadata only when the book-info policy requires them.
- 封面使用简洁署名 `LifeBook 书坊 译制`。个人贡献者名只在书籍信息页 policy 要求时进入 `book-info.xhtml` 和 metadata。
- Before asset or publication lint, remove or rebuild stale staging output so old XHTML and old asset links cannot affect the new result.
- 运行资产检查或出版检查前，应清理或重新生成旧的 staging 输出，避免旧 XHTML 和旧资产链接影响新结果。

## Language Requirements / 语言要求

- Important human-facing files must include the local language for the intended contributors.
- 面向人的重要文件必须包含目标贡献者能读懂的本地语言。
- English may be included in parallel as a bridge language, but English-only important instructions are not acceptable unless English is the template's contributor language.
- 英文可以作为桥接语言并列出现，但除非英语就是该模板贡献者语言，否则重要说明不能只写英文。
- For `en-ja`, use Japanese plus optional English. For `de-zh-Hant`, use Traditional Chinese plus optional English. For `fr-en`, English is acceptable.
- `en-ja` 使用日文，可并列英文；`de-zh-Hant` 使用繁体中文，可并列英文；`fr-en` 可使用英文。
- Shared repository-level documentation should include Chinese when project-owner review is expected.
- 需要项目发起者审阅的共享仓库级文档应包含中文。

## Hard Stops / 必须停止的情况

- Rights or public-domain status is unclear.
- 版权或公版状态不清楚。
- The only available source is a modern copyrighted translation or unclear commercial EPUB.
- 唯一来源是现代受版权保护译本或来源不明的商业 EPUB。
- The current working directory is still under `template/` while book-specific output is about to be written.
- 当前目录仍在 `template/` 下，却准备写入具体书籍产物。
- A pretranslation report, chapter gate, EPUB validation, stratified random spot-check, closure validation, independent review, or PASS release gate fails.
- 预翻译报告、章节门禁、EPUB 校验、分层随机抽检、闭环校验、独立评审或 PASS 发布门禁失败。
- Publication lint reports hard errors such as mojibake, legacy print page-number tables, abnormal spacing, or target-language punctuation violations.
- 出版文本 lint 报出硬错误，例如乱码、旧纸书页码目录、异常空格或目标语言标点违规。
- Long printed-TOC chapter titles are still being used as EPUB navigation labels without title design.
- 旧纸书目录式长章节标题仍被直接用作 EPUB 目录题名，尚未完成标题设计。
- Source-language names or parenthetical originals appear in translated chapter titles, subtitles, or navigation labels where the target-language title should stand alone.
- 译文章节标题、副标题或目录题名中出现原文人名或原文括注，而目标语言标题本应独立呈现。

## Public Policy / 公开政策

- Non-code book content is publicly licensed under `CC BY-NC-SA 4.0` unless a file says otherwise.
- 非代码书籍内容默认按 `CC BY-NC-SA 4.0` 公开授权，除非文件另有说明。
- Third-party commercial use requires separate permission from LifeBook Shufang and relevant rights holders.
- 第三方商业使用必须另行取得 LifeBook 书坊及相关权利人的授权。
- Contributor rules are defined in `license/CONTRIBUTING*.md`.
- 贡献者规则见 `license/CONTRIBUTING*.md`。
