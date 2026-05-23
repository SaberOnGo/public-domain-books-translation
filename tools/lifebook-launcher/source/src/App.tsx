import { useCallback, useEffect, useMemo, useState } from "react";
import { getCurrentWindow } from "@tauri-apps/api/window";
import { disable, enable, isEnabled } from "@tauri-apps/plugin-autostart";
import {
  Apple,
  BookOpen,
  CalendarDays,
  CheckCircle2,
  ChevronDown,
  CircleOff,
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
  chooseRepoFolder,
  checkLauncherUpdates,
  checkOpenCodeUpdates,
  closeMainWindowToTray,
  downloadAndInstallLauncherUpdate,
  downloadAndOpenOpenCode,
  getLauncherState,
  launchOpenCodeClient,
  listenLauncherDownloadProgress,
  listenOpenCodeDownloadProgress,
  minimizeMainWindow,
  openBooksFolder,
  openRepoFolder,
  prepareLifeBookProject,
  toggleMainWindowMaximized,
} from "./api";
import {
  ActivityItem,
  CommitInfo,
  LauncherSettings,
  LauncherState,
  LauncherUpdateInfo,
  LifeBookUpdateInfo,
  OpenCodeUpdateInfo,
  DownloadProgress,
} from "./types";
import launcherIconUrl from "../assets/lifebook-launcher-icon.png";

const SETTINGS_KEY = "lifebook-launcher-settings";
const LAUNCHER_VERSION = "v1.3.0";

type Locale = "zh-CN" | "zh-TW" | "ja" | "en";
type TabId = "overview" | "updates" | "settings" | "logs";

const defaultSettings: LauncherSettings = {
  autoStart: false,
  checkLauncherOnLaunch: true,
  autoInstallLauncherUpdates: false,
  autoUpdateLifeBook: true,
  checkOpenCodeOnLaunch: false,
};

const zhCN = {
  knowledge: "知识 · 开放 · 共享",
  mission: "跨平台 · 开源 · 公共领域",
  projectStatus: "项目状态",
  running: "运行正常",
  networkProxy: "网络/代理",
  direct: "直连",
  proxied: "代理",
  startup: "开机自启",
  enabled: "已启用",
  disabled: "未启用",
  quickActions: "快捷操作",
  selectRepo: "选择仓库",
  openBooks: "打开成书目录",
  repoRequired: "需选择仓库",
  preparing: "准备中",
  projectReady: "项目已就绪",
  projectPath: "项目目录",
  overview: "总览",
  updates: "更新",
  settings: "设置",
  logs: "日志",
  lifeBookTitle: "LifeBook 项目",
  lifeBookSubtitle: "公共领域书籍翻译与协作系统",
  openCodeTitle: "OpenCode 客户端",
  openCodeSubtitle: "跨平台翻译协作客户端",
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
  openCodeMissing: "未检测到 OpenCode Desktop，请先安装客户端。",
  minimizeWindow: "最小化窗口",
  maximizeWindow: "最大化窗口",
  restoreWindow: "还原窗口",
  closeToTray: "关闭窗口并驻留托盘",
  settingsTitle: "设置",
  autoStartTitle: "开机自动启动 LifeBook Launcher",
  autoStartDescription: "电脑启动后自动打开 Launcher，并按下方设置检查更新。",
  checkLauncherTitle: "启动后自动检查 LifeBook Launcher 更新",
  checkLauncherDescription: "发现新版时提示确认；确认后会自动下载、安装并重启 Launcher。",
  autoInstallLauncherTitle: "发现新版 Launcher 时自动安装",
  autoInstallLauncherDescription: "开启后不再二次确认；检查到新版会自动下载、安装并重启。",
  launcherSelfUpdate: "LifeBook Launcher 自动更新",
  launcherUpdateReady: (version: string) => `发现新版 ${version}，确认后会下载、安装并自动重启。`,
  launcherNoUpdate: "当前 Launcher 已是最新版本。",
  launcherUpdateUnknown: "可手动检查 Launcher 是否有新版；发现新版后会先询问再安装。",
  installAndRestart: "下载并安装",
  autoUpdateLifeBookTitle: "自动准备并更新 LifeBook 项目",
  autoUpdateLifeBookDescription: "默认使用 D:\\LifeBook。项目不存在时自动下载；存在时自动更新。",
  changeProjectPath: "更改目录",
  checkOpenCodeTitle: "启动后自动检查 OpenCode 更新",
  checkOpenCodeDescription: "只检查版本，不会自动下载 OpenCode。",
};

