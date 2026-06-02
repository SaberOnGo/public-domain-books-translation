# Release Notes / 发布说明

## Release v0.0.6 / 版本 v0.0.6

status: PASS
main_version: 0
sub_version: 0
patch_version: 6
created_at: 2026-06-01T23:30:24Z
epub: 一座山的故事_v0.0.6.epub
sha256: 8f99586448bab2afc390821f0e62c76404ffbafc04f94c9b10619b6cf3d0b549
size_bytes: 282089

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
- random_spotcheck_round: `reviews/random_spotcheck/round_019`
- random_spotcheck_validation: `reviews/random_spotcheck/round_019/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- release_confidence: `1.0`
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


## Release v0.0.5 / 版本 v0.0.5

status: PASS
main_version: 0
sub_version: 0
patch_version: 5
created_at: 2026-06-01T23:24:12Z
epub: 一座山的故事_v0.0.5.epub
sha256: a901521e1ae1ec455afac6d2efe92591cdb0912e637f2e89c488f8839ec95c91
size_bytes: 285123

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
- random_spotcheck_round: `reviews/random_spotcheck/round_015`
- random_spotcheck_validation: `reviews/random_spotcheck/round_015/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- release_confidence: `1.0`
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
created_at: 2026-06-01T14:10:09Z
epub: 一座山的故事_v0.0.4.epub
sha256: c515a0877972fc003c83e4b6428f23c74346b782b1aa49b17efd9794d1b283f1
size_bytes: 285138

## Release Reason / 发布原因

Post-round_013 repair release after three consecutive no-blocking random spot-check rounds.

## Changes / 修改内容

- Closed round_013 Chinese semicolon hard-gate family and rebuilt EPUB.
- Validated round_014, round_015, and round_016 as consecutive no-blocking two-agent random spot-check rounds.

## Issues / 问题点

- No new issue entry was declared for this release note. / 本发布说明未声明新的问题条目。

## Fixes / 修复方式

- Replaced the remaining reader-facing Chinese semicolon in chapter 12 with sentence-level punctuation.
- Polished the chapter 4 molten-stone sentence reported as P3 in round_013.

## QA And Evidence / QA 与证据

- source_epub: `output/book.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_003`
- random_spotcheck_validation: `reviews/random_spotcheck/round_003/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- release_confidence: `1.0`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`

## Risks / 风险

- This validation was executed in a temporary writable clone because the original book directory currently denies script writes to output and review subdirectories.

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。


## Release v0.0.3 / 版本 v0.0.3

status: PASS
main_version: 0
sub_version: 0
patch_version: 3
created_at: 2026-05-31T22:37:01Z
epub: 一座山的故事_v0.0.3.epub
sha256: 1a51da64af1668c9d59dc9874e781399ba882ae44e97021777c1cad7d0f8d9b1
size_bytes: 285091

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
- release_confidence: `1.0`
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
created_at: 2026-05-31T14:28:02Z
epub: 一座山的故事_v0.0.2.epub
sha256: 6cc6f9045f9b6bdac6778af7aaa6d3d43e59344b1aec9eefb57c0ce4443eefd6
size_bytes: 285015

## Release Reason / 发布原因

Close the public-domain Chinese release after full-book repair, repeated random spot-check rework, and a new-seed two-agent PASS. / 在完成全书修复、多轮随机抽检返工和新 seed 双 Agent 通过后，固化公版中文发布版本。

## Changes / 修改内容

- Rebuilt the cover so title and producer text no longer overlap the mountain artwork. / 重做封面，使标题和制作标识不再压在山景图案上。
- Cleaned the translator note and reader-facing frontmatter so internal workflow commands do not appear in the book. / 清理译者说明和读者可见前置页，避免把内部工作指令泄露给读者。
- Repaired full-book Chinese punctuation and prose pressure, including the zero Chinese-semicolon publication gate. / 修复全书中文标点和阅读压迫感问题，并保持中文分号数量为零。
- Closed random spot-check rounds 002-005 with targeted fixes, then passed round 006 with two independent agents. / 闭环第 002-005 轮随机抽检问题，并在第 006 轮通过两个独立 Agent 评审。

## Issues / 问题点

- Earlier draft artifacts had reader-facing prose problems: cover text overlap, command-like wording in the translator note, heavy paragraph rhythm, and Chinese semicolon violations. / 早期草稿存在读者可见问题：封面文字压图、译者说明带内部指令口吻、段落节奏偏逼迫，以及中文分号违规。
- Random spot-check rounds found blocking P2 issues in place names, historical notes, animal terminology, and quotation boundaries. / 多轮随机抽检发现地名、历史译注、动物术语和引文边界等 P2 阻塞问题。

## Fixes / 修复方式

- Replaced the problematic cover layout and regenerated EPUB cover assets. / 替换问题封面布局并重新生成 EPUB 封面资源。
- Removed internal command phrasing from the translator note and rebuilt reader-facing XHTML. / 移除译者说明中的内部指令式表述并重建读者版 XHTML。
- Fixed all known P2 findings from rounds 002-005, including `Arabie Pétrée` as “佩特拉阿拉伯”, `chamois` as “欧洲山羚”, and a complete Tai-Chan quotation paragraph. / 修复第 002-005 轮全部已知 P2，包括将 `Arabie Pétrée` 处理为“佩特拉阿拉伯”、将 `chamois` 处理为“欧洲山羚”，并修正泰山引文段落边界。
- Ran fresh round 006 random samples after rework rather than reusing an old seed. / 返工后使用第 006 轮新 seed 抽检，没有复用旧样本自证通过。

## QA And Evidence / QA 与证据

- source_epub: `output/book.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_006`
- random_spotcheck_validation: `reviews/random_spotcheck/round_006/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- release_confidence: `1.0`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`

## Risks / 风险

- Round 006 still records non-blocking P3/P4 suggestions about Chinese rhythm and historical/medical wording; these should be handled as future patch-level polish if reader feedback confirms them. / 第 006 轮仍记录了关于中文节奏、历史医学表述的非阻塞 P3/P4 建议；若读者反馈确认，可进入后续小版本润色。

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。


## Release v0.0.1 / 版本 v0.0.1

status: DRAFT
main_version: 0
sub_version: 0
patch_version: 1
created_at: 2026-05-31T10:10:41Z
epub: 一座山的故事_v0.0.1.epub
sha256: d006011fad994df56e9a1dd8edd21f8f244149ce913ac728f9eb1fa71821a350
size_bytes: 309798

## Release Reason / 发布原因

Create a draft EPUB artifact after full build and structural random-sample validation; independent review remains pending.

## Changes / 修改内容

- Translated 22 chapters of Reclus Histoire d'une Montagne into Simplified Chinese and promoted them to chapters/final.
- Added cover, book-info frontmatter, production spec, chapter gates, imagery checks, readability audits, and generated output/book.epub.

## Issues / 问题点

- PASS release is blocked until two independent random spot-check reviews and closure verification are completed.

## Fixes / 修复方式

- No fix entry was declared for this release note. / 本发布说明未声明新的修复条目。

## QA And Evidence / QA 与证据

- source_epub: `output/book.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_001`
- random_spotcheck_validation: `reviews/random_spotcheck/round_001/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `False`
- release_confidence: `1.0`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`

## Risks / 风险

- DRAFT artifact is for review only and is not a DONE/release PASS artifact.

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。
