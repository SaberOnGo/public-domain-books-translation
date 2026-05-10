# LifeBook Translation Group: Public-Domain Book Translation and EPUB Collaboration

<table align="center">
  <tr>
    <td align="center"><h3><a href="./README.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./README.zh-TW.md">繁體中文</a></h3></td>
    <td align="center"><h3><a href="./README.en.md">English</a></h3></td>
    <td align="center"><h3><a href="./README.ja.md">日本語</a></h3></td>
  </tr>
</table>

LifeBook Translation Group is a collaborative project for translating public-domain books and producing readable EPUB editions.

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
- The translation direction, such as English to Chinese, Chinese to English, or Japanese to Chinese.

Example prompt:

```text
/goal Create a Chinese EPUB for A Negro Explorer at the North Pole using the reference project
D:\project\49_public-domain-books-translation\books\pg20923_a_negro_explorer_at_the_north_pole.
Fetch the source text from https://www.gutenberg.org/ebooks/20923.
Use epub_pipeline_template_zh_en and let 00_orchestrator_zh_en.md run the current full workflow:
source and rights review, book research, pre-translation trials, chapter translation, chapter review,
chapter gates, preproduction stage 1, sample EPUB review, full EPUB production, independent review,
revision routing, final output, and retrospective.
Generate output/book.epub and pass epubcheck.
```

If you only know a title, ask AI to find a reliable public-domain source first:

```text
Please find a reliable public-domain source for {book title}.
Prioritize Project Gutenberg, Wikisource, and Standard Ebooks.
After source and rights risks are checked, create a new book project under books/ using epub_pipeline_template_zh_en.
```

## Repository Structure

### `epub_pipeline_template_zh_en/`

This is the reusable book-production template. It is mainly for AI agents to read and execute. Human contributors usually do not need to inspect every file in it. For a new book, ask AI to copy this template into a new folder under `books/`; do not put real book data into the template folder itself.

Important files and folders:

- `README_ZH_EN.md`: template guide.
- `MASTER_PROMPT_ZH_EN.md`: master prompt for starting a new book project.
- `PIPELINE_SPEC_ZH_EN.md`: pipeline contract and directory rules.
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

The first example is English to Chinese, but the project can grow beyond that:

- English public-domain books into Chinese.
- Other foreign-language public-domain books into Chinese.
- Chinese public-domain books into English.
- Chinese public-domain books into other languages.

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

Translations, notes, covers, formatting, and EPUB packaging created in this project may have their own rights status. Project maintainers should define the release license clearly before public distribution.

## A Practical Invitation

If you like books and want to help bring overlooked public-domain works to more readers, you can start small. Read a chapter. Mark one awkward sentence. Check one name. Test one EPUB. A book improves through many small acts of attention.
