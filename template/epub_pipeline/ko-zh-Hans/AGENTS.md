# ko-zh-Hans Agent Instructions / 韩语/朝鲜语到简体中文模板 Agent 指令

This file is for AI agents using the `ko-zh-Hans` template.

本文件供使用 `ko-zh-Hans` 模板的 AI agent 读取。

## Scope / 适用范围

- Source language: Korean.
- 原文语言：韩语/朝鲜语。

- Target language: Simplified Chinese.
- 目标语言：简体中文。

- Intended contributors must be able to read Simplified Chinese instructions. English can appear in parallel for precision.
- 面向本模板的贡献者必须能读到简体中文说明。为了精确，英文可以并列出现。

## Mandatory Rules / 强制规则

- Create each new book project with `books/scripts/create_book_project.py`; it copies `template/epub_pipeline/common` first, then overlays `template/epub_pipeline/ko-zh-Hans` into `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`.
- 必须用 `books/scripts/create_book_project.py` 创建每本新书；脚本会先复制 `template/epub_pipeline/common`，再覆盖复制 `template/epub_pipeline/ko-zh-Hans` 到 `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/` 书籍工程。

- Do not write book-specific files into this template directory.
- 不得把具体书籍文件写入本模板目录。

- Important files and prompts for this template must include Simplified Chinese. English may be included in parallel, but English-only important instructions are not acceptable here.
- 本模板的重要文件和 prompt 必须包含简体中文。英文可以并列，但重要说明不能只写英文。

- Preserve Korean source evidence, source edition information, text-form information, and rights checks before translation. Public projects require public-domain or licensed source evidence; private-use projects require a user-provided local source file and `metadata/private_use_declaration.md`.
- 翻译前必须保留韩语/朝鲜语来源证据、来源版本信息、底本文字形态和版权核查。公开项目必须有公版或授权来源证据；私人自用项目必须有用户提供的本地书源文件和 `metadata/private_use_declaration.md`。

- Do not use modern Chinese translations, modern annotated editions, commercial e-books, or pirate sites as source material or hidden reference material.
- 不得使用现代中文译本、现代校注本、商业电子书或盗版站点作为翻译底本或隐藏参考材料。

- A modern Korean scholarly edition, modern translation, Chinese translation, English translation, or commentary may be used only as a reference when its copyright status and use boundary are recorded; it must not be copied into the translation.
- 现代韩文/朝鲜文校注本、现代译本、中文译本、英译本或研究注释，只能在版权状态和使用边界记录清楚后作为参考；不得复制进译文。

- Translation must be based on the Korean source, not on a Chinese or English pivot translation.
- 翻译必须从韩语/朝鲜语底本出发，不得从中文或英文转译。

- Record and preserve Hangul/Hanja form, mixed-script passages, old orthography, source notes, editorial notes, OCR uncertainty, and ambiguous readings.
- 必须记录并保留韩文/汉字混排、旧拼写、旧汉字词、底本注、编者注、OCR 不确定和歧义读法。

- Before batch translation, create `metadata/korean_source_profile.md` and `qa/textual/korean_textual_notes.md`.
- 批量翻译前必须创建 `metadata/korean_source_profile.md` 和 `qa/textual/korean_textual_notes.md`，并记录韩文/汉字混排、日据时期词汇、现代输入者说明、底本来源和疑难读法。

- Do not silently normalize Korean names, place names, era terms, art terms, Buddhist terms, clothing/object terms, or variant readings. Record the Chinese rendering policy.
- 不得静默统一韩语/朝鲜语人名、地名、时代词、艺道词、佛教词、衣物器物词或异体读法；必须记录中文译名策略。

- Sensual, violent, pathological, or coercive content must be treated as literary narration. Do not eroticize, sensationalize, sanitize, or add moral commentary not present in the source.
- 官能、暴力、病态心理或强制关系内容必须按文学叙事处理；不得色情化、猎奇化、净化处理，也不得添加原文没有的道德评语。

- Before building or publishing an EPUB, run `node scripts/publication_lint.js --target=zh-Hans --write-report` and fix all hard errors.
- 构建或发布 EPUB 前，必须运行 `node scripts/publication_lint.js --target=zh-Hans --write-report`，并修复所有硬错误。

- After the first full-book EPUB and after each post-EPUB refinement pass, at least two independent agents must run the stratified random spot-check gate. The sampled population is reader-facing audit units, including paragraphs, tables, figures, formulas/proof blocks, captions, and notes. Both agents, fix closure, and `npm run review:random-validate:pass` must pass before refinement can be considered complete.
- 第一版全书 EPUB 生成后，以及每轮 EPUB 后精校完成后，必须由至少两个独立 Agent 执行分层随机抽检门禁。抽样总体是读者可见审计单元，包括正文段落、表格、图片、公式/证明块、图注和注释。两个 Agent、修复闭环和 `npm run review:random-validate:pass` 都通过后，才可认为精校完成。

- After random spot-check closure, create a versioned artifact: public-domain or licensed projects use `output/release/`, while `private_use` projects use local-only `output/private_artifacts/`; `output/book.epub` alone is not a final artifact.
- 随机抽检闭环通过后，必须创建带版本号产物：公版或授权项目使用 `output/release/`，`private_use` 项目使用仅限本地的 `output/private_artifacts/`；只有 `output/book.epub` 不是最终产物。

## Human Checkpoints / 人类可选检查点

- `metadata/source_evidence.md`
- `metadata/rights_checklist.md`
- `metadata/korean_source_profile.md`
- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `glossary/terms.csv`
- `qa/textual/korean_textual_notes.md`
- `qa/pretranslation/pretranslation_report.md`
- `qa/chapter_controls/{NNN_slug}.control.md`
- `qa/gates/{NNN_slug}.gate.md`
- `preproduction/stage1/production_spec.md`
- `preproduction/stage2_sample/sample_book.epub`
- `output/publication_lint.json`
- `reviews/random_spotcheck/round_XXX/`
- `reviews/agent_a/random_spotcheck_review.md`
- `reviews/agent_b/random_spotcheck_review.md`
- Public/licensed: `output/release/book_vX.X.X.epub`, `output/release/release_notes.md`, `output/release/release_state.json`
- Private-use: `output/private_artifacts/{title}_private_vX.X.X.epub`, `output/private_artifacts/private_artifact_notes.md`, `output/private_artifacts/private_artifact_state.json`
- `reviews/scorecards/final_quality_score.md`

If no human feedback is required, continue only when the relevant report says `PASS`.

如果不需要等待人工反馈，也只能在对应报告明确 `PASS` 后继续。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.
