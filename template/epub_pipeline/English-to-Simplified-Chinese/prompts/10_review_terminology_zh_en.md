# 10 术语一致性审校 / Terminology Review

## 输入 / Input

- `chapters/translated/{NNN_slug}.md`
- `glossary/terms.csv`
- `metadata/style_profile.md`

## 任务 / Tasks

逐章检查：

- 人名、地名、船名、组织名。
- 标题中的人名：章节标题、副标题和目录题名只使用中文译名，不计入“正文首次出现”；英文原名或括注只能放在正文第一次自然出现处。
- 普通名词、器物名、衣物名、材料名和动作名是否已译成中文；不得保留 `source term（中文释义）` 或 `中文词（source term）` 这类普通名词原文括注。
- 专业术语、行业术语、历史称谓、制度名、身份称谓和文化负载词是否默认使用中文译名或准确意译。
- 是否存在无必要的正文 `中文译名（source term）`；如需原词，是否已改为正文注号加本章译注、章末注或术语表。
- 正文括注原词是否属于明确例外：不保留原词会造成明显误解、原词本身是作者论证对象、或学界译名分歧必须当场交代。例外必须记录理由。
- 是否逐项使用 `glossary/terms.csv.forbidden_body_renderings` 扫描正文；发现禁用写法必须返工，不能只在 QA 里说明。
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

