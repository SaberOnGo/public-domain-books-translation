# Literary-Chinese-to-Simplified-Chinese Agent Instructions / 文言文到现代简体中文 Agent 指令

This file is for AI agents using the Literary Chinese to Simplified Chinese EPUB template.

本文件供使用 `Literary-Chinese-to-Simplified-Chinese` 文言文到现代简体中文模板的 AI agent 读取。

## Scope / 适用范围

- Source language: Literary Chinese / Classical Chinese (`lzh`).
- 原文语言：文言文 / 古汉语（`lzh`）。
- Target language: modern Simplified Chinese (`zh-Hans`).
- 目标语言：现代简体中文（`zh-Hans`）。
- Public projects require public-domain or licensed source evidence. Private-use projects must use `publication_mode=private_use`.
- 公开项目必须有公版或授权来源证据。私人自用项目必须走 `publication_mode=private_use`。

## Mandatory Rules / 强制规则

- Read repository `AGENTS.md`, `template/epub_pipeline/README.md`, `template/epub_pipeline/common/README.md`, and the Simplified Chinese target framework before using this template.
- 使用本模板前必须读取仓库根 `AGENTS.md`、`template/epub_pipeline/README.md`、`template/epub_pipeline/common/README.md` 和简体中文目标语言质量框架。
- Create book projects through `books/scripts/create_book_project.py --source-target Literary-Chinese-to-Simplified-Chinese`; never write book-specific source text, translations, QA, metadata, or EPUB output into this template directory.
- 必须通过 `books/scripts/create_book_project.py --source-target Literary-Chinese-to-Simplified-Chinese` 创建书籍工程；不得把具体书籍的原文、译文、QA、metadata 或 EPUB 输出写入模板目录。
- Reader-facing chapters default to parallel passage layout: one Literary Chinese source passage followed by the corresponding modern Chinese translation.
- 读者版章节默认使用对照正文：一段古文原文，随后一段对应现代中文译文。
- Preserve source evidence, base-text choice, punctuation policy, segmentation policy, variants, doubtful readings, and annotation decisions before batch translation.
- 批量翻译前必须保留来源证据、底本选择、断句标点策略、切分策略、异文、疑难读法和注释决策。
- Use notes generously when they prevent real misunderstanding, but do not turn the reader-facing EPUB into an encyclopedia or a textual-criticism article.
- 必要注释可以多；但注释必须解决真实误读风险，不得把读者版 EPUB 写成百科或校勘论文。
- If the work is historical narrative, Warring States diplomacy, chronicle, biography, ritual, warfare, statecraft, or name-heavy prose, overlay `profiles/classical-history-zh-Hans`.
- 若作品属于历史叙事、战国外交、编年、列传、礼制、战争、政论或人名密集文本，应叠加 `profiles/classical-history-zh-Hans`。

## Hard Stops / 必须停止

- Public-domain or licensed source status is unclear.
- 公开发布权利状态不清楚。
- The only available source is a modern copyrighted translation, modern commercial punctuation/annotation edition, pirate EPUB, or unclear download.
- 唯一来源是现代受版权保护译本、现代商业标点校注本、盗版 EPUB 或权利不清楚的下载。
- Source text has not been profiled for punctuation, segmentation, edition, variants, OCR/transcription state, and editorial additions.
- 尚未记录原文断句、标点、版本、异文、OCR/转写状态和现代整理成分。
- Chapters omit the required source-modern parallel passage structure without a documented exception.
- 章节未采用“古文一段、今译一段”的对照正文，且没有记录明确例外。
