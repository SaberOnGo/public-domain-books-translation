# 章节译后控制模板 / Chapter Post-Translation Control Template

chapter_file: "{NNN_slug}.md"
human_required: false
human_feedback_status: "none" # none | requested_changes | approved
control_status: "AUTO_PENDING" # AUTO_PENDING | REWORK_REQUIRED | PASS
latest_round_status: "AUTO_PENDING" # AUTO_PENDING | FIXED_RECHECK_REQUIRED | PASS
scope: "FULL_CHAPTER"
issues_found:
fixes_applied:
unresolved_blocking_issues:
allow_next_chapter: false
return_to_stage: "07_translate_chapters"

## 中文说明

每章完成 `chapters/translated/{NNN_slug}.md` 后，AI 必须为该章创建并读取：

- `qa/chapter_controls/{NNN_slug}.control.md`

如果用户对该章翻译不满意，必须把反馈写入本文件，然后回到该章的翻译，不得继续把该章送入终稿。

如果用户没有说明，且 `human_required=false`，AI 必须自动执行以下检查并给出结论：

1. 是否存在机械直译、AI 味、日语句法硬搬。
2. 是否存在“省字式翻译”：把叙事压缩成动作清单。
3. 是否存在无依据发挥：新增原文没有的比喻、声音、情节或价值判断。
4. 是否有关键句缺少画面、节奏和中文气息。
5. 是否有专名、术语、地名、时间、数字错误。
6. 是否保持段落层级和章节标题。
7. 是否符合本书 `metadata/style_profile.md`。
8. 是否按 `metadata/japanese_source_profile.md` 和 `qa/textual/japanese_textual_notes.md` 处理旧字、振假名、底本注、OCR 疑难和异读。
9. 是否把官能、暴力、病态心理或强制关系保持在原作文学边界内。
10. 是否完成整章中文成稿润色，读起来顺、不费劲，并在原作允许时有阅读兴趣。
11. 是否为了通俗化损害了术语、概念层级、叙事风格或原书专业水准。

## English

After each translated chapter is produced, the AI must create and read this chapter-control file. If the user requests changes, route the chapter back to translation. If no user feedback is provided and `human_required=false`, perform automatic checks and continue only on PASS.

## 自动 PASS 条件 / Auto PASS Criteria

- 不存在严重误译。
- 不存在明显机械直译。
- 不存在无依据加戏。
- 不存在省字式提纲化表达。
- 最近一轮记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true`。
- 发现并修复问题的轮次没有直接 PASS，而是记录为 `FIXED_RECHECK_REQUIRED` 并追加新的整章复查。
- 日语底本文字形态、敬语/称谓和官能/心理边界没有未处理风险。

## 输出 / Output

- `control_status=PASS`：仅当最近一轮同时记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` 时，才允许进入下一章，并继续忠实度、可读性、术语和门禁审校。
- `control_status=REWORK_REQUIRED`：仅该章回到 `07_translate_chapters` 重译。

> 强制规则：存在本文件不等于通过门禁。发现任何问题并修复的轮次只能记为 `FIXED_RECHECK_REQUIRED`，不得直接 PASS。只有最后一轮全章复查 `issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`，且 `latest_round_status: "PASS"`、`allow_next_chapter: true` 时，才可继续下一章。
