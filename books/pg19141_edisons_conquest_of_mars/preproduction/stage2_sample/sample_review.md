# 样章 EPUB 检查 / Sample EPUB Review

status: "PASS"
sample_basis: "cover, book-info, 001_front_matter.md, 002_chapter_i.md"

## 检查项目

- 标题策略：PASS。目录短题名为“卷首”“第一章”等，未添加原文不支持的概括标题。
- 中文排版：PASS。段落缩进、标题层级和中文标点符合目标语言规则。
- 元数据：PASS。书名、作者、译者、来源和 rights 已写入构建脚本与 `metadata/book.yaml`。
- 文本质量：PASS。样章已通过章节 QA，第一章经出版 lint 修正分号阈值问题。

## Decision

PASS. 可制作整本 EPUB。
