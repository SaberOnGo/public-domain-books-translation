# Release v0.0.1 / 版本 v0.0.1

status: DRAFT
main_version: 0
sub_version: 0
patch_version: 1
created_at: 2026-05-18T03:20:58Z
epub: book_v0.0.1.epub
sha256: 39676fbbbc4e5a5c84325111560f6580b14f7039c77af225fa05ecc5aa147ea8
size_bytes: 259251

## Release Reason / 发布原因

Initial versioned EPUB release candidate after running the stratified random spot-check template. / 执行分层随机抽检模板后生成首个版本化 EPUB 候选发布。

## Changes / 修改内容

- Created output/release/book_v0.0.1.epub from output/book.epub. / 从 output/book.epub 生成 output/release/book_v0.0.1.epub。
- Recorded random spot-check evidence from reviews/random_spotcheck/round_001. / 记录 reviews/random_spotcheck/round_001 的随机抽检证据。

## Issues / 问题点

- Independent Agent PASS review and fix closure were not completed in this example run. / 本示例未完成独立 Agent PASS 评审和修复闭环。

## Fixes / 修复方式

- No book-content fix was applied; this run only created sampling evidence and release packaging. / 本次未修改书籍正文内容，只生成抽样证据和发布包装。

## QA And Evidence / QA 与证据

- source_epub: `output/book.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_001`
- random_spotcheck_validation: `reviews/random_spotcheck/round_001/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `False`
- release_confidence: `0.998203`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`

## Risks / 风险

- DRAFT only; not eligible for DONE until review:random-validate:pass and release:create pass. / 仅为 DRAFT；必须通过 review:random-validate:pass 和 release:create 后才可作为 DONE。

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。
