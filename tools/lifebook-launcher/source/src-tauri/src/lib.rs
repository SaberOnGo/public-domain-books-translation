use chrono::Local;
use futures_util::StreamExt;
use reqwest::{header::RANGE, StatusCode};
use serde::{Deserialize, Serialize};
#[cfg(target_os = "windows")]
use std::os::windows::process::CommandExt;
use std::{
    env, fs,
    io::{Read, Write},
    path::{Path, PathBuf},
    process::{Command, Stdio},
    sync::atomic::{AtomicBool, Ordering},
    thread,
    time::{Duration, Instant},
};
use tauri::{
    menu::MenuBuilder,
    tray::{MouseButton, TrayIconBuilder, TrayIconEvent},
    Emitter, Manager, WindowEvent,
};
use tokio::{
    fs::{File, OpenOptions},
    io::AsyncWriteExt,
};

const OPENCODE_REPO_API: &str = "https://api.github.com/repos/anomalyco/opencode/releases/latest";
const OPENCODE_REPO_LATEST_RELEASE_URL: &str =
    "https://github.com/anomalyco/opencode/releases/latest";
const OPENCODE_REPO_RELEASE_DOWNLOAD_BASE: &str =
    "https://github.com/anomalyco/opencode/releases/download";
const LIFEBOOK_LAUNCHER_REPO_API: &str =
    "https://api.github.com/repos/SaberOnGo/public-domain-books-translation/releases/latest";
const LIFEBOOK_REPO_URL: &str = "https://github.com/SaberOnGo/public-domain-books-translation.git";
const LIFEBOOK_HOME_ENV: &str = "LIFEBOOK_HOME";
const LIFEBOOK_PROGRESS_EVENT: &str = "lifebook-project-progress";
const OPENCODE_DOWNLOAD_EVENT: &str = "opencode-download-progress";
const LAUNCHER_DOWNLOAD_EVENT: &str = "launcher-download-progress";
const NODE_MODULES_PROGRESS_EVENT: &str = "node-modules-install-progress";
const TRAY_SHOW_ID: &str = "tray_show";
const TRAY_HIDE_ID: &str = "tray_hide";
const TRAY_QUIT_ID: &str = "tray_quit";
const LAUNCHER_LOG_MAX_BYTES: u64 = 4 * 1024 * 1024;
const LAUNCHER_LOG_BACKUP_COUNT: usize = 5;
const GIT_LOW_SPEED_LIMIT_BYTES: &str = "1024";
const GIT_LOW_SPEED_TIME_SECONDS: &str = "60";
const GIT_FETCH_TIMEOUT_SECONDS: u64 = 90;
const PROXY_TEST_TIMEOUT_SECONDS: u64 = 8;
const PROXY_AUTO_DETECT_TIMEOUT_SECONDS: u64 = 3;
const GITHUB_CONNECTIVITY_TEST_URL: &str =
    "https://api.github.com/repos/SaberOnGo/public-domain-books-translation";
const NPM_PRIMARY_REGISTRY: &str = "https://registry.npmjs.org/";
const NPM_CN_REGISTRY: &str = "https://registry.npmmirror.com/";
const NPM_INSTALL_TIMEOUT_SECONDS: u64 = 15 * 60;
static LIFEBOOK_UPDATE_RUNNING: AtomicBool = AtomicBool::new(false);
static LIFEBOOK_UPDATE_CANCEL_REQUESTED: AtomicBool = AtomicBool::new(false);
static OPENCODE_DOWNLOAD_CANCEL_REQUESTED: AtomicBool = AtomicBool::new(false);
static NODE_MODULES_INSTALL_RUNNING: AtomicBool = AtomicBool::new(false);
static NODE_MODULES_INSTALL_CANCEL_REQUESTED: AtomicBool = AtomicBool::new(false);
static NODE_MODULES_INSTALL_REMOVE_PARTIAL: AtomicBool = AtomicBool::new(false);

fn launcher_log_path() -> Result<PathBuf, String> {
    let base = dirs::data_local_dir()
        .or_else(dirs::config_local_dir)
        .ok_or_else(|| "无法定位用户本地数据目录。".to_string())?;
    Ok(base
        .join("LifeBook")
        .join("launcher")
        .join("logs")
        .join("lifebook-launcher.log"))
}

fn append_launcher_log(level: &str, message: impl AsRef<str>) {
    let Ok(path) = launcher_log_path() else {
        return;
    };
    let _ = append_launcher_log_to_path(
        &path,
        launcher_logging_enabled(),
        LAUNCHER_LOG_MAX_BYTES,
        LAUNCHER_LOG_BACKUP_COUNT,
        level,
        message.as_ref(),
    );
}

fn append_launcher_log_to_path(
    path: &Path,
    enabled: bool,
    max_bytes: u64,
    backup_count: usize,
    level: &str,
    message: &str,
) -> Result<(), String> {
    if !enabled {
        return Ok(());
    }
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent).map_err(|err| err.to_string())?;
    }
    let timestamp = Local::now().format("%Y-%m-%d %H:%M:%S%.3f %:z");
    let line = format!("[{timestamp}] [{level}] {message}\n");
    let existing_bytes = fs::metadata(path)
        .map(|metadata| metadata.len())
        .unwrap_or(0);
    if max_bytes > 0 && existing_bytes > 0 && existing_bytes + line.len() as u64 > max_bytes {
        rotate_launcher_log(path, backup_count)?;
    }
    let mut file = fs::OpenOptions::new()
        .create(true)
        .append(true)
        .open(path)
        .map_err(|err| err.to_string())?;
    file.write_all(line.as_bytes())
        .map_err(|err| err.to_string())
}

fn rotate_launcher_log(path: &Path, backup_count: usize) -> Result<(), String> {
    if backup_count == 0 {
        if path.exists() {
            fs::remove_file(path).map_err(|err| err.to_string())?;
        }
        return Ok(());
    }
    let oldest = rotated_log_path(path, backup_count);
    if oldest.exists() {
        fs::remove_file(&oldest).map_err(|err| err.to_string())?;
    }
    for index in (1..backup_count).rev() {
        let source = rotated_log_path(path, index);
        if source.exists() {
            fs::rename(&source, rotated_log_path(path, index + 1))
                .map_err(|err| err.to_string())?;
        }
    }
    if path.exists() {
        fs::rename(path, rotated_log_path(path, 1)).map_err(|err| err.to_string())?;
    }
    Ok(())
}

fn rotated_log_path(path: &Path, index: usize) -> PathBuf {
    if let Some(extension) = path.extension().and_then(|value| value.to_str()) {
        path.with_extension(format!("{extension}.{index}"))
    } else {
        let file_name = path
            .file_name()
            .and_then(|value| value.to_str())
            .unwrap_or("lifebook-launcher");
        path.with_file_name(format!("{file_name}.{index}"))
    }
}

fn launcher_logging_enabled() -> bool {
    read_launcher_config()
        .as_ref()
        .map(diagnostic_logging_enabled_from_config)
        .unwrap_or(true)
}

fn diagnostic_logging_enabled_from_config(config: &LauncherConfig) -> bool {
    config.save_logs.unwrap_or(true)
}

fn auto_install_node_modules_enabled_from_config(config: &LauncherConfig) -> bool {
    config.auto_install_node_modules.unwrap_or(true)
}

async fn run_blocking<T, F>(work: F) -> Result<T, String>
where
    T: Send + 'static,
    F: FnOnce() -> Result<T, String> + Send + 'static,
{
    tauri::async_runtime::spawn_blocking(work)
        .await
        .map_err(|err| format!("后台任务执行失败：{err}"))?
}

struct LifeBookUpdateGuard;

impl LifeBookUpdateGuard {
    fn try_acquire() -> Result<Self, String> {
        LIFEBOOK_UPDATE_RUNNING
            .compare_exchange(false, true, Ordering::Acquire, Ordering::Relaxed)
            .map(|_| LifeBookUpdateGuard)
            .map_err(|_| "LifeBook 项目正在后台更新，请等待当前更新完成。".to_string())
    }
}

impl Drop for LifeBookUpdateGuard {
    fn drop(&mut self) {
        LIFEBOOK_UPDATE_CANCEL_REQUESTED.store(false, Ordering::Release);
        LIFEBOOK_UPDATE_RUNNING.store(false, Ordering::Release);
    }
}

struct NodeModulesInstallGuard;

impl NodeModulesInstallGuard {
    fn try_acquire() -> Result<Self, String> {
        NODE_MODULES_INSTALL_RUNNING
            .compare_exchange(false, true, Ordering::Acquire, Ordering::Relaxed)
            .map(|_| NodeModulesInstallGuard)
            .map_err(|_| "EPUB 构建依赖正在后台安装，请等待当前任务完成。".to_string())
    }
}

impl Drop for NodeModulesInstallGuard {
    fn drop(&mut self) {
        NODE_MODULES_INSTALL_CANCEL_REQUESTED.store(false, Ordering::Release);
        NODE_MODULES_INSTALL_REMOVE_PARTIAL.store(false, Ordering::Release);
        NODE_MODULES_INSTALL_RUNNING.store(false, Ordering::Release);
    }
}

#[derive(Clone)]
struct LifeBookProgressEmitter {
    app: tauri::AppHandle,
    locale: Option<String>,
}

#[derive(Clone)]
struct NodeModulesProgressEmitter {
    app: tauri::AppHandle,
}

#[derive(Clone, Copy)]
enum GitProgressPhase {
    Clone,
    Fetch,
    Pull,
}

#[derive(Clone, Copy, Debug)]
enum GitHttpMode {
    Http2,
    Http11,
}

