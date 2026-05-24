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

- Preserve source evidence and rights checks before translation. Public release projects must have public-domain or licensed source evidence. If public release rights are unclear, stop.
- 翻译前必须保留来源证据和版权核查记录。公开发布项目必须有公版或授权来源证据。公开发布权利状态不清楚时必须停止。

- A user may request a strictly personal, non-commercial, non-redistributed translation of a non-public-domain book only in `private_use` mode. This requires a user-provided local source file and an explicit private-use declaration. Create the project under ignored `books/private/{target}/{number}_{book_id_slug}/`; never place private source text, translations, QA files, EPUB output, or book-specific metadata in publishable `books/{target}/` directories or GitHub.
- 用户可以请求对非公版书做严格个人学习自用、非商业、不传播的翻译，但只能进入 `private_use` 模式。该模式必须有用户提供的本地书源文件和明确私人自用声明。工程必须创建在被忽略的 `books/private/{target}/{number}_{book_id_slug}/` 下；不得把私人原文、译文、QA、EPUB 输出或具体书籍 metadata 放入可发布的 `books/{target}/` 目录或 GitHub。

- If the user says "do not care about copyright" but does not provide a local source file, do not search for non-public-domain full text. Automatically search only public-domain, authorized, or otherwise clearly lawful sources; if none is available, stop and ask for a local source file or authorization evidence.
- 如果用户说“不用关心版权”但没有提供本地书源文件，不得自动查找非公版全文。只能自动查找公版、授权或其他权利清楚的合法来源；如果找不到，必须停止并要求用户提供本地书源文件或授权证据。

- Do not use modern copyrighted translations, pirate sites, unclear EPUB downloads, or materials the contributor has no right to submit.
- 不得使用现代受版权保护的译本、盗版站、来源不明 EPUB，或贡献者无权提交的材料。

- Raw AI output is not publishable. Use research, trial translation, chapter review, quality gates, EPUB validation, and retrospective records.
- AI 初稿不能直接发布。必须经过研究、试译、章节审校、质量门禁、EPUB 校验和复盘记录。
- Do not place language-pair-specific scripts, datasets, or exploratory files in the repository root. Put them under `research/{source-target}/...` or the matching language-pair template.
- 不要把特定语言方向的脚本、数据集或探索文件放在仓库根目录。应放到 `research/{source-target}/...` 或对应语言方向模板中。
- Scripts and prompts must not hard-code local absolute paths such as Windows drive paths or one contributor's workspace. Resolve paths from the script location, the repository root, or explicit user-provided arguments.
- 脚本和 prompt 不得写死本机绝对路径，例如 Windows 盘符路径或某个贡献者的工作目录。路径应基于脚本位置、仓库根目录或用户显式传入的参数解析。

- If a script, prompt, launcher, or external AI client integration needs an environment variable for the LifeBook repository root, use `LIFEBOOK_HOME` as the only standard variable. Do not introduce parallel repository-root variables.
- 如果脚本、prompt、启动器或外部 AI 客户端集成需要用环境变量表示 LifeBook 仓库根目录，只能使用统一变量 `LIFEBOOK_HOME`。不要再引入并行的仓库根目录变量。

## GitHub Push Commit Rules / GitHub 推送提交规则

- Before pushing to GitHub, every commit being pushed must have both a concise title and a detailed commit body. One-line commits are forbidden, because LifeBook Launcher uses commit information as user-facing update text.
- 推送到 GitHub 前，所有将被推送的 commit 都必须同时包含简洁标题和详细正文摘要。禁止只有一行标题的 commit，因为 LifeBook Launcher 会把 commit 信息作为面向用户的更新内容展示。

- The detailed commit body must contain separated `ZH:`, `EN:`, and `JA:` sections. Each language label must appear alone on its own line, and its summary must start on following lines, preferably as bullets. Do not write `ZH: long summary...` on one line. Each section must explain the user-visible or maintainer-visible change in enough detail for LifeBook Launcher to select a localized summary according to the user's computer language.
- commit 正文摘要必须分成独立的 `ZH:`、`EN:`、`JA:` 三段。每个语言标签必须独占一行，摘要内容从下一行开始，推荐使用 bullet。禁止写成 `ZH: 很长的摘要……` 这种同一行格式。每一段都必须足够详细地说明用户可见或维护者可见的变化，方便 LifeBook Launcher 按用户电脑语言选择本地化摘要。

- Before `git push`, run `python tools/git/check_commit_messages.py --range origin/main..HEAD` or the correct upstream range for the current branch. The command must pass before pushing.
- 执行 `git push` 前，必须运行 `python tools/git/check_commit_messages.py --range origin/main..HEAD`，或当前分支对应的正确 upstream range。该命令通过后才允许推送。

- When creating commits, use a multi-message commit form such as `git commit -m "Title" -m "ZH:" -m "- Chinese summary..." -m "EN:" -m "- English summary..." -m "JA:" -m "- Japanese summary..."`. Do not use a one-line `git commit -m "Title"` for work that will be pushed, and do not put summary text on the same line as the language label.
- 创建 commit 时，应使用多段提交信息，例如 `git commit -m "Title" -m "ZH:" -m "- 中文摘要……" -m "EN:" -m "- English summary..." -m "JA:" -m "- 日本語概要..."`。不要对将推送的工作使用只有一行的 `git commit -m "Title"`，也不要把摘要正文写在语言标签同一行。

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
