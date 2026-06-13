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

- 本章译后全量检查结果，必须覆盖当前整章，不得只检查抽样段落、上一轮问题点或用户点名项目。
- 日译中忠实度、漏译、误译、无依据增译。
- 中文可读性、成稿级润色、自然流畅度、叙述节奏和通俗顺读；译文应尽量读得顺、有趣、不费劲，但不得为了通俗化而损害专业术语、概念层级、叙事风格或原书专业水准。
- 标题人名检查结果：章节标题/副标题/目录题名只使用中文译名或本书确定的中文呈现方式；标题中的人名不计入“正文首次出现”；日文原名、读音或括注只出现在正文第一次自然出现处、译注、术语表或书籍信息页。
- 日语底本文字形态检查结果：本章若涉及振假名、旧字、注记、OCR 疑难或异读，已和 `qa/textual/japanese_textual_notes.md` 对齐。
- 官能、暴力、病态心理或强制关系边界检查结果。
- 是否有人类反馈。
- 是否需要回到本章重译。
- 每一轮发现的问题、修复项、复查结论、总分和是否允许进入下一章。
- 最终 `latest_round_status` 与 `allow_next_chapter`。

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

## 轮次闭环 / Round Closure

每一轮都必须是当前章全量检查。发现任何问题后必须先修复，但该轮只能记录为 `FIXED_RECHECK_REQUIRED`，不得直接 PASS；随后必须追加一轮新的整章全量检查。若新一轮仍发现问题，继续修复并追加下一轮。

最后一轮必须同时记录：

```text
scope: "FULL_CHAPTER"
issues_found: 0
fixes_applied: 0
unresolved_blocking_issues: 0
latest_round_status: "PASS"
allow_next_chapter: true
```

存在 control 文件、readability 文件或 gate 文件，不等于通过门禁。

## 串行优先 / Sequential Closure

默认逐章闭环。上一章未达到上述最后一轮零问题 PASS 时，不得进入下一章翻译。只有项目明确批准并行批处理时，才可并行处理不同章节；即便并行，每章也必须独立零问题 PASS 后才可进入后续流程。

## 输出 / Output

- `qa/chapter_controls/{NNN_slug}.control.md`
- `state/pipeline_state.json.quality_gate.chapter_post_controls_status`

## PASS 条件 / PASS Criteria

- 当前章有 control 文件。
- 最近一轮记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true`。
- 若上一轮发现并修复过任何问题，已经追加新的整章复查轮次，而不是把修复轮直接标为 PASS。
- 不存在把日文原名、读音、罗马字或解释性括注塞进章节标题、副标题或目录题名的情况。
- 任何用户明确指出的问题已回写并修正。
