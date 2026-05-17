# 04A 参考译本与校读证据政策 / Reference-Witness Policy

## 输入 / Input

- `metadata/rights_checklist.md`
- `metadata/book_specific_translation_research.md`
- `metadata/reference_witness_policy.md`
- 原书语言公版来源
- 第二语言参考译本来源列表；没有则记录 `NONE`

## 任务 / Tasks

生成或更新 `metadata/reference_witness_policy.md`，必须包含：

1. 原书语言底本信息、来源 URL、版本、编辑者、OCR/转写状态、公版证据。
2. 每个第二语言参考译本的语言、译者/版本、来源、版权状态。
3. 每个参考译本的允许用途和禁止用途。
4. 明确写入：参考译本只能用于理解、差异校对和技术核验，不能直接转译。
5. 如果参考译本仍受版权保护，明确禁止复制其措辞、注释、图表、表格、版式和编辑结构。
6. 原文和参考译本冲突时的记录方式。
7. 若项目同时使用扫描 PDF、原文转写/OCR 和参考译本，必须明确三者分工：扫描或校勘本影像是最终核验依据；原文转写/OCR 是可检索和切分控制；参考译本只能提示疑点，不能替代原文证据。

同时生成或更新 `qa/technical/reference_witness_diff_log.md`，用于后续逐章记录参考译本差异。

## 硬规则 / Hard Rules

- 原书语言公版来源不清楚，`reference_policy_status=FAIL`，停止。
- 参考译本版权状态不清楚，不得使用该参考译本。
- 不得把参考译本当作隐藏底本。
- 不得把参考译本当作 OCR/转写修正的最终依据。

## 输出 / Output

- `metadata/reference_witness_policy.md`
- `qa/technical/reference_witness_diff_log.md`

## PASS 条件 / PASS Criteria

- `reference_policy_status=PASS`
- `diff_log_status=PASS` 或已创建并说明暂无差异记录
- 原文底本和参考译本边界清楚。
- 没有版权状态不明的参考材料进入工作流。
