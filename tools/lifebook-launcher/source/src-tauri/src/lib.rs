use futures_util::StreamExt;
use reqwest::{header::RANGE, StatusCode};
use serde::{Deserialize, Serialize};
use std::{
    env,
    fs,
    path::{Path, PathBuf},
    process::Command,
    thread,
    time::Duration,
};
#[cfg(target_os = "windows")]
use std::os::windows::process::CommandExt;
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
const LIFEBOOK_LAUNCHER_REPO_API: &str =
    "https://api.github.com/repos/SaberOnGo/public-domain-books-translation/releases/latest";
const LIFEBOOK_REPO_URL: &str = "https://github.com/SaberOnGo/public-domain-books-translation.git";
const OPENCODE_DOWNLOAD_EVENT: &str = "opencode-download-progress";
const LAUNCHER_DOWNLOAD_EVENT: &str = "launcher-download-progress";
const TRAY_SHOW_ID: &str = "tray_show";
const TRAY_HIDE_ID: &str = "tray_hide";
const TRAY_QUIT_ID: &str = "tray_quit";

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
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct ActionResult {
    ok: bool,
    message: String,
}

#[derive(Debug, Serialize, Deserialize, Default)]
#[serde(rename_all = "camelCase")]
struct LauncherConfig {
    repo_root: Option<String>,
}

#[derive(Debug, Serialize, Clone)]
#[serde(rename_all = "camelCase")]
struct DownloadProgress {
    percent: u8,
    downloaded_bytes: u64,
    total_bytes: u64,
}

#[derive(Debug, Deserialize)]
struct GithubRelease {
    tag_name: String,
    assets: Vec<GithubAsset>,
}

#[derive(Debug, Deserialize)]
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
fn get_launcher_state() -> Result<LauncherState, String> {
    let repo_root = configured_or_default_repo_root()?;
    let repo_ready = is_lifebook_repo(&repo_root);
    let repo_status = if repo_ready {
        "ready"
    } else if repo_root.exists() {
        "not-ready"
    } else {
        "missing"
    }
    .to_string();
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
        git_output(&repo_root, &["rev-parse", "--short", "HEAD"]).unwrap_or_else(|_| "unknown".into())
    } else {
        String::new()
    };
    let remote_url = if repo_ready {
        git_output(&repo_root, &["config", "--get", "remote.origin.url"]).unwrap_or_else(|_| LIFEBOOK_REPO_URL.into())
    } else {
        LIFEBOOK_REPO_URL.into()
    };
    let dirty = repo_ready && !git_output(&repo_root, &["status", "--porcelain"]).unwrap_or_default().trim().is_empty();
    let proxy_configured = is_proxy_configured();
    let platform = format!("{} {}", std::env::consts::OS, std::env::consts::ARCH);
    let install_root = opencode_install_root()?;
    let client_path = detected_opencode_client(&install_root);
    let installed_version = client_path
        .as_deref()
        .and_then(|_| read_opencode_state(&install_root).map(|state| state.version));
    let opencode_available = client_path.is_some();

    Ok(LauncherState {
        repo_root: repo_root.display().to_string(),
        repo_ready,
        repo_status,
        branch: branch.trim().to_string(),
        local_commit: local_commit.trim().to_string(),
        local_commit_short: local_commit_short.trim().to_string(),
        remote_url: remote_url.trim().to_string(),
        dirty,
        proxy_configured,
        platform,
        opencode_install_root: install_root.display().to_string(),
        opencode_installed_version: installed_version,
        opencode_client_path: client_path.map(|path| path.display().to_string()),
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
        });
    };

    let repo_root = if let Some(existing_repo) = repo_root_from_path(&folder) {
        existing_repo
    } else if is_dir_empty(&folder) {
        folder
    } else {
        return Err(format!(
            "选择的目录不是 LifeBook 项目，且目录里已有其他文件。请选择空目录，或选择包含 AGENTS.md、template/ 和 books/ 的 LifeBook 项目目录。当前选择：{}",
            folder.display()
        ));
    };
    write_launcher_config(&repo_root)?;

    Ok(ActionResult {
        ok: true,
        message: format!("已设置 LifeBook 项目目录：{}", repo_root.display()),
    })
}

