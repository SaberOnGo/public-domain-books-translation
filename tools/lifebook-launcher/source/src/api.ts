import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
import {
  ActionResult,
  DiagnosticLogSettings,
  DownloadProgress,
  LauncherUpdateInfo,
  LauncherState,
  LifeBookUpdateInfo,
  NetworkProxySettings,
  NodeModulesStatus,
  OpenCodeLocalStatus,
  OpenCodeUpdateInfo,
  ProjectDocument,
  ProxyAutoDetectResult,
  ProxyTestResult,
  RuntimeStatus,
} from "./types";

declare global {
  interface Window {
    __TAURI_INTERNALS__?: unknown;
  }
}

function isTauriRuntime() {
  return typeof window !== "undefined" && Boolean(window.__TAURI_INTERNALS__);
}

function previewState(): LauncherState {
  return {
    repoRoot: "LifeBook-PublicDomain-Translator",
    repoReady: true,
    repoStatus: "ready",
    branch: "main",
    localCommit: "preview",
    localCommitShort: "preview",
    remoteUrl: "origin",
    dirty: false,
    proxyConfigured: false,
    platform: "preview",
    opencodeInstallRoot: "LifeBook/tools/opencode-desktop",
    opencodeInstalledVersion: "v1.2.3",
    opencodeClientPath: "C:\\Users\\preview\\AppData\\Local\\Programs\\OpenCode\\OpenCode.exe",
    opencodeAvailable: true,
  };
}

export function getLauncherState() {
  if (!isTauriRuntime()) {
    return Promise.resolve(previewState());
  }
  return invoke<LauncherState>("get_launcher_state");
}

export function chooseRepoFolder() {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode.", repoRoot: "D:\\LifeBook", requiresDownload: false });
  }
  return invoke<ActionResult>("choose_repo_folder");
}

export function setRepoFolder(repoRoot: string) {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode.", repoRoot, requiresDownload: false });
  }
  return invoke<ActionResult>("set_repo_folder", { repoRoot });
}

export function checkLifeBookUpdates(locale = "en") {
  if (!isTauriRuntime()) {
    const commits = [
      {
        hash: "a1b2c3d",
        date: "2025-05-25 10:15",
        title: "新增书籍：《时间简史》全文初译",
        summary: "添加《时间简史》第一版全文初译，包含第1-10章内容。",
      },
      {
        hash: "d4e5f6a",
        date: "2025-05-25 09:02",
        title: "优化术语库匹配算法",
        summary: "改进术语匹配逻辑，提高长句和复合句的识别准确率。",
      },
      {
        hash: "b7c8d9e",
        date: "2025-05-24 22:47",
        title: "修复章节导出格式问题",
        summary: "修复 Markdown 导出时标题层级丢失的问题。",
      },
      {
        hash: "e0f1a2b",
        date: "2025-05-24 18:33",
        title: "更新贡献指南",
        summary: "补充翻译规范说明，新增常见问题解答部分。",
      },
      {
        hash: "c3d4e5f",
        date: "2025-05-24 16:11",
        title: "新增西班牙语翻译支持",
        summary: "添加西班牙语语言包与基础术语库支持。",
      },
      {
        hash: "f6a7b8c",
        date: "2025-05-24 12:05",
        title: "改进 Web 编辑器体验",
        summary: "优化段落导航与快捷键提示，提升编辑效率。",
      },
      {
        hash: "9d8c7bb",
        date: "2025-05-23 23:19",
        title: "修复图片引用路径问题",
        summary: "修复部分书籍中图片相对路径失效的问题。",
      },
    ].map((commit) => ({
      ...commit,
      fullMessage: `${commit.title}\n\nZH:\n- ${commit.summary}\n\nEN:\n- Preview English summary for ${commit.hash}.\n\nJA:\n- ${commit.hash} のプレビュー概要。`,
    }));

    return Promise.resolve<LifeBookUpdateInfo>({
      repoRoot: "LifeBook-PublicDomain-Translator",
      currentCommit: "preview",
      remoteRef: "origin/main",
      behindCount: 7,
      aheadCount: 0,
      hasUpdate: true,
      commits,
    });
  }
  return invoke<LifeBookUpdateInfo>("check_lifebook_updates", { locale });
}

