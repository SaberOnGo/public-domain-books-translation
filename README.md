# LifeBook Shufang Public-Domain Book Translation

<table align="center">
  <tr>
    <td align="center"><h3><a href="./README.zh-CN.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./readme/README.zh-TW.md">繁體中文</a></h3></td>
    <td align="center"><h3><a href="./README.md">English</a></h3></td>
    <td align="center"><h3><a href="./readme/README.ja.md">日本語</a></h3></td>
  </tr>
</table>

LifeBook Shufang is a multilingual workflow for turning public-domain books into reviewed, readable EPUB editions. It is not a one-click raw AI translation repository. The workflow keeps source evidence, rights checks, translation drafts, review records, EPUB validation, random spot checks, and versioned release artifacts.

You can help without being a programmer: propose a book, verify public-domain sources, read a chapter, compare source and translation, report awkward passages, test EPUB files, or improve templates and scripts.

## Quick Start

For a short user guide, see:

- [English guide](./doc/public/how-to-use-prompts.en.md)
- [简体中文说明](./doc/public/how-to-use-prompts.zh-CN.md)
- [繁體中文說明](./doc/public/how-to-use-prompts.zh-TW.md)
- [日本語ガイド](./doc/public/how-to-use-prompts.ja.md)

Minimal prompt for an AI client:

```text
Book I want translated: {title, author, and source URL if known}
Target language: {for example Spanish, English, Japanese, or Simplified Chinese}

Read AGENTS.md first, then read the relevant template/epub_pipeline rules.
Create the book project with books/scripts/create_book_project.py.
Do not write book-specific source text, translations, QA, EPUB output, or metadata into template/.
Stop if source evidence or public-domain status is unclear.
```

## AI Clients

This repository is model-neutral. Codex App, Claude Code, OpenCode, aider, Antigravity, or any local-file AI client may be used if it can read the repository, edit files, run commands, and follow `AGENTS.md`.

For the easiest desktop setup, use **LifeBook Launcher**:

- Windows users can currently double-click `tools\lifebook-launcher\LifeBook Launcher Setup.exe`.
- Release users only need the **LifeBook Launcher** app or installer. The launcher prepares and updates the LifeBook project folder automatically; on Windows the default project folder is `D:\LifeBook`.
- The source folder in this repository is `tools/lifebook-launcher/source/` for developers and packagers.
- It keeps the LifeBook project updated automatically, checks/updates OpenCode Desktop, supports LifeBook Launcher self-update, and lets users configure startup launch.

The launcher does not store API keys and does not include OpenCode binaries in this repository. See [LifeBook Launcher design](./docs/lifebook-launcher/design.zh-CN.md) and [OpenCode client guide](./docs/ai-clients/opencode.zh-CN.md).

## Important Folders For Users

- `.\template\epub_pipeline`: check which source-language and source-to-target templates currently exist. Language-pair folders such as `en-zh-Hans`, `ja-zh-Hans`, and `grc-zh-Hans` live here.
- `.\tools\lifebook-launcher`: LifeBook Launcher entry folder. Windows users double-click `LifeBook Launcher Setup.exe` inside this folder.
- `.\doc\public\user_prompt`: public starter prompts. Read or adjust these if you want to understand or manually refine the prompt given to an AI client.
- `.\books\zh-Hans`: Simplified Chinese book projects and outputs. After a book is completed, look inside the matching book folder, especially `output\book.epub` and `output\release\`.

## Repository Layout

- `AGENTS.md`: mandatory rules for all AI agents.
- `template/epub_pipeline/`: authoritative workflow templates and policies.
- `template/epub_pipeline/common/`: shared EPUB workflow, scripts, source evidence, rights checks, quality gates, random spot checks, and release rules.
- `template/epub_pipeline/{source-target}/`: language-pair rules, prompts, glossary guidance, and review rubrics.
- `template/epub_pipeline/targets/{target}/`: target-language quality rules.
- `template/epub_pipeline/profiles/{profile-target}/`: optional overlays for special book types.
- `books/{target}/{number}_{book_slug}/`: actual book projects. Book-specific files belong here.
- `books/`: shared Node.js tooling; install dependencies once here.
- `doc/public/`: public instructions, prompt guides, and candidate-book notes.
- `research/{source-target}/`: language-pair-specific research artifacts.
- `.opencode/` and `opencode.jsonc`: thin OpenCode adapter only, not workflow rules.
- `tools/lifebook-launcher/`: LifeBook Launcher desktop entry; development source lives in `source/`.

## Making A New Book

Use the project creation script instead of copying folders manually:

```powershell
cd books
npm run new:book -- {book_id_slug} --source-target {source-target}
```

The script creates:

```text
books/{target}/{number}_{book_id_slug}/
```

It copies `template/epub_pipeline/common` first, then overlays the matching language-pair template. If a book needs a special profile, overlay the matching `profiles/{profile-target}/` after that.

## Core Rules

- Preserve public-domain source evidence and rights checks before translation.
- Do not use modern copyrighted translations, pirate sites, or unclear EPUB downloads.
- Raw AI output is not publishable.
- Keep concrete book content out of `template/`.
- Important human-facing template files must include the local language expected by contributors.
- Run EPUB validation, reader-facing policy checks, stratified random spot checks, and versioned release gates before final delivery.

## Book Tooling

Install shared dependencies once:

```powershell
cd books
npm install
```

Then run book-local scripts inside a concrete book project, for example:

```powershell
npm run build:epub
npm run check:epub
npm run review:random-samples
npm run review:random-validate:pass
npm run release:create
```

## Contributing

Useful contributions include source research, rights review, translation review, terminology checks, EPUB testing, accessibility/layout feedback, and automation improvements. Small, traceable corrections are preferred over large unreviewable rewrites.

## License And Rights

Each source book requires its own rights check. Public-domain status may vary by country.

Non-code book content produced in this project is released under `CC BY-NC-SA 4.0` by default unless a file says otherwise. Third-party commercial use requires separate permission from LifeBook Shufang and relevant rights holders.

See:

- [LICENSE.en.md](./license/LICENSE.en.md)
- [CONTRIBUTING.en.md](./license/CONTRIBUTING.en.md)
- [COMMERCIAL_LICENSE.en.md](./license/COMMERCIAL_LICENSE.en.md)
