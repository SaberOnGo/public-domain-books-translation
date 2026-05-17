---
name: classical-science-zh-Hans
description: Use this profile after a language-pair EPUB template when translating classical scientific, mathematical, astronomical, technical, diagram-heavy, or table-heavy public-domain works into Simplified Chinese.
---

# 古典科学简体中文 EPUB 控制流程 / Classical Science EPUB Control Workflow

## 何时使用 / When to Use

当一本公版书具有以下任一特征时，使用本 profile：

- 大量数学、天文、几何、科学或技术术语。
- 大量图表、表格、星表、数值、单位、比例或证明。
- 需要“原文底本 + 第二语言译本参考”共同校读。
- 一个术语翻错会影响后续多章理解。

Use this profile for classical scientific or technical works where terminology, diagrams, tables, proofs, and numerical consistency are publication blockers.

## 必须叠加的目录 / Required Overlay

具体书籍工程必须先由 `common` 和语言方向模板创建，再叠加本 profile。

```text
common -> {source-target} -> profiles/classical-science-zh-Hans -> books/{book_id_slug}/
```

## 执行步骤 / Workflow

在语言方向模板的主流程中，插入或强化以下阶段：

1. 先读取 `prompts/00_profile_integration_zh_Hans.md`，确认本 profile 如何插入语言方向模板。
2. 在本书专项研究后执行 `prompts/04a_reference_witness_policy_zh_Hans.md`。
3. 在术语表阶段执行 `prompts/06a_technical_terminology_lock_zh_Hans.md`。
4. 在批量翻译前执行 `prompts/06b_diagram_table_inventory_zh_Hans.md`。
5. 每章译后控制后执行 `prompts/08b_chapter_technical_audit_zh_Hans.md`。
6. 涉及图表/表格的章节执行 `prompts/08c_diagram_table_audit_zh_Hans.md`。
7. 最终独立评审时使用 `reviews/scorecards/_TEMPLATE_science_scorecard.md`。

## 通过标准 / Pass Standard

- 原文底本、参考译本、版权边界清晰。
- 术语表不是空模板，核心术语已冻结并有变更记录。
- 证明链、图表、表格、数值、单位和标签已经单独审计。
- 参考译本只留下差异记录和校读结论，不留下可替代原文的转译文本。
- EPUB 最终输出没有未解释的图表缺失、标签错配、数值漂移或术语漂移。

## 必要记录 / Required Records

- `qa/technical/reference_witness_diff_log.md`
- `qa/technical/terminology_change_log.md`
- `qa/technical/numeric_validation_log.md`
- `qa/technical/proof_dependency_map.md`
- `qa/technical/equation_notation_registry.csv`
- `qa/technical/table_validation_log.md`
- `qa/technical/claim_traceability_matrix.csv`
- `qa/technical/textual_variant_log.csv`
- `qa/technical/domain_authority_sources.md`
- `qa/technical/astronomical_model_registry.csv`
- `qa/technical/mathematical_term_lock.md`
- `qa/technical/chord_angle_calculation_policy.md`
- `qa/technical/diagram_redraw_workflow.md`
