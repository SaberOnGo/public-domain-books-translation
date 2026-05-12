# LifeBook Shufang: Global Public-Domain Book Translation and EPUB Collaboration

<table align="center">
  <tr>
    <td align="center"><h3><a href="./README.zh-CN.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./readme/README.zh-TW.md">繁體中文</a></h3></td>
    <td align="center"><h3><a href="./README.md">English</a></h3></td>
    <td align="center"><h3><a href="./readme/README.ja.md">日本語</a></h3></td>
  </tr>
</table>

LifeBook Shufang is a global, multilingual collaboration project for translating public-domain books and producing readable EPUB editions.

The goal is not to publish raw AI output. AI can help with repetitive work: finding and cleaning source text, splitting chapters, drafting translations, creating glossaries, checking omissions, and building EPUB files. But good books still need human judgment. People are needed to read, question, correct, polish, verify names and terms, and test the final book in real reading apps.

You do not need to be a programmer to help. Reading a chapter and saying "this part is confusing" is already useful.

## What We Are Trying To Do

- Choose public-domain books from reliable sources such as Project Gutenberg, Wikisource, and Standard Ebooks.
- Preserve source and rights evidence before translation.
- Avoid modern copyrighted editions, modern annotations, and unclear download sources.
- Use AI for traceable drafting and checking, not for one-shot unreviewed publishing.
- Keep source chapters, draft translations, final chapters, review files, glossary files, and EPUB output in a structure that other people can inspect.
- Let contributors help with small tasks: reading, proofreading, terminology, source research, layout checks, and EPUB testing.

This is intentionally modest. Think of it as a small book workshop: someone finds a book, someone checks the source, someone reviews a chapter, someone tests the EPUB. Many small contributions can make one book better.

## Easiest Way To Start

Most contributors do not need to manually copy folders or fill in metadata files. Give an AI assistant the template folder, a public-domain source URL if you have one, and the translation direction. The AI should create the book project, fill in metadata, document source evidence, run the translation pipeline, and build the EPUB.

Usually you only need to provide:

- The book you want to work on.
- A public-domain source URL, if known.
- The translation direction, such as English to Spanish, French to Japanese, Chinese to English, or Japanese to German.
- The existing language-pair template to use. If that template does not exist yet, add the matching template directory first.

Example prompt. This uses French to English as a concrete direction. If `fr-en` does not exist yet, add that language-pair template first:

```text
/goal Create an English EPUB from a French public-domain book.
Fetch the source text from {reliable public-domain source URL}.
Use template/epub_pipeline/common plus template/epub_pipeline/fr-en, and let the orchestrator prompt run the full workflow:
source and rights review, book research, pre-translation trials, chapter translation, chapter review,
chapter gates, preproduction stage 1, sample EPUB review, full EPUB production, independent review,
revision routing, final output, and retrospective.
Generate output/book.epub and pass epubcheck.
```

If you only know a title, ask AI to find a reliable public-domain source first:

```text
Please find a reliable public-domain source for {book title}.
Prioritize Project Gutenberg, Wikisource, and Standard Ebooks.
After source and rights risks are checked, choose the matching language-pair template. For French to English, use or add template/epub_pipeline/fr-en; for Japanese to Spanish, use or add template/epub_pipeline/ja-es; for English to Simplified Chinese, use template/epub_pipeline/en-zh-Hans. Then create a new book project under books/ by copying template/epub_pipeline/common first and overlaying the language-pair template.
```

## Repository Structure

### `template/epub_pipeline/`

This is the reusable book-production template area. `common/` contains shared EPUB workflow contracts, rights checks, state files, scripts, and production rules. Each language-pair directory contains prompts, glossary/style guidance, typography expectations, and review rules for that direction. For a new book, ask AI to copy `common/` into a new folder under `books/`, then overlay the matching language-pair template; do not put real book data into the template folder itself.

Important files and folders:

- `template/epub_pipeline/README.md`: template layout guide.
- `template/epub_pipeline/common/PIPELINE_SPEC.md`: pipeline contract and directory rules.
- `template/epub_pipeline/en-zh-Hans/README.md`: one currently available language-pair template guide.
- `template/epub_pipeline/en-zh-Hans/MASTER_PROMPT.md`: master prompt for starting a new book project.
- `prompts/`: step-by-step prompts from ingestion to review, EPUB production, and retrospective.
- `metadata/`: book metadata, rights checklist, source evidence, style profile.
- `chapters/`: source chapters, translated drafts, and final chapters.
- `qa/`: fidelity, readability, terminology, imagery, and gate reviews.
- `preproduction/`: cover, metadata, layout, and sample EPUB checks.
- `reviews/`: independent review and scorecards.
- `output/`: final EPUB and validation results.

