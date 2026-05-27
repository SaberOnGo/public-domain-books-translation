# 07 分章翻译 / Translate Chapters

## 输入 / Input

- `chapters/src/*.md`
- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `glossary/terms.csv`
- `qa/pretranslation/pretranslation_report.md`

## 前置门禁 / Prerequisite Gate

只有当 `qa/pretranslation/pretranslation_report.md` 明确 `PASS` 时，才可开始。

## 任务 / Tasks

逐章翻译到：

- `chapters/translated/{same_filename}.md`

每章翻译前必须先在内部判断：

1. 本章原文功能。
2. 叙述声音。
3. 关键术语。
4. 关键意象。
5. 易误译/易越界发挥/易省字式翻译的段落。

## 翻译要求 / Translation Requirements

- 保持标题和段落结构。
- 章节标题必须按 `references/english_chapter_title_strategy.md` 处理；不得把英文 `--` 标题链机械翻成多个中文 `——`。
- 强制规则：章节标题、副标题和 EPUB 目录题名里的人名不算“正文首次出现”。标题只使用中文译名，不得追加英文原名或括注；英文原名必须放到正文第一次自然出现该人名的位置。
- 普通名词、器物名、衣物名、材料名和动作名必须译成中文，不得写成 `source term（中文释义）`，也不得写成 `中文词（source term）`。人名首次出现保留英文原名的规则不适用于普通名词。
- 历史术语、制度名、身份称谓、专业术语和文化负载词正文默认使用中文译名或准确意译，不得批量写成 `中文译名（source term）`。需要交代原词时，优先在正文处加统一注号，如 `术语[1]` 或 `术语（1）`，并把原词、释义和译名理由写入本章译注、章末注或术语表。只有不保留原词会造成明显误解、原词本身是作者论证对象、或学界译名分歧必须当场交代时，才允许正文短括注原词，并在 control 或术语表记录理由。
- 盎格鲁-撒克逊制度身份词示例：`thegn` / `thane` 不得默认音译为“塞恩”，也不宜统一译成“支持者”。若语境强调土地、等级、服役和政治义务，正文按上下文用“王室领主”“领主近臣”“盎格鲁-撒克逊领主”等；术语注再写原文为 `thegns`，又作 `thanes`。`witenagemot` 正文用“贤人会议”，原词放术语注。
- 删除旧纸书中的可见分隔符，例如 `* * * * *`、`*****`、`----`；不得替换成 `---` 或其他可见分隔线。
- 忠实事实和语气。
- 中文必须自然，有叙述气息。
- 关键句要有画面和记忆点。
- 不接受第一版“通顺但无味”的译文。
- 不得直接写入 `chapters/final/`。

## 章节译后控制 / Post-Translation Control

每章写入 `chapters/translated/` 后，必须立即进入：

- `prompts/08a_chapter_post_translation_control_zh_en.md`

并创建：

- `qa/chapter_controls/{same_filename}.control.md`

这是“每章译后，全量检查并修复节点”，不是可选自检。该节点必须检查 metadata、nav、目录、正文、注释、图表、公式、表格、图片、样式、读者可见内容、通俗化、可读性、润色、名词术语和注释等，不得只检查用户点名项目。

如果该章 control 最近一轮不是 `PASS`，或 `allow_next_chapter` 不是 `true`，AI 必须修复并追加同节点复查，不得进入下一章翻译、后续审校或 `chapters/final/`。如果用户对该章不满意，AI 必须只回到该章重译，不得让该章继续进入后续审校。

## 状态 / State

成功后：

- `status = TRANSLATED`
- `chapters_translated = 章节数`
- `current_step = chapters_translated`

注意：`TRANSLATED` 不代表可进入终稿，必须等待每章 control PASS。