#[tauri::command]
fn check_lifebook_updates() -> Result<LifeBookUpdateInfo, String> {
    let repo_root = find_repo_root()?;
    lifebook_update_info(&repo_root, true)
}

#[tauri::command]
fn update_lifebook() -> Result<ActionResult, String> {
    let repo_root = find_repo_root()?;
    update_lifebook_project_at(&repo_root)?;
    Ok(ActionResult {
        ok: true,
        message: "LifeBook 已更新到最新版本。".into(),
    })
}

#[tauri::command]
fn prepare_lifebook_project() -> Result<LifeBookUpdateInfo, String> {
    let repo_root = configured_or_default_repo_root()?;
    ensure_lifebook_project_exists(&repo_root)?;
    update_lifebook_project_at(&repo_root)?;
    lifebook_update_info(&repo_root, false)
}

#[tauri::command]
async fn check_launcher_updates() -> Result<LauncherUpdateInfo, String> {
    let install_root = launcher_update_root()?;
    let release = fetch_lifebook_launcher_release().await?;
    let asset = select_launcher_asset(&release)?;
    let installed_version = launcher_current_version();

    Ok(LauncherUpdateInfo {
        installed_version: installed_version.clone(),
        latest_version: release.tag_name.clone(),
        has_update: normalize_version(&installed_version) != normalize_version(&release.tag_name),
        asset_name: asset.name.clone(),
        asset_size: asset.size,
        asset_url: asset.browser_download_url.clone(),
        install_root: install_root.display().to_string(),
    })
}

#[tauri::command]
async fn download_and_install_launcher_update(app: tauri::AppHandle) -> Result<ActionResult, String> {
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
    )
    .await?;

    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        let mut permissions = fs::metadata(&destination).map_err(|err| err.to_string())?.permissions();
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
    let release = fetch_opencode_release().await?;
    let asset_name = opencode_asset_name()?;
    let asset = release
        .assets
        .iter()
        .find(|asset| asset.name == asset_name)
        .ok_or_else(|| format!("OpenCode release 中没有找到当前系统对应的 Desktop 安装包：{asset_name}"))?;

    Ok(OpenCodeUpdateInfo {
        installed_version: installed_version.clone(),
        latest_version: release.tag_name.clone(),
        has_update: installed_version.as_deref() != Some(release.tag_name.as_str()),
        asset_name: asset.name.clone(),
        asset_size: asset.size,
        asset_url: asset.browser_download_url.clone(),
        install_root: install_root.display().to_string(),
        client_path: client_path.as_ref().map(|path| path.display().to_string()),
        client_available: client_path.is_some(),
    })
}

#[tauri::command]
async fn download_and_open_opencode(app: tauri::AppHandle) -> Result<ActionResult, String> {
    let repo_root = configured_or_default_repo_root()?;
    let install_root = opencode_install_root()?;
    let release = fetch_opencode_release().await?;
    let asset_name = opencode_asset_name()?;
    let asset = release
        .assets
        .iter()
        .find(|asset| asset.name == asset_name)
        .ok_or_else(|| format!("OpenCode release 中没有找到当前系统对应的 Desktop 安装包：{asset_name}"))?;

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
    )
    .await?;

    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        let mut permissions = fs::metadata(&destination).map_err(|err| err.to_string())?.permissions();
        permissions.set_mode(0o755);
        fs::set_permissions(&destination, permissions).map_err(|err| err.to_string())?;
    }

    write_opencode_state(&install_root, &destination, &release.tag_name, &asset.browser_download_url, &repo_root)?;
    open::that(&destination).map_err(|err| format!("无法打开 OpenCode 安装包：{err}"))?;

    Ok(ActionResult {
        ok: true,
        message: "OpenCode Desktop 安装包已打开，请按安装窗口提示继续。".into(),
    })
}

