# Release Notes / 发布说明

## Release v0.0.1 / 版本 v0.0.1

status: PASS
main_version: 0
sub_version: 0
patch_version: 1
created_at: 2026-06-01T11:08:25Z
epub: 战国策：文言今译对照_v0.0.1.epub
sha256: 06e4569e43732f5f9181201ad0fd8e853931f61d347cbdc45a843bef0596abe7
size_bytes: 281066

## Release Reason / 发布原因

Create a versioned EPUB release artifact from the current book build. / 将当前书籍构建产物固化为带版本号的 EPUB 发布文件。

## Changes / 修改内容

- Created the public-domain release candidate EPUB for `战国策：文言今译对照` from the current full-book build. / 基于当前全书构建创建《战国策：文言今译对照》公版发布候选 EPUB。
- Preserved the electronic-text-first source strategy: readable public-domain electronic text is the working source, while scans/images remain control witnesses only. / 保留“可读电子文本优先”的来源策略：以可读公版电子文本为工作底本，扫描图像仅作校勘 witness。
- Closed the final stratified random spot-check in `round_003` with two independent PASS reviews. / 最终分层随机抽检 `round_003` 已由两名独立 reviewer 判定 PASS。

## Issues / 问题点

- Earlier random spot-check rounds found source-text integrity and fidelity defects that required repair before release. / 早期随机抽检轮次发现过原文层完整性和今译忠实度问题，发布前必须修复。
- `round_003` found only P3 readability/style suggestions and no P0/P1/P2 blockers. / `round_003` 仅发现 P3 可读性或风格建议，没有 P0/P1/P2 阻断问题。

## Fixes / 修复方式

- `round_001` repaired simplified/modernized text that had entered two classical source-text units, then closed the issue family with whole-book source-layer audit evidence. / `round_001` 修复两处古文原文层误入简化/现代化文本的问题，并以全书原文层同类审计证据闭环。
- `round_002` repaired two fidelity blockers: the wrong second-person reference in `贫穷则父母不子`, and the reversed/unsupported reading of `天下莫不傷`. / `round_002` 修复两处忠实度阻断项：`贫穷则父母不子` 的第二人称误指，以及 `天下莫不傷` 的方向性误译。
- Rebuilt the EPUB after repairs, passed EPUBCheck, publication lint, asset lint, cover gate, reader-facing gate, and final random PASS validation. / 修复后重新构建 EPUB，并通过 EPUBCheck、出版 lint、资产 lint、封面门禁、读者可见门禁和最终随机抽检 PASS 校验。

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

- Status is PASS; remaining risk is limited to non-blocking P3 readability/style refinements that can be handled in a later patch if reader feedback supports it. / 当前状态为 PASS；剩余风险限于非阻断的 P3 可读性或风格润色，可在后续读者反馈支持时进入小版本修订。

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。
