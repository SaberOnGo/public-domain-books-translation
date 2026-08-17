# EPUB Pipeline Templates

This directory separates shared EPUB production infrastructure from language-pair-specific translation rules.

## Layout

- `common/`: language-neutral EPUB workflow contracts, source and rights templates, state files, preproduction templates, post-EPUB stratified random spot-check module, versioned release module, scripts, and build/check helpers.
- `common/assets/`: default directories for EPUB figures, images, styles, and table resources that must be copied into each book project.
- `targets/{target}/`: target-language quality frameworks, typography expectations, punctuation rules, and reader-experience standards.
- `{language-pair-template}/`: language-pair-specific translation prompts, glossary/style guidance, target-language metadata examples, source-language interference rules, and review scorecards.
- `profiles/{profile-target}/`: optional book-type production-control overlays for special risk classes, such as classical scientific texts with mathematics, astronomy, diagrams, tables, and strict terminology consistency requirements.
- `modes/private_use/`: mode overlay copied only for non-public-domain personal-use projects. It separates private-use cover, frontmatter, artifact, and gate scripts from public publication rules.

## Creating a Book Project

For a new book project, read the matching target-language framework when it exists, then create the project with `books/scripts/create_book_project.py`. The script copies `common/` first, overlays the matching language-pair template, and assigns the next numeric directory under the target language:

`books/{target}/{number}_{target_language_title}_{target_language_author}/`

The directory name after the numeric prefix must be readable in the target language. For `zh-Hans`, use Simplified Chinese title and author; for `ja`, use Japanese title and author; for `en`, use English title and author.

Example:

```powershell
cd books
npm run new:book -- "天文学大成_托勒密" --source-target Ancient-Greek-to-Simplified-Chinese
```

If the book belongs to a special profile, overlay the matching `profiles/{profile-target}/` template after the language-pair template. Private-use projects then overlay `modes/private_use/` last. For example, a Greek-to-Simplified-Chinese edition of a classical astronomy text should use:

1. `template/epub_pipeline/common`
2. `template/epub_pipeline/{language-pair-template}` such as `Ancient-Greek-to-Simplified-Chinese` when available
3. `template/epub_pipeline/profiles/classical-science-zh-Hans`

For non-public-domain private-use projects, append:

4. `template/epub_pipeline/modes/private_use`

All source text, translations, QA files, and EPUB output belong in the book project, never in `template/`.

### Bilingual Parallel Editions / 双语对照版

`edition_type: bilingual_parallel` is a first-class reader edition, not a lint exception or source-language residue. `English-to-Simplified-Chinese` projects default to both `output/book.epub` and `output/book_bilingual_parallel.epub`; this is independent from `publication_mode` and does not make English-to-Simplified-Chinese the repository's default translation direction.

`edition_type: bilingual_parallel` 是正式读者版本，不是 lint 例外，也不是源语残留。`English-to-Simplified-Chinese` 项目默认同时输出 `output/book.epub` 和 `output/book_bilingual_parallel.epub`；这与 `publication_mode` 解耦，也不代表仓库把英译简中作为默认翻译方向。

Other language pairs produce a bilingual parallel EPUB only when the user explicitly requests: `请输出 edition_type: bilingual_parallel，同时生成目标语言版 EPUB 和源语言-目标语言双语对照版 EPUB。`

其他语言方向只有用户明确要求时才输出双语对照 EPUB：`请输出 edition_type: bilingual_parallel，同时生成目标语言版 EPUB 和源语言-目标语言双语对照版 EPUB。`

Read `common/references/bilingual_parallel_edition_policy.md` before changing bilingual layout, production specs, quality gates, or release behavior.

Read `common/references/adaptive_parallel_orchestration.md` before changing worker concurrency, chapter ownership, audit roles, capability detection, or merge scheduling.

