# 章节译后控制模板 / Chapter Post-Translation Control Template

chapter_file: "{NNN_slug}.md"
human_required: false
human_feedback_status: "none" # none | requested_changes | approved
control_status: "AUTO_PENDING" # AUTO_PENDING | REWORK_REQUIRED | PASS
return_to_stage: "07_translate_chapters"

## 中文说明

每章完成 `chapters/translated/{NNN_slug}.md` 后，AI 必须为该章创建并读取：

- `qa/chapter_controls/{NNN_slug}.control.md`

如果用户对该章翻译不满意，必须把反馈写入本文件，然后回到该章的翻译，不得继续把该章送入终稿。

如果用户没有说明，且 `human_required=false`，AI 必须自动执行以下检查并给出结论：

1. 是否存在机械直译、AI 味、英文句法硬搬。
2. 是否存在“省字式翻译”：把叙事压缩成动作清单。
3. 是否存在无依据发挥：新增原文没有的比喻、声音、情节或价值判断。
4. 是否有关键句缺少画面、节奏和中文气息。
5. 是否有专名、术语、地名、时间、数字错误。
6. 是否保持段落层级和章节标题。
7. 是否符合本书 `metadata/style_profile.md`。

## English

After each translated chapter is produced, the AI must create and read this chapter-control file. If the user requests changes, route the chapter back to translation. If no user feedback is provided and `human_required=false`, perform automatic checks and continue only on PASS.

## 自动 PASS 条件 / Auto PASS Criteria

- 不存在严重误译。
- 不存在明显机械直译。
- 不存在无依据加戏。
- 不存在省字式提纲化表达。
- 章节可读性评分不低于 85/100。
- 忠实度评分不低于 90/100。

## 输出 / Output

- `control_status=PASS`：进入忠实度、可读性、术语、门禁审校。
- `control_status=REWORK_REQUIRED`：仅该章回到 `07_translate_chapters` 重译。
