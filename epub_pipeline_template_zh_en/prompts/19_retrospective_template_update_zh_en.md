# 19 全阶段复审与模板经验沉淀 / Full Retrospective and Template Update

## 目的 / Purpose

每本书完成后，AI 必须复审所有阶段，提炼经验教训，并写入该书工程的复盘文件。若这些经验属于通用模板规则，必须给出模板版本递增建议；当用户明确要求更新模板时，写入 `epub_pipeline_template_zh_en` 并递增版本号。

## 输入 / Input

- 全部 `metadata/`
- 全部 `qa/`
- 全部 `preproduction/`
- 全部 `reviews/`
- `state/pipeline_state.json`
- 用户在过程中指出的问题和修正记录。

## 输出 / Output

生成：

- `retrospective/book_retrospective.md`
- `retrospective/template_update_suggestions.md`

模板被用户要求更新时，还要更新：

- `TEMPLATE_VERSION.md`
- `PIPELINE_SPEC_ZH_EN.md`
- 相关 `prompts/*.md`
- 相关 `references/*.md`

## 必须总结的经验 / Required Lessons

- 哪些翻译规则有效。
- 哪些章节质量控制发现了问题。
- 预制作阶段发现了哪些 EPUB 质量问题。
- 封面、字体、metadata、标题、文件体积是否有可复用规则。
- 双 Agent 评审是否发现主执行 AI 漏掉的问题。
- 哪些流程需要改为硬门禁。

## 完成 / Done

只有复审完成并记录后，才可设置：

- `state/pipeline_state.json.status = DONE`
