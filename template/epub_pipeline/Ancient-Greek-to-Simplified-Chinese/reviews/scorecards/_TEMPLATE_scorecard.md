# 古希腊文到简体中文评审评分表模板 / Ancient Greek Review Scorecard Template

book_title: "{title}"
reviewer: "Agent A or Agent B"
review_date: "YYYY-MM-DD"
total_score: 0
pass_status: "FAIL" # PASS | FAIL

## 评分维度 / Score Dimensions

| 维度 | 分值 | 得分 | 说明 |
|---|---:|---:|---|
| 来源、版权与底本清晰度 | 12 | 0 | 公版状态、底本版本、编辑者、扫描/OCR/转写状态、source witness 是否清楚 |
| 古希腊文忠实度 | 14 | 0 | 是否从古希腊文底本翻译，语法、指代、论证、语气是否准确 |
| 文本不确定性处理 | 12 | 0 | 异文、残损、拟补、OCR 不确定、语法歧义是否记录并合理处理 |
| 参考译本边界 | 10 | 0 | 第二语言译本是否只作校读证据，是否避免直接转译和版权表达复制 |
| 专名与术语一致性 | 12 | 0 | 古希腊文原名、转写、中文译名、技术术语是否全书稳定 |
| 中文可读性 | 12 | 0 | 中文是否自然、清楚、有文类感，不保留希腊文句法外壳 |
| 标题、译注与章节结构 | 8 | 0 | 标题来源、nav/display/subtitle、译注和章节层级是否清楚 |
| 章节质量控制 | 8 | 0 | 每章 control/gate、反馈和回退是否闭环 |
| EPUB 工程质量 | 12 | 0 | OPF、nav、spine、cover-image、epubcheck、字体、排版和移动端可读性 |

## P0/P1 问题 / Blocking Issues

- P0：版权边界不清、无古希腊文底本、参考译本转译、严重误读、关键异文未处理、整章漏译。
- P1：术语/专名漂移、source witness 记录缺失、局部未解决异文、标题来源混乱、EPUB 校验错误。

## 评审结论 / Review Conclusion

- `PASS`：总分 >= 88 且无 P0/P1。
- `FAIL`：总分 < 88 或存在 P0/P1。

## 详细意见 / Detailed Findings

逐条列出问题、位置、影响、建议回退阶段。

