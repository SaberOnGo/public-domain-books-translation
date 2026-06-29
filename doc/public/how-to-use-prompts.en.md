# AI Client Guide: Using This Repository's Prompts to Make a Book

This guide is for people who want to use an AI client to make a translated public-domain book. No programming experience is required. The usual workflow is to open the project, paste a short request, and check the book files the AI creates.

## Four Things To Understand First

1. **A normal user only needs three items.**
   Tell the AI which book should be translated, the target language, and the rule for choosing the correct translation prompt automatically. The full wording for that rule is in the [Easiest Starter Prompt](#easiest-starter-prompt). The AI should handle the reliable source, source language, template, project folder, release, and validation commands.

2. **Let the AI read the rules.**
   Readers do not need to understand the repository rules. Ask the AI to choose the correct public prompt automatically.

3. **Only treat the release or private artifact result as finished.**
   The AI will handle source checks, rights checks, translation, review, EPUB build, spot-check, and release. For public-domain or licensed projects, check `output/release/`; for personal-use projects, check `output/private_artifacts/`.

4. **English to Simplified Chinese projects produce two EPUB editions by default.**
   If the source language is English and the target language is Simplified Chinese, the AI should produce both the target-only Simplified Chinese EPUB and the English-Chinese bilingual parallel EPUB. This is independent from public or private-use mode. For other language pairs, add this sentence only when you want a bilingual parallel edition: `请输出 edition_type: bilingual_parallel，同时生成目标语言版 EPUB 和源语言-目标语言双语对照版 EPUB。`

## Easiest Starter Prompt

Open the AI client and open this project, or let LifeBook Launcher open it.

Paste this into the AI client, replacing the `{...}` placeholders:

### Public-Domain Book Translation Prompt

```text
Book I want translated: {title, author optional; include a reliable source link if one is already available}
Target language: {for example Simplified Chinese}
[Important proper-noun translation format for names, places, terms, rare names, and hard-to-read transliterations] setting = 3

Automatically choose the correct translation prompt:
- If the matching source-language template already exists, execute doc/public/user_prompt/book_translation_existing_template.md.
- If the matching source-language template does not exist yet, execute doc/public/user_prompt/book_translation_new_template.md.

Do not ask me to fill technical fields unless rights or source evidence cannot be confirmed. Automatically find a reliable public-domain source, create the book project, complete translation, review, EPUB build, stratified random spot-check, and release.
If the source language is English and the target language is Simplified Chinese, default to `edition_type: bilingual_parallel` and produce both the target-only Simplified Chinese EPUB and the English-Chinese bilingual parallel EPUB. For other language pairs, produce a bilingual parallel EPUB only when I explicitly request it.
During translation, run the per-chapter post-translation full check and fix gate for every chapter. Compare the whole source chapter and whole translated chapter for fidelity, target-language readability, terminology, titles/subtitles, notes, figure/table/formula text interfaces, source-syntax residue, stiff literal prose, over-explanation, and invented additions. If any issue is found, fix it, but that round cannot PASS; append a new full-chapter recheck until the latest round is a zero-issue PASS.
After the first EPUB, run stratified random spot-checking and defect-family closure. If any sample exposes a defect, do not fix only that sample. Classify the defect family in that same round, audit the whole book for similar cases with `rg`, glossary rows, title maps, sample manifests, and small-context source comparison, fix confirmed matches, document exceptions, and run a new-seed round. Translation-quality defect families must use `skills/translation-quality-defect-families/SKILL.md`.
```

The proper-noun format setting is optional; the default is `3`. Values: `1` translate directly into the target language; `2` keep the source form untranslated; `3` first body occurrence as `translation (source)`, then translation; `4` first body occurrence as `translation (source)`, then source form; `5` first body occurrence as `translation (source)` plus an approved note marker, then translation.

## Personal-Use Book Translation Prompt

If a local source file is already available and the translation is only for personal study, with no redistribution and no commercial use, use this prompt:

```text
Book I want translated: {title, local folder/path: XXX}
Target language: {for example Simplified Chinese}
[Important proper-noun translation format for names, places, terms, rare names, and hard-to-read transliterations] setting = 3

Automatically choose the correct translation prompt:
- If the matching source-language template already exists, execute doc/public/user_prompt/book_translation_private_existing_template.md.
- If the matching source-language template does not exist yet, execute doc/public/user_prompt/book_translation_private_new_template.md.

This is for my personal use only. It will not be redistributed and will not be used commercially. Use the local source I provided.
Automatically create the project and strictly complete the full systematic translation workflow required by the templates, with no omissions.
If the source language is English and the target language is Simplified Chinese, default to `edition_type: bilingual_parallel` and produce both the target-only Simplified Chinese EPUB and the English-Chinese bilingual parallel EPUB as private artifacts. For other language pairs, produce a bilingual parallel EPUB only when I explicitly request it.
During translation, run the per-chapter post-translation full check and fix gate for every chapter. After the first EPUB, run stratified random spot-checking and defect-family closure. Translation-quality defect families must first be closed inside the book project, then reusable lessons must be merged into `skills/translation-quality-defect-families/SKILL.md`.
```

Personal-use projects must be created under `books/private/{target}/{number}_{target_language_title}_{target_language_author}/`. The final versioned artifact is under `output/private_artifacts/`; it is not a public release and must not be published to GitHub.

## Post-EPUB Refinement Prompts (Optional)

After the first EPUB has been generated, do not just tell the AI "polish this book." Choose one of these two prompts:

- **Prompt B: Full-chapter recheck and repair.** Use this when the project is old, lacks zero-issue `qa/chapter_controls/*.control.md` records, or chapter-level checking is uncertain.
- **Prompt C: Stratified random spot-check and defect-family closure.** Use this for the mandatory post-EPUB release-confidence gate. It finds systemic blind spots, audits similar cases across the book, fixes them, and reruns new-seed rounds before release/private artifact creation.

Recommended order: for old or uncertain projects, run **Prompt B** first, then **Prompt C**. If every chapter already has reliable zero-issue control records, **Prompt C** may run directly.

### Prompt B: Full-Chapter Recheck And Repair

```text
Book project: {book project path, for example books/{target}/{number}_{target_language_title}_{target_language_author}}

First read AGENTS.md, this book's SKILL.md if present, template/epub_pipeline/README.md, template/epub_pipeline/common/README.md, template/epub_pipeline/common/prompts/08a_chapter_post_translation_control.md, template/epub_pipeline/common/references/quality_gate_framework.md, the target-language quality framework, and `skills/translation-quality-defect-families/SKILL.md`.

Set a /goal: run full post-translation recheck and repair for every translated chapter in this book. For each chapter, compare the whole source chapter, whole translated chapter, and reader-facing context. Check at least fidelity, omissions, mistranslations, target-language readability, literary force, reader engagement, teaching/explanatory rhythm where applicable, terminology stability, names/places/book titles/ship names/institutions, titles and subtitles, notes, figure/table/formula/image text interfaces, source-syntax residue, stiff or overly literal prose, over-explanation, unsupported invented additions, reader-facing AI/production traces, abnormal spaces/mojibake, and legacy print residue.

Different chapters may be processed in parallel if the agent environment supports it, but each chapter must close independently. Every round must inspect the whole chapter. If any issue is found, fix that chapter, but record the round as `FIXED_RECHECK_REQUIRED`, not PASS. Append a new full-chapter recheck. A chapter only passes when the latest round records `scope: FULL_CHAPTER`, `issues_found: 0`, `fixes_applied: 0`, `unresolved_blocking_issues: 0`, `latest_round_status: PASS`, and `allow_next_chapter: true`.

If any chapter reveals a recurring translation-quality defect family, such as short-sentence fragmentation, metaphor collision, enumerative punctuation drag, unclear pronouns, source-syntax residue, terminology drift, title overload, over-explanation, or invented additions, use `skills/translation-quality-defect-families/SKILL.md`: record how it was found, classified, audited with low-token methods, fixed, and rechecked. Use `rg`, glossary rows, forbidden renderings, title maps, chapter controls, and small-context source comparison before asking an agent to review candidate passages. Do not ask an agent to blindly reread the whole book.

When done, create or update `qa/chapter_controls/*.control.md`, needed `qa/fidelity/`, `qa/readability/`, `qa/terminology/`, and `qa/gates/` records, and promote/update passing chapters in `chapters/final/`. Rebuild the EPUB and run available chapter-control, preflight, publication lint, asset, and EPUBCheck commands. Report repaired chapters, defect families, validation results, and what still needs Prompt C.
```

### Prompt C: Stratified Random Spot-Check And Defect-Family Closure

`N` means the number of consecutive clean spot-check rounds required before exit: `1` is the token-saving minimum, `2` is recommended for normal books, and `3` is stricter for terminology-heavy, scientific, mathematical, diagram-heavy, or high-quality editions.

```text
Book project: {book project path, for example books/{target}/{number}_{target_language_title}_{target_language_author}}
Consecutive clean spot-check rounds N: {1/2/3; default 2}

First read AGENTS.md, this book's SKILL.md if present, template/epub_pipeline/README.md, template/epub_pipeline/common/README.md, template/epub_pipeline/common/prompts/16a_stratified_random_spotcheck.md, template/epub_pipeline/common/references/stratified_random_spotcheck.md, template/epub_pipeline/common/references/quality_gate_framework.md, the relevant cover, book-info/frontmatter, asset, and release rules, and `skills/translation-quality-defect-families/SKILL.md`.

Set a /goal: run stratified random spot-checking and defect-family closure for the already generated EPUB, then regenerate release or private artifact output after the gate passes. Do not treat this as ordinary polishing. The purpose is to discover systemic blind spots, audit similar cases across the whole reader-facing book, close fixes, and rerun new-seed rounds.

Run stratified random sampling over reader-facing audit units, not pages and not just paragraphs. Cover every existing stratum: paragraph, table, figure, formula/proof, and caption/note. Use at least 2 independent review agents that do not read each other's conclusions. Save seed, manifest, samples, evidence, reviews, fixes/fix_log.md, and verification/closure_check.md under `reviews/random_spotcheck/round_XXX/`.

If any sample finds P0/P1/P2, any item score <80, reader-incomprehensible text, fidelity drift, factual/terminology/name/title/note/figure/formula errors, source-syntax residue, stiff literal prose, short-sentence fragmentation, metaphor collision, enumerative punctuation drag, unclear pronouns, over-explanation, or invented additions, classify it as a defect family in the same round. Audit the whole book for similar cases and fix every confirmed match. Do not fix only the sampled unit, and do not wait for a second failed round before checking the whole book.

For translation-quality defect families, use low-token auditing first: `rg`, `glossary/terms.csv`, `forbidden_body_renderings`, title maps, chapter controls, sample manifests, and small-context source comparison. Send only candidate passages to agents. Merge reusable lessons into `skills/translation-quality-defect-families/SKILL.md`.

After every fix, rebuild the EPUB and run another new-seed spot-check round. Exit only when the most recent N new-seed rounds PASS, all discovered defect families are closed, `npm run review:random-validate:pass` passes, and release_confidence satisfies the template requirement.

After passing, clean or rebuild staging, regenerate the EPUB, and run publication lint, asset manifest, cover output, reader-facing policy, EPUBCheck, and release or private artifact scripts. For public-domain or licensed projects, the publishable EPUB must be written under this book's output/release/, and release_state.json.latest_status must be PASS. For personal-use projects, the final private artifact must be written under output/private_artifacts/, and private_artifact_state.json.latest_status must be PASS. Report the release EPUB or private artifact path, spot-check rounds, fix summary, validation command results, and remaining risks.
```

## Key Places To Know

- `.\template\epub_pipeline`: check which source-language and source-to-target templates currently exist. The AI uses this to decide whether to run the existing-template prompt or the new-template prompt.
- `.\tools\lifebook-launcher`: LifeBook Launcher client install and launch folder. Users need this path to use the LifeBook project and install OpenCode.
- `.\doc\public\user_prompt`: the public prompts live here. Read or edit these when the prompt needs review or manual adjustment.
- `.\books\zh-Hans`: the most important output area for Simplified Chinese books. After translation succeeds, open the matching book folder and check `output\release\`; only release artifacts count as publishable results.
- `.\books\private`: private-use book project folder. Non-public-domain private translations should keep source text, translations, QA, EPUB output, and `output\private_artifacts\` private artifacts here only; this folder is ignored by Git and is not published to GitHub.

## What Are The Four Translation Prompts?

- `doc/public/user_prompt/book_translation_existing_template.md`: use when this repository already has the matching source-language template, such as Japanese to Simplified Chinese, English to Simplified Chinese, or Ancient Greek to Simplified Chinese.
- `doc/public/user_prompt/book_translation_new_template.md`: use when this repository does not yet have the matching source-language template, such as the first French to Simplified Chinese book.
- `doc/public/user_prompt/book_translation_private_existing_template.md`: use for a personal-use local source when the matching source-language template already exists.
- `doc/public/user_prompt/book_translation_private_new_template.md`: use for a personal-use local source when the matching source-language template does not exist yet.
- `doc/public/user_prompt/how_to_use_book_translation_prompts.md`: a shorter beginner-facing guide that only explains how to fill in the three items.

If it is unclear which one applies, ask the AI to check whether the template exists first. Normal users do not need to understand `language-pair template name`, slug, profile, release version, or npm commands.

## Which Client Should I Use?

| Client | Good for | How to use the prompt |
| --- | --- | --- |
| Codex App | Desktop UI, diffs, terminal, browser, Git review | Open the repo, create a thread, paste the `/goal` |
| Claude Code | Terminal users who want a command-line agent | Start Claude Code in the repository and paste the prompt |
| LifeBook Launcher | Fewest manual steps;<br>requires OpenCode client support | Open Launcher and install OpenCode.<br>OpenCode supports most mainstream models, such as DeepSeek and Doubao.<br>Choose the book-translation task in OpenCode and paste the three items; see the [full example](#easiest-starter-prompt) |
| Google Antigravity | AI IDE with agent workflows | Open the repo workspace and paste the prompt into the agent box |

## LifeBook Launcher

For people who prefer not to handle project and client setup manually, use LifeBook Launcher. Launcher can download and open the OpenCode client. OpenCode supports most mainstream AI models, including DeepSeek and Doubao. Before use, configure the model provider API key inside OpenCode.

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
