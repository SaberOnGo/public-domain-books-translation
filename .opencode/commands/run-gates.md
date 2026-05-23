---
description: Run or plan common publication gates inside one book project.
agent: book-runner
---

在 `$ARGUMENTS` 指定的书籍工程目录内运行或规划通用出版门禁。

执行前必须：

1. 读取 `AGENTS.md`。
2. 读取 `template/epub_pipeline/README.md`、`template/epub_pipeline/common/README.md`。
3. 在书籍工程内核对是否存在复制后的 `scripts/`、`package.json`、`metadata/`、`chapters/`、`qa/`。
4. 若已有旧 EPUB 或 staging 输出，按 `AGENTS.md` 要求先清理或重新生成 staging，避免旧 XHTML、旧链接或旧资源污染门禁结果。

默认门禁命令应来自书籍工程自身脚本和 common 规则，包括但不限于：

```powershell
python scripts/check_template_workflow_gate.py --write-report
node scripts/publication_lint.js --target={target-language} --write-report
node scripts/asset_manifest_check.js --write-report
python scripts/check_cover_output_assets.py --write-report
python scripts/check_reader_facing_policy.py --write-report
```

不要把命令写死到某个本机绝对路径；所有路径必须从当前书籍工程或仓库根目录解析。