#[tauri::command]
fn open_repo_folder() -> Result<ActionResult, String> {
    let repo_root = find_repo_root()?;
    open::that(&repo_root).map_err(|err| err.to_string())?;
    Ok(ActionResult {
        ok: true,
        message: "已打开项目目录。".into(),
    })
}

#[tauri::command]
fn open_books_folder() -> Result<ActionResult, String> {
    let repo_root = find_repo_root()?;
    let preferred = repo_root.join("books").join("zh-Hans");
    let target = if preferred.exists() {
        preferred
    } else {
        repo_root.join("books")
    };
    open::that(&target).map_err(|err| err.to_string())?;
    Ok(ActionResult {
        ok: true,
        message: format!("已打开：{}", target.display()),
    })
}

#[tauri::command]
fn launch_opencode_client() -> Result<ActionResult, String> {
    let install_root = opencode_install_root()?;
    if let Some(candidate) = detected_opencode_client(&install_root) {
        open::that(&candidate).map_err(|err| format!("无法启动 OpenCode：{err}"))?;
        return Ok(ActionResult {
            ok: true,
            message: format!("已启动 OpenCode：{}", candidate.display()),
        });
    }

    Err("没有找到已安装的 OpenCode Desktop。请先点击“检查更新/更新 OpenCode”安装官方客户端；如果已经安装，请从系统应用菜单启动一次。".into())
}

fn git_output(repo_root: &Path, args: &[&str]) -> Result<String, String> {
    let mut command = Command::new("git");
    command.args(args).current_dir(repo_root);
    #[cfg(target_os = "windows")]
    command.creation_flags(0x08000000);
    let output = command
        .output()
        .map_err(|err| format!("无法执行 git：{err}。请确认已安装 Git，或重新运行 LifeBook Launcher 安装包。"))?;
    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).trim().to_string())
    } else {
        let stderr = String::from_utf8_lossy(&output.stderr).trim().to_string();
        Err(if stderr.is_empty() {
            format!("git {:?} 执行失败", args)
        } else {
            stderr
        })
    }
}

fn ensure_lifebook_project_exists(repo_root: &Path) -> Result<(), String> {
    if is_lifebook_repo(repo_root) {
        write_launcher_config(repo_root)?;
        return Ok(());
    }

    if repo_root.exists() && !is_dir_empty(repo_root) {
        return Err(format!(
            "LifeBook 项目目录已存在但不是有效项目：{}。请在设置里选择一个空目录，或选择已有 LifeBook 项目目录。",
            repo_root.display()
        ));
    }

    let parent = repo_root
        .parent()
        .ok_or_else(|| format!("无法解析 LifeBook 项目目录：{}", repo_root.display()))?;
    fs::create_dir_all(parent).map_err(|err| format!("无法创建 LifeBook 项目父目录：{err}"))?;
    let destination = repo_root.display().to_string();
    git_output(parent, &["clone", LIFEBOOK_REPO_URL, &destination])?;

    if !is_lifebook_repo(repo_root) {
        return Err(format!(
            "LifeBook 项目下载完成后校验失败：{}。请检查网络、代理或 Git 设置。",
            repo_root.display()
        ));
    }

    write_launcher_config(repo_root)
}

fn update_lifebook_project_at(repo_root: &Path) -> Result<(), String> {
    if !is_lifebook_repo(repo_root) {
        return Err(format!(
            "LifeBook 项目尚未准备完成：{}。请等待自动准备完成，或在设置里选择项目目录。",
            repo_root.display()
        ));
    }
    let dirty = !git_output(repo_root, &["status", "--porcelain"])?.trim().is_empty();
    if dirty {
        return Err("检测到 LifeBook 项目目录内有本地修改。为避免覆盖用户文件，已跳过自动更新。".into());
    }
    git_output(repo_root, &["fetch", "origin", "--prune"])?;
    git_output(repo_root, &["pull", "--ff-only"])?;
    Ok(())
}

