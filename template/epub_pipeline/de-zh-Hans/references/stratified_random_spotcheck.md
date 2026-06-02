# 德语模板分层随机抽检说明 / Stratified Random Spotcheck for de->zh-Hans

本文件用于德语到简体中文项目执行全书抽检闭环，与 `template/epub_pipeline/common/references/stratified_random_spotcheck.md` 对齐。

## 抽检对象与层

- 本体：章节正文段落
- 补充：表格、图片/图注、公式或证明段、注释、术语高风险节点
- 每一轮抽样应覆盖上述层级中至少一个可读样本单元。

## 关键要求

- 样本必须是可复现且可追溯的随机种子（seed、样本明细应入项目档）。
- 至少两个独立评审 Agent 独立判分，任何一位发现 P0/P1/P2 或可读性阻断都触发返工。
- 一旦发现问题，先归类为问题族（family）：
  - 例：`术语链误译族`、`句式拗口族`、`术语与术语表不一致族`、`科学设定细节缺失族`。
- 问题族必须进行本书同类问题全书抽检与修复，再在 `reviews/random_spotcheck/round_x/verification/closure_check.md` 记录闭环。
- 返工后必须使用新 seed 重跑抽检，并在 `validation_report.json` 记录 `require-pass` 成功才可继续。

## 模板内闭环触发条件

- 发现与德语特有结构相关的系统性误译（如复合词误切、可分动词方向错误、否定范围偏移、术语族不一致）时，禁止仅修本样本。
- 必须同步修复 `chapters/final`、`frontmatter`、`nav`、`metadata`、术语表与引用的可读性联动文本，形成整书一致性后再复检。
