# Release v0.0.2 / 版本 v0.0.2

status: PASS
main_version: 0
sub_version: 0
patch_version: 2
created_at: 2026-05-18T03:41:16Z
epub: book_v0.0.2.epub
sha256: edfe495a7049ad94afb9f3d86120d974c1a40e9554ed9c21cd18f9ca4e0e30a4
size_bytes: 259256

## Release Reason / 发布原因

Patch release after round_003 stratified random spot-check found and closed a P2 terminology issue. / round_003 分层随机抽检发现并关闭 P2 专名术语问题后的补丁发布。

## Changes / 修改内容

- Rebuilt EPUB after fixing the Ra-Harmachis terminology translation. / 修复 Ra-Harmachis 专名译法后重建 EPUB。
- Closed round_003 Agent A P2 finding and preserved Agent A initial FAIL review plus post-fix PASS review. / 关闭 round_003 Agent A 的 P2 发现，并保留 Agent A 初审 FAIL 与修复后 PASS 记录。

## Issues / 问题点

- Agent A found P2 terminology issue: Ra-Harmachis was translated as 拉-哈拉赫提斯. / Agent A 发现 P2 专名术语问题：Ra-Harmachis 被译为拉-哈拉赫提斯。

## Fixes / 修复方式

- Changed the translation to 拉-哈马基斯 and verified it against the source paragraph. / 将译名改为拉-哈马基斯，并按原文段落复查确认。

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

- Only sampled units were reviewed in this iteration; future reader feedback or random spot-checks may still find non-sampled issues. / 本轮只审查抽样单元；后续读者反馈或随机抽检仍可能发现未抽到的问题。

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。
