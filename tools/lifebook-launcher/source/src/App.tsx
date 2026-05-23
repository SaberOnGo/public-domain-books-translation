import { useCallback, useEffect, useMemo, useRef, useState, type MouseEvent } from "react";
import { getCurrentWindow } from "@tauri-apps/api/window";
import { disable, enable, isEnabled } from "@tauri-apps/plugin-autostart";
import {
  Apple,
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
  cancelOpenCodeDownload,
  chooseRepoFolder,
  checkLauncherUpdates,
  checkOpenCodeLocalStatus,
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
  readProjectDocument,
  readProjectDocumentPath,
  setRepoFolder,
  syncLifeBookProject,
  toggleMainWindowMaximized,
} from "./api";
import {
  ActivityItem,
  CommitInfo,
  LauncherSettings,
  LauncherState,
  LauncherUpdateInfo,
  LifeBookUpdateInfo,
  OpenCodeLocalStatus,
  OpenCodeUpdateInfo,
  DownloadProgress,
  ProjectDocument,
} from "./types";
import launcherIconUrl from "../assets/lifebook-launcher-icon.png";

const SETTINGS_KEY = "lifebook-launcher-settings";
const LAUNCHER_VERSION = "v1.3.0";

type Locale = "zh-CN" | "zh-TW" | "ja" | "en";
type TabId = "overview" | "updates" | "tutorial" | "settings" | "logs";
type TutorialKind = "readme" | "howto";
type ToastTone = "info" | "success" | "warning" | "error";
type FloatingToast = { id: number; message: string; tone: ToastTone };
type DownloadHudState = "idle" | "downloading" | "cancelling" | "stopped" | "failed";
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
  tutorial: "教程",
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
  clientLaunching: "正在启动",
  clientLaunchSucceeded: "启动成功",
  tutorialTitle: "教程",
  tutorialReadme: "README",
  tutorialHowTo: "How to use",
  tutorialCurrentDocument: "当前文档",
  tutorialLoading: "正在加载教程...",
  tutorialLoadFailed: (error: string) => `教程加载失败：${error}`,
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
  checkLauncherTitle: "自动检测更新 Launcher",
  checkLauncherDescription: "启动后自动检测新版；发现更新会显示悬浮下载进度，自动安装并重启。失败后下次启动会再试。",
  changeProjectPath: "更改目录",
  confirmProjectDirectoryTitle: "确认 LifeBook 项目目录",
  confirmProjectDirectoryDownload: (path: string) => `将在此目录准备 LifeBook 项目：\n${path}\n\n如果目录为空，会重新下载 LifeBook。非空且不是 LifeBook 项目的目录会被拒绝。是否继续？`,
  confirmProjectDirectoryUse: (path: string) => `将切换到此 LifeBook 项目目录：\n${path}\n\n切换后会检查并更新项目。是否继续？`,
  projectDirectoryChangeCancelled: "已取消更改 LifeBook 项目目录。",
  checkOpenCodeTitle: "自动检测更新 OpenCode",
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
  tutorial: "教程",
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
  clientLaunching: "正在啟動",
  clientLaunchSucceeded: "啟動成功",
  tutorialLoading: "正在載入教程...",
  tutorialLoadFailed: (error) => `教程載入失敗：${error}`,
  launcherUpdateStarted: "LifeBook Launcher 更新已下載，正在自動安裝並重新啟動。",
  confirmLauncherUpdate: (version) => `將自動下載並安裝 LifeBook Launcher ${version}。安裝時目前視窗會關閉，完成後會自動重新打開。是否繼續？`,
  openCodeMissing: "未偵測到 OpenCode Desktop，請先安裝用戶端。",
  minimizeWindow: "最小化視窗",
  maximizeWindow: "最大化視窗",
  restoreWindow: "還原視窗",
  closeToTray: "關閉視窗並駐留系統列",
  settingsTitle: "設定",
  autoStartDescription: "電腦啟動後自動打開 Launcher，並按下方設定檢查更新。",
  checkLauncherTitle: "自動偵測更新 Launcher",
  checkLauncherDescription: "啟動後自動偵測新版；發現更新會顯示浮動下載進度，自動安裝並重新啟動。失敗後下次啟動會再試。",
  changeProjectPath: "更改目錄",
  confirmProjectDirectoryTitle: "確認 LifeBook 專案目錄",
  confirmProjectDirectoryDownload: (path) => `將在此目錄準備 LifeBook 專案：\n${path}\n\n如果目錄為空，會重新下載 LifeBook。非空且不是 LifeBook 專案的目錄會被拒絕。是否繼續？`,
  confirmProjectDirectoryUse: (path) => `將切換到此 LifeBook 專案目錄：\n${path}\n\n切換後會檢查並更新專案。是否繼續？`,
  projectDirectoryChangeCancelled: "已取消更改 LifeBook 專案目錄。",
  checkOpenCodeTitle: "自動偵測更新 OpenCode",
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
  tutorial: "ガイド",
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
  clientLaunching: "起動中",
  clientLaunchSucceeded: "起動成功",
  tutorialTitle: "ガイド",
  tutorialLoading: "ガイドを読み込み中...",
  tutorialLoadFailed: (error) => `ガイドの読み込みに失敗：${error}`,
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
  checkLauncherTitle: "Launcher 更新を自動確認",
  checkLauncherDescription: "起動後に新バージョンを確認し、更新があれば浮動進行状況を表示して自動インストール、再起動します。失敗時は次回起動時に再試行します。",
  changeProjectPath: "フォルダ変更",
  confirmProjectDirectoryTitle: "LifeBook プロジェクトフォルダの確認",
  confirmProjectDirectoryDownload: (path) => `このフォルダに LifeBook プロジェクトを準備します：\n${path}\n\n空フォルダの場合は LifeBook を再ダウンロードします。空でなく LifeBook プロジェクトでもないフォルダは拒否されます。続行しますか？`,
  confirmProjectDirectoryUse: (path) => `この LifeBook プロジェクトフォルダに切り替えます：\n${path}\n\n切り替え後、プロジェクトを確認して更新します。続行しますか？`,
  projectDirectoryChangeCancelled: "LifeBook プロジェクトフォルダの変更をキャンセルしました。",
  checkOpenCodeTitle: "OpenCode 更新を自動確認",
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
  tutorial: "Guide",
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
  clientLaunching: "Launching",
  clientLaunchSucceeded: "Launch succeeded",
  tutorialTitle: "Guide",
  tutorialCurrentDocument: "Current document",
  tutorialLoading: "Loading guide...",
  tutorialLoadFailed: (error) => `Guide failed to load: ${error}`,
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
  checkLauncherTitle: "Auto-check Launcher updates",
  checkLauncherDescription: "After launch, check for a new Launcher version. If found, show floating download progress, install, and restart automatically. Failed attempts retry on next launch.",
  changeProjectPath: "Change folder",
  confirmProjectDirectoryTitle: "Confirm LifeBook project folder",
  confirmProjectDirectoryDownload: (path) => `LifeBook will be prepared in this folder:\n${path}\n\nIf the folder is empty, LifeBook will be downloaded again. A non-empty folder that is not a LifeBook project will be rejected. Continue?`,
  confirmProjectDirectoryUse: (path) => `Switch to this LifeBook project folder:\n${path}\n\nAfter switching, Launcher will check and update the project. Continue?`,
  projectDirectoryChangeCancelled: "LifeBook project folder change cancelled.",
  checkOpenCodeTitle: "Auto-check OpenCode updates",
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
  if (!value) return "0 MB";
  return `${(value / 1024 / 1024).toFixed(1)} MB`;
}