type Copy = typeof zhCN;

const zhTW: Copy = {
  ...zhCN,
  knowledge: "知識 · 開放 · 共享",
  projectStatus: "專案狀態",
  networkProxy: "網路/代理",
  direct: "直連",
  startup: "開機自啟",
  quickActions: "快捷操作",
  selectRepo: "選擇倉庫",
  openBooks: "打開成書目錄",
  repoRequired: "需選擇倉庫",
  preparing: "準備中",
  projectReady: "專案已就緒",
  projectPath: "專案目錄",
  overview: "總覽",
  settings: "設定",
  logs: "日誌",
  lifeBookTitle: "LifeBook 專案",
  lifeBookSubtitle: "公共領域書籍翻譯與協作系統",
  openCodeTitle: "OpenCode 用戶端",
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
  launcherUpdateStarted: "LifeBook Launcher 更新已下載，正在自動安裝並重新啟動。",
  confirmLauncherUpdate: (version) => `將自動下載並安裝 LifeBook Launcher ${version}。安裝時目前視窗會關閉，完成後會自動重新打開。是否繼續？`,
  openCodeMissing: "未偵測到 OpenCode Desktop，請先安裝用戶端。",
  minimizeWindow: "最小化視窗",
  maximizeWindow: "最大化視窗",
  restoreWindow: "還原視窗",
  closeToTray: "關閉視窗並駐留系統列",
  settingsTitle: "設定",
  autoStartDescription: "電腦啟動後自動打開 Launcher，並按下方設定檢查更新。",
  checkLauncherTitle: "啟動後自動檢查 LifeBook Launcher 更新",
  checkLauncherDescription: "發現新版時提示確認；確認後會自動下載、安裝並重新啟動 Launcher。",
  autoInstallLauncherTitle: "發現新版 Launcher 時自動安裝",
  autoInstallLauncherDescription: "開啟後不再二次確認；檢查到新版會自動下載、安裝並重新啟動。",
  launcherSelfUpdate: "LifeBook Launcher 自動更新",
  launcherUpdateReady: (version) => `發現新版 ${version}，確認後會下載、安裝並自動重新啟動。`,
  launcherNoUpdate: "目前 Launcher 已是最新版本。",
  launcherUpdateUnknown: "可手動檢查 Launcher 是否有新版；發現新版後會先詢問再安裝。",
  installAndRestart: "下載並安裝",
  autoUpdateLifeBookTitle: "自動準備並更新 LifeBook 專案",
  autoUpdateLifeBookDescription: "預設使用 D:\\LifeBook。專案不存在時自動下載；存在時自動更新。",
  changeProjectPath: "更改目錄",
  checkOpenCodeTitle: "啟動後自動檢查 OpenCode 更新",
  checkOpenCodeDescription: "只檢查版本，不會自動下載 OpenCode。",
};

