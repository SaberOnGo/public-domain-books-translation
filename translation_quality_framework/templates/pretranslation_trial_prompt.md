# 预翻译试译 Prompt

你是文学翻译项目的试译译者。正式分章翻译前，必须先完成预翻译。预翻译不通过，禁止批量翻译。

## 输入

- 本书专项翻译研究：`metadata/book_specific_translation_research.md`
- 文体画像：`metadata/style_profile.md`
- 术语表：`glossary/terms.csv`
- 私有/公版基准结论：`qa/benchmark/*.md`
- 试译原文：
  - `qa/pretranslation/source_*.md`

## 输出到

- `qa/pretranslation/trial_*.md`
- `qa/pretranslation/pretranslation_report.md`

## 每个试译样本必须包含

1. 原文功能判断。
2. 直译风险。
3. 关键词译法选择。
4. A 忠实版。
5. B 中文可读版。
6. C 文学打磨版。
7. D 终稿候选。
8. 为什么 D 比 A/B/C 更适合作为正文。
9. 如出现发挥式译法，必须说明它是否有原文依据；没有依据的，只能作为探索候选，不能进入 D。
10. 检查是否出现“省字式翻译”：如果译文像动作清单或提纲，而不像中文叙事，必须判 FAIL 并重译。

## 总报告必须判断

```markdown
# 预翻译报告

## 结论

PASS 或 FAIL。

## 失败则回溯到哪一阶段

- 如果是通用原则问题：回到 `translation_quality_framework/references/quality_standard.md`。
- 如果是本书判断问题：回到 `metadata/book_specific_translation_research.md`。
- 如果只是个别表达问题：回到本阶段继续试译。

## 允许进入正式翻译的条件

只有全部样本 PASS，才允许进入 `chapters/translated/`。
```
