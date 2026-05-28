from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PUBLIC_SNIPPETS = [
    "公版说明",
    "公版来源",
    "公开授权",
    "公开 release",
    "可发布 EPUB",
    "Project Gutenberg",
    "CC BY-NC-SA",
    "PUBLICATION_PASS",
    "LICENSED_PASS",
    "public-domain",
    "Public-domain",
    "public release",
    "publishable release",
]

FORBIDDEN_LIFEBOOK_PRODUCER_SNIPPETS = [
    "LifeBook 书坊 SaberOnGo",
    "LifeBook 书坊 +",
    "LifeBook 书坊 译制",
    "LifeBook书坊译制",
]

REQUIRED_BOOK_INFO_SNIPPETS = [
    "参考LifeBook书坊 个人自制",
    "仅供个人自用",
    "不传播",
    "不商业使用",
    "风险由个人承担",
    "LifeBook书坊仅发布",
    "LifeBook 翻译发布系统",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check private-use reader-facing frontmatter.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--write-report", action="store_true", help="Write output/private_reader_facing_policy_check.json.")
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def rel(book_root: Path, path: Path) -> str:
    try:
        return path.relative_to(book_root).as_posix()
    except ValueError:
        return str(path)


def add_issue(issues: list[dict], rule: str, path: str, detail: str) -> None:
    issues.append({"rule": rule, "path": path, "detail": detail})


def frontmatter_candidates(book_root: Path) -> list[Path]:
    roots = [
        book_root / "frontmatter",
        book_root / "output" / "epub_work" / "EPUB",
        book_root / "output" / "book_i_publication" / "epub_source" / "EPUB",
        book_root / "output" / "epub_source" / "EPUB",
    ]
    names = [
        "cover.md",
        "cover.xhtml",
        "cover.html",
        "book_info.md",
        "book-info.md",
        "book_info.xhtml",
        "book-info.xhtml",
        "book_info.html",
        "book-info.html",
        "translator_note.md",
        "translator-note.md",
        "translator_note.xhtml",
        "translator-note.xhtml",
        "translator_note.html",
        "translator-note.html",
        "edition_note.md",
        "edition-note.md",
        "edition_note.xhtml",
        "edition-note.xhtml",
        "edition_note.html",
        "edition-note.html",
    ]
    return [root / name for root in roots for name in names]


def iter_frontmatter_files(book_root: Path) -> list[Path]:
    files = [path for path in frontmatter_candidates(book_root) if path.is_file()]
    return sorted(set(files))


def check_forbidden_public_text(book_root: Path, files: list[Path], issues: list[dict]) -> None:
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        relative = rel(book_root, path)
        for snippet in [*FORBIDDEN_PUBLIC_SNIPPETS, *FORBIDDEN_LIFEBOOK_PRODUCER_SNIPPETS]:
            if snippet in text:
                add_issue(
                    issues,
                    "private_reader_public_or_publisher_wording",
                    relative,
                    f"Private-use frontmatter must not contain public-domain/public-release/LifeBook-publisher wording: {snippet}",
                )


def check_cover(book_root: Path, files: list[Path], issues: list[dict]) -> None:
    cover_files = [path for path in files if path.stem.lower().replace("_", "-") == "cover"]
    if not cover_files:
        add_issue(
            issues,
            "missing_private_cover_frontmatter",
            "cover.md|cover.xhtml",
            "Private-use EPUB/frontmatter must contain a cover file.",
        )
        return
    for path in cover_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        relative = rel(book_root, path)
        if "仅供个人自用" in text or "不传播" in text or "不商业使用" in text:
            add_issue(issues, "private_cover_contains_long_rights_notice", relative, "Private-use cover must not contain the long rights disclaimer; keep the personal-use boundary in book-info/frontmatter.")


def check_book_info(book_root: Path, files: list[Path], issues: list[dict]) -> None:
    book_info_files = [path for path in files if path.stem.lower().replace("_", "-") == "book-info"]
    if not book_info_files:
        add_issue(
            issues,
            "missing_private_book_info_frontmatter",
            "book_info.md|book-info.xhtml",
            "Private-use EPUB/frontmatter must contain book-info with personal-use and risk-boundary wording.",
        )
        return
    for path in book_info_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        relative = rel(book_root, path)
        for snippet in REQUIRED_BOOK_INFO_SNIPPETS:
            if snippet not in text:
                add_issue(
                    issues,
                    "private_book_info_missing_required_boundary",
                    relative,
                    f"Private-use book-info/frontmatter must contain required boundary wording: {snippet}",
                )


def main() -> None:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    issues: list[dict] = []
    files = iter_frontmatter_files(book_root)

    check_forbidden_public_text(book_root, files, issues)
    check_cover(book_root, files, issues)
    check_book_info(book_root, files, issues)

    report = {
        "book_root": str(book_root),
        "ok": not issues,
        "files_checked": [rel(book_root, path) for path in files],
        "issues": issues,
    }
    if args.write_report:
        out = book_root / "output" / "private_reader_facing_policy_check.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if issues:
        for issue in issues:
            print(f"ERROR {issue['rule']}: {issue['path']} {issue['detail']}")
        raise SystemExit(1)
    print(f"private reader-facing policy gate PASS: files={len(files)}")


if __name__ == "__main__":
    main()
