# EPUB Pipeline Templates

This directory separates shared EPUB production infrastructure from language-pair-specific translation rules.

## Layout

- `common/`: language-neutral EPUB workflow contracts, source and rights templates, state files, preproduction templates, scripts, and build/check helpers.
- `common/assets/`: default directories for EPUB figures, images, styles, and table resources that must be copied into each book project.
- `targets/{target}/`: target-language quality frameworks, typography expectations, punctuation rules, and reader-experience standards.
- `{source-target}/`: language-pair-specific translation prompts, glossary/style guidance, target-language metadata examples, source-language interference rules, and review scorecards.
- `profiles/{profile-target}/`: optional book-type production-control overlays for special risk classes, such as classical scientific texts with mathematics, astronomy, diagrams, tables, and strict terminology consistency requirements.

## Creating a Book Project

For a new book project, read the matching target-language framework when it exists, copy `common/` first, then overlay the matching language-pair template into:

`books/{book_id_slug}/`

If the book belongs to a special profile, overlay the matching `profiles/{profile-target}/` template after the language-pair template. For example, a Greek-to-Simplified-Chinese edition of a classical astronomy text should use:

1. `template/epub_pipeline/common`
2. `template/epub_pipeline/{source-target}` such as `grc-zh-Hans` when available
3. `template/epub_pipeline/profiles/classical-science-zh-Hans`

All source text, translations, QA files, and EPUB output belong in the book project, never in `template/`.

Shared Node.js build dependencies belong at `books/`, not inside every book project. Run `npm install` once from `books/`; book-local npm scripts should find shared tools through `../node_modules`.

Markdown chapters are authoring sources only. During EPUB production, final chapters must be converted to XHTML, images/SVG/CSS/table resources must be copied into the EPUB package, and every used resource must be declared in OPF manifest. See `common/references/epub_assets_figures_tables.md`.

## Naming

Language-pair directories use BCP 47-style direction names:

- `en-zh-Hans`: English to Simplified Chinese.
- `grc-zh-Hans`: Ancient Greek to Simplified Chinese.
- `fr-en`: French to English.
- `ja-es`: Japanese to Spanish.
- `zh-Hant-de`: Traditional Chinese to German.

Use `common/` for workflow pieces that should be shared by every language pair.

Use `targets/{target}/` for rules shared by multiple source languages that translate into the same target language. For example, `targets/zh-Hans/` applies to English to Simplified Chinese, French to Simplified Chinese, Japanese to Simplified Chinese, and other directions that produce Simplified Chinese.

Use `profiles/{profile-target}/` for rules shared by a book type across source languages. For example, `profiles/classical-science-zh-Hans/` applies to classical scientific, mathematical, astronomical, technical, or diagram-heavy public-domain works translated into Simplified Chinese, regardless of whether the original language is Greek, Latin, Arabic, German, French, or another language.

## Documentation Language

Important human-facing files in a language-pair template, including prompts, workflow instructions, quality gates, review rubrics, and policy notes, must include the local language that contributors for that template are expected to read.

English can be included in parallel as a bridge language for precision and international collaboration, but important template instructions should not be English-only when the target contributors are expected to work in another language.

Examples:

- `en-ja`: important prompts and review instructions should include Japanese, optionally paired with English.
- `fr-en`: important prompts and review instructions should include English.
- `de-zh-Hant`: important prompts and review instructions should include Traditional Chinese, optionally paired with English.

Shared repository-level documentation should include Chinese when it is intended for project-owner review. Bilingual Chinese-English wording is acceptable when exact terminology matters.

## Public Agent and Skill Files

Each language-pair template and each reusable profile should include public `AGENTS.md` and `SKILL.md` files so downloaded copies of the repository can be used directly by AI agents.

`AGENTS.md` should state mandatory behavior for the template or profile. `SKILL.md` should state when and how to run the workflow.

These files must follow the same language rule: local contributor language plus optional English as the bridge language. For example, `en-ja/AGENTS.md` and `en-ja/SKILL.md` should include Japanese, optionally paired with English.
