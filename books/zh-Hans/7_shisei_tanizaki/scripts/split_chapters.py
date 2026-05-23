from __future__ import annotations

import argparse
import re
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Split a Markdown source text into chapter files.")
    parser.add_argument("--source", default="source/source_text.txt", help="Source text path relative to the book root.")
    parser.add_argument("--output-dir", default="chapters/src", help="Output directory relative to the book root.")
    parser.add_argument("--heading-level", type=int, default=1, help="Markdown heading level to split on.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned files without writing.")
    return parser.parse_args()


def slugify(title: str) -> str:
    ascii_slug = re.sub(r"[^a-zA-Z0-9]+", "_", title.lower()).strip("_")
    return ascii_slug or "chapter"


def split_by_heading(text: str, heading_level: int) -> list[tuple[str, str]]:
    marker = "#" * heading_level
    pattern = re.compile(rf"(?m)^{re.escape(marker)}\s+(.+?)\s*$")
    matches = list(pattern.finditer(text))
    if not matches:
        raise SystemExit(f"no level-{heading_level} Markdown headings found")

    chapters: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        title = match.group(1).strip()
        body = text[start:end].strip() + "\n"
        chapters.append((title, body))
    return chapters


def main() -> None:
    args = parse_args()
    source = BOOK_ROOT / args.source
    output_dir = BOOK_ROOT / args.output_dir
    if not source.exists():
        raise SystemExit(f"source file does not exist: {source.relative_to(BOOK_ROOT)}")

    text = source.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    chapters = split_by_heading(text, args.heading_level)
    output_dir.mkdir(parents=True, exist_ok=True)

    for index, (title, body) in enumerate(chapters, 1):
        filename = f"{index:03d}_{slugify(title)}.md"
        target = output_dir / filename
        print(f"{target.relative_to(BOOK_ROOT).as_posix()} <- {title}")
        if not args.dry_run:
            if target.exists():
                raise SystemExit(f"refusing to overwrite existing chapter: {target.relative_to(BOOK_ROOT)}")
            target.write_text(body, encoding="utf-8", newline="\n")

    print(f"chapters={len(chapters)}")


if __name__ == "__main__":
    main()
