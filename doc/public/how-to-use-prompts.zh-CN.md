# AI 客户端使用说明：怎样让 AI 按本仓库模板做书

这份说明写给希望用 AI 客户端协作制书的人。您不需要会写代码；只需要打开项目、复制一段文字、检查 AI 做出来的书籍文件。

## 您要先明白的 3 件事

1. **普通用户只需要给三项内容。**
   您只需要告诉 AI“我要翻译的书”“目标语言”和“自动选择翻译 prompt 的规则”。“自动选择翻译 prompt 的规则”的完整写法见下面的[最简单的启动方式](#最简单的启动方式)。可靠来源、源语言、模板、目录名、release 和检查命令都由 AI 自动处理。

2. **让 AI 自己读规则。**
   您不需要理解仓库规则，只要要求 AI 自动选择正确的公共 prompt。

3. **最后只看 release 或私人产物结果。**
   AI 会自动完成来源核查、版权核查、翻译、审校、EPUB 构建、抽检和发布。公版或授权项目最后检查 `output/release/`；个人自用项目最后检查 `output/private_artifacts/`。

## 最简单的启动方式

打开您正在使用的 AI 客户端，进入这个项目或让 Launcher 打开项目。

然后复制下面这段，把 `{...}` 换成您的书名和目标语言：

### 公版书翻译 prompt

```text
我要翻译的书：{书名、作者（可选）；如果您已经有可靠来源链接，也可以贴上}
目标语言：{例如 简体中文}

请自动选择正确的翻译 prompt：
- 如已有对应源语言模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应源语言模板，执行 doc/public/user_prompt/book_translation_new_template.md。

除非版权或来源无法确认，不要让我填写技术字段。请自动查找可靠公版来源，自动创建项目，完成翻译、审校、EPUB 构建、分层随机抽检和 release。
翻译执行时必须逐章执行“每章译后全量检查并修复”：每章都要对照整章原文和整章译文检查忠实度、中文顺读、术语、标题/小标题、注释、图表文字接口、源语句法残留、过硬过直句、过度解释或加戏等问题；发现问题后先修复，但该轮不能 PASS，必须追加新一轮整章复查，直到最新一轮零问题 PASS。
第一版 EPUB 生成后必须执行“分层随机抽检与问题族追杀”：抽检发现任何问题，不得只修被抽样本，必须在当轮归纳为问题族，用 `rg`、术语表、标题表、抽样 manifest 和小上下文原文对照做全书同类审计，修复确认命中，记录例外，再用新 seed 追加一轮。译文质量问题族必须使用 `skills/translation-quality-defect-families/SKILL.md` 做经验沉淀。
未声明是否启用 LifeBook Digest 时，请自动判断；长篇小说、专业书籍、哲学书在 EPUB 输出后生成 Digest，短篇小说、自然科学类和其他类型不生成。
如需生成 Digest，请在书籍工程根目录写入 `digest.config.json`（`enabled=true`、`merge_into_epub=true`），并在仓库根目录运行：`python -m digest.lifebook_digest --book-root books/{target}/{number}_{目标语言书名}_{目标语言作者名}`。输出仍然是标准 EPUB。
```

## 个人自用书翻译 prompt

如果这是您自己已有的本地书源，只供个人学习自用，不传播、不商业使用，可以使用下面这段：

```text
我要翻译的书：{书名、本地目录: XXX }
目标语言： {例如 简体中文}

请自动选择正确的翻译 prompt：
- 如已有对应源语言模板，执行 doc/public/user_prompt/book_translation_private_existing_template.md。
- 如无对应源语言模板，执行 doc/public/user_prompt/book_translation_private_new_template.md。

这是我个人自用的,不传播,不用于商业,使用我给出的本地的书源。
请自动创建项目，严格完成整个模板规定的系统翻译流程,不允许有任何遗漏。
翻译执行时必须逐章执行“每章译后全量检查并修复”；第一版 EPUB 后必须执行“分层随机抽检与问题族追杀”。发现译文质量问题族时，先在本书闭环，再把可复用经验合并进 `skills/translation-quality-defect-families/SKILL.md`。
未声明是否启用 LifeBook Digest 时，请自动判断；长篇小说、专业书籍、哲学书在 EPUB 输出后生成 Digest，短篇小说、自然科学类和其他类型不生成。
如需生成 Digest，请在书籍工程根目录写入 `digest.config.json`（`enabled=true`、`merge_into_epub=true`），并在仓库根目录运行：`python -m digest.lifebook_digest --book-root books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}`。输出仍然是本地标准 EPUB，不发布到 GitHub。
```

