# 标题与 EPUB 结构专项复查

review_status: "PASS"
review_date: "2026-05-13"

## 检查结论

- `source/toc.json` 只记录第 I-XVI 章章号，但 `chapters/src/004_i.md` 至 `019_xvi.md` 正文开头另有源文真实小题。
- 中文 EPUB 目录使用“第一章”至“第十六章”等短章号；页面标题使用章号，并通过 `metadata/chapter_title_map.yaml` 的 `subtitle` 承载真实小题。
- 第 19 章中的“附录 / 寂静之船”对应原文 `APPENDIX / The Silent Ship`，保留。
- `nav.xhtml` 使用中文目录项。
- OPF 中唯一 `dc:title` 为“幽灵海盗”。
- EPUB 内部不把真实小题塞进导航长标题，而是在章节页副标题位置显示。
- 2026-05-13 二次总审修正：早前“原书仅罗马数字”的判断只适用于 `source/toc.json`，不适用于拆章正文；当前交付以 `chapter_title_map.yaml` 的短导航题名 + 页面副标题为准。

## 读者体验判断

当前目录简洁，不把源文小题塞入导航；页面内保留真实小题，移动端阅读时标题层级由主标题和副标题分担。
