# 06A 技术术语锁定 / Technical Terminology Lock

## 输入 / Input

- `metadata/book_specific_translation_research.md`
- `metadata/reference_witness_policy.md`
- `qa/pretranslation/pretranslation_report.md`
- `glossary/terms.csv`
- `glossary/technical_terms.csv`
- `glossary/technical_style_guide.md`
- `qa/technical/equation_notation_registry.csv`
- `qa/technical/domain_authority_sources.md`
- `qa/technical/astronomical_model_registry.csv`
- `qa/technical/mathematical_term_lock.md`
- `chapters/src/*.md`

## 任务 / Tasks

生成或更新：

- `glossary/technical_terms.csv`
- `glossary/technical_style_guide.md`
- `qa/technical/terminology_lock_report.md`
- `qa/technical/terminology_change_log.md`
- `qa/technical/equation_notation_registry.csv`
- `qa/technical/domain_authority_sources.md`
- `qa/technical/astronomical_model_registry.csv`
- `qa/technical/mathematical_term_lock.md`

必须覆盖以下术语类型：

- 天文学术语。
- 数学和几何术语。
- 证明动作词和逻辑关系词。
- 图表标签、表格字段、单位、角度、时间和数值表达。
- 仪器、模型、星座、天体、古代地名和人名。
- 文本异文、版本术语、参考译本差异术语。
- 变量、符号、缩写、单位符号、图形字母和表格字段。
- 天文学模型术语：本轮、均轮、偏心圆、等分点、黄道、赤道、黄经、赤纬。
- 数学证明动作词：设、作、连结、延长、交于、相等、相似、成比例、由此可得。

## 锁定规则 / Lock Rules

- 每个核心术语必须有 `locked_status`：`LOCKED`、`PROVISIONAL` 或 `REJECTED`。
- `LOCKED` 术语不得在章节翻译中随意变化。
- `PROVISIONAL` 术语必须记录未锁定原因和下一次复核位置。
- 术语变更必须记录影响范围，不能只改当前章节。
- 已锁定术语的任何变更必须写入 `qa/technical/terminology_change_log.md`，并触发影响章节复查。
- 术语锁定必须引用 `qa/technical/domain_authority_sources.md` 中的权威来源，或说明没有可用权威来源。
- 符号、变量、单位和图表标签必须进入 `qa/technical/equation_notation_registry.csv`。
- 天文学模型术语必须进入 `qa/technical/astronomical_model_registry.csv`。
- 数学证明动作词必须进入 `qa/technical/mathematical_term_lock.md`。

## 输出 / Output

- `glossary/technical_terms.csv`
- `glossary/technical_style_guide.md`
- `qa/technical/terminology_lock_report.md`
- `qa/technical/terminology_change_log.md`
- `qa/technical/equation_notation_registry.csv`
- `qa/technical/domain_authority_sources.md`
- `qa/technical/astronomical_model_registry.csv`
- `qa/technical/mathematical_term_lock.md`

## PASS 条件 / PASS Criteria

- 核心术语不是空模板。
- 高风险术语全部至少为 `PROVISIONAL`。
- 批量分章翻译前，关键模型、证明、图表和单位术语必须 `LOCKED`。
- `terminology_lock_status=PASS`
- `terminology_change_log_status=PASS` 或已创建并说明暂无变更
- `domain_authority_sources_status=PASS`
