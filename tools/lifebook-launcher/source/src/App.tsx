import { useCallback, useEffect, useMemo, useRef, useState, type MouseEvent } from "react";
import { getCurrentWindow } from "@tauri-apps/api/window";
import { disable, enable, isEnabled } from "@tauri-apps/plugin-autostart";
import {
  Apple,
  ArrowLeft,
  BookOpen,
  CalendarDays,
  CheckCircle2,
  ChevronDown,
  Clock3,
  Code2,
  Download,
  FileText,
  FolderOpen,
  Globe2,
  Home,
  MoreHorizontal,
  Play,
  Power,
  RefreshCcw,
  Settings,
  Square,
  X,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import {
  autoDetectProxySettings,
  cancelLifeBookUpdate,
  cancelNodeModulesInstall,
  cancelOpenCodeDownload,
  chooseRepoFolder,
  checkLauncherUpdates,
  checkOpenCodeLocalStatus,
  checkOpenCodeUpdates,
  closeMainWindowToTray,
  downloadAndInstallLauncherUpdate,
  downloadAndOpenOpenCode,
  exportLauncherLogs,
  getDiagnosticLogSettings,
  getLauncherState,
  getNodeModulesStatus,
  getProxySettings,
  getRuntimeStatus,
  launchOpenCodeClient,
  listenLauncherDownloadProgress,
  listenLifeBookProgress,
  listenNodeModulesProgress,
  listenOpenCodeDownloadProgress,
  listenRuntimeProgress,
  minimizeMainWindow,
  openBooksFolder,
  openRepoFolder,
  prepareLifeBookProject,
  readProjectDocument,
  readProjectDocumentPath,
  recordFrontendActivity,
  setRepoFolder,
  setSaveLogsEnabled,
  setAutoInstallNodeModules,
  saveProxySettings,
  syncLifeBookProject,
  startNodeModulesInstall,
  startRuntimePrepare,
  testProxySettings,
  toggleMainWindowMaximized,
} from "./api";
import {
  ActivityItem,
  CommitInfo,
  DiagnosticLogSettings,
  LauncherSettings,
  LauncherState,
  LauncherUpdateInfo,
  LifeBookUpdateInfo,
  NetworkProxySettings,
  NodeModulesStatus,
  OpenCodeLocalStatus,
  OpenCodeUpdateInfo,
  DownloadProgress,
  ProjectDocument,
  ProxyTestResult,
  RuntimeStatus,
  RuntimeToolStatus,
} from "./types";
import launcherIconUrl from "../assets/lifebook-launcher-icon.png";
import launcherVersionManifest from "../launcher-version.json";

const SETTINGS_KEY = "lifebook-launcher-settings";
const LAUNCHER_VERSION = `v${launcherVersionManifest.version}`;
const LAUNCHER_UPDATE_PROMPT_TIMEOUT_MS = 60_000;

type Locale = "zh-CN" | "zh-TW" | "ja" | "en";
type TabId = "overview" | "updates" | "tutorial" | "settings" | "logs";
type TutorialKind = "readme" | "howto";
type TutorialHistoryEntry = { kind: TutorialKind; document: ProjectDocument };
type ToastTone = "info" | "success" | "warning" | "error";
type FloatingToast = { id: number; message: string; tone: ToastTone };
type DownloadHudState = "idle" | "downloading" | "cancelling" | "stopped" | "failed";
type RuntimeBootstrapState = "checking" | "preparing" | "ready" | "failed";
type ConfirmDialogState = {
  title: string;
  message: string;
  confirmLabel: string;
  cancelLabel: string;
  resolve: (value: boolean) => void;
};

const defaultSettings: LauncherSettings = {
  autoStart: false,
  checkLauncherOnLaunch: true,
  checkOpenCodeOnLaunch: false,
  saveLogsToLocal: true,
};

function runtimeToolStatusLog(tool: RuntimeToolStatus) {
  return `ready=${tool.ready} privateReady=${tool.privateReady} source=${tool.source ?? "-"} path=${tool.path ?? "-"} version=${tool.version || "-"}`;
}

function runtimeStatusLogKey(status: RuntimeStatus) {
  return [
    status.ready,
    status.privateReady,
    status.running,
    status.runtimeRoot,
    status.python.ready,
    status.python.privateReady,
    status.python.source ?? "",
    status.python.path ?? "",
    status.java.ready,
    status.java.privateReady,
    status.java.source ?? "",
    status.java.path ?? "",
  ].join("|");
}

function runtimeStatusLogMessage(status: RuntimeStatus) {
  return `runtime status ready=${status.ready} privateReady=${status.privateReady} running=${status.running} root=${status.runtimeRoot} python=[${runtimeToolStatusLog(status.python)}] java=[${runtimeToolStatusLog(status.java)}]`;
}

const zhCN = {
  knowledge: "知识 · 开放 · 共享",
  mission: "跨平台 · 开源 · 公共领域",
  projectStatus: "项目状态",
  running: "运行正常",
  networkProxy: "网络/代理",
  direct: "直连",
  proxied: "代理",
  proxySettingsTitle: "代理设置",
  proxySettingsDescription: "用于 LifeBook/GitHub 更新、Launcher 下载和 EPUB 工具依赖安装。常见本机代理端口：V2rayN HTTP 10809、SOCKS 10808；Clash HTTP 7890。",
  proxyEnable: "启用代理",
  proxyProtocol: "协议",
  proxyHost: "IP/主机",
  proxyPort: "端口",
  proxyTest: "测试连接",
  proxyAutoDetect: "自动识别",
  proxySave: "保存代理",
  proxyTesting: "正在测试代理...",
  proxyAutoDetecting: "正在识别代理...",
  proxyUntested: "未测试",
  proxyDisabledStatus: "代理已关闭",
  proxyPendingTest: "待测试",
  proxySettingsSaved: "代理设置已保存",
  proxySettingsAutoSaved: "代理设置已自动保存",
  proxyAutoDetected: "识别成功，请点击“测试连接”",
  proxyAutoDetectNotFound: "未识别到本机代理配置，可手动填写后测试。",
  proxySettingsFailed: (error: string) => `代理设置保存失败：${error}`,
  proxyTestSucceeded: (ms: number, version: string) => `代理可连接 GitHub：${ms} ms，${version}`,
  proxyTestFailed: (error: string) => `代理测试失败：${error}`,
  proxyTestAndApplied: (ms: number, version: string) => `已测试并应用代理：${ms} ms，${version}`,
  startup: "开机自启",
  enabled: "已启用",
  disabled: "未启用",
  quickActions: "快捷操作",
  selectRepo: "选择仓库",
  openBooks: "打开成书目录",
  repoRequired: "需选择仓库",
  repoMissing: "项目缺失",
  repoEmpty: "待准备",
  repoInvalid: "目录不可用",
  prepareProject: "重新准备项目",
  workspaceUnavailableTitle: "LifeBook 项目目录不可用",
  workspaceMissingDescription: (path: string) => `已设置的项目目录不存在：${path}`,
  workspaceEmptyDescription: (path: string) => `已设置的项目目录为空，尚未下载 LifeBook：${path}`,
  workspaceOccupiedDescription: (path: string) => `已设置的项目目录已有文件，但不是 LifeBook 项目：${path}`,
  workspaceMissingHelp: "Launcher 会保留这个目录设置，但不会读取其他仓库。请重新准备 LifeBook，或更改为已有 LifeBook 项目/空目录。",
  workspaceEmptyHelp: "点击“重新准备项目”会在该空目录下载 LifeBook；也可以更改为已有 LifeBook 项目或其他空目录。",
  workspaceOccupiedHelp: "为避免覆盖用户文件，Launcher 不会在此目录自动下载。请选择空目录、已有 LifeBook 项目，或先自行整理该目录。",
  noCommitsUnavailable: "LifeBook 项目尚未准备完成。恢复项目后这里会显示更新内容。",
  tutorialUnavailable: "LifeBook 项目尚未准备完成。恢复项目后才能读取 README 和 How to use。",
  preparing: "准备中",
  projectReady: "项目已就绪",
  projectPath: "项目目录",
  overview: "总览",
  updates: "更新",
  tutorial: "教程",
  settings: "设置",
  logs: "日志",
  lifeBookTitle: "LifeBook 项目",
  lifeBookSubtitle: "公共领域书籍翻译与协作系统",
  openCodeTitle: "OpenCode 客户端",
  openCodeSubtitle: "开源Agent GUI客户端",
  currentVersion: "当前版本",
  latestVersion: "最新版本",
  updateStatus: "更新状态",
  latestUpdate: "最新更新",
  upToDate: "已是最新",
  updateAvailable: "可更新",
  checking: "检查中...",
  checkUpdates: "检查更新",
  updateNow: "立即更新",
  installClient: "安装客户端",
  viewProject: "查看项目",
  launchClient: "启动客户端",
  clientNotInstalled: "未安装客户端",
  installed: "已安装",
  notInstalled: "未安装",
  updateContent: "本次 LifeBook 更新内容",
  updateTo: "更新至",
  viewAllUpdates: "查看所有更新",
  showLatestOnly: "只看最新",
  date: "日期",
  commit: "提交",
  title: "标题",
  summary: "摘要",
  noCommits: "暂无待展示的 commit。检查到远端更新后，这里会显示可滚动的更新内容。",
  recentActivity: "最近活动",
  viewFullLog: "查看完整日志",
  info: "INFO",
  downloading: "正在下载",
  working: "处理中...",
  openCodeInstallerOpened: "OpenCode Desktop 安装包已打开，请按安装窗口提示继续。",
  confirmOpenCodeUpdate: "将下载并打开 OpenCode Desktop 官方安装包。是否继续？",
  confirmOpenCodeInstall: (version: string) => `未检测到 OpenCode Desktop。将下载并打开官方安装包 ${version}。是否继续？`,
  confirmOpenCodeUseDownloaded: (version: string) => `OpenCode Desktop ${version} 安装包已下载。是否直接打开安装包？`,
  openCodeAlreadyLatestToast: "已安装最新版本",
  openCodeInstallHintToast: "请点击检查更新进行安装",
  openCodeAlreadyStartedToast: "已启动",
  openCodeCheckToast: "正在检查 OpenCode 客户端...",
  openCodeDownloadTitle: "OpenCode 安装包下载",
  openCodeDownloadStopped: "下载已停止，可重试。",
  openCodeDownloadFailed: "下载失败，可重试。",
  openCodeUpdateSkipped: "已取消 OpenCode 安装。",
  stopDownload: "停止",
  cancelDownload: "取消",
  retry: "重试",
  close: "关闭",
  yes: "是",
  no: "否",
  refreshAllStarted: "正在刷新 LifeBook 与 OpenCode 状态",
  refreshLifeBookStep: "正在更新 LifeBook 项目...",
  refreshOpenCodeStep: "正在检测 OpenCode 客户端...",
  refreshAllDone: "LifeBook 与 OpenCode 状态已刷新完成",
  updateLifeBookProject: "更新 LifeBook",
  lifeBookUpdateStarted: "正在后台更新 LifeBook 项目...",
  lifeBookUpdateComplete: "LifeBook 项目已更新完成",
  lifeBookProgressTitle: "LifeBook 项目准备与同步",
  lifeBookProgressDefault: "正在处理 LifeBook...",
  lifeBookDownloadStopped: "LifeBook 准备/同步已停止，可重试。",
  lifeBookDownloadFailed: "LifeBook 准备/同步失败，可重试。",
  nodeModulesTitle: "EPUB 构建依赖",
  nodeModulesAutoInstallTitle: "后台自动安装 node_modules",
  nodeModulesAutoInstallDescription: "LifeBook 项目准备好后，在后台安装 books/node_modules。不会阻塞 Launcher 操作，失败后可重试或让 AI 后续补装。",
  nodeModulesReady: "依赖已准备完成",
  nodeModulesMissing: "依赖尚未安装",
  nodeModulesIncomplete: "node_modules 未安装完整，可重试",
  nodeModulesNotReady: "项目准备完成后会自动安装",
  nodeModulesDisabled: "已关闭",
  nodeModulesRetryHint: "失败，可重新勾选或重启后重试",
  nodeModulesInstalling: "正在后台安装 node_modules",
  nodeModulesInstallStarted: "正在后台安装 EPUB 构建依赖，不影响继续使用 Launcher。",
  nodeModulesInstallStopped: "node_modules 安装已停止，可重试。",
  nodeModulesInstallFailed: (error: string) => `node_modules 安装失败：${error}。后续可让 AI 补充安装。`,
  nodeModulesStatusFailed: (error: string) => `读取 node_modules 状态失败：${error}`,
  runtimeBootstrapTitle: "正在检查可选运行环境",
  runtimeBootstrapDescription: "Python / Java 只用于编译 EPUB 等辅助功能；即使暂未安装，Launcher 也会继续打开并先准备 LifeBook 项目。",
  runtimeBootstrapChecking: "正在检查 Python / Java 运行环境...",
  runtimeBootstrapPreparing: "正在准备缺失的 Python / Java 运行环境...",
  runtimeBootstrapReady: "Python / Java 运行环境已准备完成",
  runtimeBootstrapFailed: "Python / Java 运行环境准备失败，Launcher 将继续打开，可稍后重试。",
  runtimeBootstrapRetry: "重试",
  runtimeBootstrapContinue: "稍后安装，进入 Launcher",
  runtimeStatusTitle: "Python / Java 运行环境",
  runtimeStatusReady: "构建环境已准备完成",
  runtimeStatusMissing: "EPUB 构建环境未准备，可重试",
  runtimeStatusDescription: "用于 EPUB 构建脚本。Launcher 优先使用本机已有环境；缺少时才准备 LifeBook 私有运行时。",
  runtimeStatusLoadFailed: (error: string) => `读取 Python / Java 运行环境状态失败：${error}`,
  runtimePrepareStarted: "正在准备 Python / Java 运行环境...",
  runtimePrepareFailed: (error: string) => `Python / Java 运行环境准备失败：${error}`,
  clientLaunching: "正在启动",
  clientLaunchSucceeded: "启动成功",
  tutorialTitle: "教程",
  tutorialReadme: "README",
  tutorialHowTo: "How to use",
  tutorialBack: "返回",
  tutorialCurrentDocument: "当前文档",
  tutorialLoading: "正在加载教程...",
  tutorialLoadFailed: (error: string) => `教程加载失败：${error}`,
  copyCode: "复制",
  codeCopied: "已复制",
  codeCopyFailed: "复制失败",
  autoStartEnabled: "已开启开机自动启动 LifeBook Launcher。",
  autoStartDisabled: "已关闭开机自动启动。",
  autoStartFailed: (error: string) => `开机启动设置失败：${error}`,
  welcome: "应用启动完成",
  checkingLifeBook: "检查 LifeBook 更新...",
  preparingLifeBook: "正在准备并更新 LifeBook 项目...",
  lifeBookReady: "LifeBook 项目已准备完成，并已更新到最新版本",
  checkingLauncher: "检查 LifeBook Launcher 更新...",
  checkingOpenCode: "检查 OpenCode 客户端更新...",
  lifeBookLatest: "LifeBook 项目已是最新版本",
  launcherLatest: "LifeBook Launcher 已是最新版本",
  openCodeLatest: "OpenCode 客户端已是最新版本",
  lifeBookFound: (count: number) => `发现 ${count} 个 LifeBook 更新`,
  launcherFound: (version: string) => `发现 LifeBook Launcher ${version}`,
  openCodeFound: (version: string) => `发现 OpenCode Desktop ${version}`,
  lifeBookCheckFailed: (error: string) => `LifeBook 更新检查失败：${error}`,
  launcherCheckFailed: (error: string) => `LifeBook Launcher 检查失败：${error}`,
  openCodeCheckFailed: (error: string) => `OpenCode 检查失败：${error}`,
  lifeBookUpdateStopped: (error: string) => `LifeBook 更新已停止：${error}`,
  launcherUpdateFailed: (error: string) => `LifeBook Launcher 自动更新失败：${error}`,
  openCodeUpdateFailed: (error: string) => `OpenCode 更新失败：${error}`,
  clientLaunchFailed: (error: string) => `OpenCode 启动失败：${error}`,
  launcherUpdateStarted: "LifeBook Launcher 更新已下载，正在自动安装并重启。",
  confirmLauncherUpdate: (version: string) => `将自动下载并安装 LifeBook Launcher ${version}。安装时当前窗口会关闭，完成后会自动重新打开。是否继续？`,
  launcherUpdatePromptTitle: (version: string) => `发现 Launcher ${version}`,
  launcherUpdatePromptFallback: "本次版本修复说明暂时不可用，可先安装以获取最新修复。",
  launcherUpdatePromptUpdate: "更新",
  launcherUpdatePromptSkip: "跳过",
  openCodeMissing: "未检测到 OpenCode Desktop，请先安装客户端。",
  minimizeWindow: "最小化窗口",
  maximizeWindow: "最大化窗口",
  restoreWindow: "还原窗口",
  closeToTray: "关闭窗口并驻留托盘",
  settingsTitle: "设置",
  autoStartTitle: "开机自动启动 LifeBook Launcher",
  autoStartDescription: "电脑启动后自动打开 Launcher，并按下方设置检查更新。",
  checkLauncherTitle: "自动检测更新 Launcher",
  checkLauncherDescription: "启动后自动检测新版；发现更新只提示，不会未经确认自动安装。",
  changeProjectPath: "更改目录",
  confirmProjectDirectoryTitle: "确认 LifeBook 项目目录",
  confirmProjectDirectoryDownload: (path: string) => `将在此目录准备 LifeBook 项目：\n${path}\n\n如果目录为空，会重新下载 LifeBook。非空且不是 LifeBook 项目的目录会被拒绝。是否继续？`,
  confirmProjectDirectoryUse: (path: string) => `将切换到此 LifeBook 项目目录：\n${path}\n\n切换后会检查并更新项目。是否继续？`,
  projectDirectoryChangeCancelled: "已取消更改 LifeBook 项目目录。",
  checkOpenCodeTitle: "自动检测更新 OpenCode",
  checkOpenCodeDescription: "只检查版本，不会自动下载 OpenCode。",
  saveLogsTitle: "保存 LOG 到本地",
  saveLogsDescription: (size: string) => `默认保存错误、关键操作、Git 输出和环境上下文；日志按容量循环保留，最多约 ${size}。`,
  exportLogs: "导出 LOG",
  exportLogsDescription: "导出最近日志和诊断上下文，便于定位用户机器上的问题。",
  exportingLogs: "正在导出 LOG...",
  logSettingsLoadFailed: (error: string) => `读取 LOG 设置失败：${error}`,
  logSettingsSaved: "LOG 保存设置已更新",
  logSettingsSaveFailed: (error: string) => `更新 LOG 设置失败：${error}`,
  logExportFailed: (error: string) => `导出 LOG 失败：${error}`,
};

type Copy = typeof zhCN;

const zhTW: Copy = {
  ...zhCN,
  knowledge: "知識 · 開放 · 共享",
  projectStatus: "專案狀態",
  networkProxy: "網路/代理",
  direct: "直連",
  proxySettingsTitle: "代理設定",
  proxySettingsDescription: "用於 LifeBook/GitHub 更新、Launcher 下載和 EPUB 工具依賴安裝。常見本機代理埠：V2rayN HTTP 10809、SOCKS 10808；Clash HTTP 7890。",
  proxyEnable: "啟用代理",
  proxyProtocol: "協議",
  proxyHost: "IP/主機",
  proxyPort: "埠",
  proxyTest: "測試連線",
  proxyAutoDetect: "自動識別",
  proxySave: "保存代理",
  proxyTesting: "正在測試代理...",
  proxyAutoDetecting: "正在識別代理...",
  proxyUntested: "未測試",
  proxyDisabledStatus: "代理已關閉",
  proxyPendingTest: "待測試",
  proxySettingsSaved: "代理設定已保存",
  proxySettingsAutoSaved: "代理設定已自動保存",
  proxyAutoDetected: "識別成功，請點擊「測試連線」",
  proxyAutoDetectNotFound: "未識別到本機代理設定，可手動填寫後測試。",
  proxySettingsFailed: (error) => `代理設定保存失敗：${error}`,
  proxyTestSucceeded: (ms, version) => `代理可連接 GitHub：${ms} ms，${version}`,
  proxyTestFailed: (error) => `代理測試失敗：${error}`,
  proxyTestAndApplied: (ms, version) => `已測試並套用代理：${ms} ms，${version}`,
  startup: "開機自啟",
  quickActions: "快捷操作",
  selectRepo: "選擇倉庫",
  openBooks: "打開成書目錄",
  repoRequired: "需選擇倉庫",
  repoMissing: "專案缺失",
  repoEmpty: "待準備",
  repoInvalid: "目錄不可用",
  prepareProject: "重新準備專案",
  workspaceUnavailableTitle: "LifeBook 專案目錄不可用",
  workspaceMissingDescription: (path) => `已設定的專案目錄不存在：${path}`,
  workspaceEmptyDescription: (path) => `已設定的專案目錄為空，尚未下載 LifeBook：${path}`,
  workspaceOccupiedDescription: (path) => `已設定的專案目錄已有檔案，但不是 LifeBook 專案：${path}`,
  workspaceMissingHelp: "Launcher 會保留此目錄設定，但不會讀取其他倉庫。請重新準備 LifeBook，或改為已有 LifeBook 專案/空目錄。",
  workspaceEmptyHelp: "點擊「重新準備專案」會在該空目錄下載 LifeBook；也可以改為已有 LifeBook 專案或其他空目錄。",
  workspaceOccupiedHelp: "為避免覆蓋使用者檔案，Launcher 不會在此目錄自動下載。請選擇空目錄、已有 LifeBook 專案，或先自行整理該目錄。",
  noCommitsUnavailable: "LifeBook 專案尚未準備完成。恢復專案後，這裡會顯示更新內容。",
  tutorialUnavailable: "LifeBook 專案尚未準備完成。恢復專案後才能讀取 README 和 How to use。",
  preparing: "準備中",
  projectReady: "專案已就緒",
  projectPath: "專案目錄",
  overview: "總覽",
  tutorial: "教程",
  settings: "設定",
  logs: "日誌",
  lifeBookTitle: "LifeBook 專案",
  lifeBookSubtitle: "公共領域書籍翻譯與協作系統",
  openCodeTitle: "OpenCode 用戶端",
  openCodeSubtitle: "開源 Agent GUI 用戶端",
  currentVersion: "目前版本",
  latestVersion: "最新版本",
  updateStatus: "更新狀態",
  latestUpdate: "最新更新",
  upToDate: "已是最新",
  updateAvailable: "可更新",
  checkUpdates: "檢查更新",
  updateNow: "立即更新",
  installClient: "安裝用戶端",
  viewProject: "查看專案",
  launchClient: "啟動用戶端",
  clientNotInstalled: "未安裝用戶端",
  installed: "已安裝",
  notInstalled: "未安裝",
  updateContent: "本次 LifeBook 更新內容",
  viewAllUpdates: "查看所有更新",
  showLatestOnly: "只看最新",
  noCommits: "暫無待展示的 commit。檢查到遠端更新後，這裡會顯示可滾動的更新內容。",
  recentActivity: "最近活動",
  viewFullLog: "查看完整日誌",
  welcome: "應用啟動完成",
  checkingLifeBook: "檢查 LifeBook 更新...",
  preparingLifeBook: "正在準備並更新 LifeBook 專案...",
  lifeBookReady: "LifeBook 專案已準備完成，並已更新到最新版本",
  checkingLauncher: "檢查 LifeBook Launcher 更新...",
  checkingOpenCode: "檢查 OpenCode 用戶端更新...",
  lifeBookLatest: "LifeBook 專案已是最新版本",
  launcherLatest: "LifeBook Launcher 已是最新版本",
  openCodeLatest: "OpenCode 用戶端已是最新版本",
  lifeBookFound: (count) => `發現 ${count} 個 LifeBook 更新`,
  launcherFound: (version) => `發現 LifeBook Launcher ${version}`,
  openCodeFound: (version) => `發現 OpenCode Desktop ${version}`,
  lifeBookCheckFailed: (error) => `LifeBook 更新檢查失敗：${error}`,
  launcherCheckFailed: (error) => `LifeBook Launcher 檢查失敗：${error}`,
  openCodeCheckFailed: (error) => `OpenCode 檢查失敗：${error}`,
  lifeBookUpdateStopped: (error) => `LifeBook 更新已停止：${error}`,
  launcherUpdateFailed: (error) => `LifeBook Launcher 自動更新失敗：${error}`,
  openCodeUpdateFailed: (error) => `OpenCode 更新失敗：${error}`,
  clientLaunchFailed: (error) => `OpenCode 啟動失敗：${error}`,
  confirmOpenCodeInstall: (version) => `未偵測到 OpenCode Desktop。將下載並打開官方安裝包 ${version}。是否繼續？`,
  confirmOpenCodeUseDownloaded: (version) => `OpenCode Desktop ${version} 安裝包已下載。是否直接打開安裝包？`,
  openCodeAlreadyLatestToast: "已安裝最新版本",
  openCodeInstallHintToast: "請點擊檢查更新進行安裝",
  openCodeAlreadyStartedToast: "已啟動",
  openCodeCheckToast: "正在檢查 OpenCode 用戶端...",
  openCodeDownloadTitle: "OpenCode 安裝包下載",
  openCodeDownloadStopped: "下載已停止，可重試。",
  openCodeDownloadFailed: "下載失敗，可重試。",
  openCodeUpdateSkipped: "已取消 OpenCode 安裝。",
  stopDownload: "停止",
  cancelDownload: "取消",
  retry: "重試",
  close: "關閉",
  refreshAllStarted: "正在刷新 LifeBook 與 OpenCode 狀態",
  refreshLifeBookStep: "正在更新 LifeBook 專案...",
  refreshOpenCodeStep: "正在偵測 OpenCode 用戶端...",
  refreshAllDone: "LifeBook 與 OpenCode 狀態已刷新完成",
  updateLifeBookProject: "更新 LifeBook",
  lifeBookUpdateStarted: "正在背景更新 LifeBook 專案...",
  lifeBookUpdateComplete: "LifeBook 專案已更新完成",
  lifeBookProgressTitle: "LifeBook 專案準備與同步",
  lifeBookProgressDefault: "正在處理 LifeBook...",
  lifeBookDownloadStopped: "LifeBook 準備/同步已停止，可重試。",
  lifeBookDownloadFailed: "LifeBook 準備/同步失敗，可重試。",
  nodeModulesTitle: "EPUB 構建依賴",
  nodeModulesAutoInstallTitle: "背景自動安裝 node_modules",
  nodeModulesAutoInstallDescription: "LifeBook 專案準備好後，在背景安裝 books/node_modules。不會阻塞 Launcher 操作，失敗後可重試或讓 AI 後續補裝。",
  nodeModulesReady: "依賴已準備完成",
  nodeModulesMissing: "依賴尚未安裝",
  nodeModulesIncomplete: "node_modules 未安裝完整，可重試",
  nodeModulesNotReady: "專案準備完成後會自動安裝",
  nodeModulesDisabled: "已關閉",
  nodeModulesRetryHint: "失敗，可重新勾選或重啟後重試",
  nodeModulesInstalling: "正在背景安裝 node_modules",
  nodeModulesInstallStarted: "正在背景安裝 EPUB 構建依賴，不影響繼續使用 Launcher。",
  nodeModulesInstallStopped: "node_modules 安裝已停止，可重試。",
  nodeModulesInstallFailed: (error) => `node_modules 安裝失敗：${error}。後續可讓 AI 補充安裝。`,
  nodeModulesStatusFailed: (error) => `讀取 node_modules 狀態失敗：${error}`,
  clientLaunching: "正在啟動",
  clientLaunchSucceeded: "啟動成功",
  tutorialBack: "返回",
  tutorialLoading: "正在載入教程...",
  tutorialLoadFailed: (error) => `教程載入失敗：${error}`,
  copyCode: "複製",
  codeCopied: "已複製",
  codeCopyFailed: "複製失敗",
  launcherUpdateStarted: "LifeBook Launcher 更新已下載，正在自動安裝並重新啟動。",
  confirmLauncherUpdate: (version) => `將自動下載並安裝 LifeBook Launcher ${version}。安裝時目前視窗會關閉，完成後會自動重新打開。是否繼續？`,
  launcherUpdatePromptTitle: (version) => `發現 Launcher ${version}`,
  launcherUpdatePromptFallback: "本次版本修復說明暫時不可用，可先安裝以取得最新修復。",
  launcherUpdatePromptUpdate: "更新",
  launcherUpdatePromptSkip: "跳過",
  openCodeMissing: "未偵測到 OpenCode Desktop，請先安裝用戶端。",
  minimizeWindow: "最小化視窗",
  maximizeWindow: "最大化視窗",
  restoreWindow: "還原視窗",
  closeToTray: "關閉視窗並駐留系統列",
  settingsTitle: "設定",
  autoStartDescription: "電腦啟動後自動打開 Launcher，並按下方設定檢查更新。",
  checkLauncherTitle: "自動偵測更新 Launcher",
  checkLauncherDescription: "啟動後自動偵測新版；發現更新只會提示，不會未經確認自動安裝。",
  changeProjectPath: "更改目錄",
  confirmProjectDirectoryTitle: "確認 LifeBook 專案目錄",
  confirmProjectDirectoryDownload: (path) => `將在此目錄準備 LifeBook 專案：\n${path}\n\n如果目錄為空，會重新下載 LifeBook。非空且不是 LifeBook 專案的目錄會被拒絕。是否繼續？`,
  confirmProjectDirectoryUse: (path) => `將切換到此 LifeBook 專案目錄：\n${path}\n\n切換後會檢查並更新專案。是否繼續？`,
  projectDirectoryChangeCancelled: "已取消更改 LifeBook 專案目錄。",
  checkOpenCodeTitle: "自動偵測更新 OpenCode",
  checkOpenCodeDescription: "只檢查版本，不會自動下載 OpenCode。",
  saveLogsTitle: "保存 LOG 到本機",
  saveLogsDescription: (size) => `預設保存錯誤、關鍵操作、Git 輸出與環境上下文；日誌按容量循環保留，最多約 ${size}。`,
  exportLogs: "匯出 LOG",
  exportLogsDescription: "匯出最近日誌與診斷上下文，方便定位使用者電腦上的問題。",
  exportingLogs: "正在匯出 LOG...",
  logSettingsLoadFailed: (error) => `讀取 LOG 設定失敗：${error}`,
  logSettingsSaved: "LOG 保存設定已更新",
  logSettingsSaveFailed: (error) => `更新 LOG 設定失敗：${error}`,
  logExportFailed: (error) => `匯出 LOG 失敗：${error}`,
};

const ja: Copy = {
  ...zhCN,
  knowledge: "知識 · オープン · 共有",
  projectStatus: "状態",
  running: "正常",
  networkProxy: "ネットワーク/プロキシ",
  direct: "直結",
  proxied: "プロキシ",
  proxySettingsTitle: "プロキシ設定",
  proxySettingsDescription: "LifeBook/GitHub 更新、Launcher ダウンロード、EPUB ツール依存関係のインストールに使います。ローカルプロキシの例：V2rayN HTTP 10809、SOCKS 10808；Clash HTTP 7890。",
  proxyEnable: "プロキシを有効化",
  proxyProtocol: "プロトコル",
  proxyHost: "IP/ホスト",
  proxyPort: "ポート",
  proxyTest: "接続テスト",
  proxyAutoDetect: "自動検出",
  proxySave: "保存",
  proxyTesting: "プロキシをテストしています...",
  proxyAutoDetecting: "プロキシを検出しています...",
  proxyUntested: "未テスト",
  proxyDisabledStatus: "プロキシは無効です",
  proxyPendingTest: "テスト待ち",
  proxySettingsSaved: "プロキシ設定を保存しました",
  proxySettingsAutoSaved: "プロキシ設定を自動保存しました",
  proxyAutoDetected: "検出しました。「接続テスト」をクリックしてください",
  proxyAutoDetectNotFound: "ローカルプロキシ設定は見つかりませんでした。手動で入力してテストできます。",
  proxySettingsFailed: (error) => `プロキシ設定の保存に失敗しました：${error}`,
  proxyTestSucceeded: (ms, version) => `GitHub に接続できました：${ms} ms、${version}`,
  proxyTestFailed: (error) => `プロキシテストに失敗しました：${error}`,
  proxyTestAndApplied: (ms, version) => `テストして適用しました：${ms} ms、${version}`,
  startup: "自動起動",
  enabled: "有効",
  disabled: "無効",
  quickActions: "クイック操作",
  selectRepo: "リポジトリ選択",
  openBooks: "出力フォルダ",
  repoRequired: "選択が必要",
  repoMissing: "プロジェクトなし",
  repoEmpty: "準備待ち",
  repoInvalid: "フォルダ使用不可",
  prepareProject: "プロジェクトを再準備",
  workspaceUnavailableTitle: "LifeBook プロジェクトフォルダを使用できません",
  workspaceMissingDescription: (path) => `設定されたプロジェクトフォルダが存在しません：${path}`,
  workspaceEmptyDescription: (path) => `設定されたプロジェクトフォルダは空で、LifeBook はまだダウンロードされていません：${path}`,
  workspaceOccupiedDescription: (path) => `設定されたフォルダにはファイルがありますが、LifeBook プロジェクトではありません：${path}`,
  workspaceMissingHelp: "Launcher はこの設定を保持しますが、別のリポジトリは読み込みません。LifeBook を再準備するか、既存プロジェクト/空フォルダを選択してください。",
  workspaceEmptyHelp: "「プロジェクトを再準備」を押すと、この空フォルダに LifeBook をダウンロードします。既存プロジェクトや別の空フォルダも選択できます。",
  workspaceOccupiedHelp: "ユーザーファイルを上書きしないため、このフォルダには自動ダウンロードしません。空フォルダ、既存の LifeBook プロジェクト、または整理済みフォルダを選択してください。",
  noCommitsUnavailable: "LifeBook プロジェクトの準備が完了していません。復旧後に更新内容が表示されます。",
  tutorialUnavailable: "LifeBook プロジェクトの準備が完了していません。復旧後に README と How to use を表示できます。",
  preparing: "準備中",
  projectReady: "準備完了",
  projectPath: "プロジェクトフォルダ",
  overview: "概要",
  updates: "更新",
  tutorial: "ガイド",
  settings: "設定",
  logs: "ログ",
  lifeBookTitle: "LifeBook プロジェクト",
  lifeBookSubtitle: "公共領域書籍の翻訳と協作システム",
  openCodeTitle: "OpenCode クライアント",
  openCodeSubtitle: "オープンソース Agent GUI クライアント",
  currentVersion: "現在",
  latestVersion: "最新",
  updateStatus: "更新状態",
  latestUpdate: "最終更新",
  upToDate: "最新",
  updateAvailable: "更新あり",
  checking: "確認中...",
  checkUpdates: "更新確認",
  updateNow: "今すぐ更新",
  installClient: "クライアントをインストール",
  viewProject: "プロジェクト",
  launchClient: "クライアント起動",
  clientNotInstalled: "未インストール",
  installed: "インストール済み",
  notInstalled: "未インストール",
  updateContent: "今回の LifeBook 更新内容",
  updateTo: "更新先",
  viewAllUpdates: "すべて表示",
  showLatestOnly: "最新のみ",
  date: "日付",
  commit: "commit",
  title: "タイトル",
  summary: "概要",
  noCommits: "表示できる commit はありません。更新がある場合ここに表示されます。",
  recentActivity: "最近の活動",
  viewFullLog: "完全ログ",
  welcome: "アプリ起動完了",
  checkingLifeBook: "LifeBook 更新を確認...",
  preparingLifeBook: "LifeBook プロジェクトを準備して更新しています...",
  lifeBookReady: "LifeBook プロジェクトの準備と更新が完了しました",
  checkingLauncher: "LifeBook Launcher 更新を確認...",
  checkingOpenCode: "OpenCode 更新を確認...",
  lifeBookLatest: "LifeBook は最新です",
  launcherLatest: "LifeBook Launcher は最新です",
  openCodeLatest: "OpenCode は最新です",
  lifeBookFound: (count) => `LifeBook の更新が ${count} 件あります`,
  launcherFound: (version) => `LifeBook Launcher ${version} が見つかりました`,
  openCodeFound: (version) => `OpenCode Desktop ${version} が見つかりました`,
  lifeBookCheckFailed: (error) => `LifeBook 更新確認に失敗：${error}`,
  launcherCheckFailed: (error) => `LifeBook Launcher 確認に失敗：${error}`,
  openCodeCheckFailed: (error) => `OpenCode 確認に失敗：${error}`,
  lifeBookUpdateStopped: (error) => `LifeBook 更新停止：${error}`,
  launcherUpdateFailed: (error) => `LifeBook Launcher 自動更新失敗：${error}`,
  openCodeUpdateFailed: (error) => `OpenCode 更新失敗：${error}`,
  clientLaunchFailed: (error) => `OpenCode 起動失敗：${error}`,
  confirmOpenCodeInstall: (version) => `OpenCode Desktop が見つかりません。公式インストーラー ${version} をダウンロードして開きますか？`,
  confirmOpenCodeUseDownloaded: (version) => `OpenCode Desktop ${version} のインストーラーはダウンロード済みです。今開きますか？`,
  openCodeAlreadyLatestToast: "最新バージョンはインストール済みです",
  openCodeInstallHintToast: "更新確認を押してインストールしてください",
  openCodeAlreadyStartedToast: "起動済みです",
  openCodeCheckToast: "OpenCode クライアントを確認しています...",
  openCodeDownloadTitle: "OpenCode インストーラーのダウンロード",
  openCodeDownloadStopped: "ダウンロードを停止しました。再試行できます。",
  openCodeDownloadFailed: "ダウンロードに失敗しました。再試行できます。",
  openCodeUpdateSkipped: "OpenCode のインストールをキャンセルしました。",
  stopDownload: "停止",
  cancelDownload: "キャンセル",
  retry: "再試行",
  close: "閉じる",
  refreshAllStarted: "LifeBook と OpenCode の状態を更新しています",
  refreshLifeBookStep: "LifeBook プロジェクトを更新しています...",
  refreshOpenCodeStep: "OpenCode クライアントを確認しています...",
  refreshAllDone: "LifeBook と OpenCode の状態を更新しました",
  updateLifeBookProject: "LifeBook を更新",
  lifeBookUpdateStarted: "LifeBook プロジェクトをバックグラウンドで更新しています...",
  lifeBookUpdateComplete: "LifeBook プロジェクトを更新しました",
  lifeBookProgressTitle: "LifeBook プロジェクトの準備と同期",
  lifeBookProgressDefault: "LifeBook を処理しています...",
  lifeBookDownloadStopped: "LifeBook の準備/同期を停止しました。再試行できます。",
  lifeBookDownloadFailed: "LifeBook の準備/同期に失敗しました。再試行できます。",
  nodeModulesTitle: "EPUB ビルド依存関係",
  nodeModulesAutoInstallTitle: "node_modules をバックグラウンドで自動インストール",
  nodeModulesAutoInstallDescription: "LifeBook プロジェクトの準備後、books/node_modules をバックグラウンドでインストールします。Launcher 操作はブロックせず、失敗後は再試行または AI に補完を依頼できます。",
  nodeModulesReady: "依存関係は準備済みです",
  nodeModulesMissing: "依存関係は未インストールです",
  nodeModulesIncomplete: "node_modules が未完成です。再試行できます",
  nodeModulesNotReady: "プロジェクト準備後に自動インストールします",
  nodeModulesDisabled: "無効",
  nodeModulesRetryHint: "失敗。再チェックまたは再起動後に再試行します",
  nodeModulesInstalling: "node_modules をバックグラウンドでインストール中",
  nodeModulesInstallStarted: "EPUB ビルド依存関係をバックグラウンドでインストールしています。Launcher は引き続き使えます。",
  nodeModulesInstallStopped: "node_modules インストールを停止しました。再試行できます。",
  nodeModulesInstallFailed: (error) => `node_modules インストールに失敗しました：${error}。後で AI に補完インストールを依頼できます。`,
  nodeModulesStatusFailed: (error) => `node_modules 状態の読み込みに失敗：${error}`,
  clientLaunching: "起動中",
  clientLaunchSucceeded: "起動成功",
  tutorialTitle: "ガイド",
  tutorialBack: "戻る",
  tutorialLoading: "ガイドを読み込み中...",
  tutorialLoadFailed: (error) => `ガイドの読み込みに失敗：${error}`,
  copyCode: "コピー",
  codeCopied: "コピー済み",
  codeCopyFailed: "コピー失敗",
  launcherUpdateStarted: "LifeBook Launcher 更新をダウンロードしました。自動インストールして再起動します。",
  confirmLauncherUpdate: (version) => `LifeBook Launcher ${version} を自動ダウンロードしてインストールします。インストール中は現在のウィンドウを閉じ、完了後に自動で開きます。続行しますか？`,
  launcherUpdatePromptTitle: (version) => `Launcher ${version} is available`,
  launcherUpdatePromptFallback: "Release notes are temporarily unavailable. Install this version to get the latest fixes.",
  launcherUpdatePromptUpdate: "Update",
  launcherUpdatePromptSkip: "Skip",
  openCodeMissing: "OpenCode Desktop が見つかりません。先にクライアントをインストールしてください。",
  minimizeWindow: "最小化",
  maximizeWindow: "最大化",
  restoreWindow: "元に戻す",
  closeToTray: "閉じてトレイに常駐",
  settingsTitle: "設定",
  autoStartTitle: "LifeBook Launcher を自動起動",
  autoStartDescription: "PC 起動時に Launcher を開き、設定に従って更新を確認します。",
  checkLauncherTitle: "Launcher 更新を自動確認",
  checkLauncherDescription: "起動後に新バージョンを確認します。更新があっても確認なしで自動インストールしません。",
  changeProjectPath: "フォルダ変更",
  confirmProjectDirectoryTitle: "LifeBook プロジェクトフォルダの確認",
  confirmProjectDirectoryDownload: (path) => `このフォルダに LifeBook プロジェクトを準備します：\n${path}\n\n空フォルダの場合は LifeBook を再ダウンロードします。空でなく LifeBook プロジェクトでもないフォルダは拒否されます。続行しますか？`,
  confirmProjectDirectoryUse: (path) => `この LifeBook プロジェクトフォルダに切り替えます：\n${path}\n\n切り替え後、プロジェクトを確認して更新します。続行しますか？`,
  projectDirectoryChangeCancelled: "LifeBook プロジェクトフォルダの変更をキャンセルしました。",
  checkOpenCodeTitle: "OpenCode 更新を自動確認",
  checkOpenCodeDescription: "バージョン確認のみで、自動ダウンロードはしません。",
  saveLogsTitle: "LOG をローカルに保存",
  saveLogsDescription: (size) => `エラー、重要操作、Git 出力、環境コンテキストを既定で保存します。容量上限でローテーションし、最大約 ${size} です。`,
  exportLogs: "LOG を書き出す",
  exportLogsDescription: "最近のログと診断コンテキストを書き出し、ユーザー環境の問題調査に使います。",
  exportingLogs: "LOG を書き出しています...",
  logSettingsLoadFailed: (error) => `LOG 設定の読み込みに失敗：${error}`,
  logSettingsSaved: "LOG 保存設定を更新しました",
  logSettingsSaveFailed: (error) => `LOG 設定の更新に失敗：${error}`,
  logExportFailed: (error) => `LOG の書き出しに失敗：${error}`,
};

const en: Copy = {
  ...zhCN,
  knowledge: "Knowledge · Open · Shared",
  mission: "Cross-platform · Open-source · Public domain",
  projectStatus: "Project status",
  running: "Running",
  networkProxy: "Network/proxy",
  direct: "Direct",
  proxied: "Proxy",
  proxySettingsTitle: "Proxy Settings",
  proxySettingsDescription: "Used for LifeBook/GitHub updates, Launcher downloads, and EPUB tool dependency installs. Common local ports: V2rayN HTTP 10809, SOCKS 10808; Clash HTTP 7890.",
  proxyEnable: "Enable proxy",
  proxyProtocol: "Protocol",
  proxyHost: "IP/host",
  proxyPort: "Port",
  proxyTest: "Test",
  proxyAutoDetect: "Auto detect",
  proxySave: "Save proxy",
  proxyTesting: "Testing proxy...",
  proxyAutoDetecting: "Detecting proxy...",
  proxyUntested: "Not tested",
  proxyDisabledStatus: "Proxy off",
  proxyPendingTest: "Needs test",
  proxySettingsSaved: "Proxy settings saved",
  proxySettingsAutoSaved: "Proxy settings saved automatically",
  proxyAutoDetected: "Detected. Click Test to verify the connection",
  proxyAutoDetectNotFound: "No local proxy settings were detected. You can still enter one manually and test it.",
  proxySettingsFailed: (error) => `Failed to save proxy settings: ${error}`,
  proxyTestSucceeded: (ms, version) => `Proxy can reach GitHub: ${ms} ms, ${version}`,
  proxyTestFailed: (error) => `Proxy test failed: ${error}`,
  proxyTestAndApplied: (ms, version) => `Tested and applied proxy: ${ms} ms, ${version}`,
  startup: "Startup",
  enabled: "Enabled",
  disabled: "Disabled",
  quickActions: "Quick actions",
  selectRepo: "Select repo",
  openBooks: "Open books",
  repoRequired: "Repo needed",
  repoMissing: "Project missing",
  repoEmpty: "Ready to prepare",
  repoInvalid: "Folder unavailable",
  prepareProject: "Prepare project",
  workspaceUnavailableTitle: "LifeBook project folder is unavailable",
  workspaceMissingDescription: (path) => `The configured project folder does not exist: ${path}`,
  workspaceEmptyDescription: (path) => `The configured project folder is empty and LifeBook has not been downloaded yet: ${path}`,
  workspaceOccupiedDescription: (path) => `The configured folder contains files, but it is not a LifeBook project: ${path}`,
  workspaceMissingHelp: "Launcher keeps this folder setting, but will not read another repository. Prepare LifeBook again, or choose an existing LifeBook project/empty folder.",
  workspaceEmptyHelp: "Click Prepare project to download LifeBook into this empty folder, or choose an existing LifeBook project/another empty folder.",
  workspaceOccupiedHelp: "To avoid overwriting user files, Launcher will not download into this folder automatically. Choose an empty folder, an existing LifeBook project, or clean the folder yourself.",
  noCommitsUnavailable: "LifeBook is not ready yet. Update details will appear here after the project is restored.",
  tutorialUnavailable: "LifeBook is not ready yet. README and How to use are available after the project is restored.",
  preparing: "Preparing",
  projectReady: "Project ready",
  projectPath: "Project folder",
  overview: "Overview",
  updates: "Updates",
  tutorial: "Guide",
  settings: "Settings",
  logs: "Logs",
  lifeBookTitle: "LifeBook Project",
  lifeBookSubtitle: "Public-domain book translation workflow",
  openCodeTitle: "OpenCode Client",
  openCodeSubtitle: "Open-source Agent GUI client",
  currentVersion: "Current",
  latestVersion: "Latest",
  updateStatus: "Status",
  latestUpdate: "Updated",
  upToDate: "Up to date",
  updateAvailable: "Update available",
  checking: "Checking...",
  checkUpdates: "Check updates",
  updateNow: "Update now",
  installClient: "Install client",
  viewProject: "View project",
  launchClient: "Launch client",
  clientNotInstalled: "Client not installed",
  installed: "Installed",
  notInstalled: "Not installed",
  updateContent: "LifeBook Changes In This Update",
  updateTo: "Update to",
  viewAllUpdates: "View all updates",
  showLatestOnly: "Latest only",
  date: "Date",
  commit: "Commit",
  title: "Title",
  summary: "Summary",
  noCommits: "No commits to show. Remote changes appear here after checking updates.",
  recentActivity: "Recent activity",
  viewFullLog: "View full log",
  downloading: "Downloading",
  working: "Working...",
  openCodeInstallerOpened: "OpenCode Desktop installer opened.",
  confirmOpenCodeUpdate: "Download and open the official OpenCode Desktop installer?",
  confirmOpenCodeInstall: (version) => `OpenCode Desktop was not detected. Download and open the official ${version} installer?`,
  confirmOpenCodeUseDownloaded: (version) => `OpenCode Desktop ${version} installer is already downloaded. Open it now?`,
  openCodeAlreadyLatestToast: "Latest version is already installed",
  openCodeInstallHintToast: "Click Check updates to install",
  openCodeAlreadyStartedToast: "Already running",
  openCodeCheckToast: "Checking OpenCode client...",
  openCodeDownloadTitle: "OpenCode installer download",
  openCodeDownloadStopped: "Download stopped. You can retry.",
  openCodeDownloadFailed: "Download failed. You can retry.",
  openCodeUpdateSkipped: "OpenCode install cancelled.",
  stopDownload: "Stop",
  cancelDownload: "Cancel",
  retry: "Retry",
  close: "Close",
  autoStartEnabled: "LifeBook Launcher will start with the computer.",
  autoStartDisabled: "Startup launch is disabled.",
  autoStartFailed: (error) => `Startup setting failed: ${error}`,
  welcome: "Application started",
  checkingLifeBook: "Checking LifeBook updates...",
  preparingLifeBook: "Preparing and updating the LifeBook project...",
  lifeBookReady: "LifeBook project is ready and up to date",
  checkingLauncher: "Checking LifeBook Launcher updates...",
  checkingOpenCode: "Checking OpenCode client updates...",
  lifeBookLatest: "LifeBook is up to date",
  launcherLatest: "LifeBook Launcher is up to date",
  openCodeLatest: "OpenCode is up to date",
  lifeBookFound: (count) => `Found ${count} LifeBook update(s)`,
  launcherFound: (version) => `Found LifeBook Launcher ${version}`,
  openCodeFound: (version) => `OpenCode Desktop ${version} is available`,
  lifeBookCheckFailed: (error) => `LifeBook check failed: ${error}`,
  launcherCheckFailed: (error) => `LifeBook Launcher check failed: ${error}`,
  openCodeCheckFailed: (error) => `OpenCode check failed: ${error}`,
  lifeBookUpdateStopped: (error) => `LifeBook update stopped: ${error}`,
  launcherUpdateFailed: (error) => `LifeBook Launcher auto-update failed: ${error}`,
  openCodeUpdateFailed: (error) => `OpenCode update failed: ${error}`,
  clientLaunchFailed: (error) => `OpenCode launch failed: ${error}`,
  refreshAllStarted: "Refreshing LifeBook and OpenCode status",
  refreshLifeBookStep: "Updating LifeBook project...",
  refreshOpenCodeStep: "Checking OpenCode client...",
  refreshAllDone: "LifeBook and OpenCode status refreshed",
  updateLifeBookProject: "Update LifeBook",
  lifeBookUpdateStarted: "Updating LifeBook project in the background...",
  lifeBookUpdateComplete: "LifeBook project update finished",
  lifeBookProgressTitle: "LifeBook project prepare and sync",
  lifeBookProgressDefault: "Working on LifeBook...",
  lifeBookDownloadStopped: "LifeBook prepare/sync stopped. You can retry.",
  lifeBookDownloadFailed: "LifeBook prepare/sync failed. You can retry.",
  nodeModulesTitle: "EPUB build dependencies",
  nodeModulesAutoInstallTitle: "Install node_modules in background",
  nodeModulesAutoInstallDescription: "After the LifeBook project is ready, install books/node_modules in the background. Launcher remains usable; failures can be retried or completed later with AI help.",
  nodeModulesReady: "Dependencies are ready",
  nodeModulesMissing: "Dependencies are not installed",
  nodeModulesIncomplete: "node_modules is incomplete; retry is available",
  nodeModulesNotReady: "Will install after the project is ready",
  nodeModulesDisabled: "Off",
  nodeModulesRetryHint: "Failed; re-check or restart to retry",
  nodeModulesInstalling: "Installing node_modules in the background",
  nodeModulesInstallStarted: "Installing EPUB build dependencies in the background. Launcher remains usable.",
  nodeModulesInstallStopped: "node_modules install stopped. You can retry.",
  nodeModulesInstallFailed: (error) => `node_modules install failed: ${error}. AI can help complete the install later.`,
  nodeModulesStatusFailed: (error) => `Failed to read node_modules status: ${error}`,
  runtimeBootstrapTitle: "Checking optional runtimes",
  runtimeBootstrapDescription: "Python / Java are only needed for helper tasks such as EPUB builds. Launcher will continue to open and prepare the LifeBook project even when they are not installed yet.",
  runtimeBootstrapChecking: "Checking Python / Java runtimes...",
  runtimeBootstrapPreparing: "Preparing missing Python / Java runtimes...",
  runtimeBootstrapReady: "Python / Java runtimes are ready",
  runtimeBootstrapFailed: "Python / Java runtime preparation failed. Launcher will continue to open and you can retry later.",
  runtimeBootstrapRetry: "Retry",
  runtimeBootstrapContinue: "Skip for now",
  runtimeStatusTitle: "Python / Java runtime",
  runtimeStatusReady: "Build environment is ready",
  runtimeStatusMissing: "EPUB build environment is not ready; retry is available",
  runtimeStatusDescription: "Used by EPUB build scripts. Launcher uses existing runtimes first and prepares private runtimes only when needed.",
  runtimeStatusLoadFailed: (error) => `Failed to read Python / Java runtime status: ${error}`,
  runtimePrepareStarted: "Preparing Python / Java runtime...",
  runtimePrepareFailed: (error) => `Python / Java runtime preparation failed: ${error}`,
  clientLaunching: "Launching",
  clientLaunchSucceeded: "Launch succeeded",
  tutorialTitle: "Guide",
  tutorialBack: "Back",
  tutorialCurrentDocument: "Current document",
  tutorialLoading: "Loading guide...",
  tutorialLoadFailed: (error) => `Guide failed to load: ${error}`,
  copyCode: "Copy",
  codeCopied: "Copied",
  codeCopyFailed: "Copy failed",
  launcherUpdateStarted: "LifeBook Launcher update downloaded. Installing and restarting automatically.",
  confirmLauncherUpdate: (version) => `Download and install LifeBook Launcher ${version} automatically? The current window will close during install and reopen after it finishes.`,
  launcherUpdatePromptTitle: (version) => `Launcher ${version} is available`,
  launcherUpdatePromptFallback: "Release notes are temporarily unavailable. Install this version to get the latest fixes.",
  launcherUpdatePromptUpdate: "Update",
  launcherUpdatePromptSkip: "Skip",
  openCodeMissing: "OpenCode Desktop was not detected. Install the client first.",
  minimizeWindow: "Minimize window",
  maximizeWindow: "Maximize window",
  restoreWindow: "Restore window",
  closeToTray: "Close window to tray",
  settingsTitle: "Settings",
  autoStartTitle: "Start LifeBook Launcher with the computer",
  autoStartDescription: "Open Launcher after boot and check updates according to the settings below.",
  checkLauncherTitle: "Auto-check Launcher updates",
  checkLauncherDescription: "After launch, check for a new Launcher version. Updates are only reported and are never installed without confirmation.",
  changeProjectPath: "Change folder",
  confirmProjectDirectoryTitle: "Confirm LifeBook project folder",
  confirmProjectDirectoryDownload: (path) => `LifeBook will be prepared in this folder:\n${path}\n\nIf the folder is empty, LifeBook will be downloaded again. A non-empty folder that is not a LifeBook project will be rejected. Continue?`,
  confirmProjectDirectoryUse: (path) => `Switch to this LifeBook project folder:\n${path}\n\nAfter switching, Launcher will check and update the project. Continue?`,
  projectDirectoryChangeCancelled: "LifeBook project folder change cancelled.",
  checkOpenCodeTitle: "Auto-check OpenCode updates",
  checkOpenCodeDescription: "Only checks the version. It will not download automatically.",
  saveLogsTitle: "Save LOG locally",
  saveLogsDescription: (size) => `Save errors, key actions, Git output, and environment context by default. Logs rotate by size and keep about ${size} at most.`,
  exportLogs: "Export LOG",
  exportLogsDescription: "Export recent logs and diagnostic context for debugging user-machine issues.",
  exportingLogs: "Exporting LOG...",
  logSettingsLoadFailed: (error) => `Failed to read LOG settings: ${error}`,
  logSettingsSaved: "LOG save setting updated",
  logSettingsSaveFailed: (error) => `Failed to update LOG setting: ${error}`,
  logExportFailed: (error) => `Failed to export LOG: ${error}`,
};

const copies: Record<Locale, Copy> = { "zh-CN": zhCN, "zh-TW": zhTW, ja, en };

function detectLocale(): Locale {
  const languages = navigator.languages?.length ? navigator.languages : [navigator.language];
  const normalized = languages.map((language) => language.toLowerCase());
  if (normalized.some((language) => language.startsWith("zh-tw") || language.startsWith("zh-hk") || language.startsWith("zh-hant"))) return "zh-TW";
  if (normalized.some((language) => language.startsWith("zh"))) return "zh-CN";
  if (normalized.some((language) => language.startsWith("ja"))) return "ja";
  return "en";
}

function releaseNotesLanguage(locale: Locale) {
  return locale.startsWith("zh") ? "ZH" : "EN";
}

function localizedReleaseNotes(body: string | null | undefined, locale: Locale, fallback: string) {
  const normalized = (body ?? "").replace(/\r\n/g, "\n").trim();
  if (!normalized) return fallback;
  const sections = parseLabeledSections(normalized);
  const preferred = sections.get(releaseNotesLanguage(locale));
  const english = sections.get("EN");
  const fallbackSection = sections.values().next().value;
  return trimReleaseNotes(preferred || english || fallbackSection || normalized || fallback);
}

function parseLabeledSections(body: string) {
  const sections = new Map<string, string>();
  let current: string | null = null;
  const buffer: string[] = [];
  const flush = () => {
    if (!current) return;
    const text = buffer.join("\n").trim();
    if (text) sections.set(current, text);
  };
  for (const line of body.split("\n")) {
    const match = line.trim().match(/^(ZH|EN|JA)\s*:\s*(.*)$/i);
    if (match) {
      flush();
      current = match[1].toUpperCase();
      buffer.length = 0;
      if (match[2]) buffer.push(match[2]);
      continue;
    }
    if (current) buffer.push(line);
  }
  flush();
  return sections;
}

function trimReleaseNotes(value: string) {
  const lines = value
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .slice(0, 5);
  const text = lines.join("\n");
  return text.length > 520 ? `${text.slice(0, 517).trimEnd()}...` : text;
}

function loadSettings(): LauncherSettings {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY);
    return raw ? { ...defaultSettings, ...JSON.parse(raw) } : defaultSettings;
  } catch {
    return defaultSettings;
  }
}

