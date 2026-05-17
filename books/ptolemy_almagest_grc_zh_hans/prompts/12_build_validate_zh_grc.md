# 12 构建与校验 EPUB（旧阶段，保留兼容）/ Build & Validate EPUB Legacy Stage

## 说明 / Note

本文件只保留为构建与校验说明。新版流程中，正式全书制作应执行：

- `13_preproduction_stage1_spec_zh_grc.md`
- `14_preproduction_stage2_sample_zh_grc.md`
- `15_full_book_production_zh_grc.md`
- `16_independent_review_agents_zh_grc.md`
- `17_revision_routing_zh_grc.md`
- `18_final_output_zh_grc.md`
- `19_retrospective_template_update_zh_grc.md`

不得在章节门禁后直接执行本文件并标记 `DONE`。

## 输入 / Input

- `frontmatter/preface.md`
- `frontmatter/translator_note.md`
- `chapters/final/*.md`
- `metadata/book.yaml`

## 前置门禁 / Prerequisite Gate

只有当所有章节都有 `qa/gates/*.gate.md` 且结论为 `PASS` 时，才可构建临时 EPUB。

构建前必须先运行出版文本、资源检查和本书来源角色门禁：

```powershell
npm run quality:source-roles
npm run lint:publication
npm run lint:assets
```

如发现三源角色混淆、分号滥用、异常连续空格、旧纸书页码目录、乱码、编码污染、图片缺失、OPF manifest 缺项或本机绝对路径，必须先修正，不得直接构建。

## 构建 / Build

必须使用项目构建脚本：

```powershell
npm run build:epub
```

不得用 `pandoc` 或手工 zip 绕过 `quality:source-roles`、`quality:translation`、`publication_lint`、`asset_manifest_check`、章节门禁和 OPF manifest 检查。

## 校验 / Validate

运行：

```powershell
npm run check:epub
```

## 输出 / Output

- `output/book.epub`
- `output/epubcheck.json` 或 `output/epubcheck.log`
- `output/publication_lint.json`
- `output/asset_manifest_check.json`

## 新版限制 / New Pipeline Restriction

本阶段通过只表示“临时 EPUB 可构建”，不能设置 `DONE`。必须继续执行新版 13-19 阶段。
