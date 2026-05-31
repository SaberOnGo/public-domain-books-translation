---
name: it-zh-Hans
description: Use this template when translating Italian public-domain or licensed source texts into Simplified Chinese EPUBs, especially adventure fiction, literary fiction, travel prose, social novels, and classic Italian prose.
---

# 意大利语到简体中文 EPUB 模板 Skill

使用场景：用户要把意大利语公版或授权原文翻译成简体中文，并制作可发布 EPUB。

## 执行顺序

1. 读取仓库根目录 `AGENTS.md`。
2. 读取 `template/epub_pipeline/README.md`、`common/README.md` 和 `targets/zh-Hans/quality_framework/README.md`。
3. 读取本目录 `AGENTS.md`、`README.md` 和 `references/` 下的意大利语专项规则。
4. 使用 `books/scripts/create_book_project.py` 创建工程，复制顺序为 `common -> it-zh-Hans`；若书籍确属某个 profile，再叠加合适 profile。没有匹配 profile 时，应在书籍工程记录“不使用 profile 的理由”，不得硬套。
5. 记录 `metadata/source_evidence.md`、`metadata/rights_checklist.md` 和 `metadata/italian_source_profile.md`；权利不清楚则停止。
6. 完成本书专项研究、文体画像、术语表、预翻译试译和小样本测试。
7. 分章翻译，每章立即生成并执行 `qa/chapter_controls/{chapter}.control.md`，再做忠实度、可读性、术语、意象/读者可见内容和章节门禁。
8. 生成 EPUB，运行出版 lint、资源检查、封面检查、读者可见内容检查、EPUBCheck、分层随机抽检、独立评审和版本化 release。
9. 将可复用意大利语经验写回本模板的 `retrospective_lessons.md` 或对应 reference；书籍专属经验留在具体书籍工程。

## 意大利语翻译重点

- 先判断句法骨架，再翻译叙事速度、动作和声调。
- 冒险小说要保留现场感、危险推进、人物称谓和海事/殖民语境，但不能为了刺激而新增原文没有的暴力、色情或道德评语。
- 意大利语修辞性倒装、长插入语和感叹句可按中文节奏重排；中文必须能朗读。
- 专名、地名、族群名、宗教名、殖民机构、船名和头衔必须稳定，不能为了文采随意换词。
- 原词呈现从严控制；正文不默认写 `中文译名（termine italiano）`。
