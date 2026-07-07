# 翻译任务预估与实际统计

本文件用于公开记录翻译前预估与翻译后实际统计，方便后续用户和 AI 参考相似书籍的时间、难度、token 消耗和模型等级选择。机器可读取的事实源是同目录下的 `translation_metrics.json`。

## 书籍信息

- 书名（title）：罗马帝国衰亡史
- 原书名（original_title）：The History of the Decline and Fall of the Roman Empire
- 作者（author）：未记录
- 语言方向模板（source_target）：template/epub_pipeline/en-zh-Hans
- 发布模式（publication_mode）：public_domain

## 翻译前预估

- 状态（status）：PASS
- 主要书籍类型（primary_book_type）：历史
- 领域（domains）：history、fiction、science、philosophy、language_learning、programming
- 原文规模（source_unit_count）：4783891 characters
- 章节数（chapter_count）：606
- 图像/图示数量（figures_count）：0
- 表格数量（tables_count）：2
- 公式或代码块数量（formula_or_code_block_count）：1
- 注释数量（notes_or_annotations_count）：2002
- 难度（difficulty）：高（4/5）
- 难度说明（difficulty_rationale）：Primary detected type is history; secondary types: fiction, science, philosophy, language_learning, programming. Source size is 4783891 characters; chapter_count=606. Detected figures=0, tables=2, formula_or_code_blocks=1, notes=2002. Named-entity density is very_high.
- 预估日历时间（estimated_calendar_days）：559-1555 天
- 预估有效工时（estimated_active_hours）：2792-4663 小时
- 预估审校轮次（estimated_review_rounds）：4
- 历史相似书籍数量（historical_reference_matched_count）：4
- 历史每 1 万原文单位有效工时（historical_active_hours_per_10k_source_units）：0.52

### 模型选择

- deepseek：建议等级 中（medium）；用途：low-cost first-pass translation, terminology expansion, and broad chapter drafts；预估输入 token 12591200；预估输出 token 9893100。
- gpt：建议等级 高（high）；用途：final-quality translation, difficult passages, polysemy checks, and release-facing QA；预估输入 token 15289300；预估输出 token 10792500。
- claude：建议等级 高（high）；用途：long-context consistency review, style comparison, and independent QA；预估输入 token 13490600；预估输出 token 4047200。

## 翻译后实际统计

- 状态（status）：PASS
- 开始时间（started_at）：2026-06-26T00:00:00Z
- 完成时间（finished_at）：2026-06-29T11:48:37Z
- 实际日历天数（actual_calendar_days）：4
- 实际有效工时（actual_active_hours）：120
- 实际审校轮次（actual_review_rounds）：304
- 实际难度（actual_difficulty）：高（4/5）
- 总输入 token（total_input_tokens）：20550631
- 总输出 token（total_output_tokens）：13288266
- 与预估的偏差（variance_against_estimate）：?????????????????????? metrics ???????????? translated/final ??????????????????????????

### 实际模型使用

- gpt：GPT-5 Codex（等级 高），角色 chapter translation, chapter-level full checks, final publication QA, random spot-check closure, and release preparation，输入 token 15289300，输出 token 10792500。
- local-scripts：LifeBook book-local QA scripts（等级 中），角色 coverage checks, publication lint, EPUB build, EPUBCheck, random sampling, Digest merge, and release gates，输入 token 1，输出 token 1。
- gpt：GPT-5 Codex review pass（等级 高），角色 independent-style random sample review records and issue-family audit support，输入 token 5261330，输出 token 2495765。

### 后续预估经验

- ?????????????????????????302 ?????????? EPUB ????????????
- ????????????????????????????????????????????????
- ?? release ?? Digest ????? EPUB ???????????? EPUBCheck???? release ?????????? EPUB?
- ???????????? review_run_id ????? PASS?????????????????? seed ?????

## 隐私与发布边界

- 本文件不得包含原文、译文片段、prompt、私人 QA 日志或本机绝对路径。
- 私人自用项目的 metrics 不得发布到 GitHub。
