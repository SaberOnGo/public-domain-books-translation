# AI 客户端接入总览

本项目是一套文件驱动的公版书翻译与 EPUB 生产流水线，不绑定某个模型或客户端。

核心规则源只有两层：

- `AGENTS.md`
- `template/epub_pipeline/`

OpenCode、Codex App、Claude Code、aider、Antigravity、本地模型客户端或其他能读写本地文件的 agent，都只是客户端。客户端可以帮助读取规则、创建书籍工程、翻译、审校、运行脚本和记录 QA，但不能替代核心规则。

## 客户端边界

| 客户端 | 推荐用途 | 规则入口 |
| --- | --- | --- |
| Codex App | 本地仓库改动、脚本执行、长流程协作 | `AGENTS.md` + `template/epub_pipeline/` |
| Claude Code | 本地 agent 执行、工程维护、批量任务 | `AGENTS.md` + `template/epub_pipeline/` |
| OpenCode | 开源轻量客户端、一键启动、DeepSeek/Qwen/OpenAI/本地模型接入 | `opencode.jsonc` + `.opencode/` + 核心规则 |
| aider | 轻量终端协作、明确文件范围的翻译或维护 | 手动指定核心规则文件 |
| Antigravity | 本地文件 agent 工作流 | `AGENTS.md` + `template/epub_pipeline/` |

## 不变规则

- 新书必须用 `books/scripts/create_book_project.py` 创建。
- 新书路径必须是 `books/{target}/{number}_{book_id_slug}/`。
- 具体书籍的原文、译文、QA、EPUB 输出和 metadata 只能写入书籍工程目录。
- 不要把具体书籍产物写回 `template/`。
- 版权或公版状态不清楚时停止。
- AI 初稿不能发布；必须经过来源证据、权利核查、研究、试译、章节门禁、EPUB 校验、分层随机抽检、独立评审、版本化 release 和复盘记录。

## OpenCode 适配层

本仓库提供一个薄 OpenCode 适配层：

- `opencode.jsonc`：项目级 OpenCode 配置，只列规则入口、watcher ignore 和基本权限。
- `.opencode/agents/book-runner.md`：可执行书籍流水线的 agent。
- `.opencode/agents/book-reviewer.md`：只读评审 agent。
- `.opencode/commands/*.md`：常用流程快捷命令。
- `tools/lifebook-launcher/`：LifeBook Launcher 桌面启动器入口；Windows 用户双击 `LifeBook Launcher Setup.exe`。
- `tools/lifebook-launcher/source/`：LifeBook Launcher 源码目录，供开发者打包和维护。

这些文件不定义翻译标准、版权政策、EPUB 规则、质量门禁或发布规则。它们只帮助 OpenCode 正确进入本项目。

`opencode.jsonc` 会把 `book-runner` 设为默认 agent，并把仓库根目录的 `skills/` 注册为 OpenCode 可发现的 skills 路径。这样 OpenCode 可以复用 `skills/public-domain-epub-pipeline/SKILL.md`，但规则仍然只有一份，不在 `.opencode/` 内复制。

## 打包原则

推荐发布两种包：

- 标准包：包含本仓库、`.opencode/`、`opencode.jsonc`、`tools/lifebook-launcher/`、文档和可双击的 LifeBook Launcher 应用。用户通过 Launcher 检查和更新 LifeBook / OpenCode Desktop。
- Windows 开箱包：在 release 附件中额外附带固定版本 OpenCode 二进制和其许可证；仓库本身不提交二进制。

不要把 DeepSeek、Qwen、Claude、OpenAI 或本地模型写死进流水线。模型只属于客户端配置。
