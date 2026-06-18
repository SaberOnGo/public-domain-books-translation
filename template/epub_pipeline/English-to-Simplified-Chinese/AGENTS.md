# English-to-Simplified-Chinese Agent Instructions / 英文到简体中文模板 Agent 指令

This file is for AI agents using the `English-to-Simplified-Chinese` template.

本文件供使用 `English-to-Simplified-Chinese` 模板的 AI agent 读取。

## Scope / 适用范围

- Source language: English.
- 原文语言：英文。

- Target language: Simplified Chinese.
- 目标语言：简体中文。

- Intended contributors must be able to read Simplified Chinese instructions. English can appear in parallel for precision.
- 面向本模板的贡献者必须能读到简体中文说明。为了精确，英文可以并列出现。

## Mandatory Rules / 强制规则

- Create each new book project with `books/scripts/create_book_project.py`; it copies `template/epub_pipeline/common` first, then overlays `template/epub_pipeline/English-to-Simplified-Chinese` into `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`.
- 必须用 `books/scripts/create_book_project.py` 创建每本新书；脚本会先复制 `template/epub_pipeline/common`，再覆盖复制 `template/epub_pipeline/English-to-Simplified-Chinese` 到 `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/` 书籍工程。

- Do not write book-specific files into this template directory.
- 不得把具体书籍文件写入本模板目录。

- Important files and prompts for this template must include Simplified Chinese. English may be included in parallel, but English-only important instructions are not acceptable here.
- 本模板的重要文件和 prompt 必须包含简体中文。英文可以并列，但重要说明不能只写英文。

- Preserve source evidence and rights checks before translation. Public projects require public-domain or licensed source evidence; private-use projects require a user-provided local source file and `metadata/private_use_declaration.md`.
- 翻译前必须保留来源证据并完成版权核查。公开项目必须有公版或授权来源证据；私人自用项目必须有用户提供的本地书源文件和 `metadata/private_use_declaration.md`。

- Do not use modern Chinese translations as source material or hidden reference material.
- 不得使用现代中文译本作为翻译底本或隐藏参考材料。

- Translation quality must be faithful, readable, and natural in Chinese. It must not be mechanical, over-compressed, or embellished beyond the source.
- 译文必须忠实、可读，并且是自然的中文；不得机械直译、过度压缩或无依据加戏。

- During the translation call itself, treat natural Chinese prose as the first hard constraint. Keep the prompt focused on the source passage, the top 5-8 style rules, and only the relevant terms; do not mix release, EPUB, lint, QA-file, or versioning instructions into the translation prompt.
- 在翻译调用本身，必须把自然中文正文作为第一硬约束。prompt 只保留原文片段、最关键的 5-8 条文体规则和当前相关术语；不得把 release、EPUB、lint、QA 文件或版本化产物规则混入翻译 prompt。

- Translation calls output only translation text. QA reports, explanations, term audits, and workflow notes belong in later QA files, not in `chapters/translated/`.
- 翻译调用只输出译文。QA 报告、解释、术语审计和流程记录属于后续 QA 文件，不得写入 `chapters/translated/`。

- No translated chapter may enter `chapters/final/` without chapter controls, review, and gate pass records.
- 任何章节没有译后控制、审校和门禁 PASS 记录，不得进入 `chapters/final/`。

