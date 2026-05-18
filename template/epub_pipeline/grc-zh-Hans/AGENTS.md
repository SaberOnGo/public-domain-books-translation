# grc-zh-Hans Agent Instructions / 古希腊文到简体中文模板 Agent 指令

This file is for AI agents using the `grc-zh-Hans` template.

本文件供使用 `grc-zh-Hans` 模板的 AI agent 读取。

## Scope / 适用范围

- Source language: Ancient Greek.
- 原文语言：古希腊文。

- Target language: Simplified Chinese.
- 目标语言：简体中文。

- Intended contributors must be able to read Simplified Chinese instructions. English can appear in parallel for precision.
- 面向本模板的贡献者必须能读到简体中文说明。为了精确，英文可以并列出现。

## Mandatory Rules / 强制规则

- Create each new book project with `books/scripts/create_book_project.py`; it copies `template/epub_pipeline/common` first, then overlays `template/epub_pipeline/grc-zh-Hans` into `books/zh-Hans/{number}_{book_id_slug}/`.
- 必须用 `books/scripts/create_book_project.py` 创建每本新书；脚本会先复制 `template/epub_pipeline/common`，再覆盖复制 `template/epub_pipeline/grc-zh-Hans` 到 `books/zh-Hans/{number}_{book_id_slug}/` 书籍工程。

- If the work is scientific, mathematical, astronomical, diagram-heavy, table-heavy, or proof-heavy, overlay `template/epub_pipeline/profiles/classical-science-zh-Hans` after this language template.
- 如果作品属于科学、数学、天文学、图表密集、表格密集或证明密集型作品，必须在本语言模板之后叠加 `template/epub_pipeline/profiles/classical-science-zh-Hans`。

- Do not write book-specific files into this template directory.
- 不得把具体书籍文件写入本模板目录。

- Important files and prompts for this template must include Simplified Chinese. English may be included in parallel, but English-only important instructions are not acceptable here.
- 本模板的重要文件和 prompt 必须包含简体中文。英文可以并列，但重要说明不能只写英文。

- Preserve Ancient Greek source evidence, edition information, editor information, and rights checks before translation.
- 翻译前必须保留古希腊文来源证据、版本信息、编辑者信息并完成版权核查。

- Do not use modern Chinese translations as source material or hidden reference material.
- 不得使用现代中文译本作为翻译底本或隐藏参考材料。

- A modern English, French, German, or other translation may be used only as a reference witness when its copyright and use boundary are recorded.
- 现代英译、法译、德译或其他译本只能在版权状态和使用边界记录清楚后作为参考证据。

- Translation must be based on the Ancient Greek source, not on a second-language pivot translation.
- 翻译必须从古希腊文底本出发，不得从第二语言译本转译。

- Record and preserve textual variants, uncertain OCR, damaged readings, lacunae, editorial conjectures, and ambiguous grammar.
- 必须记录并保留异文、OCR 不确定处、残损读法、脱文、编辑者拟补和语法歧义。

- Before batch translation, create `metadata/source_witness_manifest.md` and `qa/textual/textual_uncertainty_log.md`.
- 批量翻译前必须创建 `metadata/source_witness_manifest.md` 和 `qa/textual/textual_uncertainty_log.md`。

- Do not silently normalize Ancient Greek names, places, divine names, technical terms, or variant readings. Record the transliteration and Chinese rendering policy.
- 不得静默统一古希腊人名、地名、神名、技术术语或异文读法；必须记录转写和中文译名策略。

- Before building or publishing an EPUB, run `node scripts/publication_lint.js --target=zh-Hans --write-report` and fix all hard errors.
- 构建或发布 EPUB 前，必须运行 `node scripts/publication_lint.js --target=zh-Hans --write-report`，并修复所有硬错误。

- After the first full-book EPUB and after each post-EPUB refinement pass, at least two independent agents must run the stratified random spot-check gate. The sampled population is reader-facing audit units, including paragraphs, tables, figures, formulas/proof blocks, captions, and notes. Both agents, fix closure, and `npm run review:random-validate:pass` must pass before refinement can be considered complete.
- 第一版全书 EPUB 生成后，以及每轮 EPUB 后精校完成后，必须由至少两个独立 Agent 执行分层随机抽检门禁。抽样总体是读者可见审计单元，包括正文段落、表格、图片、公式/证明块、图注和注释。两个 Agent、修复闭环和 `npm run review:random-validate:pass` 都通过后，才可认为精校完成。
- After random spot-check closure, create a versioned EPUB release under `output/release/`; `output/book.epub` alone is not a publishable final artifact.
- 随机抽检闭环通过后，必须在 `output/release/` 下创建带版本号的 EPUB release；只有 `output/book.epub` 不是可发布最终产物。

## Human Checkpoints / 人类可选检查点

- `metadata/source_evidence.md`
- `metadata/source_witness_manifest.md`
- `metadata/rights_checklist.md`
- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `glossary/terms.csv`
- `qa/textual/textual_uncertainty_log.md`
- `qa/pretranslation/pretranslation_report.md`
- `qa/chapter_controls/{NNN_slug}.control.md`
- `qa/gates/{NNN_slug}.gate.md`
- 启用 profile 时的 `metadata/reference_witness_policy.md`
- 启用 profile 时的 `qa/technical/*.md`
- `reviews/random_spotcheck/random_sample_manifest.json`
- `reviews/random_spotcheck/round_XXX/`
- `reviews/agent_a/random_spotcheck_review.md`
- `reviews/agent_b/random_spotcheck_review.md`
- `output/release/book_vX.X.X.epub`
- `output/release/release_note_vX.X.X.md`
- `output/release/release_state.json`

If no human feedback is required, continue only when the relevant report says `PASS`.

如果不需要等待人工反馈，也只能在对应报告明确 `PASS` 后继续。
