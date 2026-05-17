# 参考译本使用政策 / Reference-Witness Policy

reference_policy_status: `PASS_FOR_RESEARCH_ONLY`

## 原文底本 / Primary Source

- 原书语言：古希腊文
- 主底本影像：Heiberg Greek edition PDF
- 来源 URL：https://commons.wikimedia.org/wiki/File:Almagest_Complete,_Heiberg.pdf
- 当前状态：Heiberg PDF 已下载和哈希；PAL Heiberg 古希腊文转写已作为辅助转写来源保存；正式全书 source split 尚未建立

## 三源分工 / PDF + PAL + English Roles

| 来源 | 本书角色 | 可用于 | 不可用于 |
|---|---|---|---|
| Heiberg PDF 扫描 | 主底本影像 | 页图、希腊正文核验、校勘/脚注区、图表、表格、几何标签、最终 facsimile 图来源 | 直接批量 OCR 后未经校验进入终稿 |
| PAL Heiberg 古希腊文转写 XML | 辅助古希腊文转写 | 检索、切分、试译 source text、PAL/Heiberg 页标、分词链和长周期句分析、OCR/转写疑点校正 | 跳过 PDF 页图核验；替代底本影像的最终判断 |
| 英译本 | reference witness only | 疑难理解、术语对照、数学/天文学解释线索、差异摘要 | 中文转译底稿、复制措辞/注释/图表/表格、单独修正希腊文底稿 |

## 参考译本 / Reference Translations

| 语言 | 译者/版本 | 来源 | 版权状态 | 允许用途 | 禁止用途 |
|---|---|---|---|---|---|
| English | G. J. Toomer, Princeton | publisher page / library copy | copyrighted | 疑难校读、术语对照、结构定位、技术理解 | 直接转译、复制措辞、复制注释、复制图表、复制表格 |
| English | R. Catesby Taliaferro, `Mathematical Composition (Almagest)` | HathiTrust record `001475750`, item `mdp.39015036048588` | public-domain candidate but HathiTrust API currently says `Limited (search-only)` | 若后续找到明确 full-view 公版文件，可下载哈希后作参考见证 | 在 full-view/rights 未确认前下载或提交全文 |
| Latin/Arabic/other historical witnesses | item-specific | Internet Archive or libraries | must verify | 比较术语传统、发现异文线索 | 未核版权或未核底本时作为底稿 |

## 硬规则 / Hard Rules

- 中文译文必须从古希腊文底本出发。
- Toomer 等现代英译只作 reference witness。
- 英译本不能作为 OCR/转写校正的最终依据；它只能提示需要回查 PDF/PAL 的疑点。
- 参考译本差异只写摘要和取舍，不复制长段表达。
- 参考译本和古希腊文冲突时，回到古希腊文底本、校勘记录和技术审计。
- 本轮未找到可合法下载进仓库的完整英译本；记录见 `research/references/english_reference_translation_search_2026-05-16.md`。

## Book I Pilot

Book I 预翻译时，可以使用参考译本帮助理解三角学、弦表和宇宙模型，但每个关键术语必须回查古希腊文原词。