impl GitHttpMode {
    fn value(self) -> &'static str {
        match self {
            GitHttpMode::Http2 => "HTTP/2",
            GitHttpMode::Http11 => "HTTP/1.1",
        }
    }
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct LauncherState {
    repo_root: String,
    repo_ready: bool,
    repo_status: String,
    branch: String,
    local_commit: String,
    local_commit_short: String,
    remote_url: String,
    dirty: bool,
    proxy_configured: bool,
    platform: String,
    opencode_install_root: String,
    opencode_installed_version: Option<String>,
    opencode_client_path: Option<String>,
    opencode_available: bool,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct CommitInfo {
    hash: String,
    date: String,
    title: String,
    summary: String,
    full_message: String,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct LifeBookUpdateInfo {
    repo_root: String,
    current_commit: String,
    remote_ref: String,
    behind_count: u32,
    ahead_count: u32,
    has_update: bool,
    commits: Vec<CommitInfo>,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct OpenCodeUpdateInfo {
    installed_version: Option<String>,
    latest_version: String,
    has_update: bool,
    asset_name: String,
    asset_size: u64,
    asset_url: String,
    install_root: String,
    client_path: Option<String>,
    client_available: bool,
    installer_path: Option<String>,
    installer_downloaded: bool,
    partial_downloaded_bytes: u64,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct OpenCodeLocalStatus {
    installed_version: Option<String>,
    install_root: String,
    client_path: Option<String>,
    client_available: bool,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct LauncherUpdateInfo {
    installed_version: String,
    latest_version: String,
    has_update: bool,
    asset_name: String,
    asset_size: u64,
    asset_url: String,
    install_root: String,
    installer_path: Option<String>,
    installer_downloaded: bool,
    partial_downloaded_bytes: u64,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct ActionResult {
    ok: bool,
    message: String,
    repo_root: Option<String>,
    requires_download: Option<bool>,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct ProjectDocument {
    kind: String,
    path: String,
    title: String,
    content: String,
}

#[derive(Debug, Serialize, Deserialize, Default)]
#[serde(rename_all = "camelCase")]
struct LauncherConfig {
    repo_root: Option<String>,
    save_logs: Option<bool>,
    proxy: Option<NetworkProxySettings>,
    auto_install_node_modules: Option<bool>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "camelCase")]
struct NetworkProxySettings {
    enabled: bool,
    scheme: String,
    host: String,
    port: Option<u16>,
}

impl Default for NetworkProxySettings {
    fn default() -> Self {
        Self {
            enabled: false,
            scheme: "http".into(),
            host: "127.0.0.1".into(),
            port: Some(7890),
        }
    }
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct ProxyTestResult {
    ok: bool,
    message: String,
    elapsed_ms: Option<u128>,
    http_version: Option<String>,
    target_url: String,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct ProxyAutoDetectResult {
    detected: bool,
    proxy: Option<NetworkProxySettings>,
    test: Option<ProxyTestResult>,
    message: String,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct NodeModulesStatus {
    ready: bool,
    running: bool,
    auto_install: bool,
    repo_ready: bool,
    books_dir: String,
    node_modules_dir: String,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct DiagnosticLogSettings {
    save_logs: bool,
    log_dir: String,
    log_file: String,
    max_bytes: u64,
    backup_count: usize,
    max_total_bytes: u64,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct DiagnosticExportContext {
    generated_at: String,
    launcher_version: String,
    os: String,
    arch: String,
    repo_root: String,
    repo_status: String,
    save_logs: bool,
    log_dir: String,
    log_max_bytes: u64,
    log_backup_count: usize,
    lifebook_home_set: bool,
    proxy_configured: bool,
}

#[derive(Debug, Serialize, Clone)]
#[serde(rename_all = "camelCase")]
struct DownloadProgress {
    percent: f64,
    downloaded_bytes: u64,
    total_bytes: u64,
    #[serde(skip_serializing_if = "Option::is_none")]
    message: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    state: Option<String>,
}

#[derive(Debug, Deserialize)]
struct GithubRelease {
    tag_name: String,
    assets: Vec<GithubAsset>,
}

#[derive(Debug, Deserialize, Clone)]
struct GithubAsset {
    name: String,
    browser_download_url: String,
    size: u64,
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct OpenCodeInstallState {
    tool: String,
    installed_at: String,
    install_root: String,
    installer: String,
    platform: String,
    version: String,
    source: String,
    repository_root: String,
}

#[tauri::command]
async fn get_launcher_state() -> Result<LauncherState, String> {
    run_blocking(collect_launcher_state).await
}

fn collect_launcher_state() -> Result<LauncherState, String> {
    let repo_root = configured_or_default_repo_root()?;
    let repo_status = repo_status_for_path(&repo_root);
    let repo_ready = repo_status == "ready";
    let branch = if repo_ready {
        git_output(&repo_root, &["branch", "--show-current"]).unwrap_or_else(|_| "unknown".into())
    } else {
        "not-ready".into()
    };
    let local_commit = if repo_ready {
        git_output(&repo_root, &["rev-parse", "HEAD"]).unwrap_or_else(|_| "unknown".into())
    } else {
        String::new()
    };
    let local_commit_short = if repo_ready {
        git_output(&repo_root, &["rev-parse", "--short", "HEAD"])
            .unwrap_or_else(|_| "unknown".into())
    } else {
        String::new()
    };
    let remote_url = if repo_ready {
        git_output(&repo_root, &["config", "--get", "remote.origin.url"])
            .unwrap_or_else(|_| LIFEBOOK_REPO_URL.into())
    } else {
        LIFEBOOK_REPO_URL.into()
    };
    let dirty = repo_ready && has_tracked_changes(&repo_root).unwrap_or(false);
    let proxy_configured = is_proxy_configured();
    let platform = format!("{} {}", std::env::consts::OS, std::env::consts::ARCH);
    let install_root = opencode_install_root()?;
    let client_path = detected_opencode_client(&install_root);
    let installed_version = client_path
        .as_deref()
        .and_then(|_| read_opencode_state(&install_root).map(|state| state.version));
    let opencode_available = client_path.is_some();

    Ok(LauncherState {
        repo_root: display_path(&repo_root),
        repo_ready,
        repo_status,
        branch: branch.trim().to_string(),
        local_commit: local_commit.trim().to_string(),
        local_commit_short: local_commit_short.trim().to_string(),
        remote_url: remote_url.trim().to_string(),
        dirty,
        proxy_configured,
        platform,
        opencode_install_root: display_path(&install_root),
        opencode_installed_version: installed_version,
        opencode_client_path: client_path.map(|path| display_path(&path)),
        opencode_available,
    })
}

#[tauri::command]
fn choose_repo_folder() -> Result<ActionResult, String> {
    let Some(folder) = rfd::FileDialog::new()
        .set_title("选择 LifeBook 项目目录")
        .pick_folder()
    else {
        return Ok(ActionResult {
            ok: false,
            message: "已取消选择 LifeBook 项目目录。".into(),
            repo_root: None,
            requires_download: None,
        });
    };

    let (repo_root, requires_download) = if let Some(existing_repo) = repo_root_from_path(&folder) {
        (existing_repo, false)
    } else if is_dir_empty(&folder) {
        (folder, true)
    } else {
        return Err(format!(
            "选择的目录不是 LifeBook 项目，且目录里已有其他文件。请选择空目录，或选择包含 AGENTS.md、template/ 和 books/ 的 LifeBook 项目目录。当前选择：{}",
            folder.display()
        ));
    };

    Ok(ActionResult {
        ok: true,
        message: format!("已选择 LifeBook 项目目录：{}", repo_root.display()),
        repo_root: Some(display_path(&repo_root)),
        requires_download: Some(requires_download),
    })
}

#[tauri::command]
fn set_repo_folder(repo_root: String) -> Result<ActionResult, String> {
    let repo_root = PathBuf::from(repo_root);
    if let Some(existing_repo) = active_repo_root_from_configured_path(&repo_root) {
        write_launcher_config(&existing_repo)?;
        return Ok(ActionResult {
            ok: true,
            message: format!("已设置 LifeBook 项目目录：{}", display_path(&existing_repo)),
            repo_root: Some(display_path(&existing_repo)),
            requires_download: Some(false),
        });
    }
    if !is_dir_empty(&repo_root) {
        return Err(format!(
            "选择的目录不是 LifeBook 项目，且目录里已有其他文件。请选择空目录，或选择包含 AGENTS.md、template/ 和 books/ 的 LifeBook 项目目录。当前选择：{}",
            display_path(&repo_root)
        ));
    }
    write_launcher_config(&repo_root)?;
    Ok(ActionResult {
        ok: true,
        message: format!("已设置 LifeBook 项目目录：{}", display_path(&repo_root)),
        repo_root: Some(display_path(&repo_root)),
        requires_download: Some(true),
    })
}

#[tauri::command]
async fn check_lifebook_updates(locale: Option<String>) -> Result<LifeBookUpdateInfo, String> {
    run_blocking(move || {
        let repo_root = active_lifebook_repo_root()?;
        if let Ok(_guard) = LifeBookUpdateGuard::try_acquire() {
            let should_fetch = remote_matches_local_head(&repo_root).is_ok_and(|matches| !matches);
            lifebook_update_info_best_effort(&repo_root, should_fetch, locale.as_deref())
        } else {
            lifebook_update_info_best_effort(&repo_root, false, locale.as_deref())
        }
    })
    .await
}

#[tauri::command]
async fn update_lifebook(app: tauri::AppHandle) -> Result<ActionResult, String> {
    run_blocking(move || {
        let repo_root = active_lifebook_repo_root()?;
        append_launcher_log(
            "INFO",
            format!(
                "update_lifebook requested repo_root={}",
                display_path(&repo_root)
            ),
        );
        let _guard = LifeBookUpdateGuard::try_acquire()?;
        LIFEBOOK_UPDATE_CANCEL_REQUESTED.store(false, Ordering::Release);
        let progress = LifeBookProgressEmitter::new(app, None);
        progress.emit_key(6, "sync_start");
        update_lifebook_project_at(&repo_root, Some(&progress))?;
        progress.emit_key(100, "complete");
        Ok(ActionResult {
            ok: true,
            message: "LifeBook 已更新到最新版本。".into(),
            repo_root: None,
            requires_download: None,
        })
    })
    .await
}

#[tauri::command]
async fn prepare_lifebook_project(
    app: tauri::AppHandle,
    locale: Option<String>,
) -> Result<LifeBookUpdateInfo, String> {
    run_blocking(move || {
        let repo_root = configured_or_default_repo_root()?;
        append_launcher_log(
            "INFO",
            format!(
                "prepare_lifebook_project requested configured_root={} locale={:?}",
                display_path(&repo_root),
                locale
            ),
        );
        let _guard = match LifeBookUpdateGuard::try_acquire() {
            Ok(guard) => guard,
            Err(error) => {
                if is_lifebook_repo(&repo_root) {
                    return lifebook_update_info_best_effort(&repo_root, false, locale.as_deref());
                }
                return Err(error);
            }
        };
        LIFEBOOK_UPDATE_CANCEL_REQUESTED.store(false, Ordering::Release);
        let progress = LifeBookProgressEmitter::new(app, locale.clone());
        progress.emit_key(5, "prepare_start");
        ensure_lifebook_project_exists(&repo_root, Some(&progress))?;
        let update_result = update_lifebook_project_at(&repo_root, Some(&progress));
        progress.emit_key(96, "read_changes");
        let info = lifebook_update_info_best_effort(&repo_root, false, locale.as_deref());
        if update_result.is_ok() && info.is_ok() {
            progress.emit_key(100, "complete");
        }
        match (update_result, info) {
            (Ok(_), Ok(info)) => Ok(info),
            (Err(update_error), _) => Err(update_error),
            (Ok(_), Err(info_error)) => Err(info_error),
        }
    })
    .await
}

#[tauri::command]
async fn sync_lifebook_project(
    app: tauri::AppHandle,
    locale: Option<String>,
) -> Result<LifeBookUpdateInfo, String> {
    run_blocking(move || {
        let repo_root = configured_or_default_repo_root()?;
        append_launcher_log(
            "INFO",
            format!(
                "sync_lifebook_project requested configured_root={} locale={:?}",
                display_path(&repo_root),
                locale
            ),
        );
        let _guard = match LifeBookUpdateGuard::try_acquire() {
            Ok(guard) => guard,
            Err(error) => {
                if is_lifebook_repo(&repo_root) {
                    return lifebook_update_info_best_effort(&repo_root, false, locale.as_deref());
                }
                return Err(error);
            }
        };
        LIFEBOOK_UPDATE_CANCEL_REQUESTED.store(false, Ordering::Release);
        let progress = LifeBookProgressEmitter::new(app, locale.clone());
        progress.emit_key(5, "sync_start");
        ensure_lifebook_project_exists(&repo_root, Some(&progress))?;
        let update_result = update_lifebook_project_at(&repo_root, Some(&progress));
        progress.emit_key(96, "read_changes");
        let info = lifebook_update_info_best_effort(&repo_root, false, locale.as_deref());
        if update_result.is_ok() && info.is_ok() {
            progress.emit_key(100, "complete");
        }
        match (update_result, info) {
            (Ok(_), Ok(info)) => Ok(info),
            (Err(update_error), _) => Err(update_error),
            (Ok(_), Err(info_error)) => Err(info_error),
        }
    })
    .await
}

#[tauri::command]
fn cancel_lifebook_update() -> Result<ActionResult, String> {
    append_launcher_log("WARN", "cancel_lifebook_update requested");
    LIFEBOOK_UPDATE_CANCEL_REQUESTED.store(true, Ordering::Release);
    Ok(ActionResult {
        ok: true,
        message: "正在停止 LifeBook 准备/同步。临时下载目录会在下次重试时自动整理。".into(),
        repo_root: None,
        requires_download: None,
    })
}

#[tauri::command]
fn get_diagnostic_log_settings() -> Result<DiagnosticLogSettings, String> {
    diagnostic_log_settings()
}

#[tauri::command]
fn set_save_logs_enabled(save_logs: bool) -> Result<DiagnosticLogSettings, String> {
    if !save_logs {
        append_launcher_log("INFO", "diagnostic logging disabled by user");
    }
    write_save_logs_config(save_logs)?;
    if save_logs {
        append_launcher_log("INFO", "diagnostic logging enabled by user");
    }
    diagnostic_log_settings()
}

#[tauri::command]
fn get_proxy_settings() -> Result<NetworkProxySettings, String> {
    Ok(configured_proxy_settings())
}

#[tauri::command]
fn save_proxy_settings(proxy: NetworkProxySettings) -> Result<NetworkProxySettings, String> {
    write_proxy_config(proxy)
}

#[tauri::command]
async fn test_proxy_settings(proxy: NetworkProxySettings) -> Result<ProxyTestResult, String> {
    let proxy_url = proxy_url_from_settings(&proxy)?;
    let Some(proxy_url) = proxy_url else {
        return Ok(ProxyTestResult {
            ok: false,
            message: "请先启用代理并填写 IP/端口。".into(),
            elapsed_ms: None,
            http_version: None,
            target_url: GITHUB_CONNECTIVITY_TEST_URL.into(),
        });
    };

    match test_github_connectivity_via_proxy(&proxy_url, false).await {
        Ok(result) => Ok(result),
        Err(auto_error) => {
            append_launcher_log(
                "WARN",
                format!("proxy automatic HTTP test failed, retrying HTTP/1.1: {auto_error}"),
            );
            test_github_connectivity_via_proxy(&proxy_url, true)
                .await
                .map_err(|retry_error| {
                    format!("代理测试失败。自动 HTTP：{auto_error}；HTTP/1.1 重试：{retry_error}")
                })
        }
    }
}

#[tauri::command]
async fn auto_detect_proxy_settings(force: Option<bool>) -> Result<ProxyAutoDetectResult, String> {
    let force = force.unwrap_or(false);
    let current = configured_proxy_settings();
    if current.enabled && !force {
        return Ok(ProxyAutoDetectResult {
            detected: true,
            proxy: Some(current),
            test: None,
            message: "已启用手动代理设置，自动识别不会覆盖。".into(),
        });
    }

    let mut last_error = String::new();
    for candidate in proxy_detection_candidates() {
        let Ok(Some(proxy_url)) = proxy_url_from_settings(&candidate) else {
            continue;
        };
        let test = match test_github_connectivity_via_proxy_with_timeout(
            &proxy_url,
            false,
            Duration::from_secs(PROXY_AUTO_DETECT_TIMEOUT_SECONDS),
        )
        .await
        {
            Ok(test) => Ok(test),
            Err(_) => {
                test_github_connectivity_via_proxy_with_timeout(
                    &proxy_url,
                    true,
                    Duration::from_secs(PROXY_AUTO_DETECT_TIMEOUT_SECONDS),
                )
                .await
            }
        };
        match test {
            Ok(test) => {
                let saved = write_proxy_config(candidate)?;
                append_launcher_log(
                    "INFO",
                    format!(
                        "auto detected proxy scheme={} host={} port={:?}",
                        saved.scheme, saved.host, saved.port
                    ),
                );
                return Ok(ProxyAutoDetectResult {
                    detected: true,
                    proxy: Some(saved),
                    test: Some(test),
                    message: "已自动识别并启用可连接 GitHub 的本机代理。".into(),
                });
            }
            Err(error) => {
                last_error = error;
            }
        }
    }

    Ok(ProxyAutoDetectResult {
        detected: false,
        proxy: None,
        test: None,
        message: if last_error.is_empty() {
            "未识别到可连接 GitHub 的本机代理。".into()
        } else {
            format!("未识别到可连接 GitHub 的本机代理。最后一次测试失败：{last_error}")
        },
    })
}

#[tauri::command]
fn get_node_modules_status() -> Result<NodeModulesStatus, String> {
    collect_node_modules_status()
}

#[tauri::command]
fn set_auto_install_node_modules(enabled: bool) -> Result<NodeModulesStatus, String> {
    write_auto_install_node_modules_config(enabled)?;
    collect_node_modules_status()
}

#[tauri::command]
fn start_node_modules_install(app: tauri::AppHandle) -> Result<ActionResult, String> {
    let repo_root = active_lifebook_repo_root()?;
    if books_node_modules_ready(&repo_root) {
        return Ok(ActionResult {
            ok: true,
            message: "EPUB 构建依赖已准备完成。".into(),
            repo_root: None,
            requires_download: None,
        });
    }
    let guard = NodeModulesInstallGuard::try_acquire()?;
    NODE_MODULES_INSTALL_CANCEL_REQUESTED.store(false, Ordering::Release);
    NODE_MODULES_INSTALL_REMOVE_PARTIAL.store(false, Ordering::Release);
    let emitter = NodeModulesProgressEmitter::new(app);
    emitter.emit(
        1.0,
        0,
        0,
        "正在后台安装 EPUB 构建依赖...".into(),
        Some("downloading"),
    );
    thread::spawn(move || {
        let _guard = guard;
        let result = ensure_books_node_modules(&repo_root, Some(&emitter));
        match result {
            Ok(()) => emitter.emit(
                100.0,
                100,
                100,
                "EPUB 构建依赖已准备完成。".into(),
                Some("success"),
            ),
            Err(error) if NODE_MODULES_INSTALL_CANCEL_REQUESTED.load(Ordering::Acquire) => {
                let remove_partial = NODE_MODULES_INSTALL_REMOVE_PARTIAL.load(Ordering::Acquire);
                if remove_partial {
                    if let Err(clean_error) = remove_node_modules_dir_safely(&repo_root) {
                        append_launcher_log(
                            "WARN",
                            format!("remove partial node_modules failed: {clean_error}"),
                        );
                    }
                }
                emitter.emit(
                    0.0,
                    0,
                    100,
                    "EPUB 构建依赖安装已停止，可重试。".into(),
                    Some("stopped"),
                );
                append_launcher_log("WARN", format!("node_modules install stopped: {error}"));
            }
            Err(error) => {
                let message = format!("EPUB 构建依赖安装失败：{error}。后续可让 AI 继续补充安装。");
                emitter.emit(0.0, 0, 100, message.clone(), Some("failed"));
                append_launcher_log("ERROR", message);
            }
        }
    });
    Ok(ActionResult {
        ok: true,
        message: "正在后台安装 EPUB 构建依赖，不影响继续使用 Launcher。".into(),
        repo_root: None,
        requires_download: None,
    })
}

#[tauri::command]
fn cancel_node_modules_install(remove_partial: Option<bool>) -> Result<ActionResult, String> {
    let remove_partial = remove_partial.unwrap_or(false);
    NODE_MODULES_INSTALL_REMOVE_PARTIAL.store(remove_partial, Ordering::Release);
    NODE_MODULES_INSTALL_CANCEL_REQUESTED.store(true, Ordering::Release);
    Ok(ActionResult {
        ok: true,
        message: if remove_partial {
            "正在取消 EPUB 构建依赖安装，并清理未完成的 node_modules。".into()
        } else {
            "正在停止 EPUB 构建依赖安装，可稍后重试。".into()
        },
        repo_root: None,
        requires_download: None,
    })
}

#[tauri::command]
fn export_launcher_logs() -> Result<ActionResult, String> {
    let Some(folder) = rfd::FileDialog::new()
        .set_title("导出 LifeBook Launcher LOG")
        .pick_folder()
    else {
        return Ok(ActionResult {
            ok: false,
            message: "已取消导出 LOG。".into(),
            repo_root: None,
            requires_download: None,
        });
    };
    let log_file = launcher_log_path()?;
    let log_dir = log_file
        .parent()
        .map(Path::to_path_buf)
        .unwrap_or_else(|| log_file.clone());
    let context = current_diagnostic_context()?;
    let export_dir = export_diagnostic_logs_to_dir(&folder, &log_dir, &context)?;
    append_launcher_log(
        "INFO",
        format!("diagnostic logs exported to {}", display_path(&export_dir)),
    );
    Ok(ActionResult {
        ok: true,
        message: format!("已导出 LOG：{}", display_path(&export_dir)),
        repo_root: None,
        requires_download: None,
    })
}

#[tauri::command]
fn record_frontend_activity(level: String, message: String) -> Result<(), String> {
    let normalized_level = match level.to_ascii_lowercase().as_str() {
        "error" => "UI-ERROR",
        "warning" => "UI-WARN",
        "success" => "UI-SUCCESS",
        _ => "UI-INFO",
    };
    append_launcher_log(normalized_level, message);
    Ok(())
}

#[tauri::command]
fn read_project_document(kind: String, locale: String) -> Result<ProjectDocument, String> {
    let repo_root = active_lifebook_repo_root()?;
    let relative_path = project_document_candidates(&kind, &locale)
        .into_iter()
        .find(|path| repo_root.join(path).is_file())
        .ok_or_else(|| format!("没有找到 {kind} 文档。请确认 LifeBook 项目已准备完成。"))?;
    read_project_document_file(&repo_root, &relative_path, &kind)
}

#[tauri::command]
fn read_project_document_path(
    relative_path: String,
    locale: String,
) -> Result<ProjectDocument, String> {
    let repo_root = active_lifebook_repo_root()?;
    let safe_path = safe_project_relative_path(&relative_path)?;
    let full_path = repo_root.join(&safe_path);
    if !full_path.is_file() {
        return read_project_document(document_kind_from_path(&safe_path), locale);
    }
    let kind = document_kind_from_path(&safe_path);
    read_project_document_file(&repo_root, &safe_path, &kind)
}

#[tauri::command]
async fn check_launcher_updates() -> Result<LauncherUpdateInfo, String> {
    let install_root = launcher_update_root()?;
    let release = fetch_lifebook_launcher_release().await?;
    let asset = select_launcher_asset(&release)?;
    let installed_version = launcher_current_version();
    let destination = install_root.join("downloads").join(&asset.name);
    let partial_destination = partial_download_path(&destination)?;
    let installer_downloaded = asset.size > 0 && file_size(&destination) >= asset.size;
    let partial_downloaded_bytes = if installer_downloaded {
        asset.size
    } else {
        file_size(&partial_destination).min(asset.size)
    };

    Ok(LauncherUpdateInfo {
        installed_version: installed_version.clone(),
        latest_version: release.tag_name.clone(),
        has_update: is_remote_version_newer(&release.tag_name, &installed_version),
        asset_name: asset.name.clone(),
        asset_size: asset.size,
        asset_url: asset.browser_download_url.clone(),
        install_root: install_root.display().to_string(),
        installer_path: installer_downloaded.then(|| destination.display().to_string()),
        installer_downloaded,
        partial_downloaded_bytes,
    })
}

#[tauri::command]
async fn download_and_install_launcher_update(
    app: tauri::AppHandle,
) -> Result<ActionResult, String> {
    let install_root = launcher_update_root()?;
    let release = fetch_lifebook_launcher_release().await?;
    let asset = select_launcher_asset(&release)?;
    let downloads_dir = install_root.join("downloads");
    fs::create_dir_all(&downloads_dir).map_err(|err| err.to_string())?;
    let destination = downloads_dir.join(&asset.name);
    download_file(
        &app,
        LAUNCHER_DOWNLOAD_EVENT,
        "LifeBook Launcher",
        &asset.browser_download_url,
        &destination,
        asset.size,
        None,
    )
    .await?;

    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        let mut permissions = fs::metadata(&destination)
            .map_err(|err| err.to_string())?
            .permissions();
        permissions.set_mode(0o755);
        fs::set_permissions(&destination, permissions).map_err(|err| err.to_string())?;
    }

    schedule_launcher_update_install(&destination)?;
    let app_for_exit = app.clone();
    thread::spawn(move || {
        thread::sleep(Duration::from_millis(900));
        app_for_exit.exit(0);
    });

    Ok(ActionResult {
        ok: true,
        message: "LifeBook Launcher 更新已下载，正在自动安装并重启。".into(),
        repo_root: None,
        requires_download: None,
    })
}

#[tauri::command]
fn minimize_main_window(app: tauri::AppHandle) -> Result<(), String> {
    let window = app
        .get_webview_window("main")
        .ok_or_else(|| "无法定位 LifeBook Launcher 主窗口。".to_string())?;
    window.minimize().map_err(|err| err.to_string())
}

#[tauri::command]
fn toggle_main_window_maximized(app: tauri::AppHandle) -> Result<bool, String> {
    let window = app
        .get_webview_window("main")
        .ok_or_else(|| "无法定位 LifeBook Launcher 主窗口。".to_string())?;
    let is_maximized = window.is_maximized().map_err(|err| err.to_string())?;
    if is_maximized {
        window.unmaximize().map_err(|err| err.to_string())?;
        Ok(false)
    } else {
        window.maximize().map_err(|err| err.to_string())?;
        Ok(true)
    }
}

#[tauri::command]
fn close_main_window_to_tray(app: tauri::AppHandle) -> Result<(), String> {
    let window = app
        .get_webview_window("main")
        .ok_or_else(|| "无法定位 LifeBook Launcher 主窗口。".to_string())?;
    window.hide().map_err(|err| err.to_string())
}

#[tauri::command]
async fn check_opencode_updates() -> Result<OpenCodeUpdateInfo, String> {
    let install_root = opencode_install_root()?;
    let client_path = detected_opencode_client(&install_root);
    let installed_version = client_path
        .as_deref()
        .and_then(|_| read_opencode_state(&install_root).map(|state| state.version));
    let (latest_version, asset) = fetch_opencode_release_asset().await?;
    let downloads_dir = install_root.join("downloads");
    let installer_path = downloads_dir.join(&asset.name);
    let installer_downloaded = asset.size > 0 && file_size(&installer_path) >= asset.size;
    let partial_downloaded_bytes = partial_download_path(&installer_path)
        .ok()
        .map(|path| file_size(&path))
        .unwrap_or(0);

    Ok(OpenCodeUpdateInfo {
        installed_version: installed_version.clone(),
        latest_version: latest_version.clone(),
        has_update: client_path.is_some()
            && installed_version
                .as_deref()
                .map(|installed| is_remote_version_newer(&latest_version, installed))
                .unwrap_or(false),
        asset_name: asset.name.clone(),
        asset_size: asset.size,
        asset_url: asset.browser_download_url.clone(),
        install_root: display_path(&install_root),
        client_path: client_path.as_ref().map(|path| display_path(path)),
        client_available: client_path.is_some(),
        installer_path: installer_downloaded.then(|| display_path(&installer_path)),
        installer_downloaded,
        partial_downloaded_bytes,
    })
}

#[tauri::command]
fn check_opencode_local_status() -> Result<OpenCodeLocalStatus, String> {
    let install_root = opencode_install_root()?;
    let client_path = detected_opencode_client(&install_root);
    let installed_version = client_path
        .as_deref()
        .and_then(|_| read_opencode_state(&install_root).map(|state| state.version));

    Ok(OpenCodeLocalStatus {
        installed_version,
        install_root: display_path(&install_root),
        client_path: client_path.as_ref().map(|path| display_path(path)),
        client_available: client_path.is_some(),
    })
}

#[tauri::command]
async fn download_and_open_opencode(app: tauri::AppHandle) -> Result<ActionResult, String> {
    OPENCODE_DOWNLOAD_CANCEL_REQUESTED.store(false, Ordering::Release);
    let repo_root = configured_or_default_repo_root()?;
    let install_root = opencode_install_root()?;
    let (latest_version, asset) = fetch_opencode_release_asset().await?;

    let downloads_dir = install_root.join("downloads");
    fs::create_dir_all(&downloads_dir).map_err(|err| err.to_string())?;
    let destination = downloads_dir.join(&asset.name);
    download_file(
        &app,
        OPENCODE_DOWNLOAD_EVENT,
        "OpenCode",
        &asset.browser_download_url,
        &destination,
        asset.size,
        Some(&OPENCODE_DOWNLOAD_CANCEL_REQUESTED),
    )
    .await?;

    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        let mut permissions = fs::metadata(&destination)
            .map_err(|err| err.to_string())?
            .permissions();
        permissions.set_mode(0o755);
        fs::set_permissions(&destination, permissions).map_err(|err| err.to_string())?;
    }

    write_opencode_state(
        &install_root,
        &destination,
        &latest_version,
        &asset.browser_download_url,
        &repo_root,
    )?;
    open::that(&destination).map_err(|err| format!("无法打开 OpenCode 安装包：{err}"))?;

    Ok(ActionResult {
        ok: true,
        message: "OpenCode Desktop 安装包已打开，请按安装窗口提示继续。".into(),
        repo_root: None,
        requires_download: None,
    })
}

#[tauri::command]
fn cancel_opencode_download() -> Result<ActionResult, String> {
    OPENCODE_DOWNLOAD_CANCEL_REQUESTED.store(true, Ordering::Release);
    Ok(ActionResult {
        ok: true,
        message: "正在停止 OpenCode 下载。已下载部分会保留，下次可继续。".into(),
        repo_root: None,
        requires_download: None,
    })
}

#[tauri::command]
fn open_repo_folder() -> Result<ActionResult, String> {
    let repo_root = configured_or_default_repo_root()?;
    let target = if repo_root.exists() {
        repo_root.clone()
    } else {
        nearest_existing_path(&repo_root)
    };
    open::that(&target).map_err(|err| err.to_string())?;
    Ok(ActionResult {
        ok: true,
        message: format!("已打开：{}", display_path(&target)),
        repo_root: None,
        requires_download: None,
    })
}

fn nearest_existing_path(path: &Path) -> PathBuf {
    path.ancestors()
        .find(|ancestor| ancestor.exists())
        .map(Path::to_path_buf)
        .unwrap_or_else(|| path.to_path_buf())
}

#[tauri::command]
fn open_books_folder() -> Result<ActionResult, String> {
    let repo_root = active_lifebook_repo_root()?;
    let preferred = repo_root.join("books").join("zh-Hans");
    let target = if preferred.exists() {
        preferred
    } else {
        repo_root.join("books")
    };
    open::that(&target).map_err(|err| err.to_string())?;
    Ok(ActionResult {
        ok: true,
        message: format!("已打开：{}", display_path(&target)),
        repo_root: None,
        requires_download: None,
    })
}

#[tauri::command]
fn launch_opencode_client() -> Result<ActionResult, String> {
    let install_root = opencode_install_root()?;
    if is_opencode_process_running() {
        return Ok(ActionResult {
            ok: true,
            message: "OpenCode 已启动。".into(),
            repo_root: None,
            requires_download: None,
        });
    }
    if let Some(candidate) = detected_opencode_client(&install_root) {
        open::that(&candidate).map_err(|err| format!("无法启动 OpenCode：{err}"))?;
        return Ok(ActionResult {
            ok: true,
            message: format!("已启动 OpenCode：{}", candidate.display()),
            repo_root: None,
            requires_download: None,
        });
    }

    Err("没有找到已安装的 OpenCode Desktop。请先点击“检查更新/更新 OpenCode”安装官方客户端；如果已经安装，请从系统应用菜单启动一次。".into())
}

#[cfg(test)]
fn git_transfer_args(args: &[&str]) -> Vec<String> {
    git_transfer_args_for_mode(args, GitHttpMode::Http2)
}

fn git_transfer_args_for_mode(args: &[&str], http_mode: GitHttpMode) -> Vec<String> {
    let mut git_args = vec![
        "-c".to_string(),
        format!("http.version={}", http_mode.value()),
        "-c".to_string(),
        format!("http.lowSpeedLimit={GIT_LOW_SPEED_LIMIT_BYTES}"),
        "-c".to_string(),
        format!("http.lowSpeedTime={GIT_LOW_SPEED_TIME_SECONDS}"),
        "-c".to_string(),
        "http.postBuffer=524288000".to_string(),
    ];
    if let Some(proxy_url) = configured_proxy_url_best_effort() {
        git_args.push("-c".to_string());
        git_args.push(format!("http.proxy={proxy_url}"));
    }
    git_args.extend(args.iter().map(|arg| (*arg).to_string()));
    git_args
}

fn lifebook_clone_args(destination: &str) -> Vec<String> {
    vec![
        "clone".to_string(),
        "--depth".to_string(),
        "1".to_string(),
        "--single-branch".to_string(),
        "--filter=blob:none".to_string(),
        "--no-tags".to_string(),
        "--progress".to_string(),
        LIFEBOOK_REPO_URL.to_string(),
        destination.to_string(),
    ]
}

fn taskkill_tree_args(pid: u32) -> Vec<String> {
    vec![
        "/PID".to_string(),
        pid.to_string(),
        "/T".to_string(),
        "/F".to_string(),
    ]
}

fn terminate_process_tree(child: &mut std::process::Child, reason: &str) {
    let pid = child.id();
    append_launcher_log(
        "WARN",
        format!("terminating git process tree pid={pid} reason={reason}"),
    );

    #[cfg(target_os = "windows")]
    {
        let taskkill_args = taskkill_tree_args(pid);
        let mut command = Command::new("taskkill");
        command
            .args(&taskkill_args)
            .stdout(Stdio::piped())
            .stderr(Stdio::piped());
        command.creation_flags(0x08000000);
        match command.output() {
            Ok(output) => {
                append_launcher_log(
                    "WARN",
                    format!(
                        "taskkill completed pid={pid} reason={reason} status={} stdout={} stderr={}",
                        output.status,
                        String::from_utf8_lossy(&output.stdout).trim(),
                        String::from_utf8_lossy(&output.stderr).trim()
                    ),
                );
            }
            Err(error) => {
                append_launcher_log(
                    "ERROR",
                    format!("taskkill failed pid={pid} reason={reason}: {error}"),
                );
                let _ = child.kill();
            }
        }
    }

    #[cfg(not(target_os = "windows"))]
    {
        let _ = child.kill();
    }
}

fn git_output(repo_root: &Path, args: &[&str]) -> Result<String, String> {
    append_launcher_log(
        "DEBUG",
        format!("git start cwd={} args={args:?}", display_path(repo_root)),
    );
    let mut command = Command::new("git");
    command.args(args).current_dir(repo_root);
    apply_network_env(&mut command, Some(repo_root));
    #[cfg(target_os = "windows")]
    command.creation_flags(0x08000000);
    let output = command.output().map_err(|err| {
        let message =
            format!("无法执行 git：{err}。请确认已安装 Git，或重新运行 LifeBook Launcher 安装包。");
        append_launcher_log(
            "ERROR",
            format!(
                "git spawn failed cwd={} args={args:?}: {message}",
                display_path(repo_root)
            ),
        );
        message
    })?;
    if output.status.success() {
        let stdout = String::from_utf8_lossy(&output.stdout).trim().to_string();
        append_launcher_log(
            "DEBUG",
            format!(
                "git ok cwd={} args={args:?} stdout={stdout}",
                display_path(repo_root)
            ),
        );
        Ok(stdout)
    } else {
        let stderr = String::from_utf8_lossy(&output.stderr).trim().to_string();
        let message = if stderr.is_empty() {
            format!("git {:?} 执行失败", args)
        } else {
            stderr
        };
        append_launcher_log(
            "ERROR",
            format!(
                "git failed cwd={} args={args:?}: {message}",
                display_path(repo_root)
            ),
        );
        Err(message)
    }
}

fn git_exit_code(repo_root: &Path, args: &[&str]) -> Result<i32, String> {
    append_launcher_log(
        "DEBUG",
        format!("git check cwd={} args={args:?}", display_path(repo_root)),
    );
    let mut command = Command::new("git");
    command.args(args).current_dir(repo_root);
    apply_network_env(&mut command, Some(repo_root));
    #[cfg(target_os = "windows")]
    command.creation_flags(0x08000000);
    let output = command.output().map_err(|err| {
        let message =
            format!("无法执行 git：{err}。请确认已安装 Git，或重新运行 LifeBook Launcher 安装包。");
        append_launcher_log(
            "ERROR",
            format!(
                "git check spawn failed cwd={} args={args:?}: {message}",
                display_path(repo_root)
            ),
        );
        message
    })?;
    let code = output.status.code().unwrap_or(2);
    if code == 0 || code == 1 {
        append_launcher_log(
            "DEBUG",
            format!(
                "git check exit cwd={} args={args:?} code={code}",
                display_path(repo_root)
            ),
        );
        Ok(code)
    } else {
        let stderr = String::from_utf8_lossy(&output.stderr).trim().to_string();
        let message = if stderr.is_empty() {
            format!("git {:?} 执行失败", args)
        } else {
            stderr
        };
        append_launcher_log(
            "ERROR",
            format!(
                "git check failed cwd={} args={args:?} code={code}: {message}",
                display_path(repo_root)
            ),
        );
        Err(message)
    }
}

fn has_tracked_changes(repo_root: &Path) -> Result<bool, String> {
    let worktree_changed =
        git_exit_code(repo_root, &["diff", "--quiet", "--ignore-submodules", "--"])? == 1;
    if worktree_changed {
        return Ok(true);
    }
    let staged_changed = git_exit_code(
        repo_root,
        &["diff", "--cached", "--quiet", "--ignore-submodules", "--"],
    )? == 1;
    Ok(staged_changed)
}

fn git_output_with_timeout(
    repo_root: &Path,
    args: &[&str],
    timeout: Duration,
) -> Result<String, String> {
    let mut last_error = None;
    for mode in [GitHttpMode::Http2, GitHttpMode::Http11] {
        match git_output_with_timeout_once(repo_root, args, timeout, mode) {
            Ok(output) => return Ok(output),
            Err(error) if should_retry_git_transfer(&error) => {
                append_launcher_log(
                    "WARN",
                    format!(
                        "git timeout transfer failed with {:?}, retrying if possible: {error}",
                        mode
                    ),
                );
                last_error = Some(error);
            }
            Err(error) => return Err(error),
        }
    }
    Err(last_error.unwrap_or_else(|| "Git 网络请求失败。".into()))
}

fn git_output_with_timeout_once(
    repo_root: &Path,
    args: &[&str],
    timeout: Duration,
    http_mode: GitHttpMode,
) -> Result<String, String> {
    let git_args = git_transfer_args_for_mode(args, http_mode);
    append_launcher_log(
        "DEBUG",
        format!(
            "git timeout start cwd={} args={git_args:?} timeout_ms={}",
            display_path(repo_root),
            timeout.as_millis()
        ),
    );
    let mut command = Command::new("git");
    command
        .args(&git_args)
        .current_dir(repo_root)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());
    apply_network_env(&mut command, Some(repo_root));
    #[cfg(target_os = "windows")]
    command.creation_flags(0x08000000);

    let mut child = command.spawn().map_err(|err| {
        let message =
            format!("无法执行 git：{err}。请确认已安装 Git，或重新运行 LifeBook Launcher 安装包。");
        append_launcher_log(
            "ERROR",
            format!(
                "git timeout spawn failed cwd={} args={git_args:?}: {message}",
                display_path(repo_root)
            ),
        );
        message
    })?;
    let mut stdout = child
        .stdout
        .take()
        .ok_or_else(|| "无法读取 git 输出。".to_string())?;
    let mut stderr = child
        .stderr
        .take()
        .ok_or_else(|| "无法读取 git 错误输出。".to_string())?;
    let stdout_handle = thread::spawn(move || {
        let mut text = String::new();
        let _ = stdout.read_to_string(&mut text);
        text
    });
    let stderr_handle = thread::spawn(move || {
        let mut text = String::new();
        let _ = stderr.read_to_string(&mut text);
        text
    });

    let started_at = Instant::now();
    let mut timed_out = false;
    let status = loop {
        if !timed_out && started_at.elapsed() >= timeout {
            terminate_process_tree(&mut child, "timeout");
            timed_out = true;
        }
        match child.try_wait().map_err(|err| err.to_string())? {
            Some(status) => break status,
            None => thread::sleep(Duration::from_millis(100)),
        }
    };
    let stdout = stdout_handle.join().unwrap_or_default();
    let stderr = stderr_handle.join().unwrap_or_default();
    if timed_out {
        let message = "检查远端更新超时。请确认网络或代理可连接 GitHub 后重试。".to_string();
        append_launcher_log(
            "ERROR",
            format!(
                "git timeout cwd={} args={git_args:?}: {message}",
                display_path(repo_root)
            ),
        );
        return Err(message);
    }
    if status.success() {
        let stdout = stdout.trim().to_string();
        append_launcher_log(
            "DEBUG",
            format!(
                "git timeout ok cwd={} args={git_args:?} stdout={stdout}",
                display_path(repo_root)
            ),
        );
        Ok(stdout)
    } else {
        let stderr = stderr.trim().to_string();
        let message = if stderr.is_empty() {
            format!("git {:?} 执行失败", &git_args)
        } else {
            stderr
        };
        append_launcher_log(
            "ERROR",
            format!(
                "git timeout failed cwd={} args={git_args:?}: {message}",
                display_path(repo_root)
            ),
        );
        Err(message)
    }
}

fn git_output_with_progress(
    repo_root: &Path,
    args: &[&str],
    progress: Option<&LifeBookProgressEmitter>,
    phase: GitProgressPhase,
) -> Result<String, String> {
    let mut last_error = None;
    for mode in [GitHttpMode::Http2, GitHttpMode::Http11] {
        match git_output_with_progress_once(repo_root, args, progress, phase, mode) {
            Ok(output) => return Ok(output),
            Err(error) if should_retry_git_transfer(&error) => {
                append_launcher_log(
                    "WARN",
                    format!(
                        "git progress transfer failed phase={} mode={:?}, retrying if possible: {error}",
                        git_progress_phase_name(phase),
                        mode
                    ),
                );
                last_error = Some(error);
            }
            Err(error) => return Err(error),
        }
    }
    Err(last_error.unwrap_or_else(|| "Git 网络传输失败。".into()))
}

fn git_output_with_progress_once(
    repo_root: &Path,
    args: &[&str],
    progress: Option<&LifeBookProgressEmitter>,
    phase: GitProgressPhase,
    http_mode: GitHttpMode,
) -> Result<String, String> {
    let git_args = git_transfer_args_for_mode(args, http_mode);
    append_launcher_log(
        "DEBUG",
        format!(
            "git progress start cwd={} phase={} args={git_args:?}",
            display_path(repo_root),
            git_progress_phase_name(phase)
        ),
    );
    let mut command = Command::new("git");
    command
        .args(&git_args)
        .current_dir(repo_root)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());
    apply_network_env(&mut command, Some(repo_root));
    #[cfg(target_os = "windows")]
    command.creation_flags(0x08000000);

    let mut child = command.spawn().map_err(|err| {
        let message =
            format!("无法执行 git：{err}。请确认已安装 Git，或重新运行 LifeBook Launcher 安装包。");
        append_launcher_log(
            "ERROR",
            format!(
                "git progress spawn failed cwd={} phase={} args={git_args:?}: {message}",
                display_path(repo_root),
                git_progress_phase_name(phase)
            ),
        );
        message
    })?;
    let mut stdout = child
        .stdout
        .take()
        .ok_or_else(|| "无法读取 git 输出。".to_string())?;
    let stderr = child
        .stderr
        .take()
        .ok_or_else(|| "无法读取 git 进度。".to_string())?;

    let stdout_handle = thread::spawn(move || {
        let mut text = String::new();
        let _ = stdout.read_to_string(&mut text);
        text
    });
    let progress_emitter = progress.cloned();
    let stderr_handle = thread::spawn(move || {
        let mut text = String::new();
        read_git_progress_stderr(stderr, phase, progress_emitter.as_ref(), &mut text);
        text
    });

    let mut stopped = false;
    let status = loop {
        if !stopped && LIFEBOOK_UPDATE_CANCEL_REQUESTED.load(Ordering::Acquire) {
            terminate_process_tree(&mut child, "cancel");
            stopped = true;
        }
        match child.try_wait().map_err(|err| err.to_string())? {
            Some(status) => break status,
            None => thread::sleep(Duration::from_millis(120)),
        }
    };

    let stdout = stdout_handle.join().unwrap_or_default();
    let stderr = stderr_handle.join().unwrap_or_default();
    if stopped {
        let message = progress_message(progress, "stopped");
        append_launcher_log(
            "WARN",
            format!(
                "git progress stopped cwd={} phase={} args={args:?}: {message}",
                display_path(repo_root),
                git_progress_phase_name(phase),
                args = &git_args
            ),
        );
        return Err(message);
    }
    if status.success() {
        let stdout = stdout.trim().to_string();
        append_launcher_log(
            "DEBUG",
            format!(
                "git progress ok cwd={} phase={} args={args:?} stdout={stdout}",
                display_path(repo_root),
                git_progress_phase_name(phase),
                args = &git_args
            ),
        );
        Ok(stdout)
    } else {
        let stderr = stderr.trim().to_string();
        let message = if stderr.is_empty() {
            format!("git {:?} 执行失败", &git_args)
        } else {
            stderr
        };
        append_launcher_log(
            "ERROR",
            format!(
                "git progress failed cwd={} phase={} args={args:?}: {message}",
                display_path(repo_root),
                git_progress_phase_name(phase),
                args = &git_args
            ),
        );
        Err(message)
    }
}

fn git_progress_phase_name(phase: GitProgressPhase) -> &'static str {
    match phase {
        GitProgressPhase::Clone => "clone",
        GitProgressPhase::Fetch => "fetch",
        GitProgressPhase::Pull => "pull",
    }
}

fn should_retry_git_transfer(error: &str) -> bool {
    let lower = error.to_ascii_lowercase();
    !lower.contains("已停止")
        && (lower.contains("curl 18")
            || lower.contains("early eof")
            || lower.contains("invalid index-pack")
            || lower.contains("unexpected disconnect")
            || lower.contains("rpc failed")
            || lower.contains("http/2")
            || lower.contains("http2")
            || lower.contains("stream")
            || lower.contains("connection")
            || lower.contains("timed out")
            || lower.contains("timeout")
            || lower.contains("operation too slow"))
}

fn read_git_progress_stderr<R: Read>(
    mut stderr: R,
    phase: GitProgressPhase,
    progress_emitter: Option<&LifeBookProgressEmitter>,
    text: &mut String,
) {
    let mut pending = String::new();
    let mut buffer = [0; 4096];
    loop {
        match stderr.read(&mut buffer) {
            Ok(0) => break,
            Ok(size) => {
                let chunk = String::from_utf8_lossy(&buffer[..size]);
                for fragment in git_progress_fragments_from_chunk(&mut pending, &chunk) {
                    handle_git_progress_fragment(phase, progress_emitter, text, &fragment);
                }
            }
            Err(error) => {
                append_launcher_log(
                    "WARN",
                    format!(
                        "git progress stderr read failed phase={}: {error}",
                        git_progress_phase_name(phase)
                    ),
                );
                break;
            }
        }
    }
    if !pending.trim().is_empty() {
        handle_git_progress_fragment(phase, progress_emitter, text, &pending);
    }
}

fn git_progress_fragments_from_chunk(pending: &mut String, chunk: &str) -> Vec<String> {
    let mut fragments = Vec::new();
    for character in chunk.chars() {
        if character == '\r' || character == '\n' {
            if !pending.trim().is_empty() {
                fragments.push(pending.trim().to_string());
            }
            pending.clear();
        } else {
            pending.push(character);
        }
    }
    fragments
}

fn handle_git_progress_fragment(
    phase: GitProgressPhase,
    progress_emitter: Option<&LifeBookProgressEmitter>,
    text: &mut String,
    fragment: &str,
) {
    append_launcher_log(
        "DEBUG",
        format!(
            "git progress stderr phase={} line={fragment}",
            git_progress_phase_name(phase)
        ),
    );
    if let Some(emitter) = progress_emitter {
        emitter.emit_git_progress(phase, fragment);
    }
    text.push_str(fragment);
    text.push('\n');
}

fn ensure_lifebook_project_exists(
    repo_root: &Path,
    progress: Option<&LifeBookProgressEmitter>,
) -> Result<(), String> {
    append_launcher_log(
        "INFO",
        format!(
            "ensure_lifebook_project_exists repo_root={} status={}",
            display_path(repo_root),
            repo_status_for_path(repo_root)
        ),
    );
    if is_lifebook_repo(repo_root) {
        write_launcher_config(repo_root)?;
        return Ok(());
    }

    if repo_root.exists() && !is_dir_empty(repo_root) {
        return Err(format!(
            "LifeBook 项目目录已存在但不是有效项目：{}。请在设置里选择一个空目录，或选择已有 LifeBook 项目目录。",
            display_path(repo_root)
        ));
    }

    let parent = repo_root
        .parent()
        .ok_or_else(|| format!("无法解析 LifeBook 项目目录：{}", display_path(repo_root)))?;
    fs::create_dir_all(parent).map_err(|err| format!("无法创建 LifeBook 项目父目录：{err}"))?;
    clone_lifebook_repo(parent, repo_root, progress)?;

    if !is_lifebook_repo(repo_root) {
        return Err(format!(
            "LifeBook 项目下载完成后校验失败：{}。请检查网络、代理或 Git 设置。",
            display_path(repo_root)
        ));
    }

    write_launcher_config(repo_root)
}

fn clone_lifebook_repo(
    parent: &Path,
    repo_root: &Path,
    progress: Option<&LifeBookProgressEmitter>,
) -> Result<(), String> {
    let clone_dir = managed_clone_dir(repo_root)?;
    if let Some(emitter) = progress {
        emitter.emit_key(10, "clone_start");
    }
    let destination = display_path(&clone_dir);
    append_launcher_log(
        "INFO",
        format!(
            "cloning LifeBook repo parent={} temp_dir={destination} final_dir={}",
            display_path(parent),
            display_path(repo_root)
        ),
    );
    let clone_args = lifebook_clone_args(&destination);
    let clone_arg_refs: Vec<&str> = clone_args.iter().map(String::as_str).collect();
    let mut last_error = None;
    for mode in [GitHttpMode::Http2, GitHttpMode::Http11] {
        if clone_dir.exists() {
            append_launcher_log(
                "WARN",
                format!(
                    "removing stale LifeBook temp clone dir {}",
                    display_path(&clone_dir)
                ),
            );
            fs::remove_dir_all(&clone_dir)
                .map_err(|err| format!("无法整理上次未完成的 LifeBook 临时下载目录：{err}"))?;
        }
        match git_output_with_progress_once(
            parent,
            &clone_arg_refs,
            progress,
            GitProgressPhase::Clone,
            mode,
        ) {
            Ok(_) => {
                finalize_lifebook_clone(&clone_dir, repo_root)?;
                return Ok(());
            }
            Err(error) if should_retry_git_transfer(&error) => {
                append_launcher_log(
                    "WARN",
                    format!(
                        "LifeBook clone failed with {:?}, retrying if possible: {error}",
                        mode
                    ),
                );
                last_error = Some(error);
            }
            Err(error) => return Err(error),
        }
    }
    if clone_dir.exists() {
        let _ = fs::remove_dir_all(&clone_dir);
    }
    let message = last_error.unwrap_or_else(|| "LifeBook 下载失败。".into());
    return Err(format!(
        "{message}\n建议：在设置页配置可用代理并测试通过后重试；如果直连 GitHub 长期低于 100 KiB/s，首次下载很容易中断。"
    ));
}

fn finalize_lifebook_clone(clone_dir: &Path, repo_root: &Path) -> Result<(), String> {
    if repo_root.exists() {
        if is_dir_empty(repo_root) {
            fs::remove_dir_all(repo_root)
                .map_err(|err| format!("无法替换空的 LifeBook 项目目录：{err}"))?;
        } else if !is_lifebook_repo(repo_root) {
            return Err(format!(
                "LifeBook 项目目录已被其他文件占用：{}。请在设置里选择一个空目录，或先整理该目录。",
                display_path(repo_root)
            ));
        }
    }
    fs::rename(&clone_dir, repo_root).map_err(|err| {
        let message = format!(
            "无法移动 LifeBook 下载目录到项目目录：{err}。临时目录：{}",
            display_path(&clone_dir)
        );
        append_launcher_log("ERROR", &message);
        message
    })
}

fn managed_clone_dir(repo_root: &Path) -> Result<PathBuf, String> {
    let name = repo_root
        .file_name()
        .and_then(|value| value.to_str())
        .ok_or_else(|| format!("无法解析 LifeBook 项目目录：{}", display_path(repo_root)))?;
    let parent = repo_root
        .parent()
        .ok_or_else(|| format!("无法解析 LifeBook 项目父目录：{}", display_path(repo_root)))?;
    Ok(parent.join(format!(".{name}.lifebook-download")))
}

fn update_lifebook_project_at(
    repo_root: &Path,
    progress: Option<&LifeBookProgressEmitter>,
) -> Result<(), String> {
    append_launcher_log(
        "INFO",
        format!(
            "update_lifebook_project_at repo_root={}",
            display_path(repo_root)
        ),
    );
    if !is_lifebook_repo(repo_root) {
        return Err(format!(
            "LifeBook 项目尚未准备完成：{}。请等待自动准备完成，或在设置里选择项目目录。",
            display_path(repo_root)
        ));
    }
    if let Some(emitter) = progress {
        emitter.emit_key(8, "local_check");
    }
    let dirty = has_tracked_changes(repo_root)?;
    if dirty {
        append_launcher_log(
            "WARN",
            format!(
                "skip LifeBook update because tracked changes exist repo_root={}",
                display_path(repo_root)
            ),
        );
        return Err(
            "检测到 LifeBook 项目目录内有本地修改。为避免覆盖用户文件，已跳过自动更新。".into(),
        );
    }
    if let Some(emitter) = progress {
        emitter.emit_key(18, "remote_check");
    }
    match remote_matches_local_head(repo_root) {
        Ok(true) => {
            append_launcher_log(
                "INFO",
                format!(
                    "LifeBook repo already matches remote repo_root={}",
                    display_path(repo_root)
                ),
            );
            if let Some(emitter) = progress {
                emitter.emit_key(94, "no_updates");
            }
            return Ok(());
        }
        Ok(false) => {}
        Err(error) => return Err(error),
    }
    if let Some(emitter) = progress {
        emitter.emit_key(30, "fetch_start");
    }
    git_output_with_progress(
        repo_root,
        &["fetch", "--progress", "origin", "--prune"],
        progress,
        GitProgressPhase::Fetch,
    )?;
    if let Some(emitter) = progress {
        emitter.emit_key(78, "pull_start");
    }
    git_output_with_progress(
        repo_root,
        &["pull", "--progress", "--ff-only"],
        progress,
        GitProgressPhase::Pull,
    )?;
    Ok(())
}

fn ensure_books_node_modules(
    repo_root: &Path,
    progress: Option<&NodeModulesProgressEmitter>,
) -> Result<(), String> {
    let books_dir = repo_root.join("books");
    let package_json = books_dir.join("package.json");
    let package_lock = books_dir.join("package-lock.json");
    if !package_json.is_file() {
        append_launcher_log(
            "WARN",
            format!(
                "skip npm install because books/package.json is missing repo_root={}",
                display_path(repo_root)
            ),
        );
        return Ok(());
    }
    if books_node_modules_ready(repo_root) {
        append_launcher_log(
            "INFO",
            format!(
                "books/node_modules already ready repo_root={}",
                display_path(repo_root)
            ),
        );
        if let Some(emitter) = progress {
            emitter.emit(
                100.0,
                100,
                100,
                "EPUB 构建依赖已准备完成。".into(),
                Some("success"),
            );
        }
        return Ok(());
    }
    if let Some(emitter) = progress {
        emitter.emit(
            1.0,
            0,
            estimate_node_modules_total_bytes(&books_dir),
            "正在后台安装 EPUB 构建依赖...".into(),
            Some("downloading"),
        );
    }
    let primary = run_npm_install(
        repo_root,
        &books_dir,
        &package_lock,
        NPM_PRIMARY_REGISTRY,
        progress,
    );
    match primary {
        Ok(_) => Ok(()),
        Err(primary_error) => {
            if NODE_MODULES_INSTALL_CANCEL_REQUESTED.load(Ordering::Acquire) {
                return Err(primary_error);
            }
            append_launcher_log(
                "WARN",
                format!(
                    "npm install with primary registry failed, retrying CN mirror: {primary_error}"
                ),
            );
            if let Some(emitter) = progress {
                emitter.emit(
                    48.0,
                    0,
                    estimate_node_modules_total_bytes(&books_dir),
                    "默认 npm registry 失败，正在切换国内镜像重试...".into(),
                    Some("downloading"),
                );
            }
            run_npm_install(repo_root, &books_dir, &package_lock, NPM_CN_REGISTRY, progress).map_err(|mirror_error| {
                format!(
                    "LifeBook 项目已下载，但 books/node_modules 自动安装失败。默认 registry：{primary_error}；国内镜像重试：{mirror_error}"
                )
            })
        }
    }
}

fn run_npm_install(
    repo_root: &Path,
    books_dir: &Path,
    package_lock: &Path,
    registry: &str,
    progress: Option<&NodeModulesProgressEmitter>,
) -> Result<(), String> {
    let mut args = if package_lock.is_file() {
        vec!["ci".to_string()]
    } else {
        vec!["install".to_string()]
    };
    args.extend([
        "--omit=dev".to_string(),
        "--no-audit".to_string(),
        "--fund=false".to_string(),
        format!("--registry={registry}"),
        "--replace-registry-host=always".to_string(),
        "--fetch-retries=3".to_string(),
        "--fetch-retry-mintimeout=10000".to_string(),
        "--fetch-retry-maxtimeout=60000".to_string(),
    ]);
    command_output_with_timeout_and_node_progress(
        books_dir,
        Some(repo_root),
        npm_program(),
        &args,
        Duration::from_secs(NPM_INSTALL_TIMEOUT_SECONDS),
        "npm install",
        progress,
    )?;
    Ok(())
}

fn collect_node_modules_status() -> Result<NodeModulesStatus, String> {
    let repo_root = configured_or_default_repo_root()?;
    let repo_ready = is_lifebook_repo(&repo_root);
    let books_dir = repo_root.join("books");
    let node_modules_dir = books_dir.join("node_modules");
    Ok(NodeModulesStatus {
        ready: repo_ready && books_node_modules_ready(&repo_root),
        running: NODE_MODULES_INSTALL_RUNNING.load(Ordering::Acquire),
        auto_install: read_launcher_config()
            .as_ref()
            .map(auto_install_node_modules_enabled_from_config)
            .unwrap_or(true),
        repo_ready,
        books_dir: display_path(&books_dir),
        node_modules_dir: display_path(&node_modules_dir),
    })
}

fn books_node_modules_ready(repo_root: &Path) -> bool {
    repo_root
        .join("books")
        .join("node_modules")
        .join("epubchecker")
        .join("package.json")
        .is_file()
}

#[derive(Clone, Copy, Debug, Default)]
struct NodeModulesInstallSnapshot {
    files: u64,
    bytes: u64,
}

fn node_modules_snapshot(books_dir: &Path) -> NodeModulesInstallSnapshot {
    let node_modules_dir = books_dir.join("node_modules");
    let mut snapshot = NodeModulesInstallSnapshot::default();
    accumulate_node_modules_snapshot(&node_modules_dir, &mut snapshot);
    snapshot
}

fn accumulate_node_modules_snapshot(path: &Path, snapshot: &mut NodeModulesInstallSnapshot) {
    let Ok(entries) = fs::read_dir(path) else {
        return;
    };
    for entry in entries.flatten() {
        let entry_path = entry.path();
        let Ok(metadata) = entry.metadata() else {
            continue;
        };
        if metadata.is_dir() {
            accumulate_node_modules_snapshot(&entry_path, snapshot);
        } else if metadata.is_file() {
            snapshot.files = snapshot.files.saturating_add(1);
            snapshot.bytes = snapshot.bytes.saturating_add(metadata.len());
        }
    }
}

fn estimate_node_modules_total_files(books_dir: &Path) -> u64 {
    if let Some(count) = package_lock_package_count(&books_dir.join("package-lock.json")) {
        return (count.saturating_mul(180)).clamp(800, 12000);
    }
    3000
}

fn package_lock_package_count(path: &Path) -> Option<u64> {
    let text = fs::read_to_string(path).ok()?;
    let json: serde_json::Value = serde_json::from_str(&text).ok()?;
    let count = json.get("packages")?.as_object()?.len() as u64;
    Some(count.max(1))
}

fn estimate_node_modules_total_bytes(_books_dir: &Path) -> u64 {
    40 * 1024 * 1024
}

fn node_modules_progress_percent(files: u64, total_files: u64) -> f64 {
    if total_files == 0 {
        return 1.0;
    }
    clamp_progress_percent(((files as f64 / total_files as f64) * 95.0).clamp(1.0, 98.0))
}

fn node_modules_progress_detail(
    current_files: u64,
    total_files: u64,
    current_bytes: u64,
    bytes_per_second: u64,
) -> String {
    format!(
        "({current_files}/{total_files}), {} | {}/s",
        format_mib(current_bytes),
        format_mib(bytes_per_second)
    )
}

fn format_mib(bytes: u64) -> String {
    format!("{:.2} MiB", bytes as f64 / 1024.0 / 1024.0)
}

fn remove_node_modules_dir_safely(repo_root: &Path) -> Result<(), String> {
    let node_modules = repo_root.join("books").join("node_modules");
    if !node_modules.exists() {
        return Ok(());
    }
    let repo_root = repo_root.canonicalize().map_err(|err| err.to_string())?;
    let node_modules = node_modules.canonicalize().map_err(|err| err.to_string())?;
    let expected = repo_root.join("books").join("node_modules");
    if node_modules != expected || !node_modules.starts_with(&repo_root) {
        return Err(format!(
            "拒绝清理非预期 node_modules 路径：{}",
            display_path(&node_modules)
        ));
    }
    fs::remove_dir_all(&node_modules).map_err(|err| err.to_string())
}

fn npm_program() -> &'static str {
    #[cfg(target_os = "windows")]
    {
        "npm.cmd"
    }
    #[cfg(not(target_os = "windows"))]
    {
        "npm"
    }
}

fn command_output_with_timeout_and_node_progress(
    cwd: &Path,
    repo_root: Option<&Path>,
    program: &str,
    args: &[String],
    timeout: Duration,
    label: &str,
    progress: Option<&NodeModulesProgressEmitter>,
) -> Result<String, String> {
    append_launcher_log(
        "INFO",
        format!(
            "{label} start cwd={} program={} args={args:?} timeout_ms={} with_node_progress=true",
            display_path(cwd),
            program,
            timeout.as_millis()
        ),
    );
    let mut command = Command::new(program);
    command
        .args(args)
        .current_dir(cwd)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());
    apply_network_env(&mut command, repo_root);
    #[cfg(target_os = "windows")]
    command.creation_flags(0x08000000);

    let mut child = command.spawn().map_err(|err| {
        format!("无法执行 {program}：{err}。请确认已安装 Node.js/npm，或重新运行 LifeBook Launcher 安装包。")
    })?;
    let mut stdout = child
        .stdout
        .take()
        .ok_or_else(|| format!("无法读取 {label} 输出。"))?;
    let mut stderr = child
        .stderr
        .take()
        .ok_or_else(|| format!("无法读取 {label} 错误输出。"))?;
    let stdout_handle = thread::spawn(move || {
        let mut text = String::new();
        let _ = stdout.read_to_string(&mut text);
        text
    });
    let stderr_handle = thread::spawn(move || {
        let mut text = String::new();
        let _ = stderr.read_to_string(&mut text);
        text
    });

    let started_at = Instant::now();
    let mut last_emit_at = Instant::now() - Duration::from_secs(2);
    let mut last_snapshot_at = started_at;
    let mut last_snapshot = NodeModulesInstallSnapshot::default();
    let total_files = estimate_node_modules_total_files(cwd);
    let total_bytes = estimate_node_modules_total_bytes(cwd);
    let mut timed_out = false;
    let mut cancelled = false;
    let status = loop {
        if NODE_MODULES_INSTALL_CANCEL_REQUESTED.load(Ordering::Acquire) {
            terminate_process_tree(&mut child, "node modules cancel");
            cancelled = true;
        } else if !timed_out && started_at.elapsed() >= timeout {
            terminate_process_tree(&mut child, "timeout");
            timed_out = true;
        }
        if let Some(emitter) = progress {
            if last_emit_at.elapsed() >= Duration::from_millis(700) {
                let snapshot = node_modules_snapshot(cwd);
                let elapsed = last_snapshot_at.elapsed().as_secs_f64().max(0.001);
                let byte_delta = snapshot.bytes.saturating_sub(last_snapshot.bytes);
                let bytes_per_second = (byte_delta as f64 / elapsed).round() as u64;
                let detail = node_modules_progress_detail(
                    snapshot.files,
                    total_files,
                    snapshot.bytes,
                    bytes_per_second,
                );
                let percent = node_modules_progress_percent(snapshot.files, total_files);
                emitter.emit(
                    percent,
                    snapshot.bytes,
                    total_bytes.max(snapshot.bytes),
                    format!("正在后台安装 EPUB 构建依赖... {detail}"),
                    Some("downloading"),
                );
                last_emit_at = Instant::now();
                last_snapshot_at = last_emit_at;
                last_snapshot = snapshot;
            }
        }
        match child.try_wait().map_err(|err| err.to_string())? {
            Some(status) => break status,
            None => {
                if cancelled {
                    thread::sleep(Duration::from_millis(100));
                } else {
                    thread::sleep(Duration::from_millis(200));
                }
            }
        }
    };
    let stdout = stdout_handle.join().unwrap_or_default();
    let stderr = stderr_handle.join().unwrap_or_default();
    if cancelled {
        return Err(format!("{label} 已停止。"));
    }
    if timed_out {
        return Err(format!("{label} 超时。"));
    }
    if status.success() {
        append_launcher_log(
            "INFO",
            format!(
                "{label} ok cwd={} stdout={}",
                display_path(cwd),
                stdout.trim()
            ),
        );
        if let Some(emitter) = progress {
            let snapshot = node_modules_snapshot(cwd);
            emitter.emit(
                99.0,
                snapshot.bytes,
                total_bytes.max(snapshot.bytes),
                "正在确认 EPUB 构建依赖...".into(),
                Some("downloading"),
            );
        }
        Ok(stdout)
    } else {
        let stderr = stderr.trim().to_string();
        let message = if stderr.is_empty() {
            format!("{label} 执行失败：{status}")
        } else {
            stderr
        };
        append_launcher_log(
            "ERROR",
            format!(
                "{label} failed cwd={} status={status}: {message}",
                display_path(cwd)
            ),
        );
        Err(message)
    }
}

impl LifeBookProgressEmitter {
    fn new(app: tauri::AppHandle, locale: Option<String>) -> Self {
        Self { app, locale }
    }

    fn emit_key(&self, percent: u8, key: &str) {
        self.emit(
            percent as f64,
            lifebook_progress_message(self.locale.as_deref(), key),
        );
    }

    fn emit(&self, percent: f64, message: String) {
        let percent = clamp_progress_percent(percent);
        let payload = DownloadProgress {
            percent,
            downloaded_bytes: percent.round() as u64,
            total_bytes: 100,
            message: Some(message),
            state: None,
        };
        let _ = self.app.emit(LIFEBOOK_PROGRESS_EVENT, payload.clone());
        if let Some(window) = self.app.get_webview_window("main") {
            let _ = window.emit(LIFEBOOK_PROGRESS_EVENT, payload);
        }
    }

    fn emit_git_progress(&self, phase: GitProgressPhase, line: &str) {
        if let Some((percent, key)) = git_progress_for_line(phase, line) {
            let mut message = lifebook_progress_message(self.locale.as_deref(), key);
            if let Some(detail) = git_progress_detail(line) {
                message = format!("{detail} - {message}");
            }
            self.emit(percent, message);
        }
    }
}

impl NodeModulesProgressEmitter {
    fn new(app: tauri::AppHandle) -> Self {
        Self { app }
    }

    fn emit(
        &self,
        percent: f64,
        downloaded_bytes: u64,
        total_bytes: u64,
        message: String,
        state: Option<&str>,
    ) {
        let payload = DownloadProgress {
            percent: clamp_progress_percent(percent),
            downloaded_bytes,
            total_bytes,
            message: Some(message),
            state: state.map(|value| value.to_string()),
        };
        let _ = self.app.emit(NODE_MODULES_PROGRESS_EVENT, payload.clone());
        if let Some(window) = self.app.get_webview_window("main") {
            let _ = window.emit(NODE_MODULES_PROGRESS_EVENT, payload);
        }
    }
}

fn progress_message(progress: Option<&LifeBookProgressEmitter>, key: &str) -> String {
    lifebook_progress_message(progress.and_then(|emitter| emitter.locale.as_deref()), key)
}

fn lifebook_progress_message(locale: Option<&str>, key: &str) -> String {
    let language = locale.unwrap_or("").to_ascii_lowercase();
    let is_ja = language.starts_with("ja");
    let is_en = language.starts_with("en");
    match key {
        "prepare_start" if is_ja => "LifeBook プロジェクトを準備しています...".into(),
        "prepare_start" if is_en => "Preparing the LifeBook project...".into(),
        "prepare_start" => "正在准备 LifeBook 项目...".into(),
        "sync_start" if is_ja => "LifeBook プロジェクトを同期しています...".into(),
        "sync_start" if is_en => "Syncing the LifeBook project...".into(),
        "sync_start" => "正在同步 LifeBook 项目...".into(),
        "clone_start" if is_ja => "LifeBook をダウンロードしています...".into(),
        "clone_start" if is_en => "Downloading LifeBook...".into(),
        "clone_start" => "正在下载 LifeBook 项目...".into(),
        "clone_compressing" if is_ja => "LifeBook ファイルを準備しています...".into(),
        "clone_compressing" if is_en => "Preparing LifeBook files...".into(),
        "clone_compressing" => "正在准备 LifeBook 文件...".into(),
        "clone_receiving" if is_ja => "LifeBook ファイルを受信しています...".into(),
        "clone_receiving" if is_en => "Receiving LifeBook files...".into(),
        "clone_receiving" => "正在接收 LifeBook 文件...".into(),
        "clone_resolving" if is_ja => "LifeBook ファイルを整理しています...".into(),
        "clone_resolving" if is_en => "Resolving LifeBook files...".into(),
        "clone_resolving" => "正在整理 LifeBook 文件...".into(),
        "local_check" if is_ja => "ローカル変更を確認しています...".into(),
        "local_check" if is_en => "Checking local changes...".into(),
        "local_check" => "正在检查本地改动...".into(),
        "remote_check" if is_ja => "リモートの更新を確認しています...".into(),
        "remote_check" if is_en => "Checking remote updates...".into(),
        "remote_check" => "正在确认远端更新...".into(),
        "no_updates" if is_ja => "LifeBook はすでに最新です".into(),
        "no_updates" if is_en => "LifeBook is already up to date".into(),
        "no_updates" => "LifeBook 已是最新版本".into(),
        "fetch_start" if is_ja => "更新情報を確認しています...".into(),
        "fetch_start" if is_en => "Checking LifeBook updates...".into(),
        "fetch_start" => "正在检查 LifeBook 更新...".into(),
        "fetch_compressing" if is_ja => "更新ファイルを準備しています...".into(),
        "fetch_compressing" if is_en => "Preparing update files...".into(),
        "fetch_compressing" => "正在准备更新文件...".into(),
        "fetch_receiving" if is_ja => "更新ファイルを受信しています...".into(),
        "fetch_receiving" if is_en => "Receiving update files...".into(),
        "fetch_receiving" => "正在接收更新文件...".into(),
        "fetch_resolving" if is_ja => "更新ファイルを整理しています...".into(),
        "fetch_resolving" if is_en => "Resolving update files...".into(),
        "fetch_resolving" => "正在整理更新文件...".into(),
        "pull_start" if is_ja => "更新を適用しています...".into(),
        "pull_start" if is_en => "Applying LifeBook updates...".into(),
        "pull_start" => "正在应用 LifeBook 更新...".into(),
        "npm_install_start" if is_ja => "EPUB ビルド用 Node.js 依存関係を準備しています...".into(),
        "npm_install_start" if is_en => "Preparing EPUB build dependencies...".into(),
        "npm_install_start" => "正在准备 EPUB 构建依赖...".into(),
        "read_changes" if is_ja => "更新内容を読み込んでいます...".into(),
        "read_changes" if is_en => "Reading update details...".into(),
        "read_changes" => "正在读取更新内容...".into(),
        "complete" if is_ja => "LifeBook の同期が完了しました".into(),
        "complete" if is_en => "LifeBook sync completed".into(),
        "complete" => "LifeBook 同步完成".into(),
        "stopped" if is_ja => "LifeBook の準備/同期を停止しました。次回再試行できます。".into(),
        "stopped" if is_en => "LifeBook prepare/sync stopped. You can retry.".into(),
        "stopped" => "LifeBook 准备/同步已停止，可重试。".into(),
        _ if is_ja => "LifeBook を処理しています...".into(),
        _ if is_en => "Working on LifeBook...".into(),
        _ => "正在处理 LifeBook...".into(),
    }
}

fn git_progress_for_line(phase: GitProgressPhase, line: &str) -> Option<(f64, &'static str)> {
    let lower = line.to_ascii_lowercase();
    let raw = parse_git_percent(line)?;
    if lower.contains("receiving objects") {
        return Some(match phase {
            GitProgressPhase::Clone => (scale_percent(raw, 18, 76), "clone_receiving"),
            GitProgressPhase::Fetch => (scale_percent(raw, 32, 68), "fetch_receiving"),
            GitProgressPhase::Pull => (scale_percent(raw, 78, 88), "fetch_receiving"),
        });
    }
    if lower.contains("compressing objects") {
        return Some(match phase {
            GitProgressPhase::Clone => (scale_percent(raw, 14, 18), "clone_compressing"),
            GitProgressPhase::Fetch => (scale_percent(raw, 30, 34), "fetch_compressing"),
            GitProgressPhase::Pull => (scale_percent(raw, 78, 82), "fetch_compressing"),
        });
    }
    if lower.contains("resolving deltas") {
        return Some(match phase {
            GitProgressPhase::Clone => (scale_percent(raw, 76, 92), "clone_resolving"),
            GitProgressPhase::Fetch => (scale_percent(raw, 68, 78), "fetch_resolving"),
            GitProgressPhase::Pull => (scale_percent(raw, 88, 94), "fetch_resolving"),
        });
    }
    if lower.contains("updating files") {
        return Some((scale_percent(raw, 88, 96), "pull_start"));
    }
    if lower.contains("enumerating objects") || lower.contains("counting objects") {
        return Some(match phase {
            GitProgressPhase::Clone => (scale_percent(raw, 10, 18), "clone_start"),
            GitProgressPhase::Fetch => (scale_percent(raw, 30, 35), "fetch_start"),
            GitProgressPhase::Pull => (scale_percent(raw, 78, 82), "pull_start"),
        });
    }
    None
}

fn scale_percent(value: f64, start: u8, end: u8) -> f64 {
    let span = end.saturating_sub(start) as f64;
    clamp_progress_percent(start as f64 + value.clamp(0.0, 100.0) * span / 100.0)
}

fn parse_git_percent(line: &str) -> Option<f64> {
    parse_git_object_percent(line).or_else(|| parse_git_percent_token(line))
}

fn parse_git_percent_token(line: &str) -> Option<f64> {
    let percent_index = line.find('%')?;
    let before_percent = &line[..percent_index];
    let digits_reversed: String = before_percent
        .chars()
        .rev()
        .skip_while(|ch| ch.is_whitespace())
        .take_while(|ch| ch.is_ascii_digit())
        .collect();
    if digits_reversed.is_empty() {
        return None;
    }
    let digits: String = digits_reversed.chars().rev().collect();
    digits
        .parse::<f64>()
        .ok()
        .filter(|value| (0.0..=100.0).contains(value))
}

fn parse_git_object_percent(line: &str) -> Option<f64> {
    let (current, total) = parse_git_object_counts(line)?;
    if total == 0 {
        return None;
    }
    Some(((current as f64 / total as f64) * 100.0).clamp(0.0, 100.0))
}

fn parse_git_object_counts(line: &str) -> Option<(u64, u64)> {
    let open_index = line.find('(')?;
    let rest = &line[open_index + 1..];
    let slash_index = rest.find('/')?;
    let current = rest[..slash_index].trim().parse::<u64>().ok()?;
    let after_slash = &rest[slash_index + 1..];
    let close_index = after_slash.find(')')?;
    let total = after_slash[..close_index].trim().parse::<u64>().ok()?;
    Some((current, total))
}

fn git_progress_detail(line: &str) -> Option<String> {
    let object_detail =
        parse_git_object_counts(line).map(|(current, total)| format!("{current}/{total}"));
    let transfer_detail = git_transfer_detail(line);
    match (object_detail, transfer_detail) {
        (Some(objects), Some(transfer)) => Some(format!("{objects} - {transfer}")),
        (Some(objects), None) => Some(objects),
        (None, Some(transfer)) => Some(transfer),
        (None, None) => None,
    }
}

fn git_transfer_detail(line: &str) -> Option<String> {
    line.split(',')
        .map(|part| {
            part.trim()
                .trim_end_matches("done.")
                .trim_end_matches("done")
                .trim()
        })
        .find(|part| {
            part.contains("B/s")
                || part.contains("bytes")
                || part.contains("KiB")
                || part.contains("MiB")
                || part.contains("GiB")
        })
        .filter(|part| !part.is_empty())
        .map(|part| part.to_string())
}

fn clamp_progress_percent(value: f64) -> f64 {
    if !value.is_finite() {
        return 0.0;
    }
    (value.clamp(0.0, 100.0) * 100.0).round() / 100.0
}

fn lifebook_update_info(
    repo_root: &Path,
    fetch: bool,
    locale: Option<&str>,
) -> Result<LifeBookUpdateInfo, String> {
    if fetch {
        git_output_with_timeout(
            repo_root,
            &["fetch", "origin", "--prune"],
            Duration::from_secs(GIT_FETCH_TIMEOUT_SECONDS),
        )?;
    }

    let remote_ref = remote_default_ref(repo_root);
    let current_commit = git_output(repo_root, &["rev-parse", "--short", "HEAD"])?;
    let counts = git_output(
        repo_root,
        &[
            "rev-list",
            "--left-right",
            "--count",
            &format!("HEAD...{remote_ref}"),
        ],
    )?;
    let (ahead_count, behind_count) = parse_ahead_behind(&counts)?;
    let commits = if behind_count > 0 {
        git_commits_between(repo_root, &remote_ref, locale)?
    } else {
        git_latest_commits(repo_root, 20, locale)?
    };

    Ok(LifeBookUpdateInfo {
        repo_root: display_path(repo_root),
        current_commit: current_commit.trim().to_string(),
        remote_ref,
        behind_count,
        ahead_count,
        has_update: behind_count > 0,
        commits,
    })
}

fn lifebook_update_info_best_effort(
    repo_root: &Path,
    fetch: bool,
    locale: Option<&str>,
) -> Result<LifeBookUpdateInfo, String> {
    match lifebook_update_info(repo_root, fetch, locale) {
        Ok(info) => Ok(info),
        Err(fetch_error) if fetch => lifebook_update_info(repo_root, false, locale)
            .map_err(|local_error| format!("{fetch_error}; {local_error}")),
        Err(error) => Err(error),
    }
}

fn active_lifebook_repo_root() -> Result<PathBuf, String> {
    let configured_root = configured_or_default_repo_root()?;
    active_repo_root_from_configured_path(&configured_root).ok_or_else(|| {
        format!(
            "LifeBook 项目尚未准备完成：{}。请等待自动准备完成，或在设置里选择已有 LifeBook 项目目录。",
            display_path(&configured_root)
        )
    })
}

fn active_repo_root_from_configured_path(path: &Path) -> Option<PathBuf> {
    if !path.exists() {
        return None;
    }
    repo_root_from_path(path)
}

fn repo_root_from_path(path: &Path) -> Option<PathBuf> {
    let canonical = path.canonicalize().unwrap_or_else(|_| path.to_path_buf());
    for ancestor in canonical.ancestors() {
        if is_lifebook_repo(ancestor) {
            return Some(ancestor.to_path_buf());
        }
    }
    None
}

fn is_lifebook_repo(path: &Path) -> bool {
    path.join("AGENTS.md").is_file()
        && path.join("template").join("epub_pipeline").is_dir()
        && path.join("books").is_dir()
}

fn repo_status_for_path(path: &Path) -> String {
    if is_lifebook_repo(path) {
        "ready".into()
    } else if !path.exists() {
        "missing".into()
    } else if is_dir_empty(path) {
        "empty".into()
    } else {
        "occupied".into()
    }
}

fn is_dir_empty(path: &Path) -> bool {
    if !path.exists() {
        return true;
    }
    path.is_dir()
        && fs::read_dir(path)
            .map(|mut entries| entries.next().is_none())
            .unwrap_or(false)
}

fn configured_or_default_repo_root() -> Result<PathBuf, String> {
    if let Some(repo_root) = configured_repo_root() {
        return Ok(repo_root);
    }
    if let Some(repo_root) = lifebook_home_repo_root() {
        return Ok(repo_root);
    }
    default_lifebook_repo_root()
}

fn configured_repo_root() -> Option<PathBuf> {
    if let Some(config) = read_launcher_config() {
        if let Some(repo_root) = config.repo_root {
            if !repo_root.trim().is_empty() {
                return Some(PathBuf::from(repo_root.trim()));
            }
        }
    }
    None
}

fn lifebook_home_repo_root() -> Option<PathBuf> {
    lifebook_home_repo_root_from_value(env::var(LIFEBOOK_HOME_ENV).ok())
}

fn lifebook_home_repo_root_from_value(value: Option<String>) -> Option<PathBuf> {
    value
        .map(|value| value.trim().to_string())
        .filter(|value| !value.is_empty())
        .map(PathBuf::from)
}

fn default_lifebook_repo_root() -> Result<PathBuf, String> {
    #[cfg(target_os = "windows")]
    {
        let d_drive = PathBuf::from(r"D:\");
        if d_drive.exists() {
            return Ok(PathBuf::from(r"D:\LifeBook"));
        }
    }
    let home = dirs::home_dir().ok_or_else(|| "无法定位用户主目录。".to_string())?;
    Ok(home.join("LifeBook"))
}

fn launcher_config_path() -> Result<PathBuf, String> {
    let base = dirs::config_local_dir()
        .or_else(dirs::data_local_dir)
        .ok_or_else(|| "无法定位用户配置目录。".to_string())?;
    Ok(base.join("LifeBook").join("launcher").join("config.json"))
}

fn read_launcher_config() -> Option<LauncherConfig> {
    let path = launcher_config_path().ok()?;
    let text = fs::read_to_string(path).ok()?;
    serde_json::from_str(&text).ok()
}

fn write_launcher_config_file(config: &LauncherConfig) -> Result<(), String> {
    let path = launcher_config_path()?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent).map_err(|err| err.to_string())?;
    }
    let text = serde_json::to_string_pretty(config).map_err(|err| err.to_string())?;
    fs::write(path, text).map_err(|err| err.to_string())
}

fn write_launcher_config(repo_root: &Path) -> Result<(), String> {
    let mut config = read_launcher_config().unwrap_or_default();
    config.repo_root = Some(display_path(repo_root));
    write_launcher_config_file(&config)?;
    append_launcher_log(
        "INFO",
        format!("launcher config repo_root={}", display_path(repo_root)),
    );
    set_process_lifebook_env(repo_root);
    persist_user_lifebook_home_env(repo_root);
    Ok(())
}

fn write_save_logs_config(save_logs: bool) -> Result<(), String> {
    let mut config = read_launcher_config().unwrap_or_default();
    config.save_logs = Some(save_logs);
    write_launcher_config_file(&config)
}

fn write_auto_install_node_modules_config(enabled: bool) -> Result<(), String> {
    let mut config = read_launcher_config().unwrap_or_default();
    config.auto_install_node_modules = Some(enabled);
    write_launcher_config_file(&config)?;
    append_launcher_log("INFO", format!("auto_install_node_modules={enabled}"));
    Ok(())
}

fn configured_proxy_settings() -> NetworkProxySettings {
    read_launcher_config()
        .and_then(|config| config.proxy)
        .unwrap_or_default()
}

fn write_proxy_config(proxy: NetworkProxySettings) -> Result<NetworkProxySettings, String> {
    validate_proxy_settings(&proxy)?;
    let mut config = read_launcher_config().unwrap_or_default();
    config.proxy = Some(proxy.clone());
    write_launcher_config_file(&config)?;
    append_launcher_log(
        "INFO",
        format!(
            "network proxy updated enabled={} scheme={} host={} port={:?}",
            proxy.enabled, proxy.scheme, proxy.host, proxy.port
        ),
    );
    Ok(proxy)
}

fn validate_proxy_settings(proxy: &NetworkProxySettings) -> Result<(), String> {
    let scheme = normalized_proxy_scheme(&proxy.scheme)?;
    if proxy.enabled {
        if proxy.host.trim().is_empty() {
            return Err("代理 IP/主机不能为空。".into());
        }
        let port = proxy.port.ok_or_else(|| "代理端口不能为空。".to_string())?;
        if port == 0 {
            return Err("代理端口必须在 1-65535 之间。".into());
        }
    }
    if scheme.is_empty() {
        return Err("代理协议不能为空。".into());
    }
    Ok(())
}

fn normalized_proxy_scheme(value: &str) -> Result<String, String> {
    let scheme = value.trim().to_ascii_lowercase();
    match scheme.as_str() {
        "http" | "https" | "socks5" | "socks5h" => Ok(scheme),
        _ => Err("代理协议只支持 http、https、socks5、socks5h。".into()),
    }
}

fn configured_proxy_url() -> Result<Option<String>, String> {
    proxy_url_from_settings(&configured_proxy_settings())
}

fn configured_proxy_url_best_effort() -> Option<String> {
    configured_proxy_url().ok().flatten()
}

fn proxy_url_from_settings(proxy: &NetworkProxySettings) -> Result<Option<String>, String> {
    validate_proxy_settings(proxy)?;
    if !proxy.enabled {
        return Ok(None);
    }
    let scheme = normalized_proxy_scheme(&proxy.scheme)?;
    let host = proxy.host.trim();
    let port = proxy.port.ok_or_else(|| "代理端口不能为空。".to_string())?;
    Ok(Some(format!("{scheme}://{host}:{port}")))
}

fn proxy_settings_from_url(value: &str) -> Option<NetworkProxySettings> {
    let trimmed = value.trim().trim_matches('"').trim_matches('\'');
    if trimmed.is_empty() || trimmed.eq_ignore_ascii_case("direct") {
        return None;
    }
    if trimmed.contains(';') {
        return trimmed
            .split(';')
            .filter_map(|part| {
                let value = part.split_once('=').map(|(_, value)| value).unwrap_or(part);
                proxy_settings_from_url(value)
            })
            .next();
    }
    let raw = trimmed
        .split_once('=')
        .map(|(_, value)| value.trim())
        .unwrap_or(trimmed);
    let candidate = if raw.contains("://") {
        raw.to_string()
    } else {
        format!("http://{raw}")
    };
    let url = reqwest::Url::parse(&candidate).ok()?;
    let scheme = normalized_proxy_scheme(url.scheme()).ok()?;
    let host = url.host_str()?.trim_matches(['[', ']']).to_string();
    if host.trim().is_empty() || host.contains(' ') {
        return None;
    }
    let port = url.port()?;
    Some(NetworkProxySettings {
        enabled: true,
        scheme,
        host,
        port: Some(port),
    })
}

fn proxy_detection_candidates() -> Vec<NetworkProxySettings> {
    let mut candidates = Vec::new();
    for name in [
        "HTTPS_PROXY",
        "HTTP_PROXY",
        "ALL_PROXY",
        "https_proxy",
        "http_proxy",
        "all_proxy",
    ] {
        if let Ok(value) = env::var(name) {
            if let Some(proxy) = proxy_settings_from_url(&value) {
                candidates.push(proxy);
            }
        }
    }
    candidates.extend(system_proxy_candidates());
    for value in [
        "http://127.0.0.1:7890",
        "http://127.0.0.1:7897",
        "http://127.0.0.1:10809",
        "socks5h://127.0.0.1:10808",
        "socks5h://127.0.0.1:7891",
        "http://127.0.0.1:20171",
        "http://localhost:7890",
        "http://localhost:10809",
    ] {
        if let Some(proxy) = proxy_settings_from_url(value) {
            candidates.push(proxy);
        }
    }
    dedupe_proxy_candidates(candidates)
}

fn dedupe_proxy_candidates(candidates: Vec<NetworkProxySettings>) -> Vec<NetworkProxySettings> {
    let mut unique = Vec::new();
    for candidate in candidates {
        let Ok(Some(url)) = proxy_url_from_settings(&candidate) else {
            continue;
        };
        let exists = unique
            .iter()
            .filter_map(|item| proxy_url_from_settings(item).ok().flatten())
            .any(|existing| existing.eq_ignore_ascii_case(&url));
        if !exists {
            unique.push(candidate);
        }
    }
    unique
}

#[cfg(target_os = "windows")]
fn system_proxy_candidates() -> Vec<NetworkProxySettings> {
    let mut candidates = Vec::new();
    if let Some(proxy_server) = windows_internet_proxy_server() {
        candidates.extend(parse_proxy_server_list(&proxy_server));
    }
    if let Some(proxy_server) = winhttp_proxy_server() {
        candidates.extend(parse_proxy_server_list(&proxy_server));
    }
    candidates
}

#[cfg(not(target_os = "windows"))]
fn system_proxy_candidates() -> Vec<NetworkProxySettings> {
    Vec::new()
}

#[cfg(target_os = "windows")]
fn windows_internet_proxy_server() -> Option<String> {
    let key = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings";
    let enable_output = hidden_command_output("reg", &["query", key, "/v", "ProxyEnable"]).ok()?;
    let proxy_enabled = enable_output
        .lines()
        .any(|line| line.contains("ProxyEnable") && (line.contains("0x1") || line.ends_with(" 1")));
    if !proxy_enabled {
        return None;
    }
    let server_output = hidden_command_output("reg", &["query", key, "/v", "ProxyServer"]).ok()?;
    registry_value_tail(&server_output, "ProxyServer")
}

#[cfg(target_os = "windows")]
fn winhttp_proxy_server() -> Option<String> {
    let output = hidden_command_output("netsh", &["winhttp", "show", "proxy"]).ok()?;
    output
        .lines()
        .filter_map(|line| {
            line.split_once(':')
                .map(|(_, value)| value.trim().to_string())
        })
        .find(|value| {
            !value.is_empty()
                && !value.to_ascii_lowercase().contains("direct")
                && (value.contains(':') || value.contains('='))
        })
}

#[cfg(target_os = "windows")]
fn hidden_command_output(program: &str, args: &[&str]) -> Result<String, String> {
    let mut command = Command::new(program);
    command.args(args);
    command.creation_flags(0x08000000);
    let output = command.output().map_err(|err| err.to_string())?;
    if !output.status.success() {
        return Err(String::from_utf8_lossy(&output.stderr).trim().to_string());
    }
    Ok(String::from_utf8_lossy(&output.stdout).to_string())
}

#[cfg(target_os = "windows")]
fn registry_value_tail(output: &str, name: &str) -> Option<String> {
    output.lines().find_map(|line| {
        if !line.contains(name) {
            return None;
        }
        line.split_whitespace()
            .last()
            .map(|value| value.to_string())
    })
}

fn parse_proxy_server_list(value: &str) -> Vec<NetworkProxySettings> {
    let mut proxies = Vec::new();
    for part in value.split(';') {
        let raw = part.trim();
        if raw.is_empty() {
            continue;
        }
        if let Some(proxy) = proxy_settings_from_url(raw) {
            proxies.push(proxy);
        }
    }
    if proxies.is_empty() {
        if let Some(proxy) = proxy_settings_from_url(value) {
            proxies.push(proxy);
        }
    }
    proxies
}

fn apply_reqwest_proxy(
    builder: reqwest::ClientBuilder,
    proxy_url: Option<&str>,
) -> Result<reqwest::ClientBuilder, String> {
    if let Some(proxy_url) = proxy_url {
        let proxy = reqwest::Proxy::all(proxy_url).map_err(|err| format!("代理配置无效：{err}"))?;
        Ok(builder.proxy(proxy))
    } else if let Some(proxy_url) = configured_proxy_url_best_effort() {
        let proxy =
            reqwest::Proxy::all(&proxy_url).map_err(|err| format!("代理配置无效：{err}"))?;
        Ok(builder.proxy(proxy))
    } else {
        Ok(builder)
    }
}

fn diagnostic_log_settings() -> Result<DiagnosticLogSettings, String> {
    let log_file = launcher_log_path()?;
    let log_dir = log_file
        .parent()
        .map(Path::to_path_buf)
        .unwrap_or_else(|| log_file.clone());
    Ok(DiagnosticLogSettings {
        save_logs: launcher_logging_enabled(),
        log_dir: display_path(&log_dir),
        log_file: display_path(&log_file),
        max_bytes: LAUNCHER_LOG_MAX_BYTES,
        backup_count: LAUNCHER_LOG_BACKUP_COUNT,
        max_total_bytes: LAUNCHER_LOG_MAX_BYTES * (LAUNCHER_LOG_BACKUP_COUNT as u64 + 1),
    })
}

fn diagnostic_context_for_export(
    launcher_version: &str,
    repo_root: &str,
    repo_status: &str,
    save_logs: bool,
    log_dir: &Path,
    log_max_bytes: u64,
    log_backup_count: usize,
) -> DiagnosticExportContext {
    DiagnosticExportContext {
        generated_at: Local::now().to_rfc3339(),
        launcher_version: launcher_version.to_string(),
        os: env::consts::OS.to_string(),
        arch: env::consts::ARCH.to_string(),
        repo_root: repo_root.to_string(),
        repo_status: repo_status.to_string(),
        save_logs,
        log_dir: display_path(log_dir),
        log_max_bytes,
        log_backup_count,
        lifebook_home_set: env::var(LIFEBOOK_HOME_ENV)
            .map(|value| !value.trim().is_empty())
            .unwrap_or(false),
        proxy_configured: is_proxy_configured(),
    }
}

fn current_diagnostic_context() -> Result<DiagnosticExportContext, String> {
    let repo_root = configured_or_default_repo_root()?;
    let log_file = launcher_log_path()?;
    let log_dir = log_file
        .parent()
        .map(Path::to_path_buf)
        .unwrap_or_else(|| log_file.clone());
    Ok(diagnostic_context_for_export(
        &launcher_current_version(),
        &display_path(&repo_root),
        &repo_status_for_path(&repo_root),
        launcher_logging_enabled(),
        &log_dir,
        LAUNCHER_LOG_MAX_BYTES,
        LAUNCHER_LOG_BACKUP_COUNT,
    ))
}

fn diagnostic_log_files(log_dir: &Path) -> Vec<PathBuf> {
    let current = log_dir.join("lifebook-launcher.log");
    let mut files = Vec::new();
    if current.is_file() {
        files.push(current.clone());
    }
    for index in 1..=LAUNCHER_LOG_BACKUP_COUNT {
        let rotated = rotated_log_path(&current, index);
        if rotated.is_file() {
            files.push(rotated);
        }
    }
    files
}

fn export_diagnostic_logs_to_dir(
    export_parent: &Path,
    log_dir: &Path,
    context: &DiagnosticExportContext,
) -> Result<PathBuf, String> {
    fs::create_dir_all(export_parent).map_err(|err| err.to_string())?;
    let export_dir = export_parent.join(format!(
        "LifeBook-Launcher-Logs-{}",
        Local::now().format("%Y%m%d-%H%M%S")
    ));
    fs::create_dir_all(&export_dir).map_err(|err| err.to_string())?;
    for source in diagnostic_log_files(log_dir) {
        if let Some(file_name) = source.file_name() {
            fs::copy(&source, export_dir.join(file_name)).map_err(|err| err.to_string())?;
        }
    }
    let context_text = serde_json::to_string_pretty(context).map_err(|err| err.to_string())?;
    fs::write(export_dir.join("diagnostic-context.json"), context_text)
        .map_err(|err| err.to_string())?;
    Ok(export_dir)
}

fn set_process_lifebook_env(repo_root: &Path) {
    let value = display_path(repo_root);
    env::set_var(LIFEBOOK_HOME_ENV, value);
}

fn apply_network_env(command: &mut Command, repo_root: Option<&Path>) {
    if let Some(repo_root) = repo_root {
        command.env(LIFEBOOK_HOME_ENV, display_path(repo_root));
    }
    if let Some(proxy_url) = configured_proxy_url_best_effort() {
        command
            .env("HTTPS_PROXY", &proxy_url)
            .env("HTTP_PROXY", &proxy_url)
            .env("ALL_PROXY", &proxy_url)
            .env("https_proxy", &proxy_url)
            .env("http_proxy", &proxy_url)
            .env("all_proxy", &proxy_url);
    }
}

#[cfg(target_os = "windows")]
fn persist_user_lifebook_home_env(repo_root: &Path) {
    let value = display_path(repo_root);
    let current = env::var(LIFEBOOK_HOME_ENV).unwrap_or_default();
    if current.trim().eq_ignore_ascii_case(value.trim()) {
        return;
    }
    let mut command = Command::new("setx");
    command.arg(LIFEBOOK_HOME_ENV).arg(&value);
    command.creation_flags(0x08000000);
    match command.output() {
        Ok(output) if output.status.success() => {
            append_launcher_log("INFO", format!("persisted user LIFEBOOK_HOME={value}"));
        }
        Ok(output) => {
            append_launcher_log(
                "WARN",
                format!(
                    "setx LIFEBOOK_HOME failed status={} stdout={} stderr={}",
                    output.status,
                    String::from_utf8_lossy(&output.stdout).trim(),
                    String::from_utf8_lossy(&output.stderr).trim()
                ),
            );
        }
        Err(error) => {
            append_launcher_log("WARN", format!("setx LIFEBOOK_HOME spawn failed: {error}"));
        }
    }
}

#[cfg(not(target_os = "windows"))]
fn persist_user_lifebook_home_env(_repo_root: &Path) {}

fn display_path(path: &Path) -> String {
    let raw = path.display().to_string();
    if let Some(value) = raw.strip_prefix("\\\\?\\UNC\\") {
        format!("\\\\{value}")
    } else if let Some(value) = raw.strip_prefix("\\\\?\\") {
        value.to_string()
    } else {
        raw
    }
}

fn project_document_candidates(kind: &str, locale: &str) -> Vec<PathBuf> {
    let locale = locale.to_ascii_lowercase();
    let is_traditional =
        locale.starts_with("zh-tw") || locale.starts_with("zh-hk") || locale.starts_with("zh-hant");
    let is_simplified = locale.starts_with("zh");
    let is_japanese = locale.starts_with("ja");

    match kind {
        "howto" => {
            let mut candidates = Vec::new();
            if is_traditional {
                candidates.push(
                    PathBuf::from("doc")
                        .join("public")
                        .join("how-to-use-prompts.zh-TW.md"),
                );
            } else if is_simplified {
                candidates.push(
                    PathBuf::from("doc")
                        .join("public")
                        .join("how-to-use-prompts.zh-CN.md"),
                );
            } else if is_japanese {
                candidates.push(
                    PathBuf::from("doc")
                        .join("public")
                        .join("how-to-use-prompts.ja.md"),
                );
            } else {
                candidates.push(
                    PathBuf::from("doc")
                        .join("public")
                        .join("how-to-use-prompts.en.md"),
                );
            }
            candidates.push(
                PathBuf::from("doc")
                    .join("public")
                    .join("how-to-use-prompts.zh-CN.md"),
            );
            candidates.push(
                PathBuf::from("doc")
                    .join("public")
                    .join("how-to-use-prompts.en.md"),
            );
            candidates.push(
                PathBuf::from("doc")
                    .join("public")
                    .join("how-to-use-prompts.ja.md"),
            );
            candidates
        }
        _ => {
            let mut candidates = Vec::new();
            if is_traditional {
                candidates.push(PathBuf::from("readme").join("README.zh-TW.md"));
            } else if is_simplified {
                candidates.push(PathBuf::from("README.zh-CN.md"));
            } else if is_japanese {
                candidates.push(PathBuf::from("readme").join("README.ja.md"));
            } else {
                candidates.push(PathBuf::from("README.md"));
            }
            candidates.push(PathBuf::from("README.zh-CN.md"));
            candidates.push(PathBuf::from("README.md"));
            candidates.push(PathBuf::from("readme").join("README.zh-TW.md"));
            candidates.push(PathBuf::from("readme").join("README.ja.md"));
            candidates
        }
    }
}

fn read_project_document_file(
    repo_root: &Path,
    relative_path: &Path,
    kind: &str,
) -> Result<ProjectDocument, String> {
    let full_path = repo_root.join(relative_path);
    let content = fs::read_to_string(&full_path)
        .map_err(|err| format!("无法读取文档 {}：{err}", display_path(&full_path)))?;
    let title = markdown_title(&content).unwrap_or_else(|| {
        if kind == "howto" {
            "How to use".into()
        } else {
            "README".into()
        }
    });

    Ok(ProjectDocument {
        kind: kind.to_string(),
        path: display_path(&full_path),
        title,
        content,
    })
}

fn markdown_title(content: &str) -> Option<String> {
    content.lines().find_map(|line| {
        line.trim()
            .strip_prefix("# ")
            .map(|title| title.trim().to_string())
            .filter(|title| !title.is_empty())
    })
}

fn document_kind_from_path(path: &Path) -> String {
    let text = path.to_string_lossy().to_ascii_lowercase();
    if text.contains("how-to-use") {
        "howto".into()
    } else {
        "readme".into()
    }
}

fn safe_project_relative_path(value: &str) -> Result<PathBuf, String> {
    let trimmed = value.trim();
    if trimmed.is_empty()
        || trimmed.starts_with("http://")
        || trimmed.starts_with("https://")
        || trimmed.starts_with("mailto:")
        || trimmed.starts_with('#')
    {
        return Err("只能打开 LifeBook 项目内的 Markdown 文档链接。".into());
    }

    let without_fragment = trimmed
        .split('#')
        .next()
        .unwrap_or(trimmed)
        .split('?')
        .next()
        .unwrap_or(trimmed);
    let normalized = without_fragment
        .replace('\\', "/")
        .trim_start_matches("./")
        .to_string();
    let path = PathBuf::from(&normalized);
    if path.is_absolute() || normalized.contains("://") {
        return Err("只能打开 LifeBook 项目内的相对链接。".into());
    }
    if path.extension().and_then(|value| value.to_str()) != Some("md") {
        return Err("教程页只打开 Markdown 文档链接。".into());
    }
    if path
        .components()
        .any(|component| !matches!(component, std::path::Component::Normal(_)))
    {
        return Err("链接路径不能离开 LifeBook 项目目录。".into());
    }
    Ok(path)
}

fn remote_default_ref(repo_root: &Path) -> String {
    git_output(
        repo_root,
        &["symbolic-ref", "--short", "refs/remotes/origin/HEAD"],
    )
    .ok()
    .filter(|value| !value.trim().is_empty())
    .unwrap_or_else(|| "origin/main".into())
}

fn remote_branch_from_ref(remote_ref: &str) -> String {
    remote_ref
        .trim()
        .strip_prefix("origin/")
        .filter(|value| !value.trim().is_empty())
        .unwrap_or("main")
        .to_string()
}

fn remote_matches_local_head(repo_root: &Path) -> Result<bool, String> {
    let local_head = git_output(repo_root, &["rev-parse", "HEAD"])?;
    let remote_ref = remote_default_ref(repo_root);
    let branch = remote_branch_from_ref(&remote_ref);
    let remote_target = format!("refs/heads/{branch}");
    let remote_head = git_output_with_timeout(
        repo_root,
        &["ls-remote", "origin", &remote_target],
        Duration::from_secs(8),
    )?;
    let Some(remote_hash) = remote_head.split_whitespace().next() else {
        return Err(format!("无法读取远端分支：{remote_target}"));
    };
    Ok(local_head.trim() == remote_hash.trim())
}

fn parse_ahead_behind(value: &str) -> Result<(u32, u32), String> {
    let mut parts = value.split_whitespace();
    let ahead = parts
        .next()
        .ok_or_else(|| "无法解析 Git ahead/behind 结果。".to_string())?
        .parse::<u32>()
        .map_err(|err| err.to_string())?;
    let behind = parts
        .next()
        .ok_or_else(|| "无法解析 Git ahead/behind 结果。".to_string())?
        .parse::<u32>()
        .map_err(|err| err.to_string())?;
    Ok((ahead, behind))
}

fn git_commits_between(
    repo_root: &Path,
    remote_ref: &str,
    locale: Option<&str>,
) -> Result<Vec<CommitInfo>, String> {
    let range = format!("HEAD..{remote_ref}");
    git_log(repo_root, &range, 80, locale)
}

fn git_latest_commits(
    repo_root: &Path,
    max_count: usize,
    locale: Option<&str>,
) -> Result<Vec<CommitInfo>, String> {
    git_log(repo_root, "HEAD", max_count, locale)
}

fn git_log(
    repo_root: &Path,
    rev: &str,
    max_count: usize,
    locale: Option<&str>,
) -> Result<Vec<CommitInfo>, String> {
    let format = "%h%x1f%ci%x1f%s%x1f%b%x1e";
    let output = git_output(
        repo_root,
        &[
            "log",
            &format!("--max-count={max_count}"),
            &format!("--pretty=format:{format}"),
            rev,
        ],
    )?;
    let commits = output
        .split('\u{1e}')
        .filter_map(|entry| {
            let trimmed = entry.trim();
            if trimmed.is_empty() {
                return None;
            }
            let mut parts = trimmed.split('\u{1f}');
            let hash = parts.next().unwrap_or_default().trim().to_string();
            let date = parts.next().unwrap_or_default().trim().to_string();
            let title = parts.next().unwrap_or_default().trim().to_string();
            let body = parts.next().unwrap_or_default();
            Some(CommitInfo {
                hash,
                date,
                full_message: full_commit_message(&title, body),
                title,
                summary: localized_commit_summary(body, locale),
            })
        })
        .collect();
    Ok(commits)
}

fn full_commit_message(title: &str, body: &str) -> String {
    let title = title.trim();
    let body = body.trim();
    match (title.is_empty(), body.is_empty()) {
        (true, true) => String::new(),
        (false, true) => title.to_string(),
        (true, false) => body.to_string(),
        (false, false) => format!("{title}\n\n{body}"),
    }
}

fn localized_commit_summary(body: &str, locale: Option<&str>) -> String {
    let sections = parse_commit_summary_sections(body);
    let preferred = commit_summary_locale_key(locale);
    for key in [preferred, "EN", "ZH", "JA"] {
        if let Some(summary) = sections.iter().find_map(|(section_key, value)| {
            (*section_key == key).then(|| cleanup_commit_summary(value))
        }) {
            if !summary.is_empty() {
                return summary;
            }
        }
    }

    body.lines()
        .map(str::trim)
        .find(|line| !line.is_empty() && !is_commit_summary_label(line))
        .map(cleanup_commit_summary)
        .unwrap_or_default()
}

fn commit_summary_locale_key(locale: Option<&str>) -> &'static str {
    let Some(locale) = locale else {
        return "EN";
    };
    let locale = locale.to_ascii_lowercase();
    if locale.starts_with("ja") {
        "JA"
    } else if locale.starts_with("zh") {
        "ZH"
    } else {
        "EN"
    }
}

fn parse_commit_summary_sections(body: &str) -> Vec<(&'static str, String)> {
    let mut sections: Vec<(&'static str, String)> = Vec::new();
    let mut current_key: Option<&'static str> = None;
    let mut current_lines: Vec<String> = Vec::new();

    let flush = |sections: &mut Vec<(&'static str, String)>,
                 key: &mut Option<&'static str>,
                 lines: &mut Vec<String>| {
        if let Some(value) = key.take() {
            sections.push((value, lines.join("\n")));
            lines.clear();
        }
    };

    for line in body.replace("\r\n", "\n").lines() {
        let trimmed = line.trim();
        if let Some((key, rest)) = commit_summary_label_and_rest(trimmed) {
            flush(&mut sections, &mut current_key, &mut current_lines);
            current_key = Some(key);
            if !rest.trim().is_empty() {
                current_lines.push(rest.trim().to_string());
            }
            continue;
        }
        if current_key.is_some() {
            current_lines.push(line.to_string());
        }
    }
    flush(&mut sections, &mut current_key, &mut current_lines);
    sections
}

fn commit_summary_label_and_rest(line: &str) -> Option<(&'static str, &str)> {
    for key in ["ZH", "EN", "JA"] {
        let label = format!("{key}:");
        if line == label {
            return Some((key, ""));
        }
        if let Some(rest) = line.strip_prefix(&label) {
            return Some((key, rest));
        }
    }
    None
}

fn is_commit_summary_label(line: &str) -> bool {
    commit_summary_label_and_rest(line)
        .map(|(_, rest)| rest.trim().is_empty())
        .unwrap_or(false)
}

fn cleanup_commit_summary(value: &str) -> String {
    value
        .lines()
        .map(|line| {
            line.trim()
                .trim_start_matches("- ")
                .trim_start_matches("* ")
                .trim()
        })
        .filter(|line| !line.is_empty())
        .collect::<Vec<_>>()
        .join(" ")
}

fn http_client() -> Result<reqwest::Client, String> {
    let builder = reqwest::Client::builder().http1_only();
    apply_reqwest_proxy(builder, None)?
        .build()
        .map_err(|err| format!("无法初始化 HTTP/1.1 网络客户端：{err}"))
}

fn http_client_auto() -> Result<reqwest::Client, String> {
    let builder = reqwest::Client::builder();
    apply_reqwest_proxy(builder, None)?
        .build()
        .map_err(|err| format!("无法初始化自动 HTTP 网络客户端：{err}"))
}

async fn test_github_connectivity_via_proxy(
    proxy_url: &str,
    http1_only: bool,
) -> Result<ProxyTestResult, String> {
    test_github_connectivity_via_proxy_with_timeout(
        proxy_url,
        http1_only,
        Duration::from_secs(PROXY_TEST_TIMEOUT_SECONDS),
    )
    .await
}

async fn test_github_connectivity_via_proxy_with_timeout(
    proxy_url: &str,
    http1_only: bool,
    timeout: Duration,
) -> Result<ProxyTestResult, String> {
    let mut builder = reqwest::Client::builder()
        .connect_timeout(timeout)
        .timeout(timeout);
    if http1_only {
        builder = builder.http1_only();
    }
    let client = apply_reqwest_proxy(builder, Some(proxy_url))?
        .build()
        .map_err(|err| format!("无法初始化代理测试客户端：{err}"))?;
    let started_at = Instant::now();
    let response = client
        .get(GITHUB_CONNECTIVITY_TEST_URL)
        .header("User-Agent", "LifeBook-Launcher")
        .send()
        .await
        .map_err(|err| format!("{err}"))?;
    let elapsed_ms = started_at.elapsed().as_millis();
    let status = response.status();
    let version = format!("{:?}", response.version());
    if !status.is_success() {
        return Err(format!("GitHub 返回 HTTP status {status}"));
    }
    Ok(ProxyTestResult {
        ok: true,
        message: format!("代理可连接 GitHub，耗时 {elapsed_ms} ms。"),
        elapsed_ms: Some(elapsed_ms),
        http_version: Some(version),
        target_url: GITHUB_CONNECTIVITY_TEST_URL.into(),
    })
}

async fn fetch_opencode_release() -> Result<GithubRelease, String> {
    fetch_github_release(OPENCODE_REPO_API, "OpenCode").await
}

async fn fetch_opencode_release_asset() -> Result<(String, GithubAsset), String> {
    let asset_name = opencode_asset_name()?;
    match fetch_opencode_release().await {
        Ok(release) => {
            let asset = release
                .assets
                .iter()
                .find(|asset| asset.name == asset_name)
                .cloned()
                .ok_or_else(|| {
                    format!(
                        "OpenCode release 中没有找到当前系统对应的 Desktop 安装包：{asset_name}"
                    )
                })?;
            Ok((release.tag_name, asset))
        }
        Err(api_error) if should_use_public_release_fallback(&api_error) => {
            append_launcher_log(
                "WARN",
                format!("OpenCode GitHub API unavailable, using public release page fallback: {api_error}"),
            );
            let tag = fetch_latest_release_tag_from_public_page(
                OPENCODE_REPO_LATEST_RELEASE_URL,
                "OpenCode",
            )
            .await
            .map_err(|fallback_error| {
                format!("{api_error}；已尝试通过 GitHub 公开 release 页面获取版本，也失败：{fallback_error}")
            })?;
            Ok((tag.clone(), opencode_asset_from_tag(&tag, &asset_name)))
        }
        Err(error) => Err(error),
    }
}

async fn fetch_lifebook_launcher_release() -> Result<GithubRelease, String> {
    fetch_github_release(LIFEBOOK_LAUNCHER_REPO_API, "LifeBook Launcher").await
}

async fn fetch_github_release(api_url: &str, label: &str) -> Result<GithubRelease, String> {
    let first_result =
        fetch_github_release_with_client(http_client()?, api_url, label, "HTTP/1.1").await;
    match first_result {
        Ok(release) => Ok(release),
        Err(error) if should_retry_with_auto_http(&error) => {
            append_launcher_log(
                "WARN",
                format!("{label} release HTTP/1.1 failed, retrying with automatic HTTP transport: {error}"),
            );
            fetch_github_release_with_client(http_client_auto()?, api_url, label, "automatic HTTP")
                .await
                .map_err(|retry_error| format!("{error}；automatic HTTP 重试也失败：{retry_error}"))
        }
        Err(error) => Err(error),
    }
}

async fn fetch_github_release_with_client(
    client: reqwest::Client,
    api_url: &str,
    label: &str,
    transport: &str,
) -> Result<GithubRelease, String> {
    let response = client
        .get(api_url)
        .header("User-Agent", "LifeBook-Launcher")
        .send()
        .await
        .map_err(|err| {
            format!("无法访问 {label} release（{transport}）：{err}。请检查网络、VPN 或代理设置。")
        })?;
    if response.status() == StatusCode::NOT_FOUND {
        return Err(format!(
            "{label} release 不存在或尚未发布。请先在 GitHub 仓库创建 release，或暂时忽略此更新检查。"
        ));
    }
    if !response.status().is_success() {
        let status = response.status();
        let body = response.text().await.unwrap_or_default();
        let summary = github_error_summary(&body);
        return Err(format!(
            "{label} release 请求失败（{transport}）：HTTP status {status}{summary} for url ({api_url})。请检查网络、VPN 或代理设置。"
        ));
    }
    response
        .json::<GithubRelease>()
        .await
        .map_err(|err| format!("无法解析 {label} release：{err}"))
}

async fn fetch_latest_release_tag_from_public_page(
    url: &str,
    label: &str,
) -> Result<String, String> {
    let response = http_client_auto()?
        .get(url)
        .header("User-Agent", "LifeBook-Launcher")
        .send()
        .await
        .map_err(|err| format!("无法访问 {label} 公开 release 页面：{err}"))?;
    let final_url = response.url().to_string();
    let status = response.status();
    if !status.is_success() {
        return Err(format!(
            "{label} 公开 release 页面请求失败：HTTP status {status} for url ({final_url})"
        ));
    }
    latest_release_tag_from_url(&final_url)
        .ok_or_else(|| format!("无法从 {label} 公开 release 页面解析最新版本：{final_url}"))
}

fn latest_release_tag_from_url(url: &str) -> Option<String> {
    let marker = "/releases/tag/";
    let (_, tag) = url.split_once(marker)?;
    let tag = tag.split(['?', '#']).next()?.trim_matches('/');
    if tag.is_empty() {
        None
    } else {
        Some(tag.to_string())
    }
}

fn opencode_asset_from_tag(tag: &str, asset_name: &str) -> GithubAsset {
    GithubAsset {
        name: asset_name.to_string(),
        browser_download_url: github_release_download_url(
            OPENCODE_REPO_RELEASE_DOWNLOAD_BASE,
            tag,
            asset_name,
        ),
        size: 0,
    }
}

fn github_release_download_url(base: &str, tag: &str, asset_name: &str) -> String {
    format!(
        "{}/{}/{}",
        base.trim_end_matches('/'),
        tag.trim_matches('/'),
        asset_name.trim_start_matches('/')
    )
}

fn github_error_summary(body: &str) -> String {
    let lower = body.to_ascii_lowercase();
    if lower.contains("rate limit") {
        " (GitHub API rate limit exceeded)".into()
    } else {
        String::new()
    }
}

fn should_use_public_release_fallback(error: &str) -> bool {
    let lower = error.to_ascii_lowercase();
    lower.contains("403") || lower.contains("rate limit")
}

fn should_retry_with_auto_http(error: &str) -> bool {
    let lower = error.to_ascii_lowercase();
    !should_use_public_release_fallback(error)
        && (lower.contains("http2")
            || lower.contains("stream")
            || lower.contains("connection")
            || lower.contains("timed out")
            || lower.contains("timeout")
            || lower.contains("operation timed out"))
}

fn launcher_current_version() -> String {
    format!("v{}", env!("CARGO_PKG_VERSION"))
}

fn normalize_version(value: &str) -> String {
    value.trim().trim_start_matches('v').to_ascii_lowercase()
}

fn is_remote_version_newer(remote: &str, installed: &str) -> bool {
    let remote_normalized = normalize_version(remote);
    let installed_normalized = normalize_version(installed);
    if remote_normalized == installed_normalized {
        return false;
    }
    match compare_version_parts(&remote_normalized, &installed_normalized) {
        Some(ordering) => ordering > 0,
        None => true,
    }
}

fn compare_version_parts(remote: &str, installed: &str) -> Option<i8> {
    let remote_parts = numeric_version_parts(remote)?;
    let installed_parts = numeric_version_parts(installed)?;
    let max_len = remote_parts.len().max(installed_parts.len());
    for index in 0..max_len {
        let left = *remote_parts.get(index).unwrap_or(&0);
        let right = *installed_parts.get(index).unwrap_or(&0);
        if left > right {
            return Some(1);
        }
        if left < right {
            return Some(-1);
        }
    }
    Some(0)
}

fn numeric_version_parts(value: &str) -> Option<Vec<u64>> {
    let cleaned = value
        .trim()
        .split(['-', '+'])
        .next()
        .unwrap_or_default()
        .trim();
    if cleaned.is_empty() {
        return None;
    }
    let mut parts = Vec::new();
    for part in cleaned.split('.') {
        if part.is_empty() || !part.chars().all(|ch| ch.is_ascii_digit()) {
            return None;
        }
        parts.push(part.parse::<u64>().ok()?);
    }
    Some(parts)
}

fn launcher_update_root() -> Result<PathBuf, String> {
    let base = dirs::data_local_dir().ok_or_else(|| "无法定位用户本地数据目录。".to_string())?;
    Ok(base.join("LifeBook").join("launcher").join("updates"))
}

#[cfg(target_os = "windows")]
fn schedule_launcher_update_install(installer: &Path) -> Result<(), String> {
    const CREATE_NO_WINDOW: u32 = 0x08000000;
    let current_exe = env::current_exe().map_err(|err| format!("无法定位当前 Launcher：{err}"))?;
    let script = installer.with_file_name("install-lifebook-launcher.cmd");
    let content = format!(
        r#"@echo off
setlocal
set "INSTALLER={installer}"
set "APP={app}"
timeout /t 2 /nobreak >nul
start /wait "" "%INSTALLER%" /S
if exist "%APP%" start "" "%APP%"
del "%~f0" >nul 2>nul
endlocal
"#,
        installer = installer.display(),
        app = current_exe.display(),
    );
    fs::write(&script, content).map_err(|err| format!("无法写入 Launcher 更新脚本：{err}"))?;
    Command::new("cmd")
        .args(["/C", "start", "", "/MIN"])
        .arg(&script)
        .creation_flags(CREATE_NO_WINDOW)
        .spawn()
        .map_err(|err| format!("无法启动 Launcher 自动安装脚本：{err}"))?;
    Ok(())
}

#[cfg(target_os = "macos")]
fn schedule_launcher_update_install(installer: &Path) -> Result<(), String> {
    let current_exe = env::current_exe().map_err(|err| format!("无法定位当前 Launcher：{err}"))?;
    let current_app = find_macos_app_bundle(&current_exe)
        .unwrap_or_else(|| PathBuf::from("/Applications/LifeBook Launcher.app"));
    let script = installer.with_file_name("install-lifebook-launcher.sh");
    let content = format!(
        r#"#!/bin/sh
set -eu
INSTALLER={installer}
TARGET_APP={target_app}
sleep 2
MOUNT_DIR=$(hdiutil attach "$INSTALLER" -nobrowse | awk '/\/Volumes\// {{for (i=3;i<=NF;i++) {{printf "%s%s", (i==3?"":" "), $i}}; print ""}}' | tail -n 1)
APP_IN_DMG=$(find "$MOUNT_DIR" -maxdepth 1 -name "*.app" -type d | head -n 1)
mkdir -p "$(dirname "$TARGET_APP")"
rm -rf "$TARGET_APP"
ditto "$APP_IN_DMG" "$TARGET_APP"
hdiutil detach "$MOUNT_DIR" >/dev/null 2>&1 || true
open "$TARGET_APP"
rm "$0"
"#,
        installer = shell_quote(&installer.display().to_string()),
        target_app = shell_quote(&current_app.display().to_string()),
    );
    fs::write(&script, content).map_err(|err| format!("无法写入 Launcher 更新脚本：{err}"))?;
    let mut permissions = fs::metadata(&script)
        .map_err(|err| err.to_string())?
        .permissions();
    use std::os::unix::fs::PermissionsExt;
    permissions.set_mode(0o755);
    fs::set_permissions(&script, permissions).map_err(|err| err.to_string())?;
    Command::new("sh")
        .arg(&script)
        .spawn()
        .map_err(|err| format!("无法启动 Launcher 自动安装脚本：{err}"))?;
    Ok(())
}

#[cfg(target_os = "linux")]
fn schedule_launcher_update_install(installer: &Path) -> Result<(), String> {
    let current_exe = env::current_exe().map_err(|err| format!("无法定位当前 Launcher：{err}"))?;
    let script = installer.with_file_name("install-lifebook-launcher.sh");
    let content = format!(
        r#"#!/bin/sh
set -eu
INSTALLER={installer}
APP={app}
sleep 2
cp "$INSTALLER" "$APP"
chmod +x "$APP"
"$APP" >/dev/null 2>&1 &
rm "$0"
"#,
        installer = shell_quote(&installer.display().to_string()),
        app = shell_quote(&current_exe.display().to_string()),
    );
    fs::write(&script, content).map_err(|err| format!("无法写入 Launcher 更新脚本：{err}"))?;
    let mut permissions = fs::metadata(&script)
        .map_err(|err| err.to_string())?
        .permissions();
    use std::os::unix::fs::PermissionsExt;
    permissions.set_mode(0o755);
    fs::set_permissions(&script, permissions).map_err(|err| err.to_string())?;
    Command::new("sh")
        .arg(&script)
        .spawn()
        .map_err(|err| format!("无法启动 Launcher 自动安装脚本：{err}"))?;
    Ok(())
}

#[cfg(target_os = "macos")]
fn find_macos_app_bundle(path: &Path) -> Option<PathBuf> {
    path.ancestors()
        .find(|ancestor| ancestor.extension().and_then(|value| value.to_str()) == Some("app"))
        .map(Path::to_path_buf)
}

#[cfg(any(target_os = "macos", target_os = "linux"))]
fn shell_quote(value: &str) -> String {
    format!("'{}'", value.replace('\'', "'\\''"))
}

fn select_launcher_asset(release: &GithubRelease) -> Result<&GithubAsset, String> {
    let platform = std::env::consts::OS;
    let arch = std::env::consts::ARCH;
    let preferred = release
        .assets
        .iter()
        .find(|asset| launcher_asset_score(asset, platform, arch) >= 100);
    let fallback = release
        .assets
        .iter()
        .find(|asset| launcher_asset_score(asset, platform, arch) > 0);
    preferred.or(fallback).ok_or_else(|| {
        format!(
            "LifeBook Launcher release 中没有找到当前系统对应的安装包：{} {}",
            platform, arch
        )
    })
}

fn launcher_asset_score(asset: &GithubAsset, platform: &str, arch: &str) -> u8 {
    let name = asset.name.to_lowercase();
    if !(name.contains("lifebook") && name.contains("launcher")) {
        return 0;
    }
    match (platform, arch) {
        ("windows", "x86_64") => {
            if (name.ends_with(".exe") || name.ends_with(".msi"))
                && (name.contains("x64") || name.contains("x86_64"))
            {
                if name.contains("setup") {
                    120
                } else {
                    100
                }
            } else if name.ends_with(".exe") || name.ends_with(".msi") {
                40
            } else {
                0
            }
        }
        ("windows", "aarch64") => {
            if (name.ends_with(".exe") || name.ends_with(".msi"))
                && (name.contains("arm64") || name.contains("aarch64"))
            {
                120
            } else {
                0
            }
        }
        ("macos", "x86_64") => {
            if name.ends_with(".dmg")
                && (name.contains("x64") || name.contains("x86_64") || name.contains("mac"))
            {
                100
            } else {
                0
            }
        }
        ("macos", "aarch64") => {
            if name.ends_with(".dmg")
                && (name.contains("arm64") || name.contains("aarch64") || name.contains("mac"))
            {
                100
            } else {
                0
            }
        }
        ("linux", "x86_64") => {
            if name.ends_with(".appimage") && (name.contains("x86_64") || name.contains("x64")) {
                100
            } else {
                0
            }
        }
        ("linux", "aarch64") => {
            if name.ends_with(".appimage") && (name.contains("arm64") || name.contains("aarch64")) {
                100
            } else {
                0
            }
        }
        _ => 0,
    }
}

fn opencode_asset_name() -> Result<String, String> {
    let arch = std::env::consts::ARCH;
    let asset = match (std::env::consts::OS, arch) {
        ("windows", "x86_64") => "opencode-desktop-win-x64.exe",
        ("windows", "aarch64") => "opencode-desktop-win-arm64.exe",
        ("macos", "x86_64") => "opencode-desktop-mac-x64.dmg",
        ("macos", "aarch64") => "opencode-desktop-mac-arm64.dmg",
        ("linux", "x86_64") => "opencode-desktop-linux-x86_64.AppImage",
        ("linux", "aarch64") => "opencode-desktop-linux-arm64.AppImage",
        _ => {
            return Err(format!(
                "当前系统暂不支持自动下载 OpenCode Desktop：{} {}",
                std::env::consts::OS,
                arch
            ))
        }
    };
    Ok(asset.into())
}

fn opencode_install_root() -> Result<PathBuf, String> {
    let base = dirs::data_local_dir().ok_or_else(|| "无法定位用户本地数据目录。".to_string())?;
    Ok(base.join("LifeBook").join("tools").join("opencode-desktop"))
}

fn opencode_client_candidates(install_root: &Path) -> Vec<PathBuf> {
    let mut candidates = Vec::new();
    if let Some(state) = read_opencode_state(install_root) {
        let installer = PathBuf::from(state.installer);
        if cfg!(target_os = "linux") {
            push_candidate(&mut candidates, installer);
        }
    }

    #[cfg(target_os = "windows")]
    {
        if let Ok(local_app_data) = std::env::var("LOCALAPPDATA") {
            let local_app_data = PathBuf::from(local_app_data);
            for folder in [
                "OpenCode",
                "opencode",
                "OpenCode Desktop",
                "opencode-desktop",
                "@opencode-aidesktop",
            ] {
                for executable in [
                    "OpenCode.exe",
                    "OpenCode Desktop.exe",
                    "opencode.exe",
                    "opencode-desktop.exe",
                ] {
                    push_candidate(
                        &mut candidates,
                        local_app_data
                            .join("Programs")
                            .join(folder)
                            .join(executable),
                    );
                }
            }
            push_candidate(
                &mut candidates,
                local_app_data
                    .join("Microsoft")
                    .join("WindowsApps")
                    .join("OpenCode.exe"),
            );
            push_candidate(
                &mut candidates,
                local_app_data
                    .join("Microsoft")
                    .join("WindowsApps")
                    .join("opencode.exe"),
            );
            find_opencode_windows_apps(&local_app_data.join("Programs"), 3, &mut candidates);
        }
        if let Ok(program_files) = std::env::var("ProgramFiles") {
            let program_files = PathBuf::from(program_files);
            for folder in [
                "OpenCode",
                "opencode",
                "OpenCode Desktop",
                "opencode-desktop",
            ] {
                for executable in [
                    "OpenCode.exe",
                    "OpenCode Desktop.exe",
                    "opencode.exe",
                    "opencode-desktop.exe",
                ] {
                    push_candidate(&mut candidates, program_files.join(folder).join(executable));
                }
            }
            find_opencode_windows_apps(&program_files, 2, &mut candidates);
        }
        if let Ok(program_files_x86) = std::env::var("ProgramFiles(x86)") {
            let program_files_x86 = PathBuf::from(program_files_x86);
            for folder in [
                "OpenCode",
                "opencode",
                "OpenCode Desktop",
                "opencode-desktop",
            ] {
                for executable in [
                    "OpenCode.exe",
                    "OpenCode Desktop.exe",
                    "opencode.exe",
                    "opencode-desktop.exe",
                ] {
                    push_candidate(
                        &mut candidates,
                        program_files_x86.join(folder).join(executable),
                    );
                }
            }
            find_opencode_windows_apps(&program_files_x86, 2, &mut candidates);
        }
        if let Ok(app_data) = std::env::var("APPDATA") {
            let start_menu = PathBuf::from(app_data)
                .join("Microsoft")
                .join("Windows")
                .join("Start Menu")
                .join("Programs");
            find_opencode_windows_apps(&start_menu, 3, &mut candidates);
        }
        if let Ok(program_data) = std::env::var("ProgramData") {
            let start_menu = PathBuf::from(program_data)
                .join("Microsoft")
                .join("Windows")
                .join("Start Menu")
                .join("Programs");
            find_opencode_windows_apps(&start_menu, 3, &mut candidates);
        }
    }

    #[cfg(target_os = "macos")]
    {
        push_candidate(&mut candidates, PathBuf::from("/Applications/OpenCode.app"));
        if let Some(home) = dirs::home_dir() {
            push_candidate(
                &mut candidates,
                home.join("Applications").join("OpenCode.app"),
            );
        }
    }

    #[cfg(target_os = "linux")]
    {
        push_candidate(&mut candidates, PathBuf::from("/usr/bin/opencode-desktop"));
        push_candidate(
            &mut candidates,
            PathBuf::from("/usr/local/bin/opencode-desktop"),
        );
        push_candidate(
            &mut candidates,
            install_root
                .join("downloads")
                .join("opencode-desktop-linux-x86_64.AppImage"),
        );
        push_candidate(
            &mut candidates,
            install_root
                .join("downloads")
                .join("opencode-desktop-linux-arm64.AppImage"),
        );
    }

    candidates
}

fn push_candidate(candidates: &mut Vec<PathBuf>, path: PathBuf) {
    if !candidates.iter().any(|candidate| candidate == &path) {
        candidates.push(path);
    }
}

fn detected_opencode_client(install_root: &Path) -> Option<PathBuf> {
    opencode_client_candidates(install_root)
        .into_iter()
        .find(|candidate| candidate.exists())
}

#[cfg(target_os = "windows")]
fn is_opencode_process_running() -> bool {
    let output = Command::new("tasklist")
        .args(["/FO", "CSV", "/NH"])
        .creation_flags(0x08000000)
        .output();
    let Ok(output) = output else {
        return false;
    };
    let text = String::from_utf8_lossy(&output.stdout).to_ascii_lowercase();
    [
        "opencode.exe",
        "opencode desktop.exe",
        "opencode-desktop.exe",
    ]
    .iter()
    .any(|name| text.contains(name))
}

#[cfg(target_os = "macos")]
fn is_opencode_process_running() -> bool {
    Command::new("pgrep")
        .args(["-f", "OpenCode"])
        .output()
        .map(|output| output.status.success())
        .unwrap_or(false)
}

#[cfg(all(unix, not(target_os = "macos")))]
fn is_opencode_process_running() -> bool {
    Command::new("pgrep")
        .args(["-f", "opencode"])
        .output()
        .map(|output| output.status.success())
        .unwrap_or(false)
}

#[cfg(target_os = "windows")]
fn find_opencode_windows_apps(base: &Path, depth: usize, candidates: &mut Vec<PathBuf>) {
    if depth == 0 || candidates.len() > 80 || !base.is_dir() {
        return;
    }
    let Ok(entries) = fs::read_dir(base) else {
        return;
    };
    for entry in entries.flatten() {
        if candidates.len() > 80 {
            return;
        }
        let path = entry.path();
        let name = path
            .file_name()
            .and_then(|value| value.to_str())
            .unwrap_or_default()
            .to_lowercase();
        if path.is_file() {
            let is_launcher = (name.ends_with(".exe") || name.ends_with(".lnk"))
                && name.contains("opencode")
                && (name.contains("desktop")
                    || name == "opencode.exe"
                    || name == "opencode.lnk"
                    || name == "opencode desktop.lnk");
            if is_launcher {
                push_candidate(candidates, path);
            }
        } else if path.is_dir() && (depth > 2 || name.contains("opencode")) {
            find_opencode_windows_apps(&path, depth - 1, candidates);
        }
    }
}

fn is_proxy_configured() -> bool {
    if configured_proxy_url_best_effort().is_some() {
        return true;
    }
    [
        "HTTPS_PROXY",
        "HTTP_PROXY",
        "ALL_PROXY",
        "https_proxy",
        "http_proxy",
        "all_proxy",
    ]
    .iter()
    .any(|key| {
        std::env::var(key)
            .map(|value| !value.trim().is_empty())
            .unwrap_or(false)
    })
}

fn read_opencode_state(install_root: &Path) -> Option<OpenCodeInstallState> {
    let path = install_root.join("install-state.json");
    let text = fs::read_to_string(path).ok()?;
    serde_json::from_str(&text).ok()
}

fn write_opencode_state(
    install_root: &Path,
    installer: &Path,
    version: &str,
    source: &str,
    repo_root: &Path,
) -> Result<(), String> {
    fs::create_dir_all(install_root).map_err(|err| err.to_string())?;
    let state = OpenCodeInstallState {
        tool: "opencode-desktop".into(),
        installed_at: chrono::Utc::now().to_rfc3339(),
        install_root: install_root.display().to_string(),
        installer: installer.display().to_string(),
        platform: format!("{}-{}", std::env::consts::OS, std::env::consts::ARCH),
        version: version.into(),
        source: source.into(),
        repository_root: repo_root.display().to_string(),
    };
    let text = serde_json::to_string_pretty(&state).map_err(|err| err.to_string())?;
    fs::write(install_root.join("install-state.json"), text).map_err(|err| err.to_string())
}

async fn download_file(
    app: &tauri::AppHandle,
    progress_event: &'static str,
    label: &str,
    url: &str,
    destination: &Path,
    total_bytes: u64,
    cancel_flag: Option<&'static AtomicBool>,
) -> Result<(), String> {
    if total_bytes > 0 && file_size(destination) >= total_bytes {
        emit_download_progress(app, progress_event, total_bytes, total_bytes);
        return Ok(());
    }
    let part_destination = partial_download_path(destination)?;
    let mut existing_bytes = fs::metadata(&part_destination)
        .map(|metadata| metadata.len())
        .unwrap_or(0);
    let client = http_client()?;
    let mut request = client.get(url).header("User-Agent", "LifeBook-Launcher");
    if existing_bytes > 0 {
        request = request.header(RANGE, format!("bytes={existing_bytes}-"));
    }

    let response = request
        .send()
        .await
        .map_err(|err| format!("下载 {label} 失败：{err}。请检查网络、VPN 或代理设置。"))?
        .error_for_status()
        .map_err(|err| format!("下载 {label} 失败：{err}。请检查网络、VPN 或代理设置。"))?;

    let can_resume = existing_bytes > 0 && response.status() == StatusCode::PARTIAL_CONTENT;
    if existing_bytes > 0 && !can_resume {
        existing_bytes = 0;
    }

    let mut file = if can_resume {
        OpenOptions::new()
            .create(true)
            .append(true)
            .open(&part_destination)
            .await
            .map_err(|err| err.to_string())?
    } else {
        File::create(&part_destination)
            .await
            .map_err(|err| err.to_string())?
    };
    let progress_total = if total_bytes > 0 {
        total_bytes
    } else {
        response.content_length().unwrap_or_default() + existing_bytes
    };
    let mut downloaded = existing_bytes;
    let mut stream = response.bytes_stream();
    emit_download_progress(app, progress_event, downloaded, progress_total);

    while let Some(chunk) = stream.next().await {
        if download_cancelled(cancel_flag) {
            file.flush().await.map_err(|err| err.to_string())?;
            return Err(format!("{label} 下载已停止，已保留临时文件，下次可继续。"));
        }
        let chunk = chunk
            .map_err(|err| format!("下载 {label} 失败：{err}。请检查网络、VPN 或代理设置。"))?;
        file.write_all(&chunk)
            .await
            .map_err(|err| err.to_string())?;
        downloaded += chunk.len() as u64;
        emit_download_progress(app, progress_event, downloaded, progress_total);
    }
    file.flush().await.map_err(|err| err.to_string())?;
    if progress_total > 0 && downloaded < progress_total {
        return Err(format!(
            "{label} 下载未完成，已保留临时文件以便下次继续：{} / {} bytes",
            downloaded, progress_total
        ));
    }
    if destination.exists() {
        fs::remove_file(destination).map_err(|err| err.to_string())?;
    }
    fs::rename(&part_destination, destination).map_err(|err| err.to_string())?;
    Ok(())
}

fn download_cancelled(cancel_flag: Option<&'static AtomicBool>) -> bool {
    cancel_flag
        .map(|flag| flag.load(Ordering::Acquire))
        .unwrap_or(false)
}

fn file_size(path: &Path) -> u64 {
    fs::metadata(path)
        .map(|metadata| metadata.len())
        .unwrap_or(0)
}

fn partial_download_path(destination: &Path) -> Result<PathBuf, String> {
    let file_name = destination
        .file_name()
        .and_then(|name| name.to_str())
        .ok_or_else(|| "无法解析下载文件名。".to_string())?;
    Ok(destination.with_file_name(format!("{file_name}.part")))
}

fn emit_download_progress(
    app: &tauri::AppHandle,
    progress_event: &str,
    downloaded: u64,
    total: u64,
) {
    let payload = DownloadProgress {
        percent: download_percent(downloaded, total),
        downloaded_bytes: downloaded,
        total_bytes: total,
        message: None,
        state: None,
    };
    let _ = app.emit(progress_event, payload.clone());
    if let Some(window) = app.get_webview_window("main") {
        let _ = window.emit(progress_event, payload);
    }
}

fn download_percent(downloaded: u64, total: u64) -> f64 {
    if downloaded == 0 {
        return 0.0;
    }
    if total == 0 {
        return 1.0;
    }
    clamp_progress_percent(((downloaded as f64 / total as f64) * 100.0).clamp(1.0, 100.0))
}

fn show_main_window(app: &tauri::AppHandle) {
    if let Some(window) = app.get_webview_window("main") {
        let _ = window.show();
        let _ = window.unminimize();
        let _ = window.set_focus();
    }
}

fn hide_main_window(app: &tauri::AppHandle) {
    if let Some(window) = app.get_webview_window("main") {
        let _ = window.hide();
    }
}

fn configure_tray(app: &mut tauri::App) -> tauri::Result<()> {
    let tray_menu = MenuBuilder::new(app)
        .text(TRAY_SHOW_ID, "打开 LifeBook Launcher")
        .text(TRAY_HIDE_ID, "隐藏窗口")
        .separator()
        .text(TRAY_QUIT_ID, "退出 LifeBook Launcher")
        .build()?;
    let mut tray = TrayIconBuilder::with_id("lifebook-launcher")
        .tooltip("LifeBook Launcher")
        .menu(&tray_menu)
        .show_menu_on_left_click(false)
        .on_menu_event(|app, event| match event.id().as_ref() {
            TRAY_SHOW_ID => show_main_window(app),
            TRAY_HIDE_ID => hide_main_window(app),
            TRAY_QUIT_ID => app.exit(0),
            _ => {}
        })
        .on_tray_icon_event(|tray, event| match event {
            TrayIconEvent::Click {
                button: MouseButton::Left,
                ..
            }
            | TrayIconEvent::DoubleClick {
                button: MouseButton::Left,
                ..
            } => show_main_window(tray.app_handle()),
            _ => {}
        });
    if let Some(icon) = app.default_window_icon().cloned() {
        tray = tray.icon(icon);
    }
    tray.build(app)?;
    Ok(())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_autostart::init(
            tauri_plugin_autostart::MacosLauncher::LaunchAgent,
            Some(vec![]),
        ))
        .setup(|app| {
            let window = app.get_webview_window("main").expect("main window missing");
            let _ = window.set_title(&format!("LifeBook Launcher {}", launcher_current_version()));
            append_launcher_log(
                "INFO",
                format!(
                    "LifeBook Launcher {} started log_path={}",
                    launcher_current_version(),
                    launcher_log_path()
                        .map(|path| display_path(&path))
                        .unwrap_or_else(|error| error)
                ),
            );
            if let Ok(repo_root) = configured_or_default_repo_root() {
                set_process_lifebook_env(&repo_root);
                persist_user_lifebook_home_env(&repo_root);
            }
            configure_tray(app)?;
            Ok(())
        })
        .on_window_event(|window, event| {
            if let WindowEvent::CloseRequested { api, .. } = event {
                api.prevent_close();
                let _ = window.hide();
            }
        })
        .invoke_handler(tauri::generate_handler![
            get_launcher_state,
            choose_repo_folder,
            set_repo_folder,
            prepare_lifebook_project,
            sync_lifebook_project,
            cancel_lifebook_update,
            get_diagnostic_log_settings,
            set_save_logs_enabled,
            get_proxy_settings,
            save_proxy_settings,
            test_proxy_settings,
            auto_detect_proxy_settings,
            get_node_modules_status,
            set_auto_install_node_modules,
            start_node_modules_install,
            cancel_node_modules_install,
            export_launcher_logs,
            record_frontend_activity,
            check_lifebook_updates,
            update_lifebook,
            read_project_document,
            read_project_document_path,
            check_launcher_updates,
            download_and_install_launcher_update,
            minimize_main_window,
            toggle_main_window_maximized,
            close_main_window_to_tray,
            check_opencode_updates,
            check_opencode_local_status,
            download_and_open_opencode,
            cancel_opencode_download,
            launch_opencode_client,
            open_repo_folder,
            open_books_folder
        ])
        .run(tauri::generate_context!())
        .expect("error while running LifeBook Launcher");
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::time::{SystemTime, UNIX_EPOCH};

    fn assert_percent_close(actual: f64, expected: f64) {
        assert!(
            (actual - expected).abs() < 0.01,
            "expected {actual} to be within 0.01 of {expected}"
        );
    }

    fn temp_test_path(name: &str) -> PathBuf {
        let suffix = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("system clock should be valid")
            .as_nanos();
        env::temp_dir().join(format!("lifebook-launcher-{name}-{suffix}"))
    }

    fn has_arg_pair(args: &[String], first: &str, second: &str) -> bool {
        args.windows(2)
            .any(|pair| pair[0] == first && pair[1] == second)
    }

    #[test]
    fn resolves_repo_root_from_nested_source_path() {
        let manifest_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        let root = repo_root_from_path(&manifest_dir)
            .expect("repo root should resolve from src-tauri path");
        assert!(is_lifebook_repo(&root));
        assert!(root.join("AGENTS.md").is_file());
        assert!(root.join("template").join("epub_pipeline").is_dir());
    }

    #[test]
    fn download_percent_reports_visible_progress_after_first_chunk() {
        assert_eq!(download_percent(0, 100), 0.0);
        assert_eq!(download_percent(1, 100_000_000), 1.0);
        assert_eq!(download_percent(1_234, 100_000), 1.23);
        assert_eq!(download_percent(50, 100), 50.0);
        assert_eq!(download_percent(100, 100), 100.0);
    }

    #[test]
    fn parses_git_progress_percent_from_stderr_lines() {
        assert_eq!(
            parse_git_percent("Receiving objects:  42% (42/100), 1.2 MiB | 300 KiB/s"),
            Some(42.0)
        );
        assert_percent_close(
            parse_git_percent("remote: Compressing objects:  75% (2557/3409)").unwrap(),
            75.01,
        );
        assert_eq!(
            parse_git_percent("Resolving deltas: 100% (20/20), done."),
            Some(100.0)
        );
        assert_eq!(parse_git_percent("Already up to date."), None);
    }

    #[test]
    fn maps_git_clone_progress_into_visible_lifebook_range() {
        assert_percent_close(
            git_progress_for_line(GitProgressPhase::Clone, "Receiving objects: 50% (5/10)")
                .map(|(percent, _)| percent)
                .unwrap(),
            47.0,
        );
        assert_percent_close(
            git_progress_for_line(GitProgressPhase::Fetch, "Resolving deltas: 50% (5/10)")
                .map(|(percent, _)| percent)
                .unwrap(),
            73.0,
        );
        assert_eq!(
            git_progress_for_line(
                GitProgressPhase::Clone,
                "remote: Compressing objects:  50% (5/10)"
            ),
            Some((16.0, "clone_compressing"))
        );
    }

    #[test]
    fn git_progress_detail_includes_object_counts_and_transfer_rate() {
        assert_eq!(
            git_progress_detail("Receiving objects:  4% (192/4539), 14.70 MiB | 92.00 KiB/s"),
            Some("192/4539 - 14.70 MiB | 92.00 KiB/s".to_string())
        );
        assert_eq!(
            git_progress_detail("Resolving deltas: 100% (20/20), done."),
            Some("20/20".to_string())
        );
    }

    #[test]
    fn git_progress_fragments_split_on_carriage_returns_and_newlines() {
        let mut pending = String::new();
        assert_eq!(
            git_progress_fragments_from_chunk(
                &mut pending,
                "Counting objects:  1%\rCounting objects:  2%\nReceiving objects:  3%"
            ),
            vec!["Counting objects:  1%", "Counting objects:  2%"]
        );
        assert_eq!(pending, "Receiving objects:  3%");
        assert_eq!(
            git_progress_fragments_from_chunk(&mut pending, "\r"),
            vec!["Receiving objects:  3%"]
        );
        assert!(pending.is_empty());
    }

    #[test]
    fn remote_branch_from_ref_uses_origin_branch_name() {
        assert_eq!(remote_branch_from_ref("origin/main"), "main");
        assert_eq!(
            remote_branch_from_ref("origin/release/stable"),
            "release/stable"
        );
        assert_eq!(remote_branch_from_ref(""), "main");
    }

    #[test]
    fn git_transfer_args_include_low_speed_limits_before_command() {
        let args = git_transfer_args(&["clone", "--progress", "https://example.invalid/repo.git"]);
        assert!(has_arg_pair(&args, "-c", "http.version=HTTP/2"));
        assert!(has_arg_pair(&args, "-c", "http.lowSpeedLimit=1024"));
        assert!(has_arg_pair(&args, "-c", "http.lowSpeedTime=60"));
        assert!(has_arg_pair(&args, "-c", "http.postBuffer=524288000"));
        assert!(args.ends_with(&[
            "clone".to_string(),
            "--progress".to_string(),
            "https://example.invalid/repo.git".to_string(),
        ]));
    }

    #[test]
    fn lifebook_clone_args_use_shallow_single_branch_checkout() {
        assert_eq!(
            lifebook_clone_args("D:\\LifeBook2"),
            vec![
                "clone",
                "--depth",
                "1",
                "--single-branch",
                "--filter=blob:none",
                "--no-tags",
                "--progress",
                LIFEBOOK_REPO_URL,
                "D:\\LifeBook2",
            ]
        );
    }

    #[test]
    fn http_client_builds_with_http1_transport() {
        assert!(http_client().is_ok());
        assert!(http_client_auto().is_ok());
    }

    #[test]
    fn public_release_fallback_extracts_tag_and_asset_url() {
        assert_eq!(
            latest_release_tag_from_url(
                "https://github.com/anomalyco/opencode/releases/tag/v1.15.10"
            ),
            Some("v1.15.10".to_string())
        );
        assert_eq!(
            latest_release_tag_from_url(
                "https://github.com/anomalyco/opencode/releases/tag/v1.15.10?expanded=true"
            ),
            Some("v1.15.10".to_string())
        );
        assert_eq!(
            github_release_download_url(
                "https://github.com/anomalyco/opencode/releases/download",
                "v1.15.10",
                "opencode-desktop-win-x64.exe"
            ),
            "https://github.com/anomalyco/opencode/releases/download/v1.15.10/opencode-desktop-win-x64.exe"
        );
    }

    #[test]
    fn github_rate_limit_uses_public_release_fallback_not_http_retry() {
        let error = "OpenCode release 请求失败：HTTP status 403 (GitHub API rate limit exceeded)";
        assert!(should_use_public_release_fallback(error));
        assert!(!should_retry_with_auto_http(error));
        assert!(should_retry_with_auto_http("connection reset by peer"));
    }

    #[test]
    fn taskkill_args_target_entire_process_tree() {
        assert_eq!(taskkill_tree_args(1234), vec!["/PID", "1234", "/T", "/F"]);
    }

    #[test]
    fn remote_version_check_only_updates_forward() {
        assert!(is_remote_version_newer("v0.0.3", "v0.0.1"));
        assert!(is_remote_version_newer("v1.10.0", "v1.9.9"));
        assert!(is_remote_version_newer("v2026.05.23", "v2025.05.25"));
        assert!(!is_remote_version_newer("v0.0.3", "v0.0.3"));
        assert!(!is_remote_version_newer("v0.0.2", "v0.0.3"));
        assert!(!is_remote_version_newer("v1.0.0", "v1.0.1"));
    }

    #[test]
    fn project_document_candidates_follow_locale() {
        assert_eq!(
            project_document_candidates("readme", "zh-CN")[0],
            PathBuf::from("README.zh-CN.md")
        );
        assert_eq!(
            project_document_candidates("readme", "zh-TW")[0],
            PathBuf::from("readme").join("README.zh-TW.md")
        );
        assert_eq!(
            project_document_candidates("howto", "ja")[0],
            PathBuf::from("doc")
                .join("public")
                .join("how-to-use-prompts.ja.md")
        );
    }

    #[test]
    fn lifebook_home_repo_root_reads_single_standard_variable() {
        let candidate = lifebook_home_repo_root_from_value(Some("D:/LifeBook".into()));

        assert_eq!(candidate, Some(PathBuf::from("D:/LifeBook")));
    }

    #[test]
    fn lifebook_home_repo_root_ignores_blank_values() {
        assert_eq!(lifebook_home_repo_root_from_value(Some("  ".into())), None);
        assert_eq!(lifebook_home_repo_root_from_value(None), None);
    }

    #[test]
    fn repo_status_marks_missing_configured_path_without_fallback() {
        let missing = temp_test_path("missing");
        let _ = fs::remove_dir_all(&missing);

        assert_eq!(repo_status_for_path(&missing), "missing");
        assert!(
            active_repo_root_from_configured_path(&missing).is_none(),
            "a missing configured path must not resolve to the development checkout"
        );
    }

    #[test]
    fn missing_child_path_inside_repo_is_not_treated_as_parent_repo() {
        let missing_inside_repo =
            PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("__missing_lifebook_workspace__");
        let _ = fs::remove_dir_all(&missing_inside_repo);

        assert_eq!(repo_status_for_path(&missing_inside_repo), "missing");
        assert!(
            active_repo_root_from_configured_path(&missing_inside_repo).is_none(),
            "a deleted configured subfolder must not silently fall back to its parent repository"
        );
    }

    #[test]
    fn repo_status_blocks_non_empty_invalid_directory() {
        let occupied = temp_test_path("occupied");
        fs::create_dir_all(&occupied).expect("test directory should be created");
        fs::write(occupied.join("user-file.txt"), "user content")
            .expect("test file should be written");

        assert_eq!(repo_status_for_path(&occupied), "occupied");

        fs::remove_dir_all(&occupied).expect("test directory should be cleaned");
    }

    #[test]
    fn project_document_links_must_stay_inside_repo() {
        assert_eq!(
            safe_project_relative_path("./doc/public/how-to-use-prompts.zh-CN.md").unwrap(),
            PathBuf::from("doc")
                .join("public")
                .join("how-to-use-prompts.zh-CN.md")
        );
        assert!(safe_project_relative_path("../AGENTS.md").is_err());
        assert!(safe_project_relative_path("C:/Windows/win.ini").is_err());
        assert!(safe_project_relative_path("https://example.com/README.md").is_err());
    }

    #[test]
    fn localized_commit_summary_selects_block_language() {
        let body = r#"ZH:
- 中文第一条。
- 中文第二条。

EN:
- English first item.

JA:
- 日本語の項目。
"#;
        assert_eq!(
            localized_commit_summary(body, Some("zh-CN")),
            "中文第一条。 中文第二条。"
        );
        assert_eq!(
            localized_commit_summary(body, Some("ja-JP")),
            "日本語の項目。"
        );
        assert_eq!(
            localized_commit_summary(body, Some("en-US")),
            "English first item."
        );
    }

    #[test]
    fn localized_commit_summary_supports_legacy_inline_language_labels() {
        let body = r#"ZH: 中文摘要。

EN: English summary.

JA: 日本語概要。"#;
        assert_eq!(localized_commit_summary(body, Some("zh-CN")), "中文摘要。");
        assert_eq!(
            localized_commit_summary(body, Some("en-US")),
            "English summary."
        );
        assert_eq!(localized_commit_summary(body, Some("ja")), "日本語概要。");
    }

    #[test]
    fn full_commit_message_keeps_title_and_body_for_tooltip() {
        let body = r#"ZH:
- 中文摘要。

EN:
- English summary."#;

        assert_eq!(
            full_commit_message("Improve Launcher updates", body),
            "Improve Launcher updates\n\nZH:\n- 中文摘要。\n\nEN:\n- English summary."
        );
    }

    #[test]
    fn diagnostic_logging_defaults_to_enabled_for_missing_config() {
        assert!(diagnostic_logging_enabled_from_config(
            &LauncherConfig::default()
        ));
    }

    #[test]
    fn diagnostic_logging_can_be_disabled_from_config() {
        let config = LauncherConfig {
            repo_root: None,
            save_logs: Some(false),
            proxy: None,
            auto_install_node_modules: None,
        };

        assert!(!diagnostic_logging_enabled_from_config(&config));
    }

    #[test]
    fn node_modules_auto_install_defaults_to_enabled() {
        assert!(auto_install_node_modules_enabled_from_config(
            &LauncherConfig::default()
        ));

        let config = LauncherConfig {
            repo_root: None,
            save_logs: None,
            proxy: None,
            auto_install_node_modules: Some(false),
        };
        assert!(!auto_install_node_modules_enabled_from_config(&config));
    }

    #[test]
    fn proxy_url_requires_host_and_port_when_enabled() {
        let proxy = NetworkProxySettings {
            enabled: true,
            scheme: "socks5h".into(),
            host: "127.0.0.1".into(),
            port: Some(10808),
        };
        assert_eq!(
            proxy_url_from_settings(&proxy).unwrap(),
            Some("socks5h://127.0.0.1:10808".into())
        );

        let missing_host = NetworkProxySettings {
            host: " ".into(),
            ..proxy.clone()
        };
        assert!(proxy_url_from_settings(&missing_host).is_err());
    }

    #[test]
    fn proxy_settings_from_url_accepts_common_local_proxy_urls() {
        let http =
            proxy_settings_from_url("http://127.0.0.1:7890").expect("HTTP proxy URL should parse");
        assert!(http.enabled);
        assert_eq!(http.scheme, "http");
        assert_eq!(http.host, "127.0.0.1");
        assert_eq!(http.port, Some(7890));

        let socks = proxy_settings_from_url("socks5h://localhost:10808")
            .expect("SOCKS proxy URL should parse");
        assert_eq!(socks.scheme, "socks5h");
        assert_eq!(socks.host, "localhost");
        assert_eq!(socks.port, Some(10808));

        let no_scheme = proxy_settings_from_url("127.0.0.1:7897")
            .expect("host:port proxy should default to HTTP");
        assert_eq!(no_scheme.scheme, "http");
        assert_eq!(no_scheme.port, Some(7897));

        assert!(proxy_settings_from_url("not-a-valid-proxy").is_none());
    }

    #[test]
    fn node_modules_progress_detail_formats_files_bytes_and_rate() {
        assert_eq!(
            node_modules_progress_detail(774, 7029, 14_459_863, 9_332_326),
            "(774/7029), 13.79 MiB | 8.90 MiB/s"
        );
        assert_eq!(
            node_modules_progress_detail(0, 0, 0, 0),
            "(0/0), 0.00 MiB | 0.00 MiB/s"
        );
    }

    #[test]
    fn git_transfer_retry_detects_common_github_disconnects() {
        assert!(should_retry_git_transfer(
            "error: RPC failed; curl 18 transfer closed with outstanding read data remaining"
        ));
        assert!(should_retry_git_transfer("fatal: early EOF"));
        assert!(should_retry_git_transfer(
            "HTTP/2 stream 5 was not closed cleanly"
        ));
        assert!(!should_retry_git_transfer("LifeBook 下载已停止"));
    }

    #[test]
    fn rotating_diagnostic_log_keeps_newest_files_and_removes_oldest() {
        let dir = temp_test_path("diagnostic-rotation");
        fs::create_dir_all(&dir).expect("log directory should be created");
        let log_path = dir.join("lifebook-launcher.log");

        append_launcher_log_to_path(&log_path, true, 24, 2, "INFO", "first-line")
            .expect("first log write should succeed");
        append_launcher_log_to_path(&log_path, true, 24, 2, "INFO", "second-line")
            .expect("second log write should rotate");
        append_launcher_log_to_path(&log_path, true, 24, 2, "INFO", "third-line")
            .expect("third log write should rotate");

        assert!(
            fs::read_to_string(&log_path)
                .expect("current log should exist")
                .contains("third-line"),
            "current log should contain newest line"
        );
        assert!(
            fs::read_to_string(log_path.with_extension("log.1"))
                .expect("first rotated log should exist")
                .contains("second-line"),
            "first backup should contain the previous line"
        );
        assert!(
            fs::read_to_string(log_path.with_extension("log.2"))
                .expect("second rotated log should exist")
                .contains("first-line"),
            "second backup should contain the oldest retained line"
        );
        assert!(
            !log_path.with_extension("log.3").exists(),
            "rotation should cap backup count"
        );

        fs::remove_dir_all(&dir).expect("test log directory should be cleaned");
    }

    #[test]
    fn disabled_diagnostic_logging_does_not_create_log_file() {
        let dir = temp_test_path("diagnostic-disabled");
        fs::create_dir_all(&dir).expect("log directory should be created");
        let log_path = dir.join("lifebook-launcher.log");

        append_launcher_log_to_path(&log_path, false, 1024, 2, "INFO", "hidden-line")
            .expect("disabled log write should still return ok");

        assert!(!log_path.exists(), "disabled logging must not create files");

        fs::remove_dir_all(&dir).expect("test log directory should be cleaned");
    }

    #[test]
    fn export_diagnostic_logs_copies_rotated_logs_and_context() {
        let log_dir = temp_test_path("diagnostic-export-source");
        let export_parent = temp_test_path("diagnostic-export-target");
        fs::create_dir_all(&log_dir).expect("log directory should be created");
        fs::create_dir_all(&export_parent).expect("export directory should be created");
        fs::write(log_dir.join("lifebook-launcher.log"), "current").expect("current log written");
        fs::write(log_dir.join("lifebook-launcher.log.1"), "previous")
            .expect("rotated log written");

        let context = diagnostic_context_for_export(
            "v-test",
            "D:\\LifeBook",
            "ready",
            true,
            &log_dir,
            4096,
            2,
        );
        let export_dir = export_diagnostic_logs_to_dir(&export_parent, &log_dir, &context)
            .expect("diagnostic logs should export");

        assert!(export_dir.join("lifebook-launcher.log").is_file());
        assert!(export_dir.join("lifebook-launcher.log.1").is_file());
        let context_text = fs::read_to_string(export_dir.join("diagnostic-context.json"))
            .expect("diagnostic context should be exported");
        assert!(context_text.contains("\"repoRoot\": \"D:\\\\LifeBook\""));
        assert!(context_text.contains("\"saveLogs\": true"));

        fs::remove_dir_all(&log_dir).expect("source log directory should be cleaned");
        fs::remove_dir_all(&export_parent).expect("export directory should be cleaned");
    }

    #[test]
    fn lifebook_update_guard_allows_only_one_update_job() {
        let first = LifeBookUpdateGuard::try_acquire().expect("first update job should start");
        assert!(
            LifeBookUpdateGuard::try_acquire().is_err(),
            "second update job should be rejected while the first job is active"
        );
        drop(first);
        let second = LifeBookUpdateGuard::try_acquire().expect("guard should release after drop");
        drop(second);
    }
}
