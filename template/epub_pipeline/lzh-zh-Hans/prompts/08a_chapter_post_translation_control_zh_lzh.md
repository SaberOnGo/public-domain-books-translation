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
