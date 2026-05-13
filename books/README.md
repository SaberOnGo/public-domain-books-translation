# Shared Book Tooling / 书籍共享工具

The concrete book projects live in sibling directories such as `pg10966_the_ghost_pirates/` and `pg20923_a_negro_explorer_at_the_north_pole/`.

具体书籍工程放在同级目录中，例如 `pg10966_the_ghost_pirates/` 和 `pg20923_a_negro_explorer_at_the_north_pole/`。

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
cd books/pg10966_the_ghost_pirates
npm run lint:publication
npm run build:epub
npm run check:epub
```

在具体书籍目录中，仍然按本书工程执行脚本；脚本会向上查找共享依赖目录。

## Scope / 写入范围

`books/package.json`, `books/package-lock.json`, and ignored `books/node_modules/` are shared tooling only. Source text, translations, QA records, metadata, EPUB files, and other book-specific outputs must remain under `books/{book_id_slug}/`.

`books/package.json`、`books/package-lock.json` 和被 Git 忽略的 `books/node_modules/` 只用于共享工具。原文、译文、QA、metadata、EPUB 等具体书籍产物仍必须写入 `books/{book_id_slug}/`。
