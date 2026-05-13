# 16 双 Agent 独立评审 / Independent Two-Agent Review

## 目的 / Purpose

全书 EPUB 制作后，主执行 AI 不得直接宣布完成。必须派生 2 个独立评审 Agent，从不同角度审查成书质量，避免主执行者自证通过。

## 强制要求 / Mandatory Requirement

AI 必须派生两个评审 Agent：

- Agent A：内容与翻译质量评审。
- Agent B：EPUB 工程、排版、metadata、封面与可读性评审。

两个 Agent 必须独立阅读模板要求、产物和评分表，不得互相参考，不得只复述主执行 AI 的结论。

## 输入 / Input

- `output/book.epub`
- `output/publication_lint.json`
- `output/epubcheck.json` 或 `output/epubcheck.log`
- `preproduction/stage1/production_spec.md`
- `preproduction/stage2_sample/sample_review.md`
- `qa/gates/*.gate.md`
- `qa/chapter_controls/*.control.md`
- `reviews/scorecards/_TEMPLATE_scorecard.md`

## 输出 / Output

- `reviews/agent_a/review.md`
- `reviews/agent_b/review.md`
- `reviews/scorecards/final_quality_score.md`

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
- metadata 是否完整：`LifeBook 书坊`、译制时间、公版来源 URL、公版说明、作者信息、原书信息。
- 文件体积是否异常。
- EPUBCheck 是否 0 fatal、0 error。

## PASS 条件 / PASS Criteria

- Agent A 总分 >= 85。
- Agent B 总分 >= 85。
- 任一 P0/P1 问题必须返工。
- 任一 Agent 明确指出严重问题时，主执行 AI 必须进入回退路由，不得忽略。
