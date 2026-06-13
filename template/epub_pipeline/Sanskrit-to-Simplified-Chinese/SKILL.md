---
name: epub-pipeline-Sanskrit-to-Simplified-Chinese
description: Use when creating or reviewing Sanskrit to Simplified Chinese public-domain EPUB translation projects with this template.
---

# Sanskrit to Simplified Chinese EPUB Pipeline / 梵语到简体中文 EPUB 流水线

Use this skill after `books/scripts/create_book_project.py` has copied `template/epub_pipeline/common` and overlaid `template/epub_pipeline/Sanskrit-to-Simplified-Chinese` into `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`.

使用本 skill 前，应先通过 `books/scripts/create_book_project.py` 把 `template/epub_pipeline/common` 复制到 `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`，再覆盖复制 `template/epub_pipeline/Sanskrit-to-Simplified-Chinese`。

If the work is classical science, mathematics, astronomy, or diagram/table-heavy, overlay `template/epub_pipeline/profiles/classical-science-zh-Hans` after this template.

如果作品属于古典科学、数学、天文学或图表/表格密集型作品，应在本模板之后叠加 `template/epub_pipeline/profiles/classical-science-zh-Hans`。

## Required Reading / 必读文件

1. `AGENTS.md`
2. `README.md`
3. `PIPELINE_SPEC.md`
4. `automation_contract.md`
5. `template/epub_pipeline/targets/zh-Hans/quality_framework/README.md`
6. `references/translation_research_universal.md`
7. `references/quality_standard.md`
8. `references/sanskrit_source_notes.md`
9. `references/sanskrit_source_types.md`
10. `references/sanskrit_textual_criticism_policy.md`
11. `references/sanskrit_reference_translation_policy.md`
12. `references/sanskrit_names_transliteration_policy.md`
13. `references/sanskrit_title_strategy.md`
14. `references/sanskrit_to_chinese_translation_notes.md`
15. `references/sanskrit_poetry_profile.md` when the work is poetry, drama verse, hymn, or verse-heavy literature
16. `references/stratified_random_spotcheck.md`
17. `references/release_versioning.md`

## Translation Standard / 翻译标准

- Preserve source meaning, facts, argument structure, tone, and genre.
- 保留原文意思、事实、论证结构、语气和文类。

- Translate from the Sanskrit source. Use second-language translations only as reference witnesses.
- 从梵语底本翻译。第二语言译本只能作为参考证据。

- When a project uses a facsimile scan, a Sanskrit transcription, and an English or other second-language translation, keep their roles separate: facsimile for base-image verification, Sanskrit transcription for searchable/source-text control, and translation only for reference.
- 若项目同时使用扫描本、梵语转写和英文等第二语言译本，必须保持三者分工：扫描本用于底本影像核验，梵语转写用于可检索原文控制，译本只作参考证据。

- Write natural Simplified Chinese, not Sanskrit grammar with Chinese words.
- 写自然的简体中文，不要写成中文词语套梵语语法。

- Preserve textual uncertainty. Do not silently “fix” damaged, doubtful, or variant readings.
- 保留文本不确定性。不得静默修复残损、疑难或异文读法。

- Keep names, places, dates, numbers, technical terms, recurring formulae, poetic images, and mythological references consistent.
- 人名、地名、年代、数字、技术术语、反复出现的固定表达、诗歌意象和神话典故必须一致。

- For poetry and verse-heavy works, create `metadata/sanskrit_poetry_profile.md` or complete `metadata/source_text_profile.md` before pretranslation.
- 对诗歌和诗体密集作品，预翻译前必须创建 `metadata/sanskrit_poetry_profile.md` 或补全 `metadata/source_text_profile.md`。

## Required Gates / 必要门禁

- Rights and source-edition checks must pass before translation.
- 版权和底本版本核查通过后才能翻译。

- `metadata/source_witness_manifest.md` must exist before batch translation.
- 批量翻译前必须存在 `metadata/source_witness_manifest.md`。