const ja: Copy = {
  ...zhCN,
  knowledge: "知識 · オープン · 共有",
  projectStatus: "状態",
  running: "正常",
  networkProxy: "ネットワーク/プロキシ",
  direct: "直結",
  proxied: "プロキシ",
  startup: "自動起動",
  enabled: "有効",
  disabled: "無効",
  quickActions: "クイック操作",
  selectRepo: "リポジトリ選択",
  openBooks: "出力フォルダ",
  repoRequired: "選択が必要",
  preparing: "準備中",
  projectReady: "準備完了",
  projectPath: "プロジェクトフォルダ",
  overview: "概要",
  updates: "更新",
  settings: "設定",
  logs: "ログ",
  lifeBookTitle: "LifeBook プロジェクト",
  lifeBookSubtitle: "公共領域書籍の翻訳と協作システム",
  openCodeTitle: "OpenCode クライアント",
  openCodeSubtitle: "クロスプラットフォーム翻訳協作クライアント",
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
  launcherUpdateStarted: "LifeBook Launcher 更新をダウンロードしました。自動インストールして再起動します。",
  confirmLauncherUpdate: (version) => `LifeBook Launcher ${version} を自動ダウンロードしてインストールします。インストール中は現在のウィンドウを閉じ、完了後に自動で開きます。続行しますか？`,
  openCodeMissing: "OpenCode Desktop が見つかりません。先にクライアントをインストールしてください。",
  minimizeWindow: "最小化",
  maximizeWindow: "最大化",
  restoreWindow: "元に戻す",
  closeToTray: "閉じてトレイに常駐",
  settingsTitle: "設定",
  autoStartTitle: "LifeBook Launcher を自動起動",
  autoStartDescription: "PC 起動時に Launcher を開き、設定に従って更新を確認します。",
  checkLauncherTitle: "起動時に LifeBook Launcher 更新を確認",
  checkLauncherDescription: "新バージョンがあれば確認後に自動ダウンロード、インストール、再起動します。",
  autoInstallLauncherTitle: "新しい Launcher を自動インストール",
  autoInstallLauncherDescription: "有効にすると確認なしでダウンロード、インストール、再起動します。",
  launcherSelfUpdate: "LifeBook Launcher 自動更新",
  launcherUpdateReady: (version) => `新バージョン ${version} があります。確認後にダウンロード、インストール、自動再起動します。`,
  launcherNoUpdate: "現在の Launcher は最新です。",
  launcherUpdateUnknown: "手動で Launcher の更新を確認できます。新バージョンがあれば確認してからインストールします。",
  installAndRestart: "ダウンロードしてインストール",
  autoUpdateLifeBookTitle: "LifeBook プロジェクトを自動準備/更新",
  autoUpdateLifeBookDescription: "既定は D:\\LifeBook。なければ自動ダウンロードし、あれば自動更新します。",
  changeProjectPath: "フォルダ変更",
  checkOpenCodeTitle: "起動時に OpenCode 更新を確認",
  checkOpenCodeDescription: "バージョン確認のみで、自動ダウンロードはしません。",
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
  startup: "Startup",
  enabled: "Enabled",
  disabled: "Disabled",
  quickActions: "Quick actions",
  selectRepo: "Select repo",
  openBooks: "Open books",
  repoRequired: "Repo needed",
  preparing: "Preparing",
  projectReady: "Project ready",
  projectPath: "Project folder",
  overview: "Overview",
  updates: "Updates",
  settings: "Settings",
  logs: "Logs",
  lifeBookTitle: "LifeBook Project",
  lifeBookSubtitle: "Public-domain book translation workflow",
  openCodeTitle: "OpenCode Client",
  openCodeSubtitle: "Cross-platform translation agent client",
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
  launcherUpdateStarted: "LifeBook Launcher update downloaded. Installing and restarting automatically.",
  confirmLauncherUpdate: (version) => `Download and install LifeBook Launcher ${version} automatically? The current window will close during install and reopen after it finishes.`,
  openCodeMissing: "OpenCode Desktop was not detected. Install the client first.",
  minimizeWindow: "Minimize window",
  maximizeWindow: "Maximize window",
  restoreWindow: "Restore window",
  closeToTray: "Close window to tray",
  settingsTitle: "Settings",
  autoStartTitle: "Start LifeBook Launcher with the computer",
  autoStartDescription: "Open Launcher after boot and check updates according to the settings below.",
  checkLauncherTitle: "Check LifeBook Launcher updates on launch",
  checkLauncherDescription: "When a new version is found, confirm once, then download, install, and restart automatically.",
  autoInstallLauncherTitle: "Install new Launcher versions automatically",
  autoInstallLauncherDescription: "When enabled, a detected Launcher update downloads, installs, and restarts without another prompt.",
  launcherSelfUpdate: "LifeBook Launcher auto-update",
  launcherUpdateReady: (version) => `Version ${version} is available. After confirmation, Launcher will download, install, and restart automatically.`,
  launcherNoUpdate: "This Launcher is already up to date.",
  launcherUpdateUnknown: "You can check Launcher updates manually. A new version will ask before installing.",
  installAndRestart: "Download and install",
  autoUpdateLifeBookTitle: "Prepare and update LifeBook automatically",
  autoUpdateLifeBookDescription: "Defaults to D:\\LifeBook. Downloads the project when missing and updates it when present.",
  changeProjectPath: "Change folder",
  checkOpenCodeTitle: "Check OpenCode updates on launch",
  checkOpenCodeDescription: "Only checks the version. It will not download automatically.",
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
  if (!value) return "";
  return `${(value / 1024 / 1024).toFixed(1)} MB`;
}

