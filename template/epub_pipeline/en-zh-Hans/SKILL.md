---
name: epub-pipeline-en-zh-Hans
description: Use when creating or reviewing English to Simplified Chinese public-domain EPUB translation projects with this template.
---

# English to Simplified Chinese EPUB Pipeline / 英文到简体中文 EPUB 流水线

Use this skill after `books/scripts/create_book_project.py` has copied `template/epub_pipeline/common` and overlaid `template/epub_pipeline/en-zh-Hans` into `books/zh-Hans/{number}_{book_id_slug}/`.

使用本 skill 前，应先通过 `books/scripts/create_book_project.py` 把 `template/epub_pipeline/common` 复制到 `books/zh-Hans/{number}_{book_id_slug}/`，再覆盖复制 `template/epub_pipeline/en-zh-Hans`。

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

11. `references/quality_gate_framework.md`
    读取通用质量门禁，尤其是每章译后全量检查硬门禁。

12. `references/stratified_random_spotcheck.md`
    读取 EPUB 后分层随机抽检门禁。
13. `references/release_versioning.md`
    读取 EPUB 版本化发布、release note 和 `output/release/` 门禁。

## Translation Standard / 翻译标准

- Preserve the source meaning, facts, tone, narrative stance, and structure.
- 保留原文意思、事实、语气、叙述姿态和结构。

- Write natural Simplified Chinese, not English syntax with Chinese words.
- 写自然的简体中文，不要写成中文词语套英文句法。

- In the translation call itself, use a slim prompt and output only translation text. Keep release, EPUB, lint, QA, and versioning rules in later workflow nodes.
- 翻译调用本身必须使用瘦身 prompt，并且只输出译文。release、EPUB、lint、QA 和版本化规则留给后续流程节点。

- Natural Chinese prose is the first hard constraint during translation. A faithful sentence that reads like English syntax or a breathless long sentence is not acceptable.
- 翻译阶段第一硬约束是自然中文正文。忠实但像英文句法、或长到读不动的句子，不可接受。

- Improve readability through Chinese expression, but do not add metaphors, sounds, facts, or emotions not supported by the source.
- 可以通过中文表达提升可读性，但不得添加原文没有依据的比喻、声音、事实或情绪。

- Avoid over-compressed "outline-like" Chinese.
- 避免把中文压缩成提纲式表达。

- Keep names, places, dates, numbers, and recurring terms consistent.
- 人名、地名、年代、数字和反复出现的术语必须一致。
- Distinguish term control levels: `locked` terms must stay fixed, `preferred` terms may use natural contextual variants, `avoid` terms are forbidden, and `note_only` terms belong in notes/glossary rather than body prose.
- 区分术语控制级别：`locked` 必须固定，`preferred` 可按上下文自然变体，`avoid` 禁用，`note_only` 只放译注/术语表，不压进正文。
- Do not mechanically convert English printed-TOC title chains using `--` into Chinese `——` chains. When needed, split them into a short navigation title, display title, and subtitle.
- 不得把英文纸书目录式 `--` 标题链机械转换成中文 `——` 链。必要时必须拆成短目录题名、页面主标题和副标题。
- Names in chapter titles, subtitles, and navigation titles must use Chinese translated names only. Title occurrences do not count as first body occurrences; keep the English original name at the first natural body occurrence, in a note, or in the glossary.
- 章节标题、副标题和目录题名中的人名只使用中文译名。标题中的出现不计入“正文首次出现”；英文原名应放在正文第一次自然出现处、译注或术语表中。

- Historical terms, institutional names, status titles, technical terms, and culture-loaded terms must not default to `Chinese term (source term)` in the body. Use a readable Chinese term first; move source terms, definitions, and translation rationale to chapter notes, endnotes, or glossary entries with note markers such as `[1]`. Body parenthetical source terms are rare exceptions and must record why a note was not enough.
- 历史术语、制度名、身份称谓、专业术语和文化负载词不得默认写成正文里的 `中文译名（source term）`。正文优先使用可读中文译名；原词、定义和译名理由放入本章译注、章末注或术语表，并用 `[1]` 等注号指向。正文括注原词只能作为少量例外，且必须记录为什么不能只用译注。

## Required Gates / 必要门禁

- Rights check must pass before translation.
- 版权核查通过后才能翻译。

- Book-specific research and style profile must exist before trial translation.
- 试译前必须有本书专项研究和文体画像。

- Pretranslation report must say `PASS` before batch translation.
- 预翻译报告必须 `PASS` 后才能批量翻译。

- After each translated chapter is written, immediately run the full post-translation check and fix node in `qa/chapter_controls/{NNN_slug}.control.md`. It must cover metadata, nav, table of contents, body text, notes, figures, formulas, tables, images, styles, reader-facing content, plain-language clarity without flattening specialist quality, readability, polishing, terminology, and annotations. Do not limit the check to items named by the user. If any issue is found and fixed, that round must be `FIXED_RECHECK_REQUIRED`; append a new full-chapter recheck. Only a latest round with `scope: FULL_CHAPTER`, `issues_found: 0`, `fixes_applied: 0`, `unresolved_blocking_issues: 0`, `latest_round_status: PASS`, and `allow_next_chapter: true` may unlock the next chapter.
- 每章译文写入后，必须立即执行 `qa/chapter_controls/{NNN_slug}.control.md` 中的“每章译后，全量检查并修复节点”。检查范围必须覆盖 metadata、nav、目录、正文、注释、图表、公式、表格、图片、样式、读者可见内容、通俗化、可读性、润色、名词术语和注释等，不得只检查用户点名项目。通俗顺读不能损害专业质量。发现并修复问题的轮次只能记为 `FIXED_RECHECK_REQUIRED`；必须追加新的整章复查。只有最近一轮 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` 时，才可继续下一章。

- Chapter control must record Chinese-only readability scoring and a 20-sentence read-aloud test before source calibration. Chinese score below 4/5, more than one awkward sentence, or breathless key sentences blocks progress.
- 章节控制必须先记录只看中文的可读性评分和 20 句朗读测试，再做原文校准。中文评分低于 4/5、明显拗口超过 1 句或关键句不断气时，不得继续。

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

- After the first full-book EPUB and after every post-EPUB refinement pass, run the stratified random spot-check module: `npm run review:random-samples`, independent agent review, fix closure, new-seed re-sampling after rework, and `npm run review:random-validate:pass` before final output. The sampled population is reader-facing audit units, including paragraphs, tables, figures, formulas/proof blocks, captions, and notes.
- 第一版全书 EPUB 生成后，以及每轮 EPUB 后精校完成后，必须执行分层随机抽检模块：运行 `npm run review:random-samples`、独立 Agent 评审、修复闭环、返工后新 seed 复抽，并在最终输出前通过 `npm run review:random-validate:pass`。抽样总体是读者可见审计单元，包括正文段落、表格、图片、公式/证明块、图注和注释。
- After random spot-check closure, create a versioned artifact. Public-domain or licensed projects run `npm run release:create` and write `output/release/book_vX.X.X.epub`; `private_use` projects run `npm run private:artifact:create` and write `output/private_artifacts/{title}_private_vX.X.X.epub`. `output/book.epub` alone is not enough for `DONE`.
- 随机抽检闭环通过后，必须创建带版本号产物。公版或授权项目运行 `npm run release:create` 并写入 `output/release/book_vX.X.X.epub`；`private_use` 项目运行 `npm run private:artifact:create` 并写入 `output/private_artifacts/{title}_private_vX.X.X.epub`。只有 `output/book.epub` 不能标记 `DONE`。
