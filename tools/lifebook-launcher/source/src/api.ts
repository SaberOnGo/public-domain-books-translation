import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
import {
  ActionResult,
  DownloadProgress,
  LauncherUpdateInfo,
  LauncherState,
  LifeBookUpdateInfo,
  OpenCodeUpdateInfo,
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
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode." });
  }
  return invoke<ActionResult>("choose_repo_folder");
}

export function checkLifeBookUpdates() {
  if (!isTauriRuntime()) {
    return Promise.resolve<LifeBookUpdateInfo>({
      repoRoot: "LifeBook-PublicDomain-Translator",
      currentCommit: "preview",
      remoteRef: "origin/main",
      behindCount: 7,
      aheadCount: 0,
      hasUpdate: true,
      commits: [
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
      ],
    });
  }
  return invoke<LifeBookUpdateInfo>("check_lifebook_updates");
}

export function prepareLifeBookProject() {
  if (!isTauriRuntime()) {
    return checkLifeBookUpdates();
  }
  return invoke<LifeBookUpdateInfo>("prepare_lifebook_project");
}

export function updateLifeBook() {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode." });
  }
  return invoke<ActionResult>("update_lifebook");
}

export function checkLauncherUpdates() {
  if (!isTauriRuntime()) {
    return Promise.resolve<LauncherUpdateInfo>({
      installedVersion: "v1.3.0",
      latestVersion: "v1.3.0",
      hasUpdate: false,
      assetName: "LifeBook Launcher_1.3.0_x64-setup.exe",
      assetSize: 2717961,
      assetUrl: "https://github.com/SaberOnGo/public-domain-books-translation/releases/latest",
      installRoot: "LifeBook/launcher/updates",
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
    });
  }
  return invoke<OpenCodeUpdateInfo>("check_opencode_updates");
}

export function downloadAndOpenOpenCode() {
  if (!isTauriRuntime()) {
    return Promise.resolve<ActionResult>({ ok: true, message: "Preview mode." });
  }
  return invoke<ActionResult>("download_and_open_opencode");
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
  if (!isTauriRuntime()) {
    void callback;
    return Promise.resolve(() => undefined);
  }
  return listen<DownloadProgress>("opencode-download-progress", (event) => {
    callback(event.payload);
  });
}

export function listenLauncherDownloadProgress(
  callback: (payload: DownloadProgress) => void,
) {
  if (!isTauriRuntime()) {
    void callback;
    return Promise.resolve(() => undefined);
  }
  return listen<DownloadProgress>("launcher-download-progress", (event) => {
    callback(event.payload);
  });
}
