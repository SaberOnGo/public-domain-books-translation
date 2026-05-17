# 古希腊文来源类型与可信度 / Ancient Greek Source Types

## 目的 / Purpose

不同来源的风险不同。AI 不能把扫描、OCR、网页文本、校勘本、现代译本混为一类。

## 来源分级 / Source Classes

| class | source_type | 可作为底本 | 必要检查 |
|---|---|---|---|
| A | 公版校勘本的清晰扫描或可信数字转写 | 可以 | 版本、编辑者、出版年、页码/行号、缺页、扫描质量 |
| B | TEI/XML、Perseus、Wikisource 等结构化古希腊文文本 | 可以，但需抽查 | 来源版本、转写依据、段落/行号、是否现代校订 |
| C | OCR 文本 | 只能作为待校材料 | 与扫描逐页抽查；高风险段不得未校使用 |
| D | 现代第二语言译本 | 不可作为底本 | 只能作参考证据；需版权和使用边界 |
| E | 商业电子书、来源不明 EPUB、盗版扫描 | 不可使用 | 停止或另找来源 |

## 多源分工 / Multi-Source Role Separation

古希腊项目常同时使用扫描本、古希腊文转写和现代译本。AI 必须先划分角色，不能把它们混成一个“来源”：

- 扫描 PDF 或校勘本影像：底本影像、页码、版面、校勘区、图表、表格和最终核验依据。
- 古希腊文转写、TEI/XML 或 OCR：检索、章节切分、source text 抽取、分词链和细节校正的辅助来源；必须记录转写依据、许可、commit/hash 或版本。
- 第二语言译本：reference witness，只能帮助理解和发现疑点；不得作为转译底稿，不得单独决定古希腊文本读法。

如果 PDF 扫描、古希腊转写和第二语言译本三者冲突，处理顺序是：先核 PDF/校勘本影像和古希腊转写，再记录异文、OCR/转写疑点或参考译本差异；不得用译本直接覆盖古希腊文。

## 必须写入 source evidence 的字段 / Required Fields

- source_url
- source_type
- source_class
- editor_or_transcriber
- publication_year
- source_language
- edition_title
- volume_or_book_range
- page_line_section_system
- scan_quality
- ocr_status
- missing_or_damaged_pages
- public_domain_evidence
- reason_for_selecting_this_base_text

## 硬规则 / Hard Rules

- 现代译本不是古希腊文来源。
- 未校 OCR 不是可靠底本。
- 第二语言译本不是 OCR 校正 authority；它只能提示疑点，不能直接修正文底稿。
- 来源页没有明确版本和编辑信息时，必须在 `metadata/source_evidence.md` 标为风险。
- 如果来源只提供现代语言译本而没有古希腊文底本，不得使用 `grc-zh-Hans` 批量翻译流程。
