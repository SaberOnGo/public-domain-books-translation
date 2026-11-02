# 33 冷读 / Cold Read

> 第 4 遍。全新上下文、只看目标语、扮演目标读者。不提供原文、译者手册、前几遍记录或任何规则。模型家族 SHOULD 与译者不同。
> Pass 4. Fresh context, target text only, acting as the target reader. No source, brief, earlier pass records or rules. Model family SHOULD differ from the translator's.

## 输入 / Inputs

- `{{TARGET_CHAPTER}}`：第 3 遍后的整章（或 ≥3000 字连续正文），带段落编号 / full chapter after pass 3, with IDs
- `{{READER_PROFILE}}`：一句话读者画像（取自译者手册第 1 节） / one-line reader profile

## Prompt

```text
你是第一次读这本书的普通{{TARGET_LANGUAGE}}读者：{{READER_PROFILE}}。
请从头读完下面这一章。

【正文】
{{TARGET_CHAPTER}}

凡是让你停顿、皱眉、需要回读、觉得“母语作者不会这样写”的句子，原样摘出来，每条一行：
段落编号 | 原句（逐字） | 你的感受（一句话，例如“读到这里不知道‘他’是谁”）

规则：
1. 不打分，不总结优点，不提修改建议，不猜原文。
2. 只写你作为读者的真实反应，不套用任何规则术语。
3. 如果整章没有任何这样的句子，请明确写“没有”，并用三到五句话解释为什么你认为它读起来像原创作品，同时摘出你认为写得最好的两句。

You are an ordinary first-time {{TARGET_LANGUAGE}} reader. Quote verbatim every sentence that made you pause, frown, re-read or feel "a native writer would not say this", with a one-line feeling. No scores, no praise summary, no fixes. If none, write "没有" and justify it, quoting the two best sentences.
```

## 调用方须知 / Caller notes

- 冷读条目交给第 3 遍的执行者按句型重写（只改被摘句、前后句和同族句），不得只换词。
  Route items to a pattern-level rewrite of the quoted sentence, its neighbours and same-pattern sentences; no word swaps.
- 一章 AI 初稿冷读结果为“没有”时，必须换一个模型家族重跑一次冷读。
  A "没有" on an AI-draft chapter requires a re-run by a different model family.
- 记录 `reader_model_family`；本遍输出是 08a 的冷读证据。
  Record the reader's model family; output is 08a cold-read evidence.