function saveSettings(settings: LauncherSettings) {
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
}

function nowLabel() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

function formatBytes(value: number) {
  if (!value) return "0.0 KB";
  return `${(value / 1024).toFixed(1)} KB`;
}

function clampPercent(value: number) {
  if (!Number.isFinite(value)) return 0;
  return Math.max(0, Math.min(100, value));
}

function formatPercent(value: number) {
  return `${clampPercent(value).toFixed(2)}%`;
}

function progressWidth(value: number) {
  return `${clampPercent(value)}%`;
}

function formatDownloadProgress(copy: Copy, progress?: DownloadProgress | null) {
  if (!progress) return "";
  if (progress.message) {
    if (progress.message.includes("%") || progress.message.includes("KB")) {
      return progress.message;
    }
    return `${progress.message} ${formatPercent(progress.percent)}`;
  }
  if (progress.totalBytes === 100 && progress.downloadedBytes <= 100) {
    return `${copy.working} ${formatPercent(progress.percent)}`;
  }
  if (!progress.totalBytes && !progress.downloadedBytes) {
    return `${copy.downloading} ${formatPercent(progress.percent)}`;
  }
  const total = progress.totalBytes ? ` / ${formatBytes(progress.totalBytes)}` : "";
  return `${copy.downloading} ${formatPercent(progress.percent)} (${formatBytes(progress.downloadedBytes)}${total})`;
}