fn lifebook_update_info(repo_root: &Path, fetch: bool) -> Result<LifeBookUpdateInfo, String> {
    if fetch {
        git_output(repo_root, &["fetch", "origin", "--prune"])?;
    }

    let remote_ref = remote_default_ref(repo_root);
    let current_commit = git_output(repo_root, &["rev-parse", "--short", "HEAD"])?;
    let counts = git_output(repo_root, &["rev-list", "--left-right", "--count", &format!("HEAD...{remote_ref}")])?;
    let (ahead_count, behind_count) = parse_ahead_behind(&counts)?;
    let commits = if behind_count > 0 {
        git_commits_between(repo_root, &remote_ref)?
    } else {
        git_latest_commits(repo_root, 20)?
    };

    Ok(LifeBookUpdateInfo {
        repo_root: repo_root.display().to_string(),
        current_commit: current_commit.trim().to_string(),
        remote_ref,
        behind_count,
        ahead_count,
        has_update: behind_count > 0,
        commits,
    })
}

fn find_repo_root() -> Result<PathBuf, String> {
    let mut candidates = Vec::new();
    if let Ok(value) = env::var("LIFEBOOK_REPO_ROOT") {
        if !value.trim().is_empty() {
            candidates.push(PathBuf::from(value));
        }
    }
    if let Some(config) = read_launcher_config() {
        if let Some(repo_root) = config.repo_root {
            candidates.push(PathBuf::from(repo_root));
        }
    }
    if let Ok(current) = std::env::current_dir() {
        candidates.push(current);
    }
    if let Ok(exe) = std::env::current_exe() {
        if let Some(parent) = exe.parent() {
            candidates.push(parent.to_path_buf());
        }
    }
    if let Some(manifest_dir) = option_env!("CARGO_MANIFEST_DIR") {
        candidates.push(PathBuf::from(manifest_dir));
    }
    if let Ok(default_root) = default_lifebook_repo_root() {
        candidates.push(default_root);
    }

    for candidate in candidates {
        if let Some(repo_root) = repo_root_from_path(&candidate) {
            let _ = write_launcher_config(&repo_root);
            return Ok(repo_root);
        }
    }

    let default_root = default_lifebook_repo_root()?;
    Err(format!(
        "LifeBook 项目尚未准备完成。默认目录是 {}，Launcher 会自动下载和更新；也可以在设置里选择其他项目目录。",
        default_root.display()
    ))
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
    if let Ok(value) = env::var("LIFEBOOK_REPO_ROOT") {
        if !value.trim().is_empty() {
            return Ok(PathBuf::from(value));
        }
    }
    if let Some(config) = read_launcher_config() {
        if let Some(repo_root) = config.repo_root {
            if !repo_root.trim().is_empty() {
                return Ok(PathBuf::from(repo_root));
            }
        }
    }
    default_lifebook_repo_root()
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

fn write_launcher_config(repo_root: &Path) -> Result<(), String> {
    let path = launcher_config_path()?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent).map_err(|err| err.to_string())?;
    }
    let config = LauncherConfig {
        repo_root: Some(repo_root.display().to_string()),
    };
    let text = serde_json::to_string_pretty(&config).map_err(|err| err.to_string())?;
    fs::write(path, text).map_err(|err| err.to_string())
}

fn remote_default_ref(repo_root: &Path) -> String {
    git_output(repo_root, &["symbolic-ref", "--short", "refs/remotes/origin/HEAD"])
        .ok()
        .filter(|value| !value.trim().is_empty())
        .unwrap_or_else(|| "origin/main".into())
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

fn git_commits_between(repo_root: &Path, remote_ref: &str) -> Result<Vec<CommitInfo>, String> {
    let range = format!("HEAD..{remote_ref}");
    git_log(repo_root, &range, 80)
}

fn git_latest_commits(repo_root: &Path, max_count: usize) -> Result<Vec<CommitInfo>, String> {
    git_log(repo_root, "HEAD", max_count)
}

fn git_log(repo_root: &Path, rev: &str, max_count: usize) -> Result<Vec<CommitInfo>, String> {
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
            Some(CommitInfo {
                hash: parts.next().unwrap_or_default().trim().to_string(),
                date: parts.next().unwrap_or_default().trim().to_string(),
                title: parts.next().unwrap_or_default().trim().to_string(),
                summary: parts.next().unwrap_or_default().trim().lines().next().unwrap_or_default().to_string(),
            })
        })
        .collect();
    Ok(commits)
}