function formatDownloadProgress(copy: Copy, progress?: DownloadProgress | null) {
  if (!progress) return "";
  const total = progress.totalBytes ? ` / ${formatBytes(progress.totalBytes)}` : "";
  return `${copy.downloading} ${progress.percent}% (${formatBytes(progress.downloadedBytes)}${total})`;
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
  const [lifeBookUpdate, setLifeBookUpdate] = useState<LifeBookUpdateInfo | null>(null);
  const [openCodeUpdate, setOpenCodeUpdate] = useState<OpenCodeUpdateInfo | null>(null);
  const [settings, setSettings] = useState<LauncherSettings>(loadSettings);
  const [busy, setBusy] = useState<string | null>(null);
  const [lifeBookPreparing, setLifeBookPreparing] = useState(false);
  const [openCodeProgress, setOpenCodeProgress] = useState<DownloadProgress | null>(null);
  const [launcherProgress, setLauncherProgress] = useState<DownloadProgress | null>(null);
  const [showAllCommits, setShowAllCommits] = useState(false);
  const [quickActionsOpen, setQuickActionsOpen] = useState(false);
  const [isMaximized, setIsMaximized] = useState(false);
  const [activities, setActivities] = useState<ActivityItem[]>([
    { id: "welcome", time: nowLabel(), level: "info", message: copy.welcome },
  ]);

  const addActivity = useCallback((level: ActivityItem["level"], message: string) => {
    setActivities((items) => [
      { id: `${Date.now()}-${Math.random()}`, time: nowLabel(), level, message },
      ...items,
    ].slice(0, 80));
  }, []);

  const refreshState = useCallback(async () => {
    try {
      setState(await getLauncherState());
    } catch (error) {
      setState(null);
      addActivity("error", String(error));
    }
  }, [addActivity]);

  const chooseRepo = useCallback(async () => {
    setBusy("repo-choose");
    try {
      const result = await chooseRepoFolder();
      addActivity(result.ok ? "success" : "info", result.message);
      if (result.ok) {
        await refreshState();
        setLifeBookPreparing(true);
        addActivity("info", copy.preparingLifeBook);
        try {
          const info = await prepareLifeBookProject();
          setLifeBookUpdate(info);
          addActivity("success", copy.lifeBookReady);
        } catch (error) {
          addActivity("warning", copy.lifeBookUpdateStopped(String(error)));
        } finally {
          setLifeBookPreparing(false);
        }
        await refreshState();
      }
    } catch (error) {
      addActivity("error", String(error));
    } finally {
      setBusy(null);
    }
  }, [addActivity, copy, refreshState]);

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
    setLifeBookPreparing(true);
    addActivity("info", copy.preparingLifeBook);
    try {
      const info = await prepareLifeBookProject();
      setLifeBookUpdate(info);
      addActivity("success", copy.lifeBookReady);
      await refreshState();
    } catch (error) {
      addActivity("error", copy.lifeBookUpdateStopped(String(error)));
      await refreshState();
    } finally {
      setLifeBookPreparing(false);
    }
  }, [addActivity, copy, refreshState]);

  const doUpdateLauncher = useCallback(async (knownUpdate?: LauncherUpdateInfo | null, skipConfirm = false) => {
    const info = knownUpdate ?? launcherUpdate;
    const version = info?.latestVersion ?? "";
    if (!skipConfirm && !window.confirm(copy.confirmLauncherUpdate(version))) {
      return;
    }
    setBusy("launcher-update");
    setLauncherProgress({ percent: 0, downloadedBytes: 0, totalBytes: info?.assetSize ?? 0 });
    try {
      const result = await downloadAndInstallLauncherUpdate();
      addActivity(result.ok ? "success" : "warning", result.message || copy.launcherUpdateStarted);
    } catch (error) {
      addActivity("error", copy.launcherUpdateFailed(String(error)));
    } finally {
      setBusy(null);
    }
  }, [addActivity, copy, launcherUpdate]);

  const checkLauncher = useCallback(async (promptWhenUpdate = false, background = false) => {
    if (!background) setBusy("launcher-check");
    addActivity("info", copy.checkingLauncher);
    try {
      const info = await checkLauncherUpdates();
      setLauncherUpdate(info);
      addActivity(info.hasUpdate ? "warning" : "success", info.hasUpdate ? copy.launcherFound(info.latestVersion) : copy.launcherLatest);
      if (promptWhenUpdate && info.hasUpdate) {
        await doUpdateLauncher(info, settings.autoInstallLauncherUpdates);
      }
    } catch (error) {
      addActivity("error", copy.launcherCheckFailed(String(error)));
    } finally {
      if (!background) setBusy((value) => (value === "launcher-check" ? null : value));
    }
  }, [addActivity, copy, doUpdateLauncher, settings.autoInstallLauncherUpdates]);

  const checkOpenCode = useCallback(async (background = false) => {
    if (!background) setBusy("opencode-check");
    addActivity("info", copy.checkingOpenCode);
    try {
      const info = await checkOpenCodeUpdates();
      setOpenCodeUpdate(info);
      addActivity(info.hasUpdate ? "warning" : "success", info.hasUpdate ? copy.openCodeFound(info.latestVersion) : copy.openCodeLatest);
    } catch (error) {
      addActivity("error", copy.openCodeCheckFailed(String(error)));
    } finally {
      if (!background) setBusy(null);
    }
  }, [addActivity, copy]);

  const doUpdateOpenCode = useCallback(async () => {
    if (!window.confirm(copy.confirmOpenCodeUpdate)) {
      return;
    }
    setBusy("opencode-update");
    setOpenCodeProgress({ percent: 0, downloadedBytes: 0, totalBytes: openCodeUpdate?.assetSize ?? 0 });
    try {
      const result = await downloadAndOpenOpenCode();
      addActivity(result.ok ? "success" : "warning", result.message || copy.openCodeInstallerOpened);
      await refreshState();
      await checkOpenCode();
    } catch (error) {
      addActivity("error", copy.openCodeUpdateFailed(String(error)));
    } finally {
      setBusy(null);
    }
  }, [addActivity, checkOpenCode, copy, openCodeUpdate, refreshState]);

  const doLaunchOpenCode = useCallback(async () => {
    setBusy("opencode-launch");
    try {
      const result = await launchOpenCodeClient();
      addActivity(result.ok ? "success" : "warning", result.message);
    } catch (error) {
      addActivity("error", copy.clientLaunchFailed(String(error)));
    } finally {
      setBusy(null);
    }
  }, [addActivity, copy]);

  const updateSetting = useCallback(
    async (key: keyof LauncherSettings, value: boolean) => {
      const next = { ...settings, [key]: value };
      setSettings(next);
      saveSettings(next);
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
    [addActivity, copy, settings],
  );

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
    refreshState();
    isEnabled()
      .then((enabled) => {
        setSettings((old) => {
          const next = { ...old, autoStart: enabled };
          saveSettings(next);
          return next;
        });
      })
      .catch(() => undefined);

    const unlistenOpenCode = listenOpenCodeDownloadProgress((progress) => {
      setOpenCodeProgress(progress);
    });
    const unlistenLauncher = listenLauncherDownloadProgress((progress) => {
      setLauncherProgress(progress);
    });
    return () => {
      unlistenOpenCode.then((fn) => fn()).catch(() => undefined);
      unlistenLauncher.then((fn) => fn()).catch(() => undefined);
    };
  }, [refreshState]);

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
    const timer = window.setTimeout(() => {
      if (settings.autoUpdateLifeBook) void prepareLifeBook();
      if (settings.checkLauncherOnLaunch) void checkLauncher(true, true);
      if (settings.checkOpenCodeOnLaunch) void checkOpenCode(true);
    }, 600);
    return () => window.clearTimeout(timer);
    // Startup automation should run once after first paint using the initial persisted settings.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const commits = lifeBookUpdate?.commits ?? [];
  const displayedCommits = showAllCommits ? commits : commits.slice(0, 1);
  const firstCommit = commits[0];
  const repoReady = Boolean(state?.repoReady);
  const latestLifeBookVersion = firstCommit ? versionFromDate(firstCommit.date) : repoReady ? copy.projectReady : copy.preparing;
  const currentLifeBookVersion = repoReady
    ? state?.localCommitShort === "preview"
      ? "v2025.05.25"
      : state?.localCommitShort || copy.projectReady
    : lifeBookPreparing
      ? copy.preparing
      : copy.repoRequired;
  const lifeBookStatus = lifeBookPreparing ? copy.preparing : repoReady ? copy.projectReady : copy.repoRequired;
  const lifeBookStatusTone: "success" | "warning" | "muted" = lifeBookPreparing ? "warning" : repoReady ? "success" : "muted";
  const openCodeAvailable = Boolean(state?.opencodeAvailable || openCodeUpdate?.clientAvailable);
  const openCodeInstalledVersion = openCodeUpdate?.installedVersion ?? state?.opencodeInstalledVersion ?? null;
  const openCodeCurrent = openCodeAvailable ? openCodeInstalledVersion ?? copy.installed : copy.notInstalled;
  const openCodeLatest = openCodeUpdate?.latestVersion ?? (openCodeInstalledVersion ?? copy.checking);
  const openCodeHasUpdate = Boolean(openCodeUpdate?.hasUpdate);
  const openCodeStatus = openCodeAvailable ? (openCodeHasUpdate ? copy.updateAvailable : copy.upToDate) : copy.notInstalled;
  const openCodePrimaryLabel = openCodeAvailable ? (openCodeHasUpdate ? copy.updateNow : copy.checkUpdates) : copy.installClient;
  const openCodePrimaryIcon = openCodeAvailable ? (openCodeHasUpdate ? Download : RefreshCcw) : Download;
  const openCodeVisibleProgress = busy === "opencode-update" ? openCodeProgress : null;
  const launcherVisibleProgress = busy === "launcher-update" ? launcherProgress : null;
  const openCodeProgressLabel = formatDownloadProgress(copy, openCodeVisibleProgress);
  const launcherProgressLabel = formatDownloadProgress(copy, launcherVisibleProgress);

  const visibleActivities = useMemo(() => activities.slice(0, 5), [activities]);

  return (
    <div className={isMaximized ? "launcher-frame maximized" : "launcher-frame"}>
      <header className="frame-titlebar">
        <div className="titlebar-brand" data-tauri-drag-region>
          <LogoMark />
          <span>LifeBook Launcher</span>
        </div>
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
            <NavButton icon={RefreshCcw} label={copy.updates} active={activeTab === "updates"} onClick={() => setActiveTab("updates")} />
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
              void checkOpenCode();
            }}
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
                  latestUpdated={commitDate(firstCommit)}
                  primaryLabel={copy.openBooks}
                  primaryIcon={FolderOpen}
                  secondaryLabel={copy.viewProject}
                  secondaryIcon={FolderOpen}
                  busy={busy === "repo-choose"}
                  busyText={copy.working}
                  onPrimary={doOpenBooksFolder}
                  onSecondary={doOpenRepoFolder}
                  onMore={chooseRepo}
                  moreLabel={copy.changeProjectPath}
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
                  secondaryLabel={openCodeAvailable ? copy.launchClient : copy.clientNotInstalled}
                  secondaryIcon={openCodeAvailable ? Play : CircleOff}
                  secondaryTone={openCodeAvailable ? "green" : "muted"}
                  secondaryDisabled={!openCodeAvailable}
                  busy={busy === "opencode-check" || busy === "opencode-update" || busy === "opencode-launch"}
                  busyText={openCodeProgressLabel || copy.working}
                  progress={openCodeVisibleProgress}
                  progressLabel={openCodeProgressLabel}
                  onPrimary={openCodeAvailable ? (openCodeHasUpdate ? doUpdateOpenCode : checkOpenCode) : doUpdateOpenCode}
                  onSecondary={doLaunchOpenCode}
                  onMore={checkOpenCode}
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
                onToggleShowAll={() => setShowAllCommits((value) => !value)}
              />
              <ActivityTable copy={copy} activities={visibleActivities} onViewFullLog={() => setActiveTab("logs")} />
            </>
          )}

          {activeTab === "settings" && (
            <section className="settings-panel">
              <PanelHeading title={copy.settingsTitle} />
              <SettingToggle title={copy.autoStartTitle} description={copy.autoStartDescription} checked={settings.autoStart} onChange={(value) => updateSetting("autoStart", value)} />
              <ProjectPathPanel copy={copy} path={state?.repoRoot || "D:\\LifeBook"} onChange={() => void chooseRepo()} />
              <SettingToggle title={copy.autoUpdateLifeBookTitle} description={copy.autoUpdateLifeBookDescription} checked={settings.autoUpdateLifeBook} onChange={(value) => updateSetting("autoUpdateLifeBook", value)} />
              <SettingToggle title={copy.checkLauncherTitle} description={copy.checkLauncherDescription} checked={settings.checkLauncherOnLaunch} onChange={(value) => updateSetting("checkLauncherOnLaunch", value)} />
              <SettingToggle title={copy.autoInstallLauncherTitle} description={copy.autoInstallLauncherDescription} checked={settings.autoInstallLauncherUpdates} onChange={(value) => updateSetting("autoInstallLauncherUpdates", value)} />
              <LauncherUpdatePanel
                copy={copy}
                update={launcherUpdate}
                progress={launcherVisibleProgress}
                progressLabel={launcherProgressLabel}
                busy={busy === "launcher-check" || busy === "launcher-update"}
                onCheck={() => void checkLauncher(false)}
                onUpdate={() => void doUpdateLauncher()}
              />
              <SettingToggle title={copy.checkOpenCodeTitle} description={copy.checkOpenCodeDescription} checked={settings.checkOpenCodeOnLaunch} onChange={(value) => updateSetting("checkOpenCodeOnLaunch", value)} />
            </section>
          )}

          {activeTab === "logs" && <ActivityTable copy={copy} activities={activities.slice(0, 12)} expanded onViewFullLog={() => undefined} />}
        </section>
      </main>
    </div>
  );
}

