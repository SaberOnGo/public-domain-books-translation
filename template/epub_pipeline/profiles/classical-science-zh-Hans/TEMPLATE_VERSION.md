# 模板版本 / Template Version

version: 1.2
updated_at: 2026-05-17

## 本次版本变化 / Changes

- 新增古典科学、数学、天文学、技术类公版书的第三层控制 profile。
- 固化“原书语言为底本，第二语言译本只作参考证据”的工作流边界。
- 新增术语锁定、图表/表格清单、章节技术审计、图表/表格审计和科学评审评分表。
- 支持未来与 `Ancient-Greek-to-Simplified-Chinese`、`Latin-to-Simplified-Chinese`、`Arabic-to-Simplified-Chinese`、`English-to-Simplified-Chinese` 等语言方向模板叠加使用。
- 补强单位/符号、图表重绘、证明依赖、表格校验、关键断言追溯、技术异文和领域权威来源记录。
- 新增天文学、数学、地理学、光学/力学、医学分领域规则。
- 补强数学/天文学专门强约束：模型注册、证明动作词锁定、弦表/角度校验、GPT-Image-2 图表草稿与结构化重绘工作流。
- 补强 EPUB 图表资源落地规则：最终图表进入 `assets/`，技术表格优先 XHTML table，图表审计必须覆盖 OPF manifest、alt/figcaption 和 asset manifest 检查。
- 接入 common 公式渲染策略：稳定显示公式优先 XHTML 内嵌 MathML，复杂/OCR 损坏公式用 SVG 或源图像兜底，行内公式不裁图，并要求全书公式清单。
