"""Bring a book project's copied tool scripts up to the current template.

Book projects copy template scripts when they are created, so later template fixes never reach them.
This tool compares each script the book has with the template version (common/scripts, then the
language-pair template, then modes/private_use for private books), reports which differ, and with
--apply copies the template versions in, backing up every replaced file under
output/history/tool_sync_<timestamp>/. Scripts that exist only in the book (book-specific tooling)
are never touched. New template scripts the book lacks are added. Missing npm scripts from the
template package.json are added to the book's package.json without overwriting book entries.
The synced template commit and file hashes are recorded in state/tool_versions.json.

书籍工程在创建时复制了模板脚本，之后模板的修复到不了旧书。本工具对比书内脚本与模板最新版，
默认只报告差异；加 --apply 才复制，被替换的文件备份到 output/history/tool_sync_<时间戳>/。
书内独有的脚本不动；模板新增的脚本补进去；package.json 只补缺失的 npm 命令，不覆盖书内已有条目。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TEMPLATE = REPO / "template" / "epub_pipeline"
SCRIPT_SUFFIXES = {".py", ".js", ".mjs"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}


def template_layers(book: Path) -> list[Path]:
    """Template script directories in overlay order (later layers win)."""
    layers = [TEMPLATE / "common"]
    state = read_json(book / "state" / "pipeline_state.json")
    pair = str(state.get("language_pair_template") or state.get("template") or "")
    if pair and (TEMPLATE / pair).is_dir():
        layers.append(TEMPLATE / pair)
    mode = str(state.get("publication_mode") or "")
    if mode == "private_use" or "private" in book.parts:
        layers.append(TEMPLATE / "modes" / "private_use")
    return layers


def template_scripts(layers: list[Path]) -> dict[str, Path]:
    scripts: dict[str, Path] = {}
    for layer in layers:
        folder = layer / "scripts"
        if folder.is_dir():
            for path in folder.iterdir():
                if path.is_file() and path.suffix in SCRIPT_SUFFIXES:
                    scripts[path.name] = path
    return scripts


def merged_template_npm_scripts(layers: list[Path]) -> dict[str, str]:
    merged: dict[str, str] = {}
    for layer in layers:
        merged.update(read_json(layer / "package.json").get("scripts", {}))
    return merged


def template_commit() -> str:
    result = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def sync(book: Path, apply: bool) -> dict:
    layers = template_layers(book)
    wanted = template_scripts(layers)
    scripts_dir = book / "scripts"
    changed, added, same = [], [], []
    for name, source in sorted(wanted.items()):
        target = scripts_dir / name
        if not target.exists():
            added.append(name)
        elif sha256(target) != sha256(source):
            changed.append(name)
        else:
            same.append(name)
    book_only = sorted(p.name for p in scripts_dir.glob("*") if p.is_file() and p.suffix in SCRIPT_SUFFIXES and p.name not in wanted) if scripts_dir.is_dir() else []

    package = book / "package.json"
    book_npm = read_json(package)
    npm_missing = {k: v for k, v in merged_template_npm_scripts(layers).items() if k not in book_npm.get("scripts", {})}

    if apply:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup = book / "output" / "history" / f"tool_sync_{stamp}"
        scripts_dir.mkdir(exist_ok=True)
        for name in changed:
            (backup / "scripts").mkdir(parents=True, exist_ok=True)
            shutil.copy2(scripts_dir / name, backup / "scripts" / name)
        for name in changed + added:
            shutil.copy2(wanted[name], scripts_dir / name)
        if npm_missing and package.exists():
            backup.mkdir(parents=True, exist_ok=True)
            shutil.copy2(package, backup / "package.json")
            book_npm.setdefault("scripts", {}).update(npm_missing)
            package.write_text(json.dumps(book_npm, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        versions = {
            "synced_at": stamp,
            "template_commit": template_commit(),
            "template_layers": [layer.relative_to(REPO).as_posix() for layer in layers],
            "files": {name: sha256(scripts_dir / name) for name in sorted(wanted)},
        }
        (book / "state").mkdir(exist_ok=True)
        (book / "state" / "tool_versions.json").write_text(json.dumps(versions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"book": book.relative_to(REPO).as_posix(), "changed": changed, "added": added, "unchanged": len(same),
            "book_only": book_only, "npm_scripts_added": sorted(npm_missing), "applied": apply}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Sync a book project's tool scripts with the current template.")
    parser.add_argument("book", nargs="+", help="Book project directory (e.g. books/zh-Hans/21_甲虫_理查德_马什).")
    parser.add_argument("--apply", action="store_true", help="Copy template scripts in (default: report only).")
    args = parser.parse_args()
    for value in args.book:
        book = Path(value).resolve()
        if not (book / "state").is_dir() and not (book / "scripts").is_dir():
            print(f"skip (not a book project): {value}")
            continue
        result = sync(book, args.apply)
        print(json.dumps(result, ensure_ascii=False))
    if not args.apply:
        print("dry run: nothing was changed; rerun with --apply after reviewing the diff list. / 仅报告，确认后加 --apply 执行。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
