# -*- coding: utf-8 -*-
"""Gera as capas com logo dos clientes (4:5 para listas e 16:9 para o topo do case).
Saída em tools/_render/covers/. Uso: python3 tools/covers.py"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Meus Trabalhos separados por cliente")
OUT = os.path.join(ROOT, "tools/_render/covers")
os.makedirs(OUT, exist_ok=True)

TALL = (1200, 1500)
WIDE = (1920, 1080)


def load(p):
    return Image.open(os.path.join(SRC, p)).convert("RGBA")


def crop_alpha(im):
    return im.crop(im.getchannel("A").getbbox())


def on_color(logo, bg, size, frac):
    """Logo centralizada sobre cor sólida; frac = largura máxima da logo."""
    canvas = Image.new("RGBA", size, bg)
    W, H = size
    lw = int(W * frac)
    lh = int(logo.height * lw / logo.width)
    if lh > H * 0.5:
        lh = int(H * 0.5); lw = int(logo.width * lh / logo.height)
    lg = logo.resize((lw, lh), Image.LANCZOS)
    canvas.alpha_composite(lg, ((W - lw) // 2, (H - lh) // 2))
    return canvas


def cover_crop(im, size):
    """Recorte central preenchendo o formato (como object-fit: cover)."""
    W, H = size
    s = max(W / im.width, H / im.height)
    r = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (r.width - W) // 2, (r.height - H) // 2
    return r.crop((x, y, x + W, y + H))


def save(im, name):
    im.convert("RGB").save(os.path.join(OUT, name), quality=92)


# Next Step: logo completa sobre preto
ns = crop_alpha(load("Next Step/Logo 2026/Vector-1.png"))
save(on_color(ns, (14, 13, 18, 255), TALL, 0.62), "next-step.jpg")
save(on_color(ns, (14, 13, 18, 255), WIDE, 0.34), "next-step-wide.jpg")

# InovOrto: capa em degradê azul já com a logo
inov = load("InovOrto/Frame 3.png")
save(cover_crop(inov, TALL), "inovorto.jpg")
save(cover_crop(inov, WIDE), "inovorto-wide.jpg")

# POD+: capa escura com a logo
pod = load("POD+/Logo/Capa.jpg")
pod_logo = crop_alpha(load("POD+/Logo/Logo.png"))
bg = pod.convert("RGB").getpixel((40, 40)) + (255,)
save(on_color(pod_logo, bg, TALL, 0.62), "pod-mais.jpg")
save(cover_crop(pod, WIDE), "pod-mais-wide.jpg")

# Dra. Brenda Seda: logo recortada da captura sobre o creme da marca
cap = load("Dr Brenda/Logo/Captura de Tela 2026-11-17 às 00.22.21.png").convert("RGB")
cream = cap.getpixel((20, 20))
# área da logo = pixels que diferem do fundo
mask = cap.point(lambda v: 255 if v < 200 else 0).convert("L")
diff = Image.eval(cap.convert("L"), lambda v: 255 if abs(v - sum(cream) / 3) > 18 else 0)
box = diff.getbbox()
logo = cap.crop(box).convert("RGBA")
save(on_color(logo, cream + (255,), TALL, 0.8), "brenda-seda.jpg")
save(on_color(logo, cream + (255,), WIDE, 0.46), "brenda-seda-wide.jpg")

# Breno Lima: B verde-limão sobre oliva
fr = load("Arquiteto Breno Lima/Logo/Frame 3089.png").convert("RGB")
olive = fr.getpixel((10, 10)) + (255,)
b = crop_alpha(load("Arquiteto Breno Lima/Logo/Vector.png"))
save(on_color(b, olive, TALL, 0.42), "breno-lima.jpg")
save(on_color(b, olive, WIDE, 0.2), "breno-lima-wide.jpg")

print("capas ok:", sorted(os.listdir(OUT)))
