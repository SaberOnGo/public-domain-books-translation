# 02 分章 / Split Chapters

## 输入 / Input

- `source/source_text.txt`

## 任务 / Tasks

1. 分析目录、章节标题、前言、附录、插图说明。
2. 按阅读逻辑拆成章节文件。
3. 文件名格式：`chapters/src/{NNN_slug}.md`。
4. 生成 `source/toc.json`。
5. 生成或更新 `source/source_manifest.json` 中章节总数。
6. 对日语原书目录、短篇题名、无题分隔、振假名题名或底本页眉残留，必须保留完整原题证据，不得只截取章节文件第一行作为唯一标题证据。

## 输出 / Output

- `chapters/src/*.md`
- `source/toc.json`

## 硬规则 / Hard Rules

- 不得把目录页误拆成正文多章。
- 不得丢失前言、导言、附录。
- 不得把日语原文自然段机械拆成一句一句的段落。青空文库等纯文本来源中的正文行通常是重要段落证据；如果为了整理引号、注记或对白而调整段落，必须在 `qa/textual/` 或章节控制文件中记录理由。
- 不得截断章节标题；若原题含振假名、异读、无题分隔、页眉残留或多层题名，必须在 `source/toc.json` 保留完整源标题和说明，供后续标题策略处理。
- 章节编号必须稳定，后续 `translated/final/qa` 全部同名。

## 状态 / State

成功后：

- `status = SOURCE_SPLIT`
- `current_step = split_chapters`
