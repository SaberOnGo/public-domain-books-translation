# 客户端适配与一键启动打包

本项目可以打包成“LifeBook Launcher + 客户端适配 + 自动准备项目”，但不要打包成“OpenCode 专属系统”。

## 推荐交付形态

```text
release assets:
  LifeBook Launcher Setup.exe

user project folder:
  D:\LifeBook\                  # Windows 默认；由 Launcher 自动准备和更新
    AGENTS.md
    template/
    books/
    skills/
    doc/project/
    .opencode/
    opencode.jsonc
```

## 标准包

标准包不内置 OpenCode 二进制，也不要求普通用户先下载整个仓库。用户安装 LifeBook Launcher 后，由 Launcher 自动准备和更新 LifeBook 项目目录。

发布包里应提供可双击的 **LifeBook Launcher** 应用或安装包。当前仓库内 Windows 本地入口是 `tools\lifebook-launcher\LifeBook Launcher Setup.exe`；源码目录是 `tools\lifebook-launcher\source\`，供开发者维护和重新打包。

优点：

- 包体小。
- LifeBook 项目可由 LifeBook Launcher 自动准备和更新。
- OpenCode Desktop 可由 LifeBook Launcher 检查并下载官方安装包。
- 更容易升级和排查。
- 不需要在仓库提交第三方二进制。

Launcher 应显示下载进度、网络错误、代理提示、系统架构和本地安装状态。OpenCode 和 Launcher 自更新下载应使用 `.part` 临时文件尽量支持断点续传。LifeBook 项目默认自动更新；首页只展示最近一条 LifeBook commit，有更多更新时允许展开查看，并在工作区有本地改动时停止更新。

GitHub 推送规则是打包层的强制依赖：每个推送到 GitHub 的 commit 必须有标题和详细正文摘要，正文必须分成 `ZH:`、`EN:`、`JA:` 三段；语言标签必须独占一行，摘要从下一行开始，不能写成 `ZH: 很长的摘要……`。推送前必须运行 `python tools/git/check_commit_messages.py --range origin/main..HEAD` 或当前分支对应 range，确保 LifeBook Launcher 有足够的多语言更新摘要可展示。

## Windows 开箱包

Windows 开箱包可以在 release 附件中额外附带固定版本 OpenCode zip 或 exe，但不要把二进制提交进 git 历史。

必须记录：

- OpenCode 版本。
- 下载来源。
- 校验方式或 checksum。
- OpenCode 许可证文件。
- 本项目自身许可证和贡献者规则。

用户 API Key 不得打包、不得写入仓库、不得写入 release。

## 模型无关

打包层只能说明如何连接 provider，不能把 provider 写死进流水线。

允许示例：

- DeepSeek API Key
- Qwen API Key
- Claude / Anthropic API Key
- OpenAI API Key
- OpenRouter API Key
- 本地 OpenAI-compatible 服务

不允许：

- 把 DeepSeek 作为默认翻译规则。
- 在 `template/epub_pipeline/` 中写入某个模型专属流程。
- 把模型名称、prompt 调参或客户端限制写进读者可见 EPUB。
- 用客户端配置替代版权、来源、质量门禁或 release 规则。