function StatusBar({
  copy,
  proxyConfigured,
  autoStart,
  projectReady,
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
      <StatusItem label={copy.projectStatus} icon={CheckCircle2} value={projectReady ? copy.running : copy.repoRequired} tone={projectReady ? "green" : "blue"} />
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
            <button type="button" onClick={onOpenBooks}>{copy.openBooks}</button>
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

function NavButton({ icon: Icon, label, active, onClick }: { icon: LucideIcon; label: string; active: boolean; onClick: () => void }) {
  return (
    <button className={active ? "nav-item active" : "nav-item"} onClick={onClick}>
      <Icon size={24} strokeWidth={1.9} />
      <span>{label}</span>
    </button>
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
  busy: boolean;
  busyText: string;
  onPrimary: () => void;
  onSecondary: () => void;
  onMore: () => void;
  moreLabel: string;
  copy: Copy;
}) {
  const Icon = props.icon;
  const PrimaryIcon = props.primaryIcon;
  const SecondaryIcon = props.secondaryIcon;
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
        <button className={`secondary ${props.secondaryTone ?? "default"}`} disabled={props.secondaryDisabled || props.busy} onClick={props.onSecondary}>
          <SecondaryIcon size={21} />
          {props.secondaryLabel}
        </button>
        <button className="icon-button" type="button" aria-label={props.moreLabel} title={props.moreLabel} onClick={props.onMore}>
          <MoreHorizontal size={22} />
        </button>
      </div>
      {props.progress && (
        <div className="progress-strip" aria-label={props.progressLabel}>
          <div className="progress-bar">
            <span style={{ width: `${props.progress.percent}%` }} />
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

function CommitTable({
  copy,
  commits,
  totalCount,
  latestVersion,
  showAll,
  onToggleShowAll,
}: {
  copy: Copy;
  commits: CommitInfo[];
  totalCount: number;
  latestVersion: string;
  showAll: boolean;
  onToggleShowAll: () => void;
}) {
  return (
    <section className="data-panel commit-panel">
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
              {commits.map((commit, index) => (
                <tr key={`${commit.hash}-${commit.date}`}>
                  <td><RowIcon index={index} />{commit.date.slice(0, 16).replace("T", " ")}</td>
                  <td><code>{commit.hash}</code></td>
                  <td>{commit.title}</td>
                  <td>{commit.summary || copy.noCommits}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="table-empty">{copy.noCommits}</div>
        )}
      </div>
    </section>
  );
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

function LauncherUpdatePanel({
  copy,
  update,
  progress,
  progressLabel,
  busy,
  onCheck,
  onUpdate,
}: {
  copy: Copy;
  update: LauncherUpdateInfo | null;
  progress?: DownloadProgress | null;
  progressLabel: string;
  busy: boolean;
  onCheck: () => void;
  onUpdate: () => void;
}) {
  const description = update?.hasUpdate
    ? copy.launcherUpdateReady(update.latestVersion)
    : update
      ? copy.launcherNoUpdate
      : copy.launcherUpdateUnknown;

  return (
    <div className="launcher-update-row">
      <div className="launcher-update-copy">
        <strong>{copy.launcherSelfUpdate}</strong>
        <span>{description}</span>
        {progress && (
          <div className="progress-strip compact" aria-label={progressLabel}>
            <div className="progress-bar">
              <span style={{ width: `${progress.percent}%` }} />
            </div>
            <strong>{progressLabel}</strong>
          </div>
        )}
      </div>
      <div className="launcher-update-actions">
        <button className="panel-button" type="button" disabled={busy} onClick={onCheck}>
          <RefreshCcw size={16} />
          {copy.checkUpdates}
        </button>
        <button className="panel-button primary-panel" type="button" disabled={busy || !update?.hasUpdate} onClick={onUpdate}>
          <Download size={16} />
          {copy.installAndRestart}
        </button>
      </div>
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
