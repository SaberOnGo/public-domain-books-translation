---
description: Create or plan a new numbered book project through the shared script.
agent: book-runner
---

根据参数 `$ARGUMENTS` 创建或规划一个新的公版书翻译工程。

执行前必须：

1. 读取 `AGENTS.md`。
2. 读取 `template/epub_pipeline/README.md` 和 `template/epub_pipeline/common/README.md`。
3. 根据参数判断 `book_id_slug`、`source-target`、目标语言 `{target}`，并读取对应的 `template/epub_pipeline/{source-target}/AGENTS.md`、`SKILL.md`、`README.md`。
4. 如果存在目标语言规则，读取 `template/epub_pipeline/targets/{target}/`。

边界：

- 必须使用 `books/scripts/create_book_project.py` 或 `books` 下现有 npm wrapper。
- 新工程路径必须是 `books/{target}/{number}_{book_id_slug}/`。
- 不要把具体书籍内容写入 `template/`。
- 版权或公版状态不清楚时停止。

如果 `$ARGUMENTS` 不足以创建工程，只输出缺少的具体参数和推荐命令，不要猜测。
