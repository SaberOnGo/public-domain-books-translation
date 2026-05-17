from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW = PROJECT_ROOT / "source" / "tables" / "book_i_11_chord_table_raw.csv"
MODERN_CHECK = PROJECT_ROOT / "source" / "tables" / "book_i_11_chord_table_modern_check.csv"
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "011_book_i_11_chord_table_raw_check.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "011_book_i_11_chord_table_raw_check.md"


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def collect_checks() -> tuple[list[dict[str, object]], list[str], dict[str, int]]:
    checks: list[dict[str, object]] = []
    failures: list[str] = []
    raw_rows = read_csv(RAW)
    modern_rows = read_csv(MODERN_CHECK)

    checks.append({"id": "raw_csv_exists", "status": "PASS" if RAW.exists() else "FAIL", "path": rel(RAW)})
    checks.append(
        {"id": "modern_check_csv_exists", "status": "PASS" if MODERN_CHECK.exists() else "FAIL", "path": rel(MODERN_CHECK)}
    )
    if not RAW.exists():
        failures.append(f"missing raw table csv: {rel(RAW)}")
    if not MODERN_CHECK.exists():
        failures.append(f"missing modern check table csv: {rel(MODERN_CHECK)}")

    raw_count = len(raw_rows)
    modern_count = len(modern_rows)
    if raw_count != 360:
        failures.append(f"raw row count must be 360, got {raw_count}")
    if modern_count != 360:
        failures.append(f"modern check row count must be 360, got {modern_count}")
    checks.append({"id": "raw_row_count_360", "status": "PASS" if raw_count == 360 else "FAIL", "actual": raw_count})
    checks.append(
        {"id": "modern_check_row_count_360", "status": "PASS" if modern_count == 360 else "FAIL", "actual": modern_count}
    )

    pending = sum(1 for row in raw_rows if row.get("pdf_transcription_status") == "PENDING_PDF_ROW_TRANSCRIPTION")
    transcribed = sum(1 for row in raw_rows if row.get("pdf_transcription_status") == "RAW_TRANSCRIBED_FROM_HEIBERG_PDF")
    checked = sum(1 for row in raw_rows if row.get("numeric_check_status") == "PASS")
    disputed = sum(1 for row in raw_rows if row.get("numeric_check_status") == "DISPUTED")

    if transcribed == 0:
        failures.append("no rows have been transcribed from Heiberg PDF yet")
    if checked < raw_count:
        failures.append(f"numeric checks incomplete: {checked}/{raw_count} PASS")
    checks.append({"id": "some_rows_pdf_transcribed", "status": "PASS" if transcribed > 0 else "FAIL", "actual": transcribed})
    checks.append({"id": "all_rows_numeric_checked", "status": "PASS" if raw_count == 360 and checked == 360 else "FAIL", "actual": checked})
    checks.append({"id": "disputed_rows_recorded", "status": "PASS", "actual": disputed})

    if raw_rows:
        first = raw_rows[0].get("arc_normalized")
        last = raw_rows[-1].get("arc_normalized")
        if first != "0°30′" or last != "180°":
            failures.append(f"arc coverage mismatch: first={first}, last={last}")
        checks.append({"id": "arc_coverage_half_degree_to_180", "status": "PASS" if first == "0°30′" and last == "180°" else "FAIL", "first": first, "last": last})

    stats = {
        "raw_count": raw_count,
        "modern_check_count": modern_count,
        "pending_pdf_transcription": pending,
        "pdf_transcribed": transcribed,
        "numeric_pass": checked,
        "numeric_disputed": disputed,
    }
    return checks, failures, stats


def write_reports(checks: list[dict[str, object]], failures: list[str], stats: dict[str, int], created: str) -> None:
    status = "PASS_RAW_TABLE_TRANSCRIBED_AND_NUMERICALLY_CHECKED" if not failures else "FAIL_RAW_TABLE_INCOMPLETE"
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(
            {
                "status": status,
                "created_at_utc": created,
                "chapter": "Book I.11",
                "stats": stats,
                "checks": checks,
                "failures": failures,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Book I.11 弦表 raw table 检查 / Raw Chord Table Check",
        "",
        f"check_status: `{status}`",
        f"created_at_utc: `{created}`",
        "",
        "## 控制结论",
        "",
        "- 本检查确认 `book_i_11_chord_table_raw.csv` 是否已完成 PDF 逐行转录和数值校验。",
        "- `book_i_11_chord_table_modern_check.csv` 只作现代数值 QA 旁证，不是底稿，也不是 Ptolemy 表的 expected source value。",
        "- 只有 360 行全部 `RAW_TRANSCRIBED_FROM_HEIBERG_PDF` 且数值检查通过，Book I.11 才能进入翻译/EPUB 表格生成。",
        "",
        "## 统计",
        "",
    ]
    for key, value in stats.items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## 检查项", "", "| id | status | detail |", "|---|---|---|"])
    for check in checks:
        detail = check.get("path", check.get("actual", check.get("first", "")))
        lines.append(f"| {check['id']} | {check['status']} | `{detail}` |")
    if failures:
        lines.extend(["", "## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    created = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    checks, failures, stats = collect_checks()
    write_reports(checks, failures, stats, created)
    print(f"wrote {OUT_JSON.relative_to(PROJECT_ROOT)}")
    print(f"wrote {OUT_MD.relative_to(PROJECT_ROOT)}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("Book I.11 raw chord table check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
