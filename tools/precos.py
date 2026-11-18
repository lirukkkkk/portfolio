# -*- coding: utf-8 -*-
"""Tabela de preços em PDF (privada, para mandar ao cliente). Mesmo visual do site e do portfólio em PDF.
Saída: Documentos/Tabela de precos Alan Veloso.pdf (fora do site e fora do GitHub).
Uso: python3 tools/precos.py  (precisa do Google Chrome)"""
import os, sys, subprocess
from html import escape as e

sys.path.insert(0, os.path.dirname(__file__))
from content import CATALOG, PLANS, PLAN_RULES, MODES, WHATSAPP, EMAIL, INSTAGRAM  # noqa: E402
from build import script_name, star_svg, SITE_URL  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "Documentos")
os.makedirs(OUTDIR, exist_ok=True)
OUT = os.path.join(OUTDIR, "Tabela de precos Alan Veloso.pdf")
TMP = os.path.join(ROOT, "tools/_render/precos.html")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
VALIDADE = "Valores válidos até maio de 2027"


def brl(v):
    return "R$ " + f"{v:,}".replace(",", ".")


def price(v):
    return e(v["pt"]) if isinstance(v, dict) else brl(v)


def items_of(g):
    out = []
    for key, one, many in (("static", "estático", "estáticos"), ("carousel", "carrossel", "carrosséis"), ("stories", "stories", "stories"),
                           ("reels", "reels", "reels"), ("ads", "criativo de tráfego", "criativos de tráfego")):
        n = g[key]
        if n:
            out.append(f'<li><strong>{n}</strong> {one if n == 1 else many}</li>')
    if g["plan"]:
        out.append("<li><strong>Planejamento do mês</strong></li>")
    return "".join(out)


def catalog_block(groups):
    html = ""
    for gname, items in groups:
        lis = "".join(f'<li><span><b>{e(n["pt"])}</b><small>{e(nt["pt"])}</small></span><span class="p">{price(p)}</span></li>' for n, nt, p in items)
        html += f'<div class="cat"><h3>{e(gname["pt"])}</h3><ul>{lis}</ul></div>'
    return html


pages = []
# 1. capa
pages.append(f'''<section class="pg cover">
<div class="name">{script_name()}</div>
{star_svg("estrela-2", "st a")}{star_svg("estrela-1", "st b")}
<div class="meta"><h1>Planos e valores</h1><p>Social media, tráfego pago, peças gráficas e branding</p><small>{VALIDADE}</small></div>
</section>''')

# 2. formas de contratar + planos
modes = "".join(f'<div class="mode"><b>{e(n["pt"])}</b><span>{e(d["pt"])}</span></div>' for k, n, d in MODES)
cards = ""
for p in PLANS:
    cards += f'''<article class="plan"><h3>{e(p["name"]["pt"])}</h3>
<p class="price">{brl(p["price"])}<small>/mês</small></p>
<p class="for">{e(p["for"]["pt"])}</p>
<ul>{items_of(p["grid"])}</ul>
<p class="save"><span>Valor avulso <s>{brl(p["single"])}</s></span><span class="off">{p["off"]}% de economia</span></p></article>'''
pages.append(f'''<section class="pg plans">
<p class="eyebrow">Formas de contratar</p>
<div class="modes">{modes}</div>
<p class="eyebrow" style="margin-top:44px">Planos mensais · para quem posta toda semana</p>
<div class="cards">{cards}</div>
</section>''')

# 3. regras + comparativo
rules = "".join(f"<li>{e(r['pt'])}</li>" for r in PLAN_RULES)
dash = '<span class="mute">—</span>'
rows = ""
for p in PLANS:
    g = p["grid"]
    c = lambda n: f"<td>{n}</td>" if n else f"<td>{dash}</td>"
    rows += (f'<tr><th>{e(p["name"]["pt"])}</th>{c(g["static"])}{c(g["carousel"])}{c(g["stories"])}{c(g["reels"])}{c(g["ads"])}'
             f'<td>{"Sim" if g["plan"] else dash}</td><td class="mute">{brl(p["single"])}</td><td>{p["off"]}%</td><td><strong>{brl(p["price"])}</strong></td></tr>')
