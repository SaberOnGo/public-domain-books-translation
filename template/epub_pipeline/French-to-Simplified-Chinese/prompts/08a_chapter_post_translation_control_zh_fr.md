# 08a 每章译后全量控制

每个 canonical 章节 patch 合并后，立即只针对当前章执行完整质量门禁。失败章不得进入下游；合同锁定后，其他独立 owner 的章节可按自适应计划继续。

必须对照整章原文逐段检查，并在 `qa/chapter_controls/{chapter}.control.md` 中留下可复核证据：

- 忠实度、漏译、误译、擅自增译。
- 中文可读性、长句重组、抽象名词链、成稿级润色和自然流畅度。必须消除法语句法残留、生硬搭配、不必要重复、翻译腔和不协调的书面语；不能只做到“意思看得懂”。译文应尽量读得顺、有趣、不费劲，但不得为了通俗化而损害专业术语、概念层级、论证水准和原书专业风格。
- 术语与原词呈现、历史术语、旧科学框架、专名。
- 标题、nav、TOC、metadata 影响。
- 注释/译注需求。
- 图表、图片、表格、公式、caption、alt text 和正文引用接口。
- 读者可见生产痕迹。
- 段落覆盖、裸外文和生产痕迹自动扫描结果。

每一轮都必须是当前章的全量检查，不得只复查上一轮问题点。发现任何问题后必须先修复，但该轮只能记录为 `FIXED_RECHECK_REQUIRED`，不得直接 PASS；随后必须追加一轮新的整章全量检查。若新一轮仍发现问题，继续修复并追加下一轮，直到最后一轮整章检查没有发现任何问题。

存在 control 文件、readability 文件或 gate 文件，不等于通过门禁。只有最后一轮为“全量检查零问题”，并记录 `scope: "FULL_CHAPTER"`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: "PASS"`、`allow_next_chapter: true`，且不存在未关闭的 P0/P1/P2、读者理解障碍、事实/术语错误、文字接口错误、明显中文翻译腔或为了通俗而损害专业度的问题时，才可继续下一章。

## 专家级与多义词回看 / Expert Quality and Polysemy Back-Check

本节点必须使用 `skills/expert-translation-quality/SKILL.md`。翻译阶段是多义词处理的第一责任节点；08a 负责审计该责任是否已经执行。后文已译出后，必须回看当前章前文的多义词、习语、称谓、术语和依赖上下文判义的语法结构。若发现译文把局部上下文已能判清的选义推给后续审校，该轮不能 PASS。`qa/chapter_controls/{chapter}.control.md` 的最近 PASS 轮必须记录：

```text
expert_translation_skill_used: true
expert_translation_skill_path: "skills/expert-translation-quality/SKILL.md"
expert_level_review_status: "PASS"
polysemy_translation_stage_review: "PASS"
polysemy_context_review: "PASS"
polysemy_watchlist_count: {number_checked}
polysemy_revisited_count: {number_revisited}
polysemy_unresolved_count: 0
```

若回看后修正了前文选义，该轮只能记为 `FIXED_RECHECK_REQUIRED`，必须追加新的整章复查轮才可 PASS。
