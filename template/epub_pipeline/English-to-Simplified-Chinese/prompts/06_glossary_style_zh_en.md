# 06 术语表与文体画像 / Glossary & Style Profile

## 输入 / Input

- `metadata/book_specific_translation_research.md`
- `qa/pretranslation/pretranslation_report.md`
- `chapters/src/*.md`

## 任务 / Tasks

1. 生成/更新 `glossary/terms.csv`。
2. 先运行全书专名候选发现并逐项裁决，再生成/更新并锁定 `glossary/proper_nouns.csv` 与 `glossary/proper_noun_occurrences.csv`。
3. 生成/更新 `glossary/style_guide.md`。
4. 根据预翻译结果修订 `metadata/style_profile.md`。

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
- `term_control`：`locked`、`preferred`、`avoid`、`note_only` 四选一。
  - `locked`：人名、地名、核心专名、符号等必须硬锁。
  - `preferred`：推荐译法，允许按上下文自然变体。
  - `avoid`：禁用译法。
  - `note_only`：只在译注、章末注或术语表解释，不压进正文。
- `display_policy`：`body_chinese_only`、`note_on_first_use`、`body_parenthetical_exception` 三选一。
- `forbidden_body_renderings`：正文禁用写法，用 `|` 分隔，例如音译、原词裸露、`中文译名（source term）` 形式或误导性泛译。
- `note_text`：若需要注释，写入读者友好的短注，不写百科条目。
- `exception_reason`：只有 `body_parenthetical_exception` 时填写，说明为什么必须在正文括注原词。

正文默认 `body_chinese_only` 或 `note_on_first_use`。不得把历史术语和专业术语批量写成 `中文译名（source term）`；需要解释时，优先使用正文注号加本章译注/章末注/术语表。

## 重点专有名词译表 / Important Proper-Noun Register

重点专有名词使用独立文件：

```text
glossary/proper_nouns.csv
```

必备列必须与 `references/proper_noun_display_policy.md` 一致：

```csv
entity_id,source_name,target_name,category,display_policy,first_rendering,subsequent_rendering,note_required,repeat_original_allowed_when,notes,source_aliases,target_aliases,scope,status,chinese_gloss,display_strategy,first_occurrence_rule,same_name_disambiguation
```

用户可在 prompt 中显式设置：

```text
[重点专有名词(人名、地名、术语、罕见名词、音译后体验很差的名字等) 的翻译格式] 设置 = 3
```

允许值为 `1` 到 `5`；用户未设置时默认 `3`：第一次正文自然出现写 `译名（原文）`，后续基本使用译名。标题、副标题和 EPUB 目录题名不计入正文首次出现，且不得放英文原名或英文括注。若后文正在讨论原文拼写、转写、音译差异或学界译名分歧，可再次出现原文，并把理由写入 `repeat_original_allowed_when`。

必须把选择来源写入 `state/translation_contract.json.proper_nouns.selection_source`：用户明确选择时为 `user`，未选择而采用策略 `3` 时为 `default`。默认策略不等于跳过发现：仍须扫描全部 `chapters/src/*.md`，生成 `proper_noun_candidates.csv` 和带 source span、`unit_id`、`entity_id` 的 occurrence ledger，逐项决定注册/排除/消歧，最后用人工或独立审查记录锁定 discovery manifest。空候选表、伪造零候选或缺少全书文件/hash 证据不得锁定。

同一原文形式可对应不同历史人物或地点，必须使用不同 `entity_id`、非重叠 `scope` 和可审计的 `same_name_disambiguation`；不得用 `source_name` 充当实体主键。所有专名决定必须在翻译前完成。翻译开始后禁止一边阅读一边追加或改写 CSV；若发现漏项，当前翻译 generation 失效，回到本步骤重做全书发现、ledger 和锁定。

正文专名只能通过 canonical unit 的 `target_template` 占位符 `{{pn:entity_id}}` 表达，再由只读取已锁定 CSV 与 occurrence ledger 的脚本渲染。译者不得在模板里直接写已锁定的中文名、原文名或首次呈现形式，也不得直接修改 `chapters/translated` / `chapters/final`。

只把确实需要原文接口的重点名词写入本表，例如人名、地名、王朝、机构、罕见术语、文化负载词，或音译后体验很差、单独汉译会影响阅读的名字。能自然翻译的普通词不要塞入本表。

策略 `5` 是专名原文括注加注号的组合：例如 `尼禄（Nero）[1]`、`尼禄（Nero）（1）` 或 `尼禄（Nero）注1`。专名括注和注释是两个不同功能；注号格式必须遵守 `references/note_marker_policy.md`。

术语表不得把所有词都硬锁。除人名、地名、符号和核心专名外，默认使用 `preferred`，让翻译阶段可以优先写出自然中文。若某个 `preferred` 术语在句中会导致拗口、重复或关系不清，允许在不改变概念的前提下改用自然变体，并在术语审校中判断是否需要回收。

盎格鲁-撒克逊制度身份词示例：`thegn` / `thane` 不得默认音译为“塞恩”，也不宜泛译为“支持者”。政治史、土地和军事义务语境中，应按本书上下文选择“王室领主”“领主近臣”“盎格鲁-撒克逊领主”等，并在术语说明中写明原文、又作形式和含义。`witenagemot` 正文用“贤人会议”，原词放术语说明。

本步骤必须把高风险术语的禁用写法写入 `forbidden_body_renderings`。例如本书若涉及 `thegn` / `thane`，应把 `塞恩`、裸露的 `thegn` / `thane`、无理由的 `王室领主（thegn）` 以及不适合作统一译名的 `支持者` 纳入禁用或需复核写法；若涉及 `witenagemot`，应把正文裸露 `witenagemot` 纳入禁用写法。

## `metadata/style_profile.md` 修订要求

必须把 `qa/pretranslation/pretranslation_report.md` 的成功译法、失败教训、越界发挥边界、省字式翻译边界写入文体画像。

## 硬规则 / Hard Rules

- 术语表不能只是空模板。
- 象征词、历史称谓、技术词必须先入表。
- 高风险术语必须填写 `term_control`，不得默认全部硬锁为 `locked`。
- 重点专有名词必须写入 `glossary/proper_nouns.csv`，并填写 `display_policy`；默认值为 `3`，不得留空。
- 每个专名必须有稳定 `entity_id`；候选表、锁定表和 occurrence ledger 必须全量一致并绑定当前 source corpus SHA-256。
- `proper_noun_discovery_manifest.json.status` 未锁定、人工复核未完成、存在 unresolved candidate/occurrence 或 CSV hash 漂移时，不得进入翻译。
- 历史术语、制度名、身份称谓、专业术语和文化负载词不得默认在正文使用 `中文译名（source term）`。凡使用正文括注原词，必须有 `exception_reason`。
- 高风险历史术语必须填写 `display_policy`、`note_text` 和 `forbidden_body_renderings`；否则不得进入批量翻译。
- 注号只能使用 `[1]`、`(1)` / `（1）`、`注1` 三类体系；不得使用带圈数字、小圆圈“注”、裸 `译注：` 或裸尾随数字。
- 如果预翻译报告是 `FAIL`，不得执行本步骤。

## 状态 / State

成功后：

- `status = GLOSSARY_STYLE_DONE`
- `current_step = glossary_style_profile_done`
