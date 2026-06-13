# 翻译任务预估与实际统计

本文件用于公开记录翻译前预估与翻译后实际统计，方便后续用户和 AI 参考相似书籍的时间、难度、token 消耗和模型等级选择。机器可读取的事实源是同目录下的 `translation_metrics.json`。

## 书籍信息

- 书名（title）：云使
- 原书名（original_title）：मेघदूतम्
- 作者（author）：迦梨陀娑
- 语言方向模板（source_target）：template/epub_pipeline/sa-zh-Hans
- 发布模式（publication_mode）：public_domain

## 翻译前预估

- 状态（status）：PASS
- 主要书籍类型（primary_book_type）：语言学习
- 领域（domains）：language_learning、history、fiction、programming、science
- 原文规模（source_unit_count）：26167 words
- 章节数（chapter_count）：4
- 图像/图示数量（figures_count）：0
- 表格数量（tables_count）：3
- 公式或代码块数量（formula_or_code_block_count）：1
- 注释数量（notes_or_annotations_count）：0
- 难度（difficulty）：高（4/5）
- 难度说明（difficulty_rationale）：Primary detected type is language_learning; secondary types: history, fiction, programming, science. Source size is 26167 words; chapter_count=4. Detected figures=0, tables=3, formula_or_code_blocks=1, notes=0. Named-entity density is very_high.
- 预估日历时间（estimated_calendar_days）：4-10 天
- 预估有效工时（estimated_active_hours）：17-29 小时
- 预估审校轮次（estimated_review_rounds）：4
- 历史相似书籍数量（historical_reference_matched_count）：1
- 历史每 1 万原文单位有效工时（historical_active_hours_per_10k_source_units）：0.32

### 模型选择

- deepseek：建议等级 中（medium）；用途：low-cost first-pass translation, terminology expansion, and broad chapter drafts；预估输入 token 68900；预估输出 token 54100。
- gpt：建议等级 高（high）；用途：final-quality translation, difficult passages, polysemy checks, and release-facing QA；预估输入 token 83600；预估输出 token 59000。
- claude：建议等级 高（high）；用途：long-context consistency review, style comparison, and independent QA；预估输入 token 73800；预估输出 token 22100。

## 翻译后实际统计

- 状态（status）：PASS
- 开始时间（started_at）：2026-06-13T07:20:00Z
- 完成时间（finished_at）：2026-06-13T08:05:00Z
- 实际日历天数（actual_calendar_days）：1
- 实际有效工时（actual_active_hours）：1.0
- 实际审校轮次（actual_review_rounds）：2
- 实际难度（actual_difficulty）：高（4/5）
- 总输入 token（total_input_tokens）：90000
- 总输出 token（total_output_tokens）：45000
- 与预估的偏差（variance_against_estimate）：Actual local execution was shorter than the heuristic estimate because the selected work is a short lyric poem; the estimator over-counted preserved OCR/witness files as source units.

### 实际模型使用

- openai：gpt-5-codex（等级 高），角色 translation, chapter controls, EPUB QA, random review synthesis，输入 token 90000，输出 token 45000。

### 后续预估经验

- For short Sanskrit poems, count clean verse units separately from preserved OCR, witness, and metadata files.
- Poetry difficulty is driven by compound resolution, imagery chains, route fidelity, and restrained notes more than by raw word count.
- Digest should remain disabled for short lyric poems even when the source language is difficult.

## 隐私与发布边界

- 本文件不得包含原文、译文片段、prompt、私人 QA 日志或本机绝对路径。
- 私人自用项目的 metrics 不得发布到 GitHub。
