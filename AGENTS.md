# Public Agent Instructions / 公共 Agent 指令

This file is for AI agents working from a downloaded copy of this repository.

本文件供下载本仓库后参与协作的 AI agent 读取。

## Mandatory Rules / 强制规则

- Before doing any task in this repository, first read this `AGENTS.md`, then read the relevant files under `template/`. Do not rely on memory, prior runs, or assumptions about the pipeline.
- 在本仓库执行任何任务前，必须先读取本 `AGENTS.md`，然后读取 `template/` 下与任务相关的规则文件。不得依赖记忆、历史执行经验或对流水线的想当然理解。

- The authoritative workflow rules live under `template/epub_pipeline/`. For EPUB production, frontmatter, cover, book-info pages, assets, quality gates, random review, or release work, read the applicable common references before editing or building, especially:
  - `template/epub_pipeline/README.md`
  - `template/epub_pipeline/common/README.md`
  - `template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md`
  - `template/epub_pipeline/common/references/cover_design_policy.md`
  - `template/epub_pipeline/common/references/book_info_frontmatter_policy.md`
  - `template/epub_pipeline/common/references/epub_assets_figures_tables.md`
  - `template/epub_pipeline/common/references/quality_gate_framework.md`
  - `template/epub_pipeline/common/references/release_versioning.md`
- 权威流程规则位于 `template/epub_pipeline/`。凡涉及 EPUB 制作、前置页、封面、书籍信息页、资产、质量门禁、随机评审或发布，编辑或构建前必须先读取适用的 common references，尤其是：
  - `template/epub_pipeline/README.md`
  - `template/epub_pipeline/common/README.md`
  - `template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md`
  - `template/epub_pipeline/common/references/cover_design_policy.md`
  - `template/epub_pipeline/common/references/book_info_frontmatter_policy.md`
  - `template/epub_pipeline/common/references/epub_assets_figures_tables.md`
  - `template/epub_pipeline/common/references/quality_gate_framework.md`
  - `template/epub_pipeline/common/references/release_versioning.md`

- Cover and book-info rules must be read as two separate policies, not merged from memory. `cover_design_policy.md` requires the cover to use the concise producer line `LifeBook 书坊 译制`; personal contributor names belong in `book-info.xhtml` and metadata according to `book_info_frontmatter_policy.md`.
- 封面规则与书籍信息页规则必须作为两份独立 policy 读取，不得凭记忆合并。`cover_design_policy.md` 要求封面使用简洁署名 `LifeBook 书坊 译制`；个人贡献者名应按 `book_info_frontmatter_policy.md` 放入 `book-info.xhtml` 和 metadata。

- When a generated EPUB or staging directory already exists, clean or rebuild the staging output before running asset or publication lint, so old XHTML, links, or assets cannot pollute the new gate result.
- 如果 EPUB 或中间构建目录已经存在，运行资产检查或出版检查前必须清理或重新生成 staging 输出，避免旧 XHTML、旧链接或旧资产污染新的门禁结果。

- Treat this as a global multilingual public-domain book translation project, not as an English-to-Chinese-only project.
- 本项目是全球多语言公版书翻译项目，不是只面向英文到中文的项目。

- Do not treat `en-zh-Hans` as the default translation direction. It is only one currently available language-pair template.
- 不要把 `en-zh-Hans` 当作默认翻译方向。它只是当前已有的一个语言方向模板。

- For every new book project, use `books/scripts/create_book_project.py` to create the project under `books/{target}/{number}_{book_id_slug}/`, where `{target}` is the output language tag such as `zh-Hans`, `en`, `ja`, or `es`, and `{number}` is the next integer in that target-language directory. The script must copy `template/epub_pipeline/common` first, then overlay the matching language-pair template. All book-specific output must stay under that numbered project directory.
- 制作每一本新书时，必须使用 `books/scripts/create_book_project.py` 在 `books/{target}/{number}_{book_id_slug}/` 下创建工程；其中 `{target}` 是输出语言标签，例如 `zh-Hans`、`en`、`ja`、`es`，`{number}` 是该目标语言目录内自动递增的下一个整数。脚本必须先复制 `template/epub_pipeline/common`，再覆盖复制匹配的语言方向模板。所有具体书籍产物只能写入这个带编号的书籍工程目录。
- Shared build dependencies are installed once under `books/` (`books/package.json`, `books/package-lock.json`, ignored `books/node_modules/`). Do not create per-book `node_modules/` directories unless a book records a justified private-toolchain exception.
- 构建依赖统一安装在 `books/`（`books/package.json`、`books/package-lock.json`、被忽略的 `books/node_modules/`）。不要为每本书重复创建 `node_modules/`；除非某本书记录了确有必要的私有工具链例外。
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
