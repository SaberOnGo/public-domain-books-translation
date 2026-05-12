# 15 全书制作 / Full Book Production

## 目的 / Purpose

只有预制作阶段 2 样章 PASS 后，才可制作整本 EPUB。

## 输入 / Input

- `preproduction/stage1/production_spec.md`
- `preproduction/stage2_sample/sample_review.md`，结论必须为 PASS。
- `chapters/final/*.md`
- `metadata/book.yaml`

## 任务 / Tasks

1. 生成或更新 EPUB 构建脚本。
2. 生成 `cover.xhtml`、`book-info.xhtml`、`nav.xhtml`、正文 XHTML、CSS、OPF。
3. 打包 `output/book.epub`。
4. 保留必要可审计产物，如 `output/cover.jpg`、`output/epubcheck.json`。
5. 运行 EPUBCheck。

## 禁止 / Forbidden

- 禁止样章未 PASS 就构建全书。
- 禁止把封面原始大图无压缩塞入 EPUB。
- 禁止嵌入完整中文字体，除非已完成字体子集化并记录原因。
- 禁止 metadata、版本说明和封面三处品牌名不一致。

## 输出 / Output

- `output/book.epub`
- `output/epubcheck.json` 或 `output/epubcheck.log`
- `state/pipeline_state.json.status = EPUB_BUILT`
