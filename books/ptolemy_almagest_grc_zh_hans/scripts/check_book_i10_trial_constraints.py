from __future__ import annotations

import subprocess
import sys
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]
CHECK_TRANSLATION_CONSTRAINTS = BOOK_ROOT / "scripts" / "check_translation_constraints.py"


def main() -> None:
    subprocess.run(
        [sys.executable, str(CHECK_TRANSLATION_CONSTRAINTS), "--scope=trial-book-i10", "--write-report"],
        cwd=BOOK_ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()
