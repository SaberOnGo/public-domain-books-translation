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
- 来源页没有明确版本和编辑信息时，必须在 `metadata/source_evidence.md` 标为风险。
- 如果来源只提供现代语言译本而没有古希腊文底本，不得使用 `grc-zh-Hans` 批量翻译流程。

