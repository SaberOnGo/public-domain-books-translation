# 文学与纪实翻译质量框架

这个目录用于先磨“刀”，再翻书。它不绑定某一本书，而是规定 AI 辅助翻译必须怎样研究、产出、审校、测试和返工。

## 目录

- `SKILL.md`：可复用技能说明，给 Codex/其他 AI 执行时读取。
- `references/research_digest.md`：翻译理论、AI 翻译研究、质量评估方法摘要。
- `references/quality_standard.md`：本项目的译文质量标准。
- `references/workflow.md`：从原文到终稿的强制流程。
- `templates/chapter_translation_prompt.md`：分章翻译提示词。
- `templates/style_profile_prompt.md`：正式翻译前生成文体画像。
- `templates/book_specific_research_prompt.md`：为具体书建立专项翻译研究。
- `templates/pretranslation_trial_prompt.md`：正式分章前的预翻译试译。
- `templates/sample_translation_test_prompt.md`：正式翻译前的小样本测试。
- `templates/private_benchmark_compare_prompt.md`：用户私有优秀译本片段对照测试。
- `templates/image_word_audit_prompt.md`：检查是否把有画面的词偷懒译成平板说明词。
- `templates/chapter_quality_gate_prompt.md`：章节进入终稿前的门禁审查。
- `templates/revision_prompt.md`：返工提示词。
- `templates/evaluation_rubric.md`：评分表。
- `tests/benchmark_protocol.md`：用优秀译本做小样本对照测试的协议。
- `tests/private_benchmark_cases/`：私有基准样本的方法卡，不保存长段受版权保护文本。

## 强制原则

任何正式翻译前，先用本框架做小样本测试。测试不通过，不进入整章批量生产。

最低交付顺序：

1. 完成通用规则研究。
2. 生成 `metadata/book_specific_translation_research.md`。
3. 生成 `metadata/style_profile.md`。
4. 生成 `qa/pretranslation/pretranslation_report.md`，且结论为 PASS。
5. 生成 `qa/samples/sample_test_report.md`，且结论为 PASS。
6. 如使用《情人》等仍在版权期优秀译本，只做私有短样本对照，结论写入 `qa/benchmark/`，不保存长段版权文本。
7. 分章翻译。
8. 每章生成 `qa/imagery/{chapter}.imagery.md` 和 `qa/gates/{chapter}.gate.md`，PASS 后才写入 `chapters/final/`。

禁止把“通顺”误认为“好译文”。本项目的好译文必须同时满足：

- 准确：事实、逻辑、语气不偏离原文。
- 顺畅：中文读者读起来不被英文句法绊住。
- 有声调：叙事有节奏，关键句有力度。
- 有判断：旧时代称谓、文化差异、修辞隐喻要经过译者判断，而不是机械搬运。
- 可验收：有评分表、样例对照、返工记录。
