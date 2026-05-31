# 章节译后控制模板 / Chapter Post-Translation Control Template

chapter_file: "{NNN_slug}.md"
human_required: false
human_feedback_status: "none" # none | requested_changes | approved
control_status: "AUTO_PENDING" # AUTO_PENDING | REWORK_REQUIRED | PASS
latest_round: 0
overall_score: null # 0-100
chinese_reading_score: null # 1-5
read_aloud_sample_count: 20
awkward_sentence_count: null
breathless_long_sentence_count: null
allow_next_chapter: false
chapter_scope_only: true
asset_route_status: "none" # none | text_fixed | routed_to_asset_gate | blocking_text_issue
return_to_stage: "07_translate_chapters"

## 中文说明

每章完成 `chapters/translated/{NNN_slug}.md` 后，AI 必须为该章创建并读取：

- `qa/chapter_controls/{NNN_slug}.control.md`

如果用户对该章翻译不满意，必须把反馈写入本文件，然后回到该章的翻译，不得继续把该章送入终稿。

如果用户没有说明，且 `human_required=false`，AI 必须自动对当前章执行全章文字检查并给出结论。不得检查成全书门禁，不得只检查用户点名项目，也不得把本文件当作抽样记录。

## 必查范围 / Required Full Check Scope

- [ ] scope：只检查当前章 `chapter_file`，不是全书章节。
- [ ] metadata/nav 影响：由本章产生的章节标题、目录题名、链接文字和章节级说明没有污染 metadata/nav。
- [ ] nav / 目录 / 标题：本章短目录题名、页面主标题、副标题自然准确，无英文标题链、英文括注或人名原文污染。
- [ ] 正文完整性：无漏译、错译、顺序错乱、段落层级损坏。
- [ ] 中文独立可读性：先不看原文，只读译文，确认它像自然中文书；中文独立阅读评分不低于 4/5。
- [ ] 朗读测试：随机朗读 20 句，明显拗口不超过 1 句，关键句没有不断气问题。
- [ ] 正文可读性：自然、通俗、可朗读；无大段长句、不断气句、机械直译、英文句法硬搬、学术腔堆叠、AI 味或省字式提纲化。
- [ ] 润色与节奏：长句已拆解或重组；连接关系符合中文；论文型内容也能让普通读者明白。
- [ ] 术语与专名：术语、专名、历史制度、身份称谓、变量名、数字、时间、地名一致且准确。
- [ ] 术语控制级别：已读取 `glossary/terms.csv.term_control`；`locked` 已硬锁，`preferred` 已按上下文自然处理，`avoid` 未进入正文，`note_only` 未压进正文。
- [ ] 原词处理：普通名词、历史术语、制度名、身份称谓、专业术语和文化负载词正文默认用中文译名或准确意译；不存在无必要的 `中文译名（source term）`。
- [ ] 原词注释：必要原词、定义和译名理由已放入本章译注、章末注或术语表；正文注号如 `[1]` / `（1）` 与注释对应。
- [ ] 正文括注例外：若正文保留 `中文译名（source term）`，已记录不可替代原因，且不是批量使用。
- [ ] 术语表禁用写法扫描：已按 `glossary/terms.csv.forbidden_body_renderings` 逐项扫描正文；未发现禁用写法、裸露源语词、误导性泛译或未授权正文括注。
- [ ] 注释：译注/脚注/尾注清楚不过密；标记不与正文黏连；关键背景足以帮助读者理解。
- [ ] 图表/表格/公式/图片文字接口：本章正文引用、编号、图题、表题、alt text、变量说明、单位和读图/读表说明为清楚中文；复杂资产问题已路由，不在本节点无限循环。
- [ ] asset route：若有重绘、裁剪、OCR、数值复核、公式排版、资源路径或 manifest 问题，已写入 `qa/assets/{NNN_slug}.asset_followup.md` 或 `qa/technical/{NNN_slug}.diagram_table_audit.md`，并阻止进入终稿/构建。
- [ ] 样式与 EPUB 可见内容：无乱码、异常空格、旧纸书页码目录、可见分隔符、内部工作说明、模板说明或 AI 痕迹。
- [ ] 用户反馈：若有用户指出问题，已逐条记录、修复并复查。

## English

After each translated chapter is produced, the AI must create and read this chapter-control file. This is a full-chapter gate, not a sampling note. If the user requests changes, route the chapter back to translation. If no user feedback is provided and `human_required=false`, perform automatic checks, fix failures, append a new round, and continue only on PASS.

## 自动 PASS 条件 / Auto PASS Criteria

- 不存在未关闭的 P0/P1/P2。
- 不存在模板硬门禁失败。
- 中文独立阅读评分 >= 4/5。
- 20 句朗读测试中明显拗口不超过 1 句，且关键句没有不断气问题。
- 不存在读者不可理解、明显拗口、学术味过重、大段长句、不断气句、机械直译或英文句法硬搬。
- 不存在严重误译、漏译、术语/专名/数字/事实错误。
- 不存在无必要的正文 `中文译名（source term）`；必要原词已移入译注、章末注或术语表，正文注号清楚。
- 不存在 `glossary/terms.csv.forbidden_body_renderings` 中列出的正文禁用写法。
- 当前章图表、公式、表格、图片的文字接口不存在 reader-facing 错误；复杂资产问题已路由到资产/技术门禁。
- 最近一轮全量检查覆盖了本模板列出的所有范围。
- 最近一轮记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true`。
- 发现并修复问题的轮次没有直接 PASS，而是记录为 `FIXED_RECHECK_REQUIRED` 并追加新的整章复查。
- `allow_next_chapter: true` 只能在 `control_status: "PASS"` 时填写。

## 输出 / Output

- `control_status=PASS`：仅当最近一轮同时记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` 时，才允许进入下一章翻译，并继续忠实度、可读性、术语和门禁审校。
- `control_status=REWORK_REQUIRED`：仅该章回到 `07_translate_chapters` 重译。

## 轮次记录 / Round Records

### Round 1

round_status: "AUTO_PENDING" # PASS | REWORK_REQUIRED
latest_round_status:
scope: "FULL_CHAPTER"
issues_found:
fixes_applied:
unresolved_blocking_issues:
score: null
chinese_reading_score: null # 1-5
read_aloud_sample_count: 20
awkward_sentence_count: null
breathless_long_sentence_count: null
allow_next_chapter: false
asset_route_status: "none"

检查范围摘要：

-

阻塞问题：

| severity | location | issue | required_fix | status |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

术语呈现审计：

| source_term | target_term | term_control | display_policy | forbidden_body_renderings_checked | findings | status |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

图表/资产分流：

| item | text_interface_status | asset_issue | routed_to | blocks_next_chapter | blocks_final_build |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

非阻塞改进：

-

已执行修复：

-

复查结论：

-

> 强制规则：存在本文件不等于通过门禁。发现任何问题并修复的轮次只能记为 `FIXED_RECHECK_REQUIRED`，不得直接 PASS。只有最后一轮全章复查 `issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`，且 `latest_round_status: "PASS"`、`allow_next_chapter: true` 时，才可继续下一章。通俗化与专业质量不是对立关系；译文要尽量顺读、有趣、不费劲，同时保持专业术语和原书水准。
