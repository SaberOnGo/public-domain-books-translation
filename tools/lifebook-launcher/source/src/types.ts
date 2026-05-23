export type LauncherState = {
  repoRoot: string;
  repoReady: boolean;
  repoStatus: string;
  branch: string;
  localCommit: string;
  localCommitShort: string;
  remoteUrl: string;
  dirty: boolean;
  proxyConfigured: boolean;
  platform: string;
  opencodeInstallRoot: string;
  opencodeInstalledVersion?: string | null;
  opencodeClientPath?: string | null;
  opencodeAvailable: boolean;
};

export type CommitInfo = {
  hash: string;
  date: string;
  title: string;
  summary: string;
};

export type LifeBookUpdateInfo = {
  repoRoot: string;
  currentCommit: string;
  remoteRef: string;
  behindCount: number;
  aheadCount: number;
  hasUpdate: boolean;
  commits: CommitInfo[];
};

export type OpenCodeUpdateInfo = {
  installedVersion?: string | null;
  latestVersion: string;
  hasUpdate: boolean;
  assetName: string;
  assetSize: number;
  assetUrl: string;
  installRoot: string;
  clientPath?: string | null;
  clientAvailable: boolean;
};

export type LauncherUpdateInfo = {
  installedVersion: string;
  latestVersion: string;
  hasUpdate: boolean;
  assetName: string;
  assetSize: number;
  assetUrl: string;
  installRoot: string;
};

export type ActionResult = {
  ok: boolean;
  message: string;
};

export type DownloadProgress = {
  percent: number;
  downloadedBytes: number;
  totalBytes: number;
};

export type LauncherSettings = {
  autoStart: boolean;
  checkLauncherOnLaunch: boolean;
  autoInstallLauncherUpdates: boolean;
  autoUpdateLifeBook: boolean;
  checkOpenCodeOnLaunch: boolean;
};

export type ActivityItem = {
  id: string;
  time: string;
  level: "info" | "success" | "warning" | "error";
  message: string;
};