async fn fetch_opencode_release() -> Result<GithubRelease, String> {
    fetch_github_release(OPENCODE_REPO_API, "OpenCode").await
}

async fn fetch_lifebook_launcher_release() -> Result<GithubRelease, String> {
    fetch_github_release(LIFEBOOK_LAUNCHER_REPO_API, "LifeBook Launcher").await
}

async fn fetch_github_release(api_url: &str, label: &str) -> Result<GithubRelease, String> {
    reqwest::Client::new()
        .get(api_url)
        .header("User-Agent", "LifeBook-Launcher")
        .send()
        .await
        .map_err(|err| format!("无法访问 {label} release：{err}。请检查网络、VPN 或代理设置。"))?
        .error_for_status()
        .map_err(|err| format!("{label} release 请求失败：{err}。请检查网络、VPN 或代理设置。"))?
        .json::<GithubRelease>()
        .await
        .map_err(|err| format!("无法解析 {label} release：{err}"))
}

fn launcher_current_version() -> String {
    format!("v{}", env!("CARGO_PKG_VERSION"))
}

fn normalize_version(value: &str) -> String {
    value.trim().trim_start_matches('v').to_ascii_lowercase()
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
    let mut permissions = fs::metadata(&script).map_err(|err| err.to_string())?.permissions();
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
    let mut permissions = fs::metadata(&script).map_err(|err| err.to_string())?.permissions();
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
    let preferred = release.assets.iter().find(|asset| launcher_asset_score(asset, platform, arch) >= 100);
    let fallback = release.assets.iter().find(|asset| launcher_asset_score(asset, platform, arch) > 0);
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
            if (name.ends_with(".exe") || name.ends_with(".msi")) && (name.contains("x64") || name.contains("x86_64")) {
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
            if (name.ends_with(".exe") || name.ends_with(".msi")) && (name.contains("arm64") || name.contains("aarch64")) {
                120
            } else {
                0
            }
        }
        ("macos", "x86_64") => {
            if name.ends_with(".dmg") && (name.contains("x64") || name.contains("x86_64") || name.contains("mac")) {
                100
            } else {
                0
            }
        }
        ("macos", "aarch64") => {
            if name.ends_with(".dmg") && (name.contains("arm64") || name.contains("aarch64") || name.contains("mac")) {
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
        _ => return Err(format!("当前系统暂不支持自动下载 OpenCode Desktop：{} {}", std::env::consts::OS, arch)),
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
            for folder in ["OpenCode", "opencode", "OpenCode Desktop", "opencode-desktop"] {
                for executable in ["OpenCode.exe", "OpenCode Desktop.exe", "opencode.exe", "opencode-desktop.exe"] {
                    push_candidate(&mut candidates, local_app_data.join("Programs").join(folder).join(executable));
                }
            }
            push_candidate(&mut candidates, local_app_data.join("Microsoft").join("WindowsApps").join("OpenCode.exe"));
            push_candidate(&mut candidates, local_app_data.join("Microsoft").join("WindowsApps").join("opencode.exe"));
            find_opencode_windows_apps(&local_app_data.join("Programs"), 3, &mut candidates);
        }
        if let Ok(program_files) = std::env::var("ProgramFiles") {
            let program_files = PathBuf::from(program_files);
            for folder in ["OpenCode", "opencode", "OpenCode Desktop", "opencode-desktop"] {
                for executable in ["OpenCode.exe", "OpenCode Desktop.exe", "opencode.exe", "opencode-desktop.exe"] {
                    push_candidate(&mut candidates, program_files.join(folder).join(executable));
                }
            }
            find_opencode_windows_apps(&program_files, 2, &mut candidates);
        }
        if let Ok(program_files_x86) = std::env::var("ProgramFiles(x86)") {
            let program_files_x86 = PathBuf::from(program_files_x86);
            for folder in ["OpenCode", "opencode", "OpenCode Desktop", "opencode-desktop"] {
                for executable in ["OpenCode.exe", "OpenCode Desktop.exe", "opencode.exe", "opencode-desktop.exe"] {
                    push_candidate(&mut candidates, program_files_x86.join(folder).join(executable));
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
            push_candidate(&mut candidates, home.join("Applications").join("OpenCode.app"));
        }
    }

    #[cfg(target_os = "linux")]
    {
        push_candidate(&mut candidates, PathBuf::from("/usr/bin/opencode-desktop"));
        push_candidate(&mut candidates, PathBuf::from("/usr/local/bin/opencode-desktop"));
        push_candidate(&mut candidates, install_root.join("downloads").join("opencode-desktop-linux-x86_64.AppImage"));
        push_candidate(&mut candidates, install_root.join("downloads").join("opencode-desktop-linux-arm64.AppImage"));
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
                && (name.contains("desktop") || name == "opencode.exe" || name == "opencode.lnk" || name == "opencode desktop.lnk");
            if is_launcher {
                push_candidate(candidates, path);
            }
        } else if path.is_dir() && (depth > 2 || name.contains("opencode")) {
            find_opencode_windows_apps(&path, depth - 1, candidates);
        }
    }
}

fn is_proxy_configured() -> bool {
    ["HTTPS_PROXY", "HTTP_PROXY", "ALL_PROXY", "https_proxy", "http_proxy", "all_proxy"]
        .iter()
        .any(|key| std::env::var(key).map(|value| !value.trim().is_empty()).unwrap_or(false))
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
) -> Result<(), String> {
    let part_destination = partial_download_path(destination)?;
    let mut existing_bytes = fs::metadata(&part_destination).map(|metadata| metadata.len()).unwrap_or(0);
    let client = reqwest::Client::new();
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
        File::create(&part_destination).await.map_err(|err| err.to_string())?
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
        let chunk = chunk.map_err(|err| format!("下载 {label} 失败：{err}。请检查网络、VPN 或代理设置。"))?;
        file.write_all(&chunk).await.map_err(|err| err.to_string())?;
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

fn partial_download_path(destination: &Path) -> Result<PathBuf, String> {
    let file_name = destination
        .file_name()
        .and_then(|name| name.to_str())
        .ok_or_else(|| "无法解析下载文件名。".to_string())?;
    Ok(destination.with_file_name(format!("{file_name}.part")))
}

fn emit_download_progress(app: &tauri::AppHandle, progress_event: &str, downloaded: u64, total: u64) {
    let percent = if total > 0 {
        ((downloaded as f64 / total as f64) * 100.0).round().clamp(0.0, 100.0) as u8
    } else {
        0
    };
    let _ = app.emit(
        progress_event,
        DownloadProgress {
            percent,
            downloaded_bytes: downloaded,
            total_bytes: total,
        },
    );
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
            let _ = window.set_title("LifeBook Launcher");
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
            prepare_lifebook_project,
            check_lifebook_updates,
            update_lifebook,
            check_launcher_updates,
            download_and_install_launcher_update,
            minimize_main_window,
            toggle_main_window_maximized,
            close_main_window_to_tray,
            check_opencode_updates,
            download_and_open_opencode,
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

    #[test]
    fn resolves_repo_root_from_nested_source_path() {
        let manifest_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        let root = repo_root_from_path(&manifest_dir).expect("repo root should resolve from src-tauri path");
        assert!(is_lifebook_repo(&root));
        assert!(root.join("AGENTS.md").is_file());
        assert!(root.join("template").join("epub_pipeline").is_dir());
    }
}
