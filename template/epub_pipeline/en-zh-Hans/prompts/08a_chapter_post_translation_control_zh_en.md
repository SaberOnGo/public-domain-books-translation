# 08A 每章译后全量检查并修复节点 / Per-Chapter Full Post-Translation Check

## 目的 / Purpose

在每章翻译完成后，立即只针对该章做全章文字检查和必要修复，避免风格、语气、可读性、术语、注释和读者可见文字问题被拖到分层随机抽检阶段才暴露。

本节点是当前章的译后文字硬门禁，不是全书门禁，也不是抽样审校。未通过时不得进入下一章翻译、后续章节审校、`chapters/final/` 或 EPUB 构建。

## 输入 / Input

- `chapters/src/{NNN_slug}.md`
- `chapters/translated/{NNN_slug}.md`
- `chapters/notes/{NNN_slug}.*`（如有）
- `metadata/style_profile.md`
- `metadata/book_specific_translation_research.md`
- `glossary/terms.csv`
- `qa/chapter_controls/_TEMPLATE.control.md`
- 该章涉及的图表、公式、表格、图片、图注、alt text、脚注/尾注和读者可见样式文件，仅用于该章读者可见文字接口和资产风险分流。

## 执行规则 / Execution Rules

每个章节翻译后，AI 必须创建：

- `qa/chapter_controls/{NNN_slug}.control.md`

该文件必须记录：

- 本章译后全量检查范围，明确覆盖当前章整章，而不是抽样、全书扫描或只看用户点名项目。
- metadata/nav/目录中由本章产生的标题和链接、正文、注释、图表/公式/表格/图片的读者可见文字接口、样式和读者可见内容的检查结论。
- 通俗化、可读性、润色、叙述节奏、术语、专名、译注、数字、事实关系和读者理解门槛的检查结论。
- 标题人名检查结果：章节标题/副标题/目录题名只使用中文译名；标题中的人名不计入“正文首次出现”；英文原名只出现在正文第一次自然出现处、译注或术语表。
- 原词呈现检查结果：普通名词、历史制度、身份称谓、专业术语和文化负载词正文原则上用中文译名或准确意译；原词、定义和译名理由优先放入本章译注、章末注或术语表。正文出现 `中文译名（source term）` 只允许作为少量例外，且必须记录必要性理由。
- 术语表逐项审计结果：必须读取 `glossary/terms.csv` 的 `display_policy`、`forbidden_body_renderings`、`note_text` 和 `exception_reason`，逐项检查本章正文。发现禁用写法、未授权正文括注原词、裸露源语词或误导性泛译，必须修复后追加复查。
- 是否有人类反馈。
- 是否需要回到本章重译。
- 每一轮发现的问题、修复项、复查结论、总分和是否允许进入下一章。
- 若该章含图表、公式、表格或图片，还必须记录资产分流结论：`none`、`text_fixed`、`routed_to_asset_gate` 或 `blocking_text_issue`。
- 最终 `control_status: "PASS"` 或 `control_status: "REWORK_REQUIRED"`。

必须逐章执行：第 N 章未通过时，不得把第 N+1 章当作正常流程继续翻译。并行执行时，每章也必须独立满足本节点后才能进入后续步骤。

## 全量检查清单 / Full Check Scope

本节点至少检查：

1. `metadata` 影响：章节标题、作者/译者/贡献者、版本说明、私有/公开模式说明不会被本章内容误带偏。
2. `nav` / 目录 / 标题：目录题名短、准、自然；页面标题可读；无英文标题链、英文括注、人名原文污染。
3. 正文：忠实、完整、自然、通俗、可朗读；无机械直译、英文句法硬搬、学术腔堆叠、过度压缩、AI 味、无依据发挥。
4. 术语与专名：全章一致；历史制度、身份称谓、组织名、变量名等以中文为主；必要原词优先放本章译注、章末注或术语表。正文注号如 `[1]` / `（1）` 必须与注释对应，不能让正文被英文或源语括注打断。必须按 `glossary/terms.csv.forbidden_body_renderings` 扫描正文并记录结果。
5. 注释：解释足够、不过密、不打断阅读；脚注标记不与正文黏连；读者不查外部资料也能理解关键处。
6. 图表、公式、表格、图片文字接口：若当前章包含这些内容，本节点检查正文引用、编号、标题、图注/表注、alt text、单位、变量说明和读图/读表提示是否为清楚中文。复杂重绘、裁剪、OCR、数值复核、公式排版和资源 manifest 问题进入 `qa/technical/{NNN_slug}.diagram_table_audit.md`、`qa/assets/{NNN_slug}.asset_followup.md` 或后续资产门禁，不在本节点无限循环。
7. 样式与 EPUB 读者可见内容：无乱码、异常空格、旧纸书页码目录、可见分隔符、内部工作说明、AI 痕迹、模板说明泄漏。
8. 可读性与润色：中文句长、节奏和连接关系适合普通读者；论文型原文也要在准确基础上译得清楚、易懂、有阅读兴趣。

