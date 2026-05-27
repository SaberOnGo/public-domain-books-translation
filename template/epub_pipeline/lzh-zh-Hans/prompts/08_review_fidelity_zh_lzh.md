# 08 忠实度审校 / Fidelity Review

## 输入

- `chapters/src/{chapter}.md`
- `chapters/translated/{chapter}.md`
- `qa/chapter_controls/{chapter}.control.md`
- `qa/textual/classical_chinese_textual_notes.md`

## 任务

逐 passage 检查：

- 古文与今译是否对应。
- 是否误判主语、宾语、否定、因果、转折、使动、意动或被动。
- 是否误解人物关系、国名、官名、地名和时代背景。
- 是否把不确定读法写成确定断言。
- 是否新增原文没有的心理、情节、评价或因果。

输出 `qa/fidelity/{chapter}.fidelity.md`。

## 门禁

任一 P0/P1 忠实度问题未关闭时，不得进入终稿。
