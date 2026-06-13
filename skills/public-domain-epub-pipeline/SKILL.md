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
11. For translation, chapter review, random spot-check, reader feedback, and final artifact review, use `skills/expert-translation-quality/SKILL.md` to enforce expert-level prose and downstream-context polysemy back-checking without bloating every prompt.
    翻译、章节审校、随机抽检、读者反馈和最终产物审阅时，使用 `skills/expert-translation-quality/SKILL.md`，把专家级译文与后文回看多义词复查作为执行流程，而不是把长规则塞进每个 prompt。
12. Before EPUB production, run `node scripts/publication_lint.js --target={target-language} --write-report` inside the book project and fix all hard errors.
   EPUB 制作前，必须在书籍工程内运行 `node scripts/publication_lint.js --target={target-language} --write-report`，并修复所有硬错误。
    Before a translated or final chapter can pass chapter controls or template preflight, also run the structural translation coverage gate: `npm run check:translation-coverage` or `python scripts/check_translation_coverage.py --write-report`. This gate compares `chapters/src/` against `chapters/translated/` and `chapters/final/` for severe paragraph-block shrinkage, chapter character shrinkage, lost footnote references, lost footnote definitions, and lost table/figure/formula units. A chapter control file that claims PASS cannot override this machine gate.
    已译章节或终稿章节通过章节控制或模板预检前，还必须运行结构性译文覆盖门禁：`npm run check:translation-coverage` 或 `python scripts/check_translation_coverage.py --write-report`。该门禁对比 `chapters/src/` 与 `chapters/translated/`、`chapters/final/`，拦截严重段落块缩水、章节字数异常缩水、脚注引用丢失、脚注定义丢失，以及表格/图片/公式单元丢失。章节 control 自称 PASS 不能覆盖这个机器门禁。
13. Before final EPUB output, check long chapter titles against `references/chapter_title_policy.md` and any matching source-to-target title strategy. EPUB navigation must use concise labels, not printed-TOC title chains.
    最终 EPUB 输出前，必须按 `references/chapter_title_policy.md` 及对应语言方向标题策略检查长章节标题。EPUB 目录应使用短题名，不应塞入纸书目录式标题链。
14. After the first full-book EPUB is built, run the stratified random spot-check module from `references/stratified_random_spotcheck.md` and `prompts/16a_stratified_random_spotcheck.md`. Use deterministic scripts, keep all samples and evidence under `books/{target}/{number}_{book_id_slug}/reviews/random_spotcheck/round_XXX/`, close every discovered P0/P1/P2, and run `npm run review:random-validate:pass` before final output.
    第一版全书 EPUB 生成后，必须执行 `references/stratified_random_spotcheck.md` 和 `prompts/16a_stratified_random_spotcheck.md` 定义的分层随机抽检模块。必须使用确定性脚本，所有样本和证据保存在 `books/{target}/{number}_{book_id_slug}/reviews/random_spotcheck/round_XXX/`，所有发现的 P0/P1/P2 必须关闭，最终输出前必须通过 `npm run review:random-validate:pass`。
    The current executor must generate new random spot-check rounds. Historical PASS rounds from previous agents, previous releases, or previous private artifacts do not count. The user may specify any current-run consecutive PASS requirement of `>=1`; when unspecified, the default validator requires the latest consecutive 2 PASS rounds from the same `review_run_id`.
    当前执行者必须生成新的随机抽检轮次。之前 Agent、之前 release 或之前 private artifact 已经 PASS 的历史轮次不得计入本次执行。用户可以指定任意 `>=1` 的当前运行连续 PASS 轮次要求；未指定时，默认强校验要求同一 `review_run_id` 下最新连续 2 轮 PASS。
15. After random spot-check closure, run the versioned release module from `references/release_versioning.md` and `prompts/18a_release_versioning.md`. Create `output/release/book_vX.X.X.epub`, `release_note_vX.X.X.md`, `release_state.json`, and `release_index.md`; `output/book.epub` alone is not enough for `DONE`.
    随机抽检闭环通过后，必须执行 `references/release_versioning.md` 和 `prompts/18a_release_versioning.md` 定义的版本化发布模块。必须创建 `output/release/book_vX.X.X.epub`、`release_note_vX.X.X.md`、`release_state.json` 和 `release_index.md`；只有 `output/book.epub` 不能标记 `DONE`。
