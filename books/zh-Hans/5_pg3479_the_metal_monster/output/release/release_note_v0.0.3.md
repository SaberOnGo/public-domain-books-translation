# Release v0.0.3 / 版本 v0.0.3

status: PASS
main_version: 0
sub_version: 0
patch_version: 3
created_at: 2026-05-18T07:44:35Z
epub: book_v0.0.3.epub
sha256: 78f42bfb43e748ec6a813bf966a9d80b05dcf810653775e9000d769b8e3988de
size_bytes: 259256

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
- random_spotcheck_round: `reviews/random_spotcheck/round_003`
- random_spotcheck_validation: `reviews/random_spotcheck/round_003/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- release_confidence: `0.998203`
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