function sleep(ms: number) {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

function versionFromDate(date?: string) {
  if (!date) return "v2025.05.25";
  return `v${date.slice(0, 10).replaceAll("-", ".")}`;
}

function commitDate(commit?: CommitInfo) {
  return commit?.date?.slice(0, 16).replace("T", " ") || "2025-05-25 10:15";
}

function hasTauriRuntime() {
  return typeof window !== "undefined" && Boolean(window.__TAURI_INTERNALS__);
}

async function windowAction(action: "minimize" | "maximize" | "close") {
  if (!hasTauriRuntime()) return undefined;
  if (action === "minimize") {
    await minimizeMainWindow();
    return undefined;
  }
  if (action === "maximize") {
    return toggleMainWindowMaximized();
  }
  await closeMainWindowToTray();
  return undefined;
}

export default function App() {
  const [locale] = useState<Locale>(detectLocale);
  const copy = copies[locale];
  const [activeTab, setActiveTab] = useState<TabId>("overview");
  const [state, setState] = useState<LauncherState | null>(null);
  const [launcherUpdate, setLauncherUpdate] = useState<LauncherUpdateInfo | null>(null);
  const [launcherUpdatePrompt, setLauncherUpdatePrompt] = useState<LauncherUpdateInfo | null>(null);
  const [lifeBookUpdate, setLifeBookUpdate] = useState<LifeBookUpdateInfo | null>(null);
  const [openCodeUpdate, setOpenCodeUpdate] = useState<OpenCodeUpdateInfo | null>(null);
  const [openCodeLocalStatus, setOpenCodeLocalStatus] = useState<OpenCodeLocalStatus | null>(null);
  const [tutorialKind, setTutorialKind] = useState<TutorialKind>("howto");
  const [tutorialDoc, setTutorialDoc] = useState<ProjectDocument | null>(null);
  const [tutorialHistory, setTutorialHistory] = useState<TutorialHistoryEntry[]>([]);
  const [tutorialLoading, setTutorialLoading] = useState(false);
  const [settings, setSettings] = useState<LauncherSettings>(loadSettings);
  const [diagnosticLogSettings, setDiagnosticLogSettings] = useState<DiagnosticLogSettings | null>(null);
  const [proxySettings, setProxySettings] = useState<NetworkProxySettings>({
    enabled: false,
    scheme: "http",
    host: "127.0.0.1",
    port: 7890,
  });
  const [proxyTestResult, setProxyTestResult] = useState<ProxyTestResult | null>(null);
  const [proxyBusy, setProxyBusy] = useState<"test" | "detect" | null>(null);
  const [runtimeStatus, setRuntimeStatus] = useState<RuntimeStatus | null>(null);
  const [runtimeProgress, setRuntimeProgress] = useState<DownloadProgress | null>(null);
  const [runtimeBootstrapState, setRuntimeBootstrapState] = useState<RuntimeBootstrapState>("ready");
  const [runtimeBootstrapMessage, setRuntimeBootstrapMessage] = useState<string | null>(null);
  const [runtimeBootstrapBlocking, setRuntimeBootstrapBlocking] = useState(false);
  const [nodeModulesStatus, setNodeModulesStatus] = useState<NodeModulesStatus | null>(null);
  const [nodeModulesProgress, setNodeModulesProgress] = useState<DownloadProgress | null>(null);
  const [nodeModulesDownloadState, setNodeModulesDownloadState] = useState<DownloadHudState>("idle");
  const [nodeModulesDownloadMessage, setNodeModulesDownloadMessage] = useState<string | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [refreshInProgress, setRefreshInProgress] = useState(false);
  const [lifeBookPreparing, setLifeBookPreparing] = useState(false);
  const [lifeBookSyncing, setLifeBookSyncing] = useState(false);
  const [lifeBookProgress, setLifeBookProgress] = useState<DownloadProgress | null>(null);
  const [lifeBookDownloadState, setLifeBookDownloadState] = useState<DownloadHudState>("idle");
  const [lifeBookDownloadMessage, setLifeBookDownloadMessage] = useState<string | null>(null);
  const [lifeBookDownloadDismissed, setLifeBookDownloadDismissed] = useState(false);
  const [lifeBookRetryMode, setLifeBookRetryMode] = useState<"prepare" | "sync">("sync");
  const [openCodeProgress, setOpenCodeProgress] = useState<DownloadProgress | null>(null);
  const [openCodeSyntheticProgress, setOpenCodeSyntheticProgress] = useState<DownloadProgress | null>(null);
  const [openCodeLaunchState, setOpenCodeLaunchState] = useState<"idle" | "starting" | "success">("idle");
  const [openCodeDownloadState, setOpenCodeDownloadState] = useState<DownloadHudState>("idle");
  const [openCodeDownloadMessage, setOpenCodeDownloadMessage] = useState<string | null>(null);
  const [openCodeDownloadDismissed, setOpenCodeDownloadDismissed] = useState(false);
  const [launcherProgress, setLauncherProgress] = useState<DownloadProgress | null>(null);
  const [showAllCommits, setShowAllCommits] = useState(true);
  const [quickActionsOpen, setQuickActionsOpen] = useState(false);
  const [isMaximized, setIsMaximized] = useState(false);
  const [floatingToast, setFloatingToast] = useState<FloatingToast | null>(null);
  const [confirmDialog, setConfirmDialog] = useState<ConfirmDialogState | null>(null);
  const [activities, setActivities] = useState<ActivityItem[]>([
    { id: "welcome", time: nowLabel(), level: "info", message: copy.welcome },
  ]);
  const openCodeDownloadStartedAt = useRef<number | null>(null);
  const openCodeLaunchResetTimer = useRef<number | null>(null);
  const runtimeBootstrapReleaseTimer = useRef<number | null>(null);
  const runtimeBootstrapStartedRef = useRef(false);
  const runtimeStatusLogKeyRef = useRef<string | null>(null);
  const refreshInProgressRef = useRef(false);
  const lifeBookSyncingRef = useRef(false);
  const lifeBookDownloadDismissedRef = useRef(false);
  const nodeModulesAutoStartRef = useRef(false);
  const startupInitializedRef = useRef(false);
  const launcherCheckInProgressRef = useRef(false);
  const launcherUpdateInProgressRef = useRef(false);
  const openCodeCheckInProgressRef = useRef(false);
  const openCodeUpdateInProgressRef = useRef(false);
  const openCodeDownloadDismissedRef = useRef(false);
  const floatingToastTimer = useRef<number | null>(null);
  const launcherUpdatePromptTimer = useRef<number | null>(null);

  const addActivity = useCallback((level: ActivityItem["level"], message: string) => {
    void recordFrontendActivity(level, message).catch(() => undefined);
    setActivities((items) => [
      { id: `${Date.now()}-${Math.random()}`, time: nowLabel(), level, message },
      ...items,
    ].slice(0, 80));
  }, []);

  const logRuntimeStatusIfChanged = useCallback((status: RuntimeStatus) => {
    const key = runtimeStatusLogKey(status);
    if (runtimeStatusLogKeyRef.current === key) return;
    runtimeStatusLogKeyRef.current = key;
    void recordFrontendActivity("info", runtimeStatusLogMessage(status)).catch(() => undefined);
  }, []);

  useEffect(() => {
    const onError = (event: ErrorEvent) => {
      const message = event.error?.stack || event.message || "Unknown frontend error";
      void recordFrontendActivity("error", `frontend error: ${message}`).catch(() => undefined);
    };
    const onUnhandledRejection = (event: PromiseRejectionEvent) => {
      const reason = event.reason instanceof Error ? event.reason.stack || event.reason.message : String(event.reason);
      void recordFrontendActivity("error", `frontend unhandled rejection: ${reason}`).catch(() => undefined);
    };
    window.addEventListener("error", onError);
    window.addEventListener("unhandledrejection", onUnhandledRejection);
    return () => {
      window.removeEventListener("error", onError);
      window.removeEventListener("unhandledrejection", onUnhandledRejection);
    };
  }, []);

  const showFloatingToast = useCallback((message: string, tone: ToastTone = "info") => {
    if (floatingToastTimer.current) {
      window.clearTimeout(floatingToastTimer.current);
    }
    setFloatingToast({ id: Date.now(), message, tone });
    floatingToastTimer.current = window.setTimeout(() => {
      setFloatingToast(null);
      floatingToastTimer.current = null;
    }, 2200);
  }, []);

  const hideLauncherUpdatePrompt = useCallback(() => {
    if (launcherUpdatePromptTimer.current) {
      window.clearTimeout(launcherUpdatePromptTimer.current);
      launcherUpdatePromptTimer.current = null;
    }
    setLauncherUpdatePrompt(null);
  }, []);

  const showLauncherUpdatePrompt = useCallback((info: LauncherUpdateInfo) => {
    if (!info.hasUpdate) return;
    if (launcherUpdatePromptTimer.current) {
      window.clearTimeout(launcherUpdatePromptTimer.current);
    }
    setLauncherUpdatePrompt(info);
    launcherUpdatePromptTimer.current = window.setTimeout(() => {
      setLauncherUpdatePrompt(null);
      launcherUpdatePromptTimer.current = null;
    }, LAUNCHER_UPDATE_PROMPT_TIMEOUT_MS);
  }, []);

  const refreshDiagnosticLogSettings = useCallback(async () => {
    try {
      const info = await getDiagnosticLogSettings();
      setDiagnosticLogSettings(info);
      setSettings((current) => {
        const next = { ...current, saveLogsToLocal: info.saveLogs };
        saveSettings(next);
        return next;
      });
    } catch (error) {
      addActivity("warning", copy.logSettingsLoadFailed(String(error)));
    }
  }, [addActivity, copy]);

  const refreshProxySettings = useCallback(async () => {
    try {
      const proxy = await getProxySettings();
      setProxySettings(proxy);
    } catch (error) {
      addActivity("warning", String(error));
    }
  }, [addActivity]);

  const refreshRuntimeStatus = useCallback(async () => {
    try {
      const status = await getRuntimeStatus();
      setRuntimeStatus(status);
      logRuntimeStatusIfChanged(status);
      return status;
    } catch (error) {
      addActivity("warning", copy.runtimeStatusLoadFailed(String(error)));
      return null;
    }
  }, [addActivity, copy, logRuntimeStatusIfChanged]);

  const startRuntimeBootstrap = useCallback(async (blocking: boolean) => {
    if (runtimeBootstrapReleaseTimer.current) {
      window.clearTimeout(runtimeBootstrapReleaseTimer.current);
      runtimeBootstrapReleaseTimer.current = null;
    }
    setRuntimeBootstrapBlocking(blocking);
    setRuntimeBootstrapState("checking");
    setRuntimeBootstrapMessage(copy.runtimeBootstrapChecking);
    setRuntimeProgress({
      percent: 0.01,
      downloadedBytes: 0,
      totalBytes: 100,
      message: copy.runtimeBootstrapChecking,
      state: "downloading",
    });
    try {
      void recordFrontendActivity("info", `runtime bootstrap start blocking=${blocking}`).catch(() => undefined);
      const status = await getRuntimeStatus();
      setRuntimeStatus(status);
      logRuntimeStatusIfChanged(status);
      if (status.ready) {
        setRuntimeBootstrapState("ready");
        setRuntimeBootstrapMessage(copy.runtimeBootstrapReady);
        setRuntimeProgress({
          percent: 100,
          downloadedBytes: 100,
          totalBytes: 100,
          message: copy.runtimeBootstrapReady,
          state: "success",
        });
        runtimeBootstrapReleaseTimer.current = window.setTimeout(() => {
          setRuntimeBootstrapBlocking(false);
          setRuntimeProgress(null);
          runtimeBootstrapReleaseTimer.current = null;
        }, blocking ? 450 : 800);
        return;
      }
      setRuntimeBootstrapState("preparing");
      setRuntimeBootstrapMessage(copy.runtimeBootstrapPreparing);
      const result = await startRuntimePrepare();
      if (result.requiresDownload === false) {
        const refreshed = await refreshRuntimeStatus();
        setRuntimeBootstrapState("ready");
        setRuntimeBootstrapMessage(refreshed?.ready ? copy.runtimeBootstrapReady : result.message);
        setRuntimeProgress({
          percent: 100,
          downloadedBytes: 100,
          totalBytes: 100,
          message: refreshed?.ready ? copy.runtimeBootstrapReady : result.message,
          state: "success",
        });
        runtimeBootstrapReleaseTimer.current = window.setTimeout(() => {
          setRuntimeBootstrapBlocking(false);
          setRuntimeProgress(null);
          runtimeBootstrapReleaseTimer.current = null;
        }, blocking ? 450 : 800);
        return;
      }
      addActivity("info", copy.runtimePrepareStarted);
    } catch (error) {
      const message = copy.runtimePrepareFailed(String(error));
      setRuntimeBootstrapState("failed");
      setRuntimeBootstrapMessage(message);
      setRuntimeProgress({
        percent: 100,
        downloadedBytes: 0,
        totalBytes: 0,
        message,
        state: "failed",
      });
      addActivity("warning", message);
      if (blocking) {
        runtimeBootstrapReleaseTimer.current = window.setTimeout(() => {
          setRuntimeBootstrapBlocking(false);
          runtimeBootstrapReleaseTimer.current = null;
        }, 1400);
      }
    }
  }, [addActivity, copy, logRuntimeStatusIfChanged, refreshRuntimeStatus]);

  const refreshNodeModulesStatus = useCallback(async () => {
    try {
      const status = await getNodeModulesStatus();
      setNodeModulesStatus(status);
      if (status.ready) {
        setNodeModulesDownloadState("idle");
        setNodeModulesDownloadMessage(null);
        setNodeModulesProgress(null);
      } else if (status.running) {
        setNodeModulesDownloadState("downloading");
      } else {
        setNodeModulesDownloadState((current) => {
          if (current === "downloading" || current === "cancelling") return "failed";
          return current;
        });
        setNodeModulesDownloadMessage((current) => current || (status.repoReady ? copy.nodeModulesIncomplete : null));
      }
    } catch (error) {
      addActivity("warning", copy.nodeModulesStatusFailed(String(error)));
    }
  }, [addActivity, copy]);

  const startLifeBookProgress = useCallback((mode: "prepare" | "sync") => {
    setLifeBookRetryMode(mode);
    setLifeBookDownloadDismissed(false);
    lifeBookDownloadDismissedRef.current = false;
    setLifeBookDownloadState("downloading");
    setLifeBookDownloadMessage(null);
    setLifeBookProgress({
      percent: 0.01,
      downloadedBytes: 0,
      totalBytes: 100,
      message: mode === "prepare" ? copy.preparingLifeBook : copy.lifeBookUpdateStarted,
    });
  }, [copy.lifeBookUpdateStarted, copy.preparingLifeBook]);

  const finishLifeBookProgress = useCallback((message: string) => {
    setLifeBookProgress((current) => ({
      percent: 100,
      downloadedBytes: 100,
      totalBytes: 100,
      message,
    } satisfies DownloadProgress));
    setLifeBookDownloadState("idle");
    window.setTimeout(() => {
      setLifeBookProgress(null);
      setLifeBookDownloadMessage(null);
    }, 900);
  }, []);

  const failLifeBookProgress = useCallback((error: unknown) => {
    const raw = String(error);
    const stopped = raw.includes("已停止") || raw.toLowerCase().includes("stopped");
    const message = stopped ? copy.lifeBookDownloadStopped : copy.lifeBookDownloadFailed;
    setLifeBookDownloadMessage(message);
    setLifeBookDownloadState(stopped ? "stopped" : "failed");
    addActivity(stopped ? "warning" : "error", stopped ? message : copy.lifeBookUpdateStopped(raw));
    if (lifeBookDownloadDismissedRef.current) {
      window.setTimeout(() => setLifeBookDownloadState("idle"), 900);
    } else {
      showFloatingToast(message, stopped ? "warning" : "error");
    }
  }, [addActivity, copy, showFloatingToast]);

  const startNodeModulesInBackground = useCallback(async (silent = false) => {
    if (nodeModulesDownloadState === "downloading" || nodeModulesDownloadState === "cancelling") return;
    setNodeModulesDownloadState("downloading");
    setNodeModulesDownloadMessage(null);
    setNodeModulesProgress({
      percent: 0.01,
      downloadedBytes: 0,
      totalBytes: 100,
      message: copy.nodeModulesInstalling,
      state: "downloading",
    });
    try {
      const result = await startNodeModulesInstall();
      if (!silent) {
        addActivity("info", result.message || copy.nodeModulesInstallStarted);
        showFloatingToast(copy.nodeModulesInstallStarted, "info");
      }
      await refreshNodeModulesStatus();
    } catch (error) {
      const message = copy.nodeModulesInstallFailed(String(error));
      setNodeModulesDownloadMessage(message);
      setNodeModulesDownloadState("failed");
      addActivity("error", message);
      showFloatingToast(message, "error");
    }
  }, [
    addActivity,
    copy,
    nodeModulesDownloadState,
    refreshNodeModulesStatus,
    showFloatingToast,
  ]);

  const stopNodeModulesInstall = useCallback(async (removePartial = false) => {
    setNodeModulesDownloadState("cancelling");
    try {
      await cancelNodeModulesInstall(removePartial);
    } catch (error) {
      const message = copy.nodeModulesInstallFailed(String(error));
      setNodeModulesDownloadMessage(message);
      setNodeModulesDownloadState("failed");
      addActivity("error", message);
      showFloatingToast(message, "error");
    }
  }, [addActivity, copy, showFloatingToast]);

  const retryRuntimePrepare = useCallback(() => {
    runtimeBootstrapStartedRef.current = true;
    void startRuntimeBootstrap(false);
  }, [startRuntimeBootstrap]);

  const continueAfterRuntimeBootstrap = useCallback(() => {
    if (runtimeBootstrapReleaseTimer.current) {
      window.clearTimeout(runtimeBootstrapReleaseTimer.current);
      runtimeBootstrapReleaseTimer.current = null;
    }
    setRuntimeBootstrapBlocking(false);
  }, []);

  const askConfirm = useCallback((options: Omit<ConfirmDialogState, "resolve">) => {
    return new Promise<boolean>((resolve) => {
      setConfirmDialog({ ...options, resolve });
    });
  }, []);

  const resolveConfirmDialog = useCallback((value: boolean) => {
    setConfirmDialog((dialog) => {
      dialog?.resolve(value);
      return null;
    });
  }, []);

  const refreshState = useCallback(async () => {
    try {
      setState(await getLauncherState());
    } catch (error) {
      setState(null);
      addActivity("error", String(error));
    }
  }, [addActivity]);

  const refreshOpenCodeLocalStatus = useCallback(async () => {
    try {
      const status = await checkOpenCodeLocalStatus();
      setOpenCodeLocalStatus(status);
      setState((old) => old ? {
        ...old,
        opencodeInstalledVersion: status.installedVersion ?? old.opencodeInstalledVersion,
        opencodeClientPath: status.clientPath,
        opencodeAvailable: status.clientAvailable,
      } : old);
    } catch (error) {
      addActivity("warning", copy.openCodeCheckFailed(String(error)));
    }
  }, [addActivity, copy]);

  const chooseRepo = useCallback(async () => {
    setBusy("repo-choose");
    try {
      const selected = await chooseRepoFolder();
      addActivity(selected.ok ? "info" : "info", selected.message);
      if (selected.ok && selected.repoRoot) {
        const confirmed = await askConfirm({
          title: copy.confirmProjectDirectoryTitle,
          message: selected.requiresDownload
            ? copy.confirmProjectDirectoryDownload(selected.repoRoot)
            : copy.confirmProjectDirectoryUse(selected.repoRoot),
          confirmLabel: copy.yes,
          cancelLabel: copy.no,
        });
        if (!confirmed) {
          addActivity("info", copy.projectDirectoryChangeCancelled);
          return;
        }
        const result = await setRepoFolder(selected.repoRoot);
        addActivity(result.ok ? "success" : "info", result.message);
        setTutorialDoc(null);
        await refreshState();
        if (lifeBookSyncingRef.current) return;
        lifeBookSyncingRef.current = true;
        setLifeBookPreparing(true);
        startLifeBookProgress("prepare");
        addActivity("info", copy.preparingLifeBook);
        try {
          const info = await prepareLifeBookProject(locale);
          setLifeBookUpdate(info);
          finishLifeBookProgress(copy.lifeBookReady);
          addActivity("success", copy.lifeBookReady);
        } catch (error) {
          failLifeBookProgress(error);
        } finally {
          lifeBookSyncingRef.current = false;
          setLifeBookPreparing(false);
        }
        await refreshState();
        await refreshNodeModulesStatus();
      }
    } catch (error) {
      const message = String(error);
      addActivity("error", message);
      showFloatingToast(message, "error");
    } finally {
      setBusy(null);
    }
  }, [addActivity, askConfirm, copy, failLifeBookProgress, finishLifeBookProgress, locale, refreshNodeModulesStatus, refreshState, showFloatingToast, startLifeBookProgress]);

  const doOpenRepoFolder = useCallback(async () => {
    try {
      const result = await openRepoFolder();
      addActivity(result.ok ? "success" : "warning", result.message);
    } catch (error) {
      addActivity("error", String(error));
    }
  }, [addActivity]);

  const doOpenBooksFolder = useCallback(async () => {
    try {
      const result = await openBooksFolder();
      addActivity(result.ok ? "success" : "warning", result.message);
    } catch (error) {
      addActivity("error", String(error));
    }
  }, [addActivity]);

  const prepareLifeBook = useCallback(async () => {
    if (lifeBookSyncingRef.current) return;
    lifeBookSyncingRef.current = true;
    setLifeBookPreparing(true);
    startLifeBookProgress("prepare");
    addActivity("info", copy.preparingLifeBook);
    try {
      const info = await prepareLifeBookProject(locale);
      setLifeBookUpdate(info);
      finishLifeBookProgress(copy.lifeBookReady);
      addActivity("success", copy.lifeBookReady);
      await refreshState();
      await refreshNodeModulesStatus();
    } catch (error) {
      failLifeBookProgress(error);
      await refreshState();
      await refreshNodeModulesStatus();
    } finally {
      lifeBookSyncingRef.current = false;
      setLifeBookPreparing(false);
    }
  }, [addActivity, copy, failLifeBookProgress, finishLifeBookProgress, locale, refreshNodeModulesStatus, refreshState, startLifeBookProgress]);

  const prepareLifeBookInBackground = useCallback(async () => {
    if (lifeBookSyncingRef.current) return;
    lifeBookSyncingRef.current = true;
    startLifeBookProgress("prepare");
    addActivity("info", copy.preparingLifeBook);
    try {
      const info = await prepareLifeBookProject(locale);
      setLifeBookUpdate(info);
      finishLifeBookProgress(copy.lifeBookReady);
      addActivity("success", copy.lifeBookReady);
      await refreshState();
      await refreshNodeModulesStatus();
    } catch (error) {
      failLifeBookProgress(error);
      await refreshState();
      await refreshNodeModulesStatus();
    } finally {
      lifeBookSyncingRef.current = false;
    }
  }, [addActivity, copy, failLifeBookProgress, finishLifeBookProgress, locale, refreshNodeModulesStatus, refreshState, startLifeBookProgress]);

  const syncLifeBookNow = useCallback(async () => {
    if (lifeBookSyncingRef.current) return;
    lifeBookSyncingRef.current = true;
    setLifeBookSyncing(true);
    startLifeBookProgress("sync");
    addActivity("info", copy.lifeBookUpdateStarted);
    try {
      const info = await syncLifeBookProject(locale);
      setLifeBookUpdate(info);
      const doneMessage = info.hasUpdate ? copy.lifeBookFound(info.behindCount) : copy.lifeBookUpdateComplete;
      finishLifeBookProgress(doneMessage);
      addActivity(info.hasUpdate ? "warning" : "success", doneMessage);
      await refreshState();
      await refreshNodeModulesStatus();
    } catch (error) {
      failLifeBookProgress(error);
      await refreshState();
      await refreshNodeModulesStatus();
    } finally {
      lifeBookSyncingRef.current = false;
      setLifeBookSyncing(false);
    }
  }, [addActivity, copy, failLifeBookProgress, finishLifeBookProgress, locale, refreshNodeModulesStatus, refreshState, startLifeBookProgress]);

  const doUpdateLauncher = useCallback(async (knownUpdate?: LauncherUpdateInfo | null, skipConfirm = false) => {
    if (launcherUpdateInProgressRef.current) return;
    launcherUpdateInProgressRef.current = true;
    const info = knownUpdate ?? launcherUpdate;
    const version = info?.latestVersion ?? "";
    if (!skipConfirm && !window.confirm(copy.confirmLauncherUpdate(version))) {
      launcherUpdateInProgressRef.current = false;
      return;
    }
    hideLauncherUpdatePrompt();
    setBusy("launcher-update");
    const initialBytes = info?.installerDownloaded ? info.assetSize : info?.partialDownloadedBytes ?? 0;
    const initialPercent = info?.assetSize ? Math.round((initialBytes / info.assetSize) * 100) : 0;
    setLauncherProgress({
      percent: Math.max(0, Math.min(100, initialPercent)),
      downloadedBytes: initialBytes,
      totalBytes: info?.assetSize ?? 0,
    });
    try {
      const result = await downloadAndInstallLauncherUpdate();
      addActivity(result.ok ? "success" : "warning", result.message || copy.launcherUpdateStarted);
    } catch (error) {
      addActivity("error", copy.launcherUpdateFailed(String(error)));
    } finally {
      launcherUpdateInProgressRef.current = false;
      setBusy(null);
    }
  }, [addActivity, copy, hideLauncherUpdatePrompt, launcherUpdate]);

  const checkLauncher = useCallback(async (promptWhenUpdate = false, background = false) => {
    if (launcherCheckInProgressRef.current) return;
    launcherCheckInProgressRef.current = true;
    if (!background) setBusy("launcher-check");
    addActivity("info", copy.checkingLauncher);
    try {
      const info = await checkLauncherUpdates();
      setLauncherUpdate(info);
      addActivity(info.hasUpdate ? "warning" : "success", info.hasUpdate ? copy.launcherFound(info.latestVersion) : copy.launcherLatest);
      if (info.hasUpdate) {
        showLauncherUpdatePrompt(info);
      }
    } catch (error) {
      addActivity("error", copy.launcherCheckFailed(String(error)));
    } finally {
      launcherCheckInProgressRef.current = false;
      if (!background) setBusy((value) => (value === "launcher-check" ? null : value));
    }
  }, [addActivity, copy, showLauncherUpdatePrompt]);

  const doUpdateOpenCode = useCallback(async (knownUpdate?: OpenCodeUpdateInfo | null, skipConfirm = false) => {
    if (openCodeUpdateInProgressRef.current) return;
    openCodeUpdateInProgressRef.current = true;
    const info = knownUpdate ?? openCodeUpdate;
    const version = info?.latestVersion ?? "";
    const confirmMessage = info?.installerDownloaded
      ? copy.confirmOpenCodeUseDownloaded(version)
      : info?.clientAvailable
        ? copy.confirmOpenCodeUpdate
        : copy.confirmOpenCodeInstall(version);
    if (!skipConfirm && !window.confirm(confirmMessage)) {
      openCodeUpdateInProgressRef.current = false;
      showFloatingToast(copy.openCodeUpdateSkipped, "info");
      return;
    }
    setBusy("opencode-update");
    setOpenCodeDownloadDismissed(false);
    openCodeDownloadDismissedRef.current = false;
    setOpenCodeDownloadState("downloading");
    setOpenCodeDownloadMessage(null);
    setOpenCodeProgress({ percent: 0, downloadedBytes: info?.partialDownloadedBytes ?? 0, totalBytes: info?.assetSize ?? 0 });
    openCodeDownloadStartedAt.current = Date.now();
    setOpenCodeSyntheticProgress({ percent: 1, downloadedBytes: info?.partialDownloadedBytes ?? 0, totalBytes: info?.assetSize ?? 0 });
    try {
      const result = await downloadAndOpenOpenCode();
      addActivity(result.ok ? "success" : "warning", result.message || copy.openCodeInstallerOpened);
      showFloatingToast(result.message || copy.openCodeInstallerOpened, result.ok ? "success" : "warning");
      setOpenCodeDownloadState("idle");
      window.setTimeout(() => {
        setOpenCodeProgress(null);
        setOpenCodeDownloadMessage(null);
      }, 900);
      await refreshState();
      await refreshOpenCodeLocalStatus();
    } catch (error) {
      const message = String(error);
      const stopped = message.includes("下载已停止") || message.includes("stopped");
      addActivity(stopped ? "warning" : "error", stopped ? copy.openCodeDownloadStopped : copy.openCodeUpdateFailed(message));
      setOpenCodeDownloadMessage(stopped ? copy.openCodeDownloadStopped : copy.openCodeDownloadFailed);
      setOpenCodeDownloadState(stopped ? "stopped" : "failed");
      if (openCodeDownloadDismissedRef.current) {
        window.setTimeout(() => setOpenCodeDownloadState("idle"), 900);
      } else {
        showFloatingToast(stopped ? copy.openCodeDownloadStopped : copy.openCodeDownloadFailed, stopped ? "warning" : "error");
      }
    } finally {
      openCodeDownloadStartedAt.current = null;
      setOpenCodeSyntheticProgress(null);
      openCodeUpdateInProgressRef.current = false;
      setBusy(null);
    }
  }, [addActivity, copy, openCodeUpdate, refreshOpenCodeLocalStatus, refreshState, showFloatingToast]);

  useEffect(() => {
    const unlistenRuntime = listenRuntimeProgress((progress) => {
      setRuntimeProgress(progress);
      setRuntimeBootstrapMessage(progress.message ?? null);
      if (progress.state === "success") {
        setRuntimeBootstrapState("ready");
        void refreshRuntimeStatus();
        if (runtimeBootstrapReleaseTimer.current) window.clearTimeout(runtimeBootstrapReleaseTimer.current);
        runtimeBootstrapReleaseTimer.current = window.setTimeout(() => {
          setRuntimeBootstrapBlocking(false);
          setRuntimeProgress(null);
          runtimeBootstrapReleaseTimer.current = null;
        }, 650);
      } else if (progress.state === "failed") {
        setRuntimeBootstrapState("failed");
        addActivity("warning", progress.message || copy.runtimeBootstrapFailed);
        void refreshRuntimeStatus();
        if (runtimeBootstrapReleaseTimer.current) window.clearTimeout(runtimeBootstrapReleaseTimer.current);
        runtimeBootstrapReleaseTimer.current = window.setTimeout(() => {
          setRuntimeBootstrapBlocking(false);
          runtimeBootstrapReleaseTimer.current = null;
        }, 1400);
      } else if (progress.percent > 0 && progress.percent < 100) {
        setRuntimeBootstrapState("preparing");
      }
    });
    if (!runtimeBootstrapStartedRef.current) {
      runtimeBootstrapStartedRef.current = true;
      void startRuntimeBootstrap(false);
    }
    return () => {
      unlistenRuntime.then((fn) => fn()).catch(() => undefined);
    };
  }, [addActivity, copy, refreshRuntimeStatus, startRuntimeBootstrap]);

  useEffect(() => {
    if (runtimeBootstrapState !== "preparing") return undefined;
    const timer = window.setInterval(async () => {
      const status = await refreshRuntimeStatus();
      if (!status) return;
      if (status.ready) {
        setRuntimeBootstrapState("ready");
        setRuntimeBootstrapMessage(copy.runtimeBootstrapReady);
        setRuntimeProgress({
          percent: 100,
          downloadedBytes: 100,
          totalBytes: 100,
          message: copy.runtimeBootstrapReady,
          state: "success",
        });
        if (runtimeBootstrapReleaseTimer.current) window.clearTimeout(runtimeBootstrapReleaseTimer.current);
        runtimeBootstrapReleaseTimer.current = window.setTimeout(() => {
          setRuntimeBootstrapBlocking(false);
          setRuntimeProgress(null);
          runtimeBootstrapReleaseTimer.current = null;
        }, 450);
      } else if (!status.running) {
        const message = copy.runtimeBootstrapFailed;
        setRuntimeBootstrapState("failed");
        setRuntimeBootstrapMessage(message);
        setRuntimeProgress({
          percent: 100,
          downloadedBytes: 0,
          totalBytes: 0,
          message,
          state: "failed",
        });
        addActivity("warning", message);
        if (runtimeBootstrapReleaseTimer.current) window.clearTimeout(runtimeBootstrapReleaseTimer.current);
        runtimeBootstrapReleaseTimer.current = window.setTimeout(() => {
          setRuntimeBootstrapBlocking(false);
          runtimeBootstrapReleaseTimer.current = null;
        }, 1400);
      }
    }, 1500);
    return () => window.clearInterval(timer);
  }, [addActivity, copy, refreshRuntimeStatus, runtimeBootstrapState]);

  const checkOpenCode = useCallback(async (background = false, installWhenNeeded = false) => {
    if (openCodeCheckInProgressRef.current) return;
    openCodeCheckInProgressRef.current = true;
    if (!background) {
      addActivity("info", copy.checkingOpenCode);
      showFloatingToast(copy.openCodeCheckToast, "info");
    }
    try {
      await refreshOpenCodeLocalStatus();
      const info = await checkOpenCodeUpdates();
      setOpenCodeUpdate(info);
      const needsInstall = !info.clientAvailable;
      const needsUpdate = info.clientAvailable && info.hasUpdate;
      if (background) {
        addActivity(info.hasUpdate ? "warning" : "success", info.hasUpdate ? copy.openCodeFound(info.latestVersion) : copy.openCodeLatest);
      } else if (!needsInstall && !needsUpdate) {
        addActivity("success", copy.openCodeLatest);
        showFloatingToast(copy.openCodeAlreadyLatestToast, "success");
      } else if (installWhenNeeded) {
        const message = info.installerDownloaded
          ? copy.confirmOpenCodeUseDownloaded(info.latestVersion)
          : needsInstall
            ? copy.confirmOpenCodeInstall(info.latestVersion)
            : copy.confirmOpenCodeUpdate;
        if (window.confirm(message)) {
          await doUpdateOpenCode(info, true);
        } else {
          addActivity("info", copy.openCodeUpdateSkipped);
          showFloatingToast(copy.openCodeUpdateSkipped, "info");
        }
      } else {
        addActivity("warning", needsInstall ? copy.openCodeMissing : copy.openCodeFound(info.latestVersion));
        showFloatingToast(needsInstall ? copy.openCodeInstallHintToast : copy.openCodeFound(info.latestVersion), "warning");
      }
    } catch (error) {
      addActivity("error", copy.openCodeCheckFailed(String(error)));
      showFloatingToast(copy.openCodeCheckFailed(String(error)), "error");
    } finally {
      openCodeCheckInProgressRef.current = false;
    }
  }, [addActivity, copy, doUpdateOpenCode, refreshOpenCodeLocalStatus, showFloatingToast]);

  const loadTutorial = useCallback(async (kind: TutorialKind) => {
    setTutorialKind(kind);
    setTutorialHistory([]);
    if (!state?.repoReady) {
      setTutorialDoc(null);
      showFloatingToast(copy.tutorialUnavailable, "warning");
      return;
    }
    setTutorialLoading(true);
    try {
      const doc = await readProjectDocument(kind, locale);
      setTutorialDoc(doc);
    } catch (error) {
      addActivity("error", copy.tutorialLoadFailed(String(error)));
      showFloatingToast(copy.tutorialLoadFailed(String(error)), "error");
    } finally {
      setTutorialLoading(false);
    }
  }, [addActivity, copy, locale, showFloatingToast, state?.repoReady]);

  const openTutorialLink = useCallback(async (href: string) => {
    if (!state?.repoReady) {
      setTutorialDoc(null);
      showFloatingToast(copy.tutorialUnavailable, "warning");
      return;
    }
    setTutorialLoading(true);
    try {
      const doc = await readProjectDocumentPath(href, locale);
      if (tutorialDoc) {
        setTutorialHistory((items) => [...items.slice(-19), { kind: tutorialKind, document: tutorialDoc }]);
      }
      setTutorialKind(doc.kind === "howto" ? "howto" : "readme");
      setTutorialDoc(doc);
    } catch (error) {
      addActivity("error", copy.tutorialLoadFailed(String(error)));
      showFloatingToast(copy.tutorialLoadFailed(String(error)), "error");
    } finally {
      setTutorialLoading(false);
    }
  }, [addActivity, copy, locale, showFloatingToast, state?.repoReady, tutorialDoc, tutorialKind]);

  const goBackTutorial = useCallback(() => {
    setTutorialHistory((items) => {
      const previous = items[items.length - 1];
      if (!previous) return items;
      setTutorialKind(previous.kind);
      setTutorialDoc(previous.document);
      return items.slice(0, -1);
    });
  }, []);

  const refreshAllStatus = useCallback(async () => {
    setActiveTab("updates");
    if (refreshInProgressRef.current) return;
    refreshInProgressRef.current = true;
    setRefreshInProgress(true);
    addActivity("info", copy.refreshAllStarted);
    await sleep(80);
    try {
      await refreshState();
      if (!lifeBookSyncingRef.current) {
        lifeBookSyncingRef.current = true;
        startLifeBookProgress("sync");
        try {
          const info = await syncLifeBookProject(locale);
          setLifeBookUpdate(info);
          const doneMessage = info.hasUpdate ? copy.lifeBookFound(info.behindCount) : copy.lifeBookLatest;
          finishLifeBookProgress(doneMessage);
          addActivity(info.hasUpdate ? "warning" : "success", doneMessage);
        } catch (error) {
          failLifeBookProgress(error);
        } finally {
          lifeBookSyncingRef.current = false;
        }
      }
      await refreshNodeModulesStatus();
      await refreshOpenCodeLocalStatus();
      if (!openCodeCheckInProgressRef.current) {
        openCodeCheckInProgressRef.current = true;
        try {
          const openCodeInfo = await checkOpenCodeUpdates();
          setOpenCodeUpdate(openCodeInfo);
          addActivity(openCodeInfo.hasUpdate ? "warning" : "success", openCodeInfo.hasUpdate ? copy.openCodeFound(openCodeInfo.latestVersion) : copy.openCodeLatest);
        } catch (error) {
          addActivity("warning", copy.openCodeCheckFailed(String(error)));
        } finally {
          openCodeCheckInProgressRef.current = false;
        }
      }
      await refreshState();
      await refreshNodeModulesStatus();
      await refreshOpenCodeLocalStatus();
      addActivity("success", copy.refreshAllDone);
    } catch (error) {
      addActivity("error", copy.lifeBookUpdateStopped(String(error)));
      await refreshState();
      await refreshNodeModulesStatus();
      await refreshOpenCodeLocalStatus();
    } finally {
      refreshInProgressRef.current = false;
      setRefreshInProgress(false);
    }
  }, [addActivity, copy, failLifeBookProgress, finishLifeBookProgress, locale, refreshNodeModulesStatus, refreshOpenCodeLocalStatus, refreshState, showFloatingToast, startLifeBookProgress]);

  const doLaunchOpenCode = useCallback(async () => {
    if (openCodeLaunchState === "starting") return;
    const localStatus = await checkOpenCodeLocalStatus().catch(() => null);
    if (localStatus) {
      setOpenCodeLocalStatus(localStatus);
      setState((old) => old ? {
        ...old,
        opencodeInstalledVersion: localStatus.installedVersion ?? old.opencodeInstalledVersion,
        opencodeClientPath: localStatus.clientPath,
        opencodeAvailable: localStatus.clientAvailable,
      } : old);
    }
    if (!localStatus?.clientAvailable) {
      showFloatingToast(copy.openCodeInstallHintToast, "warning");
      addActivity("warning", copy.openCodeMissing);
      return;
    }
    if (openCodeLaunchState === "success") {
      showFloatingToast(copy.openCodeAlreadyStartedToast, "success");
      return;
    }
    if (openCodeLaunchResetTimer.current) {
      window.clearTimeout(openCodeLaunchResetTimer.current);
      openCodeLaunchResetTimer.current = null;
    }
    setOpenCodeLaunchState("starting");
    showFloatingToast(copy.clientLaunching, "info");
    try {
      const result = await launchOpenCodeClient();
      addActivity(result.ok ? "success" : "warning", result.message);
      if (result.ok) {
        setOpenCodeLaunchState("success");
        showFloatingToast(copy.openCodeAlreadyStartedToast, "success");
        void refreshOpenCodeLocalStatus();
        window.setTimeout(() => void refreshOpenCodeLocalStatus(), 1200);
        openCodeLaunchResetTimer.current = window.setTimeout(() => {
          setOpenCodeLaunchState("idle");
          openCodeLaunchResetTimer.current = null;
        }, 4000);
      } else {
        setOpenCodeLaunchState("idle");
      }
    } catch (error) {
      setOpenCodeLaunchState("idle");
      addActivity("error", copy.clientLaunchFailed(String(error)));
      showFloatingToast(copy.openCodeInstallHintToast, "warning");
    }
  }, [addActivity, copy, openCodeLaunchState, refreshOpenCodeLocalStatus, showFloatingToast]);

  const stopLifeBookDownload = useCallback(async (dismissAfterStop = false) => {
    if (lifeBookDownloadState !== "downloading" && lifeBookDownloadState !== "cancelling") return;
    lifeBookDownloadDismissedRef.current = dismissAfterStop;
    setLifeBookDownloadDismissed(dismissAfterStop);
    setLifeBookDownloadState("cancelling");
    try {
      const result = await cancelLifeBookUpdate();
      addActivity(result.ok ? "warning" : "error", result.message);
    } catch (error) {
      addActivity("error", copy.lifeBookUpdateStopped(String(error)));
      showFloatingToast(copy.lifeBookUpdateStopped(String(error)), "error");
    }
  }, [addActivity, copy, lifeBookDownloadState, showFloatingToast]);

  const retryLifeBookDownload = useCallback(() => {
    setLifeBookDownloadDismissed(false);
    lifeBookDownloadDismissedRef.current = false;
    if (lifeBookRetryMode === "prepare") {
      void prepareLifeBook();
    } else {
      void syncLifeBookNow();
    }
  }, [lifeBookRetryMode, prepareLifeBook, syncLifeBookNow]);

  const closeLifeBookDownloadHud = useCallback(() => {
    setLifeBookDownloadDismissed(true);
    lifeBookDownloadDismissedRef.current = true;
    if (lifeBookDownloadState !== "downloading" && lifeBookDownloadState !== "cancelling") {
      setLifeBookDownloadState("idle");
    }
  }, [lifeBookDownloadState]);

  const stopOpenCodeDownload = useCallback(async (dismissAfterStop = false) => {
    if (openCodeDownloadState !== "downloading" && openCodeDownloadState !== "cancelling") return;
    openCodeDownloadDismissedRef.current = dismissAfterStop;
    setOpenCodeDownloadDismissed(dismissAfterStop);
    setOpenCodeDownloadState("cancelling");
    try {
      const result = await cancelOpenCodeDownload();
      addActivity(result.ok ? "warning" : "error", result.message);
    } catch (error) {
      addActivity("error", copy.openCodeUpdateFailed(String(error)));
      showFloatingToast(copy.openCodeUpdateFailed(String(error)), "error");
    }
  }, [addActivity, copy, openCodeDownloadState, showFloatingToast]);

  const retryOpenCodeDownload = useCallback(() => {
    setOpenCodeDownloadDismissed(false);
    openCodeDownloadDismissedRef.current = false;
    void doUpdateOpenCode(openCodeUpdate, true);
  }, [doUpdateOpenCode, openCodeUpdate]);

  const closeOpenCodeDownloadHud = useCallback(() => {
    setOpenCodeDownloadDismissed(true);
    openCodeDownloadDismissedRef.current = true;
    if (openCodeDownloadState !== "downloading" && openCodeDownloadState !== "cancelling") {
      setOpenCodeDownloadState("idle");
    }
  }, [openCodeDownloadState]);

  const updateSetting = useCallback(
    async (key: keyof LauncherSettings, value: boolean) => {
      const next = { ...settings, [key]: value };
      setSettings(next);
      saveSettings(next);
      if (key === "saveLogsToLocal") {
        try {
          const info = await setSaveLogsEnabled(value);
          setDiagnosticLogSettings(info);
          addActivity("success", copy.logSettingsSaved);
        } catch (error) {
          addActivity("error", copy.logSettingsSaveFailed(String(error)));
          void refreshDiagnosticLogSettings();
        }
      }
      if (key === "autoStart") {
        try {
          if (value) {
            await enable();
            addActivity("success", copy.autoStartEnabled);
          } else {
            await disable();
            addActivity("info", copy.autoStartDisabled);
          }
        } catch (error) {
          addActivity("error", copy.autoStartFailed(String(error)));
        }
      }
    },
    [addActivity, copy, refreshDiagnosticLogSettings, settings],
  );

  const doExportLauncherLogs = useCallback(async () => {
    addActivity("info", copy.exportingLogs);
    try {
      const result = await exportLauncherLogs();
      addActivity(result.ok ? "success" : "info", result.message);
    } catch (error) {
      addActivity("error", copy.logExportFailed(String(error)));
      showFloatingToast(copy.logExportFailed(String(error)), "error");
    }
  }, [addActivity, copy, showFloatingToast]);

  const updateProxySettingsDraft = useCallback((next: NetworkProxySettings) => {
    setProxySettings(next);
    setProxyTestResult(null);
    if (!next.enabled) {
      void saveProxySettings(next)
        .then((saved) => {
          setProxySettings(saved);
          void refreshState();
          addActivity("info", copy.proxyDisabledStatus);
        })
        .catch((error) => {
          const message = copy.proxySettingsFailed(String(error));
          addActivity("error", message);
          showFloatingToast(message, "error");
        });
    }
  }, [addActivity, copy, refreshState, showFloatingToast]);

  const doTestProxySettings = useCallback(async () => {
    setProxyBusy("test");
    setProxyTestResult(null);
    addActivity("info", copy.proxyTesting);
    try {
      const result = await testProxySettings(proxySettings);
      setProxyTestResult(result);
      if (!result.ok) {
        const message = result.message || copy.proxyTestFailed(copy.proxyUntested);
        addActivity("warning", message);
        showFloatingToast(message, "warning");
        return;
      }
      const saved = await saveProxySettings(proxySettings);
      setProxySettings(saved);
      await refreshState();
      const elapsed = result.elapsedMs ?? 0;
      const version = result.httpVersion ?? "";
      const message = copy.proxyTestAndApplied(elapsed, version);
      addActivity("success", message);
      showFloatingToast(message, "success");
    } catch (error) {
      const message = copy.proxyTestFailed(String(error));
      setProxyTestResult(proxyFailureResult(message));
      addActivity("error", message);
      showFloatingToast(message, "error");
    } finally {
      setProxyBusy(null);
    }
  }, [addActivity, copy, proxySettings, refreshState, showFloatingToast]);

  const doAutoDetectProxySettings = useCallback(async (force = true, silent = false) => {
    if (proxyBusy) return;
    setProxyBusy("detect");
    if (!silent) {
      addActivity("info", copy.proxyAutoDetecting);
    }
    try {
      const result = await autoDetectProxySettings(force);
      if (result.detected) {
        const detected = result.proxy ?? await getProxySettings();
        setProxySettings(detectedProxySettings(detected));
        setProxyTestResult(null);
      } else if (result.proxy) {
        setProxySettings(result.proxy);
      }
      if (result.test) {
        setProxyTestResult(result.test);
      }
      await refreshState();
      const message = result.detected ? copy.proxyAutoDetected : result.message || copy.proxyAutoDetectNotFound;
      if (!silent || Boolean(result.test)) {
        addActivity(result.detected ? "success" : "warning", message);
        showFloatingToast(message, result.detected ? "success" : "warning");
      }
    } catch (error) {
      if (!silent) {
        const message = copy.proxyTestFailed(String(error));
        setProxyTestResult(proxyFailureResult(message));
        addActivity("error", message);
        showFloatingToast(message, "error");
      }
    } finally {
      setProxyBusy(null);
    }
  }, [addActivity, copy, proxyBusy, refreshState, showFloatingToast]);

  const updateAutoInstallNodeModules = useCallback(async (enabled: boolean) => {
    try {
      if (!enabled && (nodeModulesDownloadState === "downloading" || nodeModulesDownloadState === "cancelling")) {
        void stopNodeModulesInstall(false);
      }
      const status = await setAutoInstallNodeModules(enabled);
      setNodeModulesStatus(status);
      if (!enabled) {
        setNodeModulesProgress(null);
        setNodeModulesDownloadMessage(null);
        setNodeModulesDownloadState("idle");
        nodeModulesAutoStartRef.current = false;
        return;
      }
      if (enabled && status.repoReady && !status.ready && !status.running) {
        nodeModulesAutoStartRef.current = false;
        void startNodeModulesInBackground(false);
      }
    } catch (error) {
      const message = copy.nodeModulesStatusFailed(String(error));
      addActivity("error", message);
      showFloatingToast(message, "error");
    }
  }, [
    addActivity,
    copy,
    nodeModulesDownloadState,
    showFloatingToast,
    startNodeModulesInBackground,
    stopNodeModulesInstall,
  ]);

  const runWindowAction = useCallback(async (action: "minimize" | "maximize" | "close") => {
    try {
      const maximized = await windowAction(action);
      if (typeof maximized === "boolean") {
        setIsMaximized(maximized);
      }
    } catch (error) {
      console.error("LifeBook Launcher window action failed:", error);
      addActivity("error", String(error));
    }
  }, [addActivity]);

  useEffect(() => {
    if (runtimeBootstrapBlocking) return undefined;
    if (!startupInitializedRef.current) {
      startupInitializedRef.current = true;
      void recordFrontendActivity("info", "frontend startup initialization begin").catch(() => undefined);
      refreshState();
      void refreshProxySettings();
      void doAutoDetectProxySettings(false, true);
      void refreshRuntimeStatus();
      void refreshNodeModulesStatus();
      void refreshOpenCodeLocalStatus();
      isEnabled()
        .then((enabled) => {
          setSettings((old) => {
            const next = { ...old, autoStart: enabled };
            saveSettings(next);
            return next;
          });
        })
        .catch(() => undefined);
    }

    const unlistenOpenCode = listenOpenCodeDownloadProgress((progress) => {
      setOpenCodeProgress(progress);
      if (progress.downloadedBytes > 0 || progress.percent > 0) {
        setOpenCodeSyntheticProgress(null);
      }
    });
    const unlistenLifeBook = listenLifeBookProgress((progress) => {
      setLifeBookProgress(progress);
      setLifeBookDownloadMessage(progress.message ?? null);
      if (progress.percent > 0 && progress.percent < 100) {
        setLifeBookDownloadState((current) => current === "idle" ? "downloading" : current);
      } else if (progress.percent >= 100 || progress.state === "success") {
        setLifeBookDownloadState("idle");
      } else if (progress.state === "failed") {
        setLifeBookDownloadState("failed");
      } else if (progress.state === "stopped") {
        setLifeBookDownloadState("stopped");
      }
    });
    const unlistenNodeModules = listenNodeModulesProgress((progress) => {
      setNodeModulesProgress(progress);
      setNodeModulesDownloadMessage(progress.message ?? null);
      if (progress.state === "success") {
        setNodeModulesDownloadState("idle");
        void refreshNodeModulesStatus();
        showFloatingToast(copy.nodeModulesReady, "success");
      } else if (progress.state === "failed") {
        setNodeModulesDownloadState("failed");
        addActivity("error", progress.message || copy.nodeModulesMissing);
        void refreshNodeModulesStatus();
      } else if (progress.state === "stopped") {
        setNodeModulesDownloadState("stopped");
        addActivity("warning", copy.nodeModulesInstallStopped);
        void refreshNodeModulesStatus();
      } else if (progress.percent > 0 && progress.percent < 100) {
        setNodeModulesDownloadState((current) => current === "idle" ? "downloading" : current);
      }
    });
    const unlistenLauncher = listenLauncherDownloadProgress((progress) => {
      setLauncherProgress(progress);
    });
    return () => {
      unlistenOpenCode.then((fn) => fn()).catch(() => undefined);
      unlistenLifeBook.then((fn) => fn()).catch(() => undefined);
      unlistenNodeModules.then((fn) => fn()).catch(() => undefined);
      unlistenLauncher.then((fn) => fn()).catch(() => undefined);
    };
  }, [
    addActivity,
    copy,
    doAutoDetectProxySettings,
    refreshNodeModulesStatus,
    refreshOpenCodeLocalStatus,
    refreshProxySettings,
    refreshRuntimeStatus,
    refreshState,
    runtimeBootstrapBlocking,
    showFloatingToast,
  ]);

  useEffect(() => {
    if (nodeModulesDownloadState !== "downloading" && nodeModulesDownloadState !== "cancelling") return undefined;
    const timer = window.setInterval(() => {
      void refreshNodeModulesStatus();
    }, 1500);
    return () => window.clearInterval(timer);
  }, [nodeModulesDownloadState, refreshNodeModulesStatus]);

  useEffect(() => {
    if (!hasTauriRuntime()) return undefined;
    const win = getCurrentWindow();
    let cancelled = false;
    win.isMaximized()
      .then((maximized) => {
        if (!cancelled) setIsMaximized(maximized);
      })
      .catch(() => undefined);
    const unlisten = win.onResized(async () => {
      try {
        const maximized = await win.isMaximized();
        if (!cancelled) setIsMaximized(maximized);
      } catch {
        // Keep the last known icon state if the platform cannot report it.
      }
    });
    return () => {
      cancelled = true;
      unlisten.then((fn) => fn()).catch(() => undefined);
    };
  }, []);

  useEffect(() => {
    void refreshDiagnosticLogSettings();
  }, [refreshDiagnosticLogSettings]);

  useEffect(() => {
    if (!nodeModulesStatus?.repoReady) {
      nodeModulesAutoStartRef.current = false;
      return;
    }
    if (nodeModulesStatus.ready) {
      nodeModulesAutoStartRef.current = true;
      return;
    }
    if (!nodeModulesStatus.autoInstall || nodeModulesStatus.running || nodeModulesAutoStartRef.current) return;
    nodeModulesAutoStartRef.current = true;
    void startNodeModulesInBackground(true);
  }, [nodeModulesStatus, startNodeModulesInBackground]);

  useEffect(() => {
    if (busy !== "opencode-update") return undefined;
    const timer = window.setInterval(() => {
      setOpenCodeSyntheticProgress((current) => {
        if (!openCodeDownloadStartedAt.current) return current;
        if (openCodeProgress && (openCodeProgress.downloadedBytes > 0 || openCodeProgress.percent > 0)) {
          return null;
        }
        const totalBytes = current?.totalBytes || openCodeProgress?.totalBytes || openCodeUpdate?.assetSize || 0;
        const elapsed = Date.now() - openCodeDownloadStartedAt.current;
        const percent = Math.min(92, Math.max(1, Math.floor(elapsed / 650) + 1));
        const downloadedBytes = totalBytes ? Math.floor((totalBytes * percent) / 100) : 0;
        return { percent, downloadedBytes, totalBytes };
      });
    }, 500);
    return () => window.clearInterval(timer);
  }, [busy, openCodeProgress, openCodeUpdate]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      void recordFrontendActivity(
        "info",
        `frontend startup automation begin checkLauncher=${settings.checkLauncherOnLaunch} checkOpenCode=${settings.checkOpenCodeOnLaunch}`,
      ).catch(() => undefined);
      void prepareLifeBookInBackground();
      if (settings.checkLauncherOnLaunch) void checkLauncher(false, true);
      if (settings.checkOpenCodeOnLaunch) void checkOpenCode(true);
    }, 600);
    return () => window.clearTimeout(timer);
    // Startup automation should run once after first paint using the initial persisted settings.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (activeTab === "tutorial" && state?.repoReady && !tutorialDoc && !tutorialLoading) {
      void loadTutorial(tutorialKind);
    }
  }, [activeTab, loadTutorial, state?.repoReady, tutorialDoc, tutorialKind, tutorialLoading]);

  useEffect(() => {
    setTutorialDoc(null);
  }, [state?.repoRoot]);

  useEffect(() => {
    if (!state?.repoReady) {
      setTutorialDoc(null);
      setTutorialLoading(false);
      setLifeBookUpdate(null);
      setShowAllCommits(true);
    }
  }, [state?.repoReady, state?.repoRoot, state?.repoStatus]);

  useEffect(() => {
    return () => {
      if (openCodeLaunchResetTimer.current) {
        window.clearTimeout(openCodeLaunchResetTimer.current);
      }
      if (floatingToastTimer.current) {
        window.clearTimeout(floatingToastTimer.current);
      }
      if (launcherUpdatePromptTimer.current) {
        window.clearTimeout(launcherUpdatePromptTimer.current);
      }
    };
  }, []);

  const commits = lifeBookUpdate?.commits ?? [];
  const displayedCommits = showAllCommits ? commits : commits.slice(0, 1);
  const firstCommit = commits[0];
  const repoReady = Boolean(state?.repoReady);
  const repoStatus = state?.repoStatus ?? "missing";
  const repoPath = state?.repoRoot || "D:\\LifeBook";
  const repoCanAutoPrepare = !repoReady && (repoStatus === "missing" || repoStatus === "empty");
  const repoIsEmpty = !repoReady && repoStatus === "empty";
  const repoIsOccupied = !repoReady && repoStatus === "occupied";
  const workspaceUnavailableDescription = repoIsOccupied
    ? copy.workspaceOccupiedDescription(repoPath)
    : repoIsEmpty
      ? copy.workspaceEmptyDescription(repoPath)
    : copy.workspaceMissingDescription(repoPath);
  const workspaceUnavailableHelp = repoIsOccupied
    ? copy.workspaceOccupiedHelp
    : repoIsEmpty
      ? copy.workspaceEmptyHelp
      : copy.workspaceMissingHelp;
  const lifeBookBusy = lifeBookPreparing || lifeBookSyncing;
  const unavailableRepoLabel = repoIsOccupied ? copy.repoInvalid : repoIsEmpty ? copy.repoEmpty : copy.repoMissing;
  const latestLifeBookVersion = firstCommit ? versionFromDate(firstCommit.date) : repoReady ? copy.projectReady : unavailableRepoLabel;
  const currentLifeBookVersion = repoReady
    ? state?.localCommitShort === "preview"
      ? "v2025.05.25"
      : state?.localCommitShort || copy.projectReady
    : lifeBookBusy
      ? copy.preparing
      : unavailableRepoLabel;
  const lifeBookStatus = lifeBookBusy ? copy.preparing : repoReady ? copy.projectReady : unavailableRepoLabel;
  const lifeBookStatusTone: "success" | "warning" | "muted" = lifeBookBusy ? "warning" : repoReady ? "success" : "muted";
  const latestLifeBookUpdated = firstCommit ? commitDate(firstCommit) : repoReady ? commitDate(firstCommit) : unavailableRepoLabel;
  const lifeBookPrimaryLabel = repoReady ? copy.openBooks : repoCanAutoPrepare ? copy.prepareProject : copy.changeProjectPath;
  const LifeBookPrimaryIcon = repoReady ? FolderOpen : repoCanAutoPrepare ? Download : FolderOpen;
  const lifeBookSecondaryLabel = repoReady ? copy.viewProject : repoCanAutoPrepare ? copy.changeProjectPath : copy.viewProject;
  const lifeBookSecondaryIcon = FolderOpen;
  const lifeBookMoreLabel = repoReady ? copy.updateLifeBookProject : repoCanAutoPrepare ? copy.prepareProject : copy.changeProjectPath;
  const openCodeAvailable = Boolean(openCodeLocalStatus?.clientAvailable ?? openCodeUpdate?.clientAvailable ?? state?.opencodeAvailable);
  const openCodeInstalledVersion = openCodeUpdate?.installedVersion ?? openCodeLocalStatus?.installedVersion ?? state?.opencodeInstalledVersion ?? null;
  const openCodeCurrent = openCodeAvailable ? openCodeInstalledVersion ?? copy.installed : copy.notInstalled;
  const openCodeLatest = openCodeUpdate?.latestVersion ?? (openCodeInstalledVersion ?? copy.checking);
  const openCodeHasUpdate = Boolean(openCodeUpdate?.hasUpdate);
  const openCodeStatus = openCodeAvailable ? (openCodeHasUpdate ? copy.updateAvailable : copy.upToDate) : copy.notInstalled;
  const openCodePrimaryLabel = copy.checkUpdates;
  const openCodePrimaryIcon = RefreshCcw;
  const openCodeSecondaryLabel = copy.launchClient;
  const showingLifeBookDownloadHud = lifeBookDownloadState !== "idle" && !lifeBookDownloadDismissed;
  const lifeBookProgressLabel = formatDownloadProgress(copy, lifeBookProgress);
  const lifeBookHudMessage = lifeBookDownloadMessage || lifeBookProgressLabel || copy.lifeBookProgressDefault;
  const openCodeVisibleProgress = busy === "opencode-update"
    ? (openCodeProgress && (openCodeProgress.downloadedBytes > 0 || openCodeProgress.percent > 0) ? openCodeProgress : openCodeSyntheticProgress ?? openCodeProgress)
    : null;
  const launcherVisibleProgress = busy === "launcher-update" ? launcherProgress : null;
  const openCodeProgressLabel = formatDownloadProgress(copy, openCodeVisibleProgress);
  const launcherProgressLabel = formatDownloadProgress(copy, launcherVisibleProgress);
  const activeGlobalProgress = launcherVisibleProgress
    ? { percent: launcherVisibleProgress.percent, label: `${copy.checkLauncherTitle} ${launcherProgressLabel}` }
    : null;
  const showingOpenCodeDownloadHud = openCodeDownloadState !== "idle" && !openCodeDownloadDismissed;
  const openCodeHudMessage = openCodeDownloadMessage || openCodeProgressLabel || copy.working;
  const nodeModulesProgressLabel = formatDownloadProgress(copy, nodeModulesProgress);
  const nodeModulesHudMessage = nodeModulesDownloadMessage || nodeModulesProgressLabel || copy.nodeModulesInstalling;
  const runtimeProgressLabel = formatDownloadProgress(copy, runtimeProgress);
  const launcherUpdatePromptNotes = launcherUpdatePrompt
    ? localizedReleaseNotes(launcherUpdatePrompt.releaseNotes, locale, copy.launcherUpdatePromptFallback)
    : "";

  const visibleActivities = useMemo(() => activities.slice(0, 5), [activities]);

  if (runtimeBootstrapBlocking) {
    return (
      <RuntimeBootstrapScreen
        copy={copy}
        state={runtimeBootstrapState}
        progress={runtimeProgress}
        message={runtimeBootstrapMessage || runtimeProgressLabel || copy.runtimeBootstrapChecking}
        onRetry={retryRuntimePrepare}
        onContinue={continueAfterRuntimeBootstrap}
      />
    );
  }

  return (
    <div className={isMaximized ? "launcher-frame maximized" : "launcher-frame"}>
      <header className="frame-titlebar">
        <div className="titlebar-brand" data-tauri-drag-region>
          <LogoMark />
          <span>LifeBook Launcher</span>
          <span className="titlebar-version">{LAUNCHER_VERSION}</span>
        </div>
        {launcherUpdatePrompt && (
          <LauncherUpdatePrompt
            copy={copy}
            info={launcherUpdatePrompt}
            notes={launcherUpdatePromptNotes}
            busy={busy === "launcher-update"}
            onUpdate={() => void doUpdateLauncher(launcherUpdatePrompt, true)}
            onSkip={hideLauncherUpdatePrompt}
          />
        )}
        <div className="titlebar-drag-region" data-tauri-drag-region onDoubleClick={() => void runWindowAction("maximize")} />
        <div className="window-controls">
          <button aria-label={copy.minimizeWindow} title={copy.minimizeWindow} onClick={() => void runWindowAction("minimize")}>-</button>
          <button aria-label={isMaximized ? copy.restoreWindow : copy.maximizeWindow} title={isMaximized ? copy.restoreWindow : copy.maximizeWindow} onClick={() => void runWindowAction("maximize")}><Square size={13} /></button>
          <button aria-label={copy.closeToTray} title={copy.closeToTray} onClick={() => void runWindowAction("close")}><X size={16} /></button>
        </div>
      </header>

      <main className="app-shell">
        <aside className="sidebar">
          <div className="brand-panel">
            <LogoMark large />
            <h1>LifeBook Launcher</h1>
            <p>{copy.knowledge}</p>
          </div>

          <nav className="nav-list">
            <NavButton icon={Home} label={copy.overview} active={activeTab === "overview"} onClick={() => setActiveTab("overview")} />
            <NavButton icon={RefreshCcw} label={copy.updates} active={activeTab === "updates"} working={refreshInProgress} onClick={() => void refreshAllStatus()} />
            <NavButton icon={BookOpen} label={copy.tutorial} active={activeTab === "tutorial"} onClick={() => setActiveTab("tutorial")} />
            <NavButton icon={Settings} label={copy.settings} active={activeTab === "settings"} onClick={() => setActiveTab("settings")} />
            <NavButton icon={FileText} label={copy.logs} active={activeTab === "logs"} onClick={() => setActiveTab("logs")} />
          </nav>

          <div className="sidebar-footer">
            <strong>LifeBook Launcher {LAUNCHER_VERSION}</strong>
            <span>{copy.mission}</span>
            <div className="platforms" aria-hidden="true">
              <span className="platform-icon">⊞</span>
              <Apple size={21} />
              <span className="platform-icon">♙</span>
            </div>
          </div>
        </aside>

        <section className="workspace">
          <StatusBar
            copy={copy}
            proxyConfigured={Boolean(state?.proxyConfigured)}
            autoStart={settings.autoStart}
            projectReady={repoReady}
            projectStatusValue={lifeBookStatus}
            quickActionsOpen={quickActionsOpen}
            onToggleQuickActions={() => setQuickActionsOpen((value) => !value)}
            onSelectRepo={() => {
              setQuickActionsOpen(false);
              void chooseRepo();
            }}
            onOpenRepo={() => {
              setQuickActionsOpen(false);
              void doOpenRepoFolder();
            }}
            onOpenBooks={() => {
              setQuickActionsOpen(false);
              void doOpenBooksFolder();
            }}
            onCheckLauncher={() => {
              setQuickActionsOpen(false);
              void checkLauncher(true);
            }}
            onCheckOpenCode={() => {
              setQuickActionsOpen(false);
              void checkOpenCode(false, true);
            }}
          />
          <FloatingFeedback
            toast={floatingToast}
            globalProgress={activeTab === "overview" || activeTab === "updates" ? activeGlobalProgress : null}
            lifeBookVisible={showingLifeBookDownloadHud}
            lifeBookTitle={copy.lifeBookProgressTitle}
            lifeBookState={lifeBookDownloadState}
            lifeBookProgress={lifeBookProgress}
            lifeBookMessage={lifeBookHudMessage}
            openCodeVisible={showingOpenCodeDownloadHud}
            openCodeTitle={copy.openCodeDownloadTitle}
            openCodeState={openCodeDownloadState}
            openCodeProgress={openCodeVisibleProgress ?? openCodeProgress}
            openCodeMessage={openCodeHudMessage}
            copy={copy}
            onStopOpenCode={() => void stopOpenCodeDownload(false)}
            onCancelOpenCode={() => void stopOpenCodeDownload(true)}
            onRetryOpenCode={retryOpenCodeDownload}
            onCloseOpenCode={closeOpenCodeDownloadHud}
            onStopLifeBook={() => void stopLifeBookDownload(false)}
            onCancelLifeBook={() => void stopLifeBookDownload(true)}
            onRetryLifeBook={retryLifeBookDownload}
            onCloseLifeBook={closeLifeBookDownloadHud}
          />

          {(activeTab === "overview" || activeTab === "updates") && (
            <>
              <section className="cards-grid">
                <ProductCard
                  accent="blue"
                  icon={BookOpen}
                  title={copy.lifeBookTitle}
                  subtitle={copy.lifeBookSubtitle}
                  current={currentLifeBookVersion}
                  latest={latestLifeBookVersion}
                  status={lifeBookStatus}
                  statusTone={lifeBookStatusTone}
                  latestUpdated={latestLifeBookUpdated}
                  primaryLabel={lifeBookPrimaryLabel}
                  primaryIcon={LifeBookPrimaryIcon}
                  secondaryLabel={lifeBookSecondaryLabel}
                  secondaryIcon={lifeBookSecondaryIcon}
                  busy={busy === "repo-choose"}
                  busyText={copy.working}
                  onPrimary={repoReady ? doOpenBooksFolder : repoCanAutoPrepare ? prepareLifeBook : chooseRepo}
                  onSecondary={repoReady ? doOpenRepoFolder : repoCanAutoPrepare ? chooseRepo : doOpenRepoFolder}
                  onMore={repoReady ? syncLifeBookNow : repoCanAutoPrepare ? prepareLifeBook : chooseRepo}
                  moreLabel={lifeBookMoreLabel}
                  moreBusy={lifeBookSyncing}
                  moreDisabled={lifeBookSyncing}
                  copy={copy}
                />
                <ProductCard
                  accent="green"
                  icon={Code2}
                  title={copy.openCodeTitle}
                  subtitle={copy.openCodeSubtitle}
                  current={openCodeCurrent}
                  latest={openCodeLatest}
                  status={openCodeStatus}
                  statusTone={openCodeAvailable ? (openCodeHasUpdate ? "warning" : "success") : "muted"}
                  latestUpdated="2025-05-24 18:42"
                  primaryLabel={openCodePrimaryLabel}
                  primaryIcon={openCodePrimaryIcon}
                  secondaryLabel={openCodeSecondaryLabel}
                  secondaryIcon={Play}
                  secondaryTone="green"
                  secondaryDisabled={false}
                  secondaryBusy={false}
                  secondaryBusyText={copy.clientLaunching}
                  busy={false}
                  busyText={openCodeProgressLabel || copy.working}
                  onPrimary={() => void checkOpenCode(false, true)}
                  onSecondary={doLaunchOpenCode}
                  onMore={() => void checkOpenCode(false, true)}
                  moreLabel={copy.checkUpdates}
                  copy={copy}
                />
              </section>

              <CommitTable
                copy={copy}
                commits={displayedCommits}
                totalCount={commits.length}
                latestVersion={latestLifeBookVersion}
                showAll={showAllCommits}
                emptyMessage={repoReady ? copy.noCommits : copy.noCommitsUnavailable}
                onToggleShowAll={() => setShowAllCommits((value) => !value)}
              />
              <ActivityTable copy={copy} activities={visibleActivities} onViewFullLog={() => setActiveTab("logs")} />
            </>
          )}

          {activeTab === "tutorial" && (
            <TutorialPanel
              copy={copy}
              kind={tutorialKind}
              document={tutorialDoc}
              loading={tutorialLoading}
              canGoBack={tutorialHistory.length > 0}
              repoReady={repoReady}
              unavailableTitle={copy.workspaceUnavailableTitle}
              unavailableDescription={workspaceUnavailableDescription}
              unavailableHelp={workspaceUnavailableHelp}
              recoverLabel={repoCanAutoPrepare ? copy.prepareProject : copy.changeProjectPath}
              onRecover={repoCanAutoPrepare ? prepareLifeBook : chooseRepo}
              onChangeProject={chooseRepo}
              onSelect={(kind) => void loadTutorial(kind)}
              onBack={goBackTutorial}
              onOpenLink={(href) => void openTutorialLink(href)}
            />
          )}

          {activeTab === "settings" && (
            <section className="settings-panel">
              <PanelHeading title={copy.settingsTitle} />
              <SettingToggle title={copy.autoStartTitle} description={copy.autoStartDescription} checked={settings.autoStart} onChange={(value) => updateSetting("autoStart", value)} />
              <ProjectPathPanel copy={copy} path={repoPath} onChange={() => void chooseRepo()} />
              <SettingToggle title={copy.checkLauncherTitle} description={copy.checkLauncherDescription} checked={settings.checkLauncherOnLaunch} onChange={(value) => updateSetting("checkLauncherOnLaunch", value)} />
              <SettingToggle title={copy.checkOpenCodeTitle} description={copy.checkOpenCodeDescription} checked={settings.checkOpenCodeOnLaunch} onChange={(value) => updateSetting("checkOpenCodeOnLaunch", value)} />
              <ProxySettingsPanel
                copy={copy}
                settings={proxySettings}
                busy={proxyBusy}
                result={proxyTestResult}
                onChange={updateProxySettingsDraft}
                onTest={() => void doTestProxySettings()}
                onAutoDetect={() => void doAutoDetectProxySettings(true, false)}
              />
              <RuntimeSettingsPanel
                copy={copy}
                status={runtimeStatus}
                onRetry={retryRuntimePrepare}
              />
              <NodeModulesSettingsPanel
                copy={copy}
                status={nodeModulesStatus}
                progress={nodeModulesProgress}
                state={nodeModulesDownloadState}
                message={nodeModulesHudMessage}
                onToggle={(value) => void updateAutoInstallNodeModules(value)}
                onStop={() => void stopNodeModulesInstall(false)}
                onCancel={() => void stopNodeModulesInstall(true)}
              />
              <DiagnosticLogPanel
                copy={copy}
                settings={diagnosticLogSettings}
                enabled={settings.saveLogsToLocal}
                onToggle={(value) => updateSetting("saveLogsToLocal", value)}
                onExport={() => void doExportLauncherLogs()}
              />
            </section>
          )}

          {activeTab === "logs" && <ActivityTable copy={copy} activities={activities.slice(0, 12)} expanded onViewFullLog={() => undefined} />}
        </section>
      </main>
      <ConfirmDialog dialog={confirmDialog} onCancel={() => resolveConfirmDialog(false)} onConfirm={() => resolveConfirmDialog(true)} />
    </div>
  );
}

