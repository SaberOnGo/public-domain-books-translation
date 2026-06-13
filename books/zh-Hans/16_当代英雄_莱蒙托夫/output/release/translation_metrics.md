# 翻译任务预估与实际统计

本文件用于公开记录翻译前预估与翻译后实际统计，方便后续用户和 AI 参考相似书籍的时间、难度、token 消耗和模型等级选择。机器可读取的事实源是同目录下的 `translation_metrics.json`。

## 书籍信息

- 书名（title）：当代英雄
- 原书名（original_title）：Герой нашего времени
- 作者（author）：莱蒙托夫
- 语言方向模板（source_target）：template/epub_pipeline/ru-zh-Hans
- 发布模式（publication_mode）：public_domain

## 翻译前预估

- 状态（status）：PASS
- 主要书籍类型（primary_book_type）：小说
- 领域（domains）：fiction、science、philosophy、history、language_learning
- 原文规模（source_unit_count）：151122 characters
- 章节数（chapter_count）：19
- 图像/图示数量（figures_count）：0
- 表格数量（tables_count）：0
- 公式或代码块数量（formula_or_code_block_count）：0
- 注释数量（notes_or_annotations_count）：0
- 难度（difficulty）：高（4/5）
- 难度说明（difficulty_rationale）：Primary detected type is fiction; secondary types: science, philosophy, history, language_learning. Source size is 151122 characters; chapter_count=19. Detected figures=0, tables=0, formula_or_code_blocks=0, notes=0. Named-entity density is very_high.
- 预估日历时间（estimated_calendar_days）：18-50 天
- 预估有效工时（estimated_active_hours）：89-149 小时
- 预估审校轮次（estimated_review_rounds）：4
- 历史相似书籍数量（historical_reference_matched_count）：3
- 历史每 1 万原文单位有效工时（historical_active_hours_per_10k_source_units）：0.42

### 模型选择

- deepseek：建议等级 中（medium）；用途：low-cost first-pass translation, terminology expansion, and broad chapter drafts；预估输入 token 397800；预估输出 token 312500。
- gpt：建议等级 高（high）；用途：final-quality translation, difficult passages, polysemy checks, and release-facing QA；预估输入 token 483000；预估输出 token 340900。
- claude：建议等级 高（high）；用途：long-context consistency review, style comparison, and independent QA；预估输入 token 426200；预估输出 token 127800。

## 翻译后实际统计

- 状态（status）：PASS
- 开始时间（started_at）：2026-06-13T00:00:00Z
- 完成时间（finished_at）：2026-06-13T08:48:42Z
- 实际日历天数（actual_calendar_days）：1
- 实际有效工时（actual_active_hours）：12
- 实际审校轮次（actual_review_rounds）：9
- 实际难度（actual_difficulty）：高（4/5）
- 总输入 token（total_input_tokens）：650000
- 总输出 token（total_output_tokens）：260000
- 与预估的偏差（variance_against_estimate）：完成用时低于模板历史估算；主要原因是使用单一高等级模型连续处理俄语模板、翻译、审校和 EPUB 门禁，且本书无图表重建负担。实际难度仍保持 high，因为专名、法语插句、十九世纪俄语心理独白和决斗语境需要逐章复核。

### 实际模型使用

- openai：GPT-5 Codex（等级 高），角色 ru-zh-Hans template creation, chapter translation, chapter controls, EPUB QA, random spot-check closure, and release preparation，输入 token 650000，输出 token 260000。

### 后续预估经验

- 俄语长篇小说即使无图表，也应按 high 难度估算，因为专名、军职、法语社交短句和心理独白会增加逐章审校成本。
- 先完善语言方向模板能减少后续章节控制返工，但新模板首本书需要额外预留模板回填和门禁调试时间。
- Digest 对长篇小说适用；应在 EPUBCheck 通过后生成并单独校验合并后的 digest EPUB。
- 随机抽检若首轮无问题，仍需要新 seed 追加第二轮当前 run PASS，避免把单轮抽样当作 release 结论。

## 隐私与发布边界

- 本文件不得包含原文、译文片段、prompt、私人 QA 日志或本机绝对路径。
- 私人自用项目的 metrics 不得发布到 GitHub。