### `books/`

This folder contains actual book projects. The current example is:

```text
books/pg20923_a_negro_explorer_at_the_north_pole/
```

It is based on Project Gutenberg #20923, Matthew A. Henson's *A Negro Explorer at the North Pole*. It includes source evidence, rights notes, 26 source chapters, translated chapters, final chapters, review files, generated EPUB output, and an EPUBCheck report with zero fatal errors, zero errors, and zero warnings.

The example proves that the workflow can run end to end. It does not mean every chapter has already received final human editorial approval.

### `translation_quality_framework/`

This folder defines the translation quality workflow. It explains how to research, sample-test, review, revise, and gate translation work before treating it as final.

### `doc/public/`

This folder stores public notes for candidate books, copyright screening, and source research.

## How You Can Help

Useful contributions include:

- Read a few pages and report awkward passages.
- Compare one source paragraph with its translation.
- Check names, places, and recurring terms.
- Find typos or punctuation issues.
- Test an EPUB on a phone, tablet, or e-reader.
- Research whether a candidate book is truly public domain.
- Improve cover, metadata, layout, or EPUB compatibility.
- Review whether a chapter sounds like natural Chinese or natural English.

Simple feedback format:

```text
Book:
Chapter:
Location or sentence:
Problem:
Suggestion, if any:
```

## Human Checkpoints

AI can run most of the workflow automatically, but people are especially useful at these points:

- Book research: `metadata/book_specific_translation_research.md`, `metadata/style_profile.md`, `glossary/terms.csv`.
- Pre-translation trial: `qa/pretranslation/pretranslation_report.md`.
- Chapter control and review: `chapters/src/`, `chapters/translated/`, `chapters/final/`, `qa/chapter_controls/`, `qa/fidelity/`, `qa/readability/`, `qa/terminology/`, `qa/imagery/`, `qa/gates/`.
- Preproduction stage 1: `preproduction/stage1/production_spec.md`.
- Preproduction stage 2: `preproduction/stage2_sample/sample_book.epub` and `sample_review.md`.
- Final output: `output/book.epub`, `output/epubcheck.json`, `reviews/`.

## Translation Directions

Templates are organized by concrete translation direction. `common` is shared by all language pairs. Directories such as `en-zh-Hans`, `fr-en`, `ja-es`, and `zh-Hant-de` identify the source and target languages.

The project can support concrete directions such as:

- English public-domain novels into Spanish.
- French essays into Japanese.
- Chinese public-domain works into English.
- Japanese travel writing into German.
- German philosophy into Traditional Chinese.
- Arabic historical texts into Indonesian.

For every direction, the same principles apply: verify rights, document sources, research before translating, run sample trials first, review chapters carefully, and validate the final EPUB.

## Rules We Care About

- Do not use modern copyrighted translations as source material.
- Do not use pirate websites or unclear EPUB downloads.
- Do not treat raw AI output as publishable text.
- Do not write real book data into the template folder.
- Keep review records and failure records.
- Prefer small, reviewable improvements over untraceable whole-book rewrites.

## License And Rights Notes

Each source book must be checked separately. A text may be public domain in one country but not automatically public domain everywhere.

Project Gutenberg texts are often public domain in the United States. Before wider distribution, contributors should review the copyright status for the target region.

Translations, notes, covers, formatting, EPUB packaging, and other non-code content produced by this project are released to the public under `CC BY-NC-SA 4.0` by default. Third-party commercial use requires separate permission from LifeBook Shufang and the relevant rights holders.

By contributing, contributors agree that their contributions may be included in this project for public release and may be used by LifeBook Shufang in LifeBook products and services. LifeBook Shufang is responsible for project organization, publication, quality control, license management, and contributor return arrangements. Specific attribution and return methods are determined according to contribution status and project rules.

See:

- [LICENSE.en.md](./license/LICENSE.en.md): public content license and code license.
- [CONTRIBUTING.en.md](./license/CONTRIBUTING.en.md): contributor authorization and participation rules.
- [COMMERCIAL_LICENSE.en.md](./license/COMMERCIAL_LICENSE.en.md): third-party commercial use notes.

## A Practical Invitation

If you like books and want to help bring overlooked public-domain works to more readers, you can start small. Read a chapter. Mark one awkward sentence. Check one name. Test one EPUB. A book improves through many small acts of attention.