function formatDownloadProgress(copy: Copy, progress?: DownloadProgress | null) {
  if (!progress) return "";
  const total = progress.totalBytes ? ` / ${formatBytes(progress.totalBytes)}` : "";
  return `${copy.downloading} ${progress.percent}% (${formatBytes(progress.downloadedBytes)}${total})`;
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
  const [lifeBookUpdate, setLifeBookUpdate] = useState<LifeBookUpdateInfo | null>(null);
  const [openCodeUpdate, setOpenCodeUpdate] = useState<OpenCodeUpdateInfo | null>(null);
  const [openCodeLocalStatus, setOpenCodeLocalStatus] = useState<OpenCodeLocalStatus | null>(null);
  const [tutorialKind, setTutorialKind] = useState<TutorialKind>("readme");
  const [tutorialDoc, setTutorialDoc] = useState<ProjectDocument | null>(null);
  const [tutorialLoading, setTutorialLoading] = useState(false);
  const [settings, setSettings] = useState<LauncherSettings>(loadSettings);
  const [busy, setBusy] = useState<string | null>(null);
  const [refreshInProgress, setRefreshInProgress] = useState(false);
  const [globalProgress, setGlobalProgress] = useState<{ percent: number; label: string } | null>(null);
  const [lifeBookPreparing, setLifeBookPreparing] = useState(false);
  const [lifeBookSyncing, setLifeBookSyncing] = useState(false);
  const [openCodeProgress, setOpenCodeProgress] = useState<DownloadProgress | null>(null);
  const [openCodeSyntheticProgress, setOpenCodeSyntheticProgress] = useState<DownloadProgress | null>(null);
  const [openCodeLaunchState, setOpenCodeLaunchState] = useState<"idle" | "starting" | "success">("idle");
  const [openCodeDownloadState, setOpenCodeDownloadState] = useState<DownloadHudState>("idle");
  const [openCodeDownloadMessage, setOpenCodeDownloadMessage] = useState<string | null>(null);
  const [openCodeDownloadDismissed, setOpenCodeDownloadDismissed] = useState(false);
  const [launcherProgress, setLauncherProgress] = useState<DownloadProgress | null>(null);
  const [showAllCommits, setShowAllCommits] = useState(false);
  const [quickActionsOpen, setQuickActionsOpen] = useState(false);
  const [isMaximized, setIsMaximized] = useState(false);
  const [floatingToast, setFloatingToast] = useState<FloatingToast | null>(null);
  const [confirmDialog, setConfirmDialog] = useState<ConfirmDialogState | null>(null);
  const [activities, setActivities] = useState<ActivityItem[]>([
    { id: "welcome", time: nowLabel(), level: "info", message: copy.welcome },
  ]);
  const openCodeDownloadStartedAt = useRef<number | null>(null);
  const openCodeLaunchResetTimer = useRef<number | null>(null);
  const refreshInProgressRef = useRef(false);
  const lifeBookSyncingRef = useRef(false);
  const launcherCheckInProgressRef = useRef(false);
  const launcherUpdateInProgressRef = useRef(false);
  const openCodeCheckInProgressRef = useRef(false);
  const openCodeUpdateInProgressRef = useRef(false);
  const openCodeDownloadDismissedRef = useRef(false);
  const floatingToastTimer = useRef<number | null>(null);

  const addActivity = useCallback((level: ActivityItem["level"], message: string) => {
    setActivities((items) => [
      { id: `${Date.now()}-${Math.random()}`, time: nowLabel(), level, message },
      ...items,
    ].slice(0, 80));
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
        await refreshState();
        if (lifeBookSyncingRef.current) return;
        lifeBookSyncingRef.current = true;
        setLifeBookPreparing(true);
        addActivity("info", copy.preparingLifeBook);
        try {
          const info = await prepareLifeBookProject(locale);
          setLifeBookUpdate(info);
          addActivity("success", copy.lifeBookReady);
        } catch (error) {
          addActivity("warning", copy.lifeBookUpdateStopped(String(error)));
        } finally {
          lifeBookSyncingRef.current = false;
          setLifeBookPreparing(false);
        }
        await refreshState();
      }
    } catch (error) {
      addActivity("error", String(error));
    } finally {
      setBusy(null);
    }
  }, [addActivity, askConfirm, copy, locale, refreshState]);

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
    addActivity("info", copy.preparingLifeBook);
    try {
      const info = await prepareLifeBookProject(locale);
      setLifeBookUpdate(info);
      addActivity("success", copy.lifeBookReady);
      await refreshState();
    } catch (error) {
      addActivity("error", copy.lifeBookUpdateStopped(String(error)));
      await refreshState();
    } finally {
      lifeBookSyncingRef.current = false;
      setLifeBookPreparing(false);
    }
  }, [addActivity, copy, locale, refreshState]);

  const prepareLifeBookInBackground = useCallback(async () => {
    if (lifeBookSyncingRef.current) return;
    lifeBookSyncingRef.current = true;
    addActivity("info", copy.preparingLifeBook);
    try {
      const info = await prepareLifeBookProject(locale);
      setLifeBookUpdate(info);
      addActivity("success", copy.lifeBookReady);
      await refreshState();
    } catch (error) {
      addActivity("warning", copy.lifeBookUpdateStopped(String(error)));
      await refreshState();
    } finally {
      lifeBookSyncingRef.current = false;
    }
  }, [addActivity, copy, locale, refreshState]);

  const syncLifeBookNow = useCallback(async () => {
    if (lifeBookSyncingRef.current) return;
    lifeBookSyncingRef.current = true;
    setLifeBookSyncing(true);
    addActivity("info", copy.lifeBookUpdateStarted);
    setGlobalProgress({ percent: 8, label: copy.refreshLifeBookStep });
    let syntheticPercent = 8;
    const progressTimer = window.setInterval(() => {
      syntheticPercent = Math.min(92, syntheticPercent + 7);
      setGlobalProgress((current) => {
        if (!current || current.label !== copy.refreshLifeBookStep) return current;
        return { ...current, percent: Math.max(current.percent, syntheticPercent) };
      });
    }, 700);
    try {
      const info = await syncLifeBookProject(locale);
      setLifeBookUpdate(info);
      const doneMessage = info.hasUpdate ? copy.lifeBookFound(info.behindCount) : copy.lifeBookUpdateComplete;
      setGlobalProgress({ percent: 100, label: doneMessage });
      addActivity(info.hasUpdate ? "warning" : "success", doneMessage);
      await refreshState();
    } catch (error) {
      addActivity("error", copy.lifeBookUpdateStopped(String(error)));
      await refreshState();
    } finally {
      window.clearInterval(progressTimer);
      window.setTimeout(() => setGlobalProgress(null), 900);
      lifeBookSyncingRef.current = false;
      setLifeBookSyncing(false);
    }
  }, [addActivity, copy, locale, refreshState]);

  const doUpdateLauncher = useCallback(async (knownUpdate?: LauncherUpdateInfo | null, skipConfirm = false) => {
    if (launcherUpdateInProgressRef.current) return;
    launcherUpdateInProgressRef.current = true;
    const info = knownUpdate ?? launcherUpdate;
    const version = info?.latestVersion ?? "";
    if (!skipConfirm && !window.confirm(copy.confirmLauncherUpdate(version))) {
      launcherUpdateInProgressRef.current = false;
      return;
    }
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
  }, [addActivity, copy, launcherUpdate]);

  const checkLauncher = useCallback(async (promptWhenUpdate = false, background = false) => {
    if (launcherCheckInProgressRef.current) return;
    launcherCheckInProgressRef.current = true;
    if (!background) setBusy("launcher-check");
    addActivity("info", copy.checkingLauncher);
    try {
      const info = await checkLauncherUpdates();
      setLauncherUpdate(info);
      addActivity(info.hasUpdate ? "warning" : "success", info.hasUpdate ? copy.launcherFound(info.latestVersion) : copy.launcherLatest);
      if (promptWhenUpdate && info.hasUpdate) {
        await doUpdateLauncher(info, true);
      }
    } catch (error) {
      addActivity("error", copy.launcherCheckFailed(String(error)));
    } finally {
      launcherCheckInProgressRef.current = false;
      if (!background) setBusy((value) => (value === "launcher-check" ? null : value));
    }
  }, [addActivity, copy, doUpdateLauncher]);

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
    setTutorialLoading(true);
    try {
      const doc = await readProjectDocument(kind, locale);
      setTutorialDoc(doc);
    } catch (error) {
      addActivity("error", copy.tutorialLoadFailed(String(error)));
    } finally {
      setTutorialLoading(false);
    }
  }, [addActivity, copy, locale]);

  const openTutorialLink = useCallback(async (href: string) => {
    setTutorialLoading(true);
    try {
      const doc = await readProjectDocumentPath(href, locale);
      setTutorialKind(doc.kind === "howto" ? "howto" : "readme");
      setTutorialDoc(doc);
    } catch (error) {
      addActivity("error", copy.tutorialLoadFailed(String(error)));
    } finally {
      setTutorialLoading(false);
    }
  }, [addActivity, copy, locale]);

  const refreshAllStatus = useCallback(async () => {
    setActiveTab("updates");
    if (refreshInProgressRef.current) return;
    refreshInProgressRef.current = true;
    setRefreshInProgress(true);
    setGlobalProgress({ percent: 8, label: copy.refreshAllStarted });
    addActivity("info", copy.refreshAllStarted);
    await sleep(80);
    try {
      setGlobalProgress({ percent: 22, label: copy.refreshLifeBookStep });
      await refreshState();
      if (!lifeBookSyncingRef.current) {
        lifeBookSyncingRef.current = true;
        try {
          const info = await syncLifeBookProject(locale);
          setLifeBookUpdate(info);
          addActivity(info.hasUpdate ? "warning" : "success", info.hasUpdate ? copy.lifeBookFound(info.behindCount) : copy.lifeBookLatest);
        } finally {
          lifeBookSyncingRef.current = false;
        }
      }
      setGlobalProgress({ percent: 68, label: copy.refreshOpenCodeStep });
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
      await refreshOpenCodeLocalStatus();
      setGlobalProgress({ percent: 100, label: copy.refreshAllDone });
      addActivity("success", copy.refreshAllDone);
    } catch (error) {
      addActivity("error", copy.lifeBookUpdateStopped(String(error)));
      await refreshState();
      await refreshOpenCodeLocalStatus();
    } finally {
      window.setTimeout(() => setGlobalProgress(null), 900);
      refreshInProgressRef.current = false;
      setRefreshInProgress(false);
    }
  }, [addActivity, copy, locale, refreshOpenCodeLocalStatus, refreshState]);

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

    const unlistenOpenCode = listenOpenCodeDownloadProgress((progress) => {
      setOpenCodeProgress(progress);
      if (progress.downloadedBytes > 0 || progress.percent > 0) {
        setOpenCodeSyntheticProgress(null);
      }
    });
    const unlistenLauncher = listenLauncherDownloadProgress((progress) => {
      setLauncherProgress(progress);
    });
    return () => {
      unlistenOpenCode.then((fn) => fn()).catch(() => undefined);
      unlistenLauncher.then((fn) => fn()).catch(() => undefined);
    };
  }, [refreshOpenCodeLocalStatus, refreshState]);

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
      void prepareLifeBookInBackground();
      if (settings.checkLauncherOnLaunch) void checkLauncher(true, true);
      if (settings.checkOpenCodeOnLaunch) void checkOpenCode(true);
    }, 600);
    return () => window.clearTimeout(timer);
    // Startup automation should run once after first paint using the initial persisted settings.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (activeTab === "tutorial" && !tutorialDoc && !tutorialLoading) {
      void loadTutorial(tutorialKind);
    }
  }, [activeTab, loadTutorial, tutorialDoc, tutorialKind, tutorialLoading]);

  useEffect(() => {
    return () => {
      if (openCodeLaunchResetTimer.current) {
        window.clearTimeout(openCodeLaunchResetTimer.current);
      }
      if (floatingToastTimer.current) {
        window.clearTimeout(floatingToastTimer.current);
      }
    };
  }, []);

  const commits = lifeBookUpdate?.commits ?? [];
  const displayedCommits = showAllCommits ? commits : commits.slice(0, 1);
  const firstCommit = commits[0];
  const repoReady = Boolean(state?.repoReady);
  const lifeBookBusy = lifeBookPreparing || lifeBookSyncing;
  const latestLifeBookVersion = firstCommit ? versionFromDate(firstCommit.date) : repoReady ? copy.projectReady : copy.preparing;
  const currentLifeBookVersion = repoReady
    ? state?.localCommitShort === "preview"
      ? "v2025.05.25"
      : state?.localCommitShort || copy.projectReady
    : lifeBookBusy
      ? copy.preparing
      : copy.repoRequired;
  const lifeBookStatus = lifeBookBusy ? copy.preparing : repoReady ? copy.projectReady : copy.repoRequired;
  const lifeBookStatusTone: "success" | "warning" | "muted" = lifeBookBusy ? "warning" : repoReady ? "success" : "muted";
  const openCodeAvailable = Boolean(openCodeLocalStatus?.clientAvailable ?? openCodeUpdate?.clientAvailable ?? state?.opencodeAvailable);
  const openCodeInstalledVersion = openCodeUpdate?.installedVersion ?? openCodeLocalStatus?.installedVersion ?? state?.opencodeInstalledVersion ?? null;
  const openCodeCurrent = openCodeAvailable ? openCodeInstalledVersion ?? copy.installed : copy.notInstalled;
  const openCodeLatest = openCodeUpdate?.latestVersion ?? (openCodeInstalledVersion ?? copy.checking);
  const openCodeHasUpdate = Boolean(openCodeUpdate?.hasUpdate);
  const openCodeStatus = openCodeAvailable ? (openCodeHasUpdate ? copy.updateAvailable : copy.upToDate) : copy.notInstalled;
  const openCodePrimaryLabel = copy.checkUpdates;
  const openCodePrimaryIcon = RefreshCcw;
  const openCodeSecondaryLabel = copy.launchClient;
  const openCodeVisibleProgress = busy === "opencode-update"
    ? (openCodeProgress && (openCodeProgress.downloadedBytes > 0 || openCodeProgress.percent > 0) ? openCodeProgress : openCodeSyntheticProgress ?? openCodeProgress)
    : null;
  const launcherVisibleProgress = busy === "launcher-update" ? launcherProgress : null;
  const openCodeProgressLabel = formatDownloadProgress(copy, openCodeVisibleProgress);
  const launcherProgressLabel = formatDownloadProgress(copy, launcherVisibleProgress);
  const activeGlobalProgress = launcherVisibleProgress
    ? { percent: launcherVisibleProgress.percent, label: `${copy.checkLauncherTitle} ${launcherProgressLabel}` }
    : globalProgress;
  const showingOpenCodeDownloadHud = openCodeDownloadState !== "idle" && !openCodeDownloadDismissed;
  const openCodeHudMessage = openCodeDownloadMessage || openCodeProgressLabel || copy.working;

  const visibleActivities = useMemo(() => activities.slice(0, 5), [activities]);

  return (
    <div className={isMaximized ? "launcher-frame maximized" : "launcher-frame"}>
      <header className="frame-titlebar">
        <div className="titlebar-brand" data-tauri-drag-region>
          <LogoMark />
          <span>LifeBook Launcher</span>
          <span className="titlebar-version">{LAUNCHER_VERSION}</span>
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
                  onMore={syncLifeBookNow}
                  moreLabel={copy.updateLifeBookProject}
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
              onSelect={(kind) => void loadTutorial(kind)}
              onOpenLink={(href) => void openTutorialLink(href)}
            />
          )}

          {activeTab === "settings" && (
            <section className="settings-panel">
              <PanelHeading title={copy.settingsTitle} />
              <SettingToggle title={copy.autoStartTitle} description={copy.autoStartDescription} checked={settings.autoStart} onChange={(value) => updateSetting("autoStart", value)} />
              <ProjectPathPanel copy={copy} path={state?.repoRoot || "D:\\LifeBook"} onChange={() => void chooseRepo()} />
              <SettingToggle title={copy.checkLauncherTitle} description={copy.checkLauncherDescription} checked={settings.checkLauncherOnLaunch} onChange={(value) => updateSetting("checkLauncherOnLaunch", value)} />
              <SettingToggle title={copy.checkOpenCodeTitle} description={copy.checkOpenCodeDescription} checked={settings.checkOpenCodeOnLaunch} onChange={(value) => updateSetting("checkOpenCodeOnLaunch", value)} />
            </section>
          )}

          {activeTab === "logs" && <ActivityTable copy={copy} activities={activities.slice(0, 12)} expanded onViewFullLog={() => undefined} />}
        </section>
      </main>
      <ConfirmDialog dialog={confirmDialog} onCancel={() => resolveConfirmDialog(false)} onConfirm={() => resolveConfirmDialog(true)} />
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
  onSelect,
  onOpenLink,
}: {
  copy: Copy;
  kind: TutorialKind;
  document: ProjectDocument | null;
  loading: boolean;
  onSelect: (kind: TutorialKind) => void;
  onOpenLink: (href: string) => void;
}) {
  const html = useMemo(() => renderMarkdownToHtml(document?.content ?? ""), [document]);
  const handleClick = (event: MouseEvent<HTMLDivElement>) => {
    const target = event.target as HTMLElement | null;
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
        <PanelHeading title={copy.tutorialTitle} />
        <div className="tutorial-switch" role="tablist" aria-label={copy.tutorialTitle}>
          <button type="button" className={kind === "readme" ? "active" : undefined} onClick={() => onSelect("readme")}>{copy.tutorialReadme}</button>
          <button type="button" className={kind === "howto" ? "active" : undefined} onClick={() => onSelect("howto")}>{copy.tutorialHowTo}</button>
        </div>
      </div>
      <div className="tutorial-doc-meta">
        <strong>{document?.title || copy.tutorialTitle}</strong>
        <span>{copy.tutorialCurrentDocument}: {document?.path || copy.tutorialLoading}</span>
      </div>
      <div className="tutorial-scroll">
        {loading ? (
          <div className="table-empty">{copy.tutorialLoading}</div>
        ) : (
          <div className="markdown-body" onClick={handleClick} dangerouslySetInnerHTML={{ __html: html }} />
        )}
      </div>
    </section>
  );
}

