# 弦表、角度与计算校验政策 / Chord, Angle, and Calculation Policy

本文件由 AI 在具体书籍工程中补全。

## 数值类型 / Numeric Types

- angle_degree
- angle_minute
- sexagesimal_value
- chord_length
- radius
- ratio
- arc
- table_entry
- astronomical_observation

## 校验规则 / Validation Rules

- 保留原文数值格式；不得默认十进制化。
- 若需现代换算，必须另列换算值，并标明算法和精度。
- 表格项必须可回查 source location。
- 数值有疑问时，记录原文、参考译本、现代计算和最终取舍。

## 抽样策略 / Sampling Strategy

- 小表：全量校验。
- 大表：先抽样校验表头、首行、末行、关键节点和异常值；发现漂移后扩大为全量校验。
- 证明中使用的数值：必须全量校验。

calculation_policy_status: `FAIL`

