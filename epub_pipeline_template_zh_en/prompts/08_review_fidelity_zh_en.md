# 08 忠实度审校 / Fidelity Review

## 输入 / Input

- `chapters/src/{NNN_slug}.md`
- `chapters/translated/{NNN_slug}.md`
- `glossary/terms.csv`

## 任务 / Tasks

逐章对照原文与译文，检查：

- 漏译。
- 误译。
- 人名、地名、数字、方向、时间。
- 因果关系。
- 语气偏移。
- 历史称谓是否被静默现代化。

## 输出 / Output

- `qa/fidelity/{NNN_slug}.md`

可以修订 `chapters/translated/{NNN_slug}.md`，但必须在 QA 报告中记录。

## 状态 / State

成功后：

- `status = REVIEWING`
- `current_step = fidelity_review_done`

