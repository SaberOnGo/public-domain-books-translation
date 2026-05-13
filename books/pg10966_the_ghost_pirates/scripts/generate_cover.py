from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "cover.jpg"
WIDTH = 1600
HEIGHT = 2400


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def centered(draw: ImageDraw.ImageDraw, text: str, y: int, face: ImageFont.FreeTypeFont, fill) -> None:
    draw.text((WIDTH / 2, y), text, font=face, anchor="mm", fill=fill)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (WIDTH, HEIGHT), "#071116")
    pix = img.load()
    random.seed(10966)

    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        red = int(6 + 18 * (1 - abs(t - 0.52)) + 4 * t)
        green = int(16 + 44 * (1 - abs(t - 0.50)) + 8 * t)
        blue = int(22 + 50 * (1 - abs(t - 0.50)))
        for x in range(WIDTH):
            wave = int(8 * math.sin((x / 95) + y / 210) + 5 * math.sin((x / 43) - y / 180))
            noise = random.randint(-3, 3)
            pix[x, y] = (
                max(0, min(255, red + wave + noise)),
                max(0, min(255, green + wave + noise)),
                max(0, min(255, blue + wave + noise)),
            )

    draw = ImageDraw.Draw(img, "RGBA")
    draw.rounded_rectangle((120, 140, 1480, 2260), radius=34, fill=(7, 17, 22, 220), outline=(184, 199, 195, 210), width=4)
    draw.ellipse((1052, 312, 1288, 548), fill=(215, 222, 214, 210))
    draw.ellipse((1086, 342, 1270, 528), fill=(205, 213, 207, 70))

    for i in range(18):
        y = 650 + i * 58
        alpha = 18 if i % 2 else 26
        draw.arc((90 - i * 20, y, 1550 + i * 30, y + 420), 188, 352, fill=(222, 233, 229, alpha), width=6)

    draw.polygon(
        [(120, 1685), (250, 1510), (430, 1410), (650, 1465), (835, 1370), (1040, 1265), (1230, 1320), (1480, 1210), (1480, 2260), (120, 2260)],
        fill=(31, 58, 66, 225),
    )
    draw.polygon(
        [(120, 1905), (180, 1775), (370, 1688), (530, 1725), (710, 1645), (900, 1560), (1110, 1600), (1480, 1460), (1480, 2260), (120, 2260)],
        fill=(93, 117, 121, 125),
    )

    draw.polygon([(460, 1275), (760, 1385), (1130, 1295), (1035, 1450), (560, 1460)], fill=(9, 15, 19, 245), outline=(210, 220, 216, 230))
    for line in [
        ((770, 430), (770, 1320)),
        ((620, 910), (1060, 780)),
        ((620, 910), (765, 510)),
        ((1060, 780), (775, 510)),
        ((770, 640), (525, 1225)),
        ((770, 640), (1115, 1190)),
    ]:
        draw.line(line, fill=(216, 224, 220, 220), width=8)
    draw.polygon([(775, 520), (675, 730), (595, 930), (535, 1215), (675, 1140), (795, 1000), (1060, 790), (955, 690), (880, 595)], fill=(223, 233, 231, 30), outline=(223, 233, 231, 60))
    draw.polygon([(1120, 1030), (1220, 1045), (1308, 1092), (1370, 1160), (1260, 1140), (1175, 1138), (1085, 1168)], fill=(224, 235, 231, 42))

    regular = r"C:\Windows\Fonts\msyh.ttc"
    bold = r"C:\Windows\Fonts\msyhbd.ttc"
    title_font = font(bold, 176)
    top_font = font(regular, 70)
    latin_font = font(regular, 62)
    cjk_font = font(regular, 58)
    small_font = font(regular, 44)

    centered(draw, "LifeBook 公版新译", 350, top_font, (203, 215, 211, 255))
    centered(draw, "幽灵海盗", 700, title_font, (255, 255, 255, 255))
    draw.line((405, 825, 1195, 825), fill=(203, 215, 211, 190), width=5)
    centered(draw, "The Ghost Pirates", 1000, latin_font, (210, 221, 218, 255))
    centered(draw, "威廉·霍普·霍奇森 著", 1138, cjk_font, (255, 255, 255, 255))
    centered(draw, "LifeBook 书坊 SaberOnGo 译制", 1225, small_font, (210, 221, 218, 255))
    centered(draw, "依据 Project Gutenberg #10966 公版原文制作", 2110, small_font, (203, 215, 211, 255))

    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=115, threshold=3))
    img.save(OUT, "JPEG", quality=90, optimize=True, progressive=True)
    print(OUT)
    print(OUT.stat().st_size)


if __name__ == "__main__":
    main()
