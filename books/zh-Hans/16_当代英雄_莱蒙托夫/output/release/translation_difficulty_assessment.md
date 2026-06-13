# 翻译难度评估

这是翻译前的聚合预估记录，不包含原文摘录或 prompt 文本。机器可读取的事实源是同目录下的 `translation_difficulty_assessment.json`。

## 总体判断

- 难度等级（difficulty）：高（4/5）
- 预估日历时间（estimated_calendar_days）：18-50 天
- 预估有效工时（estimated_active_hours）：89-149 小时
- 预估审校轮次（estimated_review_rounds）：4 轮
- 判断说明：本书主要类型为小说，检测到 19 章、约 151122 characters；专名密度为超高，目标语文体难度为 3/5。

## 复杂度画像

- 主要书籍类型（primary_book_type）：小说
- 检测到的类型（detected_book_types）：小说、科学、哲学、历史、语言学习
- 原文规模（source_unit_count）：151122 characters
- 章节数（chapter_count）：19
- 图像/图示数量（figures_count）：0
- 表格数量（tables_count）：0
- 公式或代码块数量（formula_or_code_block_count）：0
- 注释数量（notes_or_annotations_count）：0
- 专名密度（named_entity_density）：超高

## 分项评分

- 源语言复杂度（source_language_complexity）：3/5
- 领域知识负荷（domain_knowledge_load）：5/5
- 术语密度（terminology_density）：5/5
- 论证或情节复杂度（argument_or_plot_complexity）：4/5
- 历史语境负荷（historical_context_load）：4/5
- 哲学/理论密度（philosophical_or_theoretical_density）：4/5
- 技术、代码或公式负荷（technical_code_or_formula_load）：1/5
- 图表/公式处理负荷（tables_figures_formula_load）：1/5
- 目标语文体难度（target_style_difficulty）：3/5
- 注释与交叉引用负荷（annotation_and_cross_reference_load）：1/5

## 历史统计参考

- 匹配到的相似书籍数量（matched_count）：3
- 历史每 1 万原文单位有效工时（active_hours_per_10k_source_units）：0.42
- 历史每原文单位输入 token（input_tokens_per_source_unit）：1.93
- 历史每原文单位输出 token（output_tokens_per_source_unit）：0.78

- 林伯洛斯特的女孩：相似度 0.5868，实际工时 11 小时，总 token 680000，模型等级 high
- 拉萨里略·德·托尔梅斯的一生：相似度 0.3077，实际工时 6 小时，总 token 350000，模型等级 high
- 云使：相似度 0.268，实际工时 1.0 小时，总 token 135000，模型等级 high

## 模型建议

- deepseek：建议等级 中（medium）；用途：低成本初译、术语扩展和章节草稿；预估输入 token 397800；预估输出 token 312500。
- gpt：建议等级 高（high）；用途：章节质控、疑难段落、终稿润色和 release 前 QA；预估输入 token 483000；预估输出 token 340900。
- claude：建议等级 高（high）；用途：长上下文一致性复核、风格比较和独立 QA；预估输入 token 426200；预估输出 token 127800。
