# 雪月（Snowmoon）v0.0.4

作者：维塔利克·布特林（Vitalik Buterin）。译制署名：LifeBook 书坊 SaberOnGo 译制；封面署名：LifeBook 书坊译制。

正式质量状态：PASS。此版本基于作者网站 2026 年 10 月 8 日修订后的 32 章版本；原作仍可能继续更新。本书依 GNU GPL v3 许可证发布，原作权利归原作者。

## 阅读与下载

- [雪月_v0.0.4.epub](https://github.com/SaberOnGo/public-domain-books-translation/releases/download/snowmoon-v0.0.4/Snowmoon_zh-Hans_v0.0.4.epub)
- [雪月_中英双语_v0.0.4.epub](https://github.com/SaberOnGo/public-domain-books-translation/releases/download/snowmoon-v0.0.4/Snowmoon_zh-Hans-en_v0.0.4.epub)
- [雪月_英文原文_v0.0.4.epub](https://github.com/SaberOnGo/public-domain-books-translation/releases/download/snowmoon-v0.0.4/Snowmoon_en_v0.0.4.epub)
- [中文与中英双语网页版 ZIP](https://github.com/SaberOnGo/public-domain-books-translation/releases/download/snowmoon-v0.0.4/Snowmoon_Web_v0.0.4.zip)
- [可编辑 GPL 对应源码 ZIP](https://github.com/SaberOnGo/public-domain-books-translation/releases/download/snowmoon-v0.0.4/Snowmoon_Corresponding_Source_v0.0.4.zip)

网页包解压后，用任意静态网页服务器提供 `Snowmoon_Web_v0.0.4/`；中文入口为 `zh-Hans/index.html`，双语入口为 `bilingual/index.html`。远程 EPUB 附件使用 ASCII 文件名，内容与本目录同名中文文件的字节一致，`SHA256SUMS.txt` 使用远程附件名。

## v0.0.4 相对 v0.0.3 的变化

- 书中不再附 GPL v3 全文页，仅在书籍简介里用一句话写明授权；完整许可证文本仍随对应源码包提供。
- 全书成品质检后修订：中文版封面去掉图下多余文字；双语版 dc:identifier 与中文版区分；第1章相邻中文按钮标签不再含半角空格；英文原文版与双语版英文栏把作者原文的 `_强调_` 渲染为真正的斜体。
- 按两轮抽检共修订 13 处译文：补回漏译（第14章、第30章）、统一术语（伤亡比、公共汽车、参议员）、图26.3 题注补“无人机”等。
- 成品 EPUB 检查三版 0 错误；三版 EPUBCheck 均为 0 fatal/0 error/0 warning。

## 校验与范围

4373 个单元全部有独立语义复核封存记录；文学门禁通过；当前稿 round_017、round_018 连续两轮独立 A/B 分层抽检通过。审校与阅读由 AI 完成，没有人工或有声朗读；阅读器证据为 Calibre 自动化探测，没有人工目视复核；未变更单元沿用此前封存的复核结果，文学门禁判定逐条沿用、未新增阅读员判断。三 EPUB 和完整两网页树的隔离源码重建及基线比较通过；该验证使用本机共享 Node 依赖，不是干净机器或跨平台声明。

详见 `release_state.json`、`release_notes.md`、`source_delivery_manifest.json`、`source_rebuild_verification.json`、`gpl_source_delivery_verification.json`。`measurement_evidence.json`、`translation_metrics.*`、`translation_difficulty_assessment.*` 为 v0.0.2 时期的统计记录，未随 v0.0.3/v0.0.4 重算。LifeBook 在线书库目前上架的是 v0.0.3，v0.0.4 需另行更新。

## English

Three validated EPUB editions (target-only, bilingual, source-original) and both static web editions are supplied with the editable GPL v3 corresponding source. This version removes the full GPL text from inside the book (the licence is stated in one sentence in the introduction; the full text ships with the source package), restores two omissions, unifies terms, and fixes finished-artifact residue found by the new final-EPUB gate. Review was AI-only; reader evidence is automated; measurement files are historical (v0.0.2).
