# /goal：制作《爱迪生征服火星》简体中文 EPUB

## 目标

按 `template/epub_pipeline/common` + `template/epub_pipeline/en-zh-Hans` 流水线，把 Garrett P. Serviss 的 *Edison's Conquest of Mars* 从 Project Gutenberg 公版英文源文本译为简体中文，并生成可校验的 EPUB。

## 固定输入

- 书名：Edison's Conquest of Mars / 《爱迪生征服火星》
- 作者：Garrett P. Serviss
- 翻译方向：英文到简体中文，`en-zh-Hans`
- 主来源：Project Gutenberg #19141，https://www.gutenberg.org/ebooks/19141
- 官方 UTF-8 文本：https://www.gutenberg.org/ebooks/19141.txt.utf-8
- 参照重复条目：Project Gutenberg #21670，https://www.gutenberg.org/ebooks/21670
- 项目目录：`books/zh-Hans/3_pg19141_edisons_conquest_of_mars/`

## 完成定义

- 已保留来源证据和版权核查记录，版权状态不清楚时停止。
- 已完成本书研究、文体画像、试译，并在 `qa/pretranslation/pretranslation_report.md` 标记 `PASS`。
- 所有章节都有 `chapters/src/`、`chapters/translated/`、`chapters/final/` 对应文件。
- 每章都有译后控制、忠实度、可读性、术语、意象审计和 gate 文件，且结论为 `PASS`。
- 完成阶段 1 制作规格、样章 EPUB 检查、整书 EPUB 构建。
- `node scripts/publication_lint.js --target=zh-Hans --write-report` 无硬错误。
- EPUBCheck fatal/error 为 0。
- 完成两个独立评审记录、回退路由、最终清单和复盘。
- `state/pipeline_state.json.status == DONE`。

## 特别翻译目标

- 保留 1898 年美国早期科幻、报刊连载叙事和帝国时代科学幻想的语气，不把它改写成现代硬科幻。
- 技术词如 disintegrator、electric ship、Martian car、asteroid 等保持稳定译法。
- 现实人物如 Thomas Edison、Lord Kelvin、Röntgen、Tesla 等第一次自然出现时保留中文译名与英文原名策略。
- 对过时、殖民时代和战争动员语气保持忠实呈现，必要时用译注或制作说明解释，不用现代价值判断替换原文。
