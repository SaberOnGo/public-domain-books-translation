# 00 Profile 插入规则 / Profile Integration Rules

## 目的 / Purpose

本文件说明 `classical-science-zh-Hans` 如何叠加到任意语言方向模板上。

This profile adds technical production controls to a language-pair EPUB pipeline. It does not replace the language-pair prompts.

## 插入点 / Insertion Points

| 语言方向阶段 | 本 profile 追加阶段 | 必须产物 |
|---|---|---|
| `04_book_specific_research` 后 | `04a_reference_witness_policy` | `metadata/reference_witness_policy.md`, `qa/technical/reference_witness_diff_log.md` |
| `06_glossary_style` 后 | `06a_technical_terminology_lock` | `glossary/technical_terms.csv`, `qa/technical/terminology_lock_report.md`, `qa/technical/terminology_change_log.md`, `qa/technical/equation_notation_registry.csv`, `qa/technical/domain_authority_sources.md` |
| 批量翻译前 | `06b_diagram_table_inventory` | `qa/technical/diagram_table_inventory.md`, `qa/technical/verification_plan.md`, `qa/technical/numeric_validation_log.md`, `qa/technical/table_validation_log.md`, `qa/technical/proof_dependency_map.md`, `qa/technical/claim_traceability_matrix.csv` |
| 每章 `08a_chapter_post_translation_control` 后 | `08b_chapter_technical_audit` | `qa/technical/{NNN_slug}.technical_audit.md` |
| 涉及图表/表格的章节 | `08c_diagram_table_audit` | `qa/technical/{NNN_slug}.diagram_table_audit.md` |
| 第一版全书 EPUB 后 | `16a_stratified_random_spotcheck` with science profile | `reviews/random_spotcheck/round_XXX/` |
| 最终独立评审 | science scorecard | `reviews/scorecards/final_science_score.md` |

## 状态规则 / State Rules

- profile 阶段不替换语言方向模板的 `status`，但必须在对应 QA 文件中写入 `PASS/FAIL`。
- 任一 profile 文件为 `FAIL` 时，语言方向模板不得继续进入下一硬门禁。
- 如果语言审校和技术审校冲突，先修技术正确性，再修中文表达。
- 第一版全书 EPUB 后分层随机抽检必须覆盖实际存在的表格、图片、公式/证明块、图注和注释；不得只用普通正文段落抽检替代。

## 适用边界 / Boundary

- 原文语言问题仍由 `{source-target}` 语言模板处理。
- 目标中文质量仍由 `targets/zh-Hans` 处理。
- 本 profile 只处理古典科学/数学/天文学/图表/表格/数值/技术证明的生产风险。

## 必读 profile references / Required Profile References

- `references/technical_publication_control.md`
- `references/units_symbols_policy.md`
- `references/figure_redraw_spec.md`
- `references/gpt_image_diagram_workflow.md`
- `references/math_astronomy_proof_control.md`
- `references/domain_authority_sources.md`
- 相关领域文件：`references/domains/*.md`
