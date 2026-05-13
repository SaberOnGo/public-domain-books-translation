# 《幽灵海盗》EPUB 预制作规格

production_spec_status: "PASS"
human_required: false

## 书籍身份

- 中文书名：《幽灵海盗》
- 英文原名：The Ghost Pirates
- 作者：William Hope Hodgson
- 译制：LifeBook 书坊 SaberOnGo
- 译制日期：2026-05-13
- 公版来源：https://www.gutenberg.org/ebooks/10966
- 原文文件：https://www.gutenberg.org/ebooks/10966.txt.utf-8
- 公版说明：Project Gutenberg 标记为美国公版文本；作者 1918 年去世，按 life+50 基线亦可进入中国大陆公版判断。译制不使用现代中译本。

## 封面

- 封面来源：自制 JPG 封面，工程文件为 `assets/cover.jpg`。
- EPUB 内封面：`cover.xhtml` + `EPUB/images/cover.jpg`。
- OPF 要求：manifest 必须含 `properties="cover-image"`。
- 封面策略：深色海面、帆船、幽影主题，避免使用受版权限制的现代图像。

## 版本说明页

EPUB 必须包含 `book-info.xhtml`，并列出：

- 中文书名、英文原名、作者、译制方和译制日期。
- Project Gutenberg 来源 URL。
- 公版与新译说明。
- 原书出版背景和本书一句话简介。

## 字体与排版

- 不嵌入完整中文字体。
- 不锁死具体中文字体，允许阅读器与用户设置接管。
- 正文段首缩进 `2em`，行距适合中文长文阅读。
- 章节导航使用短标题：题名页、作者序、船歌、第一章至第十六章。
- 旧纸书目录、页码和 Project Gutenberg boilerplate 不进入正文。

## 构建前检查

- `output/publication_lint.json` 必须存在。
- `publication_lint` 不得有硬错误。
- 所有章节必须有 translated、final、control、fidelity、readability、imagery、terminology、gate 记录。

## PASS 条件

- 来源证据和版权核查为 PASS。
- 译前研究、风格档案、试译样本为 PASS。
- 19/19 章节通过章节门禁。
- 构建脚本能生成完整 EPUB。
- EPUBCheck fatal=0、error=0。
