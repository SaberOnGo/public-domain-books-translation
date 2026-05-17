# Book I 预翻译计划 / Pretranslation Plan

plan_status: `READY_FOR_SOURCE_INGESTION`

## 样本选择

1. 宇宙结构与地球位置段落。
2. 基础几何证明段落。
3. 弦表/角度计算段落。
4. 含图形引用的证明段落。
5. 参考译本理解分歧段落。

## 每个样本必须输出

- `qa/pretranslation/source_{case_id}.md`
- `qa/pretranslation/trial_{case_id}.md`

## 每个 trial 必须包含

1. 古希腊文原文位置。
2. source witness 和版本信息。
3. 直译风险。
4. 术语表引用。
5. 候选中文译文。
6. 数学证明链检查。
7. 天文学模型检查。
8. 图表/数值检查。
9. 参考译本差异摘要。
10. 古今概念边界注释。
11. PASS/FAIL。

## 禁止

- 禁止把任何 trial 直接复制进 `chapters/translated/`。
- 禁止无数学/天文学校对的 PASS。
- 禁止以参考译本为底稿生成 trial。

