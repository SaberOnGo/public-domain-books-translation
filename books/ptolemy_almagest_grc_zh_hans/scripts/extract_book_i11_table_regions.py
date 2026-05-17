from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import fitz
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PDF = PROJECT_ROOT / "source" / "facsimile" / "Almagest_Complete_Heiberg_1898.pdf"
OUT_DIR = PROJECT_ROOT / "source" / "tables" / "book_i_11_chord_table_regions"
REGION_CSV = PROJECT_ROOT / "source" / "tables" / "book_i_11_chord_table_regions.csv"


@dataclass(frozen=True)
class Region:
    viewer_page: int
    printed_page: int
    side: str
    x0: float
    y0: float
    x1: float
    y1: float


# Fractions are relative to each rendered PDF viewer page. Each viewer page
# contains two printed pages. The crop intentionally keeps a small margin around
# the table body so no source glyph, half-degree mark, final column, or final
# row is cut before row-level transcription.
REGIONS: list[Region] = [
    Region(28, 48, "left", 0.045, 0.095, 0.475, 0.955),
    Region(28, 49, "right", 0.560, 0.045, 0.955, 0.760),
    Region(29, 50, "left", 0.045, 0.060, 0.475, 0.965),
    Region(29, 51, "right", 0.560, 0.045, 0.955, 0.760),
    Region(30, 52, "left", 0.045, 0.070, 0.475, 0.965),
    Region(30, 53, "right", 0.560, 0.045, 0.955, 0.760),
    Region(31, 54, "left", 0.045, 0.060, 0.475, 0.965),
    Region(31, 55, "right", 0.560, 0.045, 0.955, 0.760),
    Region(32, 56, "left", 0.045, 0.075, 0.475, 0.965),
    Region(32, 57, "right", 0.560, 0.055, 0.955, 0.760),
    Region(33, 58, "left", 0.045, 0.060, 0.475, 0.965),
    Region(33, 59, "right", 0.560, 0.045, 0.955, 0.760),
    Region(34, 60, "left", 0.045, 0.060, 0.475, 0.965),
    Region(34, 61, "right", 0.560, 0.045, 0.955, 0.760),
    Region(35, 62, "left", 0.045, 0.060, 0.475, 0.955),
    Region(35, 63, "right", 0.560, 0.060, 0.955, 0.760),
]


def render_page(doc: fitz.Document, viewer_page: int, zoom: float) -> Image.Image:
    page = doc[viewer_page - 1]
    pixmap = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    mode = "RGB" if pixmap.n < 4 else "RGBA"
    return Image.frombytes(mode, (pixmap.width, pixmap.height), pixmap.samples).convert("RGB")


def crop_region(image: Image.Image, region: Region) -> Image.Image:
    width, height = image.size
    box = (
        int(round(region.x0 * width)),
        int(round(region.y0 * height)),
        int(round(region.x1 * width)),
        int(round(region.y1 * height)),
    )
    return image.crop(box)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    rendered: dict[int, Image.Image] = {}
    rows: list[dict[str, object]] = []
    for region in REGIONS:
        if region.viewer_page not in rendered:
            rendered[region.viewer_page] = render_page(doc, region.viewer_page, zoom=4.0)
        image = rendered[region.viewer_page]
        crop = crop_region(image, region)
        filename = f"book_i11_p{region.printed_page:03d}_{region.side}_table_region.png"
        out_path = OUT_DIR / filename
        crop.save(out_path)
        rows.append(
            {
                "printed_page": region.printed_page,
                "pdf_viewer_page": region.viewer_page,
                "side": region.side,
                "region_fraction": f"{region.x0:.3f},{region.y0:.3f},{region.x1:.3f},{region.y1:.3f}",
                "region_image": out_path.relative_to(PROJECT_ROOT).as_posix(),
                "extraction_status": "REGION_CROPPED__ROW_TRANSCRIPTION_PENDING",
                "notes": "Heiberg PDF facsimile is primary evidence; PAL has no table rows.",
            }
        )

    with REGION_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "printed_page",
                "pdf_viewer_page",
                "side",
                "region_fraction",
                "region_image",
                "extraction_status",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {REGION_CSV.relative_to(PROJECT_ROOT)} rows={len(rows)}")
    print(f"wrote {OUT_DIR.relative_to(PROJECT_ROOT)}/*.png")


if __name__ == "__main__":
    main()
