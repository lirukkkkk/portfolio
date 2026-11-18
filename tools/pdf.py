# -*- coding: utf-8 -*-
"""Gera o portfólio resumido em PDF (16:9, versão escura, mesma identidade do site).
Saída: site/assets/portfolio-alan-veloso.pdf   Uso: python3 tools/pdf.py  (precisa do Google Chrome)"""
import os, sys, subprocess, hashlib
from html import escape as e
from PIL import Image, ImageOps

sys.path.insert(0, os.path.dirname(__file__))
from content import CASES, SERVICES, T, WHATSAPP, EMAIL, INSTAGRAM, BEHANCE, SEGMENTS, PHOTOS  # noqa: E402
from build import script_name, star_svg, SITE_URL  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Meus Trabalhos separados por cliente")
TMP = os.path.join(ROOT, "tools/_render/pdf")
os.makedirs(TMP, exist_ok=True)
OUT = os.path.join(ROOT, "site/assets/portfolio-alan-veloso.pdf")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BY = {c["slug"]: c for c in CASES}

# Cases do PDF e as peças de cada um (índice na lista de imagens do case; "v:nome" = quadro do vídeo)
PICKS = [
    ("trafego-pago", [0, 1, 2, 9]),
    ("pod-mais", [0, 2, 7]),
    ("next-step", [11, 12, 0]),
    ("breno-lima", [0, 4, 8]),
    ("inovorto", ["v:inovorto-reels", "v:inovorto-aditek", 0]),
    ("brenda-seda", [0, 1, 2]),
    ("kits-odonto", [9, 24, 39]),
    ("terra-a-vista", [3, 4, 6]),
]


def src_path(rel):
    if rel.startswith("RENDER/"):
        return os.path.join(ROOT, "tools/_render", rel[7:])
    if rel.startswith("FOTO/"):
        return os.path.join(ROOT, "Fotos Alan", rel[5:])
    return os.path.join(SRC, rel)


def jpg(path, h=1000):
    """Versão JPEG leve da imagem (o PDF fica pequeno para mandar no WhatsApp)."""
    name = hashlib.md5(path.encode()).hexdigest()[:12] + ".jpg"
    out = os.path.join(TMP, name)
    if not os.path.exists(out):
        im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        if im.height > h:
            im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
        im.save(out, quality=78, optimize=True, progressive=True)
    w, hh = Image.open(out).size
    return "file://" + out, w / hh


def case_images(c, picks):
    flat = [it for g in c["groups"] if g["kind"] != "video" for it in g["items"]]
    imgs = []
    for p in picks:
        if isinstance(p, str) and p.startswith("v:"):
            imgs.append(jpg(os.path.join(ROOT, f"site/assets/video/{p[2:]}-poster.jpg")))
        elif flat:
            imgs.append(jpg(src_path(flat[p % len(flat)])))
    return imgs


def row(imgs, height=560, maxw=980):
    """Peças lado a lado com a mesma altura; para quando a largura acaba."""
    html, used = "", 0
    for url, ratio in imgs:
        w = ratio * height
        if used and used + w > maxw:
            break
        html += f'<img src="{url}" style="height:{height}px;width:{w:.0f}px">'
        used += w + 16
    return html


font = "file://" + os.path.join(ROOT, "site/assets/fonts/host-grotesk-latin.woff2")
photo, _ = jpg(src_path(PHOTOS[0]), 1100)
site = SITE_URL + "/"
wa = f"https://wa.me/{WHATSAPP}"

pages = []
# 1. capa (mesma composição do cartão de compartilhamento)
pages.append(f'''<section class="pg cover">
<img class="photo" src="{photo}">
<div class="name">{script_name()}</div>
{star_svg("estrela-2", "st a")}{star_svg("estrela-1", "st b")}
<div class="meta">Social media, branding e tráfego pago<small>Portfólio 2026 · Designer · São Paulo</small></div>
</section>''')

# 2. sobre + serviços
svc = "".join(f'<li><span class="n">{i+1:02d}</span><div><h3>{e(h["pt"])}</h3><p>{e(p["pt"])}</p></div></li>' for i, (h, p, _c) in enumerate(SERVICES))
pages.append(f'''<section class="pg about">
<div class="col">
<p class="pill">{e(T["about.hi"]["pt"])}</p>
<p class="lead">{e(T["about.p1"]["pt"])}</p>
<p class="sub">{e(T["about.p2"]["pt"])}</p>
</div>
<div class="col"><h2>O que eu faço</h2><ol class="svc">{svc}</ol></div>
</section>''')

# 3. cases
for i, (slug, picks) in enumerate(PICKS):
    c = BY[slug]
    url = f"{site}trabalhos/{slug}.html"
    credit = f'<p class="credit">{e(c["credit"]["pt"])}</p>' if c.get("credit") else ""
    pages.append(f'''<section class="pg case">
<div class="info">
<p class="idx">{i+1:02d} / {len(PICKS):02d}</p>
<h2>{e(c["client"])}</h2>
<p class="seg">{e(" · ".join([SEGMENTS[c["segment"]]["pt"]] + [d for d in c["deliver"]["pt"] if d != SEGMENTS[c["segment"]]["pt"]]))}</p>
<p class="title">{e(c["title"]["pt"])}</p>
<p class="intro">{e(c["intro"]["pt"])}</p>
{credit}
<a class="more" href="{url}">Ver o case completo →</a>
</div>
<div class="pics">{row(case_images(c, picks))}</div>
</section>''')