function LauncherUpdatePrompt({
  copy,
  info,
  notes,
  busy,
  onUpdate,
  onSkip,
}: {
  copy: Copy;
  info: LauncherUpdateInfo;
  notes: string;
  busy: boolean;
  onUpdate: () => void;
  onSkip: () => void;
}) {
  return (
    <section className="launcher-update-prompt" aria-live="polite">
      <div className="launcher-update-prompt-title">
        <strong>{copy.launcherUpdatePromptTitle(info.latestVersion)}</strong>
        <span>{info.assetName}</span>
      </div>
      <p>{notes}</p>
      <div className="launcher-update-prompt-actions">
        <button type="button" onClick={onSkip} disabled={busy}>
          {copy.launcherUpdatePromptSkip}
        </button>
        <button type="button" className="primary" onClick={onUpdate} disabled={busy}>
          {busy ? copy.working : copy.launcherUpdatePromptUpdate}
        </button>
      </div>
    </section>
  );
}

function StatusBar({
  copy,
  proxyConfigured,
  autoStart,
  projectReady,
  projectStatusValue,
  quickActionsOpen,
  onToggleQuickActions,
  onSelectRepo,
  onOpenRepo,
  onOpenBooks,
  onCheckLauncher,
  onCheckOpenCode,
}: {
  copy: Copy;
  proxyConfigured: boolean;
  autoStart: boolean;
  projectReady: boolean;
  projectStatusValue: string;
  quickActionsOpen: boolean;
  onToggleQuickActions: () => void;
  onSelectRepo: () => void;
  onOpenRepo: () => void;
  onOpenBooks: () => void;
  onCheckLauncher: () => void;
  onCheckOpenCode: () => void;
}) {
  return (
    <section className="status-bar">
      <StatusItem label={copy.projectStatus} icon={CheckCircle2} value={projectReady ? copy.running : projectStatusValue} tone={projectReady ? "green" : "blue"} />
      <StatusItem label={copy.networkProxy} icon={Globe2} value={proxyConfigured ? copy.proxied : copy.direct} tone={proxyConfigured ? "blue" : "green"} />
      <StatusItem label={copy.startup} icon={Power} value={autoStart ? copy.enabled : copy.disabled} tone={autoStart ? "green" : "blue"} />
      <div className="quick-action-wrap">
        <button className="quick-action" type="button" onClick={onToggleQuickActions} aria-expanded={quickActionsOpen}>
          {copy.quickActions}
          <ChevronDown size={16} />
        </button>
        {quickActionsOpen && (
          <div className="quick-menu">
            <button type="button" onClick={onSelectRepo}>{copy.selectRepo}</button>
            <button type="button" onClick={onOpenRepo}>{copy.viewProject}</button>
            <button type="button" disabled={!projectReady} onClick={onOpenBooks}>{copy.openBooks}</button>
            <button type="button" onClick={onCheckLauncher}>{copy.checkUpdates} Launcher</button>
            <button type="button" onClick={onCheckOpenCode}>{copy.checkUpdates} OpenCode</button>
          </div>
        )}
      </div>
    </section>
  );
}

