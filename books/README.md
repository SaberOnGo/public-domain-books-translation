# Shared Book Tooling / 书籍共享工具

The concrete book projects live under target-language directories, such as `zh-Hans/1_pg20923_a_negro_explorer_at_the_north_pole/`.

具体书籍工程按目标语言分目录存放，例如 `zh-Hans/1_pg20923_a_negro_explorer_at_the_north_pole/`。

## New Book Directories / 新书目录

Create new projects through the shared script so the numeric prefix is assigned consistently:

```powershell
cd books
npm run new:book -- pg20923_a_negro_explorer_at_the_north_pole --source-target en-zh-Hans
```

新书必须通过共享脚本创建，这样数字前缀才会按目标语言目录自动递增：

```powershell
cd books
npm run new:book -- pg20923_a_negro_explorer_at_the_north_pole --source-target en-zh-Hans
```

The result is `books/{target}/{number}_{book_id_slug}/`, for example `books/zh-Hans/1_pg20923_a_negro_explorer_at_the_north_pole/`. Do not manually choose the number unless you are repairing a documented migration.

结果目录是 `books/{target}/{number}_{book_id_slug}/`，例如 `books/zh-Hans/1_pg20923_a_negro_explorer_at_the_north_pole/`。除非是在修复有记录的迁移问题，否则不要手工指定数字。

Current Simplified Chinese book projects:

- `books/zh-Hans/1_pg20923_a_negro_explorer_at_the_north_pole/`
- `books/zh-Hans/2_pg10966_the_ghost_pirates/`
- `books/zh-Hans/3_pg19141_edisons_conquest_of_mars/`
- `books/zh-Hans/4_pg16611_ansons_voyage_round_the_world/`
- `books/zh-Hans/5_pg3479_the_metal_monster/`

当前简体中文书籍工程：

- `books/zh-Hans/1_pg20923_a_negro_explorer_at_the_north_pole/`
- `books/zh-Hans/2_pg10966_the_ghost_pirates/`
- `books/zh-Hans/3_pg19141_edisons_conquest_of_mars/`
- `books/zh-Hans/4_pg16611_ansons_voyage_round_the_world/`
- `books/zh-Hans/5_pg3479_the_metal_monster/`

## Node.js Dependencies / Node.js 依赖

Install Node.js tooling once in this directory:

```powershell
cd books
npm install
```

Node dependencies are shared by all book projects through `books/node_modules/`. Do not install a separate `node_modules/` inside each book directory unless a book truly needs a private toolchain and records the reason in its QA or retrospective notes.

Node 依赖统一安装在 `books/node_modules/`，供所有书籍工程共享。不要在每本书目录内重复安装 `node_modules/`；只有某本书确实需要私有工具链时，才可例外，并且必须在该书的 QA 或复盘记录中说明原因。

From a book directory, normal scripts still run locally:

```powershell
cd books/zh-Hans/2_pg10966_the_ghost_pirates
npm run lint:publication
npm run build:epub
npm run check:epub
```

在具体书籍目录中，仍然按本书工程执行脚本；脚本会向上查找共享依赖目录。

## Scope / 写入范围

`books/package.json`, `books/package-lock.json`, `books/scripts/`, and ignored `books/node_modules/` are shared tooling only. Source text, translations, QA records, metadata, EPUB files, and other book-specific outputs must remain under `books/{target}/{number}_{book_id_slug}/`.

`books/package.json`、`books/package-lock.json`、`books/scripts/` 和被 Git 忽略的 `books/node_modules/` 只用于共享工具。原文、译文、QA、metadata、EPUB 等具体书籍产物仍必须写入 `books/{target}/{number}_{book_id_slug}/`。