# 4. contato
pages.append(f'''<section class="pg contact">
{star_svg("estrela-2", "st c")}
<h2>Vamos conversar?</h2>
<p class="lede">Me conta o que você precisa. Respondo de segunda a sexta, das 9h às 22h.</p>
<ul>
<li><span>WhatsApp</span><a href="{wa}">+55 11 96574-6636</a></li>
<li><span>E-mail</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><span>Instagram</span><a href="{INSTAGRAM}">@lirukkkkk</a></li>
<li><span>Portfólio completo</span><a href="{site}">{site.replace("https://", "")}</a></li>
</ul>
<div class="sign">{script_name()}</div>
</section>''')

BG, FG, MUTE, LINE, ACC = "#121211", "#edece7", "#9a9992", "#2d2d2b", "#8f97ff"
html = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>
@font-face {{ font-family: H; src: url("{font}"); }}
@page {{ size: 1600px 900px; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; background: {BG}; color: {FG}; font-family: H, Helvetica, Arial, sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.pg {{ width: 1600px; height: 900px; position: relative; overflow: hidden; page-break-after: always; break-after: page; padding: 80px 96px; }}
.pg:last-child {{ page-break-after: auto; }}
a {{ color: {FG}; }}
.nw-p {{ fill: currentColor; }} .nw-wipe, mask {{ display: none; }} g[mask] {{ mask: none; }}
.name svg, .sign svg {{ width: 100%; height: auto; display: block; overflow: visible; }}
.st {{ position: absolute; color: {FG}; height: auto; }}
/* capa */
.cover .photo {{ position: absolute; left: 96px; top: 90px; width: 540px; height: 720px; object-fit: cover; object-position: 50% 35%; }}
.cover .name {{ position: absolute; left: 640px; top: 70px; width: 860px; color: {FG}; z-index: 2; }}
.cover .st.a {{ right: 90px; top: 60px; width: 290px; opacity: .85; }}
.cover .st.b {{ left: 560px; top: 220px; width: 280px; color: {ACC}; opacity: .7; }}
.cover .meta {{ position: absolute; right: 100px; bottom: 90px; text-align: right; font-size: 34px; letter-spacing: -0.01em; z-index: 2; }}
.cover .meta small {{ display: block; font-size: 20px; color: {MUTE}; margin-top: 10px; text-transform: uppercase; letter-spacing: .05em; }}
/* sobre */
.about {{ display: grid; grid-template-columns: 1fr 1fr; gap: 96px; align-items: start; padding-top: 110px; }}
.pill {{ display: inline-block; border: 2px solid {FG}; border-radius: 999px; padding: 8px 24px; font-size: 22px; font-weight: 600; margin: 0 0 36px; }}
.lead {{ font-size: 38px; line-height: 1.25; letter-spacing: -0.02em; margin: 0; }}
.sub {{ font-size: 23px; line-height: 1.5; color: #c9c8c2; margin: 30px 0 0; }}
.about h2 {{ font-size: 22px; font-weight: 500; color: {MUTE}; text-transform: uppercase; letter-spacing: .05em; margin: 10px 0 24px; }}
.svc {{ list-style: none; margin: 0; padding: 0; border-top: 1px solid {FG}; }}
.svc li {{ display: grid; grid-template-columns: 54px 1fr; gap: 12px; padding: 16px 0; border-bottom: 1px solid {LINE}; }}
.svc .n {{ color: {MUTE}; font-size: 18px; padding-top: 4px; }}
.svc h3 {{ margin: 0 0 4px; font-size: 25px; font-weight: 500; letter-spacing: -0.01em; }}
.svc p {{ margin: 0; font-size: 17px; line-height: 1.4; color: {MUTE}; }}
/* case */
.case {{ display: grid; grid-template-columns: 440px 1fr; gap: 64px; align-items: center; }}
.idx {{ color: {MUTE}; font-size: 18px; margin: 0 0 18px; }}
.case h2 {{ font-size: 56px; line-height: 1; letter-spacing: -0.035em; font-weight: 500; margin: 0 0 14px; }}
.seg {{ font-size: 17px; color: {MUTE}; margin: 0 0 30px; line-height: 1.4; }}
.case .title {{ font-size: 28px; line-height: 1.2; letter-spacing: -0.02em; margin: 0 0 18px; }}
.intro {{ font-size: 18px; line-height: 1.5; color: #c9c8c2; margin: 0; }}
.credit {{ font-size: 15px; color: {MUTE}; margin: 18px 0 0; }}
.more {{ display: inline-block; margin-top: 28px; font-size: 18px; color: {ACC}; text-decoration: none; }}
.pics {{ display: flex; gap: 16px; justify-content: flex-end; align-items: center; }}
.pics img {{ object-fit: cover; border-radius: 4px; display: block; }}
/* contato */
.contact h2 {{ font-size: 140px; line-height: .95; letter-spacing: -0.045em; font-weight: 500; margin: 60px 0 24px; max-width: 900px; }}
.contact .lede {{ font-size: 26px; color: #c9c8c2; margin: 0 0 48px; }}
.contact ul {{ list-style: none; margin: 0; padding: 0; width: 760px; border-top: 1px solid {FG}; }}
.contact li {{ display: flex; justify-content: space-between; padding: 18px 0; border-bottom: 1px solid {LINE}; font-size: 24px; }}
.contact li span {{ color: {MUTE}; }}
.contact li a {{ text-decoration: none; }}
.contact .st.c {{ right: 120px; top: 90px; width: 300px; color: {ACC}; }}
.contact .sign {{ position: absolute; right: 90px; bottom: 50px; width: 520px; color: {FG}; }}
</style></head><body>
{"".join(pages)}
</body></html>'''

page = os.path.join(TMP, "portfolio.html")
open(page, "w", encoding="utf-8").write(html)
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                f"--print-to-pdf={OUT}", "file://" + page], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("PDF ok:", OUT, f"{os.path.getsize(OUT) / 1e6:.1f} MB,", len(pages), "páginas")
