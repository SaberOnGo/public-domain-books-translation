# 《环球航海记》预制作规格 / Production Spec

production_spec_status: "PASS"
human_required: false

## 书籍身份 / Book Identity

- 中文书名：《环球航海记》
- 英文原名：`Anson's Voyage Round the World`
- 作者：Richard Walter
- 主题人物：George Anson
- 缩编与评注：H. W. Household
- 译制：LifeBook 书坊 SaberOnGo
- 翻译/译制时间：2026-05-13
- 公版来源 URL：https://www.gutenberg.org/ebooks/16611
- 公版说明：Project Gutenberg 页面标注美国公版；跨地区发行前仍需按目标地区复核。

## 封面 / Cover

- 封面来源：自制 SVG 确定性排版。
- EPUB 内封面格式：`cover.svg`，由 `scripts/build_epub.js` 生成并写入 `output/cover.svg`。
- 封面比例：1600 x 2400，2:3。
- 封面文字：中文书名、英文原名、作者、`LifeBook 书坊 SaberOnGo 译制`、Project Gutenberg #16611 来源说明。
- OPF：manifest 包含 `properties="cover-image"`。
- 封面页：EPUB 包含 `cover.xhtml`。

## 版本说明页 / Book Info Page

版本说明页由 `scripts/build_epub.js` 生成，必须包含：

- 中文书名。
- 英文原名。
- 作者。
- 主题人物。
- 缩编与评注。
- 译者/译制者：`LifeBook 书坊 SaberOnGo`。
- 译制时间。
- 公版来源 URL。
- 公版/版权说明。
- 本书简介和原书信息。

## 字体 / Font

默认不写死 `font-family`，不嵌入完整中文字体，允许阅读器和用户设置接管字体。

## 标题与正文 / Headings and Body

- `metadata/chapter_title_map.yaml` 已恢复有效缩进。
- EPUB `nav.xhtml` 使用短中文题名。
- 纸书目录式长标题保存在 `source_full`，不直接塞入导航。
- 正文段首缩进为 `2em`，行距为 `1.72`。
- 已删除导言、战斗章和术语表中的来源尾部工件。

## PASS 条件 / PASS Criteria

- 无旧品牌名残留。
- 封面存在且文字可读。
- 版本说明完整。
- 字体策略不锁死阅读器字体。
- `output/publication_lint.json` 无硬错误。
- EPUBCheck fatal=0、error=0、warning=0。
