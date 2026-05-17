# Source Witness Manifest / 古希腊文底本与见证清单

本文件由 AI 在具体书籍工程中补全。模板目录内不得填写具体书籍信息。

## Base Text / 主底本

- source_language:
- edition_title:
- editor_or_transcriber:
- publication_year:
- source_url:
- public_domain_evidence:
- volume_or_book_range:
- page_line_section_system:
- scan_or_text_type:
- ocr_status:
- missing_or_damaged_pages:
- reason_for_selection:

## Source Role Hierarchy / 来源角色层级

具体书籍若同时使用扫描本、古希腊文转写和第二语言译本，必须在此处明确三者职责：

1. `primary_facsimile_or_critical_source`：古希腊文底本依据。扫描 PDF 可作为页图、版面、校勘、图表、表格和最终核验依据。
2. `auxiliary_greek_transcription`：古希腊文转写/OCR/TEI/XML 辅助来源。可用于检索、切分、初步 source text 抽取、分词链和细节校正，但必须能回查到底本扫描或校勘来源。
3. `reference_translation_only`：第二语言译本。只能用于理解、疑难定位、差异摘要和技术核验；不得作为中文转译底稿，不得作为 OCR 校正的最终 authority。

硬规则：第二语言参考译本只能提示“可能有问题”，不能单独改写古希腊文底稿。任何影响正文的修正都必须回到古希腊文底本、扫描页、校勘语境或授权的古希腊转写记录。

## Witnesses / 文本见证

| id | witness_type | language | title_or_source | editor_translator | date | rights_status | allowed_use | notes |
|---|---|---|---|---|---|---|---|---|
| base | critical_edition/scan/tei/html/ocr | Ancient Greek |  |  |  |  | base text |  |
|  | auxiliary_transcription/ocr_control | Ancient Greek |  |  |  |  | auxiliary Greek control only | not a second-language translation |
|  | reference_translation/commentary/variant_edition |  |  |  |  |  | reference witness only | not a pivot source |

## Numbering System / 编号体系

- book_or_volume:
- chapter_or_section:
- page:
- line:
- figure_or_table:
- notes:

manifest_status: `FAIL`
