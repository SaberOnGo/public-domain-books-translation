# LifeBook Launcher 设计说明

LifeBook Launcher 是本仓库面向普通用户的桌面入口。它不是 OpenCode 专属工具，也不是脚本包装器；它负责把 LifeBook 公版书翻译系统和可选 AI 客户端连接起来，并用清晰的 GUI 管理更新。

## 产品边界

- 名称统一为 `LifeBook Launcher`。
- 核心流水线仍然只来自 `AGENTS.md`、`template/epub_pipeline/` 和 `skills/public-domain-epub-pipeline/SKILL.md`。
- Launcher 不保存、不提交、不打包任何 API Key。
- Launcher 不把 OpenCode 当作规则源；OpenCode 只是可下载、可更新、可启动的 AI 客户端之一。
- 根目录 `README.md`、`README.zh-CN.md` 等文档保留，只更新启动器说明，不删除。

## 用户体验目标

- 用户双击一个清楚的入口，就看到完整 GUI，不再看到一闪而过的命令行窗口。
- 界面按系统语言自动选择简体中文、繁体中文、日文或英文文案。
- 默认使用自定义桌面标题栏，窗口内容与设计稿里的单窗口产品界面保持一致。
- GUI 要像正式桌面产品：信息密度适中、按钮清楚、状态可读、错误有解释。
- 用户能一眼看到两个更新对象：
  - `LifeBook 项目`
  - `OpenCode 客户端`
- LifeBook 项目由 Launcher 自动准备和更新；普通用户不需要手动点击“检查 LifeBook”或“更新 LifeBook”。
- `本次 LifeBook 更新内容` 默认显示 Launcher 可取得的全部历史 commit；窗口仍保持固定大小，更新内容区域右侧显示滚动条并在区域内滚动，避免撑爆界面。
- 用户可设置是否开机自动启动 LifeBook Launcher。

## 主界面结构

主窗口尺寸约 `1180 x 760`，最小尺寸约 `960 x 640`。

- 左侧导航：总览、更新、教程、设置、日志。
- 顶部状态栏：当前分支、本地改动状态、代理检测状态、开机自启状态。
- 主区第一行：两个更新卡片。
  - `LifeBook 项目`：当前 commit、项目状态、按钮 `打开成书目录`、`查看项目`，更多菜单用于更改项目目录。
  - `OpenCode 客户端`：本地版本、最新版本、按钮 `检查更新/立即更新/安装客户端`、`启动客户端`。已检测到客户端时启动按钮为绿色；未检测到时为灰色禁用。
- 主区第二行：`本次 LifeBook 更新内容`。
  - 每条 commit 显示日期、短 hash、标题、摘要。
  - GitHub 上的每条 commit 必须提供标题和详细正文摘要；正文必须分成 `ZH:`、`EN:`、`JA:` 三段，且语言标签必须独占一行，供 Launcher 按系统语言选择展示。
  - 区域固定高度，内容滚动。
- 底部：活动日志，显示检查、下载、更新、失败原因。
- 设置页：开机启动、LifeBook 项目目录、自动检测更新 Launcher、自动检测更新 OpenCode，并提供 Launcher 手动检查/下载/安装入口。
- LifeBook 准备/同步进度使用悬浮进度框展示，不挤压卡片布局。GitHub archive ZIP 下载能解析到字节进度时显示 KB、百分比和速度；解析不到时显示阶段进度。用户可以停止/取消，失败后可在同一悬浮框重试或关闭。

## LifeBook 更新规则

Launcher 默认管理一个 LifeBook 项目目录。Windows 默认目录是 `D:\LifeBook`；其他系统默认在用户主目录下的 `LifeBook`。用户也可以在设置页选择已有 LifeBook 项目目录或空目录。

1. 若项目目录不存在或为空，Launcher 只能使用 GitHub archive ZIP 准备 LifeBook 项目；普通用户不需要预装 Git，也不会因为本机安装了 Git 而改用 `git clone`。
2. 若项目目录已存在，必须包含 `AGENTS.md`、`template/epub_pipeline/` 和 `books/`，否则提示用户重新选择空目录或有效项目目录。
3. 自动更新 LifeBook 内容时只允许 archive 模式：重新下载 GitHub archive，并只覆盖 manifest 记录且未被用户本地修改的托管文件；发现本地改动、同名非托管文件，或旧版 Git 托管目录没有 archive manifest 时停止，避免覆盖用户内容。
4. 若工作区有本地改动，停止更新并提示用户先提交或备份。
5. 不做会覆盖用户文件的 reset、checkout 或强制 pull。
6. 首页默认显示 Launcher 可取得的全部历史 LifeBook commit。更新内容区域固定高度，窗口尺寸不变，列表通过右侧滚动条滚动查看；如提供折叠按钮，只能作为用户主动切换到“只看最新”的辅助操作，不能作为默认状态。
7. 更新内容依赖 GitHub commit 信息。推送前必须运行 `python tools/git/check_commit_messages.py --range origin/main..HEAD` 或当前分支对应 range，确认每个待推送 commit 都有标题和 `ZH:`、`EN:`、`JA:` 三段详细摘要；`ZH:`、`EN:`、`JA:` 必须各自独占一行，摘要从下一行开始。
8. LifeBook 项目准备和同步必须通过 Tauri event 向前端发送进度，前端以悬浮进度框显示状态、停止/取消、失败重试和关闭操作。

