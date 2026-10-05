# 翻译任务预估与实际统计

本文件用于公开记录翻译前预估与翻译后实际统计，方便后续用户和 AI 参考相似书籍的时间、难度、token 消耗和模型等级选择。机器可读取的事实源是同目录下的 `translation_metrics.json`。

记录时点偏差：独立指标文件漏写，本项在翻译后补做，未满足译前记录时点要求。未倒填日期；预估时间和token不能当作实测。

## 书籍信息

- 书名（title）：雪月
- 原书名（original_title）：Snowmoon
- 作者（author）：维塔利克·布特林（Vitalik Buterin）
- 语言方向模板（source_target）：template/epub_pipeline/English-to-Simplified-Chinese
- 发布模式（publication_mode）：licensed

## 翻译前预估

- 状态（status）：PASS
- 主要书籍类型（primary_book_type）：小说
- 领域（domains）：fiction、history、science、programming、philosophy、language_learning
- 原文规模（source_unit_count）：102959 words
- 章节数（chapter_count）：32
- 图像/图示数量（figures_count）：56
- 表格数量（tables_count）：69
- 公式或代码块数量（formula_or_code_block_count）：0
- 注释数量（notes_or_annotations_count）：0
- 难度（difficulty）：高（4/5）
- 难度说明（difficulty_rationale）：Primary detected type is history; secondary types: science, fiction, programming, philosophy, language_learning. Source size is 102959 words; chapter_count=32. Detected figures=56, tables=69, formula_or_code_blocks=0, notes=0. Named-entity density is very_high.
- 预估日历时间（estimated_calendar_days）：19-53 天
- 预估有效工时（estimated_active_hours）：95-159 小时
- 预估审校轮次（estimated_review_rounds）：5
- 历史相似书籍数量（historical_reference_matched_count）：5
- 历史每 1 万原文单位有效工时（historical_active_hours_per_10k_source_units）：0.2

### 模型选择

- deepseek：建议等级 中（medium）；用途：low-cost first-pass translation, terminology expansion, and broad chapter drafts；预估输入 token 271000；预估输出 token 212900。
- gpt：建议等级 高（high）；用途：final-quality translation, difficult passages, polysemy checks, and release-facing QA；预估输入 token 329100；预估输出 token 232300。
- claude：建议等级 高（high）；用途：long-context consistency review, style comparison, and independent QA；预估输入 token 290300；预估输出 token 87100。

## 翻译后实际统计

- 状态（status）：PASS
- 开始时间（started_at）：2026-10-02T00:17:21.576Z
- 完成时间（finished_at）：2026-10-05T05:01:26.265217+00:00
- 实际日历天数（actual_calendar_days）：3.1972764955671296
- 实际有效工时（actual_active_hours）：不可测量（UNAVAILABLE）
- 实际审校轮次（actual_review_rounds）：5
- 实际难度（actual_difficulty）：高（4/5）
- 总输入 token（total_input_tokens）：3288778716
- 总输出 token（total_output_tokens）：18697766
- 与预估的偏差（variance_against_estimate）：统计窗口经过 3.197 天，低于原机器估计 19–53 天；该估计记录在开工后补齐，不视为严格事前预测。有效工时不可测量，不比较 95–159 小时估计。共启动5个seed轮，3轮有A/B实际裁决，其中1轮FAIL，最终当前稿2轮连续优秀PASS；不是5轮完整PASS。输入包括缓存，不等于计费token。

### 实际模型使用

- gpt：gpt-6.1-sol（等级 高），角色 已核验的协调、串行合并、修订与门禁阶段，输入 token 830054135，输出 token 4270222。
- gpt：gpt-6-astra（等级 高），角色 宿主记录中已核验的早期协调与直属子任务阶段；不臆测每个历史子任务角色，输入 token 282545577，输出 token 862251。
- gpt：gpt-5.6-luna（等级 高），角色 已核验的直属翻译与独立审校worker，reasoning=max，输入 token 2176179004，输出 token 13565293。

### 后续预估经验

- 在完整翻译前冻结预估及计量边界；历史记录补齐不能冒充事前估计。
- 分别统计已启动、双审交付及当前稿连续PASS轮次；未交付的DRAFT模板不计完成。
- 预算应单列全章独立复查、整书问题族闭环、矢量图表及原生阅读器视觉检查。
- 只有经核验的生成时间允许在源码重建比较中忽略；正文、资产和许可差异仍失败。
- 缓存上下文占据大部分输入；累计宿主输入、有效工时与供应商费用分别记录。

## 隐私与发布边界

- 本文件不得包含原文、译文片段、prompt、私人 QA 日志或本机绝对路径。
- 私人自用项目的 metrics 不得发布到 GitHub。
