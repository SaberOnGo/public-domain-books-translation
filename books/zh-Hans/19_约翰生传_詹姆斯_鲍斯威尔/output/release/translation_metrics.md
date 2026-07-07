# 翻译任务预估与实际统计

本文件用于公开记录翻译前预估与翻译后实际统计，方便后续用户和 AI 参考相似书籍的时间、难度、token 消耗和模型等级选择。机器可读取的事实源是同目录下的 `translation_metrics.json`。

## 书籍信息

- 书名（title）：约翰生传
- 原书名（original_title）：未记录
- 作者（author）：未记录
- 语言方向模板（source_target）：template/epub_pipeline/English-to-Simplified-Chinese
- 发布模式（publication_mode）：public_domain

## 翻译前预估

- 状态（status）：PASS
- 主要书籍类型（primary_book_type）：历史
- 领域（domains）：history、fiction、philosophy、science、language_learning、programming
- 原文规模（source_unit_count）：3579198 words
- 章节数（chapter_count）：2
- 图像/图示数量（figures_count）：0
- 表格数量（tables_count）：0
- 公式或代码块数量（formula_or_code_block_count）：18
- 注释数量（notes_or_annotations_count）：0
- 难度（difficulty）：高（4/5）
- 难度说明（difficulty_rationale）：Primary detected type is history; secondary types: fiction, philosophy, science, language_learning, programming. Source size is 3579198 words; chapter_count=2. Detected figures=0, tables=0, formula_or_code_blocks=18, notes=0. Named-entity density is very_high.
- 预估日历时间（estimated_calendar_days）：420-1167 天
- 预估有效工时（estimated_active_hours）：2096-3501 小时
- 预估审校轮次（estimated_review_rounds）：5
- 历史相似书籍数量（historical_reference_matched_count）：4
- 历史每 1 万原文单位有效工时（historical_active_hours_per_10k_source_units）：0.52

### 模型选择

- deepseek：建议等级 中（medium）；用途：low-cost first-pass translation, terminology expansion, and broad chapter drafts；预估输入 token 9420400；预估输出 token 7401800。
- gpt：建议等级 高（high）；用途：final-quality translation, difficult passages, polysemy checks, and release-facing QA；预估输入 token 11439100；预估输出 token 8074700。
- claude：建议等级 高（high）；用途：long-context consistency review, style comparison, and independent QA；预估输入 token 10093300；预估输出 token 3028000。

## 翻译后实际统计

- 状态（status）：PASS
- 开始时间（started_at）：2026-06-27T02:06:09Z
- 完成时间（finished_at）：2026-07-07T04:05:12Z
- 实际日历天数（actual_calendar_days）：11
- 实际有效工时（actual_active_hours）：27
- 实际审校轮次（actual_review_rounds）：46
- 实际难度（actual_difficulty）：超高（5/5）
- 总输入 token（total_input_tokens）：18000000
- 总输出 token（total_output_tokens）：9377464
- 与预估的偏差（variance_against_estimate）：Actual active time was far below the conservative pretranslation estimate because the run used an existing language-pair template, automated chapter/build gates, and compressed review loops. Random-review rounds were far above the initial estimate because every confirmed defect-family repair required a fresh seed and a new clean PASS chain.

### 实际模型使用

- openai：GPT-5 Codex（等级 超高），角色 full-book translation, per-chapter closure review, EPUB QA, random spot-check repair, defect-family audit, and release gating，输入 token 18000000，输出 token 9377464。

### 后续预估经验

- Long annotated biographies require substantial post-EPUB QA for index boundaries, ibid-style notes, OCR page artifacts, foreign-title interfaces, and letter-header structure.
- For book-length release workflows, budget for repeated random-review seed resets after every defect-family repair; a repair round must not be counted as the clean PASS round.
- Dense 18th-century English prose benefits from deterministic whole-book scans for Latin titles, bibliography rows, page-number residue, and title/note punctuation interfaces before final random review.
- Thread-level token totals are approximate release-planning records rather than provider billing records; future runs should record per-stage token use at chapter, EPUB, random-review, and release gates.

## 隐私与发布边界

- 本文件不得包含原文、译文片段、prompt、私人 QA 日志或本机绝对路径。
- 私人自用项目的 metrics 不得发布到 GitHub。