项目目录异常时遵循成熟桌面软件的工作区规则：

- 已配置目录被删除：保留用户设置，标记为 `missing`，不读取其他仓库；界面只提供重新准备项目或更改目录。
- 已配置目录为空：标记为 `empty`，允许在用户确认后下载 LifeBook。
- 已配置目录非空但不是 LifeBook：标记为 `occupied`，不覆盖、不清空、不合并；界面提示选择空目录或已有 LifeBook 项目，并允许打开该目录让用户自行整理。
- 教程、commit 更新内容等工作区依赖信息必须在项目不可用时清空，避免显示上一次目录的旧内容。

## 项目目录与环境变量

Launcher GUI 以本地配置文件中的 LifeBook 项目目录为唯一优先来源。跨平台路径解析顺序为：

1. 用户在 Launcher 设置页选择的项目目录。
2. `LIFEBOOK_HOME` 环境变量。
3. 默认目录：Windows 为 `D:\LifeBook`，macOS / Linux 为用户主目录下的 `LifeBook`。

`LIFEBOOK_HOME` 是 LifeBook 项目统一的项目根目录环境变量。Launcher 启动的子进程会注入 `LIFEBOOK_HOME`。项目脚本、公开 prompt 和外部客户端文档都不应写死某台电脑的绝对路径；需要显式项目根目录时，优先读取 `LIFEBOOK_HOME`，否则使用当前工作目录。

## OpenCode 更新规则

Launcher 从 OpenCode 官方 GitHub release 检查 Desktop 包：

- Windows x64：`opencode-desktop-win-x64.exe`
- Windows arm64：`opencode-desktop-win-arm64.exe`
- macOS x64：`opencode-desktop-mac-x64.dmg`
- macOS arm64：`opencode-desktop-mac-arm64.dmg`
- Linux x64：`opencode-desktop-linux-x86_64.AppImage`
- Linux arm64：`opencode-desktop-linux-arm64.AppImage`

下载前必须询问用户。下载中显示进度，并使用 `.part` 临时文件支持中断后自动续传；下载完成后打开官方安装包或 AppImage。安装状态写入用户本地目录，不写入仓库。若用户点击 `启动客户端`，Launcher 会尝试打开常见系统安装位置中的 OpenCode Desktop；找不到时提示先安装或从系统应用菜单启动一次。

## Launcher 自更新规则

Launcher 从本项目 GitHub release 检查自身安装包。发现新版时先询问用户；确认后显示下载进度，使用 `.part` 临时文件尽量续传，下载完成后自动运行安装脚本、关闭当前窗口、安装新版并重新启动 Launcher。自动检查只负责发现新版和询问，未经用户确认不直接安装。

## 开机启动

使用 Tauri 官方 autostart 插件。

- 默认不强制开启。
- 用户可在设置页打开或关闭。
- 启动后按设置自动准备/更新 LifeBook，并检查 Launcher / OpenCode 更新。

## 技术方案

- 桌面框架：Tauri 2。
- 前端：React + TypeScript + Vite。
- 后端：Rust Tauri commands。
- 自动启动：`tauri-plugin-autostart`。
- 网络下载：Rust `reqwest`，下载进度通过 Tauri event 推送给前端。
- 代理提示：检测常见 `HTTP_PROXY` / `HTTPS_PROXY` / `ALL_PROXY` 环境变量；网络失败时提示检查 VPN 或代理。
- 本地打开安装包/目录：Rust `open`。
- LifeBook 项目更新：首次准备和后续同步都只使用 GitHub archive ZIP，以适配没有 Git 的普通用户；旧版 Git 托管目录不会继续调用本机 `git`，需要用户选择新的空目录后重新用 archive 准备。archive 模式会记录托管文件 hash manifest，用于后续更新时判断是否可以安全覆盖。Windows release 构建和子进程使用无控制台方式启动，避免普通用户看到命令行窗口。

## 目录结构

普通用户入口保持在一个清爽目录内：

```text
tools/lifebook-launcher/
  LifeBook Launcher Setup.exe
  source/
```

`LifeBook Launcher Setup.exe` 是 Windows 用户可双击的安装入口。`source/` 才是 Tauri + React 开发工程，普通用户不需要进入。
