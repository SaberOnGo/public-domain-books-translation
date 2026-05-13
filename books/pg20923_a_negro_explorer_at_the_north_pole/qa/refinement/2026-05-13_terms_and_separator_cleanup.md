# 2026-05-13 普通名词与纸书分隔符清理记录

## 背景

本轮针对正文中两类出版质量问题进行清理：

1. 普通名词、器物名、衣物名、材料名不应写成“原文词（中文释义）”，也不应写成“中文词（原文词）”。
2. 旧纸书中的 `* * * * *`、`*****`、`----`、`---` 等可见分隔符不应进入 EPUB 正文，也不应替换成另一种可见符号。

## 已修正内容

- 将前言中的 `国际大奖`、`数世纪大奖` 改为比喻性表达：`近四个世纪以来各国探险者竞逐的桂冠`、`数世纪以来的目标`。原文 `international prize of nearly four centuries` 和 `prize of the centuries` 指各国长期竞逐的北极点目标，不是现实中的奖项。
- 将导言中 `Matt Henson（马特·亨森）` 调整为中文优先的 `马特·亨森（Matt Henson）`，后文使用中文名。
- 将导言中若干历史人名和地名改为中文译名优先，英文原名只在首次出现处括注。
- 将第十三章的 `_oog-sook_（海豹皮）` 调整为 `海豹皮条`。
- 将第十七章的 `_Oomiaksoah_（“船”）` 调整为 `“船。”`。
- 将附录一中帐篷、入口、火盆、锅、衣物等普通名词改为中文正文，不再保留原文词括注。
- 将第十五、十七、十九章中厚毛皮外衣、游标、皮帐篷等普通名词改为纯中文表达。
- 删除第 1、4、8、11、16、17、18 章以及附录二中的旧纸书可见分隔符。

## 新增门禁

`scripts/publication_lint.js` 和模板 common lint 已新增硬错误：

- `sourceTermBeforeTranslation`：拦截 `source term（中文释义）` 这类原文词打头的普通名词括注。
- `bodyOriginalTermGloss`：拦截 `中文普通名词（_source term_）` 这类正文普通名词原文括注。
- `bodySceneSeparator`：拦截正文中的 `* * * * *`、`*****`、`----`、`---` 等纸书分隔符。

## 验证

- `npm run lint:publication -- --strict-spaces`：通过。
- `npm run build:epub`：通过，已更新 `output/book.epub` 和 `output/黑人北极探险家.epub`。
- `npm run check:epub`：`fatal=0`、`error=0`、`warning=0`。
- 解包 `output/book.epub` 后检查：未发现星号分隔、横线分隔、`<hr>`、`ornament`、原文词打头的普通名词括注、中文普通名词后的原文括注、`国际大奖` 或 `数世纪大奖`。