16. For translated titles, title occurrences do not count as first body occurrences for terminology notes. Chapter titles, subtitles, and navigation titles must follow target-language title style; source names or parenthetical original names belong at the first natural body occurrence, in notes, or in the glossary.
    对译文标题而言，标题中的出现不计入术语译注的“正文首次出现”。章节标题、副标题和目录题名必须按目标语言标题习惯处理；原文名或括注原名应放在正文第一次自然出现处、译注或术语表中。
17. If a specific book has systematic refinement issues, place its goal under `books/{target}/{number}_{book_id_slug}/goal/`, then backfill reusable lessons into common, target-language, or source-target templates.
    如果某本书有系统性精修问题，目标文档应放在 `books/{target}/{number}_{book_id_slug}/goal/`，再把可复用经验回填到 common、目标语言或语言方向模板。
18. Put language-pair-specific scripts, datasets, and exploratory research under `research/{source-target}/...` or the matching language-pair template, not in the repository root.
   特定语言方向的脚本、数据集和探索性调研应放在 `research/{source-target}/...` 或对应语言方向模板中，不要放在仓库根目录。
19. Do not hard-code local absolute paths in scripts or prompts. Resolve paths from the script location, the repository root, or explicit user-provided arguments.
    不要在脚本或 prompt 中写死本机绝对路径。路径应基于脚本位置、仓库根目录或用户显式传入的参数解析。

## Policy Boundary Lessons / Policy 边界教训

- Read `cover_design_policy.md` and `book_info_frontmatter_policy.md` separately. Do not merge them from memory.
- 必须分别读取 `cover_design_policy.md` 与 `book_info_frontmatter_policy.md`，不得凭记忆把两者合并。
- Covers use the concise producer line `LifeBook 书坊 译制`. Personal contributor names belong in `book-info.xhtml` and metadata only when the book-info policy requires them.
- 封面使用简洁署名 `LifeBook 书坊 译制`。个人贡献者名只在书籍信息页 policy 要求时进入 `book-info.xhtml` 和 metadata。
- Before asset or publication lint, remove or rebuild stale staging output so old XHTML and old asset links cannot affect the new result.
- 运行资产检查或出版检查前，应清理或重新生成旧的 staging 输出，避免旧 XHTML 和旧资产链接影响新结果。

## Structural Translation Coverage / 结构性译文覆盖

- Treat large-chapter shrinkage and note loss as pipeline defects, not as model-style problems. The durable fix is a deterministic coverage gate, not a one-off prompt reminder.
  大章后段缩水和注释丢失应视为流水线缺陷，不是单纯模型风格问题。长期解决必须依靠确定性覆盖门禁，而不是一次性 prompt 提醒。
- `check_translation_coverage.py` is the shared gate. It checks matching chapter filenames across `chapters/src/`, `chapters/translated/`, and `chapters/final/`. It fails on low paragraph-block coverage, low non-space character coverage for long chapters, note reference/definition loss, unresolved target note references, and lost table/image/formula units.
  `check_translation_coverage.py` 是共享门禁。它按同名章节对比 `chapters/src/`、`chapters/translated/` 和 `chapters/final/`。若段落块覆盖率过低、长章非空白字符覆盖率过低、注释引用/定义丢失、译文注号没有定义，或表格/图片/公式单元丢失，必须失败。
- `preflight:template` and `check:chapter-controls` must include this gate. If an Agent writes a PASS chapter control while the coverage gate fails, the PASS is invalid and the chapter must return to translation or reconstruction before any EPUB build or release.
  `preflight:template` 和 `check:chapter-controls` 必须包含该门禁。若 Agent 写出 PASS 的章节 control，但覆盖门禁失败，该 PASS 无效；章节必须回到翻译或重组后才能进入 EPUB 构建或发布。
- For very long chapters, split translation work into stable paragraph or small-block units and keep notes with the relevant unit or a dedicated note unit. The final merge must not proceed until every unit and note definition has a target counterpart.
  对超长章节，应按稳定段落或小块单元翻译，并让注释跟随相关单元或独立注释单元。所有单元和注释定义都有对应译文前，不得合并为终稿。

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
