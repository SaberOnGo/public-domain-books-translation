# 12 构建与校验 EPUB（旧阶段，保留兼容）/ Build & Validate EPUB Legacy Stage

## 说明 / Note

本文件保留给旧模板和 pandoc 快速构建使用。新版流程中，正式全书制作应执行：

- `13_preproduction_stage1_spec_zh_en.md`
- `14_preproduction_stage2_sample_zh_en.md`
- `15_full_book_production_zh_en.md`
- `16_independent_review_agents_zh_en.md`
- `17_revision_routing_zh_en.md`
- `18_final_output_zh_en.md`
- `19_retrospective_template_update_zh_en.md`

不得在章节门禁后直接执行本文件并标记 `DONE`。

## 输入 / Input

- `frontmatter/preface.md`
- `frontmatter/translator_note.md`
- `chapters/final/*.md`
- `metadata/book.yaml`

## 前置门禁 / Prerequisite Gate

只有当所有章节都有 `qa/gates/*.gate.md` 且结论为 `PASS` 时，才可构建临时 EPUB。

构建前必须先运行出版文本检查：

```powershell
node scripts/publication_lint.js --target=zh-Hans --write-report
```

如发现分号滥用、异常连续空格、旧纸书页码目录、乱码或编码污染，必须先修正 `chapters/final/`、`frontmatter/` 或相关 metadata，不得直接构建。

## 构建 / Build

优先使用项目已有脚本或 `pandoc`：

```powershell
pandoc frontmatter/preface.md frontmatter/translator_note.md chapters/final/*.md --metadata-file=metadata/book.yaml --toc --toc-depth=2 --split-level=1 -o output/book.epub
```

## 校验 / Validate

运行：

```powershell
epubcheck output/book.epub > output/epubcheck.log
```

或使用本项目可用的等价 epubcheck 工具。

## 输出 / Output

- `output/book.epub`
- `output/epubcheck.log`
- `output/publication_lint.json`

## 新版限制 / New Pipeline Restriction

本阶段通过只表示“临时 EPUB 可构建”，不能设置 `DONE`。必须继续执行新版 13-19 阶段。
