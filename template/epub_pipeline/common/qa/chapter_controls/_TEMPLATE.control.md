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
- high_impact_opening_section / 原作者序言、导言、开篇或首章：
- literal_explanatory_style_debt / 直译腔、解释腔、平硬句债务：
- expert_translation_quality / 专家级译文质量：
- polysemy_translation_stage_handling / 翻译阶段多义词主动处理：
- polysemy_context_backcheck / 多义词上下文回看：
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
- expert_translation_skill_used:
- expert_translation_skill_path: "skills/expert-translation-quality/SKILL.md"
- high_impact_opening_section:
- target_only_reading_score:
- read_aloud_sentence_count:
- read_aloud_awkward_sentence_count:
- literal_explanatory_style_debt_count:
- expert_level_review_status:
- polysemy_translation_stage_review:
- polysemy_context_review:
- polysemy_watchlist_count:
- polysemy_revisited_count:
- polysemy_unresolved_count:
- issues_found:
- fixes_applied:
- checked_after_fix:
- unresolved_blocking_issues:
- latest_round_status:
- allow_next_chapter:

## Final Closure / 最终闭环

latest_round_status:
allow_next_chapter:
expert_translation_skill_used:
high_impact_opening_section:
target_only_reading_score:
read_aloud_awkward_sentence_count:
literal_explanatory_style_debt_count:
expert_level_review_status:
polysemy_translation_stage_review:
polysemy_context_review:
polysemy_unresolved_count:

> Mandatory rule: every round must inspect the whole current chapter. If a round finds any issue and applies any fix, that round must be `FIXED_RECHECK_REQUIRED`, not `PASS`; append a new full-chapter recheck. Only a latest round with `scope: "FULL_CHAPTER"`, `issues_found: 0`, `fixes_applied: 0`, `unresolved_blocking_issues: 0`, `latest_round_status: "PASS"`, and `allow_next_chapter: true` may unlock the next chapter.
>
> 强制规则：每一轮都必须检查当前整章。若某轮发现任何问题并应用任何修复，该轮只能记为 `FIXED_RECHECK_REQUIRED`，不得记为 `PASS`；必须追加新的整章复查。只有最近一轮同时满足 `scope: "FULL_CHAPTER"`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: "PASS"`、`allow_next_chapter: true`，才允许进入下一章。
>
> Expert/polysemy rule: a PASS round must also record `expert_translation_skill_used: true`, `expert_level_review_status: "PASS"`, `polysemy_translation_stage_review: "PASS"`, `polysemy_context_review: "PASS"`, and `polysemy_unresolved_count: 0`. If locally decidable polysemy was deferred to review, or downstream context changes an earlier word choice, the fix round is `FIXED_RECHECK_REQUIRED`; only the next full-chapter recheck can PASS.
>
> 专家级/多义词规则：PASS 轮还必须记录 `expert_translation_skill_used: true`、`expert_level_review_status: "PASS"`、`polysemy_translation_stage_review: "PASS"`、`polysemy_context_review: "PASS"` 和 `polysemy_unresolved_count: 0`。如果局部上下文已能判清的多义词被推给审校，或后文语境改变了前文选义，修复轮只能记为 `FIXED_RECHECK_REQUIRED`；只有下一轮整章复查可 PASS。
>
> Opening rule: author/source prefaces, introductions, openings, and first chapters must set `high_impact_opening_section: true` and close `literal_explanatory_style_debt_count: 0`. These sections cannot PASS with stiff, literal, flat, awkward, or explanatory prose because they decide whether readers keep reading.
>
> 开篇规则：原作者/原书序言、导言、开篇和首章必须记录 `high_impact_opening_section: true`，并关闭 `literal_explanatory_style_debt_count: 0`。这些位置不允许带着不顺口、直译感、平硬句、怪句或解释腔 PASS，因为它们决定读者是否继续读下去。
