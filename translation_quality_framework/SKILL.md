---
name: literary-translation-quality
description: Use when translating public-domain or licensed books into Chinese, especially literary nonfiction, memoir, travel, exploration, adventure, fiction, or essays. Provides a strict workflow for AI-assisted translation quality, including research-grounded standards, chapter prompts, MQM-style error review, literary revision, benchmark testing against legally available reference excerpts, and EPUB-ready final text checks.
---

# Literary Translation Quality

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
11. Audit image-bearing word choices with `templates/image_word_audit_prompt.md`.
12. Gate every chapter with `templates/chapter_quality_gate_prompt.md`.
13. Score every final chapter with `templates/evaluation_rubric.md`.

## Hard Rules

- Never optimize only for literal correspondence.
- Never keep English syntax when natural Chinese would say it differently.
- Never preserve a metaphor word-for-word when it becomes obscure or ugly in Chinese; preserve the effect instead.
- Never use copyrighted reference translations as source material unless the user provides lawful excerpts for private evaluation. Do not store long copyrighted excerpts in the project.
- If a sentence sounds like a translation, rewrite it unless the stiffness is intentional in the original.
- If a passage is historically sensitive, keep the historical fact and tone, but add translator notes instead of silently modernizing.
- Do not translate a chapter without a book-level style profile and a passing sample-test report.
- In body text, prefer accurate image-bearing words over flat explanatory words when the source is symbolic, scenic, physical, or memorable.
- Do not start batch chapter translation without a passing `qa/pretranslation/pretranslation_report.md`.

## Quality Gate

A chapter can move to `chapters/final/` only if:

- No major meaning errors.
- No missing paragraph.
- No unresolved proper noun or technical term inconsistency.
- Readability score is at least 4/5.
- Literary/narrative effect score is at least 4/5.
- The reviewer cannot point to a sentence that feels mechanically translated.
- A gate report exists under `qa/gates/` and says `PASS`.
- `qa/samples/sample_test_report.md` exists and says `PASS`.
- `qa/pretranslation/pretranslation_report.md` exists and says `PASS`.
- An imagery audit exists under `qa/imagery/` for chapters with symbolic, scenic, physical, or memorable language.
