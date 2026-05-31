---
name: de-zh-Hans
description: Use this template when translating German public-domain or licensed source texts into Simplified Chinese EPUBs, especially literature, speculative fiction, nonfiction, social thought, and classic prose.
---

# 德语到简体中文 EPUB 模板 Skill

使用场景：用户要把德语公版或授权原文翻译成简体中文，并制作可发布 EPUB。

## 执行顺序

1. 读取仓库根目录 `AGENTS.md`。
2. 读取 `template/epub_pipeline/README.md`、`common/README.md` 和 `targets/zh-Hans/quality_framework/README.md`。
3. 读取本目录 `AGENTS.md`、`README.md` 和 `references/` 下的德语专项规则。
4. 使用 `books/scripts/create_book_project.py` 创建工程，复制顺序为 `common -> de-zh-Hans`；若书籍属于专业/学术控制对象，再叠加合适 profile。
5. 记录 `metadata/source_evidence.md` 和 `metadata/rights_checklist.md`，权利不清楚则停止。
6. 完成本书专项研究、文体画像、术语表、预翻译试译和小样本测试。
7. 分章翻译，每章立即生成 `qa/chapter_controls/{chapter}.control.md`，再做忠实度、可读性、术语、意象/读者可见内容和章节门禁。
8. 生成 EPUB，运行出版 lint、资源检查、EPUBCheck、分层随机抽检、独立评审、版本化 release。
9. 将可复用经验写回本模板的 `retrospective_lessons.md` 或对应 reference；书籍专属经验留在具体书籍工程。

## 德语翻译重点

- 先判断句法骨架，再翻译修辞。
- 把德语框架结构、长定语链和复合词改成中文读者能跟上的动作、因果和承接。
- 核对可分动词、情态动词、否定作用域、虚拟式和代词回指。
- 保留德语散文的节奏，但不保留让中文拗口的逗号串联。
- 科学技术词、天文学词、政治/社会词和虚构文明设定必须稳定，不能为了文采随意换词。
- 原词呈现从严控制；正文不默认写 `中文译名（deutscher Begriff）`。
