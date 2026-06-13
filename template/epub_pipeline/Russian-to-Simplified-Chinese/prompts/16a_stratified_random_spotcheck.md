# 16a 分层随机抽检

在完成第一版 EPUB 或每次 post-EPUB 精修后执行，要求全书读者可见单元的分层抽检闭环（段落、表格、图像、公式/证明块、图注、注释）。

## 执行要点

- 运行共同门禁脚本并记录：
  - `reviews/random_spotcheck/round_x/random_sample_manifest.json`
  - `reviews/random_spotcheck/round_x/validation_report.json`
- 至少两位独立评审 Agent 分别覆盖样本；
  - 任何 P0/P1/P2、读者不可读、事实/术语错误立即打断并提交流程。
- 发现问题后先归类问题族，先在全书范围复查同类问题，再修复确认；
  - 修复结果须写入 `reviews/random_spotcheck/round_x/fixes/fix_log.md`。
- 修复后使用新 seed 复检，只有新的 `validation_report.json` 达到 PASS 且 `require-pass` 为 true 时，才进入后续交付。

## 质量边界

- 不可将抽检结果仅用于采样段修复；不得把“抽检通过”作为本轮全书无系统性问题的证据。
- 若有俄语特有结构问题（格关系误判、体貌/运动动词误译、分词/副动词链硬译、否定范围、术语族不一致）触发，必须全书同类问题排查并闭环后再复抽。