function StatusItem({ label, icon: Icon, value, tone }: { label: string; icon: LucideIcon; value: string; tone: "blue" | "green" }) {
  return (
    <div className="status-item">
      <span>{label}</span>
      <Icon size={20} className={`status-icon ${tone}`} />
      <strong className={tone}>{value}</strong>
    </div>
  );
}

function NavButton({ icon: Icon, label, active, working, onClick }: { icon: LucideIcon; label: string; active: boolean; working?: boolean; onClick: () => void }) {
  return (
    <button className={active ? "nav-item active" : "nav-item"} onClick={onClick}>
      <Icon size={24} strokeWidth={1.9} className={working ? "spin-icon" : undefined} />
      <span>{label}</span>
    </button>
  );
}

function TutorialPanel({
  copy,
  kind,
  document,
  loading,
  canGoBack,
  repoReady,
  unavailableTitle,
  unavailableDescription,
  unavailableHelp,
  recoverLabel,
  onRecover,
  onChangeProject,
  onSelect,
  onBack,
  onOpenLink,
}: {
  copy: Copy;
  kind: TutorialKind;
  document: ProjectDocument | null;
  loading: boolean;
  canGoBack: boolean;
  repoReady: boolean;
  unavailableTitle: string;
  unavailableDescription: string;
  unavailableHelp: string;
  recoverLabel: string;
  onRecover: () => void;
  onChangeProject: () => void;
  onSelect: (kind: TutorialKind) => void;
  onBack: () => void;
  onOpenLink: (href: string) => void;
}) {
  const html = useMemo(() => renderMarkdownToHtml(document?.content ?? "", copy), [copy, document]);
  const handleClick = async (event: MouseEvent<HTMLDivElement>) => {
    const target = event.target as HTMLElement | null;
    const copyButton = target?.closest<HTMLButtonElement>("button[data-copy-code]");
    if (copyButton) {
      event.preventDefault();
      event.stopPropagation();
      const payload = copyButton.dataset.copyCode ?? "";
      const originalLabel = copyButton.textContent || copy.copyCode;
      try {
        await copyTextToClipboard(decodeCodePayload(payload));
        copyButton.textContent = copy.codeCopied;
        copyButton.classList.add("copied");
      } catch {
        copyButton.textContent = copy.codeCopyFailed;
        copyButton.classList.add("failed");
      }
      window.setTimeout(() => {
        copyButton.textContent = originalLabel;
        copyButton.classList.remove("copied", "failed");
      }, 1500);
      return;
    }
    const link = target?.closest("a");
    const href = link?.getAttribute("href");
    if (!href) return;
    if (href.startsWith("http://") || href.startsWith("https://")) {
      window.open(href, "_blank", "noopener,noreferrer");
      event.preventDefault();
      return;
    }
    if (href.startsWith("#")) return;
    event.preventDefault();
    onOpenLink(href);
  };

  return (
    <section className="tutorial-panel">
      <div className="panel-title-row tutorial-title-row">
        <div className="tutorial-heading-group">
          {canGoBack && (
            <button type="button" className="tutorial-back-button" onClick={onBack}>
              <ArrowLeft size={18} />
              <span>{copy.tutorialBack}</span>
            </button>
          )}
          <PanelHeading title={copy.tutorialTitle} />
        </div>
        <div className="tutorial-switch" role="tablist" aria-label={copy.tutorialTitle}>
          <button type="button" className={kind === "readme" ? "active" : undefined} onClick={() => onSelect("readme")}>{copy.tutorialReadme}</button>
          <button type="button" className={kind === "howto" ? "active" : undefined} onClick={() => onSelect("howto")}>{copy.tutorialHowTo}</button>
        </div>
      </div>
      <div className="tutorial-doc-meta">
        <strong>{document?.title || copy.tutorialTitle}</strong>
        <span>{copy.tutorialCurrentDocument}: {repoReady ? document?.path || copy.tutorialLoading : unavailableDescription}</span>
      </div>
      <div className="tutorial-scroll">
        {!repoReady ? (
          <div className="workspace-empty">
            <strong>{unavailableTitle}</strong>
            <p>{unavailableDescription}</p>
            <p>{unavailableHelp}</p>
            <div className="workspace-empty-actions">
              <button type="button" onClick={onRecover}>{recoverLabel}</button>
              {recoverLabel !== copy.changeProjectPath && (
                <button type="button" className="secondary" onClick={onChangeProject}>{copy.changeProjectPath}</button>
              )}
            </div>
          </div>
        ) : loading ? (
          <div className="table-empty">{copy.tutorialLoading}</div>
        ) : (
          <div className="markdown-body" onClick={handleClick} dangerouslySetInnerHTML={{ __html: html }} />
        )}
      </div>
    </section>
  );
}

