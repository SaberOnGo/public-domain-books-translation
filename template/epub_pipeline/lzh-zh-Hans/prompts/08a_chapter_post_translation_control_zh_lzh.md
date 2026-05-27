# 08a 章节译后控制 / Chapter Post-Translation Control

## 输入

- `chapters/src/{chapter}.md`
- `chapters/translated/{chapter}.md`

## 任务

创建 `qa/chapter_controls/{chapter}.control.md`，检查：

1. 每段古文是否有对应今译。
2. passage id 是否稳定。
3. 注释是否存在必要项。
4. 疑难断句、异文、人物关系是否同步记录。
5. 是否出现现代版权译文或现代校注表达残留。

## 结果

- `control_status: PASS` 后才能进入忠实度审校。
- `control_status: FAIL` 时必须回到本章翻译。
