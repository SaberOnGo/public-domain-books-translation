---
name: epub-pipeline-ko-zh-Hans
description: Use when creating or reviewing Korean to Simplified Chinese public-domain EPUB translation projects with this template.
---

# Korean to Simplified Chinese EPUB Pipeline / 韩语/朝鲜语到简体中文 EPUB 流水线

Use this skill after `books/scripts/create_book_project.py` has copied `template/epub_pipeline/common` and overlaid `template/epub_pipeline/ko-zh-Hans` into `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`.

使用本 skill 前，应先通过 `books/scripts/create_book_project.py` 把 `template/epub_pipeline/common` 复制到 `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`，再覆盖复制 `template/epub_pipeline/ko-zh-Hans`。

## Required Reading / 必读文件

1. `AGENTS.md`
   读取 `AGENTS.md`。

2. `README.md`
   读取 `README.md`。

3. `PIPELINE_SPEC.md`
   读取 `PIPELINE_SPEC.md`。

4. `automation_contract.md`
   读取 `automation_contract.md`。

5. `template/epub_pipeline/targets/zh-Hans/quality_framework/README.md`
   读取简体中文目标语言质量框架。

6. `references/translation_research_universal.md`
   读取 `references/translation_research_universal.md`。

7. `references/quality_standard.md`
   读取 `references/quality_standard.md`。

8. `references/korean_source_notes.md`
   读取韩语/朝鲜语源语言干扰说明。

9. `references/korean_title_strategy.md`
   读取韩语/朝鲜语题名、章题、短标题和译注策略。

10. `references/korean_to_chinese_literary_refinement.md`
    读取韩语/朝鲜语到简体中文文学精修策略。

11. `references/stratified_random_spotcheck.md`
    读取 EPUB 后分层随机抽检门禁。

12. `references/release_versioning.md`
    读取 EPUB 版本化发布、release note 和 `output/release/` 门禁。

## Translation Standard / 翻译标准

- Preserve the source meaning, facts, narrative stance, point of view, emotional temperature, and degree of ambiguity.
- 保留原文意思、事实、叙述姿态、视角、情绪温度和暧昧程度。

- Translate from the Korean source. Use modern Chinese or English translations only as bounded references when rights and use limits are recorded.
- 从韩语/朝鲜语底本翻译。现代中文译本或英译本只能在版权和使用边界记录清楚后作有限参考。

- Write natural Simplified Chinese, not Korean syntax with Chinese words.
- 写自然的简体中文，不要写成中文词语套韩语/朝鲜语句法。

- Do not assume Korean kanji words can be copied into Chinese. Check semantic drift, register, period tone, and reader comprehension.
- 不要默认韩语/朝鲜语汉字词可以照搬成中文。必须检查语义漂移、语体、时代感和读者理解。

- Preserve furigana, old character forms, historical kana, editorial notes, OCR uncertainty, and variant readings as evidence records; translate only what belongs in reader-facing text.
- 韩文/汉字混排、旧字体、旧拼写、编者注、OCR 不确定和异体读法应作为证据记录保存；读者正文只翻译应进入正文的内容。

- Treat sensual, violent, pathological, or coercive material as literary narration. Do not add explicitness, reduce complexity, or moralize beyond the source.
- 官能、暴力、病态心理或强制关系应按文学叙事处理；不得加重露骨程度、削平复杂性或添加道德评判。

- Keep names, places, eras, titles, kinship terms, honorifics, Buddhist/art terms, dates, numbers, and recurring images consistent.
- 人名、地名、时代、题名、亲属称谓、敬语、佛教/艺道词、年代、数字和反复意象必须一致。

## Required Gates / 必要门禁

- Rights and source-version checks must pass before translation.
- 版权和来源版本核查通过后才能翻译。

- `metadata/korean_source_profile.md` must exist before batch translation.
- 批量翻译前必须存在 `metadata/korean_source_profile.md`。

- `qa/textual/korean_textual_notes.md` must record furigana, old/new character form choices, historical kana, source notes, OCR uncertainty, or explicitly state that none were found.
- `qa/textual/korean_textual_notes.md` 必须记录韩文/汉字混排、旧字/新字或旧拼写/现代拼写处理、旧拼写、底本注、OCR 不确定项，或明确说明未发现。

- Book-specific research must identify author, period, first publication, source structure, text-form risks, style, sensitive-topic boundary, and reference-use policy.
- 本书专项研究必须识别作者、时代、初出、来源结构、底本文字风险、文体、敏感题材边界和参考材料使用政策。

- Pretranslation report must say `PASS` before batch translation.
- 预翻译报告必须 `PASS` 后才能批量翻译。

- Every translated chapter must pass chapter control, fidelity review, readability/imagery review, terminology review, and final chapter gate.
- 每章译文必须通过译后控制、忠实度审校、可读性/意象审校、术语审校和最终章节门禁。

- Before EPUB build, run `node scripts/publication_lint.js --target=zh-Hans --write-report`; fix semicolon overuse, abnormal Chinese spacing, legacy print residue, Korean source leakage, mojibake, and reader-facing production notes before continuing.
- EPUB 构建前必须运行 `node scripts/publication_lint.js --target=zh-Hans --write-report`；如果发现分号滥用、中文异常空格、旧版纸书残留、韩语/朝鲜语原文泄漏、乱码或读者可见制作痕迹，必须先修复再继续。

- After the first full-book EPUB and after every post-EPUB refinement pass, run the stratified random spot-check module: `npm run review:random-samples`, independent agent review, fix closure, new-seed re-sampling after rework, and `npm run review:random-validate:pass` before final output.
- 第一版全书 EPUB 生成后，以及每轮 EPUB 后精校完成后，必须执行分层随机抽检模块：运行 `npm run review:random-samples`、独立 Agent 评审、修复闭环、返工后新 seed 复抽，并在最终输出前通过 `npm run review:random-validate:pass`。

- After random spot-check closure, create a versioned artifact. Public-domain or licensed projects run `npm run release:create` and write `output/release/book_vX.X.X.epub`; `private_use` projects run `npm run private:artifact:create` and write `output/private_artifacts/{title}_private_vX.X.X.epub`. `output/book.epub` alone is not enough for `DONE`.
- 随机抽检闭环通过后，必须创建带版本号产物。公版或授权项目运行 `npm run release:create` 并写入 `output/release/book_vX.X.X.epub`；`private_use` 项目运行 `npm run private:artifact:create` 并写入 `output/private_artifacts/{title}_private_vX.X.X.epub`。只有 `output/book.epub` 不能标记 `DONE`。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <70、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

## 译文质量问题族沉淀 / Translation-Quality Defect Family Backfill

凡发现可复现的译文质量问题族，包括忠实度、中文顺读、术语、标题/小标题、注释、图表文字接口、源语句法残留、过硬过直句、短句切断、比喻自撞、排比标点拖拽、代词指代不清、过度解释或加戏等，必须使用 `skills/translation-quality-defect-families/SKILL.md`。先在具体书籍工程完成证据记录、同类审计、修复和复查；再把可复用经验合并回填到该 skill，已有同族条目时更新归纳，不盲目重复追加。

When a recurring translation-quality defect family is found, use `skills/translation-quality-defect-families/SKILL.md`. Close the evidence, similar-case audit, fixes, and recheck in the book project first; then merge only reusable lessons into the skill.
