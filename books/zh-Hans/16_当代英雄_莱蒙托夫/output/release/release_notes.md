# Release Notes / 发布说明

## Release v0.0.2 / 版本 v0.0.2

status: PASS
main_version: 0
sub_version: 0
patch_version: 2
created_at: 2026-06-13T08:51:19Z
epub: 当代英雄_v0.0.2.epub
sha256: 804264bc95a0dfbb142b854555d05bd020dff8740d6361a2ba13d8f3f6e16aff
size_bytes: 231183

## Release Reason / 发布原因

Digest merged final EPUB

## Changes / 修改内容

- Created standard EPUB with LifeBook Digest merged
- Completed ru-zh-Hans translation, chapter controls, random spot-check, EPUBCheck, and release gates

## Issues / 问题点

- No new issue entry was declared for this release note. / 本发布说明未声明新的问题条目。

## Fixes / 修复方式

- No fix entry was declared for this release note. / 本发布说明未声明新的修复条目。

## QA And Evidence / QA 与证据

- source_epub: `output/book_digest.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_002`
- random_spotcheck_validation: `reviews/random_spotcheck/round_002/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- current_review_run_id: `814b06a74c596f4552fda772`
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
- translation_metrics_primary_book_type: `fiction`
- translation_metrics_difficulty_level: `high`
- translation_metrics_actual_difficulty_level: `high`
- translation_metrics_actual_active_hours: `12`
- translation_metrics_total_tokens: `910000`

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
created_at: 2026-06-13T08:49:53Z
epub: 当代英雄_v0.0.1.epub
sha256: df0fb730c58cf5b2a0219ee39fb793e3fa1bbdb4ae326a697bc9f4df6e32a891
size_bytes: 224980

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
- random_spotcheck_round: `reviews/random_spotcheck/round_002`
- random_spotcheck_validation: `reviews/random_spotcheck/round_002/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- current_review_run_id: `814b06a74c596f4552fda772`
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
- translation_metrics_primary_book_type: `fiction`
- translation_metrics_difficulty_level: `high`
- translation_metrics_actual_difficulty_level: `high`
- translation_metrics_actual_active_hours: `12`
- translation_metrics_total_tokens: `910000`

## Risks / 风险

- If status is DRAFT, independent agent review or closure gates may still be incomplete. / 若状态为 DRAFT，独立 Agent 评审或闭环门禁可能尚未全部完成。

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。
