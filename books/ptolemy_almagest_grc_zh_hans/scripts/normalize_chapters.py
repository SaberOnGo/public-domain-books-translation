from __future__ import annotations

import argparse
import re
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize Markdown chapter whitespace.")
    parser.add_argument("--source-dir", default="chapters/final", help="Chapter directory relative to the book root.")
    parser.add_argument("--check", action="store_true", help="Report files that would change, but do not write.")
    return parser.parse_args()


def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    text = "\n".join(lines)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip() + "\n"


def main() -> None:
    args = parse_args()
    source_dir = BOOK_ROOT / args.source_dir
    if not source_dir.exists():
        raise SystemExit(f"source directory does not exist: {source_dir.relative_to(BOOK_ROOT)}")

    changed: list[str] = []
    for path in sorted(source_dir.rglob("*.md")):
        original = path.read_text(encoding="utf-8")
        normalized = normalize(original)
        if normalized != original:
            changed.append(path.relative_to(BOOK_ROOT).as_posix())
            if not args.check:
                path.write_text(normalized, encoding="utf-8", newline="\n")

    if changed:
        for item in changed:
            print(item)
        if args.check:
            raise SystemExit(1)
    print(f"normalized={len(changed)}")


if __name__ == "__main__":
    main()
