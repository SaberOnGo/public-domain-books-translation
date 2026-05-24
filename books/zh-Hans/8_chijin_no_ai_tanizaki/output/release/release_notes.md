# Release Notes / 发布说明

## Release v0.0.3 / 版本 v0.0.3

status: PASS
main_version: 0
sub_version: 0
patch_version: 3
created_at: 2026-05-24T04:18:26Z
epub: 痴人之爱_v0.0.3.epub
sha256: a6a22d30632396ef74782418b156bd5ede7e85140225c8904bf913073b4e76b7
size_bytes: 324453

## Release Reason / 发布原因

常识误读与译文自然度专项修复后重新发布。/ Re-release after fixing common-sense misreading risks and unnatural Chinese renderings.

## Changes / 修改内容

- 补充历史货币、佛事日期、时代词和旧度量衡的克制短注规则。/ Added restrained annotation rules for historical currency, Buddhist memorial dates, period terms, and old measurements.
- 同步更新公共简体中文质量规则、日文到简体中文精修规则、本书术语表、风格档案和译制说明。/ Updated the Simplified Chinese quality rules, Japanese-to-Simplified-Chinese refinement rules, book glossary, style profile, and translator note.
- 重新生成 PASS 状态的 EPUB 发布文件。/ Regenerated the PASS release EPUB.

## Issues / 问题点

- `月給百五十円` 原文无误，但若译作现代感较强的货币表达，容易被读者按今日币值误读。/ The source `月給百五十円` is correct, but a modern-looking currency rendering can make readers misread it as present-day value.
- 部分句子存在日式副词和抽象搭配硬译，例如“可是她奇怪地并不高兴”。/ Some passages contained Japanese-influenced adverbial or abstract phrasing, such as the unnatural Chinese sentence “可是她奇怪地并不高兴”.

## Fixes / 修复方式

- 将 `円` 统一处理为历史货币语境的“圆”，首次金额处加短注说明不可按今日币值理解。/ Rendered `円` consistently as historical “圆”, with a first-use note that the value should not be read as present-day currency.
- 将 `二七日` 修正为 `二七忌（逝后第十四日的佛事）`，避免误读成二十七日。/ Corrected `二七日` to `二七忌（逝后第十四日的佛事）` to avoid misreading it as the twenty-seventh day.
- 修复“可是她奇怪地并不高兴”“可怕地摩登”“真实感威胁”等不自然表达。/ Fixed unnatural renderings including “可是她奇怪地并不高兴”, “可怕地摩登”, and “真实感威胁”.

## QA And Evidence / QA 与证据

- source_epub: `output/book.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_024`
- random_spotcheck_validation: `reviews/random_spotcheck/round_024/validation_report.json`
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
created_at: 2026-05-24T03:26:16Z
epub: 痴人之爱_v0.0.2.epub
sha256: 24d1964a04d03debbad2c54ea053a1ca6632d8e1db4d64cd66f34167fd01fb68
size_bytes: 324219

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
- random_spotcheck_round: `reviews/random_spotcheck/round_024`
- random_spotcheck_validation: `reviews/random_spotcheck/round_024/validation_report.json`
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


## Release v0.0.1 / 版本 v0.0.1

status: PASS
main_version: 0
sub_version: 0
patch_version: 1
created_at: 2026-05-23T22:38:27Z
epub: 痴人之爱_v0.0.1.epub
sha256: 87f9416e485bf4c2261f04d5145261c151ec7aa1708920e0ec23096ac9d5b864
size_bytes: 323976

## Release Reason / 发布原因

Complete the first PASS release of Tanizaki Junichiro's `Chijin no Ai` in Simplified Chinese after full translation, EPUB production, seven random spot-check rounds, and release validation. / 在完成谷崎润一郎《痴人の愛》简体中文全书翻译、EPUB 制作、七轮随机抽检与发布验证后，固化第一版 PASS 发布物。

## Changes / 修改内容

- Created the versioned release EPUB `痴人之爱_v0.0.1.epub`.
- Recorded final manifests, two-agent random review compatibility entries, scorecards, and retrospective files.
- Preserved source and rights evidence for the Aozora Bunko Japanese public-domain source.

## Issues / 问题点

- Earlier random spot-check rounds found P1/P2 translation and reader-facing defects, especially mechanical Japanese-to-Chinese connection errors around `そう云って` / `そう云うと` / `そう云われて`, paragraph-boundary hanging punctuation, and a few lexical or agency mistakes.
- Round 007 found no P0/P1/P2 and no sample below 70 across the two independent agents.

## Fixes / 修复方式

- Closed all blocking findings from rounds 001-006 in each round's `fix_log.md` and `closure_check.md`.
- Rebuilt the EPUB after the final round 006 repairs, then generated a fresh round 007 seed and passed both independent reviews.
- Final random validation passed with `release_confidence=1.0`.

## QA And Evidence / QA 与证据

- source_epub: `output/book.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_007`
- random_spotcheck_validation: `reviews/random_spotcheck/round_007/validation_report.json`
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

- No known P0/P1/P2 remains at release time.
- Some P3-level wording refinements may still be possible in future patch releases, especially for dense literary sentences.
- This book has no table, figure, formula, or caption/note strata in the reader-facing content; validation therefore treats those strata as empty.

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。
