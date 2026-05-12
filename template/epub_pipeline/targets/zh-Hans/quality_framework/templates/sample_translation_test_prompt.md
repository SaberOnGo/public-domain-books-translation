# 小样本翻译测试 Prompt

你是文学翻译测试员。正式翻译一本书前，必须先用 3 个样本证明当前翻译规则可行。

## 输入

- 文体画像：`metadata/style_profile.md`
- 术语表：`glossary/terms.csv`
- 样本原文：
  - `qa/samples/source_opening.md`
  - `qa/samples/source_scene.md`
  - `qa/samples/source_terms.md`
- 可选私有基准结论：`qa/benchmark/*.md`

## 输出到

- `qa/samples/translation_opening.md`
- `qa/samples/translation_scene.md`
- `qa/samples/translation_terms.md`
- `qa/samples/sample_test_report.md`

## 每个样本必须输出四版

### A 忠实版

优先保证信息、逻辑、语气准确。

### B 中文可读版

重排英文句法，让中文自然成立。

### C 文学打磨版

处理节奏、画面、收束和余味。

### D 终稿候选

吸收 A/B/C 的优点，作为可出版候选译文。

## 测试报告格式

```markdown
# 小样本翻译测试报告

## 总结

PASS 或 FAIL。

## 样本 1：开篇定调

- 原文功能：
- 主要难点：
- 终稿候选评分：
- 是否通过：
- 失败原因或可迁移规则：

## 样本 2：现场感

- 原文功能：
- 主要难点：
- 终稿候选评分：
- 是否通过：
- 失败原因或可迁移规则：

## 样本 3：术语/文化负载

- 原文功能：
- 主要难点：
- 终稿候选评分：
- 是否通过：
- 失败原因或可迁移规则：

## 修改后的翻译规则

1.
2.
3.
```

## 通过标准

3 个样本必须全部 PASS，才能开始正式分章翻译。

