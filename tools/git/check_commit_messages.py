#!/usr/bin/env python3
"""Validate Git commit messages before pushing to GitHub.

The repository uses commit bodies as LifeBook Launcher update text, so every
pushed commit must include a title plus separated Chinese, English, and
Japanese summaries.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


SECTION_PATTERNS = {
    "ZH": re.compile(r"^(?:ZH|中文|简体中文|繁體中文)\s*[:：]\s*(.*)$", re.IGNORECASE),
    "EN": re.compile(r"^(?:EN|English)\s*[:：]\s*(.*)$", re.IGNORECASE),
    "JA": re.compile(r"^(?:JA|日本語|日文)\s*[:：]\s*(.*)$", re.IGNORECASE),
}
MIN_SECTION_CHARS = 40


def normalized_length(text: str) -> int:
    return len(re.sub(r"[\s*\-•、。,.，；;:：`]+", "", text))


def split_title_and_body(message: str) -> tuple[str, str]:
    lines = message.strip("\n").splitlines()
    if not lines:
        return "", ""
    title = lines[0].strip()
    body = "\n".join(lines[1:]).strip()
    return title, body


def extract_sections(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw_line in body.splitlines():
        line = raw_line.strip()
        matched = next(
            ((name, match) for name, pattern in SECTION_PATTERNS.items() if (match := pattern.match(line))),
            None,
        )
        if matched:
            current, match = matched
            sections.setdefault(current, [])
            inline_text = match.group(1).strip()
            if inline_text:
                sections[current].append(inline_text)
            continue
        if current:
            sections[current].append(raw_line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def validate_commit_message(message: str) -> list[str]:
    issues: list[str] = []
    title, body = split_title_and_body(message)
    if not title:
        issues.append("missing commit title")
    if not body:
        issues.append("missing detailed commit body")
        return issues

    sections = extract_sections(body)
    for name in ("ZH", "EN", "JA"):
        text = sections.get(name, "")
        if not text:
            issues.append(f"missing {name} summary section")
        elif normalized_length(text) < MIN_SECTION_CHARS:
            issues.append(f"{name} summary section is too short")
    return issues


def git_commit_messages(revision_range: str) -> list[tuple[str, str]]:
    format_spec = "%H%x1f%B%x1e"
    result = subprocess.run(
        ["git", "log", f"--pretty=format:{format_spec}", revision_range],
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git log failed")

    commits: list[tuple[str, str]] = []
    for entry in result.stdout.split("\x1e"):
        entry = entry.strip()
        if not entry:
            continue
        commit_hash, _, message = entry.partition("\x1f")
        commits.append((commit_hash.strip(), message.strip()))
    return commits


def validate_message_file(path: Path) -> int:
    message = path.read_text(encoding="utf-8")
    issues = validate_commit_message(message)
    if not issues:
        print(f"PASS {path}")
        return 0
    print(f"FAIL {path}")
    for issue in issues:
        print(f"- {issue}")
    return 1


def validate_range(revision_range: str) -> int:
    commits = git_commit_messages(revision_range)
    if not commits:
        print(f"PASS no commits in range {revision_range}")
        return 0

    failed = False
    for commit_hash, message in commits:
        issues = validate_commit_message(message)
        if issues:
            failed = True
            print(f"FAIL {commit_hash[:12]}")
            for issue in issues:
                print(f"- {issue}")
        else:
            print(f"PASS {commit_hash[:12]}")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate that Git commits have a title and separated ZH/EN/JA detailed summaries."
    )
    parser.add_argument(
        "--range",
        default="HEAD~1..HEAD",
        help="Git revision range to validate, for example origin/main..HEAD. Default: HEAD~1..HEAD.",
    )
    parser.add_argument("--message-file", type=Path, help="Validate a single commit message file instead of git log.")
    args = parser.parse_args(argv)

    try:
        if args.message_file:
            return validate_message_file(args.message_file)
        return validate_range(args.range)
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
