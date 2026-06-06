---
name: zh-hans-target-quality
description: Use when translating public-domain or licensed books into Simplified Chinese, regardless of source language. Provides target-language quality rules for AI-assisted translation, including Chinese readability, style research, chapter gates, benchmark testing, literary revision, and EPUB-ready final text checks.
---

# Simplified Chinese Target Quality / 简体中文目标语言质量

Use this skill before translating full chapters. Do not begin batch translation until a sample passes the quality gate.

## Required Workflow

1. Read `references/research_digest.md`.
2. Read `references/quality_standard.md`.
3. Read `references/workflow.md`.
4. Create `metadata/book_specific_translation_research.md` with `templates/book_specific_research_prompt.md`.
5. Create `metadata/style_profile.md` with `templates/style_profile_prompt.md`.
6. If the user provides lawful private benchmark excerpts, evaluate them with `templates/private_benchmark_compare_prompt.md`.
7. Run pretranslation trials with `templates/pretranslation_trial_prompt.md`.
8. Run the sample test described in `tests/benchmark_protocol.md` and `templates/sample_translation_test_prompt.md`.
9. Only after pretranslation and sample tests pass, translate chapters with `templates/chapter_translation_prompt.md`.
10. Revise failed chapters with `templates/revision_prompt.md`.
11. Use `skills/expert-translation-quality/SKILL.md` during chapter translation, chapter controls, review, reader-feedback fixes, and final artifact review when expert-level prose, context-dependent word choice, or polysemy back-checking matters.
12. Audit image-bearing word choices with `templates/image_word_audit_prompt.md`.
13. Gate every chapter with `templates/chapter_quality_gate_prompt.md`.
14. Score every final chapter with `templates/evaluation_rubric.md`.
15. When a recurring translation-quality defect family is found, use `skills/translation-quality-defect-families/SKILL.md`, close the family in the current book, and merge reusable lessons into that skill.

## Hard Rules

- Never optimize only for literal correspondence.
- Never keep English syntax when natural Chinese would say it differently.
- Never preserve a metaphor word-for-word when it becomes obscure or ugly in Chinese; preserve the effect instead.
- Never use copyrighted reference translations as source material unless the user provides lawful excerpts for private evaluation. Do not store long copyrighted excerpts in the project.
- If a sentence sounds like a translation, rewrite it unless the stiffness is intentional in the original.
- During the translation call itself, use a slim prompt and output only the translation. Do not ask the model to write QA, release notes, lint records, or workflow explanations in the same call.
- Natural Chinese is the first hard constraint in translation. Faithful but breathless long sentences, English clause skeletons, or compliance-looking prose that does not read like Chinese fail the gate.
- Polysemous or context-dependent source wording must be revisited after downstream context is available. A smooth but wrong word sense is a blocking mistranslation.
- If a passage is historically sensitive, keep the historical fact and tone, but add translator notes instead of silently modernizing.
- Do not translate a chapter without a book-level style profile and a passing sample-test report.
- In body text, prefer accurate image-bearing words over flat explanatory words when the source is symbolic, scenic, physical, or memorable.
- Do not start batch chapter translation without a passing `qa/pretranslation/pretranslation_report.md`.
- If a review finds a recurring quality pattern, do not only fix the sampled sentence. Classify the defect family, audit similar cases with low-token methods first, and update `skills/translation-quality-defect-families/SKILL.md` with reusable lessons.
- 发现反复出现的质量模式时，不得只修抽中的句子。必须归纳问题族，先用低 token 方法审计同类，并把可复用经验回填到 `skills/translation-quality-defect-families/SKILL.md`。
- 专家级译文与多义词回看使用 `skills/expert-translation-quality/SKILL.md` 执行；具体复发坏例再沉淀到 `skills/translation-quality-defect-families/SKILL.md`。

## Quality Gate

A chapter can move to `chapters/final/` only if:

- No major meaning errors.
- No missing paragraph.
- No unresolved proper noun or technical term inconsistency.
- Readability score is at least 4/5.
- Literary/narrative effect score is at least 4/5.
- Chinese-only readability score is at least 4/5 before source calibration.
- `qa/chapter_controls/` records `expert_translation_skill_used: true`, `expert_level_review_status: "PASS"`, `polysemy_context_review: "PASS"`, and `polysemy_unresolved_count: 0`.
- A 20-sentence read-aloud sample has at most one clearly awkward sentence, and no key sentence is breathless.
- The reviewer cannot point to a sentence that feels mechanically translated.
- A gate report exists under `qa/gates/` and says `PASS`.
- `qa/samples/sample_test_report.md` exists and says `PASS`.
- `qa/pretranslation/pretranslation_report.md` exists and says `PASS`.
- An imagery audit exists under `qa/imagery/` for chapters with symbolic, scenic, physical, or memorable language.
- Any discovered translation-quality defect family has book-local evidence, confirmed fixes or exceptions, and a reusable merged lesson in `skills/translation-quality-defect-families/SKILL.md`.

## Expert Translation Quality / 专家级译文质量

Translation, chapter controls, independent review, random spot-checks, final artifact review, private-use artifact review, and reader-feedback fixes must use `skills/expert-translation-quality/SKILL.md` when expert-level prose, context-dependent word choice, or polysemy back-checking matters. Recurring concrete defects still belong in `skills/translation-quality-defect-families/SKILL.md`.

翻译、章节 control、独立审校、随机抽检、最终产物审阅、private-use 产物审阅和读者反馈修复中，只要涉及专家级译文、上下文依赖选义或多义词回看，必须使用 `skills/expert-translation-quality/SKILL.md`。具体复发坏例仍沉淀到 `skills/translation-quality-defect-families/SKILL.md`。
