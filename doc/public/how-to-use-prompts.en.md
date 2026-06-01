# AI Client Guide: Using This Repository's Prompts to Make a Book

This guide is for people who want to use an AI client to make a translated public-domain book. You do not need to be a programmer. You only need to open the project, paste a short request, and check the book files the AI creates.

## Three Things To Understand First

1. **A normal user only needs three items.**
   Tell the AI which book you want translated, the target language, and the rule for choosing the correct translation prompt automatically. The full wording for that rule is in the [Easiest Starter Prompt](#easiest-starter-prompt). The AI should handle the reliable source, source language, template, project folder, release, and validation commands.

2. **Let the AI read the rules.**
   You do not need to understand the repository rules. Ask the AI to choose the correct public prompt automatically.

3. **Only treat the release or private artifact result as finished.**
   The AI will handle source checks, rights checks, translation, review, EPUB build, spot-check, and release. For public-domain or licensed projects, check `output/release/`; for personal-use projects, check `output/private_artifacts/`.

## Easiest Starter Prompt

Open your AI client and open this project, or let LifeBook Launcher open it for you.

Paste this into your AI client, replacing the `{...}` placeholders:

### Public-Domain Book Translation Prompt

```text
Book I want translated: {title, author optional; include a reliable source link if you already have one}
Target language: {for example Simplified Chinese}

Automatically choose the correct translation prompt:
- If the matching source-language template already exists, execute doc/public/user_prompt/book_translation_existing_template.md.
- If the matching source-language template does not exist yet, execute doc/public/user_prompt/book_translation_new_template.md.

Do not ask me to fill technical fields unless rights or source evidence cannot be confirmed. Automatically find a reliable public-domain source, create the book project, complete translation, review, EPUB build, stratified random spot-check, and release.
```

## Personal-Use Book Translation Prompt

If you already have a local source file and only want a personal study translation, with no redistribution and no commercial use, use this prompt:

```text
Book I want translated: {title, local folder/path: XXX}
Target language: {for example Simplified Chinese}

Automatically choose the correct translation prompt:
- If the matching source-language template already exists, execute doc/public/user_prompt/book_translation_private_existing_template.md.
- If the matching source-language template does not exist yet, execute doc/public/user_prompt/book_translation_private_new_template.md.

This is for my personal use only. It will not be redistributed and will not be used commercially. Use the local source I provided.
Automatically create the project and strictly complete the full systematic translation workflow required by the templates, with no omissions.
```

Personal-use projects must be created under `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/`. The final versioned artifact is under `output/private_artifacts/`; it is not a public release and must not be published to GitHub.

## Refinement Review Prompt (Optional)

After the first EPUB has been generated, use this prompt if you want a stricter refinement pass. `N` means the number of consecutive clean rounds required before exit: `1` saves tokens, `3` is stricter and usually produces a higher-quality edition; use `2` if unsure.

```text
Book project: {book project path, for example books/{target}/{number}_{目标语言书名}_{目标语言作者名}}
Consecutive clean exit rounds N: {1/2/3; default 2}

First read AGENTS.md, this book's SKILL.md if present, template/epub_pipeline/README.md, template/epub_pipeline/common/README.md, and the relevant rules for cover, book-info/frontmatter, assets, quality gates, stratified random spot-check, and release.

Set a /goal: refine the already generated EPUB. Strictly follow the templates and check the cover, first pages/frontmatter, metadata, nav, table of contents, body text, notes, figures, formulas, tables, images, styles, reader-facing content, EPUB build, and release. Do not limit the review to only the items I named.

Start 2 independent review agents for stratified random spot-checking. Run at least 4 rounds. Use a new seed each round, and save samples, evidence, reviews, fixes, and closure records exactly as the template requires. If any round finds P0/P1/P2, any item score <70, reader-incomprehensible text, factual/terminology/figure/formula errors, or a hard template-gate failure, fix the issue and add another new round.

Exit condition: the most recent N consecutive rounds have no new blocking issues, and npm run review:random-validate:pass passes. N=1 is the lowest, token-saving strictness; N=3 is stricter and aims for a higher-quality reviewed edition. The user may choose the value.

After passing, clean or rebuild staging, regenerate the EPUB, and run publication lint, asset manifest, cover output, reader-facing policy, EPUBCheck, and release or private artifact scripts. For public-domain or licensed projects, the publishable EPUB must be written under this book's output/release/, and release_state.json.latest_status must be PASS. For personal-use projects, the final private artifact must be written under output/private_artifacts/, and private_artifact_state.json.latest_status must be PASS. Report the release EPUB or private artifact path, spot-check rounds, fix summary, validation command results, and remaining risks.
```

## Key Places To Know

- `.\template\epub_pipeline`: check which source-language and source-to-target templates currently exist. The AI uses this to decide whether to run the existing-template prompt or the new-template prompt.
- `.\tools\lifebook-launcher`: LifeBook Launcher client install and launch folder. Users need this path to use the LifeBook project and install OpenCode.
- `.\doc\public\user_prompt`: the public prompts live here. Read or edit these if you want to understand or manually adjust the prompt.
- `.\books\zh-Hans`: the most important output area for Simplified Chinese books. After translation succeeds, open the matching book folder and check `output\release\`; only release artifacts count as publishable results.
- `.\books\private`: private-use book project folder. Non-public-domain private translations should keep source text, translations, QA, EPUB output, and `output\private_artifacts\` private artifacts here only; this folder is ignored by Git and is not published to GitHub.

## What Are The Four Translation Prompts?

- `doc/public/user_prompt/book_translation_existing_template.md`: use when this repository already has the matching source-language template, such as Japanese to Simplified Chinese, English to Simplified Chinese, or Ancient Greek to Simplified Chinese.
- `doc/public/user_prompt/book_translation_new_template.md`: use when this repository does not yet have the matching source-language template, such as the first French to Simplified Chinese book.
- `doc/public/user_prompt/book_translation_private_existing_template.md`: use for a personal-use local source when the matching source-language template already exists.
- `doc/public/user_prompt/book_translation_private_new_template.md`: use for a personal-use local source when the matching source-language template does not exist yet.
- `doc/public/user_prompt/how_to_use_book_translation_prompts.md`: a shorter beginner-facing guide that only explains how to fill in the three items.

If you are unsure which one applies, ask the AI to check whether the template exists first. Normal users do not need to understand `source-target`, slug, profile, release version, or npm commands.

## Which Client Should I Use?

| Client | Good for | How to use the prompt |
| --- | --- | --- |
| Codex App | Desktop UI, diffs, terminal, browser, Git review | Open the repo, create a thread, paste the `/goal` |
| Claude Code | Terminal users who want a command-line agent | Start Claude Code in the repository and paste the prompt |
| LifeBook Launcher | Fewest manual steps;<br>requires OpenCode client support | Open Launcher and install OpenCode.<br>OpenCode supports most mainstream models, such as DeepSeek and Doubao.<br>Choose the book-translation task in OpenCode and paste the three items; see the [full example](#easiest-starter-prompt) |
| Google Antigravity | AI IDE with agent workflows | Open the repo workspace and paste the prompt into the agent box |

## LifeBook Launcher

If you do not want to handle project and client setup manually, use LifeBook Launcher. Launcher can download and open the OpenCode client. OpenCode supports most mainstream AI models, including DeepSeek and Doubao. Before use, configure the model provider API key inside OpenCode.

- Open **LifeBook Launcher**.
- Select or open this project.
- Download or open the OpenCode client if needed, then configure the API key in OpenCode.
- Paste the three items: book to translate, target language, and the prompt-selection rule. The full wording is in the [Easiest Starter Prompt](#easiest-starter-prompt).
- After the AI finishes, check `output/release/` for public-domain or licensed projects, or `output/private_artifacts/` for personal-use projects.

## Codex App

1. Install and open Codex App.
2. Select this repository folder.
3. Create a new thread.
4. Paste the `/goal`.
5. Let the AI read `AGENTS.md` and `template/`.
6. Review the files it wants to change.
7. Check the final `books/zh-Hans/.../output/release/` folder, or the matching `books/{target}/.../output/release/` folder for another target language. For personal-use projects, check `books/private/{target}/.../output/private_artifacts/`.

Codex App is useful for this repository because it makes it easy to review the files changed by the AI.

## Google Antigravity

1. Install Google Antigravity.
2. Open this repository as the workspace.
3. Paste the starter prompt into the agent input box.
4. Tell the agent to read `AGENTS.md` and `template/epub_pipeline/` first.
5. Use a confirmation/approval mode for commands and file edits.
6. Review diffs, test output, and release files.

## Common Mistakes To Avoid

- Letting the AI translate the whole book before reading the templates.
- Treating `output/book.epub` as final without `output/release/` for public projects or `output/private_artifacts/` for personal-use projects.
- Starting translation before rights are clear.
- Using a modern translation as source or reference.
- Not adding a new spot-check round after a blocking issue.
- Writing book-specific text back into `template/`.
