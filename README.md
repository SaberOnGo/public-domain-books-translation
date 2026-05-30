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
Book I want translated: {title, author optional, and source URL if known}
Target language: {for example Spanish, English, Japanese, or Simplified Chinese}

Automatically choose the correct translation prompt:
- If the matching source-language template already exists, execute doc/public/user_prompt/book_translation_existing_template.md.
- If the matching source-language template does not exist yet, execute doc/public/user_prompt/book_translation_new_template.md.

Do not ask me to fill technical fields unless rights or source evidence cannot be confirmed. Automatically find a reliable public-domain source, create the book project, complete translation, review, EPUB build, stratified random spot-check, and release.
If LifeBook Digest is not explicitly requested, decide automatically: generate it after EPUB output for long novels, specialist books, and philosophy books; skip short stories, natural-science books, and other categories.
When Digest should be generated, create `digest.config.json` in the book project root with `enabled=true` and `merge_into_epub=true`, then run from the repository root: `python -m digest.lifebook_digest --book-root books/{target}/{number}_{book_id_slug}`. The output remains a standard EPUB.
```

For non-public-domain books, use private-use mode only. The user must provide a local ebook file and explicitly declare personal study only, no redistribution, and no commercial use. The AI should create the project under `books/private/{target}/{number}_{book_slug}/`; the script also overlays `template/epub_pipeline/modes/private_use/` so private cover, frontmatter, and artifact rules cannot be confused with public publication rules. `books/private/` is ignored by Git, and its source text, translations, QA records, EPUB files, and private artifacts must not be published to GitHub.

## AI Clients

This repository is model-neutral. Codex App, Claude Code, OpenCode, aider, Antigravity, or any local-file AI client may be used if it can read the repository, edit files, run commands, and follow `AGENTS.md`.

For the easiest desktop setup, use **LifeBook Launcher**:

- Windows users can currently double-click `tools\lifebook-launcher\LifeBook Launcher Setup.exe`.
- Release users only need the **LifeBook Launcher** app or installer. The launcher prepares and updates the LifeBook project folder automatically; on Windows the default project folder is `D:\LifeBook`.
- The source folder in this repository is `tools/lifebook-launcher/source/` for developers and packagers.
- It keeps the LifeBook project updated automatically, checks/updates OpenCode Desktop, supports LifeBook Launcher self-update, and lets users configure startup launch.

The launcher does not store API keys and does not include OpenCode binaries in this repository. For OpenCode client usage, see the [OpenCode client guide](./docs/ai-clients/opencode.zh-CN.md).

## Important Folders For Users

- `.\template\epub_pipeline`: check which source-language and source-to-target templates currently exist. Language-pair folders such as `en-zh-Hans`, `ja-zh-Hans`, and `grc-zh-Hans` live here.
- `.\tools\lifebook-launcher`: LifeBook Launcher client install and launch folder. Users need this path to use the LifeBook project and install OpenCode.
- `.\doc\public\user_prompt`: public starter prompts. Read or adjust these if you want to understand or manually refine the prompt given to an AI client.
- `.\books\zh-Hans`: the most important output area for Simplified Chinese books. After translation succeeds, open the matching book folder and check `output\release\`; only release artifacts count as publishable results.
- `.\books\private`: local private-use book projects. This is for user-provided local sources used for personal non-public-domain translation. It is ignored by Git and must not be published to GitHub.

## LifeBook Digest

<table align="center">
  <tr>
    <td align="center"><h3><a href="./readme/digest/README.en.md">LifeBook Digest Guide</a></h3></td>
    <td align="center"><h3><a href="./license/DIGEST_LICENSE.en.md">Digest License</a></h3></td>
  </tr>
</table>

The LifeBook translation publishing system now includes LifeBook Digest. It helps make long books thinner: after EPUB output, LifeBook Digest can ask an AI agent to extract core content from long-form books. The result is not only a text digest; it also includes chapter topology and knowledge-structure signals so readers can see the book's shape more quickly and approach it from a different reading angle.

LifeBook Digest is currently implemented as an independent LifeBook post-processing module. See the [LifeBook Digest guide](./readme/digest/README.en.md) and [Digest license notes](./license/DIGEST_LICENSE.en.md) for acknowledgements and third-party inspiration notes. License and reuse constraints are governed by the [Digest license notes](./license/DIGEST_LICENSE.en.md).

## Repository Layout

- `AGENTS.md`: mandatory rules for all AI agents.
- `digest/`: reusable LifeBook Digest post-processing module; each book controls enablement and EPUB merge behavior through `digest.config.json`.
- `template/epub_pipeline/`: authoritative workflow templates and policies.
- `template/epub_pipeline/common/`: shared EPUB workflow, scripts, source evidence, rights checks, quality gates, random spot checks, and release rules.
- `template/epub_pipeline/{source-target}/`: language-pair rules, prompts, glossary guidance, and review rubrics.
- `template/epub_pipeline/targets/{target}/`: target-language quality rules.
- `template/epub_pipeline/profiles/{profile-target}/`: optional overlays for special book types.
- `template/epub_pipeline/modes/private_use/`: private-use overlay copied only for non-public-domain personal-use projects. It contains private cover, frontmatter, artifact, and gate scripts.
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

It copies `template/epub_pipeline/common` first, then overlays the matching language-pair template. If a book needs a special profile, overlay the matching `profiles/{profile-target}/` after that. Private-use projects receive one more overlay: `template/epub_pipeline/modes/private_use/`.

Private-use projects must be created explicitly:

```powershell
cd books
npm run new:book -- {book_id_slug} --source-target {source-target} --mode private-use --local-source-file "{path_to_local_ebook}" --private-use-declaration "Personal study only; no redistribution; no commercial use."
```

Private mode keeps the translation and QA quality bar, but changes rights, reader-facing wording, and artifact semantics. Private covers use `个人学习版`; private frontmatter uses `参考LifeBook书坊 个人自制`, removes public-domain notices, and states personal-use/no-redistribution/no-commercial-use plus personal risk responsibility. Private artifacts are written under `output/private_artifacts/` and are personal-use outputs, not public releases.

## Core Rules

- Preserve source evidence and rights checks before translation; public projects require public-domain or licensed sources.
- Non-public-domain personal-use projects must use `private_use` mode and stay under ignored `books/private/`.
- Private-use projects must carry the `modes/private_use` overlay and must not reuse public-domain cover/frontmatter/release wording.
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

For a private-use project, use the private artifact command after the same build, EPUBCheck, and random spot-check gates:

```powershell
npm run build:private-epub
npm run check:epub
npm run review:random-samples
npm run review:random-validate:pass
npm run private:artifact:create
```

## Contributing

Useful contributions include source research, rights review, translation review, terminology checks, EPUB testing, accessibility/layout feedback, and automation improvements. Small, traceable corrections are preferred over large unreviewable rewrites.

## License And Rights

Each source book requires its own rights check. Public-domain status may vary by country.

Non-code book content produced in this project is released under `CC BY-NC-SA 4.0` by default unless a file says otherwise. Third-party commercial use requires separate permission from LifeBook Shufang and relevant rights holders.

Private-use projects under `books/private/` are not public project content, are not covered by the default public release license, and must not be committed or published to GitHub. Any private translation is for the individual user's personal study only, with no redistribution and no commercial use; the user's private use risk is their own. LifeBook Shufang publishes the reusable LifeBook translation publishing system only and does not assume copyright risk or liability caused by another person's private translation, storage, redistribution, or use of non-public-domain content.

See:

- [LICENSE.en.md](./license/LICENSE.en.md)
- [CONTRIBUTING.en.md](./license/CONTRIBUTING.en.md)
- [COMMERCIAL_LICENSE.en.md](./license/COMMERCIAL_LICENSE.en.md)
