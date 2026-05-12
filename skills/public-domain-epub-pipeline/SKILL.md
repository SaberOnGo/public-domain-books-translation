---
name: public-domain-epub-pipeline
description: Use when creating, reviewing, or maintaining public-domain book translation projects and EPUB pipeline templates in this repository. Follow multilingual, language-pair-specific, rights-aware workflow rules.
---

# Public-Domain EPUB Pipeline Skill / 公版书 EPUB 流水线 Skill

Use this skill when an AI agent is asked to create a book project, add or update a language-pair template, revise prompts, review policy documents, or build EPUB output in this repository.

当 AI agent 被要求创建书籍工程、新增或更新语言方向模板、修改 prompt、审查政策文档或构建 EPUB 时，使用本 skill。

## Core Workflow / 核心流程

1. Read `AGENTS.md`.
   先读取 `AGENTS.md`。

2. Read the repository README in the user's preferred language when available.
   优先读取用户偏好语言对应的 README。

3. Read `template/epub_pipeline/README.md`.
   读取 `template/epub_pipeline/README.md`。

4. Select the matching language-pair template, for example `fr-en`, `ja-es`, `en-zh-Hans`, or `zh-Hant-de`.
   选择匹配的语言方向模板，例如 `fr-en`、`ja-es`、`en-zh-Hans` 或 `zh-Hant-de`。

5. Copy `template/epub_pipeline/common` into `books/{book_id_slug}/`, then overlay the matching language-pair template.
   先把 `template/epub_pipeline/common` 复制到 `books/{book_id_slug}/`，再覆盖复制匹配的语言方向模板。

6. Write all book-specific source text, translations, QA, EPUB output, and metadata only inside the book project.
   所有具体书籍的原文、译文、QA、EPUB 输出和 metadata 只能写入书籍工程目录。

7. Run the workflow through source evidence, rights checks, research, trial translation, chapter translation, review, gates, EPUB production, validation, independent review, and retrospective.
   按来源证据、版权核查、研究、试译、章节翻译、审校、门禁、EPUB 制作、校验、独立评审和复盘流程执行。

## Language Requirements / 语言要求

- Important human-facing files must include the local language for the intended contributors.
- 面向人的重要文件必须包含目标贡献者能读懂的本地语言。

- English may be included in parallel as a bridge language, but English-only important instructions are not acceptable unless English is the template's contributor language.
- 英文可以作为桥接语言并列出现，但除非英语就是该模板贡献者语言，否则重要说明不能只写英文。

- For `en-ja`, use Japanese plus optional English. For `de-zh-Hant`, use Traditional Chinese plus optional English. For `fr-en`, English is acceptable.
- `en-ja` 使用日文，可并列英文。`de-zh-Hant` 使用繁体中文，可并列英文。`fr-en` 可使用英文。

- Shared repository-level documentation should include Chinese when project-owner review is expected.
- 需要项目发起者审阅的共享仓库级文档应包含中文。

## Hard Stops / 必须停止的情况

- Rights or public-domain status is unclear.
- 版权或公版状态不清楚。

- The only available source is a modern copyrighted translation or unclear commercial EPUB.
- 唯一来源是现代受版权保护译本或来源不明的商业 EPUB。

- The current working directory is still under `template/` while book-specific output is about to be written.
- 当前目录仍在 `template/` 下，却准备写入具体书籍产物。

- A pretranslation report, chapter gate, EPUB validation, or independent review fails.
- 预翻译报告、章节门禁、EPUB 校验或独立评审失败。

## Public Policy / 公开政策

- Non-code book content is publicly licensed under `CC BY-NC-SA 4.0` unless a file says otherwise.
- 非代码书籍内容默认按 `CC BY-NC-SA 4.0` 公开授权，除非文件另有说明。

- Third-party commercial use requires separate permission from LifeBook Shufang and relevant rights holders.
- 第三方商业使用必须另行取得 LifeBook 书坊及相关权利人的授权。

- Contributor rules are defined in `CONTRIBUTING*.md`.
- 贡献者规则见 `CONTRIBUTING*.md`。
