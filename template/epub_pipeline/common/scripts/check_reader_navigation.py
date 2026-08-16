#!/usr/bin/env python3
"""Check reader-visible EPUB navigation labels and their packaged copies."""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
RAW_FILENAME_LABEL_RE = re.compile(r"^(?:bilingual_)?\d+_[A-Za-z0-9][A-Za-z0-9_-]*$")
KNOWN_ENGLISH_FALLBACKS = {"Translator Note", "Preface"}
CJK_RE = re.compile(r"[\u3400-\u9fff]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check reader-visible EPUB navigation labels.")
    parser.add_argument("--book-root", default=None)
    parser.add_argument("--epub", action="append", default=None, help="Check only this EPUB; may be repeated.")
    parser.add_argument("--write-report", action="store_true")
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def rel(book_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(book_root).as_posix()
    except ValueError:
        return path.name


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def nav_entries(text: str) -> list[tuple[str, str]]:
    root = ET.fromstring(text)
    entries: list[tuple[str, str]] = []
    for element in root.iter():
        if local_name(element.tag) != "a":
            continue
        href = element.attrib.get("href", "").strip()
        label = " ".join("".join(element.itertext()).split())
        entries.append((href, label))
    return entries


def read_nav(path: Path) -> str:
    if path.is_dir():
        nav_path = path / "nav.xhtml"
        if not nav_path.is_file():
            raise FileNotFoundError(nav_path)
        return nav_path.read_text(encoding="utf-8")
    with ZipFile(path) as archive:
        return archive.read("EPUB/nav.xhtml").decode("utf-8")


def check_nav(book_root: Path, label: str, path: Path, issues: list[dict]) -> dict[str, object]:
    try:
        entries = nav_entries(read_nav(path))
    except (OSError, KeyError, ET.ParseError) as exc:
        issues.append({"edition": label, "path": rel(book_root, path), "rule": "nav_read", "detail": str(exc)})
        return {"edition": label, "path": rel(book_root, path), "entries": 0}

    for href, title in entries:
        target = Path(urllib.parse.unquote(href.split("#", 1)[0])).stem
        target_stem = target.removeprefix("bilingual_")
        if not title:
            issues.append({"edition": label, "path": rel(book_root, path), "rule": "empty_nav_label", "detail": f"empty label for {href}"})
            continue
        if title in KNOWN_ENGLISH_FALLBACKS:
            issues.append({"edition": label, "path": rel(book_root, path), "rule": "english_fallback_label", "detail": f"{href} is labeled {title!r}"})
        if RAW_FILENAME_LABEL_RE.fullmatch(title) or title in {target, target_stem}:
            issues.append({"edition": label, "path": rel(book_root, path), "rule": "raw_filename_label", "detail": f"{href} exposes internal filename {title!r}"})
        if target != "cover" and not CJK_RE.search(title):
            issues.append({"edition": label, "path": rel(book_root, path), "rule": "non_chinese_nav_label", "detail": f"{href} has no Chinese reader-facing title: {title!r}"})

    return {
        "edition": label,
        "path": rel(book_root, path),
        "entries": len(entries),
        "first_labels": [title for _, title in entries[:8]],
    }


def main() -> None:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    if args.epub:
        candidates = [(Path(value), Path(value).stem) for value in args.epub]
    else:
        candidates = [
            (book_root / "output" / "epub_work" / "EPUB", "target_only_staging"),
            (book_root / "output" / "epub_work_bilingual" / "EPUB", "bilingual_staging"),
            (book_root / "output" / "book.epub", "target_only_epub"),
            (book_root / "output" / "book_bilingual_parallel.epub", "bilingual_epub"),
        ]

    issues: list[dict] = []
    editions: list[dict[str, object]] = []
    for candidate, label in candidates:
        path = candidate if candidate.is_absolute() else book_root / candidate
        if not path.exists():
            issues.append({"edition": label, "path": rel(book_root, path), "rule": "missing_nav_source", "detail": "navigation source does not exist"})
            continue
        editions.append(check_nav(book_root, label, path, issues))

    report = {
        "book_root": ".",
        "status": "PASS" if not issues else "FAIL",
        "editions": editions,
        "issues": issues,
    }
    if args.write_report:
        output = book_root / "output" / "reader_navigation_check.json"
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if issues:
        for issue in issues[:80]:
            print(f"ERROR {issue['rule']}: {issue['path']} {issue['detail']}")
        raise SystemExit(1)
    print(f"reader navigation gate PASS: editions={len(editions)} entries={sum(int(item['entries']) for item in editions)}")


if __name__ == "__main__":
    main()
