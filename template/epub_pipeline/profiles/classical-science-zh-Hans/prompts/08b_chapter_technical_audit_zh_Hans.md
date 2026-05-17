# 08B 章节技术审计 / Chapter Technical Audit

## 输入 / Input

- `chapters/src/{NNN_slug}.md`
- `chapters/translated/{NNN_slug}.md`
- `metadata/reference_witness_policy.md`
- `glossary/technical_terms.csv`
- `glossary/technical_style_guide.md`
- `qa/technical/verification_plan.md`
- `qa/technical/reference_witness_diff_log.md`
- `qa/technical/numeric_validation_log.md`
- `qa/technical/proof_dependency_map.md`
- `qa/technical/equation_notation_registry.csv`
- `qa/technical/claim_traceability_matrix.csv`
- `qa/technical/textual_variant_log.csv`
- `qa/technical/_TEMPLATE.chapter_technical_audit.md`

## 任务 / Tasks

每个章节译后控制完成后，创建：

- `qa/technical/{NNN_slug}.technical_audit.md`

必须检查：

1. 核心术语是否与术语表一致。
2. 数学、几何、证明关系是否完整。
3. 天文学模型、对象关系、运动关系是否准确。
4. 数值、角度、单位、表格字段是否漂移。
5. 原文难句是否确实从原书语言翻译，而不是被参考译本牵引。
6. 若参考译本与原文不同，是否记录差异和取舍。
7. 涉及数值、角度、比例、单位、星表、弦表或日期时，是否更新数值校验记录。
8. 涉及定义、命题、证明、推论时，是否更新证明依赖图。
9. 涉及符号、变量、图表标签或表格字段时，是否和 notation registry 一致。
10. 关键技术断言是否能追溯到原文、术语、图表、表格或审计记录。

## 回退规则 / Rework Rules

- 技术审计 `FAIL` 时，只能回到本章翻译、术语锁定或图表清单相关步骤修正。
- 不得用“中文顺畅”掩盖技术错误。
- 如果发现术语表本身错误，必须回到 `06A` 修订术语表并检查影响章节。

## PASS 条件 / PASS Criteria

- `technical_audit_status=PASS`
- 无未解释的术语漂移、数值漂移、证明断裂或参考译本误导。
