from __future__ import annotations

from pathlib import Path

import fitz
from PIL import Image, ImageChops, ImageDraw, ImageOps


BOOK_ROOT = Path(__file__).resolve().parents[1]
PDF = BOOK_ROOT / "source" / "facsimile" / "Almagest_Complete_Heiberg_1898.pdf"
OUT_DIR = BOOK_ROOT / "assets" / "figures" / "facsimile" / "book_i10"
WORK_DIR = BOOK_ROOT / "preproduction" / "stage2_sample" / "facsimile_work"
RENDER_SCALE = 4.0
TRIM_PADDING_PX = 44
MIN_CLEAR_EDGE_PX = 18
MAX_EDGE_INK_FRACTION = 0.003
HARD_CLIP_EDGE_PX = 3


# Boxes are measured on page renders at zoom=2.0, then converted back to PDF
# coordinates for high-resolution clipped rendering.
FIGURES = [
    {
        "id": "i10_fig01_decagon_pentagon_facsimile.png",
        "pdf_page": 20,
        "box_at_zoom2": (525, 460, 825, 755),
        "caption": "Book I.10 figure 1, decagon and pentagon construction",
    },
    {
        "id": "i10_fig02_cyclic_quadrilateral_lemma_facsimile.png",
        "pdf_page": 22,
        "box_at_zoom2": (900, 165, 1230, 460),
        "erase_boxes_at_zoom2": [(285, 0, 330, 295), (0, 250, 330, 295)],
        "caption": "Book I.10 figure 2, cyclic quadrilateral lemma",
    },
    {
        "id": "i10_fig03_difference_of_arcs_facsimile.png",
        "pdf_page": 23,
        "box_at_zoom2": (510, 185, 835, 460),
        "erase_boxes_at_zoom2": [(0, 0, 325, 18), (0, 0, 42, 275), (0, 245, 325, 275)],
        "caption": "Book I.10 figure 3, difference of arcs",
    },
    {
        "id": "i10_fig04_half_arc_facsimile.png",
        "pdf_page": 23,
        "box_at_zoom2": (915, 280, 1230, 515),
        "erase_boxes_at_zoom2": [(0, 0, 315, 42), (0, 205, 315, 235)],
        "caption": "Book I.10 figure 4, half arc construction",
    },
    {
        "id": "i10_fig05_sum_of_arcs_facsimile.png",
        "pdf_page": 24,
        "box_at_zoom2": (920, 295, 1210, 535),
        "caption": "Book I.10 figure 5, sum of arcs",
    },
    {
        "id": "i10_fig06_chord_arc_ratio_facsimile.png",
        "pdf_page": 25,
        "box_at_zoom2": (925, 470, 1185, 710),
        "caption": "Book I.10 figure 6, chord and arc ratio lemma",
    },
    {
        "id": "i10_fig07_one_degree_bracket_facsimile.png",
        "pdf_page": 26,
        "box_at_zoom2": (925, 365, 1195, 620),
        "caption": "Book I.10 figure 7, one degree bracket",
    },
]


def render_clip(
    doc: fitz.Document,
    pdf_page: int,
    box_at_zoom2: tuple[int, int, int, int],
    erase_boxes_at_zoom2: list[tuple[int, int, int, int]] | None = None,
) -> Image.Image:
    rect = fitz.Rect(*(value / 2.0 for value in box_at_zoom2))
    page = doc[pdf_page - 1]
    pixmap = page.get_pixmap(matrix=fitz.Matrix(RENDER_SCALE, RENDER_SCALE), clip=rect, alpha=False)
    mode = "RGB" if pixmap.n < 4 else "RGBA"
    image = Image.frombytes(mode, (pixmap.width, pixmap.height), pixmap.samples).convert("RGB")
    erase_neighboring_text(image, erase_boxes_at_zoom2 or [])
    assert_no_hard_clip(image)
    trimmed = trim_white_margin(image, padding=TRIM_PADDING_PX)
    trimmed = ImageOps.expand(trimmed, border=TRIM_PADDING_PX, fill="white")
    assert_clear_edges(trimmed)
    return trimmed


def erase_neighboring_text(image: Image.Image, erase_boxes_at_zoom2: list[tuple[int, int, int, int]]) -> None:
    if not erase_boxes_at_zoom2:
        return
    draw = ImageDraw.Draw(image)
    scale = RENDER_SCALE / 2.0
    for box in erase_boxes_at_zoom2:
        left, top, right, bottom = (int(value * scale) for value in box)
        draw.rectangle((left, top, right, bottom), fill="white")


