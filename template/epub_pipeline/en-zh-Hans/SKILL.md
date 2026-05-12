---
name: epub-pipeline-en-zh-Hans
description: Use when creating or reviewing English to Simplified Chinese public-domain EPUB translation projects with this template.
---

# English to Simplified Chinese EPUB Pipeline / 英文到简体中文 EPUB 流水线

Use this skill after copying `template/epub_pipeline/common` and overlaying `template/epub_pipeline/en-zh-Hans` into a book project.

使用本 skill 前，应先把 `template/epub_pipeline/common` 复制到书籍工程，再覆盖复制 `template/epub_pipeline/en-zh-Hans`。

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
8. `references/english_source_notes.md`
   读取英语源语言干扰说明。

## Translation Standard / 翻译标准

- Preserve the source meaning, facts, tone, narrative stance, and structure.
- 保留原文意思、事实、语气、叙述姿态和结构。

- Write natural Simplified Chinese, not English syntax with Chinese words.
- 写自然的简体中文，不要写成中文词语套英文句法。

- Improve readability through Chinese expression, but do not add metaphors, sounds, facts, or emotions not supported by the source.
- 可以通过中文表达提升可读性，但不得添加原文没有依据的比喻、声音、事实或情绪。

- Avoid over-compressed "outline-like" Chinese.
- 避免把中文压缩成提纲式表达。

- Keep names, places, dates, numbers, and recurring terms consistent.
- 人名、地名、年代、数字和反复出现的术语必须一致。

## Required Gates / 必要门禁

- Rights check must pass before translation.
- 版权核查通过后才能翻译。

- Book-specific research and style profile must exist before trial translation.
- 试译前必须有本书专项研究和文体画像。

- Pretranslation report must say `PASS` before batch translation.
- 预翻译报告必须 `PASS` 后才能批量翻译。

- Every translated chapter must pass chapter control, fidelity review, readability review, terminology review, imagery audit when relevant, and final chapter gate.
- 每章译文必须通过译后控制、忠实度审校、可读性审校、术语审校、必要时的意象词审计，以及最终章节门禁。

- EPUB output must pass validation before final output.
- EPUB 必须通过校验后才能进入最终输出。
