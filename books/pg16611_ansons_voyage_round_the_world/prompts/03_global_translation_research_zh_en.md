# 03 通用翻译研究 / Global Translation Research

## 输入 / Input

- `references/translation_research_universal.md`
- `references/quality_standard.md`
- `references/english_source_notes.md`
- `template/epub_pipeline/targets/zh-Hans/quality_framework/README.md`

## 任务 / Tasks

1. 读取通用翻译研究和质量标准。
2. 检查本工程是否已包含以下硬规则：
   - 生动必须有依据。
   - 简洁必须有气息。
   - 形象词优先，但不能越界发挥。
   - 不能省字式翻译。
   - 预翻译失败必须回溯。
3. 生成 `qa/benchmark/global_research_ack.md`，说明本次工程采用的通用翻译规则。

## 输出 / Output

- `qa/benchmark/global_research_ack.md`

## 状态 / State

成功后：

- `status = GLOBAL_RESEARCH_DONE`
- `current_step = global_translation_research_acknowledged`

