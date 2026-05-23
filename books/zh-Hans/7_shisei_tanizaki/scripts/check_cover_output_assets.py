from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAX_COVER_BYTES = 800 * 1024


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check that source and final cover assets are copied into output/.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--source-original", default=None, help="Qualified source/background cover path relative to book root.")
    parser.add_argument("--source-cover", default=None, help="Final compressed cover path relative to book root.")
    parser.add_argument("--output-original", default=None, help="Output source/background cover path relative to book root.")
    parser.add_argument("--output-cover", default=None, help="Output final compressed cover path relative to book root.")
    parser.add_argument("--max-cover-bytes", type=int, default=DEFAULT_MAX_COVER_BYTES)
    parser.add_argument("--write-report", action="store_true", help="Write output/cover_output_assets_check.json.")
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def find_repo_root(book_root: Path) -> Path | None:
    for candidate in [book_root, *book_root.parents]:
        if (candidate / "books").is_dir() and (candidate / "template").is_dir():
            return candidate
    return None


def display_root(book_root: Path, repo_root: Path | None) -> str:
    if repo_root is None:
        return "."
    try:
        return book_root.relative_to(repo_root).as_posix()
    except ValueError:
        return "."


def rel(book_root: Path, path: Path) -> str:
    try:
        return path.relative_to(book_root).as_posix()
    except ValueError:
        return str(path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def first_existing(book_root: Path, explicit: str | None, patterns: list[str]) -> Path | None:
    if explicit:
        path = book_root / explicit
        return path if path.exists() else path
    for pattern in patterns:
        matches = sorted(book_root.glob(pattern))
        for path in matches:
            if path.is_file():
                return path
    return None


def add_issue(issues: list[dict], rule: str, detail: str, path: Path | None = None, book_root: Path | None = None) -> None:
    issues.append({"rule": rule, "path": rel(book_root, path) if path and book_root else str(path) if path else "", "detail": detail})


def check_pair(
    *,
    book_root: Path,
    source: Path | None,
    output: Path | None,
    label: str,
    issues: list[dict],
) -> dict:
    entry = {"label": label, "source": rel(book_root, source) if source else "", "output": rel(book_root, output) if output else ""}
    if source is None:
        add_issue(issues, f"missing_{label}_source", f"Cannot locate {label} source cover asset.", book_root=book_root)
        return entry
    if not source.exists():
        add_issue(issues, f"missing_{label}_source", f"{label} source cover asset does not exist.", source, book_root)
        return entry
    if output is None:
        add_issue(issues, f"missing_{label}_output", f"Cannot locate {label} output cover asset under output/.", book_root=book_root)
        return entry
    if not output.exists():
        add_issue(issues, f"missing_{label}_output", f"{label} output cover asset does not exist.", output, book_root)
        return entry
    source_hash = sha256(source)
    output_hash = sha256(output)
    entry.update({"source_sha256": source_hash, "output_sha256": output_hash, "bytes": output.stat().st_size})
    if source_hash != output_hash:
        add_issue(issues, f"stale_{label}_output", f"{label} output copy does not match its source asset.", output, book_root)
    return entry


def main() -> None:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    repo_root = find_repo_root(book_root)
    issues: list[dict] = []

    source_original = first_existing(
        book_root,
        args.source_original,
        [
            "assets/cover_source.png",
            "assets/images/cover_source.png",
            "assets/images/*cover*source*.png",
            "assets/images/*cover*background*.png",
        ],
    )
    source_cover = first_existing(
        book_root,
        args.source_cover,
        [
            "assets/cover.jpg",
            "assets/images/cover.jpg",
            "assets/images/*cover*.jpg",
        ],
    )
    output_original = first_existing(
        book_root,
        args.output_original,
        [
            "output/cover_source.png",
            "output/*cover*source*.png",
            "output/*cover*background*.png",
        ],
    )
    output_cover = first_existing(
        book_root,
        args.output_cover,
        [
            "output/cover.jpg",
            "output/*cover*.jpg",
        ],
    )

    assets = [
        check_pair(book_root=book_root, source=source_original, output=output_original, label="original", issues=issues),
        check_pair(book_root=book_root, source=source_cover, output=output_cover, label="final", issues=issues),
    ]

    if source_cover and source_cover.exists() and source_cover.stat().st_size > args.max_cover_bytes:
        add_issue(
            issues,
            "final_cover_too_large",
            f"Final cover is {source_cover.stat().st_size} bytes; limit is {args.max_cover_bytes}.",
            source_cover,
            book_root,
        )
    if output_cover and output_cover.exists() and output_cover.stat().st_size > args.max_cover_bytes:
        add_issue(
            issues,
            "output_cover_too_large",
            f"Output final cover is {output_cover.stat().st_size} bytes; limit is {args.max_cover_bytes}.",
            output_cover,
            book_root,
        )

    report = {
        "book_root": display_root(book_root, repo_root),
        "ok": not issues,
        "assets": assets,
        "issues": issues,
    }
    if args.write_report:
        out = book_root / "output" / "cover_output_assets_check.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if issues:
        for issue in issues:
            location = f" {issue['path']}" if issue.get("path") else ""
            print(f"ERROR {issue['rule']}:{location} {issue['detail']}")
        raise SystemExit(1)
    print("cover output assets gate PASS")


if __name__ == "__main__":
    main()
