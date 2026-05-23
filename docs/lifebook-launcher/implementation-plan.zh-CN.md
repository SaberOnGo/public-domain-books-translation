# LifeBook Launcher Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a production-quality cross-platform LifeBook Launcher desktop app that checks and updates this repository and the OpenCode Desktop client.

**Architecture:** Tauri owns filesystem, Git, update download, installer launch, and autostart integration. React owns the polished user interface, local settings, visible update status, commit scroll area, and activity log. The user-facing launcher directory contains the setup executable at the top level and keeps development files under `source/`.

**Tech Stack:** Tauri 2, React 19, TypeScript, Vite, Rust, reqwest, tauri-plugin-autostart.

---

## File Map

- `tools/lifebook-launcher/LifeBook Launcher Setup.exe`: Windows user-facing setup entry.
- `tools/lifebook-launcher/source/package.json`: frontend and Tauri scripts.
- `tools/lifebook-launcher/source/src-tauri/Cargo.toml`: Rust dependencies.
- `tools/lifebook-launcher/source/src-tauri/tauri.conf.json`: desktop app metadata and window settings.
- `tools/lifebook-launcher/source/src-tauri/src/main.rs`: Tauri entry point.
- `tools/lifebook-launcher/source/src-tauri/src/lib.rs`: commands for Git, OpenCode release checks, download, installer opening, and directory opening.
- `tools/lifebook-launcher/source/src/main.tsx`: React bootstrap.
- `tools/lifebook-launcher/source/src/App.tsx`: main application shell.
- `tools/lifebook-launcher/source/src/api.ts`: typed Tauri API wrapper.
- `tools/lifebook-launcher/source/src/types.ts`: shared frontend types.
- `tools/lifebook-launcher/source/src/styles.css`: product UI styling.
- `tools/lifebook-launcher/source/README.zh-CN.md`: developer-facing launcher instructions.
- `README.md`, `README.zh-CN.md`, `readme/README.zh-TW.md`, `readme/README.ja.md`: update launcher section only; do not delete root README files.
- `doc/public/how-to-use-prompts.*.md`: update launcher instructions only.

## Tasks

- [x] Create the Tauri + React project structure under `tools/lifebook-launcher/source/`.
- [x] Implement Rust commands for repository state, LifeBook update check, LifeBook pull, OpenCode release check, OpenCode download/open, and safe directory opening.
- [x] Implement React UI with sidebar, status bar, two update cards, commit scroll panel, settings toggles, and activity log.
- [x] Wire Tauri autostart plugin to the settings page.
- [x] Store user settings in localStorage and run startup checks according to settings.
- [x] Update all user docs to point to LifeBook Launcher.
- [x] Keep ordinary users on the LifeBook Launcher GUI entry.
- [x] Run `npm install`, `npm run build`, `cargo check`, and Tauri build/type checks where available.
