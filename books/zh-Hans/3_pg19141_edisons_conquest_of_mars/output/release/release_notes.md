# Release Notes / 版本发布记录

## Release v0.0.2 / 版本 v0.0.2

status: PASS
created_at: 2026-05-22T04:31:44Z
epub: `book_v0.0.2.epub`
sha256: `7d0e8bb1f2c72f0009f7e313c7b3447c173a7284a88b422ab228fb54a02c572f`

### Release Reason / 发布原因

- 中文：读者反馈指出首章 `puny efforts` 旧译“微弱的努力”不自然且影响语义；本次按模板启动双 Agent 分层随机抽检，并将第 1-9 轮发现的问题逐项关闭后生成正式 PASS 发布。
- English: Reader feedback identified the old literal rendering of `puny efforts` as unnatural and semantically weak; this release ran the template-required two-agent stratified spot-check loop, closed issues from rounds 1-9, and produced a PASS artifact.

### Changes / 修改内容

- 中文：修复读者反馈句，统一术语，修正事实逻辑、数值、人名地名、战斗高潮对白、长句和直译腔，并重新生成 EPUB。
- English: Fixed the reader-reported sentence, normalized terminology, corrected logic/numeric/name/place/dialogue issues, improved stiff long sentences and literal phrasing, and rebuilt the EPUB.

### Issues / 问题点

- 中文：问题覆盖 `puny efforts` 生硬直译、洪水与粮食逻辑反向、`I cannot make it work` 反向误译、`four-fifths of an inch` 数值错误、火星飞艇与地球电力飞船术语混用、源小标题污染正文、错字、双重否定和无依据增译。
- English: Issues included the stiff `puny efforts` literalism, inverted flood/provisions logic, reversed `I cannot make it work`, a `four-fifths of an inch` numeric error, mixed Martian airship vs Earth electrical ship terminology, source-subtitle contamination, typos, double negatives, and unsupported embellishment.

### Fixes / 修复方式

- 中文：所有 P1/P2 阻断项均写入对应 `reviews/random_spotcheck/round_XXX/fixes/fix_log.md`，并同步修复 `chapters/final/` 与 `chapters/translated/`；第 10 轮双 Agent PASS 后创建 v0.0.2 发布。
- English: All P1/P2 blockers were recorded in the matching `reviews/random_spotcheck/round_XXX/fixes/fix_log.md` files and applied to both `chapters/final/` and `chapters/translated/`; v0.0.2 was created after both agents passed round 10.

### QA And Evidence / QA 与证据

- random_spotcheck_round: `reviews/random_spotcheck/round_010`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- release_confidence: `1.0`
- Agent A: `PASS`, `average_score=91.18`, `lowest_score=84`, `blocking_issue_count=0`
- Agent B: `PASS`, `average_score=95.05`, `lowest_score=93`, `blocking_issue_count=0`
- closure_check: `reviews/random_spotcheck/round_010/verification/closure_check.md`, `open_p0_p1_p2_count=0`
- epubcheck_fatal/error/warning: `0/0/0`
- publication_lint_issue_count: `0`

### Risks / 风险

- 中文：随机抽检已通过模板门禁，但不是全量逐句人工终审；后续读者反馈或 QA 新发现应进入下一 patch release。提交时需排除无关未跟踪文件。
- English: The random spot-check gate passed, but it is not a full sentence-by-sentence human proofread; later reader feedback or QA findings should enter the next patch release. Exclude unrelated untracked files when committing.

### Next Iteration / 下一轮迭代

- 中文：如有新反馈，继续按“原文核对 -> 定点修复 -> 新 seed 抽检 -> EPUBCheck/publication lint -> 版本发布”闭环处理。
- English: For new feedback, continue the source-check -> targeted fix -> new-seed spot check -> EPUBCheck/publication lint -> versioned release loop.

## Release v0.0.1 / 版本 v0.0.1

status: DRAFT
created_at: 2026-05-18T07:44:11Z
epub: `book_v0.0.1.epub`
sha256: `fa8874a254ed5aa97a86d0f2440d058db8c854e8d496de51554ba0d7cc6aa3dc`

### Release Reason / 发布原因

- 中文：将当时的 `output/book.epub` 固化为候选发布文件，供人工核查。
- English: Froze the then-current `output/book.epub` as a draft release artifact for manual review.

### QA And Evidence / QA 与证据

- status: `DRAFT`
- epubcheck_fatal/error/warning: `0/0/0`
- publication_lint_issue_count: `0`
- random_spotcheck_status: `MISSING`

### Risks / 风险

- 中文：v0.0.1 这个候选版本未完成随机抽检 PASS 闭环，不能作为最终 DONE 依据；最新正式版本 v0.0.2 已完成 PASS 闭环。
- English: The v0.0.1 draft release did not complete the random spot-check PASS closure and cannot be used as the final DONE basis; the latest formal v0.0.2 release has completed the PASS closure.
