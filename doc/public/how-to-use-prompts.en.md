# AI Client Guide: Using This Repository's Prompts to Make a Book

This guide is for contributors who want to use AI clients for book-production work. You do not need to be a programmer. You only need to open this repository, paste a clear prompt, and review the files the AI creates.

> Important: never write API keys into repository files. Do not commit `auth.json`, `.env`, screenshots of settings, or any secret.

## Three Things To Understand First

1. **A normal user only needs two inputs.**
   Tell the AI which book you want translated and the target language. The AI should handle the reliable source, source language, template, project folder, release, and validation commands.

2. **This repository has rules.**
   Always ask the AI to read `AGENTS.md` first, then the relevant files under `template/epub_pipeline/`.

3. **Raw AI output is not publishable.**
   The real workflow is source evidence, rights review, research, trial translation, chapter translation, review, EPUB build, EPUBCheck, stratified random spot-check, and release.

## Easiest Starter Prompt

Open a terminal and go to the repository root:

```powershell
cd D:\project\49_public-domain-books-translation
```

If you installed only LifeBook Launcher from a release, open the project folder it prepared instead. On Windows the default is `D:\LifeBook`.

Paste this into your AI client, replacing `{...}` with the book and target language:

```text
Book I want translated: {title, author; include a reliable source link if you already have one}
Target language: {for example Simplified Chinese}

In the current repository, automatically choose the correct public-domain book translation prompt:
- If the matching source-language template already exists, execute doc/public/user_prompt/book_translation_existing_template.md.
- If the matching source-language template does not exist yet, execute doc/public/user_prompt/book_translation_new_template.md.

Do not ask me to fill technical fields unless rights or source evidence cannot be confirmed. Automatically find a reliable public-domain source, create the book project, complete translation, review, EPUB build, stratified random spot-check, and release.
```

If your client does not support `/goal`, replace the first line with:

```text
Goal: Create a new public-domain book translation EPUB in the current repository.
```

## Four Folders You Should Know

- `.\template\epub_pipeline`: check which source-language and language-pair templates currently exist.
- `.\tools\lifebook-launcher`: LifeBook Launcher entry folder in a repository copy. Release users usually start Launcher from the installed app; it prepares the project folder automatically.
- `.\doc\public\user_prompt`: public starter prompts; read these if you want prompt details or manual edits.
- `.\books\zh-Hans`: Simplified Chinese book output folder; after a book is completed, look in the matching book folder for `output\book.epub` and `output\release\`.

## What Are The Two Public Prompts?

- `doc/public/user_prompt/book_translation_existing_template.md`: use when this repository already has the matching source-language template, such as Japanese to Simplified Chinese, English to Simplified Chinese, or Ancient Greek to Simplified Chinese.
- `doc/public/user_prompt/book_translation_new_template.md`: use when this repository does not yet have the matching source-language template, such as the first French to Simplified Chinese book.
- `doc/public/user_prompt/how_to_use_book_translation_prompts.md`: a shorter beginner-facing guide that only explains how to fill in the book and target language.

If you are unsure which one applies, ask the AI to check whether the template exists first. Normal users do not need to understand `source-target`, slug, profile, release version, or npm commands.

## Which Client Should I Use?

| Client | Good for | How to use the prompt |
| --- | --- | --- |
| Codex App | Desktop UI, diffs, terminal, browser, Git review | Open the repo, create a thread, paste the `/goal` |
| Claude Code | Terminal agent, Claude or DeepSeek backend | Run `claude` in the repo and paste the prompt |
| Google Antigravity | AI IDE with agent workflows | Open the repo workspace and paste the prompt into the agent box |
| OpenCode | Open-source client, easy DeepSeek setup | Use LifeBook Launcher to check/update OpenCode Desktop, open the repository, paste the prompt |

## LifeBook Launcher

If you do not want to handle project and client updates manually, use LifeBook Launcher. It does not save API keys and does not store OpenCode binaries in this repository.

- End users can double-click the **LifeBook Launcher** app or installer from a release package.
- Current local Windows entry: `tools\lifebook-launcher\LifeBook Launcher Setup.exe`.
- Developer source folder: `tools/lifebook-launcher/source/`.
- It prepares and updates the LifeBook project automatically. On Windows the default project folder is `D:\LifeBook`.
- It checks/updates OpenCode Desktop and can download, install, and restart LifeBook Launcher itself.
- Users can turn startup launch on or off in settings.

## Codex App

1. Install and open Codex App.
2. Select this repository folder.
3. Create a new thread.
4. Paste the `/goal`.
5. Let the AI read `AGENTS.md` and `template/`.
6. Review the files it wants to change.
7. Check the final `books/.../output/release/` folder.

Codex App is useful for this repository because it has project threads, worktrees, an integrated terminal, diff review, and Git operations.

DeepSeek note: Codex App normally uses the OpenAI/Codex models available to your account. If you specifically want DeepSeek, OpenCode or Claude Code is the simpler route. Only try a custom Codex CLI provider if your Codex version or gateway explicitly supports the required protocol.

## Claude Code With DeepSeek

DeepSeek provides an official Claude Code integration. On Windows PowerShell:

```powershell
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="<your DeepSeek API Key>"
$env:ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_EFFORT_LEVEL="max"

