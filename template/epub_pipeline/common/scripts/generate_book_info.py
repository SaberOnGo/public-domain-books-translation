"""Generate the book-info page from structured metadata instead of writing it by hand.

Hand-written book-info pages drifted across books: four different layouts, missing personal credits,
AI tool names in the credit line, English rights text, source URLs inside the synopsis, and claims of
notes or glossaries the book did not have. This script builds frontmatter/book_info.md from
metadata/book.yaml (fixed fields) and metadata/book_info_sections.md (synopsis, author, background,
written by people or agents but checked here), and fails on missing or placeholder values.

书籍信息页改为由脚本从结构化元数据生成：固定字段来自 metadata/book.yaml，简介、作者简介、创作背景
来自 metadata/book_info_sections.md。缺字段、模板默认值、AI 工具名、简介里混入来源或制作信息时直接失败。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("title", "original_title", "author", "author_original", "translator_name", "translation_date", "source_name", "source_url")
PLACEHOLDER = re.compile(r"^(?:Book Title|Original Author|Translator Name|Publisher Name|YYYY-MM-DD|TODO|TBD|待补.*|\{\{.*\}\})$", re.IGNORECASE)
TOOL_NAMES = re.compile(r"\bCodex\b|ChatGPT|\bGPT\b|\bClaude\b|\bGemini\b|\bCopilot\b|\bOpenAI\b|\bAnthropic\b")
SECTIONS = ("本书简介", "作者简介", "创作背景")
SYNOPSIS_FORBIDDEN = re.compile(r"https?://|Project Gutenberg|LifeBook|译制|EPUB|版权|公版|AI\b|人工智能|QA|门禁")
PRODUCER = {
    "translated": "LifeBook 书坊 {name}",
    "source_original": "EPUB 制作：LifeBook 书坊 {name}",
    "private_use": "参考public-domain-books-translation 开源项目 个人自制",
}


def parse_yaml(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
            if match:
                data[match.group(1)] = match.group(2).strip().strip("'\"")
    return data


def read_sections(path: Path) -> dict[str, str]:
    sections: dict[str, str] = {}
    if not path.exists():
        return sections
    current = None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            current = heading.group(1)
            sections[current] = ""
        elif current:
            sections[current] += line + "\n"
    return {key: re.sub(r"<!--.*?-->", "", value, flags=re.DOTALL).strip() for key, value in sections.items()}


def build(book_root: Path, mode: str) -> tuple[str, list[str]]:
    meta = parse_yaml(book_root / "metadata" / "book.yaml")
    sections = read_sections(book_root / "metadata" / "book_info_sections.md")
    errors: list[str] = []
    required = [key for key in REQUIRED if not (mode == "private_use" and key == "translator_name")]
    for key in required:
        value = meta.get(key, "")
        if not value or PLACEHOLDER.match(value):
            errors.append(f"metadata/book.yaml: `{key}` is missing or still a template value")
    for key, value in meta.items():
        if TOOL_NAMES.search(value):
            errors.append(f"metadata/book.yaml: `{key}` names an AI tool; credits name people or LifeBook only")
    for name in SECTIONS:
        text = sections.get(name, "")
        if not text:
            errors.append(f"metadata/book_info_sections.md: section `## {name}` is missing or empty")
        elif SYNOPSIS_FORBIDDEN.search(text):
            errors.append(f"metadata/book_info_sections.md: `## {name}` mixes in source, rights or production details; keep it about the work")
    producer = PRODUCER[mode].format(name=meta.get("translator_name", "").strip())
    author = f"{meta.get('author', '')}（{meta.get('author_original', '')}" + (f"，{meta['author_years']}" if meta.get("author_years") else "") + "）"
    lines = ["# 书籍信息", "", f"书名：{meta.get('title', '')}", "", f"原书名：{meta.get('original_title', '')}", "", f"作者：{author}", ""]
    if mode == "private_use":
        lines += ["版本：私人学习版本 / Personal study edition", "", f"制作：{producer}", ""]
    else:
        lines += [f"{'制作' if mode == 'source_original' else '译制'}：{producer}", "", f"{'制作' if mode == 'source_original' else '译制'}时间：{meta.get('translation_date', '')}", ""]
    lines += [f"原文来源：{meta.get('source_name', '')}，{meta.get('source_url', '')}", ""]
    if mode != "private_use":
        rights = meta.get("rights_note") or "原书为公版作品；跨国家或地区发行前，请复核目标地区的版权状态。"
        lines += [f"公版说明：{rights}", ""]
    for name in SECTIONS:
        lines += [f"## {name}", "", sections.get(name, ""), ""]
    return "\n".join(lines).rstrip() + "\n", errors


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Generate frontmatter/book_info.md from metadata.")
    parser.add_argument("--book-root", default=None)
    parser.add_argument("--mode", choices=sorted(PRODUCER), default="translated", help="translated, source_original (no translation) or private_use.")
    parser.add_argument("--output", default="frontmatter/book_info.md")
    parser.add_argument("--check", action="store_true", help="Validate only; do not write.")
    args = parser.parse_args()
    root = Path(args.book_root).resolve() if args.book_root else DEFAULT_BOOK_ROOT
    text, errors = build(root, args.mode)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    if not args.check:
        out = root / args.output
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {args.output}")
    else:
        print("book-info metadata PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