function renderMarkdownToHtml(source: string, copy: Copy) {
  const lines = source.replace(/\r\n/g, "\n").split("\n");
  const html: string[] = [];
  let inList = false;
  let inCode = false;
  let codeLines: string[] = [];
  let inHtmlBlock = false;
  let htmlLines: string[] = [];

  const closeList = () => {
    if (inList) {
      html.push("</ul>");
      inList = false;
    }
  };

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith("```")) {
      closeList();
      if (inCode) {
        html.push(renderCodeBlock(codeLines.join("\n"), copy.copyCode));
        codeLines = [];
        inCode = false;
      } else {
        inCode = true;
      }
      continue;
    }
    if (inCode) {
      codeLines.push(line);
      continue;
    }
    if (inHtmlBlock) {
      htmlLines.push(line);
      if (trimmed.toLowerCase().includes("</table>")) {
        html.push(sanitizeTrustedDocHtml(htmlLines.join("\n")));
        htmlLines = [];
        inHtmlBlock = false;
      }
      continue;
    }
    if (trimmed.toLowerCase().startsWith("<table")) {
      closeList();
      inHtmlBlock = true;
      htmlLines = [line];
      if (trimmed.toLowerCase().includes("</table>")) {
        html.push(sanitizeTrustedDocHtml(htmlLines.join("\n")));
        htmlLines = [];
        inHtmlBlock = false;
      }
      continue;
    }
    if (!trimmed) {
      closeList();
      continue;
    }
    const heading = trimmed.match(/^(#{1,4})\s+(.+)$/);
    if (heading) {
      closeList();
      const level = heading[1].length;
      html.push(`<h${level}>${formatInlineMarkdown(heading[2])}</h${level}>`);
      continue;
    }
    const listItem = trimmed.match(/^[-*]\s+(.+)$/);
    if (listItem) {
      if (!inList) {
        html.push("<ul>");
        inList = true;
      }
      html.push(`<li>${formatInlineMarkdown(listItem[1])}</li>`);
      continue;
    }
    closeList();
    html.push(`<p>${formatInlineMarkdown(trimmed)}</p>`);
  }
  closeList();
  if (inCode) {
    html.push(renderCodeBlock(codeLines.join("\n"), copy.copyCode));
  }
  if (inHtmlBlock && htmlLines.length) {
    html.push(sanitizeTrustedDocHtml(htmlLines.join("\n")));
  }
  return html.join("\n");
}