pages.append(f'''<section class="pg rules">
<h2>Como funcionam os planos</h2>
<ul class="rl">{rules}</ul>
<table class="cmp"><thead><tr><th>Plano</th><th>Estáticos</th><th>Carrosséis</th><th>Stories</th><th>Reels</th><th>Criativos de tráfego</th><th>Planejamento</th><th>Avulso</th><th>Desconto</th><th>Valor/mês</th></tr></thead>
<tbody>{rows}</tbody></table>
<p class="foot-note">Desconto calculado sobre os valores da tabela avulsa.</p>
</section>''')

# 4 e 5. tabela avulsa (2 grupos por página)
for i, (title, groups) in enumerate([("Tabela avulsa", CATALOG[:2]), ("Tabela avulsa", CATALOG[2:])]):
    pages.append(f'''<section class="pg catalog">
<div class="head"><h2>{title}</h2><span>Inclui 1 rodada de ajuste. Ajustes extras: R$ 35 por hora.</span></div>
<div class="cols">{catalog_block(groups)}</div>
</section>''')

# 6. contato
site = SITE_URL + "/"
pages.append(f'''<section class="pg contact">
{star_svg("estrela-2", "st c")}
<h2>Vamos fechar?</h2>
<p class="lede">Cada orçamento é ajustado ao seu projeto. Me chama e a gente define o melhor formato.</p>
<ul>
<li><span>WhatsApp</span><a href="https://wa.me/{WHATSAPP}">+55 11 96574-6636</a></li>
<li><span>E-mail</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><span>Instagram</span><a href="{INSTAGRAM}">@lirukkkkk</a></li>
<li><span>Portfólio</span><a href="{site}">{site.replace("https://", "")}</a></li>
</ul>
<p class="valid">{VALIDADE}. Projetos: 50% na entrada e 50% na entrega.</p>
<div class="sign">{script_name()}</div>
</section>''')

