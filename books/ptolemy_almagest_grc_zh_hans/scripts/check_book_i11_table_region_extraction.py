from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REGION_CSV = PROJECT_ROOT / "source" / "tables" / "book_i_11_chord_table_regions.csv"
REGION_DIR = PROJECT_ROOT / "source" / "tables" / "book_i_11_chord_table_regions"
STRATEGY = PROJECT_ROOT / "qa" / "technical" / "011_book_i_11_chord_table_strategy.md"
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "011_book_i_11_table_region_extraction_check.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "011_book_i_11_table_region_extraction_check.md"

EXPECTED_PRINTED_PAGES = list(range(48, 64))
EXPECTED_VIEWER_PAGES = list(range(28, 36))
MIN_REGION_WIDTH = 950
MIN_REGION_HEIGHT = 1300
EDGE_MARGIN_PX = 10
MAX_EDGE_INK_RATIO = 0.060


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def read_rows() -> list[dict[str, str]]:
    if not REGION_CSV.exists():
        return []
    with REGION_CSV.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def dark_ratio_on_edge(image_path: Path) -> float:
    image = Image.open(image_path).convert("L")
    width, height = image.size
    left = image.crop((0, 0, EDGE_MARGIN_PX, height))
    right = image.crop((width - EDGE_MARGIN_PX, 0, width, height))
    top = image.crop((0, 0, width, EDGE_MARGIN_PX))
    bottom = image.crop((0, height - EDGE_MARGIN_PX, width, height))
    samples = left.tobytes() + right.tobytes() + top.tobytes() + bottom.tobytes()
    dark = sum(1 for value in samples if value < 80)
    return dark / len(samples)


