# 《环球航海记》完整 EPUB 制作目标 / Full EPUB Goal

日期：2026-05-13

## /goal 定义

为 Project Gutenberg #16611 `Anson's Voyage Round the World` 建立英语到简体中文的新书工程，中文题名《环球航海记》，并按本仓库公版书流水线完成可校验 EPUB：

- 先复制 `template/epub_pipeline/common`，再覆盖 `template/epub_pipeline/en-zh-Hans`。
- 所有书籍产物只写入 `books/zh-Hans/4_pg16611_ansons_voyage_round_the_world/`。
- 保存 Project Gutenberg 来源证据与版权核查，不使用现代译本或来源不明 EPUB。
- 清洗原文，剥离 Gutenberg 许可证和纸书目录，拆分为编辑导言、40 章、术语表。
- 完成译前研究、术语表、文体画像、试译记录。
- 完成所有章节译文、终稿、忠实度/可读性/术语/意象词检查和章节门禁。
- 生成 `output/book.epub` 与中文命名副本，并通过 `publication_lint` 和 `epubcheck`。

## 交付门槛

未满足以下条件不得标记完成：

- `chapters/src/` 有 42 个原文章节文件。
- `chapters/final/` 有 42 个中文终稿文件。
- `qa/gates/` 有 42 个章节门禁记录，结论为 PASS 或 PASS_WITH_RECORDED_LIMITATIONS。
- `output/publication_lint.json` 硬错误为 0。
- `output/epubcheck.json` 中 fatal=0、error=0。
- `state/pipeline_state.json` 记录最终状态、章节数量、质量限制和下一步人工复核建议。

## 质量重点

- 本书是 18 世纪环球远征、海战、疾病、殖民贸易和中英接触叙事；译文应保持纪实叙述的清晰、海军行动的准确和旧时代文体的克制。
- 海军、航海、地理和清代官场术语必须统一；陌生专名可采用中文译名并在术语表记录英文原名。
- 原文中的时代偏见、殖民视角和对中国官员的刻板描写应如实呈现并通过必要说明控制现代误读，不用译者声音替作者辩护或消毒。
- 章节标题不能直接照搬纸书目录的长标题链；EPUB 目录使用短题名，章节页可用副标题承载原题细节。

## 当前来源差异说明

用户提供作者为 George Anson。Gutenberg #16611 页面作者字段为 Richard Walter，George Anson 是主题人物。工程 metadata 必须保留该差异，避免把来源页面没有支持的信息写成唯一作者。