## 人类反馈 / Human Feedback

如果用户对某一章不满意：

1. 把用户反馈原文写入该章 control 文件。
2. 设置 `control_status=REWORK_REQUIRED`。
3. 只回到该章 `07_translate_chapters` 或更早必要阶段，不得影响其他已经 PASS 的章节。
4. 重译后再次运行本流程。

如果用户没有说明，且 `human_required=false`：

- AI 自动按 `_TEMPLATE.control.md` 检查。
- 通过则 `PASS`。
- 不通过则自动返工，不得假装通过。

## 返工与追加轮次 / Rework and Extra Rounds

任一情况出现，本节点为 `REWORK_REQUIRED`：

- P0/P1/P2 或模板硬门禁失败。
- 读者不可理解、明显拗口、学术味过重、中文表达不通俗。
- 事实、术语、专名、数字、图表、公式、表格、图片、注释或读者可见样式错误。
- 历史术语、身份称谓、专业术语等大面积使用 `中文译名（source term）`，或正文括注原词没有必要性说明。
- `glossary/terms.csv` 已列出的任一 `forbidden_body_renderings` 出现在正文中。
- 高风险术语没有 `display_policy`、`note_text` 或必要的 `forbidden_body_renderings`，导致本章无法验证正文写法。
- 当前章图表/公式/表格/图片的正文引用、图注、表注、alt text、变量说明或读者说明错误，导致该章文字不可理解。
- 只检查用户点名项目，未覆盖全章。
- 总分低于 75，或低于项目/profile 更严格阈值。

修复后必须在同一 control 文件追加新一轮记录，不得覆盖旧失败记录。只有最近一轮无未关闭阻塞问题，并且“无问题或总分不小于 75”（若项目/profile 更严格则按更严格规则），才可设置 `control_status: "PASS"` 和 `allow_next_chapter: true`。

## 图表与资产分流 / Figure and Asset Routing

本节点主要守住当前章文字质量。图表、公式、表格、图片在本节点按以下方式处理，避免复杂资产问题造成无限循环：

- `text_fixed`：图题、表题、alt text、正文引用、变量说明、读图/读表说明等文字问题能在当前章修复，必须在本节点修复并复查。
- `blocking_text_issue`：图表文字接口错误导致该章正文无法理解，本节点 FAIL，修复后追加一轮，未修复不得进入下一章。
- `routed_to_asset_gate`：重绘、裁剪、图片质量、OCR、复杂数值复核、公式排版、资源路径或 manifest 等资产/技术问题，若不影响当前章文字译文继续处理，可登记到 `qa/assets/{NNN_slug}.asset_followup.md` 或 `qa/technical/{NNN_slug}.diagram_table_audit.md`，本节点可在文字通过且分数不低于 75 时允许进入下一章。

`routed_to_asset_gate` 不是忽略问题。它必须阻止该章进入 `chapters/final/`、样章/全书 EPUB 构建和 release，直到对应资产/技术门禁 PASS。

## 并行 / Parallelism

默认逐章闭环：上一章未通过本节点时，不得进入下一章翻译。只有项目明确批准并行批处理时，才可并行处理不同章节；即便并行，每章也必须独立 PASS 且 `allow_next_chapter: true` 后才可进入后续流程，流水线不得把未通过章节视为已完成。

## 输出 / Output

- `qa/chapter_controls/{NNN_slug}.control.md`
- `state/pipeline_state.json.quality_gate.chapter_post_controls_status`

## PASS 条件 / PASS Criteria

- 当前章有 control 文件。
- 当前章 control 文件 `control_status=PASS`。
- 最近一轮 `allow_next_chapter=true`。
- 最近一轮记录完整全量检查范围、问题、修复、复查和总分。
- 不存在把英文原名或英文括注塞进章节标题、副标题或目录题名的情况。
- 不存在无必要的正文 `中文译名（source term）`；必要原词已移入本章译注、章末注或术语表，正文注号与注释对应。
- 本章已按 `glossary/terms.csv.forbidden_body_renderings` 完成正文扫描，未发现禁用写法。
- 不存在未关闭的 P0/P1/P2、读者不可理解、事实/术语/当前章文字接口错误或模板硬门禁失败。
- 图表/公式/表格/图片若存在复杂资产问题，已路由到资产/技术门禁，且本节点未把该问题误标为已解决。
- 任何用户明确指出的问题已回写并修正。
