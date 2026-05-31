# 18 最终输出 / Final EPUB Output

## 目的 / Purpose

在所有翻译、预制作、样章、全书制作、双 Agent 评审、回退修复都通过后，输出正本 EPUB。

## 输入 / Input

- `output/book.epub`
- `reviews/scorecards/final_quality_score.md`
- `reviews/scorecards/random_spotcheck_score.md`
- `reviews/random_spotcheck/random_sample_manifest.json`
- `reviews/random_spotcheck/round_XXX/verification/closure_check.md`
- `reviews/revision_route.md`
- `output/publication_lint.json`
- `output/epubcheck.json` 或 `output/epubcheck.log`
- 公版或授权项目：`output/release/book_vX.X.X.epub`、`output/release/release_notes.md`、`output/release/release_state.json`
- `private_use` 项目：`output/private_artifacts/{title}_private_vX.X.X.epub`、`private_artifact_notes.md`、`private_artifact_state.json`

## 最终检查 / Final Checks

必须确认：

1. EPUBCheck：fatal=0，error=0；warning 必须解释或修复。
2. EPUB 内有封面，且 OPF manifest 标记 `cover-image`。
3. 公版或授权项目的版本说明页存在，并含 `LifeBook 书坊 + 个人名`、译制时间、公版来源 URL、公版说明；`private_use` 项目必须按 `modes/private_use` 覆盖层检查私人首页/前置页，含 `参考LifeBook书坊 个人自制`、个人自用/不传播/不商业使用和风险边界，且不得含公版说明。
4. 无旧品牌名残留。
5. 标题层级、字体策略、正文排版符合 `production_spec.md`。
6. 章节标题已按 `references/chapter_title_policy.md` 和 `references/japanese_title_strategy.md` 检查：无半截标题、无日文原题/读音/罗马字/解释性括注污染，EPUB 目录使用短题名。
   - 若日语原章只有编号、无题分隔或简单题名，不得出现 AI 自拟的可见中文小标题；解释性概括只能放入 `title_note`、制作说明或 QA。
7. 文件体积合理，封面和字体未异常膨胀。
8. 双 Agent 评审分数达到 PASS。
9. 分层随机抽检已覆盖实际存在的正文、表格、图片、公式/证明块、图注/注释；`reviews/random_spotcheck/round_XXX/` 下样本、证据、评审、修复记录和闭环验证齐全。
10. `npm run review:random-validate:pass` 已通过；若发生返工，最终通过轮次使用的是新 seed。
11. 公版或授权项目已执行 `prompts/18a_release_versioning.md` 或 `npm run release:create`，并且 `output/release/release_state.json.latest_status = PASS`；`private_use` 项目已执行 `npm run private:artifact:create`，并且 `output/private_artifacts/private_artifact_state.json.latest_status = PASS`。
12. `release_notes.md` 或 `private_artifact_notes.md` 已记录发布/产物原因、问题点、修复方式、QA 证据、风险和下一轮迭代。
13. `output/publication_lint.json` 无硬错误；不存在分号滥用、异常连续空格、旧纸书页码目录、乱码、普通名词原文括注或旧纸书可见分隔符，且 `targetTitleLatinResidue=0`、`sourceTermBeforeTranslation=0`、`bodyOriginalTermGloss=0`、`bodySceneSeparator=0`。
14. 如本书存在系统性精修问题，`goal/` 下已有本书目标或完成记录，且可复用经验已回填到 common、zh-Hans 或 ja-zh-Hans 模板。
15. 标题中的人名不计入“正文首次出现”：章节标题、副标题和目录题名只用中文译名或本书确定的中文呈现方式；日文原名、读音或罗马字只可放在正文第一次自然出现处、译注、术语表或书籍信息页。
16. 普通名词必须直接译成中文正文，不附加原文词括注；`* * * * *`、`*****`、`----`、`---` 等纸书分隔符已删除，而不是换成另一种符号。
17. 若模板包含 `scripts/refinement_check.js`，运行后 `qa/refinement/refinement_check.json` 已保存；出版范围内 BOM、乱码、异常连续空格和不当标点为 0，或已有明确例外说明。

## 输出 / Output

- `output/book.epub`
- 公版或授权项目：`output/release/book_vX.X.X.epub`、`output/release/release_notes.md`
- `private_use` 项目：`output/private_artifacts/{title}_private_vX.X.X.epub`、`output/private_artifacts/private_artifact_notes.md`
- `output/publication_lint.json`
- `output/final_manifest.md`

## 状态 / State

通过后：

- `state/pipeline_state.json.status = FINAL_OUTPUT_PASS`

注意：此状态还不是 `DONE`，必须进入第 19 阶段复审和经验沉淀。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <70、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.