function renderMarkdownToHtml(source: string) {
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
        html.push(`<pre><code>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
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
    html.push(`<pre><code>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
  }
  if (inHtmlBlock && htmlLines.length) {
    html.push(sanitizeTrustedDocHtml(htmlLines.join("\n")));
  }
  return html.join("\n");
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

function FloatingFeedback({
  toast,
  globalProgress,
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
}: {
  toast: FloatingToast | null;
  globalProgress: { percent: number; label: string } | null;
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
}) {
  if (!toast && !globalProgress && !openCodeVisible) return null;
  const openCodePercent = openCodeProgress?.percent ?? 0;
  const openCodeRunning = openCodeState === "downloading" || openCodeState === "cancelling";
  return (
    <div className="floating-feedback-layer" aria-live="polite">
      {toast && <div className={`floating-toast ${toast.tone}`}>{toast.message}</div>}
      {globalProgress && (
        <section className="floating-progress-card blue">
          <div className="floating-progress-header">
            <strong>{globalProgress.label}</strong>
            <span>{globalProgress.percent}%</span>
          </div>
          <div className="progress-bar">
            <span style={{ width: `${globalProgress.percent}%` }} />
          </div>
        </section>
      )}
      {openCodeVisible && (
        <section className={`floating-progress-card green ${openCodeState}`}>
          <div className="floating-progress-header">
            <strong>{openCodeTitle}</strong>
            <span>{openCodePercent}%</span>
          </div>
          <div className="progress-bar">
            <span style={{ width: `${openCodePercent}%` }} />
          </div>
          <div className="floating-progress-footer">
            <span>{openCodeState === "cancelling" ? copy.working : openCodeMessage}</span>
            <div className="floating-progress-actions">
              {openCodeRunning ? (
                <>
                  <button type="button" onClick={onStopOpenCode} disabled={openCodeState === "cancelling"}>{copy.stopDownload}</button>
                  <button type="button" onClick={onCancelOpenCode} disabled={openCodeState === "cancelling"}>{copy.cancelDownload}</button>
                </>
              ) : (
                <>
                  <button type="button" onClick={onRetryOpenCode}>{copy.retry}</button>
                  <button type="button" onClick={onCloseOpenCode}>{copy.close}</button>
                </>
              )}
            </div>
          </div>
        </section>
      )}
    </div>
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
              {commits.map((commit, index) => {
                const tooltip = formatCommitTooltip(copy, commit);
                return (
                  <tr key={`${commit.hash}-${commit.date}`}>
                    <td><RowIcon index={index} />{commit.date.slice(0, 16).replace("T", " ")}</td>
                    <td><code>{commit.hash}</code></td>
                    <td>{commit.title}</td>
                    <td className="commit-summary-cell" title={tooltip} aria-label={tooltip}>
                      {commit.summary || copy.noCommits}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        ) : (
          <div className="table-empty">{copy.noCommits}</div>
        )}
      </div>
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