cd D:\project\49_public-domain-books-translation
claude
```

On macOS/Linux:

```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN="<your DeepSeek API Key>"
export ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_EFFORT_LEVEL=max

cd /path/to/49_public-domain-books-translation
claude
```

Then paste the starter prompt.

## OpenCode With DeepSeek

OpenCode is a straightforward choice for DeepSeek.

1. Install OpenCode.
2. Start it in this repository:

```powershell
cd D:\project\49_public-domain-books-translation
opencode
```

3. In OpenCode, type:

```text
/connect
```

4. Search for and select `deepseek`.
5. Paste your DeepSeek API Key.
6. Select `DeepSeek-V4-Pro`.
7. Paste the `/goal` prompt from this guide.

If you want the AI to plan first, add:

```text
Only show the execution plan and file list first. Wait for my confirmation before writing files.
```

## Google Antigravity

1. Install Google Antigravity.
2. Open this repository as the workspace.
3. Paste the starter prompt into the agent input box.
4. Tell the agent to read `AGENTS.md` and `template/epub_pipeline/` first.
5. Use a confirmation/approval mode for commands and file edits.
6. Review diffs, test output, and release files.

DeepSeek note: if the Antigravity UI does not list DeepSeek as a provider, do not force an unsupported setup. Use its built-in models for this workflow, or use OpenCode/Claude Code when DeepSeek is required.

## Codex CLI Custom Provider Note

Codex configuration supports `model_provider` and `model_providers.<id>` with options such as `base_url` and `env_key`. DeepSeek's normal OpenAI-compatible endpoint uses Chat Completions style access. If your Codex version or gateway does not support the required protocol, do not force it. Prefer Codex App's default models, or OpenCode/Claude Code for DeepSeek.

## Common Book Commands

Inside a book project:

```powershell
npm run build:epub
npm run check:epub
npm run review:random-samples
npm run review:random-validate:pass
npm run release:create
```

If dependencies are missing, install once from `books/`:

```powershell
cd D:\project\49_public-domain-books-translation\books
npm install
```

## Common Mistakes To Avoid

- Committing an API key.
- Letting the AI translate the whole book before reading the templates.
- Treating `output/book.epub` as final without `output/release/`.
- Starting translation before rights are clear.
- Using a modern translation as source or reference.
- Not adding a new spot-check round after a blocking issue.
- Writing book-specific text back into `template/`.

## References

- Codex App: https://developers.openai.com/codex/app
- Codex configuration reference: https://developers.openai.com/codex/config-reference
- DeepSeek API quick start: https://api-docs.deepseek.com/
- DeepSeek with Claude Code: https://api-docs.deepseek.com/guides/agent_integrations/claude_code
- DeepSeek with OpenCode: https://api-docs.deepseek.com/guides/agent_integrations/opencode
- OpenCode providers: https://open-code.ai/en/docs/providers
- Google Antigravity docs: https://www.antigravity.google/docs/overview
