# -*- coding: utf-8 -*-
"""Gera as logos dos clientes em versão de uma cor (máscara branca com transparência) para a faixa
"Marcas que já confiaram no meu trabalho". No site a cor vem do tema via CSS (mask-image).
Saída: site/assets/logos/<slug>.png   Uso: python3 tools/logos.py"""
import os, colorsys
from PIL import Image, ImageOps, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Meus Trabalhos separados por cliente")
OUT = os.path.join(ROOT, "site/assets/logos")
os.makedirs(OUT, exist_ok=True)
H = 160  # altura final (px), o CSS reduz

# (slug, arquivo, método, recorte relativo opcional (x0,y0,x1,y1))
#   alpha  = usa a transparência do PNG
#   light  = partes claras viram logo (logo branca sobre fundo escuro)
#   dark   = partes escuras viram logo (logo preta sobre fundo claro)
#   color  = partes claras ou saturadas viram logo (logo colorida sobre fundo escuro)
LOGOS = [
    ("next-step", "Next Step/Logo 2026/Vector-1.png", "alpha", None),
    ("pod-mais", "POD+/Logo/Logo.png", "alpha", None),
    ("inovorto", "InovOrto/InovOrto.png", "alpha", None),
    ("brenda-seda", "Dr Brenda/Logo/Brenda Horizontal.png", "alpha", None),
    ("breno-lima", "Arquiteto Breno Lima/Logo/Vector.png", "alpha", None),
    ("cop", "_Capas/cop.jpg", "light", (0.1, 0.3, 0.9, 0.7)),
    ("cr1a-grime", "_Capas/cr1a-grime.jpg", "color", (0.08, 0.25, 0.92, 0.75)),
    ("ruido", "_Capas/ruido.jpg", "light", (0.1, 0.35, 0.9, 0.65)),
    ("sucateiro", "_Capas/sucateiro.jpg", "dark", (0.08, 0.36, 0.92, 0.64)),
    ("terra-a-vista", "TERRAAVISTA/LOGO/LOGOPRETOSFUNDO.png", "auto", None),
]


def mask_of(im, method):
    if method == "auto":
        method = "alpha" if im.mode == "RGBA" and im.getchannel("A").getextrema()[0] < 250 else "dark"
    if method == "alpha":
        return im.convert("RGBA").getchannel("A")
    rgb = im.convert("RGB")
    L = rgb.convert("L")
    if method == "light":
        return L.point(lambda v: 255 if v > 175 else (0 if v < 120 else int((v - 120) / 55 * 255)))
    if method == "dark":
        return L.point(lambda v: 255 if v < 80 else (0 if v > 140 else int((140 - v) / 60 * 255)))
    if method == "color":
        px = rgb.load(); w, h = rgb.size
        m = Image.new("L", rgb.size, 0); mp = m.load()
        for y in range(h):
            for x in range(w):
                r, g, b = px[x, y]
                hh, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                mp[x, y] = 255 if (v > 0.7 and s < 0.25) or (s > 0.3 and v > 0.3) else 0
        return m.filter(ImageFilter.MedianFilter(3))
    raise ValueError(method)


for slug, rel, method, crop in LOGOS:
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, rel)))
    if crop:
        w, h = im.size
        im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    if method == "color":  # reduz antes do laço por pixel
        im = im.convert("RGB"); im.thumbnail((700, 700))
    m = mask_of(im, method)
    box = m.point(lambda v: 255 if v > 40 else 0).getbbox()
    m = m.crop(box)
    m = m.resize((max(1, round(m.width * H / m.height)), H), Image.LANCZOS)
    out = Image.new("RGBA", m.size, (255, 255, 255, 0))
    out.putalpha(m)
    out.save(os.path.join(OUT, f"{slug}.png"), optimize=True)
    print(slug, out.size)
