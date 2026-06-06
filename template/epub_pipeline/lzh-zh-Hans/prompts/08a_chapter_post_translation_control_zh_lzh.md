# 08a 章节译后控制 / Chapter Post-Translation Control

## 输入

- `chapters/src/{chapter}.md`
- `chapters/translated/{chapter}.md`

## 任务

创建 `qa/chapter_controls/{chapter}.control.md`，检查：

1. 当前整章古文是否都有对应今译，不得只抽样。
2. passage id 是否稳定。
3. 注释是否存在必要项，注释密度是否压迫阅读。
4. 疑难断句、异文、人物关系是否同步记录。
5. 是否出现现代版权译文或现代校注表达残留。
6. 今译是否忠实、完整、通顺，是否有现代中文成稿级润色和自然流畅度。
7. 今译是否尽量读得顺、有趣、不费劲；但不得为了通俗化而损害古文语义、制度术语、人物关系、外交辞令、史料口吻或专业水准。
8. 是否存在为了“白话好懂”而把古文中的制度名、官名、爵位、礼制、地名和历史语境泛化、改扁或改错。

## 轮次闭环

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

## 结果

- 只有最近一轮零问题 PASS 后才能进入忠实度审校或下一章。
- 发现并修复问题的轮次不能 PASS，必须追加新的整章复查。
- `control_status: FAIL` 或 `latest_round_status: FIXED_RECHECK_REQUIRED` 时必须回到本章翻译/修订。

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
