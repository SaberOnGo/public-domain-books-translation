# 06 术语表与文体画像 / Glossary & Style Profile

## 输入 / Input

- `metadata/book_specific_translation_research.md`
- `qa/pretranslation/pretranslation_report.md`
- `metadata/source_witness_manifest.md`
- `qa/textual/textual_uncertainty_log.md`
- `chapters/src/*.md`

## 任务 / Tasks

1. 生成/更新 `glossary/terms.csv`。
2. 生成/更新 `glossary/style_guide.md`。
3. 根据预翻译结果修订 `metadata/style_profile.md`。
4. 把专名、转写、异文、拟补和参考译本差异中的高频术语写入术语表。

## `glossary/terms.csv` 必含类型

- `proper_noun`
- `technical_term`
- `divine_or_mythic_name`
- `place_name`
- `school_or_group`
- `formulaic_expression`
- `textual_variant`
- `editorial_term`
- `symbol`
- `historical_term`

## `metadata/style_profile.md` 修订要求

必须把 `qa/pretranslation/pretranslation_report.md` 的成功译法、失败教训、越界发挥边界、省字式翻译边界写入文体画像。

## 硬规则 / Hard Rules

- 术语表不能只是空模板。
- 人名、地名、神名、历史称谓、技术词、固定论证表达、异文和编辑术语必须先入表。
- 每个核心词条必须记录古希腊文原词、必要转写、中文译名和说明。
- 第二语言参考译本的译法只能作为 notes 中的参考线索，不能替代古希腊文原词。
- 如果预翻译报告是 `FAIL`，不得执行本步骤。

## 状态 / State

成功后：

- `status = GLOSSARY_STYLE_DONE`
- `current_step = glossary_style_profile_done`
