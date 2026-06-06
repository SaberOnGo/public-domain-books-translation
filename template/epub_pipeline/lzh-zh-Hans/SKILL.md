---
name: epub-pipeline-lzh-zh-Hans
description: Use when creating or reviewing Literary Chinese to modern Simplified Chinese public-domain EPUB translation projects with parallel source-modern passages and controlled annotations.
---

# 文言文到现代简体中文 EPUB 流水线 / Literary Chinese to Modern Simplified Chinese EPUB Pipeline

Use this skill after `books/scripts/create_book_project.py` has copied `template/epub_pipeline/common` and overlaid `template/epub_pipeline/lzh-zh-Hans` into `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`.

使用本 skill 前，应先通过 `books/scripts/create_book_project.py` 把 `template/epub_pipeline/common` 复制到 `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`，再覆盖复制 `template/epub_pipeline/lzh-zh-Hans`。

For historical prose such as `战国策`, `左传`, `国语`, or historical chapters from `史记`, overlay `template/epub_pipeline/profiles/classical-history-zh-Hans` after this template.

处理《战国策》《左传》《国语》或《史记》历史篇章等历史叙事时，应在本模板之后叠加 `template/epub_pipeline/profiles/classical-history-zh-Hans`。

## Required Reading / 必读文件

1. `AGENTS.md`
2. `README.md`
3. `PIPELINE_SPEC.md`
4. `automation_contract.md`
5. `template/epub_pipeline/targets/zh-Hans/quality_framework/README.md`
6. `references/translation_research_universal.md`
7. `references/quality_standard.md`
8. `references/classical_chinese_source_notes.md`
9. `references/classical_chinese_parallel_text_policy.md`
10. `references/classical_chinese_annotation_policy.md`
11. `references/classical_chinese_textual_criticism_policy.md`
12. `references/classical_chinese_title_strategy.md`
13. `references/classical_chinese_to_modern_chinese_literary_refinement.md`
14. `references/stratified_random_spotcheck.md`
15. `references/release_versioning.md`

## Required Records / 必要记录

- `metadata/source_evidence.md`
- `metadata/rights_checklist.md`
- `metadata/source_witness_manifest.md`
- `metadata/classical_chinese_source_profile.md`
- `qa/textual/classical_chinese_textual_notes.md`
- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `glossary/terms.csv`
- `qa/chapter_controls/{chapter}.control.md`
- `qa/gates/{chapter}.gate.md`

## Translation Standard / 翻译标准

- Use the Literary Chinese source text as the base. Modern translations and modern commentaries are not translation bases.
- 以文言文原文为底本。现代译文和现代注释不得成为翻译底本。
- Reader-facing final chapters default to source-modern paired passages.
- 读者版终稿默认采用“古文原文 + 现代译文”对照段落。
- Translation must be modern Chinese, not pseudo-classical prose and not school-exercise paraphrase.
- 今译必须是现代中文，不是假古文，也不是教辅式串讲。
- Notes should explain necessary background, names, institutions, geography, chronology, variants, punctuation, or textual uncertainty when omission would mislead readers.
- 注释用于解释必要背景、专名、制度、地理、年代、异文、断句或文本疑难；省略会造成误读时必须说明。

## Required Gates / 必要门禁

- Source and rights checks must pass before translation.
- 来源和版权核查通过后才能翻译。
- Source profile and textual notes must pass before pretranslation.
- 底本文字形态和文本疑难记录通过后才能预翻译。
- Pretranslation trial must include at least one passage with dense names/background and one passage with difficult syntax or punctuation.
- 试译必须包含至少一段人名/背景密集文本，以及一段句法或断句困难文本。
- Every final chapter must pass source-modern alignment, fidelity, readability, terminology, annotation, and chapter gate checks.
- 每个终稿章节必须通过原文-今译对齐、忠实度、可读性、术语、注释和章节门禁。
- After the first full-book EPUB, stratified random spot-check must sample source passages, modern translations, notes, and any tables/figures/captions that exist.
- 第一版全书 EPUB 后，分层随机抽检必须抽到古文原文、现代译文、注释，以及实际存在的表格/图片/图注等层。

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
