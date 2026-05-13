# Chapter Title Policy / 章节标题策略

This file defines language-neutral title and heading rules for EPUB production.

本文件定义 EPUB 制作中通用的章节标题与标题层级规则。

## Why This Exists / 为什么需要

Older public-domain books often use printed-table-of-contents chapter titles that combine several topic labels with dashes. These titles were designed for a paper table of contents, not for small-screen EPUB headings.

许多旧公版书的章节标题是纸书目录式标题，会用多个破折号串起若干小题。这类标题适合纸书目录，不一定适合手机屏幕上的 EPUB 章节页。

## Mandatory Rules / 强制规则

- Do not blindly preserve source title punctuation as display structure.
- 不得机械保留原文标题标点作为成书显示结构。

- Keep a stable canonical title for metadata, navigation, and cross-reference.
- 必须保留稳定的规范题名，用于 metadata、目录和交叉引用。

- For long chapter titles, split title information into:
  - short navigation title,
  - display main title,
  - optional subtitle or title note.
- 长章节标题必须拆分为：
  - 短目录题名，
  - 页面主标题，
  - 可选副标题或标题说明。

- EPUB navigation labels should be concise. Do not put long printed-title chains into `nav.xhtml` if they make navigation hard to scan.
- EPUB 目录标签应简洁。不要把很长的纸书标题链原样放入 `nav.xhtml`，否则目录难以扫读。

- A title that wraps over many lines on a narrow mobile screen must be redesigned before final output.
- 如果标题在手机窄屏上折成多行、压迫正文，最终输出前必须重设标题结构。

- If a chapter title contains a personal name, the title should follow the target-language title style and should not be overloaded with source-name annotations just because it is the first visible occurrence.
- 如果章节标题包含人名，应按目标语言标题习惯处理，不要因为它是读者第一次看见该人名，就把原文名、括注或解释塞进标题。

- Title occurrences do not count as first body occurrences for terminology notes. Apply first-mention notes when the name first appears naturally in the body text.
- 标题中的出现不计入术语译注的“正文首次出现”。首次出现括注或译注应放在该人名第一次自然进入正文的位置。

## Recommended Data Model / 推荐数据模型

When a book has long source titles, maintain a title map:

当一本书存在长原文标题时，应维护标题映射：

```yaml
chapter_titles:
  "004_chapter_i.md":
    source_full: "CHAPTER I THE EARLY YEARS: ..."
    nav_title: "第一章 早年岁月"
    display_title: "第一章 早年岁月"
    subtitle: "学生、船舱侍童、水手、皮里中尉的贴身仆役，以及初赴北极"
    title_note: ""
```

If the build script does not yet support this map, the preproduction stage must still define the intended title structure and mark implementation as required before final EPUB output.

如果构建脚本尚不支持该映射，预制作阶段仍必须定义目标标题结构，并把实现工作列为最终 EPUB 前的必修项。

## Quality Gate / 质量门禁

Before EPUB production, review:

EPUB 制作前必须检查：

- Longest navigation label length.
- 最长目录题名长度。
- Longest displayed heading length.
- 最长页面标题长度。
- Count of dash-like separators in each heading.
- 每个标题中破折号类分隔符数量。
- Mobile preview or generated XHTML inspection for wrapping risk.
- 手机预览或 XHTML 检查中的换行风险。

Any chapter heading that keeps three or more source dash segments should be reviewed by a human editor or a dedicated title-rewrite pass.

任何保留三个及以上原文破折号分段的章节标题，都必须经过人工编辑或专门标题重写流程复核。
