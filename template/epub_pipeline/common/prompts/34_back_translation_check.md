# 34 回译抽查 / Back-Translation Check

> 第 5 遍。只用于重写幅度大的段落：第 3 遍中长度增长超过阈值、改动过半、或冷读后重写过的段落；另加每章随机 {{RANDOM_SAMPLE_COUNT}} 段（建议 2 段）。
> Pass 5. Only for heavily rewritten paragraphs (length growth over threshold, >50% changed, or rewritten after cold read), plus a few random paragraphs per chapter.

## 步骤 / Steps

1. **回译调用**：只给目标语段落，不给原文。 / Back-translate with target only, no source.
2. **比对调用**：给原文、回译、当前译文，找意义漂移。 / Compare source, back-translation and current target.

两步 SHOULD 使用不同上下文；回译者不得是第 3 遍的执行者。
Use separate contexts; the back-translator must not be the pass-3 rewriter.

## Prompt A：回译 / Back-translate

```text
把下面的{{TARGET_LANGUAGE}}段落尽量直白地译成{{SOURCE_LANGUAGE}}。保留每一个信息点、逻辑连接词、语气和修辞；不要润色，不要解释。
按段落编号输出。

{{REWRITTEN_PARAGRAPHS}}
```

## Prompt B：比对 / Compare

```text
下面每个段落编号都有三样东西：原文、当前译文、当前译文的回译。
请只判断当前译文相对原文有没有意义漂移。

{{SOURCE_PARAGRAPHS}}
{{REWRITTEN_PARAGRAPHS}}
{{BACK_TRANSLATIONS}}

漂移类型：added-logic 补出的因果或解释 / added-image 多出的比喻或意象 / added-emotion 多出的情绪或评价 / lost-info 丢失的信息 / shifted-meaning 意思改变 / shifted-tone 语气或立场改变。

每条一行：段落编号 | 类型 | 原文引文 | 译文引文 | 一句话说明
回译措辞与原文不同、但意思一致的，不算漂移。没有漂移的段落写“无漂移”。

For each paragraph, compare source, current target and its back-translation; list only meaning drift in the six types, quoting source and target. Wording differences with identical meaning are not drift.
```

## 调用方须知 / Caller notes

- 有漂移的段落退回第 3 遍前的版本或按原文重写该句，然后对该段及前后各一段重跑第 2 遍。
  Revert or rewrite drifting sentences, then re-run pass 2 on that paragraph and one neighbour on each side.
- 保存三栏比对结果作为 08a 证据。 / Store the three-way result as 08a evidence.
