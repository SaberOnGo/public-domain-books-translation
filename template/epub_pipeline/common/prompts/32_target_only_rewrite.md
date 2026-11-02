# 32 脱稿重写（只看目标语） / Target-Only Rewrite

> 第 3 遍。看不到原文，只按译者手册把译稿改成地道的目标语。之后必须做长度比检查与回译抽查（`34_back_translation_check.md`）。
> Pass 3. No source. Rewrite against the brief. Must be followed by a length-ratio check and back-translation spot check.

## 输入 / Inputs

- `{{TARGET_SCENE}}`：第 2 遍修正后的译文（带段落编号） / pass-2-corrected target with IDs
- `{{RHYTHM_AND_DEFECTS}}`：译者手册第 2、3、11 节 / brief sections 2, 3, 11
- `{{LOCKED_TERMS}}`：本段专名与术语（不得改动） / locked names and terms

## Prompt

```text
下面是一段{{TARGET_LANGUAGE}}译稿。你看不到原文，也不需要看。
请像一位{{TARGET_LANGUAGE}}文学编辑那样，把读起来像翻译的地方改写成地道的{{TARGET_LANGUAGE}}，其余保持不动。

【本书声音、目标节奏与易犯毛病】
{{RHYTHM_AND_DEFECTS}}

【不得改动的专名与术语】
{{LOCKED_TERMS}}

【译稿】
{{TARGET_SCENE}}

重点：
- 本书易犯毛病清单里的句型（按句型找，不按字串找）；
- 可省略的代词、量词、物主词、“某种”类虚词；
- 源语从句骨架、名词堆叠、介词结构开头；
- 句长与长短交替是否符合目标节奏；分号、冒号、破折号是否符合保留条件。

禁止：
- 补出原文可能没有的隐含逻辑、因果、解释、比喻、情绪；
- 删除任何信息；改动专名、术语、数字；
- 跨段移动信息；为改而改。

输出：
1. 重写后的全文，保持原段落编号；
2. 修改清单，每处一行：段落编号 | 原句 → 新句 | 句型或理由（一句话）。
没有修改的段落不列出。

Act as a native {{TARGET_LANGUAGE}} literary editor without the source. Rewrite only what reads as translation, guided by the brief's rhythm and defect patterns. Never add implicit logic, metaphors or emotions; never delete information or touch locked terms. Output full text (same IDs) plus a change list.
```

## 调用方须知 / Caller notes

- 逐段计算新旧长度比；增长超过 {{LENGTH_GROWTH_LIMIT}}（建议 15%）或改动过半的段落，必须进入 `34_back_translation_check.md`。
  Compute per-paragraph length ratio; growth above the limit (suggested 15%) or >50% rewritten goes to back-translation.
- 修改清单是 08a 的可读性证据，原样保存。
  The change list is 08a readability evidence; store verbatim.
