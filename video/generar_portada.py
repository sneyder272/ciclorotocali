"""Genera la portada del video y el thumbnail de Devpost.

Requiere Pillow. Uso: python generar_portada.py
Salida: portada_1920x1080.png y portada_1280x720.png
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
W, H = 1920, 1080

BG = "#0B1F33"
PANEL = "#0F2740"
ROAD = "#1E3A52"
YELLOW = "#F2B705"
WHITE = "#F5F7FA"
MUTED = "#9FB3C8"
LINE = "#24445F"

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_REG = "C:/Windows/Fonts/arial.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def dashed_v(draw, x, y0, y1, dash=26, gap=20, width=6, fill=YELLOW):
    y = y0
    while y < y1:
        draw.rounded_rectangle(
            [x - width // 2, y, x + width // 2, min(y + dash, y1)],
            radius=width // 2, fill=fill,
        )
        y += dash + gap


def dashed_h(draw, y, x0, x1, dash=26, gap=20, width=6, fill=YELLOW):
    x = x0
    while x < x1:
        draw.rounded_rectangle(
            [x, y - width // 2, min(x + dash, x1), y + width // 2],
            radius=width // 2, fill=fill,
        )
        x += dash + gap


def build() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Panel decorativo a la derecha
    d.rounded_rectangle([1120, 150, 1810, 930], radius=36, fill=PANEL)
    d.rounded_rectangle([1120, 150, 1810, 930], radius=36, outline=LINE, width=3)

    # Dos vías que se cruzan
    d.rounded_rectangle([1440, 210, 1500, 870], radius=22, fill=ROAD)
    d.rounded_rectangle([1180, 510, 1770, 570], radius=22, fill=ROAD)
    dashed_v(d, 1470, 230, 450)
    dashed_h(d, 540, 1200, 1750)

    # El cruce
    d.ellipse([1416, 486, 1524, 594], fill=YELLOW)
    d.ellipse([1436, 506, 1504, 574], fill=PANEL)
    d.ellipse([1458, 528, 1482, 552], fill=YELLOW)

    # Cifra del cruce
    d.text(
        (1470, 660), "148", font=font(FONT_BOLD, 104), fill=WHITE, anchor="mm"
    )
    d.text(
        (1470, 730), "siniestros con lesionados", font=font(FONT_REG, 26),
        fill=MUTED, anchor="mm",
    )
    d.text(
        (1470, 790), "Calle 70 con Carrera 8", font=font(FONT_BOLD, 26),
        fill=WHITE, anchor="mm",
    )

    # Columna izquierda
    left = 110
    d.text(
        (left, 150), "NEIGHBORHOOD HACKS 2026",
        font=font(FONT_BOLD, 28), fill=MUTED,
    )
    d.text(
        (left, 205), "CicloRoto Vial",
        font=font(FONT_BOLD, 118), fill=WHITE,
    )
    d.text(
        (left, 345), "De la queja a la prioridad",
        font=font(FONT_BOLD, 54), fill=YELLOW,
    )
    d.line([left, 440, left + 760, 440], fill=LINE, width=3)

    # Tres indicadores
    stats = [
        ("51.236", "siniestros con lesionados"),
        ("9.261", "cruces identificados"),
        ("0", "de 17.642 reportes"),
    ]
    x = left
    for i, (valor, etiqueta) in enumerate(stats):
        d.text((x, 500), valor, font=font(FONT_BOLD, 72), fill=WHITE)
        d.text((x, 590), etiqueta, font=font(FONT_REG, 24), fill=MUTED)
        if i == 2:
            d.text(
                (x, 622), "vinculables a una obra",
                font=font(FONT_REG, 24), fill=MUTED,
            )
        x += 330

    # Pie
    d.text(
        (left, 930),
        "Cali, Colombia  ·  Datos abiertos CC-BY  ·  Código MIT",
        font=font(FONT_REG, 24), fill=MUTED,
    )
    d.text(
        (left, 975),
        "github.com/sneyder272/ciclorotocali",
        font=font(FONT_BOLD, 24), fill=WHITE,
    )
    return img


def main() -> None:
    img = build()
    img.save(BASE / "portada_1920x1080.png", optimize=True)
    img.resize((1280, 720), Image.LANCZOS).save(
        BASE / "portada_1280x720.png", optimize=True
    )

    # 3:2 para la galería de Devpost: el diseño 16:9 centrado sobre el mismo fondo.
    tres_dos = Image.new("RGB", (1500, 1000), BG)
    tres_dos.paste(img.resize((1500, 844), Image.LANCZOS), (0, 78))
    tres_dos.save(BASE / "portada_1500x1000.png", optimize=True)

    print("Listo: 1920x1080, 1280x720 y 1500x1000")


if __name__ == "__main__":
    main()
