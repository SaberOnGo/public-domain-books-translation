# 11 章节终稿门禁 / Chapter Quality Gate

## 输入 / Input

- `chapters/src/{NNN_slug}.md`
- `chapters/translated/{NNN_slug}.md`
- `qa/chapter_controls/{NNN_slug}.control.md`
- `qa/fidelity/{NNN_slug}.md`
- `qa/readability/{NNN_slug}.md`
- `qa/imagery/{NNN_slug}.imagery.md`
- `qa/terminology/{NNN_slug}.md`
- `metadata/style_profile.md`
- `glossary/proper_nouns.csv`
- `references/proper_noun_display_policy.md`
- `references/note_marker_policy.md`

## 任务 / Tasks

逐章判断是否可以进入终稿。

开始判断前，必须先读取 `qa/chapter_controls/{NNN_slug}.control.md`。若该文件不存在，或最近一轮不是零问题整章 PASS，本章直接 `FAIL`，不得写入 `chapters/final/`。最近一轮必须记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true`；发现并修复问题的轮次不能直接 PASS。

本门禁先审中文独立可读性，再审忠实、术语和工程项。准确但不像中文书、需要读者按英文句法倒推才能理解的译文，不得 PASS。

## 一票否决 / Veto

任一出现则 `FAIL`：

- 每章译后全量检查缺失、未通过，或只检查用户点名项目。
- 重大误译或漏译。
- 关键术语错误。
- 明显直译腔。
- 学术味过重、拗口难懂，普通目标读者无法顺畅理解。
- 中文独立阅读评分低于 4/5。
- 随机朗读 20 句，明显拗口超过 1 句，或关键句明显不断气。
- 成片大段长句、过密分号、英文从句硬接，导致中文读者需要反复回读。
- 关键句只说明、不成像。
- 越界发挥。
- 省字式翻译。
- 标题错误：半截标题、机械保留多个英文 `--` 对应的中文 `——`、长标题未拆分为短目录题名/页面主标题/可选副标题。
- 标题专名错误：把标题中的专名当作“正文首次出现”、标题追加首次出现括注，或标题显示与 `glossary/proper_nouns.csv.subsequent_rendering` 不一致。策略 `1`/`3`/`5` 通常显示中文，策略 `2`/`4` 可保留原名。
- 重点专有名词未按 `glossary/proper_nouns.csv.display_policy` 执行；默认策略 `3`、用户设置策略、策略 `5` 注号或重复原文例外没有核对并记录。
- 普通名词未翻译：器物名、衣物名、材料名、动作名等普通名词仍写成 `source term（中文释义）` 或 `中文词（source term）`，而不是直接译成中文正文。
- 历史制度、身份称谓、学术术语等在正文无必要地写成 `中文译名（source term）` 或大量夹杂英文/源语原词，导致阅读被打断；必要原词未移入本章译注、章末注或术语表。
- 正文括注原词没有记录必要性理由，或可以用正文注号加译注解决却仍在正文堆括注。
- 本章出现 `glossary/terms.csv.forbidden_body_renderings` 中列出的禁用写法，或 control 文件没有记录术语呈现审计。
- 正文注号使用带圈数字、小圆圈“注”、裸 `译注：` / `脚注：` / `尾注：` / `附注：` 或句末裸数字；策略 `5` 的重点专名首次正文出现缺少 `[1]`、`(1)` / `（1）`、`注1` 之一。
- `thegn` / `thane` 在正文音译为“塞恩”，或被统一泛译为“支持者”，导致土地、等级和服役义务信息丢失；`witenagemot` 在正文夹杂原词而不是使用“贤人会议”。
- 图表、公式、表格、图片、图注、alt text、注释或读者可见样式存在错误，或读者无法独立理解。
- 分号滥用：把英文连接关系机械处理成大量 `；`，或普通中文正文出现 ASCII `;`。
- 排版污染：中文字符之间出现连续空格、旧纸书页码目录/插图页码目录原样进入正文、出现乱码或编码污染。
- 旧纸书分隔符污染：正文中出现 `* * * * *`、`*****`、`----`、`---` 等可见分隔符。
- 翻译阶段把 QA、解释、流程说明、术语审计文字混入译文正文。
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

## 专家级与多义词硬门禁 / Expert Quality and Polysemy Hard Gate

章节进入 `chapters/final/` 前，必须确认 `qa/chapter_controls/{chapter}.control.md` 最近 PASS 轮记录 `expert_translation_skill_used: true`、`expert_level_review_status: "PASS"`、`polysemy_translation_stage_review: "PASS"`、`polysemy_context_review: "PASS"`、`polysemy_unresolved_count: 0`。若后文线索推翻前文选义，或译文只是良好但未达专家级出版质量，本章 FAIL，回到翻译、译后控制或相应审校节点。
