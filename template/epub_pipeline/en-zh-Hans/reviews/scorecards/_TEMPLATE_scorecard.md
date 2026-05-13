# 评审评分表模板 / Review Scorecard Template

book_title: "{title}"
reviewer: "Agent A or Agent B"
review_date: "YYYY-MM-DD"
total_score: 0
pass_status: "FAIL" # PASS | FAIL

## 评分维度 / Score Dimensions

| 维度 | 分值 | 得分 | 说明 |
|---|---:|---:|---|
| 来源与版权清晰度 | 10 | 0 | 原文来源、公版状态、URL、版本证据是否清楚 |
| 翻译忠实度 | 15 | 0 | 是否忠实事实、语气、叙事关系 |
| 中文可读性 | 15 | 0 | 是否自然、有叙述气息、无机械味 |
| 文学与画面感 | 10 | 0 | 关键句是否有记忆点，同时不越界发挥 |
| 术语与专名一致性 | 10 | 0 | 人名、地名、术语、年代、数字是否一致 |
| 章节质量控制 | 10 | 0 | 每章 control/gate 是否完整，反馈是否闭环 |
| 封面与书籍信息 | 10 | 0 | 封面、书籍信息、作者信息、LifeBook 书坊 + 个人名、公版 URL 是否完整 |
| 字体与排版 | 10 | 0 | 字体策略、标题层级、正文行距、移动端可读性 |
| EPUB 工程质量 | 10 | 0 | OPF、nav、spine、cover-image、epubcheck、体积控制 |

## P0/P1 问题 / Blocking Issues

- P0：必须立即停止发布的问题。
- P1：必须修复后才能进入最终输出的问题。

## 评审结论 / Review Conclusion

- `PASS`：总分 >= 85 且无 P0/P1。
- `FAIL`：总分 < 85 或存在 P0/P1。

## 详细意见 / Detailed Findings

逐条列出问题、位置、影响、建议回退阶段。
