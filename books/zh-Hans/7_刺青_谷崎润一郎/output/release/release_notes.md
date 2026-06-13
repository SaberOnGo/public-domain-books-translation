# Release Notes / 发布说明

## Release v0.0.4 / 版本 v0.0.4

status: PASS
main_version: 0
sub_version: 0
patch_version: 4
created_at: 2026-05-23T07:27:28Z
epub: 刺青_v0.0.4.epub
sha256: 3cb26939d4af776d6ac584f2e303881b179083911d3ffa936f01f23f3c70f449
size_bytes: 296901

## Release Reason / 发布原因

Fix reader-facing paragraph structure after user review found sentence-by-sentence paragraphing in the body text. / 用户复查发现正文被拆成一句一段，影响阅读版式；本版本修复读者可见段落结构并重新发布。

## Changes / 修改内容

- Restored `chapters/src/001_shisei.md` to Aozora-style natural paragraph and dialogue boundaries. / 将 `chapters/src/001_shisei.md` 恢复为青空整理稿的自然段和对白边界。
- Synchronized `chapters/translated/001_shisei.md` and `chapters/final/001_shisei.md`; final body now has 54 reader paragraphs instead of 121 sentence-level paragraphs. / 同步修复 `chapters/translated/001_shisei.md` 与 `chapters/final/001_shisei.md`；终稿正文由 121 个句级段落恢复为 54 个读者段落。
- Added a paragraph-structure QA record and strengthened the Japanese-to-Simplified-Chinese template prompts against sentence-level paragraph splitting. / 新增段落结构 QA 记录，并补强日语到简体中文模板，防止继续把自然段拆成单句段落。

## Issues / 问题点

- Body text had been over-split into many one-sentence paragraphs, although the Japanese source preserved longer natural paragraphs. / 正文此前被过度拆成大量单句段落，但日文底本保留的是较长自然段。

## Fixes / 修复方式

- Compared the full short story against `source/source_text.txt`, merged sentence-level paragraph splits, retained supported dialogue and strong-pause paragraphing, rebuilt EPUB output, and generated a new random spot-check round. / 对照 `source/source_text.txt` 全篇检查，合并句级拆段，保留有依据的对白和强停顿段落，重新构建 EPUB，并生成新一轮随机抽检。

## QA And Evidence / QA 与证据

- source_epub: `output/book.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_005`
- random_spotcheck_validation: `reviews/random_spotcheck/round_005/validation_report.json`
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

- Minor style notes remain P3 only; no P0/P1/P2 or blocking paragraph-structure issue was found in round_005. / 仍有少量 P3 级别顺滑度意见；round_005 未发现 P0/P1/P2 或阻断性段落结构问题。

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。


## Release v0.0.3 / 版本 v0.0.3

status: PASS
main_version: 0
sub_version: 0
patch_version: 3
created_at: 2026-05-23T06:37:25Z
epub: 刺青_v0.0.3.epub
sha256: 24f7a87c491ef1f62f321216d64d1457159a0f0e0dbfbb814a63119d65dc3b03
size_bytes: 296935

## Release Reason / 发布原因

Final release from the post-closure rebuilt EPUB after round_004 PASS validation.

## Changes / 修改内容

- Created final release artifact from the latest rebuilt output/book.epub.
- Kept cleaned release notes, final manifest, and synchronized pipeline state.

## Issues / 问题点

- Previous release artifact hash no longer matched the final rebuilt output/book.epub.

## Fixes / 修复方式

- Created a new patch release after final rebuild and EPUBCheck PASS.

## QA And Evidence / QA 与证据

- source_epub: `output/book.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_004`
- random_spotcheck_validation: `reviews/random_spotcheck/round_004/validation_report.json`
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

- Cross-region copyright and platform policy still require review before distribution outside the verified Japanese source-public-domain basis.

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。


## Release v0.0.2 / 版本 v0.0.2

status: PASS
main_version: 0
sub_version: 0
patch_version: 2
created_at: 2026-05-23T06:31:42Z
epub: 刺青_v0.0.2.epub
sha256: 6ebba4284d65d05da8b505cfab552b050e15ca82886e2a24131617399b6e8d11
size_bytes: 296934

## Release Reason / 发布原因

Complete release after cover/frontmatter/metadata rights repair and round_004 stratified random spot-check closure.

## Changes / 修改内容

- Updated cover/frontmatter/metadata synchronization and contributor naming.
- Corrected Japanese rights evidence for Tanizaki Junichiro and rebuilt EPUB.
- Closed round_003 findings and verified a new round_004 seed with two independent agents.

## Issues / 问题点

- round_003 found rights/contributor/release evidence issues before release.

## Fixes / 修复方式

- Synchronized book-info, metadata, OPF contributor, source evidence, rights checklist, and build script frontmatter ordering/metadata output.
- round_004 passed with release_confidence=1.0 and no open P0/P1/P2.

## QA And Evidence / QA 与证据

- source_epub: `output/book.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_004`
- random_spotcheck_validation: `reviews/random_spotcheck/round_004/validation_report.json`
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

- Cross-region copyright and platform policy still require review before distribution outside the verified Japanese source-public-domain basis.

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。


## Release v0.0.1 / 版本 v0.0.1

status: PASS
main_version: 0
sub_version: 0
patch_version: 1
created_at: 2026-05-22T15:45:07Z
epub: 刺青_v0.0.1.epub
sha256: 92e1e93aba57bdabef4924db35a0036d54271e0cfca8f19d557b08153cfcf654
size_bytes: 158822

## Release Reason / 发布原因

Complete Japanese-to-Simplified-Chinese template trial run for Tanizaki Junichiro's Shisei after stratified random spot-check closure.

## Changes / 修改内容

- Generated source evidence, rights records, translation, QA, EPUB, and final release artifact.

## Issues / 问题点

- No new issue entry was declared for this release note. / 本发布说明未声明新的问题条目。

## Fixes / 修复方式

- Closed round_001 P2 proper-noun issue by changing 絵の島 from 绘岛 to 江之岛 and rerunning build/check/round_002.

## QA And Evidence / QA 与证据

- source_epub: `output/book.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_002`
- random_spotcheck_validation: `reviews/random_spotcheck/round_002/validation_report.json`
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

- Superseded by v0.0.2 rights review: Tanizaki Junichiro's Japanese economic rights had expired before the 2018 term extension, but cross-region distribution still requires review.

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。
