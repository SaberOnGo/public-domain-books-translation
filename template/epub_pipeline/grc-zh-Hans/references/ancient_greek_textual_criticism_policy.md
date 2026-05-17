# 古希腊文校勘与文本不确定性政策 / Ancient Greek Textual-Criticism Policy

## 目的 / Purpose

古希腊文公版书经常来自校勘本、扫描本、OCR、TEI/XML、网页转写或多版本汇编。翻译不能只记录“来源 URL”，还必须记录文本依据。

This policy requires explicit records for editions, witnesses, variant readings, conjectures, lacunae, uncertain OCR, and ambiguous grammar.

## 核心术语 / Core Terms

- `base_text`：本项目采用的主底本。
- `witness`：用于校读的文本见证，例如手稿、古本、校勘本、扫描、转写、参考译本。
- `lemma`：当前讨论的底本文字或词组。
- `reading`：某个 witness 给出的不同读法。
- `siglum`：校勘本给 witness 使用的简称或符号。
- `lacuna`：脱文、缺文、残损。
- `conjecture`：编辑者拟补或现代学者推测读法。
- `apparatus`：校勘记，记录读法差异和证据。

## 必须记录 / Required Records

在具体书籍工程中必须创建：

- `metadata/source_witness_manifest.md`
- `qa/textual/textual_uncertainty_log.md`

如果启用 `classical-science-zh-Hans` profile，还必须把影响术语、数值、图表或证明的异文同步到 profile 的技术审计记录中。

## 记录粒度 / Required Granularity

以下情况必须登记：

- 多个版本在同一句、同一术语、同一数字、同一图表标签上不同。
- OCR 或转写疑似错误，但尚未人工确认。
- 扫描页残损、模糊、缺页、错页、页序异常。
- 校勘本标注疑问、拟补、脱文、移位、删改。
- 语法结构可以支持两种以上合理解释。
- 第二语言参考译本和古希腊文底本解释不一致。

## 翻译规则 / Translation Rules

- 不得静默选择读法。疑难处必须记录位置、证据和最终取舍。
- 不得用第二语言译本覆盖古希腊文底本的歧义。
- 译文中需要保留不确定性时，应使用译注、括注或校读说明，不能把不确定句改成确定断言。
- 如果异文影响技术术语、数学证明、数字或图表，必须触发 profile 技术审计。

## PASS 条件 / PASS Criteria

- `metadata/source_witness_manifest.md` 已列出底本和相关 witness。
- `qa/textual/textual_uncertainty_log.md` 已记录所有已知不确定项，或明确说明本轮未发现。
- 所有 `UNRESOLVED` 项都有阻断范围；相关章节不得进入 `chapters/final/`。

