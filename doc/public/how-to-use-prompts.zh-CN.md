# AI 客户端使用说明：怎样让 AI 按本仓库模板做书

这份说明写给希望用 AI 客户端协作制书的人。你不需要会写代码；只需要会打开这个仓库、复制一段 prompt、检查 AI 做出来的文件。

> 重要：不要把 API Key 写进仓库文件，不要提交 `auth.json`、`.env`、配置截图或任何密钥。

## 你要先明白的 3 件事

1. **普通用户只需要给两项信息。**
   你只需要告诉 AI“我要翻译的书”和“目标语言”。可靠来源、源语言、模板、目录名、release 和检查命令都由 AI 自动处理。

2. **本仓库必须先读规则。**
   每次都要求 AI 先读 `AGENTS.md`，再读 `template/epub_pipeline/` 下的模板规则。不要让 AI 凭记忆做书。

3. **不要直接把 AI 初稿当成成品。**
   正确流程是：来源核查、版权核查、译前研究、试译、分章翻译、章节审校、EPUB 构建、EPUBCheck、分层随机抽检、release。

## 最简单的启动方式

打开任意 AI 客户端后，先进入仓库根目录：

```powershell
cd D:\project\49_public-domain-books-translation
```

如果你是从发布版只安装了 LifeBook Launcher，就进入 Launcher 自动准备好的项目目录；Windows 默认是 `D:\LifeBook`。

然后复制下面这段，把 `{...}` 换成你的书名和目标语言：

```text
我要翻译的书：{书名、作者；如果你已经有可靠来源链接，也可以贴上}
目标语言：{例如 简体中文}

请在当前仓库自动选择正确的公版书翻译 prompt：
- 如果已有对应源语言模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如果没有对应源语言模板，执行 doc/public/user_prompt/book_translation_new_template.md。

除非版权或来源无法确认，不要让我填写技术字段。请自动查找可靠公版来源，自动创建项目，完成翻译、审校、EPUB 构建、分层随机抽检和 release。
```

没有 `/goal` 的客户端也可以用，把第一行改成：

```text
目标：请在当前仓库制作一本新的公版书翻译 EPUB。
```

## 你需要知道的 4 个目录

- `.\template\epub_pipeline`：查看当前有哪些源语言/语言方向模板。
- `.\tools\lifebook-launcher`：仓库副本里的 LifeBook Launcher 入口目录。发布版用户通常直接启动已安装的 Launcher，它会自动准备项目目录。
- `.\doc\public\user_prompt`：公共提示词目录；想看 prompt 细节或手动调整时看这里。
- `.\books\zh-Hans`：简体中文书籍输出目录；书做好后，到对应书籍目录找 `output\book.epub` 和 `output\release\`。

## 两个公共 prompt 是什么

- `doc/public/user_prompt/book_translation_existing_template.md`：仓库已经有对应源语言模板时使用，例如日语到简体中文、英语到简体中文、古希腊语到简体中文。
- `doc/public/user_prompt/book_translation_new_template.md`：仓库还没有对应源语言模板时使用，例如第一次做法语到简体中文。
- `doc/public/user_prompt/how_to_use_book_translation_prompts.md`：更短的小白版说明，只解释怎么填写“我要翻译的书”和“目标语言”。

如果你不确定该用哪个，就让 AI 先检查模板是否存在。普通用户不需要理解 `source-target`、slug、profile、release version 或 npm 命令。

## 选择哪个客户端

| 客户端 | 适合谁 | 怎么用本仓库 prompt |
| --- | --- | --- |
| Codex App | 想要图形界面、文件 diff、终端、浏览器都集成的人 | 打开仓库，新建 thread，粘贴 `/goal`，让它读模板并执行 |
| Claude Code | 想在终端里用 Claude/DeepSeek 跑 agent 的人 | 进入仓库目录，运行 `claude`，粘贴目标 prompt |
| Google Antigravity | 想在 AI IDE 里让 agent 计划、改文件、跑命令的人 | 打开仓库 workspace，在 agent 输入框粘贴目标 prompt |
| OpenCode | 想用开源客户端，并方便接 DeepSeek 的人 | 用 LifeBook Launcher 检查/更新 OpenCode Desktop，打开仓库后粘贴目标 prompt |

## LifeBook Launcher

如果你不想手动处理项目和客户端更新，可以使用 LifeBook Launcher。它不会保存 API Key，也不会把 OpenCode 本体放进仓库。

- 普通用户拿到发布包后，双击 **LifeBook Launcher** 应用或安装包即可。
- 当前 Windows 本地入口：`tools\lifebook-launcher\LifeBook Launcher Setup.exe`。
- 开发者源码目录：`tools/lifebook-launcher/source/`。
- 它会自动准备并更新 LifeBook 项目；Windows 默认项目目录是 `D:\LifeBook`。
- 它可以检查并更新 OpenCode Desktop，也可以下载、安装并重启 LifeBook Launcher 自身。
- 用户可以在设置里开启或关闭开机自动启动。

## Codex App 用法

1. 安装并打开 Codex App。
2. 选择本仓库目录。
3. 新建一个 thread。
4. 粘贴上面的 `/goal`。
5. 等 AI 先读 `AGENTS.md` 和 `template/`。
6. 审查它要改的文件；确认无误后让它继续。
7. 最后检查 `books/.../output/release/`。

Codex App 的重点是项目线程、worktree、内置终端、diff review 和 Git 操作。它适合这个仓库的长流程任务。

DeepSeek 说明：Codex App 通常使用 OpenAI/Codex 登录后的模型。若你想用 DeepSeek，优先用 OpenCode 或 Claude Code；只有在你的 Codex CLI/网关明确支持对应 OpenAI-compatible 或 Responses API 时，才尝试自定义 provider。

## Claude Code 接入 DeepSeek

DeepSeek 官方提供了 Claude Code 接入方式。Windows PowerShell 可以临时这样设置：

```powershell
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="<你的 DeepSeek API Key>"
$env:ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_EFFORT_LEVEL="max"

