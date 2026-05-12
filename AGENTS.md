# Public Agent Instructions / 公共 Agent 指令

This file is for AI agents working from a downloaded copy of this repository.

本文件供下载本仓库后参与协作的 AI agent 读取。

## Mandatory Rules / 强制规则

- Treat this as a global multilingual public-domain book translation project, not as an English-to-Chinese-only project.
- 本项目是全球多语言公版书翻译项目，不是只面向英文到中文的项目。

- Do not treat `en-zh-Hans` as the default translation direction. It is only one currently available language-pair template.
- 不要把 `en-zh-Hans` 当作默认翻译方向。它只是当前已有的一个语言方向模板。

- For every new book project, copy `template/epub_pipeline/common` first, then overlay the matching language-pair template, and write all book-specific output only under `books/{book_id_slug}/`.
- 制作每一本新书时，必须先复制 `template/epub_pipeline/common`，再覆盖复制匹配的语言方向模板；所有具体书籍产物只能写入 `books/{book_id_slug}/`。
- Target-language quality rules live under `template/epub_pipeline/targets/{target}/`; source-to-target-specific rules live under `template/epub_pipeline/{source-target}/`.
- 目标语言质量规则放在 `template/epub_pipeline/targets/{target}/`；源语言到目标语言的专用规则放在 `template/epub_pipeline/{source-target}/`。

- Never write source text, translations, QA files, EPUB output, or book-specific metadata back into `template/`.
- 严禁把原文、译文、QA、EPUB 输出或具体书籍 metadata 写回 `template/`。

- Human-facing important files must include the local language expected by that template's contributors. English may be added in parallel, but important instructions must not be English-only unless English is the target contributor language.
- 面向人的重要文件必须包含该模板贡献者预期能读懂的本地语言。英文可以并列补充，但除非英语就是该模板贡献者语言，否则重要说明不能只写英文。

- Examples: `en-ja` important files must include Japanese plus optional English; `de-zh-Hant` important files must include Traditional Chinese plus optional English; `fr-en` important files can be English.
- 示例：`en-ja` 的重要文件必须包含日文，可并列英文；`de-zh-Hant` 的重要文件必须包含繁体中文，可并列英文；`fr-en` 的重要文件可以使用英文。

- Important files include prompts, workflow instructions, quality gates, review rubrics, policy notes, contribution instructions, and template README files. Code and purely machine-readable data are exempt.
- 重要文件包括 prompt、工作流说明、质量门禁、评审规则、政策说明、贡献说明和模板 README。代码和纯机器读取数据除外。

- Preserve public-domain source evidence and rights checks before translation. If rights are unclear, stop.
- 翻译前必须保留公版来源证据和版权核查记录。版权状态不清楚时必须停止。

- Do not use modern copyrighted translations, pirate sites, unclear EPUB downloads, or materials the contributor has no right to submit.
- 不得使用现代受版权保护的译本、盗版站、来源不明 EPUB，或贡献者无权提交的材料。

- Raw AI output is not publishable. Use research, trial translation, chapter review, quality gates, EPUB validation, and retrospective records.
- AI 初稿不能直接发布。必须经过研究、试译、章节审校、质量门禁、EPUB 校验和复盘记录。
- Do not place language-pair-specific scripts, datasets, or exploratory files in the repository root. Put them under `research/{source-target}/...` or the matching language-pair template.
- 不要把特定语言方向的脚本、数据集或探索文件放在仓库根目录。应放到 `research/{source-target}/...` 或对应语言方向模板中。
- Scripts and prompts must not hard-code local absolute paths such as Windows drive paths or one contributor's workspace. Resolve paths from the script location, the repository root, or explicit user-provided arguments.
- 脚本和 prompt 不得写死本机绝对路径，例如 Windows 盘符路径或某个贡献者的工作目录。路径应基于脚本位置、仓库根目录或用户显式传入的参数解析。

## Recommended Reading / 建议读取

- `README.md`, `README.zh-CN.md`, `readme/README.zh-TW.md`, or `readme/README.ja.md`
- `template/epub_pipeline/README.md`
- Matching target-language quality files under `template/epub_pipeline/targets/{target}/`
- `skills/public-domain-epub-pipeline/SKILL.md`
- Matching language-pair template files under `template/epub_pipeline/{source-target}/`

## Output Discipline / 输出要求

- Keep project-wide documentation multilingual and globally framed.
- 项目级文档应保持多语言、全球化定位。

- Use concrete language-pair examples, but balance them across multiple directions such as French to English, Japanese to Spanish, Chinese to English, English to Spanish, German to Traditional Chinese, and Arabic to Indonesian.
- 可以使用具体语言方向示例，但要在多个方向之间保持平衡，例如法语到英语、日语到西班牙语、中文到英语、英语到西班牙语、德语到繁体中文、阿拉伯语到印尼语。

- If a new language-pair template is added, include an `AGENTS.md` and `SKILL.md` inside that template using the local contributor language plus English.
- 如果新增语言方向模板，必须在该模板内加入 `AGENTS.md` 和 `SKILL.md`，并使用本地贡献者语言 + 英文并列说明。
