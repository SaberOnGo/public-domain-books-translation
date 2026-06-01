#!/usr/bin/env python3
"""Reject local absolute paths in reusable/book-production artifacts.

This is a portability gate. EPUB projects are expected to be usable from a
downloaded repository, so generated metadata, QA evidence, review manifests,
release state, and public prompt examples must not leak one contributor's local
workspace path.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TEXT_SUFFIXES = {
    "",
    ".css",
    ".csv",
    ".html",
    ".js",
    ".json",
    ".jsonc",
    ".md",
    ".mjs",
    ".opf",
    ".py",
    ".svg",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".xhtml",
    ".xml",
    ".yaml",
    ".yml",
}
BINARY_SUFFIXES = {
    ".7z",
    ".class",
    ".dll",
    ".epub",
    ".gif",
    ".gz",
    ".icns",
    ".ico",
    ".jar",
    ".jpeg",
    ".jpg",
    ".lock",
    ".mp4",
    ".pdf",
    ".png",
    ".ttf",
    ".webp",
    ".woff",
    ".woff2",
    ".zip",
}
SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "target",
}
BOOK_ARTIFACT_DIRS = {
    "chapters",
    "frontmatter",
    "metadata",
    "output",
    "preproduction",
    "qa",
    "reviews",
    "state",
}
REPO_ARTIFACT_ROOTS = {
    "doc/public",
    "template/epub_pipeline",
}
WINDOWS_ABSOLUTE_PATH = re.compile(
    r"(?<![A-Za-z0-9_])(?:[A-Za-z]:[\\/][^\s\"'<>)]*|file://(?:/|[A-Za-z]:)[^\s\"'<>)]*)",
    re.IGNORECASE,
)
POSIX_LOCAL_PATH = re.compile(r"(?<![A-Za-z0-9_])(?:/(?:Users|home)/[^\s\"'<>)]*|/mnt/[A-Za-z]/[^\s\"'<>)]*)")


@dataclass
class Issue:
    path: str
    line: int
    rule: str
    snippet: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check for local absolute paths in reusable artifacts.")
    parser.add_argument("--root", type=Path, default=None, help="Root to scan. Defaults to the parent of scripts/.")
    parser.add_argument("--scope", choices=["book", "repo"], default="book", help="Use book-project or repository scan rules.")
    parser.add_argument("--write-report", action="store_true", help="Write output/local_absolute_path_check.json when possible.")
    return parser.parse_args()


def default_root() -> Path:
    return Path(__file__).resolve().parents[1]


def rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def is_text_candidate(path: Path) -> bool:
    if path.suffix.lower() in BINARY_SUFFIXES:
        return False
    return path.suffix.lower() in TEXT_SUFFIXES


def should_skip_path(root: Path, path: Path, scope: str) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    rel_path = rel(root, path)
    if rel_path == "output/local_absolute_path_check.json":
        return True
    if scope == "repo":
        if rel_path == "books/output/local_absolute_path_check.json":
            return True
        if rel_path == "books/private" or rel_path.startswith("books/private/"):
            return True
    return False


def iter_files(root: Path, scope: str) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if should_skip_path(root, path, scope):
            continue
        if path.is_file() and is_text_candidate(path):
            files.append(path)
    return sorted(files)


def is_under(rel_path: str, prefixes: set[str]) -> bool:
    normalized = rel_path.replace("\\", "/")
    return any(normalized == prefix or normalized.startswith(f"{prefix}/") for prefix in prefixes)


def should_scan_for_generic_local_path(scope: str, rel_path: str) -> bool:
    parts = rel_path.replace("\\", "/").split("/")
    if scope == "book":
        return bool(parts and parts[0] in BOOK_ARTIFACT_DIRS)
    if is_under(rel_path, REPO_ARTIFACT_ROOTS):
        if rel_path.startswith("template/epub_pipeline/") and "/scripts/" in rel_path:
            return False
        return True
    if len(parts) >= 4 and parts[0] == "books" and parts[2][:1].isdigit() and parts[3] in BOOK_ARTIFACT_DIRS:
        return True
    return False


def repo_leak_patterns(root: Path, scope: str) -> list[str]:
    if scope != "repo":
        return []
    resolved = root.resolve()
    raw = str(resolved)
    slash = raw.replace("\\", "/")
    escaped = raw.replace("\\", "\\\\")
    name = resolved.name
    return [raw, slash, escaped, f"\\{name}", f"/{name}"]


def allowed_match(text: str) -> bool:
    normalized = text.replace("\\\\", "\\")
    return normalized.startswith("D:\\LifeBook") or normalized == "D:\\"


def scan_file(root: Path, path: Path, scope: str, repo_patterns: list[str]) -> list[Issue]:
    rel_path = rel(root, path)
    issues: list[Issue] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return [Issue(rel_path, 0, "read_error", str(exc))]

    generic_scan = should_scan_for_generic_local_path(scope, rel_path)
    for line_no, line in enumerate(lines, start=1):
        for pattern in repo_patterns:
            if pattern and pattern in line:
                issues.append(Issue(rel_path, line_no, "repo_absolute_path", line.strip()[:220]))
        if generic_scan:
            for match in WINDOWS_ABSOLUTE_PATH.finditer(line):
                token = match.group(0)
                if allowed_match(token):
                    continue
                issues.append(Issue(rel_path, line_no, "local_absolute_path", line.strip()[:220]))
            for match in POSIX_LOCAL_PATH.finditer(line):
                issues.append(Issue(rel_path, line_no, "local_absolute_path", line.strip()[:220]))
    return issues


def write_report(root: Path, issues: list[Issue], scope: str) -> None:
    output_dir = root / "output"
    if scope == "repo":
        output_dir = root / "books" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "status": "FAIL" if issues else "PASS",
        "scope": scope,
        "issue_count": len(issues),
        "issues": [issue.__dict__ for issue in issues],
    }
    (output_dir / "local_absolute_path_check.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    args = parse_args()
    root = (args.root or default_root()).resolve()
    patterns = repo_leak_patterns(root, args.scope)
    issues: list[Issue] = []
    for path in iter_files(root, args.scope):
        issues.extend(scan_file(root, path, args.scope, patterns))
    issues = list({(issue.path, issue.line, issue.rule, issue.snippet): issue for issue in issues}.values())

    if args.write_report:
        write_report(root, issues, args.scope)

    if issues:
        print("local absolute path policy FAIL")
        for issue in issues[:200]:
            print(f"- {issue.path}:{issue.line}: {issue.rule}: {issue.snippet}")
        if len(issues) > 200:
            print(f"- ... {len(issues) - 200} more issue(s)")
        return 1

    print("local absolute path policy PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
