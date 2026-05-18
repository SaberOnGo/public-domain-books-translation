from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a versioned EPUB release artifact and bilingual release note.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--source-epub", default="output/book.epub", help="Source EPUB path relative to the book root.")
    parser.add_argument("--release-dir", default="output/release", help="Release directory relative to the book root.")
    parser.add_argument("--version", default=None, help="Explicit version such as v0.0.1. Defaults to next patch version.")
    parser.add_argument("--main-version", type=int, default=None, help="Main version used when no release state exists.")
    parser.add_argument("--sub-version", type=int, default=None, help="Sub version used when no release state exists.")
    parser.add_argument("--status", choices=("DRAFT", "PASS"), default="DRAFT", help="Release status.")
    parser.add_argument("--require-pass", action="store_true", help="Require PASS gate records before creating release.")
    parser.add_argument("--reason", default="", help="Release reason.")
    parser.add_argument("--changes", action="append", default=[], help="Release change entry. Can be repeated.")
    parser.add_argument("--issues", action="append", default=[], help="Issue entry. Can be repeated.")
    parser.add_argument("--fixes", action="append", default=[], help="Fix entry. Can be repeated.")
    parser.add_argument("--risks", action="append", default=[], help="Risk entry. Can be repeated.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing release artifact for the same version.")
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def rel_or_abs(book_root: Path, path: Path) -> str:
    try:
        return path.relative_to(book_root).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_version(version: str) -> tuple[int, int, int]:
    clean = version[1:] if version.startswith("v") else version
    parts = clean.split(".")
    if len(parts) != 3:
        raise SystemExit(f"version must use vX.Y.Z: {version}")
    return tuple(int(part) for part in parts)  # type: ignore[return-value]


def format_version(main: int, sub: int, patch: int) -> str:
    return f"v{main}.{sub}.{patch}"


def next_version(state: dict, main_override: int | None, sub_override: int | None) -> tuple[int, int, int, str]:
    if state:
        main = int(state.get("main_version", 0))
        sub = int(state.get("sub_version", 0))
        patch = int(state.get("patch_version", 0)) + 1
    else:
        main = 0 if main_override is None else main_override
        sub = 0 if sub_override is None else sub_override
        patch = 1
    return main, sub, patch, format_version(main, sub, patch)


def latest_round_dir(book_root: Path) -> Path | None:
    root = book_root / "reviews" / "random_spotcheck"
    if not root.exists():
        return None
    rounds: list[tuple[int, Path]] = []
    for path in root.iterdir():
        if path.is_dir() and path.name.startswith("round_"):
            try:
                rounds.append((int(path.name.split("_", 1)[1]), path))
            except ValueError:
                continue
    return sorted(rounds)[-1][1] if rounds else None


def gate_summary(book_root: Path) -> dict:
    round_dir = latest_round_dir(book_root)
    validation_report = round_dir / "validation_report.json" if round_dir else None
    validation = read_json(validation_report) if validation_report else {}
    epubcheck = read_json(book_root / "output" / "epubcheck.json")
    lint = read_json(book_root / "output" / "publication_lint.json")
    epubcheck_checker = epubcheck.get("checker", {}) if isinstance(epubcheck, dict) else {}
    lint_issues = lint.get("issues", []) if isinstance(lint, dict) else []
    return {
        "random_spotcheck_round": rel_or_abs(book_root, round_dir) if round_dir else "",
        "random_spotcheck_validation": rel_or_abs(book_root, validation_report) if validation_report and validation_report.exists() else "",
        "release_confidence": validation.get("release_confidence"),
        "random_spotcheck_status": validation.get("status", ""),
        "random_spotcheck_require_pass": bool(validation.get("require_pass", False)),
        "epubcheck_path": "output/epubcheck.json" if epubcheck else "",
        "epubcheck_fatal": int(epubcheck_checker.get("nFatal", 0)) if epubcheck_checker else None,
        "epubcheck_error": int(epubcheck_checker.get("nError", 0)) if epubcheck_checker else None,
        "epubcheck_warning": int(epubcheck_checker.get("nWarning", 0)) if epubcheck_checker else None,
        "publication_lint_path": "output/publication_lint.json" if lint else "",
        "publication_lint_issue_count": len(lint_issues) if lint else None,
    }


def require_pass_gates(summary: dict) -> None:
    errors: list[str] = []
    if summary.get("random_spotcheck_status") != "PASS":
        errors.append("latest random spot-check validation status is not PASS")
    if not summary.get("random_spotcheck_require_pass"):
        errors.append("latest random spot-check validation was not run with --require-pass")
    confidence = summary.get("release_confidence")
    if confidence is None or float(confidence) < 0.80:
        errors.append("release_confidence is missing or below 0.80")
    if not summary.get("epubcheck_path"):
        errors.append("output/epubcheck.json is missing")
    if summary.get("epubcheck_fatal") not in (0, None) or summary.get("epubcheck_error") not in (0, None):
        errors.append("EPUBCheck fatal/error count is not zero")
    if not summary.get("publication_lint_path"):
        errors.append("output/publication_lint.json is missing")
    elif summary.get("publication_lint_issue_count") not in (0, None):
        errors.append("publication lint has unresolved issues")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)


def bullet_lines(values: list[str], fallback: str) -> list[str]:
    items = values or [fallback]
    return [f"- {item}" for item in items]


