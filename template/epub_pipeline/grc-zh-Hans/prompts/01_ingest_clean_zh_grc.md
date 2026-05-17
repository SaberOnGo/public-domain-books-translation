# 01 抓取、版权核查与清洗 / Ingest, Rights Check & Clean

## 输入 / Input

- `SOURCE_URL`
- `PROJECT_ROOT`

## 任务 / Tasks

1. 从 `SOURCE_URL` 获取原文或原文页面。
2. 判断可用的古希腊文版本：优先可审计的校勘文本、TEI/XML、HTML 转写或清晰扫描；纯文本必须记录来源版本。
3. 保存原始文本到 `source/source_text_raw.txt`。
4. 清洗头尾样板、版权头、下载说明，保存正文到 `source/source_text.txt`。
5. 生成 `source/source_manifest.json`：
   - source_url
   - retrieved_at_utc
   - raw_sha256
   - clean_sha256
   - raw_bytes
   - clean_bytes
6. 生成 `metadata/source_evidence.md`：
   - 来源链接
   - 选用哪个文本版本
   - 古希腊文底本名称、编辑者、出版年、卷册/页码/行号体系
   - OCR、人工转写或数字文本状态
   - 为什么不用第三方商业电子版
7. 生成 `metadata/source_witness_manifest.md`：
   - 主底本。
   - 相关 witness。
   - 编号体系。
   - 扫描/OCR/转写风险。
   - 若同时存在扫描 PDF、古希腊文转写和第二语言译本，必须写清 `primary_facsimile_or_critical_source`、`auxiliary_greek_transcription`、`reference_translation_only` 三个角色。
8. 若存在三源或多源校对，生成 `source/triangulated_source_control.md`：
   - PDF/校勘本影像的职责。
   - 古希腊转写/OCR/TEI/XML 的职责。
   - 第二语言参考译本的职责和禁用边界。
   - 三者冲突时的处理顺序。
9. 生成 `metadata/rights_checklist.md`：
   - 原文作者
   - 作者生卒年，如可查
   - 出版年份，如可查
   - 来源站点的版权口径
   - 美国/中国/常见地区公版风险初判
   - 是否允许进入翻译制作

## 硬规则 / Hard Rules

- 如果当前目录仍在 `template/epub_pipeline/common` 或 `template/epub_pipeline/grc-zh-Hans` 模板目录内，必须停止，回到 `00_orchestrator` 先复制模板到书籍工程。
- 如果版权状态不明，设置 `status=FAILED`，不得继续。
- 如果只找到商业电子书而无公版原文，不得继续。
- 不要把来源方自动生成的 EPUB 当唯一翻译底本；优先可审计的纯文本或 HTML 原文。
- 不要把现代第二语言译本当作原文来源。
- 不要把现代第二语言译本当作 OCR 校正 authority；它只能提示疑点，不能直接修正古希腊底稿。
- 未校 OCR 只能作为待校材料，不得直接进入批量翻译。

## 输出 / Output

- `source/source_text_raw.txt`
- `source/source_text.txt`
- `source/source_manifest.json`
- `metadata/source_evidence.md`
- `metadata/source_witness_manifest.md`
- `metadata/rights_checklist.md`

## 状态 / State

成功后：

- `status = SOURCE_INGESTED`
- `current_step = ingest_clean_rights_checked`
