# EPUB 生成后版式复查记录

日期：2026-05-13

## 检查对象

- `output/book.epub`
- `output/黑人北极探险家.epub`

## 已执行检查

- 重新执行 `npm run build:epub`。
- 执行 `npm run lint:publication -- --strict-spaces`。
- 执行 `npm run check:epub`。
- 抽取 EPUB 内部 XHTML，检查目录、章节标题、副标题、附录、正文残留和关键章节。

## 结果

- 出版 lint：`asciiSemicolon=0`、`zhSemicolon=0`、`cjkMultiSpace=0`、`repeatedSpace=0`、`mojibake=0`、`legacyPrintToc=0`。
- EPUBCheck：`fatal=0`、`error=0`、`warning=0`。
- EPUB 内部章节 XHTML 数量：26。
- EPUB nav 章节条目数量：26。
- 第三章目录与页面标题已显示为“第三章 发现鲁道夫·弗兰克”。
- 第三章副标题已显示为“惠特尼登陆、交易装煤，以及与浮冰群搏斗”。
- 第三章标题只使用中文译名，不在标题中追加英文原名。
- 标题中的人名不计入“正文首次出现”；第三章正文第一次自然出现该人名时保留英文原名：`鲁道夫·弗兰克（Rudolph Franke）`。
- 附录二姓名清单保留为 `<pre>`，并由 CSS `white-space: pre-wrap` 支持窄屏换行。
- 未发现 `Transcriber's Notes`、`转录者说明`、`fiendlike/readjusting/forepaws` 等数字来源工件残留。

## 结论

本次生成后的 EPUB 在结构、目录、标题、副标题、附录名单呈现、正文异常空格、分号、乱码和旧纸书残留方面通过复查，可作为当前交付版本。
