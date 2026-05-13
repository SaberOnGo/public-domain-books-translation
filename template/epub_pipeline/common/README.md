# Common EPUB Pipeline / EPUB 通用流水线

This directory contains shared workflow files for all language-pair templates.

本目录包含所有语言方向模板共享的工作流文件。

## Contents / 内容

- `PIPELINE_SPEC.md`: state machine, project directory contract, naming rules, and done definition.
- `automation_contract.md`: automation and template-protection rules.
- `metadata/rights_checklist.md` and `metadata/source_evidence.md`: source and public-domain evidence templates.
- `preproduction/`: shared EPUB preproduction templates.
- `references/`: language-neutral title, literary refinement, quality gate, and benchmark policies.
- `scripts/`: reusable chapter splitting, Markdown normalization, publication lint, and refinement-check helpers.
- `package.json`: book-local npm script template only; shared dependencies are installed once under `books/`.
- `state/`: initial pipeline state and human-feedback control files.
- `Makefile`: generic EPUB build/check entry points.

目标语言质量框架放在 `template/epub_pipeline/targets/{target}/`。源语言到目标语言的专用模板只应在确实需要不同翻译、排版或评审规则时覆盖或扩展 common 文件。

Target-language quality frameworks live under `template/epub_pipeline/targets/{target}/`. Source-to-target-specific templates should override or extend common files only when the direction needs different translation, typography, or review rules.

## Shared Tooling / 共享工具

Node.js dependencies for EPUB building and validation are repository-level book tooling. Install them once from `books/`:

```powershell
cd books
npm install
```

Do not install a duplicate `node_modules/` inside every `books/{book_id_slug}/` directory. Book-local `package.json` files keep only scripts; scripts such as `scripts/run_epubcheck.js` must resolve tools by walking up to the shared `books/node_modules/`.

Node.js 依赖属于书籍区共享工具，应在 `books/` 下统一安装一次：

```powershell
cd books
npm install
```

不要在每个 `books/{book_id_slug}/` 目录里重复安装 `node_modules/`。具体书籍的 `package.json` 只保留脚本；`scripts/run_epubcheck.js` 等脚本必须向上查找共享的 `books/node_modules/`。

## Publication Lint / 出版文本检查

Before building a final EPUB, run:

```powershell
node scripts/publication_lint.js --target={target-language} --write-report
```

在构建最终 EPUB 前必须运行：

```powershell
node scripts/publication_lint.js --target={target-language} --write-report
```

This check is common because encoding damage, legacy print tables of contents, repeated spacing, and path portability problems can affect any language.

这项检查属于通用层，因为编码污染、旧纸书页码目录、连续空格和路径可移植性问题可能影响任何语言方向。

## Refinement Check / 精修复查

After a full EPUB has been built, run the reusable refinement scan from the book project root:

```powershell
node scripts/refinement_check.js
```

整本 EPUB 构建后，应在书籍工程根目录运行可复用精修扫描：

```powershell
node scripts/refinement_check.js
```

The report is written to `qa/refinement/refinement_check.json`. It separates reader-facing publication files from raw source evidence, so original downloaded source files can be preserved while EPUB-facing text stays clean.

报告会写入 `qa/refinement/refinement_check.json`。它会区分面向读者的出版文本和原始来源证据，因此既能保留下载原文的原貌，也能保证进入 EPUB 的文本干净。
