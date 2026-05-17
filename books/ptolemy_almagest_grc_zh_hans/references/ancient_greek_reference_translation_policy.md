# 第二语言参考译本政策 / Reference Translation Policy

## 原则 / Principle

古希腊文是翻译底本。现代英语、法语、德语、拉丁语或其他语言译本只能作为 reference witness，用于理解、疑难定位、差异校对和技术核验。

The Ancient Greek text is the base text. A second-language translation is a reference witness, not a pivot source.

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

