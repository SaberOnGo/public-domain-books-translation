# 05 预翻译试译 / Pretranslation Trials

## 输入

- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `glossary/terms.csv`
- `qa/textual/classical_chinese_textual_notes.md`

## 任务

选择至少三类样本：

1. 人物、国家、官名或制度背景密集段。
2. 断句、标点或省略关系困难段。
3. 叙事、对话、游说、反讽或外交辞令强的段。

输出 `qa/pretranslation/pretranslation_report.md`，每个样本必须包含：

- 古文原文。
- 现代中文今译。
- 注释候选。
- 断句/词义/人物关系说明。
- PASS/FAIL 与返工理由。

## 门禁

试译报告必须为 `PASS` 才能批量翻译。只证明“能翻出大意”不算 PASS。

## 状态区分 / Status Distinction

文言文新模板建设时允许使用：

- `PASS_FOR_TEMPLATE_TRIAL`：说明模板形态、对照正文、注释策略和审校流程已被小样本验证；不得据此开始全书批量翻译。
- `PRETRANSLATION_PASS`：说明正式来源权利、底本策略、人物/术语锁定、注释策略和试译质量均已通过；只有这个状态才允许进入正式批量翻译。

若来源策略仍是 trial-only，或历史 profile 的人物/国家/年代记录尚未补齐，报告必须写 `PASS_FOR_TEMPLATE_TRIAL` 或 `FAIL`，不得写 `PRETRANSLATION_PASS`。
