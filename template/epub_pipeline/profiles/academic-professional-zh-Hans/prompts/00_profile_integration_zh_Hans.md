# 00 Profile 插入规则 / Profile Integration Rules

## 目的

本文件说明 `academic-professional-zh-Hans` 如何叠加到任意语言方向模板上。

This profile adds academic/professional readability controls to a language-pair EPUB pipeline. It does not replace the language-pair prompts.

## 插入点

| 语言方向阶段 | 本 profile 追加阶段 | 必须产物 |
| --- | --- | --- |
| `04_book_specific_research` 后 | `04a_academic_professional_style_profile` | `metadata/academic_professional_style_profile.md` |
| `06_glossary_style` 后 | `06a_domain_term_readability_lock` | 术语锁定表或本书 glossary；不得为了通俗随意换译 |
| 每章翻译后 | `08b_chapter_academic_readability_review` | `qa/readability/{NNN_slug}.academic_readability_audit.md` |
| 第一版全书 EPUB 后 | `16a_stratified_random_spotcheck` with academic profile | `reviews/random_spotcheck/round_XXX/`，使用 `--profile auto` 或 `--profile academic` |
| 最终独立评审 | academic/professional scorecard | `reviews/scorecards/final_academic_professional_score.md` |

## 状态规则

- 任一逐章 academic readability audit 为 `FAIL` 时，不得进入最终 EPUB 输出。
- 任一术语、公式、图表、统计解释因“通俗化”而失真，必须按 P1/P2 处理。
- 任一读者不可理解的专业段落，必须按 P2 或更高处理。
- P3 可以保留，但必须说明为什么“不够轻松”仍不影响理解或专业准确性。

## 与其他 profile 的关系

本 profile 可以同 `classical-science-zh-Hans` 或 `classical-history-zh-Hans` 叠加。若同时启用：

- 科学/历史 profile 负责事实、术语、图表、数值、人物和时间线硬门禁。
- 本 profile 负责让专业解释和章节叙述在中文中可跟、可读。
- 冲突时先保事实与专业精度，再修中文表达。
