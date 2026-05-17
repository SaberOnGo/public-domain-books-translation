# 09 可读性与意象审计 / Readability & Imagery Review

## 输入 / Input

- `chapters/translated/{NNN_slug}.md`
- `metadata/style_profile.md`
- `metadata/book_specific_translation_research.md`
- `references/quality_standard.md`

## 任务 / Tasks

逐章检查：

1. 中文是否自然。
2. 是否有直译腔。
3. 是否有“只说明、不成像”的懒译词。
4. 是否有越界发挥。
5. 是否有省字式翻译。
6. 开篇、结尾、危险现场、象征物、人物评价是否足够有力。
7. 技术证明中的古典简语是否被译成现代读者能复原关系的中文，例如作图中的交点、延长线、弧、弦、半径和圆心关系。
8. 是否存在过度解释：原文一个作图动作被扩写成多句说明，反而干扰证明阅读。
9. 《几何原本》等依据是否用小号依据标记，且章末注释说明对应命题、定义或系的大意。

## 输出 / Output

- `qa/readability/{NNN_slug}.md`
- `qa/imagery/{NNN_slug}.imagery.md`

## `qa/imagery` 必含

| 原文词/短语 | 当前译法 | 问题 | 建议译法 | 理由 |
| --- | --- | --- | --- | --- |

并列出：

- 懒译词警报。
- 过度发挥警报。
- 省字式翻译警报。
- 古典技术语硬译警报，例如“将割”“超过某线”“所对弧之半所对的直线”等。
- 技术说明过度展开警报。
- 修改后的关键句。

## 状态 / State

成功后：

- `current_step = readability_imagery_review_done`

