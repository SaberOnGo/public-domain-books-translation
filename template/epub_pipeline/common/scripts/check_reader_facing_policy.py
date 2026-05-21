from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_READER_HEADINGS = [
    "译文说明",
    "章节控制说明",
]

BOOK_INFO_FORBIDDEN_SNIPPETS = [
    "prompt",
    "Prompt",
    "QA 过程",
    "工作流日志",
    "制作日志",
    "图表审计日志",
    "项目链接",
    "GitHub 项目",
]

BOOK_INFO_FORBIDDEN_TERMS = [
    "底本与参考",
    "图表说明",
]

LIFEBOOK_URL = "https://yourlifebook.app"
READER_PRODUCTION_RESIDUE_SNIPPETS = [
    "终稿前",
    "QA 校验状态",
    "EPUB 阶段必须",
    "技术记录中，不进入读者正文",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check reader-facing EPUB/frontmatter policy constraints.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--write-report", action="store_true", help="Write output/reader_facing_policy_check.json.")
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def rel(book_root: Path, path: Path) -> str:
    try:
        return path.relative_to(book_root).as_posix()
    except ValueError:
        return str(path)


def add_issue(issues: list[dict], rule: str, path: str, detail: str, line: int | None = None) -> None:
    item = {"rule": rule, "path": path, "detail": detail}
    if line is not None:
        item["line"] = line
    issues.append(item)


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def iter_reader_text_files(book_root: Path) -> list[Path]:
    roots = [
        book_root / "frontmatter",
        book_root / "chapters" / "translated",
        book_root / "chapters" / "final",
        book_root / "output" / "epub_source" / "EPUB",
        book_root / "output" / "book_i_publication" / "epub_source" / "EPUB",
    ]
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        files.extend(
            path
            for path in root.rglob("*")
            if path.is_file() and path.suffix.lower() in {".md", ".xhtml", ".html"}
        )
    return sorted(set(files))


def check_reader_headings(book_root: Path, files: list[Path], issues: list[dict]) -> None:
    pattern = re.compile(r"^\s*#{1,6}\s+(" + "|".join(map(re.escape, FORBIDDEN_READER_HEADINGS)) + r")\s*$", re.MULTILINE)
    xhtml_pattern = re.compile(r"<h[1-6][^>]*>\s*(" + "|".join(map(re.escape, FORBIDDEN_READER_HEADINGS)) + r")\s*</h[1-6]>", re.IGNORECASE)
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in pattern.finditer(text):
            add_issue(
                issues,
                "reader_facing_control_heading",
                rel(book_root, path),
                "Chapter/control notes must not be reader-visible headings. Move them to QA, notes, or concise frontmatter.",
                line_number(text, match.start()),
            )
        for match in xhtml_pattern.finditer(text):
            add_issue(
                issues,
                "reader_facing_control_heading",
                rel(book_root, path),
                "Generated EPUB still contains a reader-visible control heading.",
                line_number(text, match.start()),
            )


def check_book_info(book_root: Path, files: list[Path], issues: list[dict]) -> None:
    book_info_files = [path for path in files if path.name in {"book-info.xhtml", "book-info.html", "book_info.md"}]
    for path in book_info_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        rel_path = rel(book_root, path)
        for snippet in BOOK_INFO_FORBIDDEN_SNIPPETS:
            index = text.find(snippet)
            if index != -1:
                add_issue(
                    issues,
                    "book_info_reader_noise",
                    rel_path,
                    f"book-info must be concise and must not contain reader-facing project/promotion/log text: {snippet}",
                    line_number(text, index),
                )
        for term in BOOK_INFO_FORBIDDEN_TERMS:
            index = text.find(term)
            if index != -1:
                add_issue(
                    issues,
                    "book_info_overdetailed_production_note",
                    rel_path,
                    f"Move detailed production explanation out of book-info: {term}",
                    line_number(text, index),
                )
        rights_label_count = len(re.findall(r"版权说明|权利说明|译本授权", text))
        if rights_label_count > 1:
            add_issue(
                issues,
                "book_info_repeated_rights_labels",
                rel_path,
                "Do not repeat multiple rights/copyright sections in reader-visible book-info.",
            )
        lifebook_count = text.count(LIFEBOOK_URL)
        if lifebook_count > 1:
            add_issue(
                issues,
                "book_info_repeated_lifebook_link",
                rel_path,
                "book-info may contain at most one concise LifeBook link.",
            )
        if LIFEBOOK_URL in text and re.search(r">\s*https?://yourlifebook\.app\s*<", text):
            add_issue(
                issues,
                "book_info_visible_long_lifebook_url",
                rel_path,
                "Use short linked text such as '访问 LifeBook'; do not display the raw LifeBook URL in book-info.",
            )


def check_reader_production_residue(book_root: Path, files: list[Path], issues: list[dict]) -> None:
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        rel_path = rel(book_root, path)
        for snippet in READER_PRODUCTION_RESIDUE_SNIPPETS:
            index = text.find(snippet)
            if index != -1:
                add_issue(
                    issues,
                    "reader_visible_production_residue",
                    rel_path,
                    f"Move production/QA todo wording out of reader-visible text: {snippet}",
                    line_number(text, index),
                )


def main() -> None:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    issues: list[dict] = []
    files = iter_reader_text_files(book_root)

    check_reader_headings(book_root, files, issues)
    check_book_info(book_root, files, issues)
    check_reader_production_residue(book_root, files, issues)

    report = {
        "book_root": ".",
        "ok": not issues,
        "files_checked": [rel(book_root, path) for path in files],
        "issues": issues,
    }
    if args.write_report:
        out = book_root / "output" / "reader_facing_policy_check.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if issues:
        for issue in issues[:80]:
            line = f":{issue['line']}" if "line" in issue else ""
            print(f"ERROR {issue['rule']}: {issue['path']}{line} {issue['detail']}")
        if len(issues) > 80:
            print(f"... {len(issues) - 80} more issues")
        raise SystemExit(1)
    print(f"reader-facing policy gate PASS: files={len(files)}")


if __name__ == "__main__":
    main()
