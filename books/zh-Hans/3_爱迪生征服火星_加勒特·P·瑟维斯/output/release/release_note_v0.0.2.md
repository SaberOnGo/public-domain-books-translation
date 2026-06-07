# Release v0.0.2 / 版本 v0.0.2

status: PASS
main_version: 0
sub_version: 0
patch_version: 2
created_at: 2026-05-22T04:31:44Z
epub: book_v0.0.2.epub
sha256: 7d0e8bb1f2c72f0009f7e313c7b3447c173a7284a88b422ab228fb54a02c572f
size_bytes: 620222

## Release Reason / 发布原因

- 中文：本次发布由读者反馈和发布前分层随机抽检触发。读者指出首章 `puny efforts` 被译为“微弱的努力”极不自然，暴露出局部直译腔和语义框架问题；随后按模板启动双 Agent 分层随机抽检，发现并关闭多轮 P1/P2 阻断项。
- English: This release was triggered by reader feedback and pre-release stratified random spot checks. The reader-reported rendering of `puny efforts` as a stiff literal phrase exposed a local fluency and framing problem; the template-required two-agent spot-check loop then found and closed multiple P1/P2 blockers.

## Changes / 修改内容

- 中文：修复读者反馈句，将“微弱的努力”改为“我们那点微不足道的抵抗”，恢复原文自贬语气和疾病导致火星人败亡的因果关系。
- 中文：完成 10 轮分层随机抽检闭环；第 1-9 轮发现的问题已定点修复，第 10 轮双 Agent 均 PASS，无 P0/P1/P2、无低于 70 分样本。
- 中文：对全书多章进行出版级精修，覆盖事实逻辑、数值、术语一致性、人物/地名、战斗高潮对白、长句顺排、直译腔和不必要增译。
- 中文：重新构建 EPUB 并创建正式发布产物 `output/release/book_v0.0.2.epub`。
- English: Fixed the reader-reported `puny efforts` sentence so the Chinese now conveys humble resistance, not an awkward literal phrase.
- English: Completed ten stratified random spot-check rounds; issues from rounds 1-9 were fixed in place, and round 10 passed with both independent agents.
- English: Refined full-book publication text across factual logic, numeric accuracy, terminology consistency, names and places, battle-scene dialogue, long-sentence flow, literal translation residue, and unsupported embellishment.
- English: Rebuilt the EPUB and created the formal release artifact `output/release/book_v0.0.2.epub`.

## Issues / 问题点

- 中文：读者反馈：`puny efforts` 旧译“微弱的努力”不符合中文表达习惯，也弱化了原文“人类并非真正击败火星人”的语义。
- 中文：事实逻辑类问题：如洪水退去与粮食储备概率被译反、`those who were to do the work` 行动者关系错误、`one in ten` 避难容量关系失真、`wrecked here` 被误成“被困”。
- 中文：战斗与科学场景问题：如 `I cannot make it work` 被反向误译、闪电长度修饰错位、`four-fifths of an inch` 误作“四分之三英寸”。
- 中文：术语一致性问题：火星 `airship/aerial vessel` 与地球 `electrical ship/electric ship` 曾混用为“飞船/飞艇/空中舰艇”等，影响敌我装备区分。
- 中文：文学性与可读性问题：存在源文小标题污染正文、错字、双重否定、欧化长句、直译腔、口吻不稳和若干生硬专业词。
- 中文：无依据增译问题：`gillravaging villains` 曾被加重为“啃人骨头的恶棍”，引入原文没有的食人意象。
- English: Reader feedback identified the literal `puny efforts` rendering as unnatural and misleading in Chinese.
- English: Factual and logic blockers included inverted flood/provisions logic, actor-relation errors, a distorted one-in-ten refuge-capacity statement, and mistranslation of `wrecked here`.
- English: Battle and scientific blockers included a reversed `I cannot make it work`, a misplaced lightning-length modifier, and the numeric error `four-fifths of an inch` -> three-fourths.
- English: Terminology blockers mixed Martian `airship/aerial vessel` with Earth `electrical ship/electric ship`, weakening the enemy/fleet distinction.
- English: Literary and readability issues included source-subtitle contamination, typos, double negatives, stiff long sentences, literal phrasing, unstable tone, and awkward technical wording.
- English: One unsupported embellishment added a cannibalistic image not present in the source.

## Fixes / 修复方式

