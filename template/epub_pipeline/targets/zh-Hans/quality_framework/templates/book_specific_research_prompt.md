# 本书专项翻译研究 Prompt

你是本书中文译本的总编辑。正式试译前，必须先完成本书专项翻译研究。此阶段不是翻译正文，而是建立这一本书独有的翻译判断。

## 输入

- 简体中文目标语言通用研究：`template/epub_pipeline/targets/zh-Hans/quality_framework/references/research_digest.md`
- 简体中文目标语言质量标准：`template/epub_pipeline/targets/zh-Hans/quality_framework/references/quality_standard.md`
- 原书全文：`source/source_text.txt`
- 章节列表：`source/source_manifest.json`
- 元数据：`metadata/book.yaml`
- 初始术语表：`glossary/terms.csv`

## 输出到

`metadata/book_specific_translation_research.md`

## 必须回答

```markdown
# 本书专项翻译研究：{书名}

## 这本书的翻译难点

1.
2.
3.

## 不能照搬通用规则的地方

说明本书在哪些地方需要特殊判断。

## 本书关键词分层

| 类型 | 原文 | 推荐译法 | 是否可变 | 判断理由 |
| --- | --- | --- | --- | --- |
| 核心身份词 |  |  |  |  |
| 象征词 |  |  |  |  |
| 场景词 |  |  |  |  |
| 技术词 |  |  |  |  |
| 历史敏感词 |  |  |  |  |

## 本书句法策略

- 长句：
- 动作句：
- 说明句：
- 修辞句：
- 口语/日记句：

## 本书意象策略

哪些词必须翻出画面，而不是解释。

## 试译样本选择

| 样本 | 位置 | 为什么必须试译 | 通过标准 |
| --- | --- | --- | --- |

## 进入预翻译阶段的条件

列出明确条件。
```

