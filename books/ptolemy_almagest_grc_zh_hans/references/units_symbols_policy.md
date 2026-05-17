# 单位、符号与数值政策 / Units, Symbols, and Numbers Policy

## 目的 / Purpose

古典科学书常同时包含古代单位、角度、比例、天文常数、表格数值和现代编辑符号。翻译时必须分清原文数值、现代解释和译者注释。

## 基本规则 / Core Rules

- 不得为了中文顺口改写数值、单位、比例、角度或表格字段。
- 古代单位可保留原单位，并在译注或术语表说明；不要未经说明直接换成现代单位。
- 若需要现代换算，必须同时保留原值、换算值、换算依据和精度说明。
- 数学符号、变量、图表标签、单位符号必须进入 `qa/technical/equation_notation_registry.csv`。
- 数值校验必须进入 `qa/technical/numeric_validation_log.md`。

## 角度和天文数值 / Angles and Astronomical Values

- 度、分、秒、黄经、赤纬、弧、弦、半径、比例等必须稳定翻译。
- 六十进制数值不得被十进制化，除非明确加注说明。
- 星表、弦表、历法数值和观测值必须逐项校验或抽样说明校验策略。

## PASS 条件 / PASS Criteria

- 所有高风险单位和符号进入 registry。
- 所有高风险数值进入 numeric validation。
- 换算和现代解释没有混入正文冒充原文。

