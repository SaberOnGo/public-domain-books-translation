# 15 全书制作 / Full Book Production

## 目的 / Purpose

只有预制作阶段 2 样章 PASS 后，才可制作整本 EPUB。

## 输入 / Input

- `preproduction/stage1/production_spec.md`
- `preproduction/stage2_sample/sample_review.md`，结论必须为 PASS。
- `chapters/final/*.md`
- `metadata/book.yaml`
- `assets/figures/`、`assets/images/`、`assets/styles/`、`source/tables/`，如本书使用图表、图片、CSS 或结构化表格。

## 任务 / Tasks

1. 生成或更新 EPUB 构建脚本。
2. 运行 `node scripts/publication_lint.js --target=zh-Hans --write-report`。
3. 运行 `node scripts/asset_manifest_check.js --write-report`；在 OPF 生成前可先检查 Markdown/XHTML 引用路径，OPF 生成后必须再次检查 manifest 覆盖。
4. 确认 `output/publication_lint.json` 中 `targetTitleLatinResidue=0`、`sourceTermBeforeTranslation=0`、`bodyOriginalTermGloss=0`、`bodySceneSeparator=0`；否则不得继续构建或发布。
5. 把 `chapters/final/*.md` 转换为正文 XHTML；Markdown 图片必须转换为 XHTML `<figure>` 或等效结构。
6. 生成 `cover.xhtml`、`book-info.xhtml`、`nav.xhtml`、正文 XHTML、CSS、OPF。
7. 把 EPUB 实际使用的 `assets/figures/*`、`assets/images/*`、`assets/styles/*` 等复制到 EPUB 包内，并写入 OPF manifest。
8. 技术表格必须优先生成 XHTML `<table>`；源 CSV/TSV 保留在 `source/tables/`，不得只以图片形式发布可结构化表格。
9. 打包 `output/book.epub`。
10. 保留必要可审计产物，如 `output/cover.jpg`、`output/publication_lint.json`、`output/asset_manifest_check.json`、`output/epubcheck.json`。
11. 运行 EPUBCheck。

## 禁止 / Forbidden

- 禁止样章未 PASS 就构建全书。
- 禁止把封面原始大图无压缩塞入 EPUB。
- 禁止嵌入完整中文字体，除非已完成字体子集化并记录原因。
- 禁止 metadata、版本说明和封面三处品牌名不一致。
- 禁止在出版文本 lint 未通过时构建或发布全书 EPUB。
- 禁止在资源引用检查未通过时构建或发布全书 EPUB。
- 禁止 XHTML、CSS 或 OPF 中出现本机绝对路径、`file://`、Windows 盘符或未经许可的远程图片热链接。
- 禁止把可结构化技术表格只做成图片；表格应输出为 XHTML `<table>`。
- 禁止图片资源存在但未写入 OPF manifest。
- 禁止章节标题、副标题或目录题名出现古希腊文原名、拉丁化转写或外文括注；标题中的人名不计入“正文首次出现”。
- 禁止普通名词写成 `source term（中文释义）` 或 `中文词（source term）`；禁止旧纸书星号或横线分隔符进入最终正文。

## 输出 / Output

- `output/book.epub`
- `output/publication_lint.json`
- `output/asset_manifest_check.json`
- `output/epubcheck.json` 或 `output/epubcheck.log`
- `state/pipeline_state.json.status = EPUB_BUILT`