export function prepareLifeBookProject(locale = "en") {
  if (!isTauriRuntime()) {
    return checkLifeBookUpdates(locale);
  }
  return invoke<LifeBookUpdateInfo>("prepare_lifebook_project", { locale });
}

export function syncLifeBookProject(locale = "en") {
  if (!isTauriRuntime()) {
    return checkLifeBookUpdates(locale);
  }
  return invoke<LifeBookUpdateInfo>("sync_lifebook_project", { locale });
}

export function updateLifeBook() {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode." });
  }
  return invoke<ActionResult>("update_lifebook");
}

export function cancelLifeBookUpdate() {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode." });
  }
  return invoke<ActionResult>("cancel_lifebook_update");
}

export function getDiagnosticLogSettings() {
  if (!isTauriRuntime()) {
    return Promise.resolve<DiagnosticLogSettings>({
      saveLogs: true,
      logDir: "LifeBook/launcher/logs",
      logFile: "LifeBook/launcher/logs/lifebook-launcher.log",
      maxBytes: 4 * 1024 * 1024,
      backupCount: 5,
      maxTotalBytes: 24 * 1024 * 1024,
    });
  }
  return invoke<DiagnosticLogSettings>("get_diagnostic_log_settings");
}

export function setSaveLogsEnabled(saveLogs: boolean) {
  if (!isTauriRuntime()) {
    return Promise.resolve<DiagnosticLogSettings>({
      saveLogs,
      logDir: "LifeBook/launcher/logs",
      logFile: "LifeBook/launcher/logs/lifebook-launcher.log",
      maxBytes: 4 * 1024 * 1024,
      backupCount: 5,
      maxTotalBytes: 24 * 1024 * 1024,
    });
  }
  return invoke<DiagnosticLogSettings>("set_save_logs_enabled", { saveLogs });
}

export function getProxySettings() {
  if (!isTauriRuntime()) {
    return Promise.resolve<NetworkProxySettings>({
      enabled: false,
      scheme: "http",
      host: "127.0.0.1",
      port: 7890,
    });
  }
  return invoke<NetworkProxySettings>("get_proxy_settings");
}

export function saveProxySettings(proxy: NetworkProxySettings) {
  if (!isTauriRuntime()) {
    return Promise.resolve<NetworkProxySettings>(proxy);
  }
  return invoke<NetworkProxySettings>("save_proxy_settings", { proxy });
}

export function testProxySettings(proxy: NetworkProxySettings) {
  if (!isTauriRuntime()) {
    return Promise.resolve<ProxyTestResult>({
      ok: true,
      message: "Preview mode: proxy test succeeded in 38 ms.",
      elapsedMs: 38,
      httpVersion: "HTTP/2",
      targetUrl: "https://api.github.com/repos/SaberOnGo/public-domain-books-translation",
    });
  }
  return invoke<ProxyTestResult>("test_proxy_settings", { proxy });
}

export function autoDetectProxySettings(force = true) {
  if (!isTauriRuntime()) {
    return Promise.resolve<ProxyAutoDetectResult>({
      detected: true,
      proxy: { enabled: true, scheme: "http", host: "127.0.0.1", port: 7890 },
      test: {
        ok: true,
        message: "Preview mode: proxy auto detection succeeded.",
        elapsedMs: 36,
        httpVersion: "HTTP/2",
        targetUrl: "https://api.github.com/repos/SaberOnGo/public-domain-books-translation",
      },
      message: "Preview mode: detected local proxy.",
    });
  }
  return invoke<ProxyAutoDetectResult>("auto_detect_proxy_settings", { force });
}

export function getNodeModulesStatus() {
  if (!isTauriRuntime()) {
    return Promise.resolve<NodeModulesStatus>({
      ready: true,
      running: false,
      autoInstall: true,
      repoReady: true,
      booksDir: "LifeBook/books",
      nodeModulesDir: "LifeBook/books/node_modules",
    });
  }
  return invoke<NodeModulesStatus>("get_node_modules_status");
}

