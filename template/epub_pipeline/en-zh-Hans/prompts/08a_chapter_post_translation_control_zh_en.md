# 08A 每章节译后控制 / Per-Chapter Post-Translation Control

## 目的 / Purpose

在每章翻译完成后立即控制质量，避免整本翻完才发现风格、语气、可读性、术语或机械直译问题，导致大规模返工。

## 输入 / Input

- `chapters/src/{NNN_slug}.md`
- `chapters/translated/{NNN_slug}.md`
- `metadata/style_profile.md`
- `metadata/book_specific_translation_research.md`
- `glossary/terms.csv`
- `qa/chapter_controls/_TEMPLATE.control.md`

## 执行规则 / Execution Rules

每个章节翻译后，AI 必须创建：

- `qa/chapter_controls/{NNN_slug}.control.md`

该文件必须记录：

- 本章译后自检结果。
- 是否有人类反馈。
- 是否需要回到本章重译。
- 关键修改项。
- 最终 PASS/FAIL。

## 人类反馈 / Human Feedback

如果用户对某一章不满意：

1. 把用户反馈原文写入该章 control 文件。
2. 设置 `control_status=REWORK_REQUIRED`。
3. 只回到该章 `07_translate_chapters`，不得影响其他已经 PASS 的章节。
4. 重译后再次运行本流程。

如果用户没有说明，且 `human_required=false`：

- AI 自动按 `_TEMPLATE.control.md` 检查。
- 通过则 `PASS`。
- 不通过则自动返工，不得假装通过。

## 并行 / Parallelism

章节可并行翻译、并行控制。每章 control 文件互不覆盖。

## 输出 / Output

- `qa/chapter_controls/{NNN_slug}.control.md`
- `state/pipeline_state.json.quality_gate.chapter_post_controls_status`

## PASS 条件 / PASS Criteria

- 所有章节均有 control 文件。
- 所有 control 文件 `control_status=PASS`。
- 任何用户明确指出的问题已回写并修正。
