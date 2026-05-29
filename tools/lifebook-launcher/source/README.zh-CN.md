# LifeBook Launcher

LifeBook Launcher 是本仓库的桌面启动器和更新中心。它负责：

- 自动准备并更新 LifeBook 公版书翻译系统；Windows 默认项目目录是 `D:\LifeBook`。普通用户不需要预装 Git，Launcher 首次准备和后续同步都只使用 GitHub archive ZIP 下载。
- 检查并更新 OpenCode Desktop 客户端。
- 检查、下载、安装并重启 LifeBook Launcher 自身更新。
- 在界面中显示最近的 GitHub commit 更新内容。
- 允许用户设置是否开机自动启动。

## 使用方式

普通用户不需要运行下面的开发命令。Windows 用户可在上一层目录双击：

```text
tools\lifebook-launcher\LifeBook Launcher Setup.exe
```

开发环境运行：

```powershell
cd tools\lifebook-launcher\source
npm install
npm run tauri:dev
```

正式打包：

```powershell
cd tools\lifebook-launcher\source
npm run tauri:build
```

Windows 打包成功后会生成：

```text
src-tauri\target\release\bundle\nsis\LifeBook Launcher_1.3.2_x64-setup.exe
src-tauri\target\release\bundle\msi\LifeBook Launcher_1.3.2_x64_en-US.msi
```

## Windows 兼容性

当前 Launcher 基于 Tauri 2 和 Microsoft Edge WebView2。公开发行版支持 Windows 10 / Windows 11 x64；Windows 7 不再作为可支持安装目标。

Win7 用户看到 `MicrosoftEdgeUpdate.exe - 无法找到入口`、`GetPackagesByPackageFamily`、`KERNEL32.dll` 或 WebView2 安装中断时，根因是 Microsoft Edge/WebView2 对 Win7/8/8.1 的支持已经停留在 109 系列，当前 WebView2 Evergreen 安装器与运行时更新链路不再兼容 Win7。Launcher 安装包使用 `embedBootstrapper`，只是把 Evergreen bootstrapper 打进安装包，避免在安装时先下载 bootstrapper 导致 Win10/Win11 弱网机器直接失败；它仍然会运行 Microsoft 的 Evergreen 安装链路，不能把 Win7 变成当前 WebView2 的受支持系统。

如果未来确实要做 Win7 专门版本，不能只靠 `embedBootstrapper`。需要改成 `fixedRuntime`，随安装包携带 Win7 可用的 WebView2 109 固定版运行时，并接受安装包明显变大、WebView2 安全更新停留在旧版本、Tauri/WebView2 新能力可能不可用的限制。当前公开发行版不走这个分支，仍以 Windows 10 / Windows 11 为支持目标。

如果用户在 Windows 10/11 上启动后停在“正在检查运行环境”或窗口退出，请让用户导出或提供：

```text
%LOCALAPPDATA%\LifeBook\launcher\logs\lifebook-launcher.log
```

日志会记录启动期 panic、前端未捕获错误、Python/Java 探测超时，以及私有运行时下载/解压失败原因。

开发环境需要 Node.js 与 Rust。仓库已在本目录固定 Rust `1.88.0`，避免因本机默认 Rust 版本过旧导致 Tauri 依赖无法编译。

## 安全规则

- Launcher 不保存 API Key。
- Launcher 不把 OpenCode 本体提交进仓库。
- Launcher 与 OpenCode 下载都显示进度，并使用 `.part` 临时文件；网络中断后再次更新会尽量续传。
- Launcher 自更新下载完成后会退出当前窗口、运行安装器并重新启动。
- 自动更新 LifeBook 前会检查 archive 托管文件；如果有本地改动，会停止更新，避免覆盖用户文件。archive 模式会记录托管文件 hash manifest，后续更新只覆盖未被用户改过的托管文件；旧版 Git 托管目录不会再调用本机 `git` 更新，需要重新选择空目录并用 archive ZIP 准备。
- LifeBook 流水线规则仍然只来自 `AGENTS.md`、`template/epub_pipeline/` 和 `skills/public-domain-epub-pipeline/SKILL.md`。
- LifeBook 更新内容来自 GitHub commit 信息；推送前每个 commit 必须有标题和 `ZH:`、`EN:`、`JA:` 三段详细摘要，语言标签必须独占一行，并通过 `python tools/git/check_commit_messages.py --range origin/main..HEAD` 检查。
