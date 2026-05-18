# 《幽灵海盗》多轮精修复查记录

refinement_status: "PASS"
review_date: "2026-05-13"

## 精修目标

本轮参考 `1_pg20923_a_negro_explorer_at_the_north_pole` 的后置处理经验，把检查重点从“能生成 EPUB”推进到“标题、正文、元数据和出版细节更接近可交付版本”。本轮不重翻全书，只修复可确认的细节问题。

## 第一轮：编码与出版文本 lint

- 新增 `scripts/refinement_check.js`，按本书目录相对路径扫描，避免硬编码本机绝对路径。
- 去除非 raw 文件中的 UTF-8 BOM。
- `source/source_text_raw.txt` 的 BOM 和原始空白保留为 Gutenberg 原文证据，不作为出版文本错误处理。
- 将出版范围内的中文分号从 16 处清到 0 处。
- `publication_lint` 结果：`asciiSemicolon=0`、`zhSemicolon=0`、`cjkMultiSpace=0`、`repeatedSpace=0`、`mojibake=0`、`legacyPrintToc=0`、`targetTitleLatinResidue=0`。

## 第二轮：章节标题与来源一致性

原书正文各章只使用罗马数字编号。复查发现最终稿第 4-15 章开头存在来源不支持的中文小标题，部分会进入 EPUB 成为 `h2` 或斜体标题。本轮已删除这些自拟小标题，只保留“第一章”至“第十二章”等章节号。

保留项：

- 题名页中的书名、题辞、作者、年份和献辞来自原书前置页，保留。
- 第十六章内的“附录 / 寂静之船”来自原文 `APPENDIX / The Silent Ship`，保留为正文内小标题。

## 第三轮：英文残留与术语一致性

- `chapters/final/` 中英文残留仅剩 1 处：`莫尔腾号（Mortzestus）`，这是船名首次正文出现时按术语表保留英文原名，属于允许项。
- 未发现半角逗号、分号、冒号夹在中文正文中的异常用法。
- 未发现“作为 AI / 人工智能 / 语言模型 / 无法翻译”等 AI 输出残留。
- 核心专名复查：`杰索普`、`塔米`、`普卢默`、`威廉斯`、`斯塔宾斯`、`雅各布斯`、`贾斯克特`、`奎因` 等在最终稿中有稳定译名。

## 第四轮：EPUB 内部结构

抽取 `output/book.epub` 内部资源复查：

- EPUB 内章节 XHTML：19。
- OPF 主标题：`幽灵海盗`。
- `cover-image` metadata：存在。
- `EPUB/book-info.xhtml`：存在。
- 已删除的非来源小标题未在 EPUB XHTML 中残留。

## 第五轮：重建与校验

- `npm run build:epub`：PASS。
- `npm run check:epub`：PASS。
- EPUBCheck：fatal=0、error=0、warning=0。
- EPUB 字符统计：80562。
- `output/book.epub` 与 `output/幽灵海盗.epub` SHA256 相同：`86C509ECCAC82E0A4483CB985090274F38BDB7AB24C5387E0A21AD660AF460F2`。

## 结论

本轮精修已修复可确认的出版细节问题：BOM、出版文本分号、来源不支持的章节小标题、元数据主标题和 EPUB 内部结构均已复核。当前版本可作为比上一版更严格的交付版本。
