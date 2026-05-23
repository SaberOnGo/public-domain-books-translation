# 模板反馈与回填记录

status: "PASS"

## 已发现并修复

- `ja-zh-Hans/package.json` 初始缺少 `preflight:template`、`cover:check`、`reader:check` 以及 build/release 链式 gate，已回填到 `template/epub_pipeline/ja-zh-Hans/package.json` 并同步本书。
- 通用 `build_epub.js` 未把 `images/cover.jpg` 标记为 OPF `cover-image`，已回填到 `template/epub_pipeline/common/scripts/build_epub.js` 并同步本书。
- 通用 `build_epub.js` 将 EPUB 3 修改时间写成 `dcterms:modified` 元素，EPUBCheck 报 `RSC-005`；已改为 `<meta property="dcterms:modified">...` 并同步本书。
- 发布前复查发现通用 `build_epub.js` 默认按文件名排序前置页，导致 `book_info` 早于 `cover`；同时 OPF metadata 未写入 contributor、publisher、source、description、rights，`nav.xhtml` 也没有 landmarks。已回填 common 构建脚本并同步本书。

## 本书侧处理

当前书籍先完成本地修复，再用 npm gate 验证。没有把具体书籍原文、译文、QA 或 metadata 写回 template。