def trim_white_margin(image: Image.Image, padding: int) -> Image.Image:
    background = Image.new("RGB", image.size, "white")
    diff = ImageChops.difference(image, background).convert("L")
    mask = diff.point(lambda value: 255 if value > 18 else 0)
    bbox = mask.getbbox()
    if not bbox:
        return image
    left, top, right, bottom = bbox
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(image.width, right + padding)
    bottom = min(image.height, bottom + padding)
    return image.crop((left, top, right, bottom))


def assert_clear_edges(image: Image.Image) -> None:
    mask = image.convert("L").point(lambda value: 255 if value < 220 else 0)
    width, height = mask.size
    strips = {
        "left": (0, 0, MIN_CLEAR_EDGE_PX, height),
        "right": (width - MIN_CLEAR_EDGE_PX, 0, width, height),
        "top": (0, 0, width, MIN_CLEAR_EDGE_PX),
        "bottom": (0, height - MIN_CLEAR_EDGE_PX, width, height),
    }
    failures: list[str] = []
    for edge, box in strips.items():
        strip = mask.crop(box)
        ink = strip.histogram()[255]
        threshold = max(12, int(strip.width * strip.height * MAX_EDGE_INK_FRACTION))
        if ink > threshold:
            failures.append(f"{edge}={ink}>{threshold}")
    if failures:
        raise ValueError(
            "Facsimile crop has ink too close to the image edge; "
            "expand the rough crop box so labels are not clipped: " + ", ".join(failures)
        )


def assert_no_hard_clip(image: Image.Image) -> None:
    mask = image.convert("L").point(lambda value: 255 if value < 220 else 0)
    width, height = mask.size
    strips = {
        "left": (0, 0, HARD_CLIP_EDGE_PX, height),
        "right": (width - HARD_CLIP_EDGE_PX, 0, width, height),
        "top": (0, 0, width, HARD_CLIP_EDGE_PX),
        "bottom": (0, height - HARD_CLIP_EDGE_PX, width, height),
    }
    failures: list[str] = []
    for edge, box in strips.items():
        strip = mask.crop(box)
        ink = strip.histogram()[255]
        threshold = max(4, int(strip.width * strip.height * 0.0015))
        if ink > threshold:
            failures.append(f"{edge}={ink}>{threshold}")
    if failures:
        raise ValueError(
            "Facsimile rough crop appears to cut through ink at the source edge; "
            "expand the rough crop box or erase neighboring text explicitly: " + ", ".join(failures)
        )


def save_contact_sheet(images: list[tuple[dict[str, object], Image.Image]]) -> None:
    thumbs: list[tuple[dict[str, object], Image.Image]] = []
    for spec, image in images:
        thumb = image.copy()
        thumb.thumbnail((360, 260))
        thumbs.append((spec, thumb))

    width = 760
    row_height = 320
    sheet = Image.new("RGB", (width, row_height * ((len(thumbs) + 1) // 2)), "white")
    draw = ImageDraw.Draw(sheet)
    for index, (spec, thumb) in enumerate(thumbs):
        x = (index % 2) * 380
        y = (index // 2) * row_height
        label = f"{spec['id']} / PDF page {spec['pdf_page']}"
        draw.text((x + 8, y + 8), label, fill="black")
        sheet.paste(thumb.convert("RGB"), (x + 8, y + 34))

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    sheet.save(WORK_DIR / "book_i10_facsimile_figures_contact.jpg", quality=92)


def main() -> None:
    if not PDF.exists():
        raise FileNotFoundError(PDF)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    generated: list[tuple[dict[str, object], Image.Image]] = []
    for spec in FIGURES:
        try:
            image = render_clip(
                doc,
                int(spec["pdf_page"]),
                spec["box_at_zoom2"],
                spec.get("erase_boxes_at_zoom2"),
            )
        except ValueError as exc:
            raise ValueError(f"{spec['id']}: {exc}") from exc
        out = OUT_DIR / str(spec["id"])
        image.save(out, optimize=True)
        generated.append((spec, image))

    save_contact_sheet(generated)
    print(f"wrote {len(generated)} facsimile figures to {OUT_DIR.relative_to(BOOK_ROOT)}")
    print((WORK_DIR / "book_i10_facsimile_figures_contact.jpg").relative_to(BOOK_ROOT))


if __name__ == "__main__":
    main()