- After each translated chapter is written, immediately run the full post-translation check and fix node for that chapter only in `qa/chapter_controls/{NNN_slug}.control.md`. It must cover the current chapter's body text, notes, terminology, reader-facing wording, readability, polish, plain-language clarity without flattening specialist quality, and text interfaces for figures/tables/formulas/images. Do not limit the check to items named by the user. If any issue is found and fixed, that round must be `FIXED_RECHECK_REQUIRED`, not PASS; append a new full-chapter recheck. Only a latest round with `scope: FULL_CHAPTER`, `issues_found: 0`, `fixes_applied: 0`, `unresolved_blocking_issues: 0`, `latest_round_status: PASS`, and `allow_next_chapter: true` may unlock the next chapter.
- 每章译文写入后，必须立即只针对该章执行 `qa/chapter_controls/{NNN_slug}.control.md` 中的“每章译后，全量检查并修复节点”。检查范围必须覆盖当前章正文、注释、术语、读者可见文字、通俗化、可读性、润色，以及图表/表格/公式/图片的文字接口，不得只检查用户点名项目。译文要尽量顺读、有趣、不费劲，但不得为了通俗化损害专业质量。发现并修复问题的轮次只能记为 `FIXED_RECHECK_REQUIRED`，不得 PASS；必须追加新的整章复查。只有最近一轮 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` 时，才可进入下一章。

- The chapter control must include a Chinese-only readability pass: score the translated chapter without looking at the English source first. A score below 4/5, more than one awkward sentence in a 20-sentence read-aloud sample, or breathless key sentences blocks progress even if the facts are mostly correct.
- 章节控制必须包含“只看中文”的可读性复查：先不看英文原文，只读译文评分。中文独立阅读低于 4/5、20 句朗读中明显拗口超过 1 句，或关键句不断气时，即使事实大体准确也不得继续。

- After the first full-book EPUB and after each post-EPUB refinement pass, at least two independent agents must run the stratified random spot-check gate. The sampled population is reader-facing audit units, including paragraphs, tables, figures, formulas/proof blocks, captions, and notes. Both agents, fix closure, and `npm run review:random-validate:pass` must pass before refinement can be considered complete.
- 第一版全书 EPUB 生成后，以及每轮 EPUB 后精校完成后，必须由至少两个独立 Agent 执行分层随机抽检门禁。抽样总体是读者可见审计单元，包括正文段落、表格、图片、公式/证明块、图注和注释。两个 Agent、修复闭环和 `npm run review:random-validate:pass` 都通过后，才可认为精校完成。
- After random spot-check closure, create a versioned artifact: public-domain or licensed projects use `output/release/`, while `private_use` projects use local-only `output/private_artifacts/`; `output/book.epub` alone is not a final artifact.
- 随机抽检闭环通过后，必须创建带版本号产物：公版或授权项目使用 `output/release/`，`private_use` 项目使用仅限本地的 `output/private_artifacts/`；只有 `output/book.epub` 不是最终产物。

- Before building or publishing an EPUB, run `node scripts/publication_lint.js --target=zh-Hans --write-report` and fix all hard errors.
- 构建或发布 EPUB 前，必须运行 `node scripts/publication_lint.js --target=zh-Hans --write-report`，并修复所有硬错误。

- Node.js dependencies are shared under `books/node_modules/`. Install once from `books/`; do not create duplicate per-book `node_modules/` directories.
- Node.js 依赖统一共享在 `books/node_modules/`。应在 `books/` 下安装一次；不要为每本书重复创建 `node_modules/`。

- Do not allow semicolon overuse, visible abnormal spaces between Chinese text, legacy print page-number tables, or garbled characters into final output.
- 不得让分号滥用、中文可见异常空格、旧纸书页码目录或乱码进入最终成书。

- Old English printed tables of contents often use `--` to chain several topics into one chapter title. Do not mechanically translate those chains into multiple Chinese em dashes; create a short navigation title, a readable display title, and an optional subtitle when needed.
- 英文旧纸书目录常用 `--` 把多个主题连成一个章节标题。不得机械翻成一串中文破折号；必要时应设计短目录题名、页面主标题和可选副标题。

- Important proper nouns must follow `glossary/proper_nouns.csv` and `references/proper_noun_display_policy.md`. If the user does not set a value, use policy `3`: first natural body occurrence as translated name plus source in parentheses, then translated name. Title occurrences do not count as first body occurrences.
- 重点专有名词必须遵守 `glossary/proper_nouns.csv` 和 `references/proper_noun_display_policy.md`。用户未设置时使用策略 `3`：第一次正文自然出现写译名加原文括注，后续使用译名。标题中的出现不计入正文首次出现。

- Names in chapter titles, subtitles, and EPUB navigation labels must use Chinese translated names only. Do not put English original names or parenthetical English names in titles; place them at the first natural body occurrence, in a note, or in the glossary according to the proper-noun register.
- 章节标题、副标题和 EPUB 目录题名中的人名只使用中文译名。不得把英文原名或英文括注放进标题；英文原名应按重点专名译表放在正文第一次自然出现处、译注或术语表中。

- Common nouns, object names, clothing names, material names, and action terms must be translated into Chinese without original source terms in parentheses. The first-body-mention English rule applies to transliterated names, not to ordinary nouns that can be translated accurately.
- 普通名词、器物名、衣物名、材料名和动作名必须译成中文，正文不得附加原文词括注。正文首次出现保留英文原名的规则只适用于音译人名，不适用于能准确翻译的普通名词。

- Historical terms, institutional names, status titles, technical terms, and culture-loaded terms must not default to `Chinese term (source term)` in body text. Prefer a readable Chinese term in the body and put the source term, definition, and translation rationale in a chapter note, endnote, or glossary entry with a note marker such as `[1]`. Body parenthetical source terms are rare exceptions and require a recorded reason.
- 历史术语、制度名、身份称谓、专业术语和文化负载词不得默认写成正文里的 `中文译名（source term）`。正文优先使用可读的中文译名，原词、定义和译名理由放入本章译注、章末注或术语表，并用 `[1]` 等注号指向。正文括注原词只能作为少量例外，且必须记录理由。

- Note markers must use only `[1]`, `(1)` / `（1）`, or `注1`. Proper-noun source parentheses such as `尼禄（Nero）` are not note markers; policy `5` adds a separate approved marker such as `尼禄（Nero）[1]`.
- 注号只能使用 `[1]`、`(1)` / `（1）`、`注1`。`尼禄（Nero）` 这类专名原文括注不是注号；策略 `5` 才在其后另加合规注号，例如 `尼禄（Nero）[1]`。

- Delete printed-book separators such as `* * * * *`, `*****`, `----`, or `---` from body text. Do not replace them with another visible separator.
- 删除旧纸书正文分隔符，例如 `* * * * *`、`*****`、`----` 或 `---`。不得替换成另一种可见分隔符。

## Human Checkpoints / 人类可选检查点

- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `glossary/terms.csv`
- `glossary/proper_nouns.csv`
- `qa/pretranslation/pretranslation_report.md`
- `qa/chapter_controls/{NNN_slug}.control.md`
- `qa/gates/{NNN_slug}.gate.md`
- `preproduction/stage2_sample/sample_book.epub`
- `output/publication_lint.json`
- `reviews/random_spotcheck/random_sample_manifest.json`
- `reviews/random_spotcheck/round_XXX/`
- `reviews/agent_a/random_spotcheck_review.md`
- `reviews/agent_b/random_spotcheck_review.md`
- Public/licensed: `output/release/book_vX.X.X.epub`, `output/release/release_note_vX.X.X.md`, `output/release/release_state.json`
- Private-use: `output/private_artifacts/{title}_private_vX.X.X.epub`, `output/private_artifacts/private_artifact_notes.md`, `output/private_artifacts/private_artifact_state.json`
- `reviews/scorecards/final_quality_score.md`

If no human feedback is required, continue only when the relevant report says `PASS`.

如果不需要等待人工反馈，也只能在对应报告明确 `PASS` 后继续。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.
