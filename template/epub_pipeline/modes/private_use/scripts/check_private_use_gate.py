from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_OVERLAY_FILES = [
    "references/private_use_cover_policy.md",
    "references/private_use_frontmatter_policy.md",
    "references/private_use_artifact_policy.md",
    "preproduction/stage1/_TEMPLATE.private_use_production_spec.md",
    "scripts/check_private_use_gate.py",
    "scripts/check_private_reader_facing_policy.py",
    "scripts/create_private_artifact.py",
    "scripts/build_private_epub.js",
]

REQUIRED_PACKAGE_SCRIPTS = [
    "preflight:private-use",
    "reader:private-check",
    "build:private-epub",
    "private:artifact:create",
]

PRIVATE_USE_NOTICE = "本版本仅供个人自用，风险由个人承担。public-domain-books-translation 开源项目仅用于公版书翻译发布，不承担其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任。"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check private-use mode boundary requirements.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--write-report", action="store_true", help="Write output/private_use_gate.json.")
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def find_repo_root(book_root: Path) -> Path | None:
    for candidate in [book_root, *book_root.parents]:
        if (candidate / "books").is_dir() and (candidate / "template").is_dir():
            return candidate
    return None


def rel(book_root: Path, path: Path) -> str:
    try:
        return path.relative_to(book_root).as_posix()
    except ValueError:
        return str(path)


def add_issue(issues: list[dict], rule: str, detail: str, path: str = "") -> None:
    issues.append({"rule": rule, "path": path, "detail": detail})


def read_json(path: Path, issues: list[dict], book_root: Path) -> dict:
    if not path.exists():
        add_issue(issues, "missing_json", f"Missing {rel(book_root, path)}.", rel(book_root, path))
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_issue(issues, "invalid_json", f"Cannot parse JSON: {exc}", rel(book_root, path))
        return {}


def check_private_path(book_root: Path, repo_root: Path | None, issues: list[dict]) -> None:
    if repo_root is None:
        add_issue(issues, "repo_root_not_found", "Cannot find repository root containing books/ and template/.")
        return
    try:
        relative = book_root.relative_to(repo_root / "books")
    except ValueError:
        add_issue(issues, "private_project_outside_books", "Private-use project must be under books/private/{target}/{number}_{target_language_title}_{target_language_author}.", str(book_root))
        return
    if len(relative.parts) != 3 or relative.parts[0] != "private":
        add_issue(issues, "private_project_outside_private_tree", "Private-use project must be under books/private/{target}/{number}_{target_language_title}_{target_language_author}.", relative.as_posix())


def check_state(book_root: Path, issues: list[dict]) -> dict:
    state_path = book_root / "state" / "pipeline_state.json"
    state = read_json(state_path, issues, book_root)
    if state and state.get("publication_mode") != "private_use":
        add_issue(issues, "not_private_use_mode", "pipeline_state.json must set publication_mode=private_use.", rel(book_root, state_path))
    private_record = state.get("private_use", {}) if isinstance(state, dict) else {}
    if not private_record.get("user_declaration"):
        add_issue(issues, "private_use_state_missing_field", "state.private_use.user_declaration is required.", rel(book_root, state_path))
    local_name = private_record.get("local_source_file_name")
    local_hash = private_record.get("local_source_sha256")
    source_url = private_record.get("source_url") or state.get("source_url")
    if not ((local_name and local_hash) or source_url):
        add_issue(issues, "private_use_source_missing", "A local source file or online source URL is required.", rel(book_root, state_path))
    if source_url:
        parsed = urlparse(source_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
            add_issue(issues, "private_use_source_url_invalid", "Online source URL must be HTTP(S).", rel(book_root, state_path))
    if private_record.get("github_publish_allowed") is not False:
        add_issue(issues, "private_use_github_boundary_missing", "state.private_use.github_publish_allowed must be false.", rel(book_root, state_path))
    return state


def check_declaration(book_root: Path, issues: list[dict]) -> None:
    path = book_root / "metadata" / "private_use_declaration.md"
    if not path.exists():
        add_issue(issues, "missing_private_use_declaration", "metadata/private_use_declaration.md is required.", rel(book_root, path))
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    for token in ["PRIVATE_USE_PASS", "Personal study only", PRIVATE_USE_NOTICE, "Do not publish"]:
        if token not in text:
            add_issue(issues, "private_use_declaration_missing_boundary", f"private declaration must contain {token!r}.", rel(book_root, path))


def check_overlay_files(book_root: Path, issues: list[dict]) -> None:
    for relative in REQUIRED_OVERLAY_FILES:
        if not (book_root / relative).exists():
            add_issue(issues, "missing_private_use_overlay_file", "Private-use mode overlay file is missing.", relative)


def check_package(book_root: Path, issues: list[dict]) -> None:
    path = book_root / "package.json"
    data = read_json(path, issues, book_root)
    scripts = data.get("scripts", {}) if isinstance(data, dict) else {}
    for script in REQUIRED_PACKAGE_SCRIPTS:
        if script not in scripts:
            add_issue(issues, "missing_private_package_script", f"package.json must define {script}.", rel(book_root, path))
    if scripts.get("release:create") != "npm run private:artifact:create":
        add_issue(issues, "private_release_alias_not_isolated", "release:create must delegate to private:artifact:create in private-use projects.", rel(book_root, path))


def main() -> None:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    repo_root = find_repo_root(book_root)
    issues: list[dict] = []

    check_private_path(book_root, repo_root, issues)
    check_state(book_root, issues)
    check_declaration(book_root, issues)
    check_overlay_files(book_root, issues)
    check_package(book_root, issues)

    report = {
        "book_root": str(book_root),
        "ok": not issues,
        "issues": issues,
    }
    if args.write_report:
        out = book_root / "output" / "private_use_gate.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if issues:
        for issue in issues:
            location = f" {issue['path']}" if issue.get("path") else ""
            print(f"ERROR {issue['rule']}:{location} {issue['detail']}")
        raise SystemExit(1)
    print("private-use gate PASS")


if __name__ == "__main__":
    main()
