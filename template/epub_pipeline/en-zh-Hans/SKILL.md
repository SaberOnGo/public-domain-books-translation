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
9. `references/english_chapter_title_strategy.md`
   读取英文旧式章节标题链的中文处理规则。
10. `references/english_to_chinese_literary_refinement.md`
   读取英文到简体中文文学精修策略。

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
- Do not mechanically convert English printed-TOC title chains using `--` into Chinese `——` chains. When needed, split them into a short navigation title, display title, and subtitle.
- 不得把英文纸书目录式 `--` 标题链机械转换成中文 `——` 链。必要时必须拆成短目录题名、页面主标题和副标题。
- Names in chapter titles, subtitles, and navigation titles must use Chinese translated names only. Title occurrences do not count as first body occurrences; keep the English original name at the first natural body occurrence, in a note, or in the glossary.
- 章节标题、副标题和目录题名中的人名只使用中文译名。标题中的出现不计入“正文首次出现”；英文原名应放在正文第一次自然出现处、译注或术语表中。

## Required Gates / 必要门禁

- Rights check must pass before translation.
- 版权核查通过后才能翻译。

- Book-specific research and style profile must exist before trial translation.
- 试译前必须有本书专项研究和文体画像。

- Pretranslation report must say `PASS` before batch translation.
- 预翻译报告必须 `PASS` 后才能批量翻译。

- Every translated chapter must pass chapter control, fidelity review, readability review, terminology review, imagery audit when relevant, and final chapter gate.
- 每章译文必须通过译后控制、忠实度审校、可读性审校、术语审校、必要时的意象词审计，以及最终章节门禁。

- Before EPUB build, run `node scripts/publication_lint.js --target=zh-Hans --write-report`; fix semicolon overuse, abnormal Chinese spacing, legacy print page-number tables, and mojibake before continuing.
- EPUB 构建前必须运行 `node scripts/publication_lint.js --target=zh-Hans --write-report`；如果发现分号滥用、中文异常空格、旧纸书页码目录、乱码或 `targetTitleLatinResidue`，必须先修复再继续。
- Before final EPUB output, verify chapter headings against `references/english_chapter_title_strategy.md` and `references/title_punctuation_and_heading_style.md`.
- 最终 EPUB 输出前，必须按 `references/english_chapter_title_strategy.md` 和 `references/title_punctuation_and_heading_style.md` 检查章节标题。
- If systematic refinement issues are found in a specific book, create the goal document under that book project and backfill reusable lessons to the template layer.
- 如果某本书发现系统性精修问题，目标文档必须放到该书工程内，并把可复用经验回填到模板层。

- EPUB output must pass validation before final output.
- EPUB 必须通过校验后才能进入最终输出。

- After every post-EPUB refinement pass, run `npm run review:random-samples` or the equivalent random-sampling script. Two independent agents must each review at least ten random reader-facing Chinese paragraphs, with both averages >= 75 and no paragraph < 70.
- 每轮 EPUB 后精校完成后，必须运行 `npm run review:random-samples` 或等效随机抽样脚本。两个独立 Agent 各抽检至少十个读者可见中文正文段落，两个平均分都必须 >= 75，且不得有单段 < 70。
