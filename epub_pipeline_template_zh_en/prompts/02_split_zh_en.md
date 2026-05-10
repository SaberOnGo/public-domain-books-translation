# 02 分章 / Split Chapters

## 输入 / Input

- `source/source_text.txt`

## 任务 / Tasks

1. 分析目录、章节标题、前言、附录、插图说明。
2. 按阅读逻辑拆成章节文件。
3. 文件名格式：`chapters/src/{NNN_slug}.md`。
4. 生成 `source/toc.json`。
5. 生成或更新 `source/source_manifest.json` 中章节总数。

## 输出 / Output

- `chapters/src/*.md`
- `source/toc.json`

## 硬规则 / Hard Rules

- 不得把目录页误拆成正文多章。
- 不得丢失前言、导言、附录。
- 章节编号必须稳定，后续 `translated/final/qa` 全部同名。

## 状态 / State

成功后：

- `status = SOURCE_SPLIT`
- `current_step = split_chapters`

