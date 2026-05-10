# 10 术语一致性审校 / Terminology Review

## 输入 / Input

- `chapters/translated/{NNN_slug}.md`
- `glossary/terms.csv`
- `metadata/style_profile.md`

## 任务 / Tasks

逐章检查：

- 人名、地名、船名、组织名。
- 专业术语、行业术语。
- 历史称谓。
- 象征词。
- 同一术语是否前后不一致。

## 输出 / Output

- `qa/terminology/{NNN_slug}.md`

可以修订 `chapters/translated/{NNN_slug}.md`，但必须记录。

## 状态 / State

成功后：

- `current_step = terminology_review_done`

