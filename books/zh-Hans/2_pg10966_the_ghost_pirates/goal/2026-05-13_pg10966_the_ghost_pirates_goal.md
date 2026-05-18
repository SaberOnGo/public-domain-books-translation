# 《幽灵海盗》制作目标 / Goal

日期：2026-05-13

本文件定义 `books/zh-Hans/2_pg10966_the_ghost_pirates/` 的 `/goal`。本书工程必须严格遵守仓库根目录 `AGENTS.md`、`template/epub_pipeline/common`、`template/epub_pipeline/en-zh-Hans` 和 `template/epub_pipeline/targets/zh-Hans/` 的规则。所有书籍产物只能写入本目录，禁止写回 `template/`。

## 目标

依据 Project Gutenberg #10966 官方英文原文，制作 William Hope Hodgson 的 *The Ghost Pirates* 简体中文新译 EPUB，中文题名暂定《幽灵海盗》。

完成定义：

- 来源证据和版权核查记录完整，且结论允许进入翻译。
- 原文已下载、清洗、分章，Gutenberg 许可证和转录说明不混入正文。
- 完成译前研究、术语表、文体画像和预翻译试译，且预翻译结论为 PASS。
- 19 个章节/前置文本均有 `chapters/translated/` 初译、`chapters/final/` 终稿和对应 QA 文件。
- 每章通过译后控制、忠实度、可读性、意象词、术语和章节门禁。
- EPUB 构建前运行 `node scripts/publication_lint.js --target=zh-Hans --write-report` 且无硬错误。
- 生成 `output/book.epub` 与 `output/幽灵海盗.epub`。
- EPUBCheck fatal=0、error=0。若 warning 存在，必须记录是否影响发布。
- 完成独立评审、返工路由、最终清单和复盘记录。
- `state/pipeline_state.json` 标记为 `DONE` 前，不得宣布目标完成。

## 翻译方向与模板

- Source language: English
- Target language: Simplified Chinese
- Language pair template: `template/epub_pipeline/en-zh-Hans`
- Target framework: `template/epub_pipeline/targets/zh-Hans`

## 本书风险

- 大量航海术语、帆装部位、船上值班和船员称谓。
- 叙述者口吻朴素，恐怖感来自逐步逼近，不可改写成夸张惊悚文案。
- 关键船名 `Mortzestus` 暂译“莫尔腾号”，首次出现需保留英文原名。
- `mate`、`Second Mate`、`bo'sun`、`royal mast`、`yard`、`halyards`、`gantline` 等术语必须统一。
- 海员号子 `The Hell O! O! Chaunty` 需保留节奏、呼喊和船上劳动感，不可译成平板说明。

## 执行路线

1. 复制 common 与 `en-zh-Hans` 模板到本书目录。
2. 下载 Project Gutenberg #10966 UTF-8 plain text。
3. 记录来源证据、版权核查、哈希和清洗结果。
4. 生成本书研究、术语表、标题映射和预翻译报告。
5. 分批完成 19 个章节的翻译、QA 和门禁。
6. 生成封面、目录、metadata、EPUB。
7. 运行 publication lint 与 EPUBCheck。
8. 进行出版前评审与复盘。
