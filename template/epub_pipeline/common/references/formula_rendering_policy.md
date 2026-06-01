# 公式渲染与 EPUB 输出策略 / Formula Rendering Policy

## 适用范围 / Scope

本规则用于任何含有公式、模型、统计表达式、方程组、证明、技术符号或表格内统计符号的 EPUB 项目。它是 `common/references/epub_assets_figures_tables.md` 的补充规则；相关 profile 只负责声明何时必须启用本规则，不应各自维护重复副本。

This policy applies to EPUB projects that contain formulas, models, statistical expressions, equation groups, proofs, technical notation, or statistical symbols inside tables.

## 核心原则 / Core Principle

公式处理不得默认走“全部手工裁图”。先建立全书公式清单并分类，再为每一类选择 XHTML 文本、Presentation MathML、SVG 或源图像兜底。目标是同时满足原书忠实性、EPUB 可访问性、可缩放性、可重排性和 EPUBCheck 可通过性。

Do not default to cropping every formula. Build a book-wide formula inventory first, classify each formula, and then choose XHTML text, Presentation MathML, SVG, or source-image fallback according to risk.

## 分类与处理策略 / Classification and Strategy

| 类型 | 首选处理 | 兜底处理 | 说明 |
|---|---|---|---|
| 行内短公式、变量、上下标、简单等式 | XHTML 文本、`sub`/`sup` 或行内 MathML | 不裁图 | 正文不应被切碎成大量图片。 |
| 稳定可识别的独立显示公式 | XHTML 内嵌 Presentation MathML | SVG 或高清 PNG | MathML 更适合 EPUB：可缩放、可访问、可重排。 |
| 多行公式、方程组、推导块 | 按完整公式块输出 MathML 或 SVG | 源 PDF/扫描页渲染为高清 PNG | 不得按单行孤立裁剪；必须避免漏行、截断括号或切断上下文。 |
| OCR 已明显错乱的复杂公式 | 源 PDF/扫描页渲染为 SVG 或高清 PNG | 手工校对后 MathML | 复杂矩阵、长方程组、特殊符号、偏导矩阵、连分式等应优先保真。 |
| 表格内统计符号、变量名、系数标签 | 保留原表含义和原书标签 | 必要时加术语表或译注 | 不得把生产说明、读表教程、统计标签对照等塞进表注或图注。 |

## 全书公式清单 / Book-Wide Formula Inventory

正式修复或输出 EPUB 前，必须建立 `qa/technical/formula_strategy_audit.md` 或等效记录，至少包括：

- 章节文件和行号，或源 PDF 页码与区域。
- 公式类型：`inline_formula_text`、`display_mathml`、`multi_line_formula_block`、`table_stat_symbol`、`ocr_broken_formula`、`image_fallback`。
- 处理策略：XHTML 文本、Presentation MathML、SVG、源 PDF/扫描页 PNG。
- 如果使用图像兜底，记录源页码、裁剪区域、生成文件、`alt`/`figcaption` 和非空检查结果。
- 如果使用 MathML，记录 EPUBCheck 结果，并确认 OPF manifest 中对应 XHTML item 有 `properties="mathml"`。

## MathML 输出要求 / MathML Requirements

- 稳定可识别的显示公式优先输出 XHTML 内嵌 Presentation MathML。
- MathML 必须放在 EPUB XHTML 中，使用 `xmlns="http://www.w3.org/1998/Math/MathML"`。
- 含 MathML 的 XHTML manifest item 必须声明 `properties="mathml"`。
- 生成 EPUB 后必须运行 EPUBCheck；任何 MathML 相关 OPF、命名空间或结构错误都必须修复。
- 不得把不确定、OCR 已损坏或无法校对的复杂公式硬转成 MathML。

## 图像兜底要求 / Image Fallback Requirements

- 复杂公式、方程组、推导块或 OCR 已损坏公式可使用源 PDF/扫描页渲染的 SVG 或高清 PNG。
- 图像兜底必须保留原书公式排版，不得重新解释或扩写公式。
- 多行公式必须按完整公式块裁剪，不得逐行裁剪后让读者自行拼接。
- 每个公式图像必须有简短、忠实的 `alt` 和 `figcaption`，例如“公式：命题二条件二”；不得加入额外读者教程或生产说明。
- 公式图像必须进入 EPUB 包内相对路径，并登记到 OPF manifest；不得引用本机绝对路径、`file://` 或在线图片。
- 公式图像必须做非空、非截断检查，必要时人工抽看。

## 禁止事项 / Forbidden

- 禁止把全书公式一律手工裁图，导致行内公式碎片化、不可重排或难以访问。
- 禁止把复杂公式 OCR 错误文本直接排入 EPUB。
- 禁止把生产过程说明、变量解释教程、统计标签对照或“读表重点”写成读者可见的公式说明、图注或表注。
- 禁止按固定坐标批量裁剪所有公式而不核对多行块、右侧括号、上下标和源页边界。
- 禁止使用图片承载本可稳定结构化为 MathML 的显示公式，除非记录了兼容性或识别风险理由。

## 验证门禁 / Verification Gate

公式密集书籍在最终 EPUB 或私人自用产物输出前，必须至少验证：

- 全书公式清单存在，并覆盖行内公式、显示公式、多行方程组、表格内统计符号和 OCR 破损公式。
- EPUB 中稳定显示公式已优先转为 MathML。
- 复杂公式图像兜底已登记 manifest，且文件存在、非空、未明显截断。
- EPUBCheck `fatal=0, error=0`。
- 随机抽检公式/证明块层时，公式不得被普通段落样本替代。