export function setAutoInstallNodeModules(enabled: boolean) {
  if (!isTauriRuntime()) {
    return Promise.resolve<NodeModulesStatus>({
      ready: true,
      running: false,
      autoInstall: enabled,
      repoReady: true,
      booksDir: "LifeBook/books",
      nodeModulesDir: "LifeBook/books/node_modules",
    });
  }
  return invoke<NodeModulesStatus>("set_auto_install_node_modules", { enabled });
}

export function getRuntimeStatus() {
  if (!isTauriRuntime()) {
    return Promise.resolve<RuntimeStatus>({
      ready: true,
      privateReady: true,
      running: false,
      runtimeRoot: "LifeBook/runtimes",
      python: {
        ready: true,
        privateReady: true,
        version: "3.12.10",
        source: "private",
        path: "LifeBook/runtimes/python/python.exe",
        message: "Python private runtime is ready.",
      },
      java: {
        ready: true,
        privateReady: true,
        version: "17.0.19",
        source: "private",
        path: "LifeBook/runtimes/java/bin/java.exe",
        message: "Java private runtime is ready.",
      },
    });
  }
  return invoke<RuntimeStatus>("get_runtime_status");
}

export function startRuntimePrepare() {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode." });
  }
  return invoke<ActionResult>("start_runtime_prepare");
}

export function startNodeModulesInstall() {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode." });
  }
  return invoke<ActionResult>("start_node_modules_install");
}

export function cancelNodeModulesInstall(removePartial = false) {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode." });
  }
  return invoke<ActionResult>("cancel_node_modules_install", { removePartial });
}

export function exportLauncherLogs() {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode." });
  }
  return invoke<ActionResult>("export_launcher_logs");
}

export function recordFrontendActivity(level: string, message: string) {
  if (!isTauriRuntime()) {
    void level;
    void message;
    return Promise.resolve();
  }
  return invoke<void>("record_frontend_activity", { level, message });
}

export function readProjectDocument(kind: "readme" | "howto", locale: string) {
  if (!isTauriRuntime()) {
    const content = kind === "readme"
      ? `# LifeBook 书坊公版书翻译项目

<table align="center">
  <tr>
    <td align="center"><h3><a href="./README.zh-CN.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./doc/public/how-to-use-prompts.zh-CN.md">How to use</a></h3></td>
  </tr>
</table>

LifeBook 书坊是一个多语言公版书翻译与 EPUB 制作流程。

## 快速开始

- 打开 [How to use](./doc/public/how-to-use-prompts.zh-CN.md)
- 查看 \`template/epub_pipeline\`
`
      : `# How to use

## 选择客户端

- 使用 LifeBook Launcher 安装 OpenCode Desktop。
- 阅读 [README](./README.zh-CN.md)。
`;
    return Promise.resolve<ProjectDocument>({
      kind,
      path: `preview/${kind}.md`,
      title: kind === "readme" ? "README" : "How to use",
      content,
    });
  }
  return invoke<ProjectDocument>("read_project_document", { kind, locale });
}

export function readProjectDocumentPath(relativePath: string, locale: string) {
  if (!isTauriRuntime()) {
    return readProjectDocument(relativePath.toLowerCase().includes("how-to-use") ? "howto" : "readme", locale);
  }
  return invoke<ProjectDocument>("read_project_document_path", { relativePath, locale });
}

export function checkLauncherUpdates() {
  if (!isTauriRuntime()) {
    return Promise.resolve<LauncherUpdateInfo>({
      installedVersion: "v1.3.2",
      latestVersion: "v1.3.2",
      hasUpdate: false,
      releaseNotes: null,
      assetName: "LifeBook Launcher_1.3.2_x64-setup.exe",
      assetSize: 2717961,
      assetUrl: "https://github.com/SaberOnGo/public-domain-books-translation/releases/latest",
      installRoot: "LifeBook/launcher/updates",
      installerPath: null,
      installerDownloaded: false,
      partialDownloadedBytes: 0,
    });
  }
  return invoke<LauncherUpdateInfo>("check_launcher_updates");
}

