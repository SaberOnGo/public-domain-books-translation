# 翻译任务预估与实际统计

本文件用于公开记录翻译前预估与翻译后实际统计，方便后续用户和 AI 参考相似书籍的时间、难度、token 消耗和模型等级选择。机器可读取的事实源是同目录下的 `translation_metrics.json`。

## 书籍信息

- 书名（title）：甲虫
- 原书名（original_title）：The Beetle: A Mystery
- 作者（author）：Richard Marsh
- 语言方向模板（source_target）：template/epub_pipeline/English-to-Simplified-Chinese
- 发布模式（publication_mode）：public_domain

## 翻译前预估

- 状态（status）：PASS
- 主要书籍类型（primary_book_type）：小说
- 领域（domains）：fiction、history、programming、science、language_learning、philosophy
- 原文规模（source_unit_count）：231569 words
- 章节数（chapter_count）：48
- 图像/图示数量（figures_count）：0
- 表格数量（tables_count）：0
- 公式或代码块数量（formula_or_code_block_count）：1
- 注释数量（notes_or_annotations_count）：0
- 难度（difficulty）：高（4/5）
- 难度说明（difficulty_rationale）：Primary detected type is fiction; secondary types: history, programming, science, language_learning, philosophy. Source size is 231569 words; chapter_count=2. Detected figures=0, tables=0, formula_or_code_blocks=1, notes=0. Named-entity density is high.
- 预估日历时间（estimated_calendar_days）：28-76 天
- 预估有效工时（estimated_active_hours）：136-228 小时
- 预估审校轮次（estimated_review_rounds）：4
- 历史相似书籍数量（historical_reference_matched_count）：0
- 历史每 1 万原文单位有效工时（historical_active_hours_per_10k_source_units）：0

### 模型选择

- deepseek：建议等级 中（medium）；用途：low-cost first-pass translation, terminology expansion, and broad chapter drafts；预估输入 token 609500；预估输出 token 478900。
- gpt：建议等级 高（high）；用途：final-quality translation, difficult passages, polysemy checks, and release-facing QA；预估输入 token 740100；预估输出 token 522400。
- claude：建议等级 高（high）；用途：long-context consistency review, style comparison, and independent QA；预估输入 token 653000；预估输出 token 195900。

## 翻译后实际统计

- 状态（status）：PASS
- 开始时间（started_at）：2026-06-26T15:37:28Z
- 完成时间（finished_at）：2026-06-26T19:05:00Z
- 实际日历天数（actual_calendar_days）：1
- 实际有效工时（actual_active_hours）：9
- 实际审校轮次（actual_review_rounds）：50
- 实际难度（actual_difficulty）：高（4/5）
- 总输入 token（total_input_tokens）：1500000
- 总输出 token（total_output_tokens）：620000
- 与预估的偏差（variance_against_estimate）：Actual wall-clock execution was shorter than the conservative pretranslation estimate because the run used a single high-tier agent, deterministic gates, and narrow chapter-control batches; active effort remained high due to 48 full-chapter controls, EPUB/Digest generation, and two random spot-check PASS rounds.

### 实际模型使用

- openai：GPT-5 Codex（等级 高），角色 full translation, per-chapter control, EPUB production, Digest, and release QA，输入 token 1500000，输出 token 620000。

### 后续预估经验

- Long Gothic novels with many short chapters need per-chapter control overhead that can dominate final QA even when terminology density is moderate.
- Existing English-to-Simplified-Chinese templates and deterministic coverage gates reduce setup time, but release still needs explicit cover, book-info, asset, Digest, random-review, and metrics closure.
- Future estimates should count post-EPUB random review and release metrics as separate production work, not as part of translation drafting.

## 隐私与发布边界

- 本文件不得包含原文、译文片段、prompt、私人 QA 日志或本机绝对路径。
- 私人自用项目的 metrics 不得发布到 GitHub。
