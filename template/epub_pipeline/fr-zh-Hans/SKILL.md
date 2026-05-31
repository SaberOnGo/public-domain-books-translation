---
name: fr-zh-Hans
description: Use this template when translating French public-domain or licensed source texts into Simplified Chinese EPUBs, especially literary nonfiction, natural history, travel, social thought, and classic prose.
---

# 法语到简体中文 EPUB 模板 Skill

使用场景：用户要把法语公版或授权原文翻译成简体中文，并制作可发布 EPUB。

## 执行顺序

1. 读取仓库根目录 `AGENTS.md`。
2. 读取 `template/epub_pipeline/README.md`、`common/README.md` 和 `targets/zh-Hans/quality_framework/README.md`。
3. 读取本目录 `AGENTS.md`、`README.md` 和 `references/` 下的法语专项规则。
4. 使用 `books/scripts/create_book_project.py` 创建工程，复制顺序为 `common -> fr-zh-Hans`；若书籍属于专业/学术控制对象，再叠加合适 profile。
5. 记录 `metadata/source_evidence.md` 和 `metadata/rights_checklist.md`，权利不清楚则停止。
6. 完成本书专项研究、文体画像、术语表、预翻译试译和小样本测试。
7. 分章翻译，每章立即生成 `qa/chapter_controls/{chapter}.control.md`，再做忠实度、可读性、术语、意象/读者可见内容和章节门禁。
8. 生成 EPUB，运行出版 lint、资源检查、EPUBCheck、分层随机抽检、独立评审、版本化 release。
9. 将可复用经验写回本模板的 `retrospective_lessons.md` 或对应 reference；书籍专属经验留在具体书籍工程。

## 法语翻译重点

- 先判断句法骨架，再翻译修辞。
- 把法语抽象名词链改成中文读者能跟上的动词、因果和承接。
- 保留法语散文的节奏，但不保留让中文拗口的逗号串联。
- 自然科学词、地理词、政治/社会词必须稳定，不能为了文采随意换词。
- 原词呈现从严控制；正文不默认写 `中文译名（terme francais）`。
