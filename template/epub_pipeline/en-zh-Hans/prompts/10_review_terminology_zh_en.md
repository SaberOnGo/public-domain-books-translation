# 10 术语一致性审校 / Terminology Review

## 输入 / Input

- `chapters/translated/{NNN_slug}.md`
- `glossary/terms.csv`
- `metadata/style_profile.md`

## 任务 / Tasks

逐章检查：

- 人名、地名、船名、组织名。
- 标题中的人名：章节标题、副标题和目录题名只使用中文译名，不计入“正文首次出现”；英文原名或括注只能放在正文第一次自然出现处。
- 普通名词、器物名、衣物名、材料名和动作名是否已译成中文；不得保留 `source term（中文释义）` 这种英文或原文词打头的正文。
- 专业术语、行业术语。
- 历史称谓。
- 象征词。
- 同一术语是否前后不一致。
- 是否残留旧纸书可见分隔符，如 `* * * * *`、`*****`、`----`、`---`。

## 输出 / Output

- `qa/terminology/{NNN_slug}.md`

可以修订 `chapters/translated/{NNN_slug}.md`，但必须记录。

## 状态 / State

成功后：

- `current_step = terminology_review_done`