- `qa/textual/textual_uncertainty_log.md` must record variants, conjectures, lacunae, OCR uncertainty, or explicitly state that none were found.
- `qa/textual/textual_uncertainty_log.md` 必须记录异文、拟补、残损、OCR 不确定项，或明确说明未发现。

- Book-specific research must identify edition, editor, source structure, textual risks, and reference-witness policy.
- 本书专项研究必须识别版本、编辑者、来源结构、文本风险和参考译本政策。

- Pretranslation report must say `PASS` before batch translation.
- 预翻译报告必须 `PASS` 后才能批量翻译。

- Every translated chapter must pass chapter control, fidelity review, readability review, terminology review, and final chapter gate.
- 每章译文必须通过译后控制、忠实度审校、可读性审校、术语审校和最终章节门禁。

- If the classical-science profile is enabled, every relevant chapter must also pass technical and diagram/table audits.
- 如果启用古典科学 profile，相关章节还必须通过技术审计和图表/表格审计。

- After the first full-book EPUB and after every post-EPUB refinement pass, run the stratified random spot-check module: `npm run review:random-samples`, independent agent review, fix closure, new-seed re-sampling after rework, and `npm run review:random-validate:pass` before final output. The sampled population is reader-facing audit units, including paragraphs, tables, figures, formulas/proof blocks, captions, and notes.
- 第一版全书 EPUB 生成后，以及每轮 EPUB 后精校完成后，必须执行分层随机抽检模块：运行 `npm run review:random-samples`、独立 Agent 评审、修复闭环、返工后新 seed 复抽，并在最终输出前通过 `npm run review:random-validate:pass`。抽样总体是读者可见审计单元，包括正文段落、表格、图片、公式/证明块、图注和注释。
- After random spot-check closure, create a versioned artifact. Public-domain or licensed projects run `npm run release:create` and write `output/release/book_vX.X.X.epub`; `private_use` projects run `npm run private:artifact:create` and write `output/private_artifacts/{title}_private_vX.X.X.epub`. `output/book.epub` alone is not enough for `DONE`.
- 随机抽检闭环通过后，必须创建带版本号产物。公版或授权项目运行 `npm run release:create` 并写入 `output/release/book_vX.X.X.epub`；`private_use` 项目运行 `npm run private:artifact:create` 并写入 `output/private_artifacts/{title}_private_vX.X.X.epub`。只有 `output/book.epub` 不能标记 `DONE`。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

## 译文质量问题族沉淀 / Translation-Quality Defect Family Backfill

凡发现可复现的译文质量问题族，包括忠实度、中文顺读、术语、标题/小标题、注释、图表文字接口、源语句法残留、过硬过直句、短句切断、比喻自撞、排比标点拖拽、代词指代不清、过度解释或加戏等，必须使用 `skills/translation-quality-defect-families/SKILL.md`。先在具体书籍工程完成证据记录、同类审计、修复和复查；再把可复用经验合并回填到该 skill，已有同族条目时更新归纳，不盲目重复追加。

When a recurring translation-quality defect family is found, use `skills/translation-quality-defect-families/SKILL.md`. Close the evidence, similar-case audit, fixes, and recheck in the book project first; then merge only reusable lessons into the skill.

## Expert Translation Quality / 专家级译文质量

Translation, chapter controls, independent review, random spot-checks, final artifact review, private-use artifact review, and reader-feedback fixes must use `skills/expert-translation-quality/SKILL.md` when expert-level prose, context-dependent word choice, or polysemy back-checking matters. Recurring concrete defects still belong in `skills/translation-quality-defect-families/SKILL.md`.

翻译、章节 control、独立审校、随机抽检、最终产物审阅、private-use 产物审阅和读者反馈修复中，只要涉及专家级译文、上下文依赖选义或多义词回看，必须使用 `skills/expert-translation-quality/SKILL.md`。具体复发坏例仍沉淀到 `skills/translation-quality-defect-families/SKILL.md`。
