# OpenCode 客户端接入

OpenCode 在本项目中只是一个本地 AI 客户端适配层。它可以连接 DeepSeek、Qwen、Claude、OpenAI、OpenRouter、本地 OpenAI-compatible 服务或其他 provider，但不改变本项目的核心流水线。

## 推荐入口：LifeBook Launcher

普通用户推荐使用：

```text
tools\lifebook-launcher\LifeBook Launcher Setup.exe
```

LifeBook Launcher 会：

- 自动准备并更新 LifeBook 项目；Windows 默认项目目录是 `D:\LifeBook`。
- 在首页显示最近一条 LifeBook commit 更新内容，需要时可展开查看更多。
- 检查并更新 OpenCode Desktop。
- 检查、下载并安装 LifeBook Launcher 自身更新。
- 允许用户开启或关闭开机自动启动。
- 保持 API Key 在用户本机客户端中，不写入仓库。

开发者需要维护或重新打包 Launcher 时，再进入源码目录 `tools/lifebook-launcher/source/`。

## OpenCode 适配文件

```text
opencode.jsonc
.opencode/
  agents/
    book-runner.md
    book-reviewer.md
  commands/
    new-book.md
    run-gates.md
    random-spotcheck.md
```

`opencode.jsonc` 和 `.opencode/` 只是客户端适配层，不是流程规则源。核心规则仍然来自：

- `AGENTS.md`
- `template/epub_pipeline/`
- `skills/public-domain-epub-pipeline/SKILL.md`

## 连接 DeepSeek

在 OpenCode Desktop 中连接 provider。若客户端提供命令面板或聊天命令，也可以使用：

```text
/connect
```

选择 `DeepSeek`，输入 DeepSeek Platform API Key，然后选择需要的 DeepSeek 模型。

注意：

- DeepSeek 网页聊天账号或订阅账号不等于 API Key。
- 本项目不保存、不提交、不打包任何用户 API Key。
- DeepSeek 只是可选 provider；也可以使用 Qwen、OpenAI、Claude、OpenRouter、本地模型或其他 provider。

## 推荐首次提示

```text
请使用 book-runner agent。先读取 AGENTS.md，然后读取 template/epub_pipeline/README.md、template/epub_pipeline/common/README.md 和 skills/public-domain-epub-pipeline/SKILL.md。

本项目是模型无关的公版书翻译与 EPUB 生产流水线。OpenCode 只是客户端适配层，不能把 .opencode/ 当作规则源。
```

## 常用命令

OpenCode 中可以使用：

```text
/new-book <book_id_slug> --source-target <source-target> [SOURCE_URL]
/run-gates <books/{target}/{number}_{book_id_slug}>
/random-spotcheck <books/{target}/{number}_{book_id_slug}>
```

这些命令会生成任务提示，不会绕过核心规则。执行前仍必须读取 `AGENTS.md` 和对应 template 规则。
