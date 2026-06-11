# Translation Effort Metrics Policy / 翻译任务预估与实际统计规则

policy_status: "ACTIVE"
scope: "public-domain or licensed publication projects / 公版或授权发布项目"

## Purpose / 目的

Every public release should preserve a publishable record of the translation estimate and the actual outcome. Future users and AI agents can then compare similar books by type, length, structural complexity, difficulty, model tier, token use, review effort, and time.

每个公开发布项目都应保存一份可发布的翻译任务记录。后续用户和 AI 可以据此按书籍类型、篇幅、结构复杂度、难度、模型等级、token 使用量、评审工作量和时间，对类似书籍做快速预估。

## Required Files / 必备文件

Public projects write the records under:

```text
output/release/translation_metrics.json
output/release/translation_metrics.md
```

`translation_metrics.json` is the AI-readable source of truth. `translation_metrics.md` is the GitHub-readable human summary.

Generated Markdown summaries such as `translation_metrics.md` and `translation_difficulty_assessment.md` are human-facing release files. They must use the target contributor language first, with English field keys kept only as stable machine-readable hints when useful. For Simplified Chinese projects, Chinese-only or Chinese-primary output is acceptable and does not reduce AI readability because AI agents should read the structured JSON as the source of truth.

自动生成的 Markdown 摘要（例如 `translation_metrics.md` 和 `translation_difficulty_assessment.md`）属于面向人的 release 文件，必须以目标贡献者语言为主；英文 key 只作为稳定的机器提示保留即可。对简体中文项目，全中文或中文优先输出都是允许的，不会降低 AI 可读性，因为 AI 应以结构化 JSON 作为事实源。

`translation_metrics.json` 是 AI 可读取的事实源；`translation_metrics.md` 是面向 GitHub 用户的人类可读摘要。

## Module Boundary / 模块边界

This feature is intentionally isolated from the main EPUB production policies.

本功能刻意作为独立模块维护，不把完整规则塞进封面、前置页、release 或 AGENTS 等已有文档。

Authoritative files:

- `template/epub_pipeline/common/references/translation_effort_metrics.md`: policy and schema contract.
- `template/epub_pipeline/common/scripts/evaluate_translation_difficulty.py`: pre-translation multidimensional difficulty evaluator.
- `template/epub_pipeline/common/scripts/update_translation_metrics.py`: metrics initializer, renderer, and release-gate validator.

Book-local npm commands:

```powershell
npm run metrics:evaluate
npm run metrics:init
npm run metrics:validate
npm run metrics:validate:actual
```

## Pre-Translation Estimate / 翻译前预估

Before full-book translation starts, create the metrics draft:

```powershell
npm run metrics:evaluate
```

`metrics:evaluate` scans the current book project, writes `output/release/translation_difficulty_assessment.json`, `output/release/translation_difficulty_assessment.md`, and updates the pre-translation estimate inside `output/release/translation_metrics.json`.

`metrics:evaluate` 会扫描当前书籍工程，输出 `output/release/translation_difficulty_assessment.json`、`output/release/translation_difficulty_assessment.md`，并同步更新 `output/release/translation_metrics.json` 中的翻译前预估字段。

If the source material is not yet present in the project, run `npm run metrics:init` to create an empty metrics draft, then run `npm run metrics:evaluate` after source ingestion.

预估必须先分析书本身，而不是只按 token 粗略估算。至少记录：

- `primary_book_type`: such as fiction, history, philosophy, programming, language learning, science, mathematics, biography, poetry, drama, religious text, legal text, or mixed.
- `domains`: subject domains, for example classical history, political theory, astronomy, software engineering, linguistics, literary fiction, or ethics.
- `source_unit_count`: characters, words, pages, or another recorded source unit.
- `chapter_count`.
- `figures_count`, `tables_count`, `formula_or_code_block_count`, `notes_or_annotations_count`.
- `requires_external_research`, `requires_table_or_figure_reconstruction`, `requires_formula_or_code_validation`, `requires_historical_or_philosophical_context`.
- `difficulty_components_1_to_5`: source-language complexity, domain knowledge load, terminology density, argument or plot complexity, historical context, philosophical or theoretical density, technical code or formula load, figures/tables/formulas, target style difficulty, annotation/cross-reference load.
- `difficulty_level` and `difficulty_score_1_to_5`, with `difficulty_rationale`.
- time estimate: calendar days, active hours, and expected review rounds.
- model recommendations for at least DeepSeek, GPT, and Claude, using model tiers `low`, `medium`, `high`, or `very_high`.

The model recommendation must explain when a cheaper model is enough and when a higher-tier model is justified. It must not hard-code provider prices unless they were verified for the current date and recorded separately.

模型建议必须说明什么时候低成本模型足够，什么时候需要更高等级模型。除非已按当前日期核验并另行记录，不要把供应商价格写死在模板中。

## Post-Translation Actuals / 翻译后实际统计

After translation, review, random spot-check, and final release gates are closed, fill `post_translation_actual` and mark it `PASS`.

实际统计至少记录：

- start and finish timestamps.
- actual calendar days and active hours.
- actual review rounds.
- actual difficulty level and score.
- models used, provider, model name, model tier, role, input tokens, and output tokens.
- total input and output tokens.
- random spot-check score summary and release confidence.
- variance against the estimate.
- lessons for future estimates.

## Release Gate / 发布门禁

`npm run release:create` must reject a PASS public release unless:

- `output/release/translation_metrics.json` exists.
- `pretranslation_estimate.status = "PASS"`.
- `post_translation_actual.status = "PASS"`.
- privacy flags confirm that the metrics contain no source text, prompt text, or local absolute paths.

The release script copies the metrics summary into `output/release/release_state.json.gate_summary` and into the latest `release_notes.md` entry.

## Privacy and Rights / 隐私与权利边界

Metrics are publishable only when they contain aggregate production facts. They must not include:

- source text excerpts.
- translation passages.
- prompt text.
- private QA logs.
- local absolute paths.
- private-use source filenames beyond what the private-use policy explicitly allows locally.

For `publication_mode=private_use`, do not publish metrics to GitHub. Private-use statistics may be kept only in the ignored private project if the user wants local estimation history.

## Examples / 示例

Difficulty examples:

- A short plain-language public-domain novel with few names and no notes may be `medium`, even when the source length is large.
- A historical work with many places, offices, dynasties, chronology chains, and annotation decisions may be `high` or `very_high`.
- A philosophy book may become `very_high` because argument structure, term consistency, and conceptual density dominate the work, even without figures.
- A programming book may be `high` or `very_high` when code blocks, API names, version-specific behavior, and runnable examples require validation.
- A science or mathematics book with formulas, tables, diagrams, and numeric checks usually needs a high structural QA budget even if the prose is short.

示例说明：难度不是单纯由字数决定。历史、哲学、编程、科学、小说等类型的成本来源不同，预估必须把这些因素拆开记录。
