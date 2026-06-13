# 章节译后全量控制模板

chapter:
status: "DRAFT"
allow_next_chapter: false
score:

## 检查范围

- 忠实度：
- 中文可读性：
- 中文成稿润色与自然流畅度：
- 西班牙语长句和插入语处理：
- 一人称自述、讽刺距离和叙述者自辩：
- 术语、专名和原词呈现：
- 宗教、阶层、称谓、食物、货币和旧制度语境：
- 注释/译注：
- 标题/nav/metadata 影响：
- 图表/图片/表格/公式文字接口：
- 读者可见生产痕迹：
- expert_translation_skill_used:
- expert_translation_skill_path: "skills/expert-translation-quality/SKILL.md"
- expert_level_review_status:
- polysemy_translation_stage_review:
- polysemy_context_review:
- polysemy_watchlist_count:
- polysemy_revisited_count:
- polysemy_unresolved_count:

## 本轮自动扫描

- 段落覆盖：
- 裸外文扫描：
- 生产痕迹扫描：
- 图表/图片/表格/公式接口扫描：
- `glossary/terms.csv.forbidden_body_renderings` 扫描：

## 问题与处理

| priority | issue | fix | status |
|---|---|---|---|

## 复查轮次

- round:
- scope: "FULL_CHAPTER"
- issues_found:
- fixes_applied:
- checked_after_fix:
- unresolved_blocking_issues:

## 结论

latest_round_status:
allow_next_chapter:

> 强制规则：存在本文件不等于通过门禁。每一轮都必须对照整章原文完成全量检查，并逐段执行中文成稿润色。译文应尽量读得顺、有趣、不费劲，但不能为了通俗化而损害专名、术语、历史语境、叙事水准和原书风格。发现任何问题后先修正文或读者可见接口，但该轮只能记为 `FIXED_RECHECK_REQUIRED`；必须追加一轮新的整章全量检查。只有最后一轮 `scope: "FULL_CHAPTER"`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: "PASS"`、`allow_next_chapter: true` 时，才可继续下一章。
