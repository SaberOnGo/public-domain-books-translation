# Release Notes / 发布说明

## Release v0.0.4 / 版本 v0.0.4

status: ITERATIVE_RELEASE
quality_gate_status: NOT_PASS
main_version: 0
sub_version: 0
patch_version: 4
created_at: 2026-09-25T13:35:11Z
epubs:
- target_only: 约翰生传_v0.0.4.epub sha256=fdd8acdeadc7f116750d6ef22ad860915e1ef04d35116cd4cea305c7b7598eca size_bytes=5833025
- bilingual_parallel: 约翰生传_中英双语_v0.0.4.epub sha256=ac05a0af744ff80e64e4c019299bbf4659f0f3469be50724fb49c5bacf741cbd size_bytes=9468100

## Release Reason / 发布原因

按读者要求，将当前版本作为可持续更新的迭代发行版提供。 / At the reader’s request, this version is available as a maintained iterative release.

## Changes / 修改内容

- 重建并固化中文版与中英双语版，双语版按自然段逐段配对。 / Rebuilt and versioned the Chinese and English-Chinese editions with paragraph-by-paragraph pairing.
- 修复已核实的双语错位、重复引诗及表格配对问题。 / Corrected verified bilingual alignment shifts, a duplicated poem quotation, and table pairing.
- 保留章节末注及正文与注释之间的双向跳转。 / Preserved chapter-end notes and two-way navigation between note markers and note text.

## Issues / 问题点

- 全书整章复检尚未全部通过，翻译覆盖检查仍有未关闭提示。 / Full-chapter review is not yet complete, and translation-coverage findings remain open.
- 纸本页码指向注仍有未核实项。 / Some print-page cross-reference notes remain unverified.

## Fixes / 修复方式

- 中文版和双语版 EPUBCheck 均为 0 fatal、0 error、0 warning；两份发行文件与已检查构建件哈希一致。 / EPUBCheck reported 0 fatal errors, 0 errors, and 0 warnings for both editions; both release files match the checked build hashes.
- 读者导航、双语配对与交替结构检查通过；注释编号及回跳链接已核验。 / Reader navigation, bilingual pairing and interleaving checks passed; note numbering and return links were verified.

## QA And Evidence / QA 与证据

- random_spotcheck_status: NOT_RUN_AFTER_CURRENT_CHANGES；round_075 是前一发行版本的历史证据，不计入本次。 / round_075 is historical evidence from the preceding release and does not count for this version.
- current_run_pass_rounds: 0/4；release_confidence: 未针对本版本测量。 / Current-run PASS rounds: 0/4; release confidence was not measured for this version.
- chapter_controls: NOT_PASS；当前轮未建立全书整章 PASS。 / chapter_controls: NOT_PASS; full-book, full-chapter PASS is not established for this run.
- translation_coverage: NOT_PASS；已有报告列出 78 条提示。 / translation_coverage: NOT_PASS; the current report lists 78 findings.
- EPUBCheck: both editions 0 fatal / 0 error / 0 warning.
- publication_lint: 0 blocking issues; bilingual parallel/interleave and reader navigation checks passed.

## Risks / 风险

- 本版是可分发的迭代发行，不等于正式质量门禁 PASS，也不宣称 650 个章节控制或全部纸本页码指向注已闭环。 / This is a distributable iterative release, not a formal quality-gate PASS; it does not claim all 650 chapter controls or all print-page references are closed.

## Next Iteration / 下一轮迭代

- 继续整章复检、覆盖提示处理及纸本页码指向注核实，并在修订后重新运行对应门禁。 / Continue full-chapter review, resolve coverage findings, verify print-page references, and rerun the relevant gates after revisions.
- 后续读者反馈和 QA 修复递增小版本号。 / Increment the patch version for subsequent reader feedback and QA fixes.

## Release v0.0.3 / 版本 v0.0.3

status: DRAFT
main_version: 0
sub_version: 0
patch_version: 3
created_at: 2026-09-25T11:26:17Z
epubs:
- target_only: `约翰生传_v0.0.3.epub` sha256=`fdd8acdeadc7f116750d6ef22ad860915e1ef04d35116cd4cea305c7b7598eca` size_bytes=`5833025`
- bilingual_parallel: `约翰生传_中英双语_v0.0.3.epub` sha256=`ac05a0af744ff80e64e4c019299bbf4659f0f3469be50724fb49c5bacf741cbd` size_bytes=`9468100`

## Release Reason / 发布原因

依据全书快速扫描及读者反馈，先发布可持续更新的迭代版，并保留未完成门禁状态。

## Changes / 修改内容

- 重建中文版与中英双语版，采用哈希核对的13,647组段落配对。
- 修正四处双语段落错位，删除引诗重复，并修正共享渲染器的表格配对。
- 保持章节注释分章置后及正文与注释间的回跳链接。

## Issues / 问题点

- 650份章节控制尚未形成当前轮整章PASS；翻译覆盖检查仍有78条提示。
- 纸本页码回指注的批量核实与补注尚未完成。

## Fixes / 修复方式

- 完成4处已核实错位的修复，并对修复后候选逐一复核。
- 两版EPUBCheck均为0 fatal、0 error、0 warning；读者导航、双语配对与交替检查通过。

## QA And Evidence / QA 与证据