export function downloadAndInstallLauncherUpdate() {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode." });
  }
  return invoke<ActionResult>("download_and_install_launcher_update");
}

export function minimizeMainWindow() {
  if (!isTauriRuntime()) return Promise.resolve();
  return invoke<void>("minimize_main_window");
}

export function toggleMainWindowMaximized() {
  if (!isTauriRuntime()) return Promise.resolve(false);
  return invoke<boolean>("toggle_main_window_maximized");
}

export function closeMainWindowToTray() {
  if (!isTauriRuntime()) return Promise.resolve();
  return invoke<void>("close_main_window_to_tray");
}

export function checkOpenCodeUpdates() {
  if (!isTauriRuntime()) {
    return Promise.resolve<OpenCodeUpdateInfo>({
      installedVersion: "v1.2.3",
      latestVersion: "v1.2.3",
      hasUpdate: false,
      assetName: "opencode-desktop-win-x64.exe",
      assetSize: 156000000,
      assetUrl: "https://github.com/anomalyco/opencode/releases/latest",
      installRoot: "LifeBook/tools/opencode-desktop",
      clientPath: "C:\\Users\\preview\\AppData\\Local\\Programs\\OpenCode\\OpenCode.exe",
      clientAvailable: true,
      installerPath: "LifeBook/tools/opencode-desktop/downloads/opencode-desktop-win-x64.exe",
      installerDownloaded: true,
      partialDownloadedBytes: 0,
    });
  }
  return invoke<OpenCodeUpdateInfo>("check_opencode_updates");
}

export function checkOpenCodeLocalStatus() {
  if (!isTauriRuntime()) {
    return Promise.resolve<OpenCodeLocalStatus>({
      installedVersion: "v1.2.3",
      installRoot: "LifeBook/tools/opencode-desktop",
      clientPath: "C:\\Users\\preview\\AppData\\Local\\Programs\\OpenCode\\OpenCode.exe",
      clientAvailable: true,
    });
  }
  return invoke<OpenCodeLocalStatus>("check_opencode_local_status");
}

export function downloadAndOpenOpenCode() {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode." });
  }
  return invoke<ActionResult>("download_and_open_opencode");
}

export function cancelOpenCodeDownload() {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode." });
  }
  return invoke<ActionResult>("cancel_opencode_download");
}

export function launchOpenCodeClient() {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode." });
  }
  return invoke<ActionResult>("launch_opencode_client");
}

export function openRepoFolder() {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode." });
  }
  return invoke<ActionResult>("open_repo_folder");
}

export function openBooksFolder() {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode." });
  }
  return invoke<ActionResult>("open_books_folder");
}

export function listenOpenCodeDownloadProgress(
  callback: (payload: DownloadProgress) => void,
) {
  return listenDownloadProgress("opencode-download-progress", callback);
}

function listenDownloadProgress(
  eventName: string,
  callback: (payload: DownloadProgress) => void,
) {
  if (!isTauriRuntime()) return Promise.resolve(() => undefined);
  return listen<DownloadProgress>(eventName, (event) => {
    callback(event.payload);
  }).catch((error) => {
    const message = `frontend event listen failed event=${eventName} error=${String(error)}`;
    console.warn(`Unable to listen for ${eventName}:`, error);
    void recordFrontendActivity("warning", message).catch(() => undefined);
    return () => undefined;
  });
}

export function listenLauncherDownloadProgress(
  callback: (payload: DownloadProgress) => void,
) {
  return listenDownloadProgress("launcher-download-progress", callback);
}

export function listenLifeBookProgress(
  callback: (payload: DownloadProgress) => void,
) {
  return listenDownloadProgress("lifebook-project-progress", callback);
}

export function listenNodeModulesProgress(
  callback: (payload: DownloadProgress) => void,
) {
  return listenDownloadProgress("node-modules-install-progress", callback);
}

export function listenRuntimeProgress(
  callback: (payload: DownloadProgress) => void,
) {
  return listenDownloadProgress("runtime-install-progress", callback);
}