font = "file://" + os.path.join(ROOT, "site/assets/fonts/host-grotesk-latin.woff2")
BG, FG, FG2, MUTE, LINE, ACC, PANEL = "#121211", "#edece7", "#c9c8c2", "#9a9992", "#2d2d2b", "#8f97ff", "#1a1a19"
html = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>
@font-face {{ font-family: H; src: url("{font}"); }}
@page {{ size: 1600px 900px; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; background: {BG}; color: {FG}; font-family: H, Helvetica, Arial, sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; font-variant-numeric: tabular-nums; }}
.pg {{ width: 1600px; height: 900px; position: relative; overflow: hidden; page-break-after: always; break-after: page; padding: 80px 96px; }}
.pg:last-child {{ page-break-after: auto; }}
a {{ color: {FG}; text-decoration: none; }}
.mute {{ color: {MUTE}; }}
.nw-p {{ fill: currentColor; }} .nw-wipe, mask {{ display: none; }} g[mask] {{ mask: none; }}
.name svg, .sign svg {{ width: 100%; height: auto; display: block; overflow: visible; }}
.st {{ position: absolute; color: {FG}; height: auto; }}
.eyebrow {{ font-size: 15px; letter-spacing: .07em; text-transform: uppercase; color: {MUTE}; margin: 0 0 16px; }}
h2 {{ font-size: 56px; letter-spacing: -0.035em; font-weight: 500; line-height: 1; margin: 0 0 32px; }}
/* capa */
.cover .name {{ position: absolute; left: 70px; top: 60px; width: 860px; }}
.cover .st.a {{ right: 110px; top: 70px; width: 300px; opacity: .85; }}
.cover .st.b {{ left: 820px; top: 300px; width: 260px; color: {ACC}; opacity: .7; }}
.cover .meta {{ position: absolute; right: 100px; bottom: 90px; text-align: right; }}
.cover h1 {{ font-size: 96px; letter-spacing: -0.045em; font-weight: 500; line-height: .95; margin: 0 0 16px; }}
.cover .meta p {{ font-size: 26px; margin: 0 0 12px; color: {FG2}; }}
.cover .meta small {{ font-size: 18px; color: {MUTE}; text-transform: uppercase; letter-spacing: .05em; }}
/* formas + planos */
.modes {{ display: grid; grid-template-columns: repeat(3, 1fr); border-top: 1px solid {FG}; }}
.mode {{ padding: 18px 24px 0 0; display: flex; flex-direction: column; gap: 6px; }}
.mode + .mode {{ padding-left: 24px; border-left: 1px solid {LINE}; }}
.mode b {{ font-size: 24px; font-weight: 500; letter-spacing: -0.02em; }}
.mode span {{ font-size: 17px; color: {FG2}; line-height: 1.4; }}
.cards {{ display: grid; grid-template-columns: repeat(3, 1fr); border-top: 1px solid {FG}; }}
.plan {{ padding: 20px 28px 0 0; display: flex; flex-direction: column; gap: 10px; }}
.plan + .plan {{ padding-left: 28px; border-left: 1px solid {LINE}; }}
.plan h3 {{ margin: 0; font-size: 24px; font-weight: 600; }}
.price {{ margin: 0; font-size: 60px; font-weight: 600; letter-spacing: -0.035em; line-height: 1; }}
.price small {{ font-size: 20px; color: {MUTE}; font-weight: 400; margin-left: 6px; letter-spacing: 0; }}
.for {{ margin: 0; color: {FG2}; font-size: 17px; min-height: 48px; }}
.plan ul {{ list-style: none; margin: 0; padding: 12px 0 0; border-top: 1px solid {LINE}; display: grid; gap: 6px; font-size: 18px; min-height: 172px; align-content: start; }}
.plan strong {{ font-weight: 600; }}
.save {{ display: flex; justify-content: space-between; font-size: 15px; color: {MUTE}; padding-top: 12px; border-top: 1px solid {LINE}; margin: 0; }}
.off {{ color: {ACC}; font-weight: 600; }}
/* regras */
.rl {{ margin: 0 0 44px; padding: 4px 0 4px 26px; border-left: 2px solid {ACC}; font-size: 21px; line-height: 1.5; color: {FG2}; max-width: 1150px; list-style: none; display: grid; gap: 8px; }}
.cmp {{ width: 100%; border-collapse: collapse; font-size: 19px; }}
.cmp th, .cmp td {{ text-align: left; padding: 16px 12px 16px 0; border-bottom: 1px solid {LINE}; }}
.cmp thead th {{ font-size: 14px; font-weight: 500; color: {MUTE}; border-bottom-color: {FG}; text-transform: uppercase; letter-spacing: .04em; }}
.cmp tbody th {{ font-weight: 600; }}
.cmp td:last-child, .cmp th:last-child {{ text-align: right; padding-right: 0; }}
.foot-note {{ font-size: 15px; color: {MUTE}; margin-top: 14px; }}
/* tabela avulsa */
.catalog .head {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 28px; }}
.catalog .head h2 {{ margin: 0; }}
.catalog .head span {{ color: {MUTE}; font-size: 16px; }}
.cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 64px; }}
.cat h3 {{ font-size: 14px; font-weight: 500; letter-spacing: .07em; text-transform: uppercase; color: {ACC}; margin: 0; padding-bottom: 10px; border-bottom: 1px solid {FG}; }}
.cat ul {{ list-style: none; margin: 0; padding: 0; }}
.cat li {{ display: flex; justify-content: space-between; align-items: baseline; gap: 20px; padding: 12px 0; border-bottom: 1px solid {LINE}; }}
.cat li > span:first-child {{ display: flex; flex-direction: column; gap: 2px; }}
.cat b {{ font-weight: 500; font-size: 20px; letter-spacing: -0.01em; }}
.cat small {{ font-size: 14px; color: {MUTE}; }}
.cat .p {{ font-size: 20px; font-weight: 600; white-space: nowrap; }}
/* contato */
.contact h2 {{ font-size: 140px; line-height: .95; letter-spacing: -0.045em; margin: 50px 0 24px; }}
.contact .lede {{ font-size: 26px; color: {FG2}; margin: 0 0 40px; max-width: 760px; }}
.contact ul {{ list-style: none; margin: 0; padding: 0; width: 760px; border-top: 1px solid {FG}; }}
.contact li {{ display: flex; justify-content: space-between; padding: 16px 0; border-bottom: 1px solid {LINE}; font-size: 23px; }}
.contact li span {{ color: {MUTE}; }}
.contact .valid {{ font-size: 16px; color: {MUTE}; margin-top: 22px; }}
.contact .st.c {{ right: 120px; top: 80px; width: 300px; color: {ACC}; }}
.contact .sign {{ position: absolute; right: 90px; bottom: 50px; width: 480px; }}
</style></head><body>{"".join(pages)}</body></html>'''

open(TMP, "w", encoding="utf-8").write(html)
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                f"--print-to-pdf={OUT}", "file://" + TMP], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("ok:", OUT, f"{os.path.getsize(OUT) / 1e6:.1f} MB,", len(pages), "páginas")
