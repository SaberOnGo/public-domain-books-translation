from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
BACKGROUND = ROOT / "assets" / "cover_background_gpt_image_2.png"
OUT = ROOT / "assets" / "cover.jpg"
WIDTH = 1600
HEIGHT = 2400


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def fit_font(path: str, text: str, start_size: int, max_width: int) -> ImageFont.FreeTypeFont:
    size = start_size
    probe = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(probe)
    while size >= 24:
        face = font(path, size)
        box = draw.textbbox((0, 0), text, font=face)
        if box[2] - box[0] <= max_width:
            return face
        size -= 2
    return font(path, size)


def centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    y: int,
    face: ImageFont.FreeTypeFont,
    fill,
    stroke_width: int = 0,
) -> None:
    draw.text(
        (WIDTH / 2, y),
        text,
        font=face,
        anchor="mm",
        fill=fill,
        stroke_width=stroke_width,
        stroke_fill=(4, 12, 15, 210),
    )


def add_readability_overlays(img: Image.Image) -> Image.Image:
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    pix = overlay.load()
    for y in range(HEIGHT):
        if y < 860:
            alpha = int(132 * (1 - y / 920))
        elif y > 2160:
            alpha = int(92 * ((y - 2160) / 240))
        else:
            alpha = 0
        if alpha:
            for x in range(WIDTH):
                pix[x, y] = (0, 8, 11, alpha)
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def main() -> None:
    if not BACKGROUND.exists():
        raise FileNotFoundError(f"Missing GPT-IMAGE-2 background: {BACKGROUND}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = Image.open(BACKGROUND).convert("RGB")
    if img.size != (WIDTH, HEIGHT):
        img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    img = add_readability_overlays(img)

    draw = ImageDraw.Draw(img, "RGBA")
    regular = r"C:\Windows\Fonts\msyh.ttc"
    bold = r"C:\Windows\Fonts\msyhbd.ttc"

    title_font = fit_font(bold, "幽灵海盗", 190, 1320)
    english_font = fit_font(regular, "The Ghost Pirates", 74, 1260)
    author_font = fit_font(regular, "威廉·霍普·霍奇森 著", 58, 1260)
    producer_font = fit_font(regular, "LifeBook 书坊 译制", 52, 1260)
    source_font = fit_font(regular, "依据 Project Gutenberg #10966 公版原文制作", 34, 1380)

    centered(draw, "幽灵海盗", 310, title_font, (245, 250, 247, 255), stroke_width=3)
    centered(draw, "The Ghost Pirates", 470, english_font, (210, 224, 221, 255), stroke_width=2)
    centered(draw, "威廉·霍普·霍奇森 著", 610, author_font, (238, 245, 242, 255), stroke_width=2)
    centered(draw, "LifeBook 书坊 译制", 700, producer_font, (205, 220, 216, 255), stroke_width=2)
    centered(draw, "依据 Project Gutenberg #10966 公版原文制作", 2258, source_font, (199, 214, 210, 255), stroke_width=2)

    img = img.convert("RGB").filter(ImageFilter.UnsharpMask(radius=1.0, percent=110, threshold=3))
    img.save(OUT, "JPEG", quality=88, optimize=True, progressive=True)
    print(OUT)
    print(OUT.stat().st_size)


if __name__ == "__main__":
    main()
