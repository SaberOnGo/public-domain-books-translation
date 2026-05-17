# 06B 图表与表格清单 / Diagram and Table Inventory

## 输入 / Input

- `source/source_text.txt`
- `source/toc.json`
- `chapters/src/*.md`
- 原书 PDF、扫描图或图表来源文件
- `qa/technical/diagram_table_inventory.md`
- `qa/technical/verification_plan.md`
- `qa/technical/numeric_validation_log.md`
- `qa/technical/table_validation_log.md`
- `qa/technical/proof_dependency_map.md`
- `qa/technical/claim_traceability_matrix.csv`
- `references/units_symbols_policy.md`
- `references/figure_redraw_spec.md`
- `references/gpt_image_diagram_workflow.md`
- `references/technical_publication_control.md`

## 任务 / Tasks

生成或更新：

- `qa/technical/diagram_table_inventory.md`
- `qa/technical/verification_plan.md`
- `qa/technical/numeric_validation_log.md`
- `qa/technical/table_validation_log.md`
- `qa/technical/proof_dependency_map.md`
- `qa/technical/claim_traceability_matrix.csv`
- `qa/technical/chord_angle_calculation_policy.md`
- `qa/technical/diagram_redraw_workflow.md`

必须登记：

1. 全书图、几何图、天文模型图、表格、星表、数值表。
2. 图表在原书中的位置。
3. 图表在 EPUB 中的输出策略：保留、重绘、转结构化表格、加注说明。
4. 是否需要数值核验。
5. 是否需要 SVG、TikZ、HTML 表格或可访问替代文本。
6. 与章节翻译的依赖关系。
7. 涉及数值、角度、比例、单位、星表、弦表或日期时，写入 `qa/technical/numeric_validation_log.md`。
8. 涉及表格时，写入 `qa/technical/table_validation_log.md`。
9. 涉及定义、命题、证明、推论时，写入 `qa/technical/proof_dependency_map.md`。
10. 涉及关键技术断言时，写入 `qa/technical/claim_traceability_matrix.csv`。
11. 涉及弦表、角度、比例或计算时，写入 `qa/technical/chord_angle_calculation_policy.md`。
12. 涉及 GPT-Image-2 或其他 AI 重绘图时，写入 `qa/technical/diagram_redraw_workflow.md`。

## AI 图表规则 / AI Diagram Rules

- AI 可用于草拟重绘图，但不能跳过源图核对。
- 最终图必须核对标签、正文引用、数学关系和图注。
- 优先生成可维护的 SVG、TikZ 或结构化 HTML 表格；不要只生成不可复核的装饰性位图。

## PASS 条件 / PASS Criteria

- `inventory_status=PASS`
- `verification_plan_status=PASS`
- `numeric_validation_status=PASS` 或已创建并标出待逐章校验项
- `table_validation_status=PASS` 或已创建并标出待逐章校验项
- `proof_dependency_status=PASS` 或已创建并说明不适用
- `calculation_policy_status=PASS` 或已创建并说明不适用
- `diagram_redraw_workflow_status=PASS` 或已创建并说明不适用
- 高风险图表已有明确校验策略。
- 没有未登记的图表/表格进入生产阶段。
