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

## 术语呈现策略 / Term Presentation Policy

生成 `glossary/terms.csv` 和 `glossary/style_guide.md` 时，必须为历史术语、制度名、身份称谓、专业术语和文化负载词写明呈现策略：

- `translation`：正文采用的中文译名或意译。
- `source_term`：原词，仅用于术语表、译注或确有必要的正文例外。
- `display_policy`：`body_chinese_only`、`note_on_first_use`、`body_parenthetical_exception` 三选一。
- `forbidden_body_renderings`：正文禁用写法，用 `|` 分隔，例如音译、原词裸露、`中文译名（source term）` 形式或误导性泛译。
- `note_text`：若需要注释，写入读者友好的短注，不写百科条目。
- `exception_reason`：只有 `body_parenthetical_exception` 时填写，说明为什么必须在正文括注原词。

正文默认 `body_chinese_only` 或 `note_on_first_use`。不得把历史术语和专业术语批量写成 `中文译名（source term）`；需要解释时，优先使用正文注号加本章译注/章末注/术语表。

盎格鲁-撒克逊制度身份词示例：`thegn` / `thane` 不得默认音译为“塞恩”，也不宜泛译为“支持者”。政治史、土地和军事义务语境中，应按本书上下文选择“王室领主”“领主近臣”“盎格鲁-撒克逊领主”等，并在术语说明中写明原文、又作形式和含义。`witenagemot` 正文用“贤人会议”，原词放术语说明。

本步骤必须把高风险术语的禁用写法写入 `forbidden_body_renderings`。例如本书若涉及 `thegn` / `thane`，应把 `塞恩`、裸露的 `thegn` / `thane`、无理由的 `王室领主（thegn）` 以及不适合作统一译名的 `支持者` 纳入禁用或需复核写法；若涉及 `witenagemot`，应把正文裸露 `witenagemot` 纳入禁用写法。

## `metadata/style_profile.md` 修订要求

必须把 `qa/pretranslation/pretranslation_report.md` 的成功译法、失败教训、越界发挥边界、省字式翻译边界写入文体画像。

## 硬规则 / Hard Rules

- 术语表不能只是空模板。
- 象征词、历史称谓、技术词必须先入表。
- 历史术语、制度名、身份称谓、专业术语和文化负载词不得默认在正文使用 `中文译名（source term）`。凡使用正文括注原词，必须有 `exception_reason`。
- 高风险历史术语必须填写 `display_policy`、`note_text` 和 `forbidden_body_renderings`；否则不得进入批量翻译。
- 如果预翻译报告是 `FAIL`，不得执行本步骤。

## 状态 / State

成功后：

- `status = GLOSSARY_STYLE_DONE`
- `current_step = glossary_style_profile_done`
