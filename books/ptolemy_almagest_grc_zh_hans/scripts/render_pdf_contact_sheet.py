from __future__ import annotations

import argparse
from pathlib import Path

import fitz
from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PDF = PROJECT_ROOT / "source" / "facsimile" / "Almagest_Complete_Heiberg_1898.pdf"


def parse_pages(value: str) -> list[int]:
    pages: list[int] = []
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if end < start:
                raise ValueError(f"Invalid page range: {part}")
            pages.extend(range(start, end + 1))
        else:
            pages.append(int(part))
    if not pages:
        raise ValueError("No pages requested")
    return pages


def render_page(doc: fitz.Document, viewer_page: int, zoom: float) -> Image.Image:
    if viewer_page < 1 or viewer_page > doc.page_count:
        raise ValueError(f"Viewer page {viewer_page} is outside 1..{doc.page_count}")
    page = doc[viewer_page - 1]
    pixmap = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    mode = "RGB" if pixmap.n < 4 else "RGBA"
    return Image.frombytes(mode, (pixmap.width, pixmap.height), pixmap.samples).convert("RGB")


def make_contact_sheet(pages: list[tuple[int, Image.Image]], columns: int, thumb_width: int) -> Image.Image:
    thumbs: list[tuple[int, Image.Image]] = []
    for viewer_page, image in pages:
        thumb = image.copy()
        ratio = thumb_width / thumb.width
        thumb = thumb.resize((thumb_width, max(1, int(thumb.height * ratio))))
        thumbs.append((viewer_page, thumb))

    label_height = 28
    padding = 14
    row_height = max(thumb.height for _, thumb in thumbs) + label_height + padding
    rows = (len(thumbs) + columns - 1) // columns
    width = columns * (thumb_width + padding) + padding
    height = rows * row_height + padding
    sheet = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(sheet)

    for index, (viewer_page, thumb) in enumerate(thumbs):
        col = index % columns
        row = index // columns
        x = padding + col * (thumb_width + padding)
        y = padding + row * row_height
        draw.text((x, y), f"PDF viewer page {viewer_page}", fill="black")
        sheet.paste(thumb, (x, y + label_height))
    return sheet


def main() -> None:
    parser = argparse.ArgumentParser(description="Render selected PDF viewer pages into a contact sheet.")
    parser.add_argument("--pages", required=True, help="Viewer pages, e.g. 4-12,19,28")
    parser.add_argument("--out", required=True, help="Output image path relative to the book project root")
    parser.add_argument("--zoom", type=float, default=1.3)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--thumb-width", type=int, default=300)
    args = parser.parse_args()

    pages = parse_pages(args.pages)
    doc = fitz.open(PDF)
    rendered = [(page, render_page(doc, page, args.zoom)) for page in pages]
    sheet = make_contact_sheet(rendered, args.columns, args.thumb_width)
    out = PROJECT_ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=92)
    print(f"wrote {out.relative_to(PROJECT_ROOT)} pages={','.join(str(page) for page in pages)}")


if __name__ == "__main__":
    main()
