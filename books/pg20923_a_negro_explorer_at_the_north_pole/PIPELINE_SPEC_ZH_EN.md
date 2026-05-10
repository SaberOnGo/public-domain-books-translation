# 流水线规范（中英双语） / Pipeline Spec (ZH-EN)

## 1) 输入 / Inputs
- TEMPLATE_ROOT
- SOURCE_URL

## 2) 硬规则 / Hard rules
- 仅可写入 TEMPLATE_ROOT 内文件。
- 每一步结束必须更新 `state/pipeline_state.json`。
- 失败时将 `status=FAILED` 并写入 `last_error`。

## 3) 目录合约 / Directory contract
- `source/source_text.txt`：清洗后的原文
- `chapters/src/{NNN_slug}.md`：分章原文
- `chapters/translated/{NNN_slug}.md`：初译
- `chapters/final/{NNN_slug}.md`：终稿
- `qa/fidelity/*.md`：忠实度审校报告
- `qa/readability/*.md`：可读性审校报告
- `qa/terminology/*.md`：术语一致性报告
- `output/book.epub`：最终电子书
- `output/epubcheck.log`：校验日志

## 4) 命名规则 / Naming rule
- 统一三位序号：`001_xxx.md`、`002_xxx.md`。
- src/translated/final/qa 必须使用同名文件。

## 5) 完成定义 / Done definition
- `output/book.epub` 存在
- `output/epubcheck.log` 无 ERROR
- `state/pipeline_state.json.status == DONE`