个人自用项目必须创建在 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/`，最终版本化产物在 `output/private_artifacts/`，不是公开 release，不得发布到 GitHub。

## EPUB 后精修审校 prompt（可选）

第一版 EPUB 已经生成后，不要只给 AI 一句“帮我精修”。请按目的选择下面两个 prompt：

- **Prompt B：章节全量复检与修复。** 用于担心之前翻译阶段没把每章质量做到位，或旧项目缺少 `qa/chapter_controls/*.control.md` 零问题 PASS 记录时。它会逐章做源文对照全量复检并修到零问题。
- **Prompt C：分层随机抽检与问题族追杀。** 用于第一版 EPUB 后的发布前置信度检查。它负责抽样发现系统性盲点、问题族全书审计、新 seed 复抽和 release/private artifact。

推荐顺序：如果书是旧流程或您不确定每章是否做过零问题复检，先跑 **Prompt B**，再跑 **Prompt C**。如果本书每章已有可靠的零问题 control 记录，可以直接跑 **Prompt C**。

### Prompt B：章节全量复检与修复

```text
本书项目：{书籍项目路径，例如 books/{target}/{number}_{目标语言书名}_{目标语言作者名}}

请先读取 AGENTS.md、该书 SKILL.md（如有）、template/epub_pipeline/README.md、template/epub_pipeline/common/README.md、template/epub_pipeline/common/prompts/08a_chapter_post_translation_control.md、template/epub_pipeline/common/references/quality_gate_framework.md、目标语言质量框架，以及 `skills/translation-quality-defect-families/SKILL.md`。

请设置 /goal：对本书所有已翻译章节执行“每章译后全量复检并修复”。每章必须对照整章原文、整章译文和读者可见上下文，覆盖但不限于忠实度、漏译误译、中文顺读、文学性、可读性和吸引力、教学/解释节奏、术语稳定、案例/专名/地名/书名/船名/机构名、标题与小标题、注释、图表/公式/表格/图片文字接口、源语句法残留、过硬过直过板句、过度解释、无依据加戏、读者可见 AI/制作痕迹、异常空格/乱码、旧纸书目录残留。

可并行处理不同章节，但每个章节必须独立闭环：每一轮都检查整章；只要发现任何问题，先修复该章，但该轮只能记为 `FIXED_RECHECK_REQUIRED`，不能 PASS；随后追加新一轮整章复查。只有最新一轮记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` 时，该章才算通过。

若任一章发现可复现译文质量问题族，例如短句切断、比喻自撞、排比标点拖拽、代词指代不清、源语句法残留、术语漂移、标题超载、过度解释或加戏，必须按 `skills/translation-quality-defect-families/SKILL.md` 处理：记录如何发现、如何归纳、如何用低 token 方法查全书同类、如何修复、如何复查。先用 `rg`、术语表、禁用写法、标题表、章节控制记录和小上下文原文对照收集候选，只把候选片段交给 agent 复核；不要让 agent 盲读全书。

完成后重新生成或更新 `qa/chapter_controls/*.control.md`、必要的 `qa/fidelity/`、`qa/readability/`、`qa/terminology/`、`qa/gates/` 记录，把通过章节写入或更新到 `chapters/final/`。然后重建 EPUB，运行可用的 chapter-control/preflight/publication lint/asset/EPUBCheck 命令。报告修复章节、问题族、验证命令结果和仍需进入 Prompt C 的事项。
```

### Prompt C：分层随机抽检与问题族追杀

`N` 是“连续无问题抽检轮数”：`1` 最省 token，是模板最低退出强度；`2` 更稳，推荐给普通书；`3` 更严格，适合术语密集、科学/数学/图表多或您想冲更高质量的书。

```text
本书项目：{书籍项目路径，例如 books/{target}/{number}_{目标语言书名}_{目标语言作者名}}
连续无问题抽检轮数 N：{1/2/3；默认 2}

请先读取 AGENTS.md、该书 SKILL.md（如有）、template/epub_pipeline/README.md、template/epub_pipeline/common/README.md、template/epub_pipeline/common/prompts/16a_stratified_random_spotcheck.md、template/epub_pipeline/common/references/stratified_random_spotcheck.md、template/epub_pipeline/common/references/quality_gate_framework.md、封面、book-info/frontmatter、图表资产、release 相关规则，以及 `skills/translation-quality-defect-families/SKILL.md`。

请设置 /goal：对已生成 EPUB 执行“分层随机抽检与问题族追杀”，并在通过后重新生成 release 或 private artifact。不要把本 prompt 当作普通润色；它的核心是发布前发现系统性盲点、全书同类审计、修复闭环和新 seed 复抽。

运行分层随机抽样，抽样总体是 reader-facing audit units，不是页数，也不只是段落。必须覆盖实际存在的 paragraph、table、figure、formula/proof、caption/note。至少派生 2 个独立评审 agent，互不参考，并按模板保存 `reviews/random_spotcheck/round_XXX/` 下的 seed、manifest、samples、evidence、reviews、fixes/fix_log.md、verification/closure_check.md。

若任一样本发现 P0/P1/P2、单项 <80、读者不可理解、忠实度偏移、事实/术语/专名/标题/注释/图表/公式错误、源语句法残留、过硬过直句、短句切断、比喻自撞、排比标点拖拽、代词指代不清、过度解释或加戏，必须在本轮把它归纳为问题族，执行全书同类问题审计并修复所有确认命中。不得只修被抽中的样本，不得等第二轮才查全书。

译文质量问题族必须优先低 token 审计：先用 `rg`、`glossary/terms.csv`、`forbidden_body_renderings`、标题映射、章节控制记录、抽样 manifest 和小上下文原文对照收集候选，再把候选片段交给 agent 复核。修复后在本轮 `fix_log.md` 和 `closure_check.md` 写清问题族、检索式/审计方法、命中数、修复位置、合理例外和复查结果；可复用经验合并进 `skills/translation-quality-defect-families/SKILL.md`，不要重复堆条目。

每次修复后必须重建 EPUB，并用新 seed 追加下一轮抽检。退出条件：最近连续 N 个新 seed 抽检轮均 PASS，所有已发现问题族均关闭，`npm run review:random-validate:pass` 通过，且 release_confidence 达到模板要求。

通过后清理或重建 staging，重新生成 EPUB，运行 publication lint、asset manifest、cover output、reader-facing policy、EPUBCheck，以及 release 或 private artifact 脚本。公版或授权项目的最终可发布 EPUB 必须输出到该书 output/release/，release_state.json.latest_status 必须为 PASS。个人自用项目的最终私人产物必须输出到 output/private_artifacts/，private_artifact_state.json.latest_status 必须为 PASS。报告 release EPUB 或 private artifact 路径、抽检轮次、修复摘要、验证命令结果和剩余风险。
```

## 您需要知道的关键位置

- `.\template\epub_pipeline`：查看当前有哪些源语言/语言方向模板。AI 会据此判断该用已有模板 prompt，还是新建语言模板 prompt。
- `.\tools\lifebook-launcher`：LifeBook Launcher 客户端安装启动目录。用户需要知道这个位置，以使用 LifeBook 项目和安装 OpenCode。
- `.\doc\public\user_prompt`：公共 prompt 放在这里。想了解提示词细节，或想手动修改 prompt 时，看这个目录。
- `.\books\zh-Hans`：最重要的成书目录。翻译成简体中文成功后，到对应书籍目录里找 `output\release\`；只有 release 目录里的成品才算可发布结果。
- `.\books\private`：个人自用书籍工程目录。非公版私人翻译的原文、译文、QA、EPUB 和 `output\private_artifacts\` 私人产物只应保存在这里；该目录被 Git 忽略，不发布到 GitHub。
- `.\digest`：LifeBook Digest 通用后处理模块。每本书通过自己的 `digest.config.json` 决定是否启用、是否把 Digest 章节合并进标准 EPUB。

## 四个翻译 prompt 是什么

- `doc/public/user_prompt/book_translation_existing_template.md`：仓库已经有对应源语言模板时使用，例如日语到简体中文、英语到简体中文、古希腊语到简体中文。
- `doc/public/user_prompt/book_translation_new_template.md`：仓库还没有对应源语言模板时使用，例如第一次做法语到简体中文。
- `doc/public/user_prompt/book_translation_private_existing_template.md`：个人自用、本地书源、已有对应源语言模板时使用。
- `doc/public/user_prompt/book_translation_private_new_template.md`：个人自用、本地书源、还没有对应源语言模板时使用。
- `doc/public/user_prompt/how_to_use_book_translation_prompts.md`：更短的小白版说明，只解释怎么填写三项内容。

如果您不确定该用哪个，就让 AI 先检查模板是否存在。普通用户不需要理解 `source-target`、slug、profile、release version 或 npm 命令。

## 选择哪个客户端

| 客户端 | 适合谁 | 怎么用本仓库 prompt |
| --- | --- | --- |
| Codex App | 想要图形界面、文件 diff、终端、浏览器都集成的人 | 打开仓库，新建 thread，粘贴 `/goal`，让它读模板并执行 |
| Claude Code | 熟悉终端、想用命令行 Agent 的人 | 在仓库中启动 Claude Code，粘贴目标 prompt |
| LifeBook Launcher | 想要最少手动步骤的人；<br>需安装 OpenCode 客户端支持 | 打开 Launcher，安装 OpenCode；<br>OpenCode 支持市面大多数模型（如 DeepSeek、豆包等）；<br>在 OpenCode 里选择翻译书籍任务，粘贴三项内容（见[完整示例](#最简单的启动方式)） |
| Google Antigravity | 想在 AI IDE 里让 agent 计划、改文件、跑命令的人 | 打开仓库 workspace，在 agent 输入框粘贴目标 prompt |

## LifeBook Launcher

如果您不想手动处理项目和客户端，可以使用 LifeBook Launcher。Launcher 可以下载并打开 OpenCode 客户端；OpenCode 支持市面上大多数 AI 模型，例如 DeepSeek、豆包等。使用前需要在 OpenCode 里配置对应模型的 API Key。

- 打开 **LifeBook Launcher**。
- 选择或打开本项目。
- 按需要下载或打开 OpenCode 客户端，并在 OpenCode 中配置 API Key。
- 粘贴三项内容：我要翻译的书、目标语言、自动选择 prompt 的规则（见[最简单的启动方式](#最简单的启动方式)里的完整示例）。
- 等 AI 完成后，公版或授权项目检查书籍目录里的 `output/release/`；个人自用项目检查 `output/private_artifacts/`。

## Codex App 用法

1. 安装并打开 Codex App。
2. 选择本仓库目录。
3. 新建一个 thread。
4. 粘贴上面的 `/goal`。
5. 等 AI 先读 `AGENTS.md` 和 `template/`。
6. 审查它要改的文件；确认无误后让它继续。
7. 最后检查 `books/zh-Hans/.../output/release/`，或对应目标语言的 `books/{target}/.../output/release/`；个人自用项目检查 `books/private/{target}/.../output/private_artifacts/`。

Codex App 适合这个仓库的长流程任务，因为它方便查看 AI 修改了哪些文件。

## Google Antigravity 用法

1. 安装 Google Antigravity。
2. 打开本仓库作为 workspace。
3. 在 agent 输入框粘贴目标 prompt。
4. 让 agent 先读 `AGENTS.md` 和 `template/epub_pipeline/`。
5. 开启需要确认的执行模式，避免 agent 在您没看清前执行危险命令。
6. 最后检查 diff、测试输出和 release 文件。

## 常见错误

- 让 AI 不读模板，直接翻译整本。
- 只生成 `output/book.epub`，公版项目没有 `output/release/`，或个人自用项目没有 `output/private_artifacts/`。
- 版权没查清就开始翻译。
- 使用现代译本作为参考或改写对象。
- 分层随机抽检发现问题后，没有追加新一轮。
- 把某本书的原文、译文或 QA 写回 `template/`。
