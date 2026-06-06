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
- 标题人名检查结果：章节标题/副标题/目录题名只使用中文译名或本书确定的中文呈现方式；标题中的人名不计入“正文首次出现”；日文原名、读音或括注只出现在正文第一次自然出现处、译注、术语表或书籍信息页。
- 日语底本文字形态检查结果：本章若涉及振假名、旧字、注记、OCR 疑难或异读，已和 `qa/textual/japanese_textual_notes.md` 对齐。
- 官能、暴力、病态心理或强制关系边界检查结果。
- 是否有人类反馈。
- 是否需要回到本章重译。
- 关键修改项。
- 最终 PASS/FAIL。

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

## 并行 / Parallelism

章节可并行翻译、并行控制。每章 control 文件互不覆盖。

## 输出 / Output

- `qa/chapter_controls/{NNN_slug}.control.md`
- `state/pipeline_state.json.quality_gate.chapter_post_controls_status`

## PASS 条件 / PASS Criteria

- 所有章节均有 control 文件。
- 所有 control 文件 `control_status=PASS`。
- 不存在把日文原名、读音、罗马字或解释性括注塞进章节标题、副标题或目录题名的情况。
- 任何用户明确指出的问题已回写并修正。
