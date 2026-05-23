# AI 客户端使用说明：怎样让 AI 按本仓库模板做书

这份说明写给希望用 AI 客户端协作制书的人。你不需要会写代码；只需要打开项目、复制一段文字、检查 AI 做出来的书籍文件。

## 你要先明白的 3 件事

1. **普通用户只需要给三项内容。**
   你只需要告诉 AI“我要翻译的书”“目标语言”和“自动选择翻译 prompt 的规则”。可靠来源、源语言、模板、目录名、release 和检查命令都由 AI 自动处理。

2. **让 AI 自己读规则。**
   你不需要理解仓库规则，只要要求 AI 自动选择正确的公共 prompt。

3. **最后只看 release 结果。**
   AI 会自动完成来源核查、版权核查、翻译、审校、EPUB 构建、抽检和发布。你最后检查 `output/release/` 里的成品。

## 最简单的启动方式

打开你正在使用的 AI 客户端，进入这个项目或让 Launcher 打开项目。

然后复制下面这段，把 `{...}` 换成你的书名和目标语言：

```text
我要翻译的书：{书名、作者（可选）；如果你已经有可靠来源链接，也可以贴上}
目标语言：{例如 简体中文}

请自动选择正确的翻译 prompt：
- 如已有对应源语言模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应源语言模板，执行 doc/public/user_prompt/book_translation_new_template.md。

除非版权或来源无法确认，不要让我填写技术字段。请自动查找可靠公版来源，自动创建项目，完成翻译、审校、EPUB 构建、分层随机抽检和 release。
```

## 你需要知道的关键位置

- `doc/public/user_prompt/`：公共 prompt 放在这里。
- `books/.../output/release/`：AI 完成后，可发布 EPUB 放在这里。

## 两个公共 prompt 是什么

- `doc/public/user_prompt/book_translation_existing_template.md`：仓库已经有对应源语言模板时使用，例如日语到简体中文、英语到简体中文、古希腊语到简体中文。
- `doc/public/user_prompt/book_translation_new_template.md`：仓库还没有对应源语言模板时使用，例如第一次做法语到简体中文。
- `doc/public/user_prompt/how_to_use_book_translation_prompts.md`：更短的小白版说明，只解释怎么填写三项内容。

如果你不确定该用哪个，就让 AI 先检查模板是否存在。普通用户不需要理解 `source-target`、slug、profile、release version 或 npm 命令。

## 选择哪个客户端

| 客户端 | 适合谁 | 怎么用本仓库 prompt |
| --- | --- | --- |
| Codex App | 想要图形界面、文件 diff、终端、浏览器都集成的人 | 打开仓库，新建 thread，粘贴 `/goal`，让它读模板并执行 |
| Claude Code | 熟悉终端、想用命令行 Agent 的人 | 在仓库中启动 Claude Code，粘贴目标 prompt |
| LifeBook Launcher | 想要最少手动步骤的人；<br>需安装 OpenCode 客户端支持 | 打开 Launcher，安装 OpenCode；<br>OpenCode 支持市面大多数模型（如 DeepSeek、豆包等）；<br>在 OpenCode 里选择翻译书籍任务，粘贴三项内容 |
| Google Antigravity | 想在 AI IDE 里让 agent 计划、改文件、跑命令的人 | 打开仓库 workspace，在 agent 输入框粘贴目标 prompt |

## LifeBook Launcher

如果你不想手动处理项目和客户端，可以使用 LifeBook Launcher。Launcher 可以下载并打开 OpenCode 客户端；OpenCode 支持市面上大多数 AI 模型，例如 DeepSeek、豆包等。使用前需要在 OpenCode 里配置对应模型的 API Key。

- 打开 **LifeBook Launcher**。
- 选择或打开本项目。
- 按需要下载或打开 OpenCode 客户端，并在 OpenCode 中配置 API Key。
- 粘贴三项内容：我要翻译的书、目标语言、自动选择 prompt 的规则。
- 等 AI 完成后，检查书籍目录里的 `output/release/`。

## Codex App 用法

1. 安装并打开 Codex App。
2. 选择本仓库目录。
3. 新建一个 thread。
4. 粘贴上面的 `/goal`。
5. 等 AI 先读 `AGENTS.md` 和 `template/`。
6. 审查它要改的文件；确认无误后让它继续。
7. 最后检查 `books/.../output/release/`。

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
- 只生成 `output/book.epub`，没有 `output/release/`。
- 版权没查清就开始翻译。
- 使用现代译本作为参考或改写对象。
- 分层随机抽检发现问题后，没有追加新一轮。
- 把某本书的原文、译文或 QA 写回 `template/`。
