# 模板版本 / Template Version

version: grc-zh-Hans 1.2 + classical-science-zh-Hans 1.2
updated_at: 2026-05-17

## 本次版本变化 / Changes

- 新增古典科学、数学、天文学、技术类公版书的第三层控制 profile。
- 固化“原书语言为底本，第二语言译本只作参考证据”的工作流边界。
- 新增术语锁定、图表/表格清单、章节技术审计、图表/表格审计和科学评审评分表。
- 支持未来与 `grc-zh-Hans`、`la-zh-Hans`、`ar-zh-Hans`、`en-zh-Hans` 等语言方向模板叠加使用。
- 补强单位/符号、图表重绘、证明依赖、表格校验、关键断言追溯、技术异文和领域权威来源记录。
- 新增天文学、数学、地理学、光学/力学、医学分领域规则。
- 补强数学/天文学专门强约束：模型注册、证明动作词锁定、弦表/角度校验、GPT-Image-2 图表草稿与结构化重绘工作流。
- 已同步 EPUB 图表资源落地规则：`assets/`、`source/tables/`、`asset_manifest_check.js`、预制作模板和 grc 生产 prompts 均要求 Markdown 转 XHTML、资源进入 OPF manifest、技术表格优先 XHTML table。