cd D:\project\49_public-domain-books-translation
claude
```

macOS/Linux：

```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN="<your DeepSeek API Key>"
export ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_EFFORT_LEVEL=max

cd /path/to/49_public-domain-books-translation
claude
```

进入后粘贴本说明开头的目标 prompt。

## OpenCode 接入 DeepSeek

OpenCode 是尝试 DeepSeek 的直接选择之一。

1. 安装 OpenCode。
2. 打开终端，进入仓库：

```powershell
cd D:\project\49_public-domain-books-translation
opencode
```

3. 在 OpenCode 输入框里输入：

```text
/connect
```

4. 搜索并选择 `deepseek`。
5. 粘贴你的 DeepSeek API Key。
6. 选择 `DeepSeek-V4-Pro`。
7. 粘贴本说明开头的 `/goal` prompt。

如果你只想让 AI 先计划，不马上改文件，可以在 prompt 后加一句：

```text
先只给执行计划和将要修改的文件列表，等我确认后再写文件。
```

## Google Antigravity 用法

1. 安装 Google Antigravity。
2. 打开本仓库作为 workspace。
3. 在 agent 输入框粘贴目标 prompt。
4. 让 agent 先读 `AGENTS.md` 和 `template/epub_pipeline/`。
5. 开启需要确认的执行模式，避免 agent 在你没看清前执行危险命令。
6. 最后检查 diff、测试输出和 release 文件。

DeepSeek 说明：如果 Antigravity 当前界面没有 DeepSeek provider，就不要硬改配置。使用它内置支持的模型跑本仓库流程；需要 DeepSeek 时改用 OpenCode 或 Claude Code。

## Codex CLI 自定义 provider 提醒

Codex 的配置文件支持 `model_provider` 和 `model_providers.<id>`。官方配置项包括 `base_url`、`env_key` 等。
但 DeepSeek 的普通 OpenAI-compatible endpoint 是 Chat Completions 形式；如果你的 Codex 版本或中间网关不支持相应协议，不要强行配置。优先用 Codex App 默认模型，或用 OpenCode/Claude Code 接 DeepSeek。

## 做书时常用的检查命令

进入某本书目录后：

```powershell
npm run build:epub
npm run check:epub
npm run review:random-samples
npm run review:random-validate:pass
npm run release:create
```

如果没有安装依赖，先在 `books/` 目录运行一次：

```powershell
cd D:\project\49_public-domain-books-translation\books
npm install
```

## 常见错误

- 把 API Key 写进 Markdown 或配置文件并提交。
- 让 AI 不读模板，直接翻译整本。
- 只生成 `output/book.epub`，没有 `output/release/`。
- 版权没查清就开始翻译。
- 使用现代译本作为参考或改写对象。
- 分层随机抽检发现问题后，没有追加新一轮。
- 把某本书的原文、译文或 QA 写回 `template/`。

## 参考链接

- Codex App 官方说明：https://developers.openai.com/codex/app
- Codex 配置参考：https://developers.openai.com/codex/config-reference
- DeepSeek API 快速开始：https://api-docs.deepseek.com/
- DeepSeek 接入 Claude Code：https://api-docs.deepseek.com/guides/agent_integrations/claude_code
- DeepSeek 接入 OpenCode：https://api-docs.deepseek.com/guides/agent_integrations/opencode
- OpenCode provider 文档：https://open-code.ai/en/docs/providers
- Google Antigravity 文档：https://www.antigravity.google/docs/overview
