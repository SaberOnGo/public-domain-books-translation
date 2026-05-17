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
- 古典技术语硬译：例如“将割”“超过某线”“所对弧之半所对的直线”等让现代读者无法复原几何关系的表达。
- 技术说明过度展开：原文一个作图动作被扩写成多句解释，导致证明主线被稀释。
- 关键句只说明、不成像。
- 越界发挥。
- 省字式翻译。
- 存在未解决的 `qa/textual/textual_uncertainty_log.md` 相关 `UNRESOLVED` 项。
- 有参考译本转译痕迹。
- 标题错误：半截标题、机械保留现代目录长链、长标题未拆分为短目录题名/页面主标题/可选副标题。
- 标题人名错误：章节标题、副标题或目录题名中出现古希腊文原名、拉丁化转写或外文括注，或把标题中的人名当作“正文首次出现”。标题只用中文译名；原名或转写必须放在正文第一次自然出现处、译注或术语表。
- 普通名词未翻译：器物名、衣物名、材料名、动作名等普通名词仍写成 `source term（中文释义）` 或 `中文词（source term）`，而不是直接译成中文正文。
- 分号滥用：把古希腊文连接关系机械处理成大量 `；`，或普通中文正文出现 ASCII `;`。
- 技术依据污染：正文裸写 `Eucl.`，或出现无章末说明的《几何原本》编号。
- 数值显示污染：读者版正文裸露 `37;4,55` 等内部记法、`37份4′55″` 等伪角分秒写法，或把非角度六十进制值改成十进制小数。
- 排版污染：中文字符之间出现连续空格、旧纸书页码目录/插图页码目录原样进入正文、出现乱码或编码污染。
- 旧纸书分隔符污染：正文中出现 `* * * * *`、`*****`、`----`、`---` 等可见分隔符。
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

