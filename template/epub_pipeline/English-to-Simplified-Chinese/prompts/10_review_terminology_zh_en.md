# 10 术语一致性审校 / Terminology Review

## 输入 / Input

- `chapters/translated/{NNN_slug}.md`
- `glossary/terms.csv`
- `glossary/proper_nouns.csv`
- `references/proper_noun_display_policy.md`
- `references/note_marker_policy.md`
- `metadata/style_profile.md`

## 任务 / Tasks

逐章检查：

- 人名、地名、船名、组织名。
- 标题中的专名：章节标题、副标题和目录题名不计入“正文首次出现”，按 `glossary/proper_nouns.csv.subsequent_rendering` 显示；策略 `2`/`4` 可以保留原名，但不得在标题追加正文首次出现括注。
- 重点专有名词是否按 `glossary/proper_nouns.csv.display_policy` 执行；用户未设置时默认策略 `3`，即第一次正文自然出现 `译名（原文）`、后续用译名。
- 策略 `5` 的重点专名首次正文出现是否同时有 `译名（原文）` 和 `[1]`、`(1)` / `（1）`、`注1` 之一；专名括注不得被当作注号。
- 首次出现后再次显示原文，是否只发生在讨论原文拼写、转写、音译差异、源语形式或学界译名分歧的位置，并记录到 `repeat_original_allowed_when`。
- 普通名词、器物名、衣物名、材料名和动作名是否已译成中文；不得保留 `source term（中文释义）` 或 `中文词（source term）` 这类普通名词原文括注。
- 专业术语、行业术语、历史称谓、制度名、身份称谓和文化负载词是否默认使用中文译名或准确意译。
- 是否存在无必要的正文 `中文译名（source term）`；如需原词，是否已改为正文注号加本章译注、章末注或术语表。
- 正文括注原词是否属于明确例外：不保留原词会造成明显误解、原词本身是作者论证对象、或学界译名分歧必须当场交代。例外必须记录理由。
- 是否逐项使用 `glossary/terms.csv.forbidden_body_renderings` 扫描正文；发现禁用写法必须返工，不能只在 QA 里说明。
- 注号是否只使用 `[1]`、`(1)` / `（1）`、`注1` 三类体系；不得出现带圈数字、小圆圈“注”、裸 `译注：` / `脚注：` / `尾注：` / `附注：` 或句末裸数字。
- `thegn` / `thane` 是否避免正文音译“塞恩”和现代政治化泛译“支持者”；是否按语境使用“王室领主”“领主近臣”“盎格鲁-撒克逊领主”等，并把原词说明放入术语注。`witenagemot` 是否正文用“贤人会议”并把原词放术语注。
- 象征词。
- 同一术语是否前后不一致。
- 是否残留旧纸书可见分隔符，如 `* * * * *`、`*****`、`----`、`---`。

## 输出 / Output

- `qa/terminology/{NNN_slug}.md`

可以修订 `chapters/translated/{NNN_slug}.md`，但必须记录。

## 状态 / State

成功后：

- `current_step = terminology_review_done`

