from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any


JAVA_NAMES = {"java.exe", "java"}


def default_books_root() -> Path:
    return Path(__file__).resolve().parents[1]


def find_java_in_tree(root: Path) -> Path | None:
    root = Path(root)
    if not root.exists():
        return None
    for item in root.rglob("*"):
        if item.is_file() and item.name.lower() in JAVA_NAMES:
            return item.resolve()
    return None


def java_from_java_home(env: dict[str, str] | None = None) -> Path | None:
    env = env or dict(os.environ)
    java_home = env.get("JAVA_HOME")
    if not java_home:
        return None
    home = Path(java_home)
    for name in ("java.exe", "java"):
        candidate = home / "bin" / name
        if candidate.exists():
            return candidate.resolve()
    return None


def java_from_lifebook_runtime(env: dict[str, str] | None = None) -> Path | None:
    env = env or dict(os.environ)
    lifebook_java = env.get("LIFEBOOK_JAVA")
    if lifebook_java:
        candidate = Path(lifebook_java)
        if candidate.exists():
            return candidate.resolve()
    local_app_data = env.get("LOCALAPPDATA")
    if not local_app_data:
        return None
    return find_java_in_tree(Path(local_app_data) / "LifeBook" / "runtimes" / "java")


def java_from_path() -> Path | None:
    java = shutil.which("java")
    return Path(java).resolve() if java else None


def local_jre_root(books_root: Path) -> Path:
    return Path(books_root).resolve() / "tools" / "zulu17-jre"


def _validate_zip_member(member: zipfile.ZipInfo) -> None:
    path = Path(member.filename)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Unsafe archive path: {member.filename}")


def ensure_local_jre(books_root: Path, archive: Path, force: bool = False) -> dict[str, Any]:
    books_root = Path(books_root).resolve()
    archive = Path(archive).resolve()
    destination = local_jre_root(books_root)

    if not archive.exists():
        raise FileNotFoundError(f"JRE archive not found: {archive}")
    if destination.exists():
        existing_java = find_java_in_tree(destination)
        if existing_java and not force:
            return {
                "status": "already-present",
                "destination": str(destination),
                "java_path": str(existing_java),
            }
        if force:
            shutil.rmtree(destination)

    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as zf:
        for member in zf.infolist():
            _validate_zip_member(member)
        zf.extractall(destination)

    java = find_java_in_tree(destination)
    if not java:
        raise RuntimeError(f"No java executable found after extracting {archive}")

    return {
        "status": "installed",
        "destination": str(destination),
        "java_path": str(java),
    }


def collect_status(books_root: Path) -> dict[str, Any]:
    books_root = Path(books_root).resolve()
    local_root = local_jre_root(books_root)
    local_java = find_java_in_tree(local_root)
    lifebook_java = java_from_lifebook_runtime()
    java_home = java_from_java_home()
    path_java = java_from_path()
    epubcheck_jar = (
        books_root
        / "node_modules"
        / "epubchecker"
        / "vendors"
        / "epubcheck-5.2.1"
        / "epubcheck.jar"
    )
    available_java = local_java or lifebook_java or java_home or path_java
    return {
        "books_root": str(books_root),
        "local_tools_root": str(books_root / "tools"),
        "local_jre": {
            "present": local_java is not None,
            "path": str(local_root),
            "java_path": str(local_java) if local_java else "",
        },
        "lifebook_java": str(lifebook_java) if lifebook_java else "",
        "java_home": str(java_home) if java_home else "",
        "path_java": str(path_java) if path_java else "",
        "java_available": available_java is not None,
        "selected_java": str(available_java) if available_java else "",
        "epubchecker_installed": epubcheck_jar.exists(),
        "epubcheck_jar": str(epubcheck_jar) if epubcheck_jar.exists() else "",
    }


def print_human_status(payload: dict[str, Any]) -> None:
    print(f"books_root: {payload['books_root']}")
    print(f"local_tools_root: {payload['local_tools_root']}")
    print(f"java_available: {payload['java_available']}")
    print(f"selected_java: {payload['selected_java'] or 'MISSING'}")
    print(f"local_jre_present: {payload['local_jre']['present']}")
    print(f"epubchecker_installed: {payload['epubchecker_installed']}")
    if not payload["java_available"]:
        print("Missing Java. Install Java 17+ or run with --jre-zip path/to/zulu17-jre.zip.")
    if not payload["epubchecker_installed"]:
        print("Missing epubchecker. Run npm install from the books directory.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare or check local-only EPUB tooling under books/tools."
    )
    parser.add_argument("--books-root", type=Path, default=default_books_root())
    parser.add_argument("--jre-zip", type=Path, help="Local JRE zip to extract into books/tools/zulu17-jre.")
    parser.add_argument("--force", action="store_true", help="Replace an existing local JRE cache.")
    parser.add_argument("--check", action="store_true", help="Only check current local tools.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    install_result: dict[str, Any] | None = None
    try:
        if args.jre_zip:
            install_result = ensure_local_jre(args.books_root, args.jre_zip, args.force)
        payload = collect_status(args.books_root)
        if install_result:
            payload["install"] = install_result
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            if install_result:
                print(f"local_jre_install: {install_result['status']}")
                print(f"local_jre_java: {install_result['java_path']}")
            print_human_status(payload)
        return 0 if payload["java_available"] else 1
    except Exception as exc:
        if args.json:
            print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
