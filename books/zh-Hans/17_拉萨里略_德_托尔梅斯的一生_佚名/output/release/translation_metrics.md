# 翻译任务预估与实际统计

本文件用于公开记录翻译前预估与翻译后实际统计，方便后续用户和 AI 参考相似书籍的时间、难度、token 消耗和模型等级选择。机器可读取的事实源是同目录下的 `translation_metrics.json`。

## 书籍信息

- 书名（title）：拉萨里略·德·托尔梅斯的一生
- 原书名（original_title）：La vida de Lazarillo de Tormes
- 作者（author）：佚名
- 语言方向模板（source_target）：template/epub_pipeline/es-zh-Hans
- 发布模式（publication_mode）：public_domain

## 翻译前预估

- 状态（status）：PASS
- 主要书籍类型（primary_book_type）：历史
- 领域（domains）：history、philosophy、fiction、science、programming
- 原文规模（source_unit_count）：56226 characters
- 章节数（chapter_count）：18
- 图像/图示数量（figures_count）：0
- 表格数量（tables_count）：0
- 公式或代码块数量（formula_or_code_block_count）：1
- 注释数量（notes_or_annotations_count）：0
- 难度（difficulty）：高（4/5）
- 难度说明（difficulty_rationale）：Primary detected type is history; secondary types: philosophy, fiction, science, programming. Source size is 56226 characters; chapter_count=18. Detected figures=0, tables=0, formula_or_code_blocks=1, notes=0. Named-entity density is very_high.
- 预估日历时间（estimated_calendar_days）：7-19 天
- 预估有效工时（estimated_active_hours）：34-57 小时
- 预估审校轮次（estimated_review_rounds）：4
- 历史相似书籍数量（historical_reference_matched_count）：2
- 历史每 1 万原文单位有效工时（historical_active_hours_per_10k_source_units）：0.32

### 模型选择

- deepseek：建议等级 中（medium）；用途：low-cost first-pass translation, terminology expansion, and broad chapter drafts；预估输入 token 148000；预估输出 token 116300。
- gpt：建议等级 高（high）；用途：final-quality translation, difficult passages, polysemy checks, and release-facing QA；预估输入 token 179700；预估输出 token 126800。
- claude：建议等级 高（high）；用途：long-context consistency review, style comparison, and independent QA；预估输入 token 158600；预估输出 token 47600。

## 翻译后实际统计

- 状态（status）：PASS
- 开始时间（started_at）：2026-06-13T00:00:00Z
- 完成时间（finished_at）：2026-06-13T08:12:40Z
- 实际日历天数（actual_calendar_days）：1
- 实际有效工时（actual_active_hours）：6
- 实际审校轮次（actual_review_rounds）：5
- 实际难度（actual_difficulty）：高（4/5）
- 总输入 token（total_input_tokens）：240000
- 总输出 token（total_output_tokens）：110000
- 与预估的偏差（variance_against_estimate）：Actual active hours were below the heuristic estimate because the book is short fiction, but difficulty remained high due to archaic Spanish, picaresque tone, historical currency/social terms, and strict chapter/release gates.

### 实际模型使用

- openai：GPT-5 Codex（等级 高），角色 translation drafting, chapter full checks, EPUB QA, random spotcheck review, and release preparation，输入 token 240000，输出 token 110000。

### 后续预估经验

- Short early-modern fiction can still require high-tier review because old social ranks, church terms, and currency words carry narrative evidence.
- Post-EPUB random sampling should treat source-form residue in names and currency as a defect family and audit with exact-string scans before PASS.
- For short fiction, LifeBook Digest should remain disabled unless the book is long, professional, or philosophical by the project policy.

## 隐私与发布边界

- 本文件不得包含原文、译文片段、prompt、私人 QA 日志或本机绝对路径。
- 私人自用项目的 metrics 不得发布到 GitHub。
