# EPUB 质量整改记录

日期：2026-05-10

## 用户指出的问题

1. 章节标题过大，手机窄屏打开后容易折成多行，影响阅读。
2. 正文字体观感差。
3. 没有封面图片。
4. 书籍详情信息过薄，缺少 LifeBook 翻译组、翻译时间、公版来源 URL、公版说明等关键版本信息。

## 参考对比

参考用户本地提供的 Calibre/中文 EPUB 样本目录（不提交到仓库）：

- 常见结构包含：OPF metadata、manifest、spine、nav/toc、封面图片、封面页。
- Calibre EPUB 通常写入 `<meta name="cover" content="cover"/>` 或 manifest `properties="cover-image"`。
- 中文 EPUB 的标题字号通常约 `1.2em-1.5em`，正文 `line-height` 约 `1.5em` 以上，段首缩进 `2em`。
- 较好的 EPUB 会把封面作为图片资源加入包内，而不是只依赖阅读器自动生成封面。

## 外部规范要点

- W3C EPUB 3.3：package document 负责集中描述 metadata、manifest、spine；manifest 应列出出版物资源；EPUB 必须声明且只能声明一个 `nav` 导航文档；如有封面图，建议在 manifest item 上设置 `cover-image`。
- Apple Books Asset Guide：OPF package document 包含书籍 metadata、manifest 和 spine，是书籍结构和展示信息的核心。
- DAISY Accessible Publishing Knowledge Base：EPUB 3 应按可访问出版实践制作；图片应有可理解的替代文本，结构应语义清楚。
- Kindle/KDP：Kindle 电子书需要内部封面图片；封面不应只作为外部营销图存在。
- Standard Ebooks：高质量 EPUB 应采用统一的内部结构、语义化 XHTML、独立 CSS，并针对旧书做现代化清理，而不是把原始文本粗暴塞进 EPUB。

## 本轮整改

- `scripts/build_epub.js` 改为生成完整 EPUB 结构：封面页、版本说明页、目录、正文、CSS、OPF metadata。
- 新增包内封面图：`EPUB/images/cover.png`，并在 OPF manifest 标记 `properties="cover-image"`。
- 新增可见版本说明页：写入中文书名、英文原名、作者、译者 `LifeBook 翻译组`、翻译时间、原文来源 URL、公版说明、原书信息和本书简介。
- OPF metadata 增补：`dc:creator`、`dc:contributor` 译者、`dc:publisher`、`dc:source`、`dc:description`、`dc:rights`、`dc:subject`、`dcterms:modified`。
- CSS 调整：正文使用中文宋体优先的字体栈，标题字号降为 `1.18em`，章节号和章节题分层显示，降低手机窄屏标题压迫感。
- 保留 `output/book.epub` 作为流水线标准输出，同时生成中文文件名副本 `output/黑人北极探险家.epub`。

## 仍可继续优化

- 当前封面已升级为 1600x2400 PNG，并作为 OPF `cover-image` 写入 EPUB；如果以后要上架平台，可继续做更精细的商业封面设计。
- 字体不建议强制嵌入商业字体；更稳妥做法是给出中文字体栈，并允许阅读器/用户覆盖。
- 后续可增加移动端抽样截图流程：用 Readest、Apple Books、Kindle Previewer、Calibre Viewer 分别检查标题换行、封面、目录和详情页。

## 验证

- `npm run build:epub`：通过。
- `npm run check:epub`：EPUBCheck 5.2.1，fatal=0，error=0，warning=0。
- 拆包检查：`cover.png`、`cover.xhtml`、`book-info.xhtml`、`nav.xhtml` 均存在。
- OPF 检查：`cover-image`、legacy cover meta、LifeBook 翻译组、公版来源 URL 均存在。

