# 第二语言参考译本政策 / Reference Translation Policy

## 原则 / Principle

古希腊文是翻译底本。现代英语、法语、德语、拉丁语或其他语言译本只能作为 reference witness，用于理解、疑难定位、差异校对和技术核验。

The Ancient Greek text is the base text. A second-language translation is a reference witness, not a pivot source.

## 与扫描和转写的关系 / Relation to Facsimile and Transcription

- 扫描 PDF 或校勘本影像负责底本页图、版面、校勘、图表、表格和最终核验。
- 古希腊文转写、OCR 或 TEI/XML 负责检索、切分、初步抽取、分词链、长周期句分析和细节校正，但必须能回查到底本。
- 第二语言译本只负责参考理解和差异提示；不能作为 OCR 校正、分章、术语锁定或中文转译的最终依据。
- 当英译本与古希腊底稿不一致时，只能记录差异摘要，并回到古希腊文、扫描页、校勘记或授权转写判断。

## 允许用途 / Allowed Uses

- 帮助定位古希腊文难句的可能结构。
- 对照专名、术语、段落边界、图表编号和技术解释。
- 发现底本/OCR 可能错误。
- 记录不同学者对疑难句的理解差异。

## 禁止用途 / Forbidden Uses

- 直接从参考译本转译成中文。
- 复制仍受版权保护译本的措辞、注释、图表、表格或编排。
- 用参考译本抹平古希腊文歧义。
- 让参考译本的章节标题、术语或解释覆盖底本证据。
- 用参考译本直接修正 OCR/转写文本，而没有回查古希腊底本或扫描页。

## 必须记录 / Required Records

在具体书籍工程中记录：

- `metadata/reference_witness_policy.md`：如果启用 profile。
- `qa/textual/textual_uncertainty_log.md`：参考译本和底本冲突时。
- `qa/technical/reference_witness_diff_log.md`：如果启用古典科学 profile。

## 冲突处理 / Conflict Handling

1. 回到古希腊文底本。
2. 检查底本是否有异文、OCR 错误或标点/分章问题。
3. 记录参考译本差异。
4. 写明最终取舍。
5. 若仍不确定，相关句段不得进入最终版，必须保留 `UNRESOLVED`。
