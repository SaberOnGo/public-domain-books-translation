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
  fullMessage: string;
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
  installerPath?: string | null;
  installerDownloaded: boolean;
  partialDownloadedBytes: number;
};

export type OpenCodeLocalStatus = {
  installedVersion?: string | null;
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
  installerPath?: string | null;
  installerDownloaded: boolean;
  partialDownloadedBytes: number;
};

export type ActionResult = {
  ok: boolean;
  message: string;
  repoRoot?: string | null;
  requiresDownload?: boolean | null;
};

export type ProjectDocument = {
  kind: string;
  path: string;
  title: string;
  content: string;
};

export type DownloadProgress = {
  percent: number;
  downloadedBytes: number;
  totalBytes: number;
  message?: string | null;
  state?: "downloading" | "success" | "failed" | "stopped" | null;
};

export type DiagnosticLogSettings = {
  saveLogs: boolean;
  logDir: string;
  logFile: string;
  maxBytes: number;
  backupCount: number;
  maxTotalBytes: number;
};

export type NetworkProxySettings = {
  enabled: boolean;
  scheme: "http" | "https" | "socks5" | "socks5h";
  host: string;
  port: number | null;
};

export type ProxyTestResult = {
  ok: boolean;
  message: string;
  elapsedMs?: number | null;
  httpVersion?: string | null;
  targetUrl: string;
};

export type ProxyAutoDetectResult = {
  detected: boolean;
  proxy?: NetworkProxySettings | null;
  test?: ProxyTestResult | null;
  message: string;
};

export type NodeModulesStatus = {
  ready: boolean;
  running: boolean;
  autoInstall: boolean;
  repoReady: boolean;
  booksDir: string;
  nodeModulesDir: string;
};

export type LauncherSettings = {
  autoStart: boolean;
  checkLauncherOnLaunch: boolean;
  checkOpenCodeOnLaunch: boolean;
  saveLogsToLocal: boolean;
};

export type ActivityItem = {
  id: string;
  time: string;
  level: "info" | "success" | "warning" | "error";
  message: string;
};