function renderCodeBlock(code: string, copyLabel: string) {
  return [
    `<div class="code-block">`,
    `<button type="button" class="code-copy-button" data-copy-code="${encodeCodePayload(code)}">${escapeHtml(copyLabel)}</button>`,
    `<pre><code>${escapeHtml(code)}</code></pre>`,
    `</div>`,
  ].join("");
}

function encodeCodePayload(value: string) {
  return encodeURIComponent(value);
}

function decodeCodePayload(value: string) {
  return decodeURIComponent(value);
}

async function copyTextToClipboard(text: string) {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "fixed";
  textarea.style.left = "-9999px";
  document.body.appendChild(textarea);
  textarea.select();
  const ok = document.execCommand("copy");
  textarea.remove();
  if (!ok) throw new Error("copy failed");
}

function formatInlineMarkdown(value: string) {
  let html = escapeHtml(value);
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_match, label, href) => {
    const safeHref = sanitizeHref(String(href));
    return `<a href="${safeHref}">${label}</a>`;
  });
  return html;
}

function escapeHtml(value: string) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function sanitizeHref(value: string) {
  const trimmed = value.trim();
  if (/^javascript:/i.test(trimmed)) return "#";
  return escapeHtml(trimmed);
}

function sanitizeTrustedDocHtml(value: string) {
  return value
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/\son\w+="[^"]*"/gi, "")
    .replace(/\son\w+='[^']*'/gi, "")
    .replace(/javascript:/gi, "");
}

function RuntimeBootstrapScreen({
  copy,
  state,
  progress,
  message,
  onRetry,
  onContinue,
}: {
  copy: Copy;
  state: RuntimeBootstrapState;
  progress: DownloadProgress | null;
  message: string;
  onRetry: () => void;
  onContinue: () => void;
}) {
  const percent = progress?.percent ?? (state === "checking" ? 0.01 : state === "ready" ? 100 : 1);
  const isFailed = state === "failed";
  return (
    <div className="runtime-bootstrap-shell">
      <section className={`runtime-bootstrap-card ${state}`}>
        <LogoMark large />
        <div>
          <p className="runtime-bootstrap-kicker">LifeBook Launcher</p>
          <h1>{copy.runtimeBootstrapTitle}</h1>
          <p className="runtime-bootstrap-description">{copy.runtimeBootstrapDescription}</p>
        </div>
        <div className="runtime-bootstrap-progress">
          <div className="floating-progress-header">
            <strong>
              {state === "checking"
                ? copy.runtimeBootstrapChecking
                : state === "ready"
                  ? copy.runtimeBootstrapReady
                  : isFailed
                    ? copy.runtimeBootstrapFailed
                    : copy.runtimeBootstrapPreparing}
            </strong>
            <span>{formatPercent(percent)}</span>
          </div>
          <div className="progress-bar">
            <span style={{ width: progressWidth(percent) }} />
          </div>
          <div className="runtime-bootstrap-message">{message}</div>
        </div>
        {state !== "ready" && (
          <div className="runtime-bootstrap-actions">
            <button type="button" onClick={onContinue}>{copy.runtimeBootstrapContinue}</button>
            {isFailed && (
              <button type="button" className="primary" onClick={onRetry}>{copy.runtimeBootstrapRetry}</button>
            )}
          </div>
        )}
      </section>
    </div>
  );
}

