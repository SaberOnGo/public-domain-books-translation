---
name: epub-pipeline-ja-zh-Hans
description: Use when creating or reviewing Japanese to Simplified Chinese public-domain EPUB translation projects with this template.
---

# Japanese to Simplified Chinese EPUB Pipeline / 日语到简体中文 EPUB 流水线

Use this skill after `books/scripts/create_book_project.py` has copied `template/epub_pipeline/common` and overlaid `template/epub_pipeline/ja-zh-Hans` into `books/zh-Hans/{number}_{book_id_slug}/`.

使用本 skill 前，应先通过 `books/scripts/create_book_project.py` 把 `template/epub_pipeline/common` 复制到 `books/zh-Hans/{number}_{book_id_slug}/`，再覆盖复制 `template/epub_pipeline/ja-zh-Hans`。

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

8. `references/japanese_source_notes.md`
   读取日语源语言干扰说明。

9. `references/japanese_title_strategy.md`
   读取日语题名、章题、短标题和译注策略。

10. `references/japanese_to_chinese_literary_refinement.md`
    读取日语到简体中文文学精修策略。

11. `references/stratified_random_spotcheck.md`
    读取 EPUB 后分层随机抽检门禁。

12. `references/release_versioning.md`
    读取 EPUB 版本化发布、release note 和 `output/release/` 门禁。

## Translation Standard / 翻译标准

- Preserve the source meaning, facts, narrative stance, point of view, emotional temperature, and degree of ambiguity.
- 保留原文意思、事实、叙述姿态、视角、情绪温度和暧昧程度。

- Translate from the Japanese source. Use modern Chinese or English translations only as bounded references when rights and use limits are recorded.
- 从日语底本翻译。现代中文译本或英译本只能在版权和使用边界记录清楚后作有限参考。

- Write natural Simplified Chinese, not Japanese syntax with Chinese words.
- 写自然的简体中文，不要写成中文词语套日语句法。

- Do not assume Japanese kanji words can be copied into Chinese. Check semantic drift, register, period tone, and reader comprehension.
- 不要默认日语汉字词可以照搬成中文。必须检查语义漂移、语体、时代感和读者理解。

- Preserve furigana, old character forms, historical kana, editorial notes, OCR uncertainty, and variant readings as evidence records; translate only what belongs in reader-facing text.
- 振假名、旧字体、历史假名遣、编者注、OCR 不确定和异体读法应作为证据记录保存；读者正文只翻译应进入正文的内容。

- Treat sensual, violent, pathological, or coercive material as literary narration. Do not add explicitness, reduce complexity, or moralize beyond the source.
- 官能、暴力、病态心理或强制关系应按文学叙事处理；不得加重露骨程度、削平复杂性或添加道德评判。

- Keep names, places, eras, titles, kinship terms, honorifics, Buddhist/art terms, dates, numbers, and recurring images consistent.
- 人名、地名、时代、题名、亲属称谓、敬语、佛教/艺道词、年代、数字和反复意象必须一致。

## Required Gates / 必要门禁

- Rights and source-version checks must pass before translation.
- 版权和来源版本核查通过后才能翻译。

- `metadata/japanese_source_profile.md` must exist before batch translation.
- 批量翻译前必须存在 `metadata/japanese_source_profile.md`。

- `qa/textual/japanese_textual_notes.md` must record furigana, old/new character form choices, historical kana, source notes, OCR uncertainty, or explicitly state that none were found.
- `qa/textual/japanese_textual_notes.md` 必须记录振假名、旧字/新字处理、历史假名遣、底本注、OCR 不确定项，或明确说明未发现。

- Book-specific research must identify author, period, first publication, source structure, text-form risks, style, sensitive-topic boundary, and reference-use policy.
- 本书专项研究必须识别作者、时代、初出、来源结构、底本文字风险、文体、敏感题材边界和参考材料使用政策。

- Pretranslation report must say `PASS` before batch translation.
- 预翻译报告必须 `PASS` 后才能批量翻译。

- Every translated chapter must pass chapter control, fidelity review, readability/imagery review, terminology review, and final chapter gate.
- 每章译文必须通过译后控制、忠实度审校、可读性/意象审校、术语审校和最终章节门禁。

- Before EPUB build, run `node scripts/publication_lint.js --target=zh-Hans --write-report`; fix semicolon overuse, abnormal Chinese spacing, legacy print residue, Japanese source leakage, mojibake, and reader-facing production notes before continuing.
- EPUB 构建前必须运行 `node scripts/publication_lint.js --target=zh-Hans --write-report`；如果发现分号滥用、中文异常空格、旧版纸书残留、日语原文泄漏、乱码或读者可见制作痕迹，必须先修复再继续。

- After the first full-book EPUB and after every post-EPUB refinement pass, run the stratified random spot-check module: `npm run review:random-samples`, independent agent review, fix closure, new-seed re-sampling after rework, and `npm run review:random-validate:pass` before final output.
- 第一版全书 EPUB 生成后，以及每轮 EPUB 后精校完成后，必须执行分层随机抽检模块：运行 `npm run review:random-samples`、独立 Agent 评审、修复闭环、返工后新 seed 复抽，并在最终输出前通过 `npm run review:random-validate:pass`。

- After random spot-check closure, create a versioned artifact. Public-domain or licensed projects run `npm run release:create` and write `output/release/book_vX.X.X.epub`; `private_use` projects run `npm run private:artifact:create` and write `output/private_artifacts/{title}_private_vX.X.X.epub`. `output/book.epub` alone is not enough for `DONE`.
- 随机抽检闭环通过后，必须创建带版本号产物。公版或授权项目运行 `npm run release:create` 并写入 `output/release/book_vX.X.X.epub`；`private_use` 项目运行 `npm run private:artifact:create` 并写入 `output/private_artifacts/{title}_private_vX.X.X.epub`。只有 `output/book.epub` 不能标记 `DONE`。