Read `common/references/ai_parallel_execution_guidance.md` before an AI dispatches translation or audit workers. It defines provider-neutral `MUST`/`SHOULD`/`MAY` behavior, the GPT worker-model default, and the boundary that LifeBook does not implement a runtime task queue.

修改双语排版、制作规格、质量门禁或 release 行为前，必须读取 `common/references/bilingual_parallel_edition_policy.md`。

修改 worker 并发、章节所有权、审核角色、能力检测或合并调度前，必须读取 `common/references/adaptive_parallel_orchestration.md`。

AI 派生翻译或审计 worker 前，必须读取 `common/references/ai_parallel_execution_guidance.md`。该文件定义通用的 `MUST`/`SHOULD`/`MAY` 行为、GPT worker 模型默认规则，以及 LifeBook 不实现运行时任务队列的边界。

### Private-Use Projects / 私人自用工程

Public-domain or licensed projects use the normal publishable tree above. A non-public-domain book may be translated only as a strictly private-use project when the user provides a local source file and explicitly declares personal study only, no redistribution, and no commercial use.

公版或授权项目使用上面的可发布目录。非公版书只有在用户提供本地书源文件，并明确声明仅供个人学习自用、不传播、不商业使用时，才可以作为严格私人自用工程翻译。

Private-use projects must be created with:

```powershell
cd books
npm run new:book -- "{target_language_title}_{target_language_author}" --source-target {language-pair-template} --mode private-use --local-source-file "{path_to_local_ebook}" --private-use-declaration "Personal study only; no redistribution; no commercial use."
```

The script writes private projects under `books/private/{target}/{number}_{target_language_title}_{target_language_author}/` and overlays `template/epub_pipeline/modes/private_use/` after the common, language-pair, and profile layers. That tree is ignored by Git. Scripts, templates, and configuration may be published to GitHub, but private source text, translations, QA files, EPUB output, private artifacts, and book-specific metadata under `books/private/` must not be published.

