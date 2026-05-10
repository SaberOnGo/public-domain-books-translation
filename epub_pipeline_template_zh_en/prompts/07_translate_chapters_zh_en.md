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

如果用户对该章不满意，AI 必须只回到该章重译，不得让该章继续进入后续审校。其他章节可并行继续，不必全部阻塞。

## 状态 / State

成功后：

- `status = TRANSLATED`
- `chapters_translated = 章节数`
- `current_step = chapters_translated`

注意：`TRANSLATED` 不代表可进入终稿，必须等待每章 control PASS。