def collect_checks() -> tuple[list[dict[str, object]], list[str]]:
    checks: list[dict[str, object]] = []
    failures: list[str] = []
    rows = read_rows()

    if not REGION_CSV.exists():
        failures.append(f"missing region csv: {rel(REGION_CSV)}")
    checks.append({"id": "region_csv_exists", "status": "PASS" if REGION_CSV.exists() else "FAIL", "path": rel(REGION_CSV)})

    printed_pages = sorted(int(row["printed_page"]) for row in rows if row.get("printed_page", "").isdigit())
    viewer_pages = sorted({int(row["pdf_viewer_page"]) for row in rows if row.get("pdf_viewer_page", "").isdigit()})
    if printed_pages != EXPECTED_PRINTED_PAGES:
        failures.append(f"printed page coverage mismatch: expected {EXPECTED_PRINTED_PAGES}, got {printed_pages}")
    checks.append(
        {
            "id": "printed_page_coverage",
            "status": "PASS" if printed_pages == EXPECTED_PRINTED_PAGES else "FAIL",
            "expected": EXPECTED_PRINTED_PAGES,
            "actual": printed_pages,
        }
    )
    if viewer_pages != EXPECTED_VIEWER_PAGES:
        failures.append(f"viewer page coverage mismatch: expected {EXPECTED_VIEWER_PAGES}, got {viewer_pages}")
    checks.append(
        {
            "id": "viewer_page_coverage",
            "status": "PASS" if viewer_pages == EXPECTED_VIEWER_PAGES else "FAIL",
            "expected": EXPECTED_VIEWER_PAGES,
            "actual": viewer_pages,
        }
    )

    missing_images: list[str] = []
    small_images: list[str] = []
    clipped_edge_images: list[str] = []
    for row in rows:
        rel_image = row.get("region_image", "")
        image = PROJECT_ROOT / rel_image
        if not image.exists():
            missing_images.append(rel_image)
        elif image.stat().st_size < 30_000:
            small_images.append(rel_image)
        else:
            with Image.open(image) as region_image:
                width, height = region_image.size
            if width < MIN_REGION_WIDTH or height < MIN_REGION_HEIGHT:
                small_images.append(f"{rel_image} ({width}x{height})")
            if dark_ratio_on_edge(image) > MAX_EDGE_INK_RATIO:
                clipped_edge_images.append(rel_image)
    if missing_images:
        failures.append(f"missing region images: {missing_images}")
    if small_images:
        failures.append(f"region images suspiciously small or narrow: {small_images}")
    if clipped_edge_images:
        failures.append(f"region images have too much ink on crop edge; likely clipped or too tight: {clipped_edge_images}")
    checks.append({"id": "region_images_exist", "status": "PASS" if not missing_images else "FAIL", "missing": missing_images})
    checks.append({"id": "region_images_not_tiny", "status": "PASS" if not small_images else "FAIL", "small": small_images})
    checks.append({"id": "region_images_have_edge_margin", "status": "PASS" if not clipped_edge_images else "FAIL", "bad": clipped_edge_images})

    bad_status = [row for row in rows if row.get("extraction_status") != "REGION_CROPPED__ROW_TRANSCRIPTION_PENDING"]
    if bad_status:
        failures.append("one or more region rows have an unexpected extraction_status")
    checks.append({"id": "row_transcription_not_claimed", "status": "PASS" if not bad_status else "FAIL", "bad_count": len(bad_status)})

    strategy_text = STRATEGY.read_text(encoding="utf-8") if STRATEGY.exists() else ""
    required_strategy = [
        "source/tables/book_i_11_chord_table_regions.csv",
        "REGION_CROPPED__ROW_TRANSCRIPTION_PENDING",
        "弦表区域裁图不是弦表转录",
    ]
    missing_strategy = [item for item in required_strategy if item not in strategy_text]
    if missing_strategy:
        failures.append(f"strategy file missing region extraction wording: {missing_strategy}")
    checks.append({"id": "strategy_mentions_region_stage", "status": "PASS" if not missing_strategy else "FAIL", "missing": missing_strategy})

    if (PROJECT_ROOT / "chapters" / "final").exists() and any((PROJECT_ROOT / "chapters" / "final").glob("011_*")):
        failures.append("Book I.11 final chapter exists before table row transcription")
    checks.append({"id": "book_i11_final_absent", "status": "PASS" if not any((PROJECT_ROOT / "chapters" / "final").glob("011_*")) else "FAIL"})

    return checks, failures


def write_reports(checks: list[dict[str, object]], failures: list[str], created: str) -> None:
    status = "PASS_TABLE_REGIONS_CROPPED__ROW_TRANSCRIPTION_PENDING" if not failures else "FAIL"
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(
            {
                "status": status,
                "created_at_utc": created,
                "chapter": "Book I.11",
                "row_transcription_complete": False,
                "translation_allowed": False,
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
        "# Book I.11 弦表区域抽取检查 / Table Region Extraction Check",
        "",
        f"check_status: `{status}`",
        f"created_at_utc: `{created}`",
        "",
        "## 控制结论",
        "",
        "- 本检查只确认 Heiberg PDF 弦表区域已经稳定裁出。",
        "- 区域裁图不是弦表行列转录，不允许把本检查解释为 Book I.11 已翻译或可进入终稿。",
        "- 下一步必须逐行转录 `48`-`63` 页弦表，形成结构化 CSV/JSON 后再进入表格数值校验。",
        "",
        "## 检查项",
        "",
        "| id | status | detail |",
        "|---|---|---|",
    ]
    for check in checks:
        detail = check.get("path", check.get("actual", check.get("missing", check.get("bad_count", ""))))
        lines.append(f"| {check['id']} | {check['status']} | `{detail}` |")
    if failures:
        lines.extend(["", "## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    created = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    checks, failures = collect_checks()
    write_reports(checks, failures, created)
    print(f"wrote {OUT_JSON.relative_to(PROJECT_ROOT)}")
    print(f"wrote {OUT_MD.relative_to(PROJECT_ROOT)}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("Book I.11 table region extraction check passed; row transcription remains pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
