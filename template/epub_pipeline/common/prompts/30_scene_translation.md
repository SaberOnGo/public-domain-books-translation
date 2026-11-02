# 30 场景翻译（初译） / Scene Translation (First Draft)

> 第 1 遍。调用方只填下列占位符；不得追加流程、门禁、记录或发布规则。
> Pass 1. The caller fills only the placeholders below; never append process, gate, record or release rules.

## 输入 / Inputs

| 占位符 Placeholder | 内容 Content |
|---|---|
| `{{TRANSLATOR_BRIEF}}` | 本书译者手册全文（≤3000 字） / full brief |
| `{{PREVIOUS_SUMMARY}}` | 本章到此为止的情节或论证摘要，≤150 字 / chapter-so-far summary |
| `{{PREVIOUS_TARGET_TAIL}}` | 上一段译文的最后两句 / last two target sentences |
| `{{MATCHED_TERMS}}` | 只列本段命中的术语与专名行 / only matched glossary rows |
| `{{SOURCE_SCENE}}` | 800–2000 字（或等量源语词数）完整段落，带段落编号 / complete paragraphs with IDs |

## Prompt

```text
你是一位资深文学译者，正在把一本书从{{SOURCE_LANGUAGE}}译成{{TARGET_LANGUAGE}}。
这一次只做一件事：把下面的原文译成{{TARGET_LANGUAGE}}。

【本书译者手册】
{{TRANSLATOR_BRIEF}}

【前情】
{{PREVIOUS_SUMMARY}}
上一段译文结尾：{{PREVIOUS_TARGET_TAIL}}

【本段命中的术语与专名】
{{MATCHED_TERMS}}

【原文】
{{SOURCE_SCENE}}

要求：
1. 按原文段落编号逐段输出译文，一段原文对应一段译文；不输出任何解释、注记或自评。
2. 段落内可以调整语序、合句、拆句、调换信息顺序；不得跨段移动信息。
3. 不得增加原文没有的信息、逻辑、比喻或情绪；不得删减任何信息。
4. 声音、称谓、节奏、标点按译者手册；专名与术语严格按命中清单。
5. 遇到确实无法确定的地方，照常译出，并在该段末尾另起一行写“[疑：一句话说明]”。
6. 目标是让{{TARGET_LANGUAGE}}读者感觉这是一位母语作家写成的书。

You are a senior literary translator. Translate the source into {{TARGET_LANGUAGE}} paragraph by paragraph (same IDs). Output translation only. Restructure freely within a paragraph; never add or delete information; follow the brief and matched terms; flag genuine uncertainty with one "[疑: ...]" line.
```

## 调用方须知 / Caller notes

- 单次原文不足 800 字时，与相邻完整段落合并；超过 2000 字时，在场景或论证转折处切开，绝不在段落中间切。
  Merge short inputs with neighbouring paragraphs; split long ones only at scene or argument boundaries, never mid-paragraph.
- 对齐与双语切分在译后做，以原书自然段为单位；单语版保持原段落。
  Alignment is done after translation, by source paragraph; the monolingual edition keeps original paragraphs.
- “[疑]”行由第 2 遍（`31_source_fidelity_pass.md`）处理后删除，不得进入成书。
  `[疑]` lines are resolved in pass 2 and must never reach the book.
