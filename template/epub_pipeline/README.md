# EPUB Pipeline Templates

This directory separates shared EPUB production infrastructure from language-pair-specific translation rules.

## Layout

- `common/`: language-neutral EPUB workflow contracts, source and rights templates, state files, preproduction templates, scripts, and build/check helpers.
- `{source-target}/`: language-pair-specific translation prompts, glossary/style guidance, target-language metadata examples, translation quality rules, and review scorecards.

## Creating a Book Project

For a new book project, copy `common/` first, then overlay the matching language-pair template into:

`books/{book_id_slug}/`

All source text, translations, QA files, and EPUB output belong in the book project, never in `template/`.

## Naming

Language-pair directories use BCP 47-style direction names:

- `en-zh-Hans`: English to Simplified Chinese.
- `fr-en`: French to English.
- `ja-es`: Japanese to Spanish.
- `zh-Hant-de`: Traditional Chinese to German.

Use `common/` for workflow pieces that should be shared by every language pair.

## Documentation Language

Important human-facing files in a language-pair template, including prompts, workflow instructions, quality gates, review rubrics, and policy notes, must include the local language that contributors for that template are expected to read.

English can be included in parallel as a bridge language for precision and international collaboration, but important template instructions should not be English-only when the target contributors are expected to work in another language.

Examples:

- `en-ja`: important prompts and review instructions should include Japanese, optionally paired with English.
- `fr-en`: important prompts and review instructions should include English.
- `de-zh-Hant`: important prompts and review instructions should include Traditional Chinese, optionally paired with English.

Shared repository-level documentation should include Chinese when it is intended for project-owner review. Bilingual Chinese-English wording is acceptable when exact terminology matters.