function FloatingFeedback({
  toast,
  globalProgress,
  lifeBookVisible,
  lifeBookTitle,
  lifeBookState,
  lifeBookProgress,
  lifeBookMessage,
  openCodeVisible,
  openCodeTitle,
  openCodeState,
  openCodeProgress,
  openCodeMessage,
  copy,
  onStopOpenCode,
  onCancelOpenCode,
  onRetryOpenCode,
  onCloseOpenCode,
  onStopLifeBook,
  onCancelLifeBook,
  onRetryLifeBook,
  onCloseLifeBook,
}: {
  toast: FloatingToast | null;
  globalProgress: { percent: number; label: string } | null;
  lifeBookVisible: boolean;
  lifeBookTitle: string;
  lifeBookState: DownloadHudState;
  lifeBookProgress?: DownloadProgress | null;
  lifeBookMessage: string;
  openCodeVisible: boolean;
  openCodeTitle: string;
  openCodeState: DownloadHudState;
  openCodeProgress?: DownloadProgress | null;
  openCodeMessage: string;
  copy: Copy;
  onStopOpenCode: () => void;
  onCancelOpenCode: () => void;
  onRetryOpenCode: () => void;
  onCloseOpenCode: () => void;
  onStopLifeBook: () => void;
  onCancelLifeBook: () => void;
  onRetryLifeBook: () => void;
  onCloseLifeBook: () => void;
}) {
  if (!toast && !globalProgress && !lifeBookVisible && !openCodeVisible) return null;
  const lifeBookPercent = lifeBookProgress?.percent ?? 0;
  const lifeBookRunning = lifeBookState === "downloading" || lifeBookState === "cancelling";
  const openCodePercent = openCodeProgress?.percent ?? 0;
  const openCodeRunning = openCodeState === "downloading" || openCodeState === "cancelling";
  return (
    <div className="floating-feedback-layer" aria-live="polite">
      {toast && <div className={`floating-toast ${toast.tone}`}>{toast.message}</div>}
      {globalProgress && (
        <section className="floating-progress-card blue">
          <div className="floating-progress-header">
            <strong>{globalProgress.label}</strong>
            <span>{formatPercent(globalProgress.percent)}</span>
          </div>
          <div className="progress-bar">
            <span style={{ width: progressWidth(globalProgress.percent) }} />
          </div>
        </section>
      )}
      {lifeBookVisible && (
        <TaskProgressCard
          accent="blue"
          title={lifeBookTitle}
          state={lifeBookState}
          percent={lifeBookPercent}
          message={lifeBookState === "cancelling" ? copy.working : lifeBookMessage}
          running={lifeBookRunning}
          copy={copy}
          onStop={onStopLifeBook}
          onCancel={onCancelLifeBook}
          onRetry={onRetryLifeBook}
          onClose={onCloseLifeBook}
        />
      )}
      {openCodeVisible && (
        <TaskProgressCard
          accent="green"
          title={openCodeTitle}
          state={openCodeState}
          percent={openCodePercent}
          message={openCodeState === "cancelling" ? copy.working : openCodeMessage}
          running={openCodeRunning}
          copy={copy}
          onStop={onStopOpenCode}
          onCancel={onCancelOpenCode}
          onRetry={onRetryOpenCode}
          onClose={onCloseOpenCode}
        />
      )}
    </div>
  );
}

function TaskProgressCard({
  accent,
  title,
  state,
  percent,
  message,
  running,
  copy,
  onStop,
  onCancel,
  onRetry,
  onClose,
}: {
  accent: "blue" | "green";
  title: string;
  state: DownloadHudState;
  percent: number;
  message: string;
  running: boolean;
  copy: Copy;
  onStop: () => void;
  onCancel: () => void;
  onRetry: () => void;
  onClose: () => void;
}) {
  return (
    <section className={`floating-progress-card ${accent} ${state}`}>
      <div className="floating-progress-header">
        <strong>{title}</strong>
        <span>{formatPercent(percent)}</span>
      </div>
      <div className="progress-bar">
        <span style={{ width: progressWidth(percent) }} />
      </div>
      <div className="floating-progress-footer">
        <span>{message}</span>
        <div className="floating-progress-actions">
          {running ? (
            <>
              <button type="button" onClick={onStop} disabled={state === "cancelling"}>{copy.stopDownload}</button>
              <button type="button" onClick={onCancel} disabled={state === "cancelling"}>{copy.cancelDownload}</button>
            </>
          ) : (
            <>
              <button type="button" onClick={onRetry}>{copy.retry}</button>
              <button type="button" onClick={onClose}>{copy.close}</button>
            </>
          )}
        </div>
      </div>
    </section>
  );
}

function ProductCard(props: {
  accent: "blue" | "green";
  icon: LucideIcon;
  title: string;
  subtitle: string;
  current: string;
  latest: string;
  status: string;
  statusTone: "success" | "warning" | "muted";
  latestUpdated: string;
  progress?: DownloadProgress | null;
  progressLabel?: string;
  primaryLabel: string;
  primaryIcon: LucideIcon;
  secondaryLabel: string;
  secondaryIcon: LucideIcon;
  secondaryTone?: "default" | "green" | "muted";
  secondaryDisabled?: boolean;
  secondaryBusy?: boolean;
  secondaryBusyText?: string;
  busy: boolean;
  busyText: string;
  onPrimary: () => void;
  onSecondary: () => void;
  onMore: () => void;
  moreLabel: string;
  moreBusy?: boolean;
  moreDisabled?: boolean;
  copy: Copy;
}) {
  const Icon = props.icon;
  const PrimaryIcon = props.primaryIcon;
  const SecondaryIcon = props.secondaryIcon;
  const secondaryBusy = Boolean(props.secondaryBusy);
  return (
    <article className={`product-card ${props.accent}`}>
      <div className="product-heading">
        <div className={`product-icon ${props.accent}`}>
          <Icon size={36} strokeWidth={2.2} />
        </div>
        <div>
          <h2>{props.title}</h2>
          <p>{props.subtitle}</p>
        </div>
      </div>
      <div className="product-meta">
        <MetaPair label={props.copy.currentVersion} value={props.current} highlight />
        <MetaPair label={props.copy.updateStatus} value={props.status} tone={props.statusTone} />
        <MetaPair label={props.copy.latestVersion} value={props.latest} />
        <MetaPair label={props.copy.latestUpdate} value={props.latestUpdated} />
      </div>
      <div className="product-actions">
        <button className={`primary ${props.accent}`} disabled={props.busy} onClick={props.onPrimary}>
          <PrimaryIcon size={22} />
          {props.busy ? props.busyText : props.primaryLabel}
        </button>
        <button className={`secondary ${props.secondaryTone ?? "default"}`} disabled={props.secondaryDisabled || props.busy || secondaryBusy} onClick={props.onSecondary}>
          <SecondaryIcon size={21} className={secondaryBusy ? "spin-icon" : undefined} />
          {secondaryBusy ? props.secondaryBusyText ?? props.busyText : props.secondaryLabel}
        </button>
        <button className="icon-button" type="button" aria-label={props.moreLabel} title={props.moreLabel} disabled={props.moreDisabled || props.moreBusy} onClick={props.onMore}>
          <MoreHorizontal size={22} className={props.moreBusy ? "spin-icon" : undefined} />
        </button>
      </div>
      {props.progress && (
        <div className="progress-strip" aria-label={props.progressLabel}>
          <div className="progress-bar">
            <span style={{ width: progressWidth(props.progress.percent) }} />
          </div>
          <strong>{props.progressLabel}</strong>
        </div>
      )}
    </article>
  );
}

function MetaPair({ label, value, highlight, tone }: { label: string; value: string; highlight?: boolean; tone?: "success" | "warning" | "muted" }) {
  return (
    <div className="meta-pair">
      <span>{label}</span>
      <strong className={tone ? `${tone}-pill` : highlight ? "version-pill" : undefined}>{value}</strong>
    </div>
  );
}

function proxyFailureResult(message: string): ProxyTestResult {
  return {
    ok: false,
    message,
    elapsedMs: null,
    httpVersion: null,
    targetUrl: "",
  };
}

function detectedProxySettings(proxy: NetworkProxySettings): NetworkProxySettings {
  return {
    ...proxy,
    enabled: true,
    host: proxy.host || "127.0.0.1",
    port: proxy.port ?? 7890,
  };
}

function CommitTable({
  copy,
  commits,
  totalCount,
  latestVersion,
  showAll,
  emptyMessage,
  onToggleShowAll,
}: {
  copy: Copy;
  commits: CommitInfo[];
  totalCount: number;
  latestVersion: string;
  showAll: boolean;
  emptyMessage?: string;
  onToggleShowAll: () => void;
}) {
  const [hoverTooltip, setHoverTooltip] = useState<{ text: string; left: number; top: number } | null>(null);

  const showTooltip = useCallback((target: HTMLElement, text: string) => {
    const rect = target.getBoundingClientRect();
    const margin = 18;
    const tooltipWidth = Math.min(720, Math.max(320, window.innerWidth - margin * 2));
    const left = Math.min(
      Math.max(rect.left, margin),
      Math.max(margin, window.innerWidth - tooltipWidth - margin),
    );
    const belowTop = rect.bottom + 10;
    const top = belowTop < window.innerHeight - 120 ? belowTop : Math.max(margin, rect.top - 220);
    setHoverTooltip({ text, left, top });
  }, []);

  const hideTooltip = useCallback(() => {
    setHoverTooltip(null);
  }, []);

  return (
    <section className={showAll ? "data-panel commit-panel expanded" : "data-panel commit-panel"}>
      <div className="panel-title-row">
        <PanelHeading title={copy.updateContent} />
        <div className="panel-actions">
          <span>{copy.updateTo} {latestVersion}</span>
          {totalCount > 1 && (
            <button type="button" onClick={onToggleShowAll}>
              {showAll ? copy.showLatestOnly : copy.viewAllUpdates}
            </button>
          )}
        </div>
      </div>
      <div className="table-wrap commit-table-wrap">
        {commits.length ? (
          <table className="data-table commit-table">
            <thead>
              <tr>
                <th>{copy.date}</th>
                <th>{copy.commit}</th>
                <th>{copy.title}</th>
                <th>{copy.summary}</th>
              </tr>
            </thead>
            <tbody>
              {commits.map((commit, index) => {
                const tooltipText = formatCommitTooltip(copy, commit);
                return (
                  <tr key={`${commit.hash}-${commit.date}`}>
                    <td><RowIcon index={index} />{commit.date.slice(0, 16).replace("T", " ")}</td>
                    <td><code>{commit.hash}</code></td>
                    <td>{commit.title}</td>
                    <td
                      className="commit-summary-cell"
                      data-tooltip={tooltipText}
                      aria-label={tooltipText}
                      onMouseEnter={(event) => showTooltip(event.currentTarget, tooltipText)}
                      onMouseLeave={hideTooltip}
                      onFocus={(event) => showTooltip(event.currentTarget, tooltipText)}
                      onBlur={hideTooltip}
                      tabIndex={0}
                    >
                      {commit.summary || copy.noCommits}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        ) : (
          <div className="table-empty">{emptyMessage ?? copy.noCommits}</div>
        )}
      </div>
      {hoverTooltip && (
        <div
          className="commit-hover-tooltip"
          role="tooltip"
          style={{ left: hoverTooltip.left, top: hoverTooltip.top }}
        >
          {hoverTooltip.text}
        </div>
      )}
    </section>
  );
}

function formatCommitTooltip(copy: Copy, commit: CommitInfo) {
  const date = commit.date.slice(0, 16).replace("T", " ");
  const details = commit.fullMessage?.trim() || commit.summary || copy.noCommits;
  return [
    `${copy.date}: ${date}`,
    `${copy.commit}: ${commit.hash}`,
    `${copy.title}: ${commit.title}`,
    "",
    details,
  ].join("\n");
}

function ActivityTable({ copy, activities, expanded, onViewFullLog }: { copy: Copy; activities: ActivityItem[]; expanded?: boolean; onViewFullLog: () => void }) {
  return (
    <section className={`data-panel activity-panel ${expanded ? "expanded" : ""}`}>
      <div className="panel-title-row">
        <PanelHeading title={copy.recentActivity} />
        {!expanded && <button className="panel-button" onClick={onViewFullLog}>{copy.viewFullLog}</button>}
      </div>
      <div className="table-wrap activity-table-wrap">
        <table className="data-table activity-table">
          <tbody>
            {activities.map((item) => (
              <tr key={item.id}>
                <td><Clock3 size={16} />{item.time}</td>
                <td>{item.message}</td>
                <td><span className={`level-badge ${item.level}`}>{copy.info}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function PanelHeading({ title }: { title: string }) {
  return (
    <div className="panel-heading">
      <span />
      <h2>{title}</h2>
    </div>
  );
}

function RowIcon({ index }: { index: number }) {
  const icons = [CalendarDays, RefreshCcw, FileText, Settings];
  const Icon = icons[index % icons.length];
  return <Icon size={16} className={`row-icon color-${index % 4}`} />;
}

function ProjectPathPanel({ copy, path, onChange }: { copy: Copy; path: string; onChange: () => void }) {
  return (
    <div className="project-path-row">
      <div className="project-path-copy">
        <strong>{copy.projectPath}</strong>
        <code title={path}>{path}</code>
      </div>
      <button className="panel-button" type="button" onClick={onChange}>
        <FolderOpen size={16} />
        {copy.changeProjectPath}
      </button>
    </div>
  );
}

function ProxySettingsPanel({
  copy,
  settings,
  busy,
  result,
  onChange,
  onTest,
  onAutoDetect,
}: {
  copy: Copy;
  settings: NetworkProxySettings;
  busy: "test" | "detect" | null;
  result: ProxyTestResult | null;
  onChange: (value: NetworkProxySettings) => void;
  onTest: () => void;
  onAutoDetect: () => void;
}) {
  const update = (patch: Partial<NetworkProxySettings>) => onChange({ ...settings, ...patch });
  const portValue = settings.port ?? "";
  const statusClass = !settings.enabled ? "muted" : result ? result.ok ? "success" : "error" : "muted";
  const statusText = !settings.enabled
    ? copy.proxyDisabledStatus
    : result
      ? result.ok
        ? `${result.elapsedMs ?? 0} ms${result.httpVersion ? ` · ${result.httpVersion}` : ""}`
        : result.message
      : copy.proxyPendingTest;
  return (
    <div className="proxy-settings-panel">
      <div className="proxy-settings-copy">
        <strong>{copy.proxySettingsTitle}</strong>
        <span>{copy.proxySettingsDescription}</span>
      </div>
      <div className="proxy-settings-grid">
        <label className="proxy-toggle">
          <input
            type="checkbox"
            checked={settings.enabled}
            onChange={(event) => update({ enabled: event.currentTarget.checked })}
          />
          <span>{copy.proxyEnable}</span>
        </label>
        <label>
          <span>{copy.proxyProtocol}</span>
          <select
            value={settings.scheme}
            onChange={(event) => update({ scheme: event.currentTarget.value as NetworkProxySettings["scheme"] })}
          >
            <option value="http">HTTP</option>
            <option value="https">HTTPS</option>
            <option value="socks5">SOCKS5</option>
            <option value="socks5h">SOCKS5H</option>
          </select>
        </label>
        <label>
          <span>{copy.proxyHost}</span>
          <input
            type="text"
            value={settings.host}
            placeholder="127.0.0.1"
            onChange={(event) => update({ host: event.currentTarget.value })}
          />
        </label>
        <label>
          <span>{copy.proxyPort}</span>
          <input
            type="number"
            min={1}
            max={65535}
            value={portValue}
            placeholder="7890"
            onChange={(event) => {
              const value = event.currentTarget.value.trim();
              update({ port: value ? Number(value) : null });
            }}
          />
        </label>
      </div>
      <div className="proxy-actions">
        <button className="panel-button" type="button" onClick={onAutoDetect} disabled={busy !== null}>
          <RefreshCcw size={16} />
          {busy === "detect" ? copy.proxyAutoDetecting : copy.proxyAutoDetect}
        </button>
        <button className="panel-button" type="button" onClick={onTest} disabled={busy !== null}>
          <Globe2 size={16} />
          {busy === "test" ? copy.proxyTesting : copy.proxyTest}
        </button>
        <span className={`proxy-inline-status ${statusClass}`}>{statusText}</span>
      </div>
    </div>
  );
}

function RuntimeSettingsPanel({
  copy,
  status,
  onRetry,
}: {
  copy: Copy;
  status: RuntimeStatus | null;
  onRetry: () => void;
}) {
  const ready = Boolean(status?.ready);
  const running = Boolean(status?.running);
  const text = ready ? copy.runtimeStatusReady : copy.runtimeStatusMissing;
  return (
    <div className="runtime-settings-panel">
      <div className="runtime-settings-copy">
        <div className="setting-title-line">
          <strong>{copy.runtimeStatusTitle}</strong>
          <span className={`setting-status-pill ${ready ? "success" : running ? "working" : "error"}`}>
            {text}
          </span>
        </div>
        <span>{copy.runtimeStatusDescription}</span>
        <div className="runtime-tool-lines">
          <code>Python {status?.python.version ?? "3.12"}: {status?.python.path || status?.python.message || "-"}</code>
          <code>Java {status?.java.version ?? "17"}: {status?.java.path || status?.java.message || "-"}</code>
        </div>
      </div>
      {!ready && (
        <button className="panel-button" type="button" onClick={onRetry} disabled={running}>
          <RefreshCcw size={16} />
          {copy.runtimeBootstrapRetry}
        </button>
      )}
    </div>
  );
}

function NodeModulesSettingsPanel({
  copy,
  status,
  progress,
  state,
  message,
  onToggle,
  onStop,
  onCancel,
}: {
  copy: Copy;
  status: NodeModulesStatus | null;
  progress: DownloadProgress | null;
  state: DownloadHudState;
  message: string;
  onToggle: (value: boolean) => void;
  onStop: () => void;
  onCancel: () => void;
}) {
  const running = state === "downloading" || state === "cancelling" || Boolean(status?.running);
  const ready = Boolean(status?.ready);
  const autoInstall = status?.autoInstall ?? true;
  const failedOrStopped = state === "failed" || state === "stopped";
  const statusText = !autoInstall
    ? copy.nodeModulesDisabled
    : failedOrStopped
      ? copy.nodeModulesRetryHint
      : running
    ? copy.nodeModulesInstalling
    : ready
      ? copy.nodeModulesReady
      : status?.repoReady
        ? copy.nodeModulesMissing
        : copy.nodeModulesNotReady;
  const percent = progress?.percent ?? 0;
  const showProgress = running || state === "failed" || state === "stopped";
  return (
    <div className="node-modules-settings-panel">
      <label className="setting-row node-modules-setting-row">
        <div className="node-modules-setting-copy">
          <div className="setting-title-line">
            <strong>{copy.nodeModulesAutoInstallTitle}</strong>
            <span className={`setting-status-pill ${ready ? "success" : failedOrStopped ? "error" : running ? "working" : "muted"}`}>
              {statusText}
            </span>
          </div>
          <span>{copy.nodeModulesAutoInstallDescription}</span>
          {showProgress && (
            <div className={`node-modules-inline-progress ${state}`}>
              <div className="floating-progress-header">
                <strong>{copy.nodeModulesInstalling}</strong>
                <span>{formatPercent(percent)}</span>
              </div>
              <div className="progress-bar">
                <span style={{ width: progressWidth(percent) }} />
              </div>
              <div className="node-modules-progress-detail">{message}</div>
              {running && (
                <div className="node-modules-actions">
                  <button className="panel-button" type="button" onClick={(event) => { event.preventDefault(); onStop(); }} disabled={state === "cancelling"}>{copy.stopDownload}</button>
                  <button className="panel-button" type="button" onClick={(event) => { event.preventDefault(); onCancel(); }} disabled={state === "cancelling"}>{copy.cancelDownload}</button>
                </div>
              )}
            </div>
          )}
        </div>
        <input type="checkbox" checked={autoInstall} onChange={(event) => onToggle(event.target.checked)} />
      </label>
    </div>
  );
}

function DiagnosticLogPanel({
  copy,
  settings,
  enabled,
  onToggle,
  onExport,
}: {
  copy: Copy;
  settings: DiagnosticLogSettings | null;
  enabled: boolean;
  onToggle: (value: boolean) => void;
  onExport: () => void;
}) {
  const maxSize = formatBytes(settings?.maxTotalBytes ?? 24 * 1024 * 1024);
  const logPath = settings?.logFile || "";
  return (
    <div className="diagnostic-log-panel">
      <SettingToggle
        title={copy.saveLogsTitle}
        description={copy.saveLogsDescription(maxSize)}
        checked={enabled}
        onChange={onToggle}
      />
      <div className="project-path-row diagnostic-log-row">
        <div className="project-path-copy">
          <strong>{copy.exportLogs}</strong>
          <span>{copy.exportLogsDescription}</span>
          {logPath && <code title={logPath}>{logPath}</code>}
        </div>
        <button className="panel-button" type="button" onClick={onExport}>
          <Download size={16} />
          {copy.exportLogs}
        </button>
      </div>
    </div>
  );
}

function ConfirmDialog({
  dialog,
  onCancel,
  onConfirm,
}: {
  dialog: ConfirmDialogState | null;
  onCancel: () => void;
  onConfirm: () => void;
}) {
  if (!dialog) return null;
  return (
    <div className="modal-backdrop" role="presentation">
      <section className="confirm-dialog" role="dialog" aria-modal="true" aria-labelledby="confirm-dialog-title">
        <h2 id="confirm-dialog-title">{dialog.title}</h2>
        <p>{dialog.message}</p>
        <div className="confirm-actions">
          <button className="panel-button" type="button" autoFocus onClick={onCancel}>
            {dialog.cancelLabel}
          </button>
          <button className="panel-button primary-panel" type="button" onClick={onConfirm}>
            {dialog.confirmLabel}
          </button>
        </div>
      </section>
    </div>
  );
}

function SettingToggle(props: { title: string; description: string; checked: boolean; onChange: (value: boolean) => void }) {
  return (
    <label className="setting-row">
      <div>
        <strong>{props.title}</strong>
        <span>{props.description}</span>
      </div>
      <input type="checkbox" checked={props.checked} onChange={(event) => props.onChange(event.target.checked)} />
    </label>
  );
}

function LogoMark({ large }: { large?: boolean }) {
  return (
    <div className={large ? "logo-mark large" : "logo-mark"}>
      <img src={launcherIconUrl} alt="" />
    </div>
  );
}
