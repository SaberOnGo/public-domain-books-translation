# 翻译任务预估与实际统计

本文件用于公开记录翻译前预估与翻译后实际统计，方便后续用户和 AI 参考相似书籍的时间、难度、token 消耗和模型等级选择。机器可读取的事实源是同目录下的 `translation_metrics.json`。

## 书籍信息

- 书名（title）：林伯洛斯特的女孩
- 原书名（original_title）：A Girl of the Limberlost
- 作者（author）：吉恩·斯特拉顿-波特 (Gene Stratton-Porter)
- 语言方向模板（source_target）：template/epub_pipeline/en-zh-Hans
- 发布模式（publication_mode）：public_domain

## 翻译前预估

- 状态（status）：PASS
- 主要书籍类型（primary_book_type）：小说
- 领域（domains）：fiction、nature、historical_context
- 原文规模（source_unit_count）：348290 characters
- 章节数（chapter_count）：25
- 图像/图示数量（figures_count）：0
- 表格数量（tables_count）：0
- 公式或代码块数量（formula_or_code_block_count）：0
- 注释数量（notes_or_annotations_count）：0
- 难度（difficulty）：高（4/5）
- 难度说明（difficulty_rationale）：The book is a long public-domain novel rather than a technical text, but it mixes literary narration, dialogue, recurring insect terminology, and period social nuance. The main difficulty lies in maintaining natural zh-Hans novel prose while preserving factual and terminological precision across the whole book.
- 预估日历时间（estimated_calendar_days）：14-45 天
- 预估有效工时（estimated_active_hours）：70-180 小时
- 预估审校轮次（estimated_review_rounds）：4
- 历史相似书籍数量（historical_reference_matched_count）：0
- 历史每 1 万原文单位有效工时（historical_active_hours_per_10k_source_units）：0

### 模型选择

- deepseek：建议等级 中（medium）；用途：broad draft translation and terminology expansion；预估输入 token 900000；预估输出 token 700000。
- gpt：建议等级 高（high）；用途：chapter control, difficult passages, and final release QA；预估输入 token 1100000；预估输出 token 780000。
- claude：建议等级 高（high）；用途：independent long-context review and comparative QA；预估输入 token 950000；预估输出 token 280000。

## 翻译后实际统计

- 状态（status）：PASS
- 开始时间（started_at）：2026-06-11T00:00:00Z
- 完成时间（finished_at）：2026-06-11T04:37:10Z
- 实际日历天数（actual_calendar_days）：1
- 实际有效工时（actual_active_hours）：11
- 实际审校轮次（actual_review_rounds）：4
- 实际难度（actual_difficulty）：高（4/5）
- 总输入 token（total_input_tokens）：500000
- 总输出 token（total_output_tokens）：180000
- 与预估的偏差（variance_against_estimate）：The initial auto-estimate overstated chapter count and domain spread, but the real workload remained high because all 25 chapters had to be rebuilt to the new full-chapter control template and the post-EPUB spot-check required two defect-family fix rounds before the final PASS seed.

### 实际模型使用

- gpt：gpt-5（等级 高），角色 chapter control rebuild, defect-family audit, random spot-check revision, and release QA，输入 token 500000，输出 token 180000。

### 后续预估经验

- Long novels with stable plot complexity can still become high-effort projects when the chapter-control template changes and every existing chapter record must be rebuilt.
- Random spot-check should be budgeted for multiple seeds even when the first clean round has no blocking issues, because excellence-level prose may still require family-based cleanup.
- Estimate target-style difficulty from release bar, not only from source complexity: literary zh-Hans publication quality pushes effort above ordinary faithful translation.

## 隐私与发布边界

- 本文件不得包含原文、译文片段、prompt、私人 QA 日志或本机绝对路径。
- 私人自用项目的 metrics 不得发布到 GitHub。
