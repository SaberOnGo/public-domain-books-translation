# 08 忠实度审校 / Fidelity Review

## 输入 / Input

- `chapters/src/{NNN_slug}.md`
- `chapters/translated/{NNN_slug}.md`
- `metadata/source_witness_manifest.md`
- `qa/textual/textual_uncertainty_log.md`
- `glossary/terms.csv`

## 任务 / Tasks

逐章对照原文与译文，检查：

- 漏译。
- 误译。
- 人名、地名、数字、方向、时间。
- 因果关系。
- 语气偏移。
- 历史称谓是否被静默现代化。
- 是否从古希腊文底本翻译，而不是从第二语言参考译本转译。
- 已记录异文、残损、拟补、OCR 不确定或语法歧义是否被正确处理。

## 输出 / Output

- `qa/fidelity/{NNN_slug}.md`

可以修订 `chapters/translated/{NNN_slug}.md`，但必须在 QA 报告中记录。

## 状态 / State

成功后：

- `status = REVIEWING`
- `current_step = fidelity_review_done`

