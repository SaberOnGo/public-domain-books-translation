# 预制作阶段 1：制作规格 / Preproduction Stage 1 Spec

status: "PASS"

## Metadata

- 中文书名：爱迪生征服火星
- 原名：Edison's Conquest of Mars
- 作者：Garrett P. Serviss / 加勒特·P. 瑟维斯
- 译者：LifeBook 书坊 SaberOnGo
- 语言：zh-CN
- 来源：Project Gutenberg #19141
- 标识：pg19141-zh-cn-lifebook-v1

## EPUB Structure

- 封面页：使用 `scripts/build_epub.js` 生成的火星主题 SVG。
- 版本说明页：说明中文书名、原名、作者、译者、来源和公版状态。
- 正文：`chapters/final/001_front_matter.md` 至 `019_chapter_xviii.md`。
- 导航：使用 `metadata/chapter_title_map.yaml` 中的短标题，卷首、第一章至第十八章。

## Typography

- 中文正文行高约 1.72，段首缩进 2 字。
- 普通中文正文不使用 ASCII 分号。
- 不保留旧纸书页码、Project Gutenberg license boilerplate 或源文件尾部说明。

## Gate

PASS. 可进入样章 EPUB 检查。
