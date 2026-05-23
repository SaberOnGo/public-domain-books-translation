# AI Client Guide: Using This Repository's Prompts to Make a Book

This guide is for people who want to use an AI client to make a translated public-domain book. You do not need to be a programmer. You only need to open the project, paste a short request, and check the book files the AI creates.

## Three Things To Understand First

1. **A normal user only needs two inputs.**
   Tell the AI which book you want translated and the target language. The AI should handle the reliable source, source language, template, project folder, release, and validation commands.

2. **Let the AI read the rules.**
   You do not need to understand the repository rules. Ask the AI to choose the correct public prompt automatically.

3. **Only treat the release result as finished.**
   The AI will handle source checks, rights checks, translation, review, EPUB build, spot-check, and release. You only need to check the final `output/release/` folder.

## Easiest Starter Prompt

Open your AI client and open this project, or let LifeBook Launcher open it for you.

Paste this into your AI client, replacing `{...}` with the book and target language:

```text
Book I want translated: {title, author; include a reliable source link if you already have one}
Target language: {for example Simplified Chinese}

In the current repository, automatically choose the correct public-domain book translation prompt:
- If the matching source-language template already exists, execute doc/public/user_prompt/book_translation_existing_template.md.
- If the matching source-language template does not exist yet, execute doc/public/user_prompt/book_translation_new_template.md.

Do not ask me to fill technical fields unless rights or source evidence cannot be confirmed. Automatically find a reliable public-domain source, create the book project, complete translation, review, EPUB build, stratified random spot-check, and release.
```

## Two Places To Know

- `doc/public/user_prompt/`: the public prompts live here.
- `books/.../output/release/`: the publishable EPUB appears here after the AI finishes.

## What Are The Two Public Prompts?

- `doc/public/user_prompt/book_translation_existing_template.md`: use when this repository already has the matching source-language template, such as Japanese to Simplified Chinese, English to Simplified Chinese, or Ancient Greek to Simplified Chinese.
- `doc/public/user_prompt/book_translation_new_template.md`: use when this repository does not yet have the matching source-language template, such as the first French to Simplified Chinese book.
- `doc/public/user_prompt/how_to_use_book_translation_prompts.md`: a shorter beginner-facing guide that only explains how to fill in the book and target language.

If you are unsure which one applies, ask the AI to check whether the template exists first. Normal users do not need to understand `source-target`, slug, profile, release version, or npm commands.

## Which Client Should I Use?

| Client | Good for | How to use the prompt |
| --- | --- | --- |
| Codex App | Desktop UI, diffs, terminal, browser, Git review | Open the repo, create a thread, paste the `/goal` |
| Claude Code | Terminal users who want a command-line agent | Start Claude Code in the repository and paste the prompt |
| LifeBook Launcher | Fewest manual steps; requires OpenCode client support | Open Launcher and install OpenCode. OpenCode supports most mainstream models, such as DeepSeek and Doubao. Choose the book-translation task in OpenCode and paste the two-line input |
| Google Antigravity | AI IDE with agent workflows | Open the repo workspace and paste the prompt into the agent box |

## LifeBook Launcher

If you do not want to handle project and client setup manually, use LifeBook Launcher. Launcher can download and open the OpenCode client. OpenCode supports most mainstream AI models, including DeepSeek and Doubao. Before use, configure the model provider API key inside OpenCode.

- Open **LifeBook Launcher**.
- Select or open this project.
- Download or open the OpenCode client if needed, then configure the API key in OpenCode.
- Paste the two-line input: book to translate and target language.
- After the AI finishes, check the book folder's `output/release/`.

## Codex App

1. Install and open Codex App.
2. Select this repository folder.
3. Create a new thread.
4. Paste the `/goal`.
5. Let the AI read `AGENTS.md` and `template/`.
6. Review the files it wants to change.
7. Check the final `books/.../output/release/` folder.

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
- Treating `output/book.epub` as final without `output/release/`.
- Starting translation before rights are clear.
- Using a modern translation as source or reference.
- Not adding a new spot-check round after a blocking issue.
- Writing book-specific text back into `template/`.
