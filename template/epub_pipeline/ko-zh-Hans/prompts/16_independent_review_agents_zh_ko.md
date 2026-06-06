# 16 双 Agent 独立评审 / Independent Two-Agent Review

## 目的 / Purpose

全书 EPUB 制作后，主执行 AI 不得直接宣布完成。必须派生 2 个独立评审 Agent，从不同角度审查成书质量，避免主执行者自证通过。

## 强制要求 / Mandatory Requirement

AI 必须派生两个评审 Agent：

- Agent A：内容与翻译质量评审。
- Agent B：EPUB 工程、排版、metadata、封面与可读性评审。

两个 Agent 必须独立阅读模板要求、产物和评分表，不得互相参考，不得只复述主执行 AI 的结论。

精校后还必须执行分层随机抽检。随机抽检不是可选补充，而是进入最终独立评审前的硬门禁：第一版全书 EPUB 生成后和每一轮精校完成后，都必须重新生成抽检样本，并由至少 2 个独立 Agent 检查正文段落、表格、图片、公式/证明块、图注/注释等读者可见审计单元。

## 输入 / Input

- `output/book.epub`
- `output/publication_lint.json`
- `output/epubcheck.json` 或 `output/epubcheck.log`
- `preproduction/stage1/production_spec.md`
- `preproduction/stage2_sample/sample_review.md`
- `qa/gates/*.gate.md`
- `qa/chapter_controls/*.control.md`
- `reviews/scorecards/_TEMPLATE_scorecard.md`
- `reviews/scorecards/_TEMPLATE_random_spotcheck_score.md`
- `reviews/random_spotcheck/random_sample_manifest.json`
- `reviews/random_spotcheck/agent_a_samples.md`
- `reviews/random_spotcheck/agent_b_samples.md`
- `reviews/random_spotcheck/round_XXX/`

## 输出 / Output

- `reviews/agent_a/review.md`
- `reviews/agent_b/review.md`
- `reviews/agent_a/random_spotcheck_review.md`
- `reviews/agent_b/random_spotcheck_review.md`
- `reviews/scorecards/random_spotcheck_score.md`
- `reviews/scorecards/final_quality_score.md`

## 分层随机抽检硬门禁 / Stratified Random Spot-Check Gate

主执行 AI 在第一版全书 EPUB 生成后和每一轮精校完成后，必须先生成分层随机抽检样本：

```powershell
npm run review:random-samples
```

若项目没有 npm 脚本，则运行等效命令：

```powershell
python scripts/select_random_review_passages.py --source-dir chapters/final --agents 2 --samples-per-agent 120 --rounds-planned 4 --target-confidence 0.80 --defect-rate 0.10 --profile auto
```

抽检规则：

- 至少 2 个独立 Agent。
- 默认发布抽检为 `T=4`、`agents=2`。正文/文本层每个 Agent 每轮 120 个样本；表格、图片 `N<=80` 全检，否则每轮总抽 20 个；公式/证明块 `N<=100` 全检，否则每轮总抽 20 个；图注/表注/注释 `N<=120` 全检，否则每轮总抽 20 个。
- 若任一层、任一样本发现任何需要修复或可能系统性复现的问题，本轮立即把发现归纳为问题族，并执行全书同类问题审计和闭环；不得只修被抽中的样本，也不得等到第二轮才全书检查。同层可被标记为高风险，用于后续抽样和人工复核，但不能替代本轮全书同类问题审计。
- 脚本会读取最近 `round_XXX/reviews/*_review.md` 中带样本单元编号的 P0/P1/P2 行，并自动记录该层风险字段；主执行 AI 不得手动删除脚本生成的风险字段。风险字段只用于后续抽样和复核，不能替代本轮问题族全书同类审计。
- 抽样总体 `N` 是读者可见审计单元总数，不是页数，也不只是正文段落数。
- 抽样层至少包括 `paragraph`、`table`、`figure`、`formula`、`caption_note`。
- 样本必须来自读者可见终稿文本和对应资源；不得由主执行 AI 人工挑选“看起来没问题”的内容。
- `round_XXX/random_sample_manifest.json` 必须记录 seed、每层候选数、每层抽样数、Agent 数和每个 Agent 的样本编号。
- 图片、表格、公式等证据必须保存在 `round_XXX/evidence/`，方便人工核查。
- 两个 Agent 不得互相参考结论；不得只复述主执行 AI 的判断。

