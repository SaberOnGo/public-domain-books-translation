from __future__ import annotations

import csv
import math
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT = PROJECT_ROOT / "source" / "tables" / "book_i_11_chord_table_modern_check.csv"


def split_seconds(total_seconds: int) -> tuple[int, int, int]:
    parts, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return parts, minutes, seconds


def split_seconds_with_thirds(value_seconds: float) -> tuple[int, int, int, int]:
    total_thirds = int(round(value_seconds * 60))
    parts, rem = divmod(total_thirds, 3600 * 60)
    minutes, rem = divmod(rem, 60 * 60)
    seconds, thirds = divmod(rem, 60)
    return parts, minutes, seconds, thirds


def fmt_chord(parts: int, minutes: int, seconds: int) -> str:
    return f"{parts};{minutes:02d},{seconds:02d}"


def fmt_sixtieths(parts: int, minutes: int, seconds: int, thirds: int) -> str:
    return f"{parts};{minutes:02d},{seconds:02d},{thirds:02d}"


def fmt_arc(total_minutes: int) -> str:
    degrees, minutes = divmod(total_minutes, 60)
    return f"{degrees}°{minutes:02d}′" if minutes else f"{degrees}°"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    previous_chord_seconds = 0
    rows: list[dict[str, object]] = []
    for row_number in range(1, 361):
        arc_minutes = row_number * 30
        arc_degrees = arc_minutes / 60
        chord_value = 120 * math.sin(math.radians(arc_degrees / 2))
        chord_seconds = int(round(chord_value * 3600))
        c_parts, c_minutes, c_seconds = split_seconds(chord_seconds)

        diff_seconds = chord_seconds - previous_chord_seconds
        per_arc_minute = diff_seconds / 30
        d_parts, d_minutes, d_seconds, d_thirds = split_seconds_with_thirds(per_arc_minute)

        rows.append(
            {
                "row_number": row_number,
                "arc_minutes_total": arc_minutes,
                "arc_normalized": fmt_arc(arc_minutes),
                "modern_formula_chord": fmt_chord(c_parts, c_minutes, c_seconds),
                "modern_formula_chord_total_seconds": chord_seconds,
                "modern_formula_sixtieths_per_arc_minute": fmt_sixtieths(
                    d_parts, d_minutes, d_seconds, d_thirds
                ),
                "modern_formula_increment_total_seconds_from_previous_half_degree": diff_seconds,
                "calculation_method": "120*sin(arc/2), rounded to sexagesimal seconds; used only as modern QA witness",
                "source_role": "MODERN_NUMERIC_QA_ONLY_NOT_SOURCE_TRANSCRIPTION",
            }
        )
        previous_chord_seconds = chord_seconds

    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {OUT.relative_to(PROJECT_ROOT)} rows={len(rows)}")


if __name__ == "__main__":
    main()
