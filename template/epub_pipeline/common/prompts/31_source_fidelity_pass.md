# 31 对读（源文忠实度） / Source Fidelity Pass

> 第 2 遍。逐段对照原文，只找意义错误，不改风格。
> Pass 2. Paragraph-by-paragraph against the source; meaning errors only, no style edits.

## 输入 / Inputs

- `{{SOURCE_SCENE}}`：原文（带段落编号） / source with paragraph IDs
- `{{TARGET_SCENE}}`：第 1 遍译文（同编号） / pass-1 target, same IDs
- `{{MATCHED_TERMS}}`：本段命中的术语与专名 / matched glossary rows
- `{{FALSE_FRIENDS_AND_IDIOMS}}`：译者手册第 7、8 节 / brief sections 7–8

不提供译者手册其余部分，也不提供流程规则。 / No other brief sections, no process rules.

## Prompt

```text
你是一位{{SOURCE_LANGUAGE}}与{{TARGET_LANGUAGE}}都精通的审校。请逐段对照原文和译文，只找意义层面的错误。

【原文】{{SOURCE_SCENE}}
【译文】{{TARGET_SCENE}}
【术语与专名】{{MATCHED_TERMS}}
【本书假朋友、旧义项、习语与构式】{{FALSE_FRIENDS_AND_IDIOMS}}

错误类型只限以下八种：
- omission 漏译
- addition 增译（原文没有的信息、逻辑、情绪、解释）
- mistranslation 误译
- number 数字、日期、单位、货币
- negation 否定或肯定方向
- reference 指代、主语、说话人归属
- false-friend 假朋友或旧义项
- idiom 习语、构式按字面误解

输出格式，每条一项：
段落编号 | 类型 | 严重度(critical/major/minor) | 原文引文 | 译文引文 | 正确意思（一句话）

规则：
1. 每条必须同时逐字引用原文和译文；引不出来的不算。
2. 不评价文风，不重写句子，不给分数。语序调整、合句拆句只要意义不变，就不算错误。
3. 同时处理译文中的“[疑]”行：给出判定，并按上述格式列入或注明“无误”。
4. 如果没有发现任何错误，写“没有”，并列出你核对过的三处最容易出错的位置及核对结论。

Bilingual reviewer: list meaning errors only, in the eight types above, each quoting BOTH source and target verbatim. No style comments, no rewrites, no scores. Resolve every [疑] line. If none found, write "没有" and show three hardest spots you checked.
```

## 调用方须知 / Caller notes

- 修复时只改被列出的段落，然后对改动段及前后各一段重跑本遍。
  Fix only listed paragraphs, then re-run this pass on changed paragraphs plus one neighbour on each side.
- 本遍输出是 08a 的忠实度证据，原样保存，不得事后编辑。
  The output is 08a fidelity evidence; store it verbatim and never edit it afterwards.
