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
