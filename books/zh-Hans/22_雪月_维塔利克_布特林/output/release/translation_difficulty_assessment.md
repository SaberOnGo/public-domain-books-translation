# 翻译难度评估

这是翻译前的聚合预估记录，不包含原文摘录或 prompt 文本。机器可读取的事实源是同目录下的 `translation_difficulty_assessment.json`。

## 总体判断

- 难度等级（difficulty）：高（4/5）
- 预估日历时间（estimated_calendar_days）：19-53 天
- 预估有效工时（estimated_active_hours）：95-159 小时
- 预估审校轮次（estimated_review_rounds）：5 轮
- 判断说明：本书主要类型为小说，检测到 32 章、约 102959 words；专名密度为超高，目标语文体难度为 4/5。

## 复杂度画像

- 主要书籍类型（primary_book_type）：小说
- 检测到的类型（detected_book_types）：小说、历史、科学、编程、哲学、语言学习
- 原文规模（source_unit_count）：102959 words
- 章节数（chapter_count）：32
- 图像/图示数量（figures_count）：56
- 表格数量（tables_count）：69
- 公式或代码块数量（formula_or_code_block_count）：0
- 注释数量（notes_or_annotations_count）：0
- 专名密度（named_entity_density）：超高

## 并行规划输入

- 加权原文工作量估计（weighted_source_unit_estimate）：137171
- 规划依据（planning_basis）：weighted_source_units_and_chapters_not_page_count；页数不是唯一依据。
- 客户端能力声明必需（capability_declaration_required）：true
- 下一步命令（next_command）：`npm run translation:orchestration:plan`
- 未获得可靠客户端能力、用户上限、速率或预算声明时，默认派生 worker 数为 0。

## 分项评分

- 源语言复杂度（source_language_complexity）：3/5
- 领域知识负荷（domain_knowledge_load）：5/5
- 术语密度（terminology_density）：5/5
- 论证或情节复杂度（argument_or_plot_complexity）：4/5
- 历史语境负荷（historical_context_load）：4/5
- 哲学/理论密度（philosophical_or_theoretical_density）：4/5
- 技术、代码或公式负荷（technical_code_or_formula_load）：1/5
- 图表/公式处理负荷（tables_figures_formula_load）：4/5
- 目标语文体难度（target_style_difficulty）：4/5
- 注释与交叉引用负荷（annotation_and_cross_reference_load）：1/5

## 历史统计参考

- 匹配到的相似书籍数量（matched_count）：5
- 历史每 1 万原文单位有效工时（active_hours_per_10k_source_units）：0.2
- 历史每原文单位输入 token（input_tokens_per_source_unit）：4.65
- 历史每原文单位输出 token（output_tokens_per_source_unit）：2.69

- 拉萨里略·德·托尔梅斯的一生：相似度 0.8509，实际工时 6 小时，总 token 350000，模型等级 high
- 约翰生传：相似度 0.8058，实际工时 27 小时，总 token 27377464，模型等级 very_high
- 罗马帝国衰亡史：相似度 0.8043，实际工时 120 小时，总 token 33838897，模型等级 high, medium
- 甲虫：相似度 0.4389，实际工时 9 小时，总 token 2120000，模型等级 high
- 当代英雄：相似度 0.4279，实际工时 12 小时，总 token 910000，模型等级 high

## 模型建议

- deepseek：建议等级 中（medium）；用途：低成本初译、术语扩展和章节草稿；预估输入 token 271000；预估输出 token 212900。
- gpt：建议等级 高（high）；用途：章节质控、疑难段落、终稿润色和 release 前 QA；预估输入 token 329100；预估输出 token 232300。
- claude：建议等级 高（high）；用途：长上下文一致性复核、风格比较和独立 QA；预估输入 token 290300；预估输出 token 87100。

## 类型修正边界

主要类型按冻结正文与本书研究修正为小说；旧关键词标签仅表示题材，不是作者对体裁的声明。原规模、估算分项及时间范围未重算。原预估属于翻译开始后补录，仍不能声称满足翻译前记录的时间要求。
