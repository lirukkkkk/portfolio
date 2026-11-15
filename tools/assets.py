# -*- coding: utf-8 -*-
"""Gera imagens otimizadas (AVIF + WebP) e o manifest usado pelo build."""
import os, sys, json, hashlib
from PIL import Image, ImageOps
sys.path.insert(0, os.path.dirname(__file__))
from content import CASES, SRC

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site/assets/img")
man = {}

def widths(w):
    return [480, 960] if w <= 1200 else [800, 1600]

def export(src, slug, idx):
    if src.startswith("RENDER/"):
        p = os.path.join(ROOT, "tools/_render", src[7:])
    else:
        p = os.path.join(ROOT, SRC, src)
    name = hashlib.md5(src.encode()).hexdigest()[:10]
    d = os.path.join(OUT, slug); os.makedirs(d, exist_ok=True)
    im = ImageOps.exif_transpose(Image.open(p))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        a = im.getchannel("A")
        if a.getextrema()[0] < 250:
            lum = Image.composite(im.convert("L"), Image.new("L", im.size, 0), a)
            bright = sum(lum.getdata()) / max(1, sum(1 for v in a.getdata() if v > 128)) > 150
            bg = Image.new("RGBA", im.size, (24, 24, 23, 255) if bright else (242, 241, 237, 255))
            im = Image.alpha_composite(bg, im)
    im = im.convert("RGB")
    im.info.pop("icc_profile", None)
    W, H = im.size
    ws = widths(W)
    for w in ws:
        h = round(H * w / W)
        r = im.resize((w, h), Image.LANCZOS)
        for ext, kw in (("avif", {"quality": 58, "speed": 6}), ("webp", {"quality": 80, "method": 5})):
            f = os.path.join(d, f"{name}-{w}.{ext}")
            if not os.path.exists(f):
                r.save(f, **kw)
    # paleta (cores dominantes)
    q = im.resize((120, 150)).quantize(6, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:18]; counts = sorted(q.getcolors(), reverse=True)
    cols = ["#%02x%02x%02x" % tuple(pal[i*3:i*3+3]) for _, i in counts]
    man[src] = {"base": f"assets/img/{slug}/{name}", "w": ws, "ratio": [W, H], "colors": cols}

for c in CASES:
    i = 0
    for g in c["groups"]:
        if g["kind"] == "video": continue
        for it in g["items"]:
            if it in man: continue
            i += 1; export(it, c["slug"], i)
    if c["cover"] not in man:
        i += 1; export(c["cover"], c["slug"], i)
    print(c["slug"], i)

json.dump(man, open(os.path.join(ROOT, "tools/manifest.json"), "w"), ensure_ascii=False, indent=1)
