# 章节译后控制模板 / Chapter Post-Translation Control Template

chapter_file: "{NNN_slug}.md"
human_required: false
human_feedback_status: "none" # none | requested_changes | approved
control_status: "AUTO_PENDING" # AUTO_PENDING | REWORK_REQUIRED | PASS
return_to_stage: "07_translate_chapters"
expert_translation_skill_used: false
expert_translation_skill_path: "skills/expert-translation-quality/SKILL.md"
expert_level_review_status: "AUTO_PENDING"
polysemy_translation_stage_review: "AUTO_PENDING"
polysemy_context_review: "AUTO_PENDING"
polysemy_watchlist_count: null
polysemy_revisited_count: null
polysemy_unresolved_count: null

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
10. 是否按 `skills/expert-translation-quality/SKILL.md` 达到专家级译文质量，并确认翻译阶段已主动处理局部上下文可判清的多义词、称谓、习语、术语和语法歧义。
11. 是否在后文已译出后回看当前章前文多义词和依赖上下文判义的位置；若后文推翻前文选义，必须修订并追加新一轮整章复查。

## English

After each translated chapter is produced, the AI must create and read this chapter-control file. If the user requests changes, route the chapter back to translation. If no user feedback is provided and `human_required=false`, perform automatic checks and continue only on PASS.

## 自动 PASS 条件 / Auto PASS Criteria

- 不存在严重误译。
- 不存在明显机械直译。
- 不存在无依据加戏。
- 不存在省字式提纲化表达。
- 章节可读性评分不低于 85/100。
- 忠实度评分不低于 90/100。
- 日语底本文字形态、敬语/称谓和官能/心理边界没有未处理风险。
- `expert_translation_skill_used: true`、`expert_level_review_status: "PASS"`、`polysemy_translation_stage_review: "PASS"`、`polysemy_context_review: "PASS"`、`polysemy_unresolved_count: 0`。
- 若局部上下文已能判清的多义词被留给审校，或后文推翻前文选义，修复轮不能直接 PASS，必须追加新的整章复查轮。

## 输出 / Output

- `control_status=PASS`：进入忠实度、可读性、术语、门禁审校。
- `control_status=REWORK_REQUIRED`：仅该章回到 `07_translate_chapters` 重译。
