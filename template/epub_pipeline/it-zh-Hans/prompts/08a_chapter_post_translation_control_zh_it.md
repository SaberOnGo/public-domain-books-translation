# 08a 每章译后全量控制

每章译入 `chapters/translated/` 后立即停止翻译下一章，只针对当前章执行完整质量门禁。

必须对照整章原文逐段检查，并在 `qa/chapter_controls/{chapter}.control.md` 中留下可复核证据：

- 忠实度、漏译、误译、擅自增译。
- 中文可读性、长句重组、动作链、对话节奏、成稿级润色和自然流畅度。译文应尽量读得顺、有趣、不费劲，但不得为了通俗化而损害专名、术语、历史语境、叙事水准和原书风格。
- 术语与原词呈现、殖民时代称谓、地名、船名、头衔、宗教和族群词。
- 标题、nav、TOC、metadata 影响。
- 注释/译注需求。
- 图表、图片、表格、公式、caption、alt text 和正文引用接口。
- 读者可见生产痕迹。
- 段落覆盖、裸外文、术语禁用写法和生产痕迹自动扫描结果。

每一轮都必须是当前章的全量检查，不得只复查上一轮问题点。发现任何问题后必须先修复，但该轮只能记录为 `FIXED_RECHECK_REQUIRED`，不得直接 PASS；随后必须追加一轮新的整章全量检查。只有最后一轮记录 `scope: "FULL_CHAPTER"`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: "PASS"`、`allow_next_chapter: true`，才可继续下一章。
