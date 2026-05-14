# /goal：Project Gutenberg #3479《金属巨兽》完整中文 EPUB 制作

## 目标

在 `books/pg3479_the_metal_monster/` 内完成 A. Merritt / Abraham Merritt 的英文公版小说 *The Metal Monster* 的简体中文新译工程，中文题名暂定为《金属巨兽》。

本目标按 `template/epub_pipeline/common` 与 `template/epub_pipeline/en-zh-Hans` 执行，最终必须产出：

- `output/book.epub`
- `output/金属巨兽.epub`
- `output/epubcheck.json` 或 `output/epubcheck.log`
- `output/publication_lint.json`
- `output/final_manifest.md`
- `retrospective/book_retrospective.md`
- `retrospective/template_update_suggestions.md`
- `state/pipeline_state.json`，状态为 `DONE`

## 来源与版权边界

- 原文来源：Project Gutenberg #3479
- 来源页：`https://www.gutenberg.org/ebooks/3479`
- UTF-8 文本：`https://www.gutenberg.org/ebooks/3479.txt.utf-8`
- Project Gutenberg 页面显示版权状态为 `Public domain in the USA`。
- 本项目只使用 Project Gutenberg 英文原文，不使用现代中文译本、盗版 EPUB、未知来源文本或现代注释本。
- 面向美国以外地区公开发布前，仍需按目标地区复核版权状态。

## 翻译与制作要求

1. 先保留来源证据与版权核查，再开始翻译。
2. 先完成本书专项研究、文体画像、术语表和预翻译试译，试译 `PASS` 后才进入分章翻译。
3. 分章译文必须有 `chapters/src/`、`chapters/translated/`、`chapters/final/` 同名文件。
4. 每章必须有：
   - `qa/chapter_controls/{chapter}.control.md`
   - `qa/fidelity/{chapter}.md`
   - `qa/readability/{chapter}.md`
   - `qa/imagery/{chapter}.imagery.md`
   - `qa/terminology/{chapter}.md`
   - `qa/gates/{chapter}.gate.md`
5. 只有章节门禁 `PASS` 的译文才能进入 `chapters/final/`。
6. 章节标题必须按 `metadata/chapter_title_map.yaml` 处理：EPUB 导航用简短中文题名，必要时页面副标题承载源文小题。
7. 译文风格应忠实、顺畅、有奇幻/科幻冒险小说的华丽感；避免机械直译、现代网文腔、过度解释和省字式漏译。
8. 构建前必须运行 `npm run lint:publication` 并修复硬错误。
9. 构建后必须运行 `npm run check:epub`；fatal/error 必须为 0。
10. 最终必须有独立评审、返工路由、复盘和产物清单。

## 完成定义

未同时满足以下条件，不得退出并宣称完成：

- 来源证据与版权核查存在且结论允许继续。
- 预翻译报告结论为 `PASS`。
- 全部章节均有译文、终稿和 QA 门禁。
- 出版文本 lint 无硬错误。
- EPUB 已生成并通过 EPUBCheck。
- 独立评审无未关闭 P0/P1/P2 必修项。
- 复盘与最终清单已写入。
- `state/pipeline_state.json.status == "DONE"`。
