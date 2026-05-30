# AI 客户端使用说明：怎样让 AI 按本仓库模板做书

这份说明写给希望用 AI 客户端协作制书的人。你不需要会写代码；只需要打开项目、复制一段文字、检查 AI 做出来的书籍文件。

## 你要先明白的 3 件事

1. **普通用户只需要给三项内容。**
   你只需要告诉 AI“我要翻译的书”“目标语言”和“自动选择翻译 prompt 的规则”。“自动选择翻译 prompt 的规则”的完整写法见下面的[最简单的启动方式](#最简单的启动方式)。可靠来源、源语言、模板、目录名、release 和检查命令都由 AI 自动处理。

2. **让 AI 自己读规则。**
   你不需要理解仓库规则，只要要求 AI 自动选择正确的公共 prompt。

3. **最后只看 release 或私人产物结果。**
   AI 会自动完成来源核查、版权核查、翻译、审校、EPUB 构建、抽检和发布。公版或授权项目最后检查 `output/release/`；个人自用项目最后检查 `output/private_artifacts/`。

## 最简单的启动方式

打开你正在使用的 AI 客户端，进入这个项目或让 Launcher 打开项目。

然后复制下面这段，把 `{...}` 换成你的书名和目标语言：

### 公版书翻译 prompt

```text
我要翻译的书：{书名、作者（可选）；如果你已经有可靠来源链接，也可以贴上}
目标语言：{例如 简体中文}

请自动选择正确的翻译 prompt：
- 如已有对应源语言模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应源语言模板，执行 doc/public/user_prompt/book_translation_new_template.md。

除非版权或来源无法确认，不要让我填写技术字段。请自动查找可靠公版来源，自动创建项目，完成翻译、审校、EPUB 构建、分层随机抽检和 release。
未声明是否启用 LifeBook Digest 时，请自动判断；长篇小说、专业书籍、哲学书在 EPUB 输出后生成 Digest，短篇小说、自然科学类和其他类型不生成。
如需生成 Digest，请在书籍工程根目录写入 `digest.config.json`（`enabled=true`、`merge_into_epub=true`），并在仓库根目录运行：`python -m digest.lifebook_digest --book-root books/{target}/{number}_{book_id_slug}`。输出仍然是标准 EPUB。
```

## 个人自用书翻译 prompt

如果这是你自己已有的本地书源，只供个人学习自用，不传播、不商业使用，可以使用下面这段：

```text
我要翻译的书：{书名、本地目录: XXX }
目标语言： {例如 简体中文}

请自动选择正确的翻译 prompt：
- 如已有对应源语言模板，执行 doc/public/user_prompt/book_translation_private_existing_template.md。
- 如无对应源语言模板，执行 doc/public/user_prompt/book_translation_private_new_template.md。

这是我个人自用的,不传播,不用于商业,使用我给出的本地的书源。
请自动创建项目，严格完成整个模板规定的系统翻译流程,不允许有任何遗漏。
未声明是否启用 LifeBook Digest 时，请自动判断；长篇小说、专业书籍、哲学书在 EPUB 输出后生成 Digest，短篇小说、自然科学类和其他类型不生成。
如需生成 Digest，请在书籍工程根目录写入 `digest.config.json`（`enabled=true`、`merge_into_epub=true`），并在仓库根目录运行：`python -m digest.lifebook_digest --book-root books/private/{target}/{number}_{book_id_slug}`。输出仍然是本地标准 EPUB，不发布到 GitHub。
```

个人自用项目必须创建在 `books/private/{target}/{number}_{slug}/`，最终版本化产物在 `output/private_artifacts/`，不是公开 release，不得发布到 GitHub。

## 精修审校 prompt（可选）

第一版 EPUB 已经生成后，如果你想继续提高译本质量，可以再使用下面这段。`N` 是“连续无问题轮数”：`1` 最省 token，`3` 更严格，质量要求更高；不确定时填 `2`。

```text
本书项目：{书籍项目路径，例如 books/{target}/{number}_{slug}}
连续无问题退出轮数 N：{1/2/3；默认 2}

请先读取 AGENTS.md、该书 SKILL.md（如有）、template/epub_pipeline/README.md、template/epub_pipeline/common/README.md，以及封面、book-info/frontmatter、图表资产、质量门禁、分层随机抽检、release 相关规则。

请设置 /goal：对已生成 EPUB 做精修审校，严格按模板要求检查封面、首页/前置页、metadata、nav、目录、正文、注释、图表、公式、表格、图片、样式、读者可见内容、EPUB 构建与 release。不得只检查我点名的项目。

启动 2 个独立评审 agent 做分层随机抽检。至少执行 4 轮；每轮使用新 seed，并按模板保存样本、证据、评审、修复和闭环记录。若任何轮发现 P0/P1/P2、单项 <70、读者不可理解、事实/术语/图表/公式错误或模板硬门禁失败，修复后必须追加新一轮。

退出条件：最近连续 N 轮均无新增阻塞问题，且 npm run review:random-validate:pass 通过。N=1 为最低强度，较省 token；N=3 更严格，审校后译本质量更高，用户可自行调整。

通过后清理或重建 staging，重新生成 EPUB，运行 publication lint、asset manifest、cover output、reader-facing policy、EPUBCheck，以及 release 或 private artifact 脚本。公版或授权项目的最终可发布 EPUB 必须输出到该书 output/release/，release_state.json.latest_status 必须为 PASS。个人自用项目的最终私人产物必须输出到 output/private_artifacts/，private_artifact_state.json.latest_status 必须为 PASS。报告 release EPUB 或 private artifact 路径、抽检轮次、修复摘要、验证命令结果和剩余风险。
```

## 你需要知道的关键位置

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

如果你不确定该用哪个，就让 AI 先检查模板是否存在。普通用户不需要理解 `source-target`、slug、profile、release version 或 npm 命令。

## 选择哪个客户端

| 客户端 | 适合谁 | 怎么用本仓库 prompt |
| --- | --- | --- |
| Codex App | 想要图形界面、文件 diff、终端、浏览器都集成的人 | 打开仓库，新建 thread，粘贴 `/goal`，让它读模板并执行 |
| Claude Code | 熟悉终端、想用命令行 Agent 的人 | 在仓库中启动 Claude Code，粘贴目标 prompt |
| LifeBook Launcher | 想要最少手动步骤的人；<br>需安装 OpenCode 客户端支持 | 打开 Launcher，安装 OpenCode；<br>OpenCode 支持市面大多数模型（如 DeepSeek、豆包等）；<br>在 OpenCode 里选择翻译书籍任务，粘贴三项内容（见[完整示例](#最简单的启动方式)） |
| Google Antigravity | 想在 AI IDE 里让 agent 计划、改文件、跑命令的人 | 打开仓库 workspace，在 agent 输入框粘贴目标 prompt |

## LifeBook Launcher

如果你不想手动处理项目和客户端，可以使用 LifeBook Launcher。Launcher 可以下载并打开 OpenCode 客户端；OpenCode 支持市面上大多数 AI 模型，例如 DeepSeek、豆包等。使用前需要在 OpenCode 里配置对应模型的 API Key。

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
5. 开启需要确认的执行模式，避免 agent 在你没看清前执行危险命令。
6. 最后检查 diff、测试输出和 release 文件。

## 常见错误

- 让 AI 不读模板，直接翻译整本。
- 只生成 `output/book.epub`，公版项目没有 `output/release/`，或个人自用项目没有 `output/private_artifacts/`。
- 版权没查清就开始翻译。
- 使用现代译本作为参考或改写对象。
- 分层随机抽检发现问题后，没有追加新一轮。
- 把某本书的原文、译文或 QA 写回 `template/`。
