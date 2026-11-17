# -*- coding: utf-8 -*-
"""Gera o favicon (SVG + PNG) a partir do ícone vetor e o cartão de compartilhamento (og.jpg) na versão preta.
Uso: python3 tools/og.py  (precisa do Google Chrome instalado)"""
import os, re, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from build import script_name, star_svg  # noqa: E402  (reaproveita o nome em lettering e o brilho pontilhado)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
TMP = os.path.join(ROOT, "tools/_render")
os.makedirs(TMP, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BG, FG = "#121211", "#f2f1ed"

# ---------- favicon vetor ----------
svg = open(os.path.join(ROOT, "Icons Alan/Stiker 3.svg"), encoding="utf-8").read()
paths = "".join(f'<path d="{d}"/>' for d in re.findall(r'<path d="([^"]+)"', svg))
fav = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -100 1081 1081">'
       f'<rect x="-60" y="-100" width="1081" height="1081" rx="240" fill="{BG}"/>'
       f'<g fill="{FG}">{paths}</g></svg>')
open(os.path.join(SITE, "assets/avatar/favicon.svg"), "w", encoding="utf-8").write(fav)


def shot(html, out, w, h):
    f = os.path.join(TMP, "shot.html")
    open(f, "w", encoding="utf-8").write(html)
    png = os.path.join(TMP, "shot.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={w},{h}", f"--screenshot={png}", "file://" + f],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    from PIL import Image
    im = Image.open(png).convert("RGB").crop((0, 0, w, h))
    im.save(out, quality=90) if out.endswith(".jpg") else im.save(out)


shot(f'<html><body style="margin:0;background:transparent">{fav.replace("<svg ", "<svg width=180 height=180 ")}</body></html>',
     os.path.join(SITE, "assets/avatar/favicon.png"), 180, 180)

# ---------- cartão de compartilhamento (1200x630, preto) ----------
font = "file://" + os.path.join(SITE, "assets/fonts/host-grotesk-latin.woff2")
og = f'''<html><head><meta charset="utf-8"><style>
@font-face {{ font-family: H; src: url("{font}"); }}
body {{ margin: 0; width: 1200px; height: 630px; background: {BG}; color: {FG}; font-family: H, Helvetica, sans-serif; position: relative; overflow: hidden; }}
.name {{ position: absolute; left: 40px; top: 30px; width: 640px; color: {FG}; }}
.name svg {{ width: 100%; height: auto; display: block; overflow: visible; }}
.name .nw-wipe {{ display: none; }} .name mask {{ display: none; }} .name g[mask] {{ mask: none; }}
.nw-p {{ fill: currentColor; }}
.meta {{ position: absolute; right: 76px; bottom: 64px; text-align: right; font-size: 26px; letter-spacing: -0.01em; }}
.meta small {{ display: block; font-size: 18px; color: #9a9992; margin-top: 8px; text-transform: uppercase; letter-spacing: .04em; }}
.dm {{ position: absolute; color: {FG}; }} .dm.a {{ right: 90px; top: 50px; width: 230px; height: auto; }}
.dm.c {{ right: 330px; top: 170px; width: 190px; height: auto; color: #8f97ff; }}
</style></head><body>
<div class="name">{script_name()}</div>
{star_svg("estrela-2", "a")}{star_svg("estrela-1", "c")}
<div class="meta">Social media, branding e tráfego pago<small>Designer · São Paulo</small></div>
</body></html>'''
shot(og, os.path.join(SITE, "assets/og.jpg"), 1200, 630)
print("favicon + og ok")
