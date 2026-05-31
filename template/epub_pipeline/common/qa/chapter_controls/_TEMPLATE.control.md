# Per-Chapter Post-Translation Full Check / 每章译后全量检查模板

chapter:
status: "DRAFT"
allow_next_chapter: false
score:

## Required Scope / 必查范围

- source_fidelity / 原文忠实度：
- omissions_mistranslations_additions / 漏译误译擅自增译：
- target_language_readability / 目标语可读性：
- target_language_polish_naturalness / 目标语成稿润色与自然流畅度：
- plain_language_without_flattening / 通俗顺读但不损害专业度：
- terminology_and_source_term_display / 术语和原词呈现：
- notes_or_endnotes / 注释或章末注：
- title_nav_metadata_impact / 标题、nav、metadata 影响：
- figures_tables_formula_image_text_interface / 图表、表格、公式、图片文字接口：
- reader_visible_production_traces / 读者可见生产痕迹：

## Automated Scans / 自动扫描

- paragraph_coverage / 段落覆盖：
- naked_source_or_foreign_text_scan / 裸源语或外文扫描：
- production_trace_scan / 生产痕迹扫描：
- forbidden_term_rendering_scan / 术语禁用写法扫描：
- figure_table_formula_image_interface_scan / 图表/表格/公式/图片接口扫描：

## Issues And Fixes / 问题与处理

| priority | issue | fix | status |
|---|---|---|---|

## Rounds / 复查轮次

### round 1

- scope: "FULL_CHAPTER"
- issues_found:
- fixes_applied:
- checked_after_fix:
- unresolved_blocking_issues:
- latest_round_status:
- allow_next_chapter:

## Final Closure / 最终闭环

latest_round_status:
allow_next_chapter:

> Mandatory rule: every round must inspect the whole current chapter. If a round finds any issue and applies any fix, that round must be `FIXED_RECHECK_REQUIRED`, not `PASS`; append a new full-chapter recheck. Only a latest round with `scope: "FULL_CHAPTER"`, `issues_found: 0`, `fixes_applied: 0`, `unresolved_blocking_issues: 0`, `latest_round_status: "PASS"`, and `allow_next_chapter: true` may unlock the next chapter.
>
> 强制规则：每一轮都必须检查当前整章。若某轮发现任何问题并应用任何修复，该轮只能记为 `FIXED_RECHECK_REQUIRED`，不得记为 `PASS`；必须追加新的整章复查。只有最近一轮同时满足 `scope: "FULL_CHAPTER"`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: "PASS"`、`allow_next_chapter: true`，才允许进入下一章。
