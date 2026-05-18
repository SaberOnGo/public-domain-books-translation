# 模板版本 / Template Version

version: 1.2
updated_at: 2026-05-17

## 本次版本变化 / Changes

- 新增古希腊文到简体中文语言方向模板 `grc-zh-Hans`。
- 固化古希腊文底本、版本、编辑者、OCR/转写、异文和参考译本边界的工作流要求。
- 保留 00-19 EPUB 制作流程，并支持与 `profiles/classical-science-zh-Hans` 叠加。
- 语言方向模板只处理古希腊文源语言问题；数学、天文学、图表、表格和技术审计由 profile 处理。
- 补强 source witness、文本校勘、参考译本、专名转写、标题策略和古希腊文评审评分表。
- 新增 `metadata/source_witness_manifest.md` 与 `qa/textual/textual_uncertainty_log.md` 模板。
- 预制作、样章、全书制作和最终输出 prompts 接入 EPUB 图表/图片/表格资源规则：Markdown 必须转 XHTML，SVG/PNG/CSS 等必须登记 OPF manifest，并运行 asset manifest 检查。
- 接入 EPUB 后分层随机抽检门禁：第一版全书 EPUB 后自动抽样正文段落、表格、图片、公式/证明块、图注和注释，保留轮次目录、seed、证据、Agent 评审、修复记录和闭环验证；最终输出前必须通过 `npm run review:random-validate:pass`。
