# Release Notes / 发布说明

## Release v0.0.6 / 版本 v0.0.6

status: PASS
main_version: 0
sub_version: 0
patch_version: 6
created_at: 2026-06-27T04:39:15Z
epub: 罗马人的私生活_v0.0.6.epub
sha256: 8d6a0bad0e8aa41012434b9fe51c8373340e0f585dda5ffdafc1960a870a4f29
size_bytes: 8090711

## Release Reason / 发布原因

N=3 current-run stratified random spot-check closure and rebuilt EPUB release.

## Changes / 修改内容

- Added round_037 as the third consecutive current-run clean PASS round after v0.0.5.
- Rebuilt output/book.epub after publication lint, asset, cover, reader-facing, and EPUBCheck gates.

## Issues / 问题点

- No new issue entry was declared for this release note. / 本发布说明未声明新的问题条目。

## Fixes / 修复方式

- Recorded semicolon lint exceptions for reviewed reader-facing high-level parallel clauses without changing chapter text.

## QA And Evidence / QA 与证据

- source_epub: `output/book.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_037`
- random_spotcheck_validation: `reviews/random_spotcheck/round_037/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- current_review_run_id: `419eb0e52cc92d81cb44d0af`
- current_run_pass_rounds: `3/3`
- release_confidence: `0.999782`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`

## Risks / 风险

- Formula and caption_note strata have zero candidate units in this book; paragraph, table, and figure strata were sampled or full-scanned according to the manifest.

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。


## Release v0.0.5 / 版本 v0.0.5

status: PASS
main_version: 0
sub_version: 0
patch_version: 5
created_at: 2026-06-14T06:26:05Z
epub: 罗马人的私生活_v0.0.5.epub
sha256: af9fbafaebf1b29ceaad3e69d3080a041865fd2a1b4b0ab395480b98ba121385
size_bytes: 8090487

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
- random_spotcheck_round: `reviews/random_spotcheck/round_031`
- random_spotcheck_validation: `reviews/random_spotcheck/round_031/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- current_review_run_id: `419eb0e52cc92d81cb44d0af`
- current_run_pass_rounds: `4/2`
- release_confidence: `0.999782`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`

## Risks / 风险

- If status is DRAFT, independent agent review or closure gates may still be incomplete. / 若状态为 DRAFT，独立 Agent 评审或闭环门禁可能尚未全部完成。

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。


## Release v0.0.4 / 版本 v0.0.4

status: PASS
main_version: 0
sub_version: 0
patch_version: 4
created_at: 2026-06-13T23:03:40Z
epub: 罗马人的私生活_v0.0.4.epub
sha256: 2454f0cb65fbbb16a31a61aa7f6b767225322131fd0b5cff16ae1a6cecbf07cc
size_bytes: 8090785

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
- random_spotcheck_round: `reviews/random_spotcheck/round_026`
- random_spotcheck_validation: `reviews/random_spotcheck/round_026/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- current_review_run_id: `419eb0e52cc92d81cb44d0af`
- current_run_pass_rounds: `4/2`
- release_confidence: `0.999782`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`

## Risks / 风险

- If status is DRAFT, independent agent review or closure gates may still be incomplete. / 若状态为 DRAFT，独立 Agent 评审或闭环门禁可能尚未全部完成。

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。


## Release v0.0.3 / 版本 v0.0.3

status: PASS
main_version: 0
sub_version: 0
patch_version: 3
created_at: 2026-06-13T13:13:36Z
epub: 罗马人的私生活_v0.0.3.epub
sha256: 2454f0cb65fbbb16a31a61aa7f6b767225322131fd0b5cff16ae1a6cecbf07cc
size_bytes: 8090785

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
- random_spotcheck_round: `reviews/random_spotcheck/round_022`
- random_spotcheck_validation: `reviews/random_spotcheck/round_022/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- current_review_run_id: `419eb0e52cc92d81cb44d0af`
- current_run_pass_rounds: `3/2`
- release_confidence: `0.999782`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`

## Risks / 风险

- If status is DRAFT, independent agent review or closure gates may still be incomplete. / 若状态为 DRAFT，独立 Agent 评审或闭环门禁可能尚未全部完成。

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。


## Release v0.0.2 / 版本 v0.0.2

status: PASS
main_version: 0
sub_version: 0
patch_version: 2
created_at: 2026-06-13T09:31:51Z
epub: 罗马人的私生活_v0.0.2.epub
sha256: 642f6606b3245f17ececa30758629dd49c553b1c061c79cb3b8131e2fa7aa233
size_bytes: 8090769

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
- random_spotcheck_round: `reviews/random_spotcheck/round_014`
- random_spotcheck_validation: `reviews/random_spotcheck/round_014/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- current_review_run_id: `419eb0e52cc92d81cb44d0af`
- current_run_pass_rounds: `3/3`
- release_confidence: `0.999782`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`

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
created_at: 2026-06-13T08:03:38Z
epub: 罗马人的私生活_v0.0.1.epub
sha256: f9803d58effac5149bc30f762bdef1158f632a70b85055df4f4d04f55a948e90
size_bytes: 8090727

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
- random_spotcheck_round: `reviews/random_spotcheck/round_006`
- random_spotcheck_validation: `reviews/random_spotcheck/round_006/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- current_review_run_id: `419eb0e52cc92d81cb44d0af`
- current_run_pass_rounds: `2/2`
- release_confidence: `0.999782`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`

## Risks / 风险

- If status is DRAFT, independent agent review or closure gates may still be incomplete. / 若状态为 DRAFT，独立 Agent 评审或闭环门禁可能尚未全部完成。

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。
