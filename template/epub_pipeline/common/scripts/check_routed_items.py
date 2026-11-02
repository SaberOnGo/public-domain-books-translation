"""Block release while items routed to "later" are still open.

Chapter gates may pass with routed items (PASS_WITH_ROUTED_ITEMS) or notes such as 终稿前需核对
("verify before the final draft"). Those items used to be forgotten: a gate in one book flagged a
mistranslation for verification, and the book shipped with it. This check lists every routed item in
qa/gates, qa/chapter_controls and qa/refinement, and passes only when qa/routed_items/closure.md
records `open_routed_items: 0` and was written after the newest routed item.

章节门禁允许带“转后续处理”的事项通过（PASS_WITH_ROUTED_ITEMS、“终稿前需核对”等），但这些事项
过去常被遗忘。本检查列出所有转出事项；只有 qa/routed_items/closure.md 写明 `open_routed_items: 0`，
且晚于最新的转出记录，才放行。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
ROUTED = re.compile(r"PASS_WITH_ROUTED_ITEMS|终稿前需核对|发布前需核对|routed_to_final|待终稿核对")
SCAN_DIRS = ("qa/gates", "qa/chapter_controls", "qa/refinement")
CLOSURE = "qa/routed_items/closure.md"


def find_routed(book_root: Path) -> list[dict]:
    items = []
    for folder in SCAN_DIRS:
        for path in sorted((book_root / folder).glob("**/*.md")):
            for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
                if ROUTED.search(line):
                    items.append({"file": path.relative_to(book_root).as_posix(), "line": number,
                                  "text": line.strip()[:160], "mtime": path.stat().st_mtime})
    return items


def closure_state(book_root: Path) -> tuple[bool, float]:
    path = book_root / CLOSURE
    if not path.exists():
        return False, 0.0
    match = re.search(r"open_routed_items\s*:\s*(\d+)", path.read_text(encoding="utf-8", errors="replace"))
    return bool(match and int(match.group(1)) == 0), path.stat().st_mtime


def check(book_root: Path) -> dict:
    items = find_routed(book_root)
    closed, closed_at = closure_state(book_root)
    stale = [item for item in items if item["mtime"] > closed_at]
    status = "PASS" if not items or (closed and not stale) else "FAIL"
    return {"status": status, "routed_item_count": len(items), "closure_file": CLOSURE, "closure_recorded": closed,
            "items_newer_than_closure": len(stale), "items": [{k: v for k, v in i.items() if k != "mtime"} for i in items[:80]]}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Fail while routed gate items are not closed.")
    parser.add_argument("--book-root", default=None)
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    root = Path(args.book_root).resolve() if args.book_root else DEFAULT_BOOK_ROOT
    result = check(root)
    if args.write_report:
        out = root / "output" / "routed_items_check.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"routed items {result['status']}: {result['routed_item_count']} routed, closure_recorded={result['closure_recorded']}, "
          f"newer_than_closure={result['items_newer_than_closure']}")
    if result["status"] == "FAIL":
        for item in result["items"][:10]:
            print(f"  {item['file']}:{item['line']}: {item['text']}")
        print(f"Resolve each item, then write {CLOSURE} listing them with `open_routed_items: 0`. "
              "/ 逐项处理后在 closure.md 记录处理结果并写明 open_routed_items: 0。")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
