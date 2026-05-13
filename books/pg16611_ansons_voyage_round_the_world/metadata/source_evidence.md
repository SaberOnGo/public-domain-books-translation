# 来源证据 / Source Evidence

书籍工程：`books/pg16611_ansons_voyage_round_the_world/`

## 来源

- Project Gutenberg 条目：https://www.gutenberg.org/ebooks/16611
- UTF-8 纯文本：https://www.gutenberg.org/ebooks/16611.txt.utf-8
- 本地保存：`source/source_text_raw.txt`
- 本地拆章清单：`source/toc.json`
- 本地来源 manifest：`source/source_manifest.json`

## Gutenberg 条目记录

- Gutenberg 标题：`Anson's Voyage Round the World`
- Gutenberg 作者字段：`Richard Walter`
- Gutenberg 注释/评注字段：`H. W. Household`
- Gutenberg 主题人物：`George Anson, Baron Anson, 1697-1762`
- 电子书编号：`16611`
- 语言：English
- 发布日期：2005-08-28
- 最近更新：2020-12-12
- 页面版权状态：Public domain in the USA.

## 处理说明

本项目只使用 Project Gutenberg 提供的英文公版原文，不使用现代中文译本、商业 EPUB、现代注释版或来源不明文本。中文译制署名为 `LifeBook 书坊 SaberOnGo`。

Gutenberg 页面将 Richard Walter 标为作者，将 George Anson 标为主题人物。用户提供的“作者：George Anson”与来源页面作者字段不完全一致，因此本工程在 metadata 中保留两者关系：`creator` 记录 Richard Walter，`subject_person` 记录 George Anson，中文题名采用用户指定的《环球航海记》。

清洗时剥离了 Gutenberg 许可证尾注和纸书式目录页，不把 `NOTES` 目录占位误拆为正文，正文保留编辑导言、40 章和术语表。
