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
2. 运行 `node scripts/publication_lint.js --target=zh-Hans --write-report`。
3. 确认 `output/publication_lint.json` 中 `targetTitleLatinResidue=0`、`sourceTermBeforeTranslation=0`、`bodyOriginalTermGloss=0`、`bodySceneSeparator=0`；否则不得继续构建或发布。
4. 生成 `cover.xhtml`、`book-info.xhtml`、`nav.xhtml`、正文 XHTML、CSS、OPF。
5. 打包 `output/book.epub`。
6. 保留必要可审计产物，如 `output/cover.jpg`、`output/publication_lint.json`、`output/epubcheck.json`。
7. 运行 EPUBCheck。
8. EPUBCheck 通过后，下一步必须进入 `prompts/16a_stratified_random_spotcheck.md`；不得直接进入最终输出或宣布完成。

## 禁止 / Forbidden

- 禁止样章未 PASS 就构建全书。
- 禁止把封面原始大图无压缩塞入 EPUB。
- 禁止嵌入完整中文字体，除非已完成字体子集化并记录原因。
- 禁止 metadata、版本说明和封面三处品牌名不一致。
- 禁止在出版文本 lint 未通过时构建或发布全书 EPUB。
- 禁止第一版 `output/book.epub` 生成后跳过 EPUB 后分层随机抽检模块。
- 禁止章节标题、副标题或目录题名出现英文原名或英文括注；标题中的人名不计入“正文首次出现”。
- 禁止普通名词写成 `source term（中文释义）` 或 `中文词（source term）`；禁止旧纸书星号或横线分隔符进入最终正文。

## 输出 / Output

- `output/book.epub`
- `output/publication_lint.json`
- `output/epubcheck.json` 或 `output/epubcheck.log`
- `state/pipeline_state.json.status = EPUB_BUILT`
