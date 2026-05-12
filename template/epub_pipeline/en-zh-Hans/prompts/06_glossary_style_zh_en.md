# 06 术语表与文体画像 / Glossary & Style Profile

## 输入 / Input

- `metadata/book_specific_translation_research.md`
- `qa/pretranslation/pretranslation_report.md`
- `chapters/src/*.md`

## 任务 / Tasks

1. 生成/更新 `glossary/terms.csv`。
2. 生成/更新 `glossary/style_guide.md`。
3. 根据预翻译结果修订 `metadata/style_profile.md`。

## `glossary/terms.csv` 必含类型

- `proper_noun`
- `technical_term`
- `industry_term`
- `symbol`
- `historical_term`

## `metadata/style_profile.md` 修订要求

必须把 `qa/pretranslation/pretranslation_report.md` 的成功译法、失败教训、越界发挥边界、省字式翻译边界写入文体画像。

## 硬规则 / Hard Rules

- 术语表不能只是空模板。
- 象征词、历史称谓、技术词必须先入表。
- 如果预翻译报告是 `FAIL`，不得执行本步骤。

## 状态 / State

成功后：

- `status = GLOSSARY_STYLE_DONE`
- `current_step = glossary_style_profile_done`
