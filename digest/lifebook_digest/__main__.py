from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import run_digest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the optional LifeBook Digest post-EPUB step.",
    )
    parser.add_argument(
        "--book-root",
        default=".",
        help="Book project root. Defaults to the current directory.",
    )
    args = parser.parse_args()
    result = run_digest(Path(args.book_root))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
