#!/usr/bin/env python3
"""Create a numbered book project under books/{target}/ or books/private/{target}/."""

from __future__ import annotations

import argparse
import hashlib
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
    parser.add_argument(
        "--mode",
        choices=["public-domain", "private-use"],
        default="public-domain",
        help="Project mode. public-domain writes to books/{target}/; private-use writes to ignored books/private/{target}/.",
    )
    parser.add_argument("--source-url", default="", help="Optional public-domain or authorized source URL to record in state.")
    parser.add_argument(
        "--local-source-file",
        default="",
        help="Required for --mode private-use. User-provided local source file for personal study only.",
    )
    parser.add_argument(
        "--private-use-declaration",
        default="",
        help="Required for --mode private-use. User declaration that output is personal study only, not redistributed, and not commercial.",
    )
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
    src_root = src.resolve()

    def ignore(_dir: str, names: list[str]) -> set[str]:
        ignored = {name for name in names if name in {"node_modules", "__pycache__"}}
        if Path(_dir).resolve() == src_root and "package.json" in names:
            ignored.add("package.json")
        return ignored

    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=ignore)
    package_src = src / "package.json"
    if package_src.exists():
        merge_package_json(package_src, dst / "package.json")


def merge_package_json(src: Path, dst: Path) -> None:
    overlay = json.loads(src.read_text(encoding="utf-8"))
    base = json.loads(dst.read_text(encoding="utf-8")) if dst.exists() else {}
    merged = dict(base)
    base_scripts = base.get("scripts", {})
    overlay_scripts = overlay.get("scripts", {})
    if isinstance(base_scripts, dict) or isinstance(overlay_scripts, dict):
        scripts = dict(base_scripts) if isinstance(base_scripts, dict) else {}
        if isinstance(overlay_scripts, dict):
            scripts.update(overlay_scripts)
        merged["scripts"] = scripts
    for key, value in overlay.items():
        if key == "scripts":
            continue
        merged[key] = value
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def private_use_mode_root(template_root: Path) -> Path:
    mode_root = template_root / "modes" / "private_use"
    if not mode_root.is_dir():
        raise SystemExit(f"Missing private-use mode overlay: {mode_root}")
    return mode_root


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_private_use_record(local_source_file: str, declaration: str) -> dict[str, str | bool]:
    source_path = Path(local_source_file).expanduser().resolve()
    if not source_path.is_file():
        raise SystemExit(f"--local-source-file must point to an existing file in private-use mode: {source_path}")
    normalized_declaration = declaration.strip()
    if not normalized_declaration:
        raise SystemExit("--private-use-declaration is required in private-use mode.")
    return {
        "local_source_file_name": source_path.name,
        "local_source_sha256": sha256_file(source_path),
        "user_declaration": normalized_declaration,
        "redistribution_allowed": False,
        "commercial_use_allowed": False,
        "github_publish_allowed": False,
    }


def write_private_use_declaration(project_root: Path, record: dict[str, str | bool]) -> None:
    metadata_dir = project_root / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    declaration_path = metadata_dir / "private_use_declaration.md"
    declaration_path.write_text(
        "\n".join(
            [
                "# Private Use Declaration / 私人自用声明",
                "",
                "private_use_status: `PRIVATE_USE_PASS`",
                "",
                "## User Declaration / 用户声明",
                "",
                str(record["user_declaration"]),
                "",
                "## Source File Evidence / 本地书源证据",
                "",
                f"- Local source file name: {record['local_source_file_name']}",
                f"- Local source SHA256: {record['local_source_sha256']}",
                "",
                "## Boundaries / 边界",
                "",
                "- Personal study only. / 仅限个人学习自用。",
                "- No redistribution. / 不得传播。",
                "- No commercial use. / 不得商业使用。",
                "- Personal risk is borne by the individual user. / 风险由个人承担。",
                "- LifeBook Shufang publishes only the LifeBook translation publishing system. / LifeBook书坊仅发布 LifeBook 翻译发布系统。",
                "- LifeBook Shufang does not assume copyright risk or liability caused by other individuals' translation, storage, redistribution, or use of non-public-domain content. / LifeBook书坊不承担任何因其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任。",
                "- Do not publish source text, translations, QA files, or EPUB output to GitHub. / 不得把原文、译文、QA 或 EPUB 输出发布到 GitHub。",
                "",
            ]
        ),
        encoding="utf-8",
    )


def update_state(
    project_root: Path,
    repo_root: Path,
    source_target: str,
    source_url: str,
    publication_mode: str,
    private_use_record: dict[str, str | bool] | None,
) -> None:
    state_file = project_root / "state" / "pipeline_state.json"
    if not state_file.exists():
        return
    data = json.loads(state_file.read_text(encoding="utf-8"))
    data["project_root"] = project_root.relative_to(repo_root).as_posix()
    data["template_root"] = f"template/epub_pipeline/{source_target}"
    data["common_template_root"] = "template/epub_pipeline/common"
    data["publication_mode"] = "private_use" if publication_mode == "private-use" else "public_domain"
    if source_url:
        data["source_url"] = source_url
    if private_use_record is not None:
        data["private_use"] = private_use_record
        quality_gate = data.get("quality_gate")
        if isinstance(quality_gate, dict):
            quality_gate["release_state"] = "output/private_artifacts/private_artifact_state.json"
        shortcuts = data.get("forbidden_shortcuts")
        if isinstance(shortcuts, list):
            data["forbidden_shortcuts"] = [
                "declaring DONE before output/private_artifacts/private_artifact_state.json latest_status is PASS"
                if item == "declaring DONE before output/release/release_state.json latest_status is PASS"
                else item
                for item in shortcuts
            ]
    state_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    repo_root, books_root, template_root = repo_paths()
    source_target = args.source_target.strip()
    target = args.target.strip() if args.target else infer_target(source_target, template_root)
    slug = clean_slug(args.book_slug)
    private_use_record = None
    if args.mode == "private-use":
        private_use_record = build_private_use_record(args.local_source_file, args.private_use_declaration)

    common_root = template_root / "common"
    language_root = template_root / source_target
    if not common_root.is_dir():
        raise SystemExit(f"Missing common template: {common_root}")
    if not language_root.is_dir():
        raise SystemExit(f"Missing language-pair template: {language_root}")

    target_dir = books_root / "private" / target if args.mode == "private-use" else books_root / target
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
    mode_roots = [private_use_mode_root(template_root)] if args.mode == "private-use" else []

    print(project_root.relative_to(repo_root).as_posix())
    if args.dry_run:
        return

    target_dir.mkdir(parents=True, exist_ok=True)
    copy_overlay(common_root, project_root)
    copy_overlay(language_root, project_root)
    for profile_root in profile_roots:
        copy_overlay(profile_root, project_root)
    for mode_root in mode_roots:
        copy_overlay(mode_root, project_root)
    if private_use_record is not None:
        write_private_use_declaration(project_root, private_use_record)
    update_state(project_root, repo_root, source_target, args.source_url, args.mode, private_use_record)


if __name__ == "__main__":
    main()
