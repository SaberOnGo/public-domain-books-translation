# Literary Style Review / 文学顺读复审

status: "DRAFT" # PASS | REWORK_REQUIRED | DRAFT
target_only_reading_score:
read_aloud_sentence_count: 30
read_aloud_awkward_sentence_count:
unresolved_style_debt_count:
literal_explanatory_style_debt_count:
high_impact_sections_reviewed: false
author_preface_and_first_chapter_reviewed: false
source_fidelity_backcheck_after_polish: false

## Scope / 范围

- Review author/source prefaces, introductions, openings, and first chapters first. These sections decide whether readers keep reading.
- 先复审原作者序言、导言、开篇和首章。这些位置如果有直译腔、解释腔、平硬句，伤害比普通章节更大。
- This review is target-language-first: read the target text aloud and silently before looking at the source.
- 本复审先只看目标语：先默读、朗读，判断是否像自然成书文本，再回到原文校准忠实度。

## Findings / 发现

| file | section | issue_family | severity | action |
| --- | --- | --- | --- | --- |

## Closure / 闭环

- [ ] All stiff, literal, flat, awkward, or explanatory passages found in high-impact sections have been rewritten or justified.
- [ ] Rewritten passages were checked against the source so polish did not add meaning or alter tone.
- [ ] Recurring families were audited with low-token searches and recorded in the book QA/fix log.
- [ ] Reusable translation-quality lessons were merged into `skills/translation-quality-defect-families/SKILL.md` when applicable.

Final PASS requires `target_only_reading_score: 5`, `read_aloud_awkward_sentence_count: 0`, `unresolved_style_debt_count: 0`, `literal_explanatory_style_debt_count: 0`, `high_impact_sections_reviewed: true`, `author_preface_and_first_chapter_reviewed: true`, and `source_fidelity_backcheck_after_polish: true`.