- source_epub_target_only: `output/book.epub`
- source_epub_bilingual_parallel: `output/book_bilingual_parallel.epub`
- random_spotcheck_round: `round_075 (historical; predates v0.0.3)`
- random_spotcheck_validation: `reviews/random_spotcheck/round_075/validation_report.json (historical only)`
- random_spotcheck_status: `NOT_RUN_AFTER_CURRENT_CHANGES`
- random_spotcheck_require_pass: `False`
- current_review_run_id: `NOT_RUN_AFTER_CURRENT_CHANGES`
- current_run_pass_rounds: `0/4`
- release_confidence: `NOT_MEASURED_FOR_V0.0.3`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`
- translation_metrics: `output/release/translation_metrics.json`
- translation_metrics_estimate_status: `PASS`
- translation_metrics_actual_status: `PASS`
- translation_metrics_primary_book_type: `history`
- translation_metrics_difficulty_level: `high`
- translation_metrics_actual_difficulty_level: `very_high`
- translation_metrics_actual_active_hours: `27`
- translation_metrics_total_tokens: `27377464`
- literary_style_review: `qa/literary_style/literary_style_review.md`
- literary_style_status: `CANDIDATES_REQUIRE_REVIEW`
- literary_target_only_reading_score: `MISSING`
- literary_read_aloud_awkward_sentence_count: `MISSING`
- literary_unresolved_style_debt_count: `MISSING`
- literary_literal_explanatory_style_debt_count: `MISSING`
- literary_high_impact_sections_reviewed: `False`
- literary_author_preface_and_first_chapter_reviewed: `True`

## Risks / 风险

- 上一版随机抽查 PASS 来自 v0.0.2，早于本次修订；v0.0.3 尚未完成新一轮随机抽查。
- 本版为迭代DRAFT；未完成的整章复检、覆盖提示和注释工作继续进入后续版本。

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。


## Release v0.0.2 / 版本 v0.0.2

status: PASS
main_version: 0
sub_version: 0
patch_version: 2
created_at: 2026-07-08T20:46:31Z
epubs:
- target_only: `约翰生传_v0.0.2.epub` sha256=`e842376666c751ed0153ce2bd796179893661dbbfd7eab1c005e6309c12d0344` size_bytes=`4047735`

## Release Reason / 发布原因

Create a versioned EPUB release artifact from the current book build. / 将当前书籍构建产物固化为带版本号的 EPUB 发布文件。

## Changes / 修改内容

- Versioned EPUB artifact created; no content change was declared in command arguments. / 已创建版本化 EPUB 文件；命令参数未声明具体内容修改。

## Issues / 问题点

- No new issue entry was declared for this release note. / 本发布说明未声明新的问题条目。

## Fixes / 修复方式

- No fix entry was declared for this release note. / 本发布说明未声明新的修复条目。

## QA And Evidence / QA 与证据

- source_epub_target_only: `output/book.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_075`
- random_spotcheck_validation: `reviews/random_spotcheck/round_075/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- current_review_run_id: `1ca0b4c37e4ca1e49358a3fc`
- current_run_pass_rounds: `4/4`
- release_confidence: `0.999782`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`
- translation_metrics: `output/release/translation_metrics.json`
- translation_metrics_estimate_status: `PASS`
- translation_metrics_actual_status: `PASS`
- translation_metrics_primary_book_type: `history`
- translation_metrics_difficulty_level: `high`
- translation_metrics_actual_difficulty_level: `very_high`
- translation_metrics_actual_active_hours: `27`
- translation_metrics_total_tokens: `27377464`
- literary_style_review: `qa/literary_style/literary_style_review.md`
- literary_style_status: `PASS`
- literary_target_only_reading_score: `5.0`
- literary_read_aloud_awkward_sentence_count: `0.0`
- literary_unresolved_style_debt_count: `0.0`
- literary_literal_explanatory_style_debt_count: `0.0`
- literary_high_impact_sections_reviewed: `True`
- literary_author_preface_and_first_chapter_reviewed: `True`

## Risks / 风险

- If status is DRAFT, independent agent review or closure gates may still be incomplete. / 若状态为 DRAFT，独立 Agent 评审或闭环门禁可能尚未全部完成。

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。


## Release v0.0.1 / 版本 v0.0.1

status: PASS
main_version: 0
sub_version: 0
patch_version: 1
created_at: 2026-07-07T04:06:11Z
epub: 约翰生传_v0.0.1.epub
sha256: 65c96e5a7ca2ef4ef9064245122c8a22cd35bf16d3cda2a860c6de1c8220b3c8
size_bytes: 4042019

## Release Reason / 发布原因

Create a versioned EPUB release artifact from the current book build. / 将当前书籍构建产物固化为带版本号的 EPUB 发布文件。

## Changes / 修改内容

- Versioned EPUB artifact created; no content change was declared in command arguments. / 已创建版本化 EPUB 文件；命令参数未声明具体内容修改。

## Issues / 问题点

- No new issue entry was declared for this release note. / 本发布说明未声明新的问题条目。

## Fixes / 修复方式

- No fix entry was declared for this release note. / 本发布说明未声明新的修复条目。

## QA And Evidence / QA 与证据

- source_epub: `output/book.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_046`
- random_spotcheck_validation: `reviews/random_spotcheck/round_046/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- current_review_run_id: `1ca0b4c37e4ca1e49358a3fc`
- current_run_pass_rounds: `2/2`
- release_confidence: `1.0`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`
- translation_metrics: `output/release/translation_metrics.json`
- translation_metrics_estimate_status: `PASS`
- translation_metrics_actual_status: `PASS`
- translation_metrics_primary_book_type: `history`
- translation_metrics_difficulty_level: `high`
- translation_metrics_actual_difficulty_level: `very_high`
- translation_metrics_actual_active_hours: `27`
- translation_metrics_total_tokens: `27377464`

## Risks / 风险

- If status is DRAFT, independent agent review or closure gates may still be incomplete. / 若状态为 DRAFT，独立 Agent 评审或闭环门禁可能尚未全部完成。

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。
