# 35 异构成对评审 / Heterogeneous Pairwise Review

> 用于发布前评审、改写前后比较、候选版本比较、与金标准对比。评审模型家族 SHOULD 与译者不同；同一家族的多个 agent 只算一个视角。不给 0–100 分。
> For release review, before/after, candidates, or gold-standard comparison. Reviewer family SHOULD differ from the translator's. No 0–100 scores.

## 输入 / Inputs

- `{{SOURCE_TEXT}}`：原文（带段落编号） / source with IDs
- `{{VERSION_A}}` / `{{VERSION_B}}`：两个译本，调用方随机决定 A/B 顺序并在评审外记录映射 / two versions, order randomised by the caller, mapping kept outside the prompt
- `{{TARGET_CHAR_COUNT}}`：被评译本的目标语字符数 / target character count

## Prompt

```text
下面是同一段{{SOURCE_LANGUAGE}}原文的两个{{TARGET_LANGUAGE}}译本 A 和 B（顺序随机，来源不告诉你）。
请以一位{{TARGET_LANGUAGE}}文学编辑兼双语审校的眼光评审。

【原文】{{SOURCE_TEXT}}
【A】{{VERSION_A}}
【B】{{VERSION_B}}

一、逐错标注（A、B 分别列出）。每条一行：
版本 | 段落编号 | 类别 | 严重度 | 译文引文（逐字） | 原文引文（意义类必填） | 一句话说明
类别：accuracy（误译/漏译/增译/数字/否定/指代）、terminology、style（翻译腔/搭配/语域/节奏/标点）、fluency、notes。
严重度与权重：critical=10，major=5，minor=1。

二、按每千字计算：错误分 =（权重之和 ÷ 目标语字符数 × 1000）；另单列 style 类条数 ÷ 字符数 × 1000。

三、摘出 A、B 各自最好的 3 句和最差的 3 句（逐字引用，一句话说明）。摘不出最差的 3 句，说明没有认真读。

四、判断：哪一个更忠实？哪一个更像母语优秀译者写的？各引两三处决定性证据。两者都有严重问题时明确指出。

规则：每条判断都必须逐字引用；引不出原句的条目无效。不给 0–100 分。不问“有没有阻塞问题”，而问“哪里还不像母语作家写的”。

Pairwise review of A and B (random order). Annotate every error MQM-style with category, severity and verbatim quotes; compute per-1000-character error points and style density; quote best 3 and worst 3 sentences per version; decide which is more faithful and which reads more native, with quoted evidence. No 0–100 scores.
```

## 判定阈值 / Thresholds（调用方按脚本计算 / computed by script）

| 条件 Condition | 结果 Result |
|---|---|
| 任一 critical | FAIL |
| style 类 > 3 处 / 千字 / per 1000 chars | FAIL |
| 错误分 > {{ERROR_POINTS_LIMIT}} / 千字（建议 10） | FAIL |
| 改写版未在成对比较中胜出 / rewrite does not win | 不得替换原版 / do not replace |

## 有效性规则 / Validity rules

- 脚本校验每条引文确实存在于当前成书与原文；不存在的条目作废，作废过半则整轮无效。
  Script-verify every quote; if over half are invalid the run is void.
- 对 AI 初稿章节报告零问题的评审，必须由另一模型家族重跑；零问题本身不是放行证据。
  Zero issues on an AI-draft chapter must be re-run by a different model family.
- 记录 `reviewer_model_family`、A/B 映射和随机种子；评审者不得是该章译者或第 3 遍执行者。
  Record reviewer family, A/B mapping and seed; the reviewer must not be the chapter's translator or rewriter.
