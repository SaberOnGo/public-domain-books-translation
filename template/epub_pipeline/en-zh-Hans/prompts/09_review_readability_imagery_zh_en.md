# 09 可读性与意象审计 / Readability & Imagery Review

## 输入 / Input

- `chapters/translated/{NNN_slug}.md`
- `metadata/style_profile.md`
- `metadata/book_specific_translation_research.md`
- `references/quality_standard.md`

## 任务 / Tasks

逐章检查，并按顺序执行两段式审校：

### 第一段：只看中文 / Chinese-Only Polish

先不要看英文原文，只读 `chapters/translated/{NNN_slug}.md`，判断它作为中文书是否成立：

1. 中文是否自然。
2. 是否有直译腔。
3. 是否有大段长句、不断气句、过密分号或英文从句硬接。
4. 是否像说明书、学术报告或动作清单，而不是本书应有的叙述声音。
5. 随机朗读 20 句，明显拗口是否超过 1 句。
6. 中文独立阅读评分是否达到 4/5。

若第一段 FAIL，先修中文，不得用“忠实原文”作为保留拗口译文的理由。

### 第二段：对照原文 / Source-Aware Check

中文独立润色后，再对照原文检查：

1. 是否有“只说明、不成像”的懒译词。
2. 是否有越界发挥。
3. 是否有省字式翻译。
4. 开篇、结尾、危险现场、象征物、人物评价是否足够有力。
5. 第一段润色是否改错事实、动作强度、情绪强度或叙述立场。

## 输出 / Output

- `qa/readability/{NNN_slug}.md`
- `qa/imagery/{NNN_slug}.imagery.md`

## `qa/imagery` 必含

| 原文词/短语 | 当前译法 | 问题 | 建议译法 | 理由 |
| --- | --- | --- | --- | --- |

并列出：

- 中文独立阅读评分。
- 20 句朗读测试结果。
- 大段长句/不断气句警报。
- 懒译词警报。
- 过度发挥警报。
- 省字式翻译警报。
- 修改后的关键句。

## 状态 / State

成功后：

- `current_step = readability_imagery_review_done`