每个抽检 Agent 必须假设自己是认真阅读本书的中文读者，并逐段检查：

- 这一段中文是否能自然读懂。
- 是否忠实于韩语/朝鲜语公版原文，不借现代中文译本或其他译本改写。
- 韩语/朝鲜语修饰链、省略、敬语、称谓、人物关系、历史语境、动作强度和叙述立场是否被正确转成自然中文。
- 官能、暴力、病态心理或强制关系内容是否保持原作文学边界，没有加重、删弱、猎奇化或道德说教化。
- 术语、专名、译注、标题策略和段落节奏是否符合本模板设计。
- EPUB 手机阅读时是否会因长段、注释、标题、图表或排版影响理解。
- 表格行列、表头、数值、单位、caption 和 XHTML 结构是否正确。
- 图片裁剪是否过大或过小，是否带入周边无关文字，是否裁掉标签，插入点、caption、alt 是否正确。
- 公式/证明块的符号、依赖关系和读者可理解性是否正确。

评分规则：

- 每个样本 0-100 分。
- 发布硬失败线：每个 Agent 的平均分和最低分不得低于 80；最终优秀出版线：每个 Agent 平均分必须 >= 92，最低分必须 >= 88。
- 任一单段 < 80，则该 Agent 抽检失败。
- 任一样本出现读者读不懂、事实或叙述关系误解、韩语/朝鲜语句法硬搬、无依据润饰、术语/专名/译注/表格/图片/公式错误，必须判为失败，即使平均分达标。
- 任一 Agent 抽检失败时，必须写入 `reviews/revision_route.md`，回到精校或更早阶段修复；修复后必须在旧轮次 `fixes/fix_log.md` 和 `verification/closure_check.md` 中记录问题族、全书同类问题审计范围、命中、修复、合理例外和关闭结论，并用新 seed 重新生成样本。

## Agent A 重点 / Agent A Focus

- 译文忠实度。
- 中文可读性。
- 是否有 AI 味、机械味、省字式翻译。
- 是否存在无依据发挥、韩语/朝鲜语汉字词误用或暧昧心理过度解释。
- 专名、术语、年代、地点、人物一致性。
- 章节标题是否忠实传达原题功能，而不是半截标题、读音堆积或解释性括注。
- 章节质量是否符合前置研究和风格画像。

## Agent B 重点 / Agent B Focus

- EPUB 结构、OPF、spine、nav、cover-image。
- 封面大小、格式、清晰度、书架显示。
- 字体策略是否合理，是否影响阅读器字体设置。
- 章节标题、正文排版、版本说明页。
- `nav.xhtml` 是否使用短目录题名；页面标题是否有合理层级和可选副标题。
- 出版文本 lint 是否通过；是否还有分号滥用、异常空格、旧纸书页码目录或乱码。
- metadata 是否完整：公版或授权项目检查 `LifeBook 书坊 + 个人名`、译制时间、公版来源 URL、公版说明、作者信息、原书信息；`private_use` 项目检查 `参考LifeBook书坊 个人自制`、个人自用/不传播/不商业使用、风险边界、本地书源证据，且不得含公版说明。
- 文件体积是否异常。
- EPUBCheck 是否 0 fatal、0 error。

## PASS 条件 / PASS Criteria

- Agent A 总分 >= 85。
- Agent B 总分 >= 85。
- 分层随机抽检已通过：Agent A/B 抽检均达到优秀出版线（平均分 >= 92、最低分 >= 88），无单项 < 80，无缺失逐样本评分行，无未关闭 P0/P1/P2，且 `npm run review:random-validate:pass` 通过。
- 任一 P0/P1 问题必须返工。
- 任一 Agent 明确指出严重问题时，主执行 AI 必须进入回退路由，不得忽略。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.
