# 《Almagest》技术校验计划 / Technical Verification Plan

verification_plan_status: `PASS_FOR_PRETRANSLATION_PLANNING_ONLY`

## 校验范围 / Scope

- 术语一致性：本轮、均轮、偏心圆、等分点、弦、角度、黄道、赤道。
- 领域权威来源：中国天文学名词、IAU、BIPM/SI、TEI critical apparatus 等。
- 数学证明：定义、命题、证明、推论、证明依赖。
- 天文模型：地心几何模型、圆和点的角色、均匀运动假设。
- 数值与单位：弦表、角度、六十进制、比例、表格字段。
- 图表与标签：原图、重绘图、图注、正文引用、替代文本。
- 古今概念边界：正文呈现古代模型，现代解释进入注释。
- 参考译本差异：只作 reference witness。

## 章节风险分级 / Chapter Risk Levels

| chapter | risk_level | reason | required_audits |
|---|---|---|---|
| Book I | HIGH | foundational geometry, cosmology, chord/angle terms, possible diagrams | terminology/technical/diagram/table/numeric/proof/notation/variant/claim_traceability |
| Books II-XIII | HIGH | later model terms, tables, planetary theory, star catalogue | not in current scope |

## 工具与人工校对 / Tools and Human Review

- 可自动检查：术语漂移、表格字段、图表标签、重复数值、文件引用。
- 必须人工或专家检查：数学证明链、天文学模型解释、古今概念边界。
- 可以由 AI 初审但必须复核：图表重绘、参考译本差异、译注解释。

## 当前边界

当前只完成预翻译计划。正式翻译前必须将 Book I 的 source text、figure/table inventory、proof dependency map 和 pretranslation trials 补齐并 PASS。

