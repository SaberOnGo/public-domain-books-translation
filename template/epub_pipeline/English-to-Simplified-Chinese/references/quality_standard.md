# 英语到简体中文译文质量标准 / English To Simplified Chinese Quality Standard

本文件是 `template/epub_pipeline/targets/zh-Hans/quality_framework/` 的简体中文目标语言规则在英语源文本场景下的应用摘要。更完整的中文目标语言质量规则见目标语言质量框架；英语源语言干扰问题见 `references/english_source_notes.md`；英文旧式章节标题链见 `references/english_chapter_title_strategy.md`。

## 总目标

译文要像优秀中文译者写出来的书，而不是英文文本的中文影子。

## 优秀出版线 / Excellence Gate

英语到简体中文的最终 EPUB 不能只做到“可读”。随机抽检里的 `80` 是硬失败线；80 多分常常仍表示较硬、偏密、解释化、抽象腔或英文句法残留。

正式 release/private artifact 默认要求：

- 每个独立 Agent `average_score >= 92`。
- 每个独立 Agent `lowest_score >= 88`。
- 每个抽中样本都有逐项评分行，不能只写总评。
- 反复出现的“可读但略硬/偏密/解释化/抽象”必须作为 `style_debt` 或译文质量问题族处理。

Final output must pass the excellence gate, not only the hard minimum. Scores in the 80s indicate readable but still unfinished prose unless the review evidence proves otherwise.

## 五维质量

1. 准确：事实、人物、地点、数字、因果、语气不误。
2. 通达：中文自然，不保留英文从句骨架。
3. 风格：译出原书的叙述声音，不把所有书都翻成说明文。
4. 审美：关键句有节奏、有画面、有收束。
5. 可出版：术语、标点、译注、目录、EPUB 格式稳定。

## 意象词优先

翻译要让读者在中文里看见、听见、感到原文要造成的效果。

每个关键译法必须问：

1. 是否准确？
2. 是否有画面？
3. 是否有场景或情绪附着力？
4. 是否比解释词更容易记住？
5. 是否越界添加了原文没有的东西？

## 意象增强边界

允许：

- 增强原文已有体感。
- 转化原文已有空间关系。
- 把原文象征物译成中文中更有画面的对应表达。

不允许：

- 新增原文没有的比喻物。
- 新增原文没有的声音。
- 新增原文没有的情节。
- 为了好看而替原文写作。

## 省字式翻译警报

中文有节奏，不等于省字。出现以下情况必须返工：

- 像提纲：`解绳，卸载，取出……`
- 像说明书：`天气寒冷并且有风。`
- 像机器压缩：省略连接，中文没有叙述气息。

## 一票否决

以下任一出现，章节不得进入 `chapters/final/`：

- 漏译整段或重要事实。
- 关键人物、地点、数字、方向错误。
- 明显直译腔。
- 关键句只说明、不成像。
- 为了生动而越界发挥。
- 为了简洁而省成提纲。
- 历史敏感称谓未经判断就现代化或硬搬。
## 随机抽检优秀出版线 / Random Review Excellence Gate

`80` 分只是硬失败线，不是优秀线。低于 80 必须 FAIL；80-87 代表基本可读但仍需精修；88-91 代表较好但未达到最终优秀门槛。

最终 release/private artifact 默认要求每个独立 Agent `average_score >= 92`、`lowest_score >= 88`、`blocking_issue_count = 0`，并且每个抽中样本都有逐项评分行。只写总评、缺少逐样本表格，或把“可读但略硬/偏密/略抽象/解释化/翻译腔”当作优秀分，均不得作为最终 PASS 证据。

反复出现的“可读但不顺”必须归入 `style_debt` 或相应译文质量问题族，回到目标语独立润色、源语句法重组或本书专项精修。随机抽检用于发现盲点和验证闭环，不应成为主要润色引擎。

## 专家级译文与上下文选义 / Expert Quality and Context Disambiguation

专家级译文不是“意思正确且大体顺”。翻译、审校和最终抽检必须按 `skills/expert-translation-quality/SKILL.md` 执行目标语独立阅读、原文忠实复核、多义词后文回看和句法重建。多义词、习语、称谓、术语和依赖后文判义的语法结构若被后文推翻，前文译法必须修订；保留未决歧义只能发生在原文本身有意暧昧，且译文保留了同等暧昧时。
