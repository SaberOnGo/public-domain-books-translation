# LifeBook Digest Workflow

LifeBook Digest 是 `output/book.epub` 之后的可选后处理模块，不是翻译主流程的一部分。它的边界是：

1. 输入已经生成的标准 EPUB。
2. 读取 EPUB 的 OPF、spine、nav 和 XHTML 正文。
3. 生成 `output/digest/` 中的 Digest XHTML、章节拓扑、知识脉络图、agent 输入包和状态文件。
4. 生成 `qa/digest/` 中的报告和审校清单。
5. 只有当书籍工程配置允许时，才把 Digest 作为一个新增章节合并进新的标准 EPUB。

## 自动判断规则

用户或书籍工程未声明是否启用 Digest 时，模块可以进入 `auto` 模式：

- 长篇小说、专业书籍、哲学书：生成 Digest。
- 短篇小说、自然科学类和其他不在上述范围内的书：跳过。
- 自动判断只决定是否生成 Digest；是否合并进 EPUB 仍由 `digest.config.json` 控制。

## 输出边界

- 旁路输出：`output/digest/`
- QA 输出：`qa/digest/`
- 合并输出：默认 `output/book_digest.epub`
- 不输出专用阅读器格式。
- 不把具体书籍内容写入仓库根目录 `digest/`。

## 发布边界

Digest 是读者可见内容。若合并进 EPUB：

- 必须更新 OPF manifest、spine、nav。
- 必须重新运行 EPUB 结构校验。
- 必须对 Digest 章节做专项 QA。
- 若进入 release，必须生成新版本产物，不能复用旧 release 文件名代表不同内容。

已有正文不需要重新翻译，也不需要因为新增 Digest 而重跑整本翻译流程。
