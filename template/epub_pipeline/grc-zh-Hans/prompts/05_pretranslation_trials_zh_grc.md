# 05 预翻译试译 / Pretranslation Trials

## 输入 / Input

- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `metadata/source_witness_manifest.md`
- `qa/textual/textual_uncertainty_log.md`
- `glossary/terms.csv`
- `source/toc.json`
- `chapters/src/*.md`

## 任务 / Tasks

若 `metadata/style_profile.md` 不存在或为空，说明上一步未完成，必须停止并回到 `04_book_specific_research_zh_grc.md`。

在正式分章翻译前，必须建立 `qa/pretranslation/` 并完成 3-5 个试译样本。

至少包含：

1. 开篇/定调段。
2. 高现场感或动作段。
3. 长周期句或分词链密集段。
4. 术语/历史敏感段。
5. 存在异文、残损、拟补、OCR 不确定或参考译本分歧的段落。
6. 修辞强、结尾强或象征物强的句子。

每个样本输出：

- `qa/pretranslation/source_{case_id}.md`
- `qa/pretranslation/trial_{case_id}.md`

每个 `trial` 必须包含：

1. 原文。
2. 原文功能判断。
3. 直译风险。
4. 关键词译法选择。
5. A 忠实版。
6. B 中文可读版。
7. C 文学打磨版。
8. D 终稿候选。
9. 为什么 D 更适合作为正文。
10. 意象增强边界自检。
11. 省字式翻译自检。
12. 古希腊文底本依据和第二语言参考译本差异说明。
13. 异文、残损、拟补或 OCR 不确定处处理记录。
14. `PASS` 或 `FAIL`。

## 失败回溯 / Failure Rollback

- 通用规则不足：修改 `references/translation_research_universal.md` 或 `references/quality_standard.md`。
- 本书判断不足：修改 `metadata/book_specific_translation_research.md`。
- 个别表达不足：保留失败 trial，生成 V2/V3，直到 PASS。

失败记录不得删除。

## 总报告 / Report

生成：

- `qa/pretranslation/pretranslation_report.md`

报告必须列出所有 trial 的 PASS/FAIL、失败原因、最终是否允许正式分章翻译。

## 状态 / State

如果任何样本未通过：

- `status = PRETRANSLATION_FAILED`
- `current_step = pretranslation_failed`
- 不得继续 `07_translate_chapters`

全部通过：

- `status = PRETRANSLATION_PASS`
- `current_step = pretranslation_pass`
