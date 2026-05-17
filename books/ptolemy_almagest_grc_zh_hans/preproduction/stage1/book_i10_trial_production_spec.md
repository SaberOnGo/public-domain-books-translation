# Book I.10 试译样本 EPUB 预制作规格

production_spec_status: "PASS_FOR_TRIAL_SAMPLE_ONLY__FULL_BOOK_BLOCKED"
human_required: false
scope: "Book I.10 trial sample EPUB only"

## 书籍身份

- 中文书名：天文学大成
- 原名：Μαθηματικὴ Σύνταξις / Almagest
- 作者：Claudius Ptolemaeus / 克劳狄乌斯·托勒密
- 当前产物：Book I.10 单章节试译样本 EPUB
- 译制标识：LifeBook 书坊试译样本
- 试译时间：2026-05-17
- 公版来源候选：Wikimedia Commons, Heiberg Greek edition PDF
- 权利状态：研究与预翻译试点；正式出版前仍需完成来源页、文件哈希和公版状态复核。

## 构建范围

- 输入译文：`chapters/translated/010_book_i_10_chords.md`
- QA 图像输入：`assets/figures/drafts/i10_fig01_*.svg` through `i10_fig07_*.svg`
- EPUB 正文图像输入：`assets/figures/facsimile/book_i10/i10_fig01_*_facsimile.png` through `i10_fig07_*_facsimile.png`
- XHTML 样章：`preproduction/stage2_sample/sample_chapter.xhtml`
- EPUB 样本：`preproduction/stage2_sample/sample_book.epub`
- 构建脚本：`scripts/build_book_i10_trial_epub.py`

本规格不读取 `chapters/final/`，不生成 `output/book.epub`，不翻译 Book I.11 弦表，不代表全书 EPUB 生产规格通过。

## 封面与版本说明

- EPUB 内含 `cover.xhtml` 和 `images/cover.svg`。
- OPF manifest 将 `images/cover.svg` 标为 `properties="cover-image"`。
- `book-info.xhtml` 明确说明该 EPUB 只用于 Book I.10 单章节试译预制作评审。

## 字体与版式

- 不嵌入中文字体。
- 不锁定具体中文字体，允许阅读器接管字体。
- 正文采用单栏、段首缩进、较宽行距，面向可重排 EPUB 阅读。
- XHTML 头部含 viewport meta；CSS 对长路径、六十进制数值和希腊标签允许断行。

## 图表策略

- 7 张 PDF facsimile PNG 图进入 EPUB `EPUB/images/`。
- Markdown 图片位已转换为 XHTML `<figure>`、`<img alt>` 和 `<figcaption>`，构建时由 SVG 草图名映射到 facsimile PNG。
- CSS 使用 `img max-width: 100%; height: auto`，facsimile 图整行居中显示，手机端按屏幕宽度缩放。
- SVG 草图仍保留为 QA 辅助，不作为本轮 EPUB 正文图。正式出版前需要逐张复核裁边、来源页标注、无障碍长描述，并决定是否升级为精确重绘 SVG。

## 与原语言 PDF 版式关系

Heiberg PDF 是双页扫描/纸书版式，含希腊文本、校勘/脚注区域、页眉页码和嵌入式几何图。Book I.10 样本 EPUB 采用中文单栏可重排版式，不复刻 PDF 的双栏/页码/校勘外观；预制作目标是保留章节顺序、证明段落、图形插入点和几何标签，而不是把扫描页原样搬入 EPUB。

## 通过边界

通过仅表示 Book I.10 试译样本可用于预制作效果讨论。以下事项仍被阻断：

- 全书翻译
- Book I.11 弦表翻译
- `chapters/final/`
- 正式 `output/book.epub`
- 全书级 EPUBCheck/出版门禁