def append_release_index(path: Path, version: str, epub_name: str, note_name: str, status: str, created_at: str) -> None:
    if not path.exists():
        path.write_text(
            "# Release Index / 版本发布索引\n\n| version | status | epub | release note | created_at |\n| --- | --- | --- | --- | --- |\n",
            encoding="utf-8",
            newline="\n",
        )
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"| {version} | {status} | `{epub_name}` | `{note_name}` | {created_at} |\n")


def main() -> None:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    source_epub = (book_root / args.source_epub).resolve() if not Path(args.source_epub).is_absolute() else Path(args.source_epub).resolve()
    if not source_epub.exists():
        raise SystemExit(f"source EPUB does not exist: {source_epub}")

    release_dir = (book_root / args.release_dir).resolve() if not Path(args.release_dir).is_absolute() else Path(args.release_dir).resolve()
    state_path = release_dir / "release_state.json"
    state = read_json(state_path)
    if args.version:
        main_version, sub_version, patch_version = parse_version(args.version)
        version = format_version(main_version, sub_version, patch_version)
    else:
        main_version, sub_version, patch_version, version = next_version(state, args.main_version, args.sub_version)

    summary = gate_summary(book_root)
    if args.require_pass or args.status == "PASS":
        require_pass_gates(summary)

    release_dir.mkdir(parents=True, exist_ok=True)
    epub_name = f"book_{version}.epub"
    note_name = f"release_note_{version}.md"
    target_epub = release_dir / epub_name
    release_note = release_dir / note_name
    if not args.overwrite and (target_epub.exists() or release_note.exists()):
        raise SystemExit(
            f"release artifact already exists for {version}; create the next patch version or pass --overwrite deliberately"
        )
    shutil.copy2(source_epub, target_epub)

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    size_bytes = target_epub.stat().st_size
    digest = sha256(target_epub)

    reason = args.reason or "Create a versioned EPUB release artifact from the current book build. / 将当前书籍构建产物固化为带版本号的 EPUB 发布文件。"
    note = [
        f"# Release {version} / 版本 {version}",
        "",
        f"status: {args.status}",
        f"main_version: {main_version}",
        f"sub_version: {sub_version}",
        f"patch_version: {patch_version}",
        f"created_at: {created_at}",
        f"epub: {epub_name}",
        f"sha256: {digest}",
        f"size_bytes: {size_bytes}",
        "",
        "## Release Reason / 发布原因",
        "",
        reason,
        "",
        "## Changes / 修改内容",
        "",
        *bullet_lines(args.changes, "Versioned EPUB artifact created; no content change was declared in command arguments. / 已创建版本化 EPUB 文件；命令参数未声明具体内容修改。"),
        "",
        "## Issues / 问题点",
        "",
        *bullet_lines(args.issues, "No new issue entry was declared for this release note. / 本发布说明未声明新的问题条目。"),
        "",
        "## Fixes / 修复方式",
        "",
        *bullet_lines(args.fixes, "No fix entry was declared for this release note. / 本发布说明未声明新的修复条目。"),
        "",
        "## QA And Evidence / QA 与证据",
        "",
        f"- source_epub: `{rel_or_abs(book_root, source_epub)}`",
        f"- random_spotcheck_round: `{summary.get('random_spotcheck_round') or 'MISSING'}`",
        f"- random_spotcheck_validation: `{summary.get('random_spotcheck_validation') or 'MISSING'}`",
        f"- random_spotcheck_status: `{summary.get('random_spotcheck_status') or 'MISSING'}`",
        f"- random_spotcheck_require_pass: `{summary.get('random_spotcheck_require_pass')}`",
        f"- release_confidence: `{summary.get('release_confidence') if summary.get('release_confidence') is not None else 'MISSING'}`",
        f"- epubcheck: `{summary.get('epubcheck_path') or 'MISSING'}`",
        f"- epubcheck_fatal: `{summary.get('epubcheck_fatal') if summary.get('epubcheck_fatal') is not None else 'MISSING'}`",
        f"- epubcheck_error: `{summary.get('epubcheck_error') if summary.get('epubcheck_error') is not None else 'MISSING'}`",
        f"- epubcheck_warning: `{summary.get('epubcheck_warning') if summary.get('epubcheck_warning') is not None else 'MISSING'}`",
        f"- publication_lint: `{summary.get('publication_lint_path') or 'MISSING'}`",
        f"- publication_lint_issue_count: `{summary.get('publication_lint_issue_count') if summary.get('publication_lint_issue_count') is not None else 'MISSING'}`",
        "",
        "## Risks / 风险",
        "",
        *bullet_lines(args.risks, "If status is DRAFT, independent agent review or closure gates may still be incomplete. / 若状态为 DRAFT，独立 Agent 评审或闭环门禁可能尚未全部完成。"),
        "",
        "## Next Iteration / 下一轮迭代",
        "",
        "- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。",
        "- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。",
        "",
    ]
    release_note.write_text("\n".join(note), encoding="utf-8", newline="\n")

    new_state = {
        "current_version": version,
        "main_version": main_version,
        "sub_version": sub_version,
        "patch_version": patch_version,
        "latest_epub": epub_name,
        "latest_release_note": note_name,
        "latest_status": args.status,
        "latest_created_at": created_at,
        "latest_sha256": digest,
        "latest_size_bytes": size_bytes,
        "gate_summary": summary,
    }
    write_json(state_path, new_state)
    append_release_index(release_dir / "release_index.md", version, epub_name, note_name, args.status, created_at)

    print(f"created {rel_or_abs(book_root, target_epub)}")
    print(f"created {rel_or_abs(book_root, release_note)}")
    print(f"version={version}")


if __name__ == "__main__":
    main()
