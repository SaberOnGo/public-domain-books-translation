from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODERN_CHECK = PROJECT_ROOT / "source" / "tables" / "book_i_11_chord_table_modern_check.csv"
OUT = PROJECT_ROOT / "source" / "tables" / "book_i_11_chord_table_raw.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    modern_rows = read_csv(MODERN_CHECK)
    rows: list[dict[str, str]] = []
    for modern in modern_rows:
        row_number = int(modern["row_number"])
        rows.append(
            {
                "row_id": f"I.11.r{row_number:03d}",
                "row_number": modern["row_number"],
                "pdf_viewer_page": "",
                "printed_page": "",
                "page_local_row": "",
                "region_image": "",
                "arc_raw_pdf": "",
                "arc_normalized": modern["arc_normalized"],
                "chord_raw_pdf_columns": "",
                "chord_normalized": "",
                "modern_formula_chord": modern["modern_formula_chord"],
                "difference_raw_pdf_columns": "",
                "sixtieths_normalized": "",
                "modern_formula_sixtieths_per_arc_minute": modern["modern_formula_sixtieths_per_arc_minute"],
                "page_assignment_status": "PENDING_PDF_ROW_ALIGNMENT",
                "pdf_transcription_status": "PENDING_PDF_ROW_TRANSCRIPTION",
                "numeric_check_status": "PENDING",
                "english_witness_status": "NOT_USED",
                "notes": "Modern formula values are QA witnesses only and may differ from Ptolemy's table by rounding; assign PDF page/row and fill raw PDF columns from Heiberg crop before using this row as source data.",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {OUT.relative_to(PROJECT_ROOT)} rows={len(rows)}")


if __name__ == "__main__":
    main()
