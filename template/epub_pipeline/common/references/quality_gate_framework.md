# Language-Neutral Quality Gate Framework

This file defines quality-gate concepts that apply to every translation direction. It intentionally avoids target-language style rules.

本文件定义所有翻译方向都适用的质量门禁概念。它刻意不写入某个目标语言的文体规则。

## Universal Gates / 通用门禁

- Source and rights evidence must exist before translation starts.
- 翻译开始前必须已有来源证据和版权核查记录。
- A book-level research note and style profile must exist before batch translation.
- 批量翻译前必须已有本书专项研究和文体画像。
- Trial translation must pass before full chapter production.
- 试译通过后才能进入整章批量生产。
- Every chapter must pass fidelity, readability, terminology, and final gate checks before it enters `chapters/final/`.
- 每章进入 `chapters/final/` 前，必须通过忠实度、可读性、术语和最终门禁检查。
- EPUB output must pass structural validation before final release.
- 最终发布前，EPUB 必须通过结构校验。
- After the first full-book EPUB and after each post-EPUB refinement pass, the workflow must run the stratified random spot-check module in `references/stratified_random_spotcheck.md`. At least two independent review agents must review deterministic random samples across reader-facing audit-unit strata: paragraphs, tables, figures, formula/proof blocks, captions, and notes. Both agents must pass, every discovered P0/P1/P2 must be fixed and closed, and a new-seed round must pass after rework before refinement can be considered complete.
- 第一版全书 EPUB 生成后，以及每一轮 EPUB 后精校完成后，必须执行 `references/stratified_random_spotcheck.md` 定义的分层随机抽检模块。至少两个独立评审 Agent 必须检查确定性随机样本，抽样层包括正文段落、表格、图片、公式/证明块、图注和注释。两个 Agent 都必须通过；所有发现的 P0/P1/P2 必须修复并定点关闭；返工后还必须使用新 seed 再通过一轮抽检，才可认为精校完成。
- Final publication requires a versioned release from `references/release_versioning.md`: `output/release/book_vX.X.X.epub`, bilingual release note, `release_state.json.latest_status = PASS`, and evidence that the latest random spot-check validation used `--require-pass`.
- 最终发布必须执行 `references/release_versioning.md` 定义的版本化发布：生成 `output/release/book_vX.X.X.epub`、中英文 release note、`release_state.json.latest_status = PASS`，并证明最近一次随机抽检校验使用了 `--require-pass`。

## What Belongs Elsewhere / 哪些内容不属于这里

- Target-language prose standards belong under `template/epub_pipeline/targets/{target}/`.
- 目标语言文体标准应放在 `template/epub_pipeline/targets/{target}/`。
- Source-language interference rules belong under `template/epub_pipeline/{source-target}/`.
- 源语言干扰规则应放在 `template/epub_pipeline/{source-target}/`。
- Book-specific decisions belong inside `books/{target}/{number}_{book_id_slug}/`.
- 具体书籍判断应写入 `books/{target}/{number}_{book_id_slug}/`。
