# 英文到简体中文文学精修策略 / English-to-Simplified-Chinese Literary Refinement

本文件面向 `en-zh-Hans` 模板。它把通用精修策略落实到英文公版书译入简体中文的场景，供 AI 在翻译、审校、返工和最终 EPUB 输出前读取。

This file applies the common refinement policy to English public-domain books translated into Simplified Chinese.

## 基本判断 / Basic Judgment

英文到简体中文的 EPUB 不能只满足“意思大概对”和“文件能打开”。中文读者最终读到的应是一本有中文节奏、历史质地和出版完成度的书。

An English-to-Chinese EPUB is not finished just because the meaning is mostly preserved and the file opens. It must read like a finished Chinese book while preserving the historical texture of the source.

## 精修重点 / Refinement Focus

### 1. 标题 / Titles

- 旧英文纸书目录常用 `--` 串联小题，不能机械译成多个中文 `——`。
- 必须读取完整英文原标题，不得使用被分章脚本截断的标题。
- 必要时建立 `metadata/chapter_title_map.yaml`，包含 `source_full`、`nav_title`、`display_title`、`subtitle`、`title_note`。
- `nav.xhtml` 使用短目录题名，页面内再用主标题和副标题承载完整信息。

English printed-title chains with `--` must not be mechanically converted into Chinese em-dash chains. Use a title map when needed.

### 2. 句子 / Sentences

- 先保事实，再调中文；不得为了“雅”改写事实、情绪、动作强度或叙述立场。
- 英文长句不应直接搬成中文长串；要按中文阅读顺序重排，但保留因果、转折、递进。
- 英文短促句也不能被压成中文动作清单。中文可以紧，但必须像人在叙述。
- 关键句要复核“信、达、雅”：事实不误，中文自足，声调与原文功能相当。

Refinement must preserve facts first, then improve Chinese rhythm. Short source sentences should not become dry Chinese bullet-like prose.

### 3. 段落 / Paragraphs

- 超过 300 字的普通叙述段应进入人工或 AI 专门复核；超过 500 字通常要判断是否拆段。
- 拆段不能破坏原文逻辑。按场景转换、动作阶段、时间推进、人物判断或情绪转折拆分。
- 不能为了“看起来整齐”随意拆段；也不能保留旧纸书中不适合 EPUB 的巨段。

Long paragraphs should be reviewed for mobile readability, but paragraph breaks must respect scene, logic, and narrative rhythm.

### 4. 专名、历史称谓与译注 / Names, Historical Terms, and Notes

- 人名、地名、船名、机构名必须统一。正文中的陌生人名或陌生地名不强制汉译，可以保留英文原名，例如 `Professor Marvin`、`Grant Land`；但章节标题和副标题中的人名优先使用中文译名，英文原名放在正文首次出现处或术语表中。若正文选择中文译名，正文首次出现必须保留英文原名，后文保持一致。章节标题、目录、页眉、图注索引等标题性位置不计入“正文首次出现”；如果人名第一次出现在章节标题里，标题仍只用中文译名，英文原名应延后到正文第一次自然出现处。
- 历史称谓应忠实呈现原书时代语境，同时用译注帮助现代读者理解。
- 不得在同一本书里随意切换称谓，例如一处用旧称、一处用现代称，除非译注策略明确。

Names and historically loaded terms need a stable first-mention and note policy. Less familiar personal names and place names may stay in English; if translated, the first occurrence must preserve the original English name.

### 5. 标点和排版 / Punctuation and Typography

- 普通中文正文不得出现 ASCII 分号 `;`。
- 中文分号 `；` 只能用于真实并列分层，不得机械对应英文分号或连接词。
- 中文字符之间不得保留用于纸书对齐的连续空格。
- 英文原书分章后，常会在译文正文开头或结尾残留重复标题、running title、下一节书名或目录碎片。精修时必须检查每章首尾，正文中不得保留这类副文本残片。
- Project Gutenberg 等英文数字源常带有 `Transcriber's Notes`、OCR correction notes 或源文件尾注。除非本书版本有意保留来源制作说明，否则不要把这些内容混入中文正文；若保留，必须译为清楚标注的“原文转录说明/来源制作说明”，不能让读者误以为是作者正文。
- 附录、名单、表格、页码目录等旧纸书结构，必须转成适合 EPUB 的列表、表格、注释或导航结构。

Chinese punctuation and EPUB typography are publication issues, not cosmetic details.

## 本书目标文档位置 / Book Goal Location

如果某本书已经发现标题、段落、术语、译注、排版或文学精修方面的系统问题，目标文档必须放在：

```text
books/{book_id_slug}/goal/
```

不能放在仓库根目录的通用 `goal/` 下。根目录目标会让 AI 误以为这是项目级任务，而不是某本书的执行目标。

If systematic issues are found in a specific book, the goal document belongs under that book project, not in a repository-level goal directory.

## 模板回填 / Template Backfill

英文到简体中文项目中的可复用经验必须回填到三层：

1. `books/{book_id_slug}/goal/`：记录这本书的具体问题和执行计划。
2. `template/epub_pipeline/common/`：记录所有语言方向都适用的 EPUB、标题、QA、路径和流程规则。
3. `template/epub_pipeline/en-zh-Hans/`：记录英文源文到简体中文的专用问题，例如英文标题链、英文长句干扰、英文称谓和中文译注策略。

这三层可以有必要重复。重复不是浪费，而是为了让不同阶段、不同 agent、不同上下文都能读到关键规则，避免生成过程中跑偏。

These three layers may intentionally overlap. The overlap helps different agents read the right rule at the right execution layer.
