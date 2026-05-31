---
name: classical-history-zh-Hans
description: Use this profile after a language-pair EPUB template when translating ancient historical, chronicle, biography, diplomacy, warfare, ritual, or name-heavy works into Simplified Chinese.
---

# 古代历史简体中文 EPUB 控制流程 / Classical History EPUB Control Workflow

## 何时使用 / When to Use

当一本书具有以下任一特征时，使用本 profile：

- 春秋战国、秦汉或其他古代历史叙事。
- 人物、国名、地名、官名、爵位、宗族、使节、战争或外交关系密集。
- 年代、事件顺序、会盟、朝聘、游说、策反、礼制背景会影响理解。
- 注释密度明显高于普通文学翻译。

Use this profile for ancient historical prose where people, states, chronology, institutions, diplomacy, warfare, and annotation control are publication blockers.

## 必须叠加的目录 / Required Overlay

```text
common -> {source-target} -> profiles/classical-history-zh-Hans -> books/zh-Hans/{number}_{book_id_slug}/
```

## 执行步骤 / Workflow

在语言方向模板的主流程中插入：

1. `prompts/00_profile_integration_zh_Hans.md`
2. `prompts/04a_historical_context_zh_Hans.md`
3. `prompts/06a_named_entity_lock_zh_Hans.md`
4. `prompts/08b_chapter_historical_audit_zh_Hans.md`
5. `prompts/16b_history_random_spotcheck_zh_Hans.md`

## 必要记录 / Required Records

- `metadata/historical_context.md`
- `glossary/historical_terms.csv`
- `glossary/people_places.csv`
- `qa/historical/event_timeline.md`
- `qa/historical/state_relations_matrix.csv`
- `qa/historical/{chapter}.historical_audit.md`
- `reviews/scorecards/_TEMPLATE_history_scorecard.md`

## PASS 标准 / Pass Standard

- 核心人物、国家、官名、地名和时间线已锁定。
- 章节历史审计没有未关闭 P0/P1/P2。
- 注释既足够防误读，又没有把正文压成百科。
- 随机抽检对人物、国家关系、年代、制度和注释独立检查。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <70、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.
