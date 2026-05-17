# 16 双 Agent 独立评审 / Independent Two-Agent Review

## 目的 / Purpose

全书 EPUB 制作后，主执行 AI 不得直接宣布完成。必须派生 2 个独立评审 Agent，从不同角度审查成书质量，避免主执行者自证通过。

## 强制要求 / Mandatory Requirement

AI 必须派生两个评审 Agent：

- Agent A：内容与翻译质量评审。
- Agent B：EPUB 工程、排版、metadata、封面与可读性评审。

两个 Agent 必须独立阅读模板要求、产物和评分表，不得互相参考，不得只复述主执行 AI 的结论。

精校后还必须执行随机段落抽检。随机抽检不是可选补充，而是进入最终独立评审前的硬门禁：每一轮精校完成后，都必须重新生成抽检样本，并由至少 2 个独立 Agent 各自检查不少于 10 个随机段落。

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

## 输出 / Output

- `reviews/agent_a/review.md`
- `reviews/agent_b/review.md`
- `reviews/agent_a/random_spotcheck_review.md`
- `reviews/agent_b/random_spotcheck_review.md`
- `reviews/scorecards/random_spotcheck_score.md`
- `reviews/scorecards/final_quality_score.md`

## 随机抽检硬门禁 / Random Spot-Check Gate

主执行 AI 在每一轮精校完成后，必须先生成随机抽检样本：

```powershell
npm run review:random-samples
```

若项目没有 npm 脚本，则运行等效命令：

```powershell
python scripts/select_random_review_passages.py --source-dir chapters/final --agents 2 --samples-per-agent 10
```

抽检规则：

- 至少 2 个独立 Agent。
- 每个 Agent 至少 10 个随机正文段落。
- 样本必须来自读者可见终稿文本；不得由主执行 AI 人工挑选“看起来没问题”的段落。
- `random_sample_manifest.json` 必须记录 seed、候选段落数、每个 Agent 的样本编号。
- 两个 Agent 不得互相参考结论；不得只复述主执行 AI 的判断。

每个抽检 Agent 必须假设自己是认真阅读本书的中文读者，并逐段检查：

- 这一段中文是否能自然读懂。
- 是否忠实于英文公版原文，不借现代中文译本或其他译本改写。
- 英文长句、称谓、人物关系、历史语境、动作强度和叙述立场是否被正确转成自然中文。
- 术语、专名、译注、标题策略和段落节奏是否符合本模板设计。
- EPUB 手机阅读时是否会因长段、注释、标题、图表或排版影响理解。

评分规则：

- 每段 0-100 分。
- 每个 Agent 的平均分必须 >= 75。
- 任一单段 < 70，则该 Agent 抽检失败。
- 任一段出现读者读不懂、事实或叙述关系误解、英文句法硬搬、无依据润饰、术语/专名/译注错误，必须判为失败，即使平均分达标。
- 任一 Agent 抽检失败时，必须写入 `reviews/revision_route.md`，回到精校或更早阶段修复；修复后重新生成随机样本，重新执行两个 Agent 抽检。

## Agent A 重点 / Agent A Focus

- 译文忠实度。
- 中文可读性。
- 是否有 AI 味、机械味、省字式翻译。
- 是否存在无依据发挥。
- 专名、术语、年代、地点、人物一致性。
- 章节标题是否忠实传达原题功能，而不是机械破折号链或半截标题。
- 章节质量是否符合前置研究和风格画像。

## Agent B 重点 / Agent B Focus

- EPUB 结构、OPF、spine、nav、cover-image。
- 封面大小、格式、清晰度、书架显示。
- 字体策略是否合理，是否影响阅读器字体设置。
- 章节标题、正文排版、版本说明页。
- `nav.xhtml` 是否使用短目录题名；页面标题是否有合理层级和可选副标题。
- 出版文本 lint 是否通过；是否还有分号滥用、异常空格、旧纸书页码目录或乱码。
- metadata 是否完整：`LifeBook 书坊 + 个人名`、译制时间、公版来源 URL、公版说明、作者信息、原书信息。
- 文件体积是否异常。
- EPUBCheck 是否 0 fatal、0 error。

## PASS 条件 / PASS Criteria

- Agent A 总分 >= 85。
- Agent B 总分 >= 85。
- 随机段落抽检已通过：Agent A/B 抽检平均分均 >= 75，且无单段 < 70。
- 任一 P0/P1 问题必须返工。
- 任一 Agent 明确指出严重问题时，主执行 AI 必须进入回退路由，不得忽略。
