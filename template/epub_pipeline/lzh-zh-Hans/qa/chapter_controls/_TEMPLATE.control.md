# 章节译后控制 / Chapter Post-Translation Control

control_status: "DRAFT" # DRAFT | PASS | FAIL
latest_round_status: "AUTO_PENDING" # AUTO_PENDING | FIXED_RECHECK_REQUIRED | PASS
scope: "FULL_CHAPTER"
issues_found:
fixes_applied:
unresolved_blocking_issues:
allow_next_chapter: false

## Chapter

- chapter_id:
- source_range:
- translated_file:

## Source-Modern Alignment / 原文-今译对齐

| passage_id | source_start | source_end | modern_translation_present | notes_present | alignment_status |
| --- | --- | --- | --- | --- | --- |

## Risk Review / 风险复查

- 断句/标点疑难：
- 人物/地名/国名：
- 官名/爵位/制度：
- 古今词义：
- 省略关系：
- 语气/讽刺/外交辞令：
- 今译中文成稿润色与自然流畅度：
- 通俗顺读但不损害制度术语、史料口吻和专业水准：
- 注释必要性：
- 不应进入读者正文的校勘或制作说明：

## PASS Criteria

- 每个古文 passage 都有对应现代译文。
- 今译未省略关键事实、人物关系、否定、因果和语气。
- 必要注释已补足；非必要注释未压迫阅读。
- 文本疑难已同步到 `qa/textual/classical_chinese_textual_notes.md`。
- 最近一轮记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true`。
- 发现并修复问题的轮次没有直接 PASS，而是记录为 `FIXED_RECHECK_REQUIRED` 并追加新的整章复查。
- 本章可进入忠实度、可读性和术语审校。

> 强制规则：存在本文件不等于通过门禁。发现任何问题并修复的轮次只能记为 `FIXED_RECHECK_REQUIRED`，不得直接 PASS。只有最后一轮全章复查 `issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`，且 `latest_round_status: "PASS"`、`allow_next_chapter: true` 时，才可继续下一章。
