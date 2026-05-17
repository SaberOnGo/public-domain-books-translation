# en-zh-Hans Agent Instructions / 英文到简体中文模板 Agent 指令

This file is for AI agents using the `en-zh-Hans` template.

本文件供使用 `en-zh-Hans` 模板的 AI agent 读取。

## Scope / 适用范围

- Source language: English.
- 原文语言：英文。

- Target language: Simplified Chinese.
- 目标语言：简体中文。

- Intended contributors must be able to read Simplified Chinese instructions. English can appear in parallel for precision.
- 面向本模板的贡献者必须能读到简体中文说明。为了精确，英文可以并列出现。

## Mandatory Rules / 强制规则

- Copy `template/epub_pipeline/common` first, then overlay `template/epub_pipeline/en-zh-Hans` into a book project under `books/{book_id_slug}/`.
- 必须先复制 `template/epub_pipeline/common`，再覆盖复制 `template/epub_pipeline/en-zh-Hans` 到 `books/{book_id_slug}/` 书籍工程。

- Do not write book-specific files into this template directory.
- 不得把具体书籍文件写入本模板目录。

- Important files and prompts for this template must include Simplified Chinese. English may be included in parallel, but English-only important instructions are not acceptable here.
- 本模板的重要文件和 prompt 必须包含简体中文。英文可以并列，但重要说明不能只写英文。

- Preserve source evidence and rights checks before translation.
- 翻译前必须保留来源证据并完成版权核查。

- Do not use modern Chinese translations as source material or hidden reference material.
- 不得使用现代中文译本作为翻译底本或隐藏参考材料。

- Translation quality must be faithful, readable, and natural in Chinese. It must not be mechanical, over-compressed, or embellished beyond the source.
- 译文必须忠实、可读，并且是自然的中文；不得机械直译、过度压缩或无依据加戏。

- No translated chapter may enter `chapters/final/` without chapter controls, review, and gate pass records.
- 任何章节没有译后控制、审校和门禁 PASS 记录，不得进入 `chapters/final/`。

- After each post-EPUB refinement pass, at least two independent agents must randomly spot-check no fewer than ten reader-facing Chinese paragraphs each. Both agents must pass the random spot-check threshold before refinement can be considered complete.
- 每轮 EPUB 后精校完成后，必须由至少两个独立 Agent 各随机抽检不少于十个读者可见中文正文段落；两个 Agent 都通过随机抽检门槛后，才可认为精校完成。

- Before building or publishing an EPUB, run `node scripts/publication_lint.js --target=zh-Hans --write-report` and fix all hard errors.
- 构建或发布 EPUB 前，必须运行 `node scripts/publication_lint.js --target=zh-Hans --write-report`，并修复所有硬错误。

- Node.js dependencies are shared under `books/node_modules/`. Install once from `books/`; do not create duplicate per-book `node_modules/` directories.
- Node.js 依赖统一共享在 `books/node_modules/`。应在 `books/` 下安装一次；不要为每本书重复创建 `node_modules/`。

- Do not allow semicolon overuse, visible abnormal spaces between Chinese text, legacy print page-number tables, or garbled characters into final output.
- 不得让分号滥用、中文可见异常空格、旧纸书页码目录或乱码进入最终成书。

- Old English printed tables of contents often use `--` to chain several topics into one chapter title. Do not mechanically translate those chains into multiple Chinese em dashes; create a short navigation title, a readable display title, and an optional subtitle when needed.
- 英文旧纸书目录常用 `--` 把多个主题连成一个章节标题。不得机械翻成一串中文破折号；必要时应设计短目录题名、页面主标题和可选副标题。

- Names in chapter titles, subtitles, and EPUB navigation labels must use Chinese translated names only. A title occurrence does not count as the first body occurrence for a name. Do not put English original names or parenthetical English names in titles; place them at the first natural body occurrence, in a note, or in the glossary.
- 章节标题、副标题和 EPUB 目录题名中的人名只使用中文译名。标题中的出现不计入该人名的“正文首次出现”。不得把英文原名或英文括注放进标题；英文原名应放在正文第一次自然出现处、译注或术语表中。

- Common nouns, object names, clothing names, material names, and action terms must be translated into Chinese without original source terms in parentheses. The first-body-mention English rule applies to transliterated names, not to ordinary nouns that can be translated accurately.
- 普通名词、器物名、衣物名、材料名和动作名必须译成中文，正文不得附加原文词括注。正文首次出现保留英文原名的规则只适用于音译人名，不适用于能准确翻译的普通名词。

- Delete printed-book separators such as `* * * * *`, `*****`, `----`, or `---` from body text. Do not replace them with another visible separator.
- 删除旧纸书正文分隔符，例如 `* * * * *`、`*****`、`----` 或 `---`。不得替换成另一种可见分隔符。

## Human Checkpoints / 人类可选检查点

- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `glossary/terms.csv`
- `qa/pretranslation/pretranslation_report.md`
- `qa/chapter_controls/{NNN_slug}.control.md`
- `qa/gates/{NNN_slug}.gate.md`
- `preproduction/stage2_sample/sample_book.epub`
- `output/publication_lint.json`
- `reviews/random_spotcheck/random_sample_manifest.json`
- `reviews/agent_a/random_spotcheck_review.md`
- `reviews/agent_b/random_spotcheck_review.md`
- `reviews/scorecards/final_quality_score.md`

If no human feedback is required, continue only when the relevant report says `PASS`.

如果不需要等待人工反馈，也只能在对应报告明确 `PASS` 后继续。