- 中文：读者反馈句已按原文 `not from our puny efforts, but from disease` 重译为“这并不是靠我们那点微不足道的抵抗，而是因为疾病”。
- 中文：所有 P1/P2 阻断项均在对应 `reviews/random_spotcheck/round_XXX/fixes/fix_log.md` 中登记，修复后写入 `chapters/final/` 与 `chapters/translated/`。
- 中文：统一装备术语：地球方 `electrical ship/electric ship` 以“电力飞船/飞船”为主，火星方 `airship/aerial vessel` 统一为“飞艇/火星飞艇”；清除“空中舰艇/电气飞船/电气飞艇/电气战舰”等残留混称。
- 中文：对数值、逻辑、人物名和地名逐项回查原文，包括“五分之四英寸”、Princess Masaco/公主雅子、Zanzibar/维多利亚女王一行等。
- 中文：修复战斗高潮和关键对白，使分解器故障、停火判断、小行星坠毁推理、补给危机等情节因果清楚。
- 中文：删除源文小标题污染和无依据增译，顺手精修可定位的 P3 直译腔、长句和专业表达。
- English: The reader-reported sentence was retranslated against `not from our puny efforts, but from disease`.
- English: Every P1/P2 blocker is logged in the matching round fix log and applied to both `chapters/final/` and `chapters/translated/`.
- English: Equipment terms were normalized so Earth ships and Martian airships remain distinct throughout the book.
- English: Numeric, logic, name, and place fixes were checked against the source text.
- English: Battle climaxes and key dialogue were rewritten for correct cause-and-effect and readable Chinese.
- English: Source-title contamination and unsupported embellishment were removed; localized P3 literalness and long-sentence issues were refined.

## Detailed Fix Points / 详细修复点

| area | examples | evidence |
| --- | --- | --- |
| 读者反馈 / reader feedback | `puny efforts` -> “我们那点微不足道的抵抗” | `reviews/random_spotcheck/round_001/fixes/fix_log.md`; `chapters/final/002_chapter_i.md` |
| 逻辑与事实 / logic and fidelity | 洪水与粮食概率、行动者关系、避难容量、坠毁推理 | rounds 001, 002, 004, 005 |
| 战斗高潮 / battle climaxes | 分解器“没法让它工作”、停火对白、闪电长度、太空跳跃动作 | rounds 001, 006 |
| 数值与科学 / numeric and science | `four-fifths of an inch` -> “五分之四英寸”；气闸门、电荷、电力作用等术语 | rounds 002, 004, 007 |
| 术语统一 / terminology | `airship/aerial vessel` -> “飞艇/火星飞艇”；`electrical ship/electric ship` -> “电力飞船/飞船” | rounds 008, 009 |
| 人名地名 / names and places | Princess Masaco -> “公主雅子”；Zanzibar/维多利亚女王一行语义修正 | round 005 |
| 文学性 / literary polish | 删除标题污染、修复错字和双重否定，精修欧化长句、直译腔、画面描写 | rounds 001-009 |
| 无依据增译 / unsupported embellishment | “啃人骨头的恶棍”改为“作恶的恶棍” | round 009 |

## QA And Evidence / QA 与证据

- source_epub: `output/book.epub`
- release_epub: `output/release/book_v0.0.2.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_010`
- random_spotcheck_validation: `reviews/random_spotcheck/round_010/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- release_confidence: `1.0`
- Agent A: `PASS`, `average_score=91.18`, `lowest_score=84`, `blocking_issue_count=0`
- Agent B: `PASS`, `average_score=95.05`, `lowest_score=93`, `blocking_issue_count=0`
- closure_check: `reviews/random_spotcheck/round_010/verification/closure_check.md`, `open_p0_p1_p2_count=0`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`

## Risks / 风险

- 中文：第 10 轮已通过模板门禁，但随机抽检不是全量逐句人工终审；后续如出现读者反馈、人工复核或自动化 QA 新发现，应进入下一个 patch release。
- 中文：本次修复覆盖大量章节和术语扫尾，提交前应避免把无关未跟踪文件混入同一 commit。
- English: Round 10 passed the required gate, but random spot-checking is not a full sentence-by-sentence human proofread; new reader feedback or QA findings should become a later patch release.
- English: This patch touches many chapters and terminology cleanups, so unrelated untracked files must be excluded from the commit.

## Next Iteration / 下一轮迭代

- 中文：如读者继续反馈具体句子，先对照原文定点修复，再按模板重新执行抽检闭环、EPUBCheck、publication lint 和版本化发布。
- 中文：如准备推送 GitHub，使用 `output/release/commit_message_v0.0.2.md` 中的中英日提交说明；代理只在本机 shell 环境中临时设置，不写入项目文件。
- English: For any later sentence-level reader feedback, fix against the source and then rerun the spot-check closure, EPUBCheck, publication lint, and versioned release flow.
- English: For GitHub delivery, use the trilingual commit message in `output/release/commit_message_v0.0.2.md`; proxy settings must remain shell-local and must not be committed.