脚本会把私人项目写入 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/`，并在 common、语言方向和 profile 层之后叠加 `template/epub_pipeline/modes/private_use/`。该目录被 Git 忽略。脚本、模板和配置可以发布到 GitHub，但 `books/private/` 下的私人原文、译文、QA、EPUB 输出、私人产物和具体书籍 metadata 不得发布。

Private-use cover and frontmatter rules are mode-specific. The cover must not show public-domain source claims or long rights disclaimers; the book-info/frontmatter producer line is `参考public-domain-books-translation 开源项目 个人自制`; public-domain notices and public license wording must be removed. Versioned private artifacts are created with:

```powershell
npm run private:artifact:create
```

They are written to `output/private_artifacts/` and are not public releases.

Shared Node.js build dependencies belong at `books/`, not inside every book project. Run `npm install` once from `books/`; book-local scripts must find shared tools by walking up to `books/node_modules/`, because book projects may now be nested under `books/{target}/`.

Markdown chapters are authoring sources only. During EPUB production, final chapters must be converted to XHTML, images/SVG/CSS/table resources must be copied into the EPUB package, and every used resource must be declared in OPF manifest. See `common/references/epub_assets_figures_tables.md`.

After the first full-book EPUB is generated, every book project must run the stratified random spot-check module in `common/references/stratified_random_spotcheck.md` and `common/prompts/16a_stratified_random_spotcheck.md`. The module samples reader-visible audit units, including paragraphs, tables, figures, formulas/proof blocks, captions, and notes, and writes human-checkable rounds under `books/{target}/{number}_{target_language_title}_{target_language_author}/reviews/random_spotcheck/round_XXX/`.

Every executor must generate new spot-check rounds for the current run. Earlier PASS rounds from previous agents, previous releases, or previous private artifacts are audit history only; they do not count toward the current run's final PASS requirement. The user may specify any current-run consecutive PASS requirement of `>=1`; when the user does not specify it, the default is 2 latest consecutive PASS rounds under the same `review_run_id`.

每个执行中的 AI 必须为当前运行生成新的抽检轮次。之前 Agent、之前 release 或之前 private artifact 已经 PASS 的轮次只能作为历史审计记录，不能计入本次运行的最终 PASS 条件。用户可以指定任意 `>=1` 的当前运行连续 PASS 轮次要求；用户未指定时，默认要求同一 `review_run_id` 下最新连续 2 轮 PASS。

If any random sample exposes a defect, the executor must treat it as a possible defect family: audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in that round's `fix_log.md` and `closure_check.md` before running a new-seed resample. 抽检发现问题时，不得只修被抽中的样本；必须先归纳问题族，再做全书同类问题审计和闭环。

For translation-quality defect families, also use `skills/translation-quality-defect-families/SKILL.md`. Record book-specific evidence in the book project, then backfill only reusable lessons into that skill: how the family was found, how it was classified, how similar cases were audited, how confirmed matches were fixed, and how the fix was rechecked. 译文质量问题族还必须使用 `skills/translation-quality-defect-families/SKILL.md`：具体证据留在书籍工程内，可复用经验回填到该 skill，且只写有效归纳，不盲目重复追加。

After the random spot-check gate is closed, public-domain and licensed book projects must run the versioned release module in `common/references/release_versioning.md` and `common/prompts/18a_release_versioning.md`. The release artifact must be saved under `books/{target}/{number}_{target_language_title}_{target_language_author}/output/release/`; `output/book.epub` alone is not a publishable final artifact. Private-use projects instead run the private artifact module from `modes/private_use/` and write local-only artifacts under `output/private_artifacts/`.

## Naming

Language-pair directories use readable English direction names:

- `English-to-Simplified-Chinese`: English to Simplified Chinese.
- `Ancient-Greek-to-Simplified-Chinese`: Ancient Greek to Simplified Chinese.
- `Japanese-to-Simplified-Chinese`: Japanese to Simplified Chinese.
- `French-to-English`: French to English.
- `Japanese-to-Spanish`: Japanese to Spanish.
- `Traditional-Chinese-to-German`: Traditional Chinese to German.

Use `common/` for workflow pieces that should be shared by every language pair.

Use `targets/{target}/` for rules shared by multiple source languages that translate into the same target language. For example, `targets/zh-Hans/` applies to English to Simplified Chinese, French to Simplified Chinese, Japanese to Simplified Chinese, and other directions that produce Simplified Chinese.

Use `profiles/{profile-target}/` for rules shared by a book type across source languages. For example, `profiles/classical-science-zh-Hans/` applies to classical scientific, mathematical, astronomical, technical, or diagram-heavy public-domain works translated into Simplified Chinese, regardless of whether the original language is Greek, Latin, Arabic, German, French, or another language.

## Documentation Language

Important human-facing files in a language-pair template, including prompts, workflow instructions, quality gates, review rubrics, and policy notes, must include the local language that contributors for that template are expected to read.

English can be included in parallel as a bridge language for precision and international collaboration, but important template instructions should not be English-only when the target contributors are expected to work in another language.

Examples:

- `English-to-Japanese`: important prompts and review instructions should include Japanese, optionally paired with English.
- `French-to-English`: important prompts and review instructions should include English.
- `German-to-Traditional-Chinese`: important prompts and review instructions should include Traditional Chinese, optionally paired with English.

Shared repository-level documentation should include Chinese when it is intended for project-owner review. Bilingual Chinese-English wording is acceptable when exact terminology matters.

## Public Agent and Skill Files

Each language-pair template and each reusable profile should include public `AGENTS.md` and `SKILL.md` files so downloaded copies of the repository can be used directly by AI agents.

`AGENTS.md` should state mandatory behavior for the template or profile. `SKILL.md` should state when and how to run the workflow.

These files must follow the same language rule: local contributor language plus optional English as the bridge language. For example, `English-to-Japanese/AGENTS.md` and `English-to-Japanese/SKILL.md` should include Japanese, optionally paired with English.
