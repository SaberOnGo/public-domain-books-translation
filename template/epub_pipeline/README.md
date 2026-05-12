# EPUB Pipeline Templates

This directory separates shared EPUB production infrastructure from language-pair-specific translation rules.

## Layout

- `common/`: language-neutral EPUB workflow contracts, source and rights templates, state files, preproduction templates, scripts, and build/check helpers.
- `en-zh-Hans/`: English to Simplified Chinese translation prompts, glossary/style guidance, target-language metadata examples, translation quality rules, and review scorecards.

## Creating a Book Project

For a new English to Simplified Chinese book, copy `common/` first, then overlay `en-zh-Hans/` into:

`books/{book_id_slug}/`

All source text, translations, QA files, and EPUB output belong in the book project, never in `template/`.

## Naming

Language-pair directories use BCP 47-style direction names:

- `en-zh-Hans`: English to Simplified Chinese.
- `en-zh-Hant`: English to Traditional Chinese.
- `ja-zh-Hans`: Japanese to Simplified Chinese.

Use `common/` for workflow pieces that should be shared by every language pair.
