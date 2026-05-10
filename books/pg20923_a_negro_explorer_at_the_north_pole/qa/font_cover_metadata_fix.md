# EPUB 字体、封面体积与版本信息修正记录

日期：2026-05-10

## 问题

1. 正文 CSS 写死中文字体栈，部分阅读器会尊重出版商字体，导致用户无法在 App 内改字体。
2. 如果设备没有 `Noto Serif CJK SC`、`Source Han Serif SC`，会回落到宋体/中易宋体一类字体，观感较差。
3. 每章标题里 `第X章` 与章节说明字号不一致，视觉不统一。
4. 版本说明和 OPF metadata 仍有 `LifeBook 翻译组` 残留。
5. 封面 PNG 约 3.03MB，相对于正文体积过大。

## 处理

- 移除 EPUB 正文 CSS 中所有 `font-family` 设置，不再强制出版商字体，交给阅读器默认字体或用户设置接管。
- 不嵌入完整 `霞鹜文楷/LXGW WenKai` 字体。完整中文 TTF 体积约 25MB，直接嵌入会严重放大 EPUB 文件。
- 章节标题统一：`.chapter-kicker` 与 `.chapter-title` 均为 `1em`，避免 `第X章` 小、章节说明大的问题。
- 全部品牌信息改为 `LifeBook 书坊`，版本页、OPF、description、rights 均已同步。
- 封面从 PNG 转为 JPEG，质量 86，保留视觉效果同时降低体积：约 3.03MB -> 394KB。
- EPUB 内封面 manifest 改为 `EPUB/images/cover.jpg`，media-type 为 `image/jpeg`，仍保留 `properties="cover-image"`。

## 当前验证

- `npm run build:epub`：通过。
- `npm run check:epub`：通过。
- EPUBCheck：fatal=0，error=0，warning=0。
- 拆包检查：
  - 无 `font-family` 锁定。
  - 无 `LifeBook 翻译组` 残留。
  - 已使用 `LifeBook 书坊`。
  - 封面为 `cover.jpg`。
  - 章节标题两部分字号一致。

## 字体建议

- 正式 EPUB 默认不建议强制嵌入完整中文字体，尤其是公版书批量制作场景。
- 如果必须指定观感，可在模板层提供两种构建模式：
  - `reader-default`：不写死字体，推荐默认模式。
  - `embedded-font`：嵌入字体子集，适合必须保证视觉一致的特殊版本，但需要额外做字体子集化，避免几十 MB 体积。
- `霞鹜文楷/LXGW WenKai` 适合作为可选字体方向，但不适合直接完整嵌入本书。
