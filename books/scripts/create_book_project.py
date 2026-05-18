#!/usr/bin/env python3
"""Create a numbered book project under books/{target}/."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


BOOK_DIR_PATTERN = re.compile(r"^(\d+)_")
SAFE_SLUG_PATTERN = re.compile(r"[^A-Za-z0-9._-]+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a book project by copying template/epub_pipeline/common, "
            "overlaying a language-pair template, and assigning the next "
            "books/{target}/{number}_{slug} directory."
        )
    )
    parser.add_argument("book_slug", help="Book slug without the numeric prefix.")
    parser.add_argument(
        "--source-target",
        required=True,
        help="Language-pair template directory, for example en-zh-Hans or grc-zh-Hans.",
    )
    parser.add_argument(
        "--target",
        help="Target language directory under books/. If omitted, infer from existing targets/ directories.",
    )
    parser.add_argument(
        "--profile",
        action="append",
        default=[],
        help="Optional profile template under template/epub_pipeline/profiles/. Can be repeated.",
    )
    parser.add_argument("--source-url", default="", help="Optional public-domain source URL to record in state.")
    parser.add_argument("--dry-run", action="store_true", help="Print the planned directory without copying files.")
    return parser.parse_args()


def repo_paths() -> tuple[Path, Path, Path]:
    books_root = Path(__file__).resolve().parents[1]
    repo_root = books_root.parent
    template_root = repo_root / "template" / "epub_pipeline"
    return repo_root, books_root, template_root


def clean_slug(raw: str) -> str:
    slug = BOOK_DIR_PATTERN.sub("", raw.strip())
    slug = SAFE_SLUG_PATTERN.sub("_", slug).strip("._-")
    if not slug:
        raise SystemExit("Book slug is empty after normalization.")
    return slug


def infer_target(source_target: str, template_root: Path) -> str:
    targets_root = template_root / "targets"
    targets = []
    if targets_root.exists():
        targets = sorted(
            [entry.name for entry in targets_root.iterdir() if entry.is_dir()],
            key=len,
            reverse=True,
        )
    for target in targets:
        if source_target == target or source_target.endswith(f"-{target}"):
            return target
    raise SystemExit(
        "Cannot infer target language. Pass --target explicitly, for example --target zh-Hans."
    )


def next_number(target_dir: Path) -> int:
    if not target_dir.exists():
        return 1
    highest = 0
    for entry in target_dir.iterdir():
        if not entry.is_dir():
            continue
        match = BOOK_DIR_PATTERN.match(entry.name)
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def copy_overlay(src: Path, dst: Path) -> None:
    def ignore(_dir: str, names: list[str]) -> set[str]:
        return {name for name in names if name in {"node_modules", "__pycache__"}}

    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=ignore)


def update_state(project_root: Path, repo_root: Path, source_target: str, source_url: str) -> None:
    state_file = project_root / "state" / "pipeline_state.json"
    if not state_file.exists():
        return
    data = json.loads(state_file.read_text(encoding="utf-8"))
    data["project_root"] = project_root.relative_to(repo_root).as_posix()
    data["template_root"] = f"template/epub_pipeline/{source_target}"
    data["common_template_root"] = "template/epub_pipeline/common"
    if source_url:
        data["source_url"] = source_url
    state_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    repo_root, books_root, template_root = repo_paths()
    source_target = args.source_target.strip()
    target = args.target.strip() if args.target else infer_target(source_target, template_root)
    slug = clean_slug(args.book_slug)

    common_root = template_root / "common"
    language_root = template_root / source_target
    if not common_root.is_dir():
        raise SystemExit(f"Missing common template: {common_root}")
    if not language_root.is_dir():
        raise SystemExit(f"Missing language-pair template: {language_root}")

    target_dir = books_root / target
    number = next_number(target_dir)
    project_root = target_dir / f"{number}_{slug}"
    if project_root.exists():
        raise SystemExit(f"Refusing to overwrite existing project: {project_root}")

    profile_roots = []
    for profile in args.profile:
        profile_root = template_root / "profiles" / profile
        if not profile_root.is_dir():
            raise SystemExit(f"Missing profile template: {profile_root}")
        profile_roots.append(profile_root)

    print(project_root.relative_to(repo_root).as_posix())
    if args.dry_run:
        return

    target_dir.mkdir(parents=True, exist_ok=True)
    copy_overlay(common_root, project_root)
    copy_overlay(language_root, project_root)
    for profile_root in profile_roots:
        copy_overlay(profile_root, project_root)
    update_state(project_root, repo_root, source_target, args.source_url)


if __name__ == "__main__":
    main()
