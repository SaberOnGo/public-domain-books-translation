# 11 章节终稿门禁 / Chapter Quality Gate

## 输入 / Input

- `chapters/src/{NNN_slug}.md`
- `chapters/translated/{NNN_slug}.md`
- `qa/fidelity/{NNN_slug}.md`
- `qa/readability/{NNN_slug}.md`
- `qa/imagery/{NNN_slug}.imagery.md`
- `qa/terminology/{NNN_slug}.md`
- `metadata/style_profile.md`

## 任务 / Tasks

逐章判断是否可以进入终稿。

## 一票否决 / Veto

任一出现则 `FAIL`：

- 重大误译或漏译。
- 关键术语错误。
- 明显直译腔。
- 关键句只说明、不成像。
- 越界发挥。
- 省字式翻译。
- 标题错误：半截标题、机械保留多个英文 `--` 对应的中文 `——`、长标题未拆分为短目录题名/页面主标题/可选副标题。
- 分号滥用：把英文连接关系机械处理成大量 `；`，或普通中文正文出现 ASCII `;`。
- 排版污染：中文字符之间出现连续空格、旧纸书页码目录/插图页码目录原样进入正文、出现乱码或编码污染。
- 随机朗读 10 句，有 2 句以上明显拗口。
- QA 文件缺失。

## 输出 / Output

- `qa/gates/{NNN_slug}.gate.md`

如果 PASS：

- 写入 `chapters/final/{NNN_slug}.md`

如果 FAIL：

- 不得写入 `chapters/final/`
- 报告必须说明回到哪个阶段：
  - 翻译阶段
  - 忠实度审校
  - 可读性/意象审计
  - 术语审校

## 状态 / State

所有章节 PASS 后：

- `status = CHAPTER_GATES_PASS`
- `chapters_reviewed = 章节数`
- `current_step = chapter_quality_gates_pass`

