# -*- coding: utf-8 -*-
"""Gera o site estático em /site. Uso: python3 tools/build.py"""
import os, sys, json, colorsys, re
from html import escape as e
sys.path.insert(0, os.path.dirname(__file__))
from content import *  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
MAN = json.load(open(os.path.join(ROOT, "tools/manifest.json")))
SITE_URL = "https://lirukkkkk.github.io/portfolio"
GA_ID = ""     # ex.: G-XXXXXXX
I18N = {k: v["en"] for k, v in T.items()}
CASES = sorted(CASES, key=lambda c: ORDER.index(c["slug"]))
BY = {c["slug"]: c for c in CASES}

ICON = {
    "arr": '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "ne": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.2A9.7 9.7 0 0 0 3.7 16.9L2.3 21.8l5-1.3A9.7 9.7 0 1 0 12 2.2Zm0 17.7a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 19.9Zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8 1c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.8 3 .6a2.5 2.5 0 0 0 1.7-1.2 2 2 0 0 0 .1-1.2c0-.1-.2-.2-.4-.3Z"/></svg>',
    "moon": '<svg class="theme-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z"/></svg>',
    "sun": '<svg class="theme-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    "l": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>',
    "r": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>',
    "x": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    "share": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 15V3.5M7.5 8 12 3.5 16.5 8"/><path d="M5 12.5v5.5a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-5.5"/></svg>',
    "down": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3.5V15M7.5 10.5 12 15l4.5-4.5"/><path d="M5 12.5v5.5a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-5.5"/></svg>',
    "link": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1 1"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1-1"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="m4 7 8 6 8-6"/></svg>',
    "snd": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 9h4l5-4v14l-5-4H4zM16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/></svg>',
}


def tx(key, tag="span", cls="", attrs=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-i18n="{key}"{attrs}>{e(T[key]["pt"])}</{tag}>'


def lt(key, d):
    """Texto bilíngue de conteúdo (registra EN no dicionário)."""
    I18N[key] = d["en"]
    return e(d["pt"])


def pic(src, pre, sizes="100vw", alt="", eager=False, cls="", zoom=False, cap=""):
    m = MAN[src]
    base = pre + m["base"]
    W, H = m["ratio"]
    ws = m["w"]
    srcset = lambda ext: ", ".join(f"{base}-{w}.{ext} {w}w" for w in ws)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    z = f' data-zoom data-cap="{e(cap)}" tabindex="0" role="button"' if zoom else ""
    zc = " zoomable" if zoom else ""
    return (f'<picture class="media{zc} {cls}"{z} style="aspect-ratio:{W}/{H}">'
            f'<source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">'
            f'<img src="{base}-{ws[-1]}.webp" width="{W}" height="{H}" alt="{e(alt)}" {load} decoding="async"></picture>')


def palette(kit_items):
    score = {}
    for it in kit_items:
        for rank, c in enumerate(MAN[it]["colors"]):
            score[c] = score.get(c, 0) + (6 - rank)
    def rgb(c): return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
    def hsv(c): return colorsys.rgb_to_hsv(*(v / 255 for v in rgb(c)))
    def dist(a, b): return sum((x - y) ** 2 for x, y in zip(rgb(a), rgb(b))) ** 0.5
    def skin(c):
        h_, s_, v_ = hsv(c)
        return 0.02 < h_ < 0.11 and s_ < 0.75   # tons de pele/madeira das fotos
    vivid = sorted([c for c in score if hsv(c)[1] > 0.35 and hsv(c)[2] > 0.3 and not skin(c)], key=lambda c: -score[c] * (0.3 + hsv(c)[1]))
    picked = []
    for c in vivid:
        if all(dist(c, p) > 80 for p in picked):
            picked.append(c)
        if len(picked) == 2:
            break
    rest = sorted(score, key=lambda c: -score[c])
    light = [c for c in rest if hsv(c)[2] > 0.82 and hsv(c)[1] < 0.25]
    if light:
        picked.append(light[0])
    for c in rest:
        if len(picked) >= 3:
            break
        if all(dist(c, p) > 60 for p in picked):
            picked.append(c)
    return picked[:3]


_SVG = open(os.path.join(ROOT, "Icons Alan/Stiker 3.svg"), encoding="utf-8").read()
_PATHS = re.findall(r'<path d="([^"]+)"', _SVG)
_FRECKLES = "".join(f'<path d="{d}"/>' for d in _PATHS[:-1])
_FACE = _PATHS[-1]


def avatar(uid, pre):
    return f'''<div class="avatar" data-sticker role="img" aria-label="Autorretrato ilustrado de Alan Veloso">
<svg viewBox="0 0 961 881" aria-hidden="true" fill="currentColor"><path class="face" d="{_FACE}"/><g class="frk">{_FRECKLES}</g></svg>
</div>'''


def ver(rel):
    import hashlib
    return hashlib.md5(open(os.path.join(SITE, rel), "rb").read()).hexdigest()[:8]


def head(title, desc, pre, css, canonical=""):
    ga = ""
    if GA_ID:
        ga = f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}");</script>'
    og = (f"{SITE_URL}/assets/og.jpg" if SITE_URL else f"{pre}assets/og.jpg") + f"?v={ver('assets/og.jpg')}"
    links = "".join(f'<link rel="stylesheet" href="{pre}assets/css/{c}.css?v={ver("assets/css/" + c + ".css")}">' for c in css)
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#121211">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="Alan Veloso">
<meta name="twitter:image" content="{og}">
<meta property="og:locale" content="pt_BR">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pre}assets/avatar/favicon.svg" type="image/svg+xml"><link rel="icon" href="{pre}assets/avatar/favicon.png" type="image/png" sizes="180x180"><link rel="apple-touch-icon" href="{pre}assets/avatar/favicon.png">
<link rel="preload" href="{pre}assets/fonts/host-grotesk-latin.woff2" as="font" type="font/woff2" crossorigin>
<script>try{{var t=localStorage.getItem("theme")||"dark";document.documentElement.dataset.theme=t;var l=localStorage.getItem("lang");if(l==="en")document.documentElement.lang="en"}}catch(e){{}}</script>
{links}
{ga}
</head>'''


def header(pre, home):
    home = home or "./"
    nav = [("nav.work", "trabalhos"), ("nav.ads", "trafego"), ("nav.services", "servicos"), ("nav.about", "sobre"), ("nav.contact", "contato")]
    links = "".join(f'<a href="{home}#{a}" >{tx(k)}</a>' for k, a in nav[:3])
    links += f'<a href="{home}planos.html">{tx("nav.plans")}</a>'
    links += "".join(f'<a href="{home}#{a}" >{tx(k)}</a>' for k, a in nav[3:])
    return f'''<a class="skip" href="#main" data-i18n="skip">{T["skip"]["pt"]}</a>
<header class="top"><div class="wrap">
<a class="brand" href="{home}">Alan Veloso</a>
<nav class="nav" aria-label="Principal">{links}</nav>
<div class="tools">
<a class="nav-m" href="{home}planos.html">{tx("nav.plans")}</a>
<button class="icon-btn" type="button" data-lang-toggle aria-label="{T["lang"]["pt"]}" data-i18n-attr="aria-label:lang">EN</button>
<button class="icon-btn" type="button" data-theme-toggle aria-label="{T["theme"]["pt"]}" data-i18n-attr="aria-label:theme">{ICON["moon"]}{ICON["sun"]}</button>
</div></div></header>'''


def footer(pre):
    return f'''<footer class="foot"><div class="wrap">
<span>© 2026 Alan Veloso · {tx("footer")}</span>
<div class="foot-act">
<a class="icon-btn foot-btn" href="{pre}assets/portfolio-alan-veloso.pdf" download="Portfolio Alan Veloso.pdf" aria-label="{T["pdf.download"]["pt"]}" data-i18n-attr="aria-label:pdf.download" title="{T["pdf.download"]["pt"]}">{ICON["down"]}</a>
<div class="share">
<button class="icon-btn foot-btn" type="button" data-share aria-haspopup="true" aria-expanded="false" aria-label="{T["share"]["pt"]}" data-i18n-attr="aria-label:share" title="{T["share"]["pt"]}">{ICON["share"]}</button>
<div class="share-pop" role="menu" hidden>
<button type="button" role="menuitem" data-share-copy>{ICON["link"]}{tx("share.copy")}</button>
<a role="menuitem" data-share-whats href="#" target="_blank" rel="noopener">{ICON["wa"]}{tx("share.whats")}</a>
<a role="menuitem" data-share-mail href="#">{ICON["mail"]}{tx("share.email")}</a>
</div>
</div>
</div>
<span><a href="{INSTAGRAM}" rel="noopener" target="_blank">Instagram</a> · <a href="{BEHANCE}" rel="noopener" target="_blank">Behance</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
</div></footer>
<dialog class="lb" aria-label="Imagem ampliada">
<div class="lb-bar"><span class="lb-cap"></span><button class="icon-btn" type="button" data-lb-close aria-label="{T["close"]["pt"]}" data-i18n-attr="aria-label:close">{ICON["x"]}</button></div>
<div class="lb-stage"><button class="icon-btn" type="button" data-lb-prev aria-label="{T["prev"]["pt"]}" data-i18n-attr="aria-label:prev">{ICON["l"]}</button><div class="lb-pic"></div><button class="icon-btn" type="button" data-lb-next aria-label="{T["next"]["pt"]}" data-i18n-attr="aria-label:next">{ICON["r"]}</button></div>
</dialog>
<script src="{pre}assets/js/i18n.js"></script>
<script src="{pre}assets/js/site.js?v={ver("assets/js/site.js")}" defer></script>
</body></html>'''


def wa_link(text_pt="Oi, Alan! Vi seu portfólio e queria conversar sobre um projeto."):
    from urllib.parse import quote
    return f"https://wa.me/{WHATSAPP}?text={quote(text_pt)}"


def cta_whats(cls="btn"):
    return f'<a class="{cls}" href="{wa_link()}" target="_blank" rel="noopener">{ICON["wa"]}{tx("cta.whats")}</a>'


def client_name(c):
    if c.get("client_en"):
        I18N[f"client.{c['slug']}"] = c["client_en"]
        return f'<span data-i18n="client.{c["slug"]}">{e(c["client"])}</span>'
    return e(c["client"])


def seg_name(seg):
    I18N[f"seg.{seg}"] = SEGMENTS[seg]["en"]
    return f'<span data-i18n="seg.{seg}">{e(SEGMENTS[seg]["pt"])}</span>'


def cat_name(k):
    I18N[f"cat.{k}"] = CATS[k]["en"]
    return f'<span data-i18n="cat.{k}">{e(CATS[k]["pt"])}</span>'


def cat_chips(target):
    chips = f'<button class="chip" type="button" data-seg="all" aria-pressed="true">{tx("archive.all")}</button>'
    for k in CATS:
        chips += f'<button class="chip" type="button" data-seg="{k}" aria-pressed="false">{cat_name(k)}</button>'
    return f'<div class="filters" data-filter="{target}" role="group" aria-label="Filtrar por categoria">{chips}</div>'


def tags(c):
    return " ".join(c.get("tags", []))


# ---------- shared home sections ----------

def sec_services():
    items = ""
    for i, (h, p) in enumerate(SERVICES):
        items += f'<li class="rv"><h3>{f"<span data-i18n=svc.h{i}>"}{lt(f"svc.h{i}", h)}</span></h3><p data-i18n="svc.p{i}">{lt(f"svc.p{i}", p)}</p></li>'
    return f'''<section class="sec" id="servicos" aria-labelledby="h-svc"><div class="wrap">
<div class="sec-head"><h2 class="sec-title rv" id="h-svc">{tx("services.title", "span")}</h2><div class="sec-note rv"><p>{tx("services.note", "span")}</p><a class="link-arr" href="planos.html">{tx("plans.see")}{ICON["arr"]}</a></div></div>
<ol class="svc">{items}</ol></div></section>'''


def sec_process():
    items = ""
    for i, (h, p) in enumerate(PROCESS):
        items += f'<li class="rv" style="--d:{i*70}ms"><span class="n">{i+1:02d}</span><h3 data-i18n="pr.h{i}">{lt(f"pr.h{i}", h)}</h3><p data-i18n="pr.p{i}">{lt(f"pr.p{i}", p)}</p></li>'
    return f'''<section class="sec" aria-labelledby="h-pr"><div class="wrap">
<div class="sec-head"><h2 class="sec-title rv" id="h-pr">{tx("process.title", "span")}</h2></div>
<ol class="steps">{items}</ol></div></section>'''


def sec_palettes(pre):
    kit = BY["kits-odonto"]
    cards = ""
    for g in kit["groups"]:
        cols = palette(g["items"])
        chips = "".join(f'<span style="background:{c}"></span>' for c in cols)
        I18N[f"kit.{g['slug']}"] = g["label"]["en"]
        cards += (f'<a class="pal rv" href="#kit-{g["slug"]}"><div class="pal-chips">{chips}</div>'
                  f'<div class="pal-name"><span data-i18n="kit.{g["slug"]}">{e(g["label"]["pt"])}</span><span>{len(g["items"]):02d}</span></div></a>')
    return f'''<section class="group pal-block" aria-labelledby="h-pal">
<div class="group-head"><h2 id="h-pal">{tx("palettes.title", "span")}</h2><span>{tx("palettes.text", "span")}</span></div>
<div class="pals">{cards}</div></section>'''


# (case, índice da peça contando todas as imagens do case)
ARCHIVE = [
    ("trafego-pago", 1), ("pod-mais", 3), ("inovorto", 0), ("trafego-pago", 15), ("pod-mais", 9),
    ("next-step", 11), ("terra-a-vista", 3), ("brenda-seda", 0), ("ilustracao", 0), ("breno-lima", 0), ("cr1a-grime", 0),
    ("kits-odonto", 9), ("jennifer-perez", 0), ("ruido", 0), ("raggaclubberz", 0), ("sucateiro", 1), ("cop", 0),
    ("ilustracao", 3), ("next-step", 2), ("cr1a-grime", 3), ("breno-lima", 23), ("terra-a-vista", 4), ("kits-odonto", 24),
    ("dj-liru", 0), ("ruido", 2), ("brenda-seda", 3), ("jennifer-perez", 4), ("ilustracao", 1), ("cr1a-grime", 5),
    ("breno-lima", 8), ("sucateiro", 3), ("kits-odonto", 39), ("ruido", 4),
]


def sec_archive(pre):
    items = ""
    for slug, gi in ARCHIVE:
        c = BY[slug]
        flat = [it for x in c["groups"] if x["kind"] != "video" for it in x["items"]]
        src = flat[gi % len(flat)]
        items += (f'<a href="{pre}trabalhos/{slug}.html" data-tags="{tags(c)}"><figure>{pic(src, pre, "(max-width:600px) 50vw, 25vw", alt=c["client"])}'
                  f'<figcaption><span>{client_name(c)}</span><span>{seg_name(c["segment"])}</span></figcaption></figure></a>')
    return f'''<section class="sec" id="arquivo" aria-labelledby="h-arc"><div class="wrap">
<div class="sec-head"><h2 class="sec-title rv" id="h-arc">{tx("archive.title", "span")}</h2>{cat_chips("#arch")}</div>
<div class="arch" id="arch">{items}</div></div></section>'''


def sec_about(pre, uid="a"):
    return f'''<section class="sec" id="sobre" aria-labelledby="h-ab"><div class="wrap about">
<div class="rv">{avatar(uid, pre)}</div>
<div class="about-copy"><h2 class="visually-hidden" id="h-ab">{tx("about.title", "span")}</h2><p class="pill rv">{tx("about.hi", "span")}</p>{tx("about.p1", "p", "rv about-lead")}{tx("about.p2", "p", "rv")}<hr class="about-rule rv"></div>
</div></section>'''


def sec_contact():
    opts = "".join(f'<option value="{k}" data-i18n="opt.{k}">{e(T["opt." + k]["pt"])}</option>' for k in ["monthly", "ads", "identity", "pieces", "motion", "agency", "other"])
    return f'''<section class="sec contact" id="contato" aria-labelledby="h-ct"><div class="wrap contact-grid">
<div>
{star_svg("estrela-2", "dm-contact")}
<h2 class="contact-big rv" id="h-ct">{tx("contact.title", "span")}</h2>
<p class="contact-lede rv">{tx("contact.text", "span")}</p>
<div class="btn-row rv" style="margin-top:28px">{cta_whats()}</div>
<ul class="contact-links rv">
<li><a href="mailto:{EMAIL}"><span>E-mail</span><span>{EMAIL}</span></a></li>
<li><a href="{wa_link()}" target="_blank" rel="noopener"><span>WhatsApp</span><span>+55 11 96574-6636</span></a></li>
<li><a href="{INSTAGRAM}" target="_blank" rel="noopener"><span>Instagram</span><span>@lirukkkkk</span></a></li>
<li><a href="{BEHANCE}" target="_blank" rel="noopener"><span>Behance</span><span>alanllacer8389</span></a></li>
</ul>
</div>
<form class="form rv" data-brief data-whats="{WHATSAPP}" data-email="{EMAIL}" novalidate>
<h3 class="full" style="grid-column:1/-1;font-size:26px;font-weight:500" data-i18n="cta.brief">{T["cta.brief"]["pt"]}</h3>
<div class="field"><label for="f-name">{tx("form.name")}</label><input id="f-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="f-company">{tx("form.company")}</label><input id="f-company" name="company" autocomplete="organization"></div>
<div class="field"><label for="f-service">{tx("form.service")}</label><select id="f-service" name="service" required><option value="" data-i18n="opt.choose">{T["opt.choose"]["pt"]}</option>{opts}</select></div>
<div class="field"><label for="f-seg">{tx("form.segment")}</label><input id="f-seg" name="segment"></div>
<div class="field"><label for="f-deadline">{tx("form.deadline")}</label><input id="f-deadline" name="deadline"></div>
<div class="field"><label for="f-refs">{tx("form.refs")}</label><input id="f-refs" name="refs" inputmode="url"></div>
<div class="field full"><label for="f-msg">{tx("form.msg")}</label><textarea id="f-msg" name="msg" rows="4"></textarea></div>
<p class="form-msg" role="status" aria-live="polite"></p>
<div class="form-foot"><button class="btn" type="submit" name="via" value="whats">{ICON["wa"]}{tx("form.send.whats")}</button><button class="btn ghost" type="submit" name="via" value="mail">{tx("form.send.mail")}</button></div>
<p class="form-msg" style="margin-top:-6px">{tx("form.hint", "span")}</p>
</form>
</div></section>'''


def deliver_line(c):
    I18N[f"dl.{c['slug']}"] = " · ".join(c["deliver"]["en"])
    return f'<span data-i18n="dl.{c["slug"]}">{e(" · ".join(c["deliver"]["pt"]))}</span>'


# ---------- Homes ----------

# Nome em lettering (Desirable Brush), montado como no layout do Alan.
# Posições de cada palavra dentro do quadro 1118x792 (x, y = canto do SVG original).
NAME_BOX = (1118, 792)
NAME_POS = {"Alan": (60, 95), "Veloso": (150, 365)}


def script_name():
    W, H = NAME_BOX
    defs, words = "", ""
    for i, word in enumerate(("Alan", "Veloso")):
        svg = open(os.path.join(ROOT, f"tools/nome/{word}.svg"), encoding="utf-8").read()
        d = re.search(r'<path d="([^"]+)"', svg).group(1)
        vw, vh = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups())
        x, y = NAME_POS[word]
        # máscara: faixa longa com borda suave na frente, que corre da esquerda para a direita (efeito de escrita).
        # A faixa é bem mais larga que o desenho, então ao fim ela cobre tudo (inclusive floreios que saem do quadro).
        BAND, FEATHER = 4000, 140
        start = x - 260               # frente da faixa começa antes do floreio mais à esquerda
        end = x + vw + 260            # e termina depois do último traço
        defs += (f'<linearGradient id="nw-g{i}" x1="0" x2="1" y1="0" y2="0">'
                 f'<stop offset="0" stop-color="#fff"/><stop offset="{1 - FEATHER / BAND:.4f}" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
                 f'<mask id="nw-m{i}" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="{W + 4000}" height="{H + 4000}">'
                 f'<rect class="nw-wipe nw-w{i}" x="{start - BAND}" y="-2000" width="{BAND}" height="{H + 4000}" fill="url(#nw-g{i})" style="--dx:{end - start:.0f}px"/></mask>')
        words += f'<g mask="url(#nw-m{i})"><path class="nw-p nw-p{i}" transform="translate({x} {y})" d="{d}"/></g>'
    return (f'<svg class="nw" viewBox="0 0 {W} {H}" aria-hidden="true" focusable="false">'
            f'<defs>{defs}</defs>{words}</svg>')


def split_name():
    out, k = "", 0
    for word in ("Alan", "Veloso"):
        chars = ""
        for ch in word:
            chars += f'<span class="ch" style="--i:{k}">{ch}</span>'
            k += 1
        out += f'<span class="ln" aria-hidden="true">{chars}</span>'
    return out


def star_svg(name, cls):
    """Estrelas pontilhadas desenhadas pelo Alan (tools/estrelas). Cor = currentColor, sem animação."""
    svg = open(os.path.join(ROOT, f"tools/estrelas/{name}.svg"), encoding="utf-8").read()
    svg = re.sub(r'\s+fill="(?!none)[^"]*"', "", svg)
    svg = re.sub(r'<svg width="[^"]*" height="[^"]*"', f'<svg class="dm {cls}" aria-hidden="true" focusable="false"', svg, count=1)
    svg = svg.replace('fill="none" xmlns', 'fill="currentColor" xmlns', 1)
    return svg.strip()


def dot_sparkle(cls, n=41, seed=1, rays=0.58):
    """Brilho de 4 pontas feito de pontos (efeito dot matrix / bitmap pontilhado).
    n = pontos por lado; os pontos rareiam nas pontas para parecer pontilhado."""
    import random
    rnd = random.Random(seed)
    c = (n - 1) / 2
    groups = ["", "", ""]
    for yy in range(n):
        for xx in range(n):
            x, y = abs(xx - c) / c, abs(yy - c) / c
            v = x ** rays + y ** rays          # astroide: estrela de 4 pontas
            if v > 1:
                continue
            dens = 1 - v ** 1.4                # mais cheio no centro
            if rnd.random() > dens * 2.6 + 0.08:
                continue
            size = 0.78 if rnd.random() < 0.75 else 0.5
            groups[rnd.randrange(3)] += f'<rect x="{xx + (1 - size) / 2:.2f}" y="{yy + (1 - size) / 2:.2f}" width="{size}" height="{size}"/>'
    g = "".join(f'<g class="dm-g dm-g{i}">{d}</g>' for i, d in enumerate(groups))
    return f'<svg class="dm {cls}" viewBox="0 0 {n} {n}" aria-hidden="true" fill="currentColor" shape-rendering="crispEdges">{g}</svg>'


STAR = '<svg class="star" viewBox="0 0 100 100" aria-hidden="true"><path fill="currentColor" d="M50 0l7.6 31.6L85.4 14.6 68.4 42.4 100 50 68.4 57.6 85.4 85.4 57.6 68.4 50 100 42.4 68.4 14.6 85.4 31.6 57.6 0 50 31.6 42.4 14.6 14.6 42.4 31.6z"/></svg>'


def marquee():
    def one(hidden):
        out = ""
        for k in CATS:
            a = ' tabindex="-1" aria-hidden="true"' if hidden else ""
            out += f'<button type="button" class="mq-btn" data-cat="{k}"{a}>{cat_name(k)}</button><i aria-hidden="true">✦</i>'
        return out
    return (f'<nav class="mq" data-marquee aria-label="Categorias de trabalho"><div class="mq-track">'
            f'<div class="mq-set">{one(False)}</div><div class="mq-set" aria-hidden="true">{one(True)}</div><div class="mq-set" aria-hidden="true">{one(True)}</div></div></nav>')


def sec_ads(pre):
    c = BY["trafego-pago"]
    picks = [g["items"] for g in c["groups"]]
    flat = [picks[0][0], picks[0][1], picks[1][0], picks[2][0], picks[0][2], picks[4][0], picks[3][0], picks[0][3]]
    cards = "".join(f'<a class="ads-card" href="{pre}trabalhos/trafego-pago.html">{pic(it, pre, "(max-width:600px) 62vw, 280px", alt="Criativo de tráfego pago")}</a>' for it in flat)
    return f'''<section class="sec ads" id="trafego" aria-labelledby="h-ads"><div class="wrap">
<div class="sec-head"><h2 class="sec-title rv" id="h-ads">{tx("ads.title", "span")}</h2><div class="sec-note rv"><p>{tx("ads.text", "span")}</p><a class="link-arr" href="{pre}trabalhos/trafego-pago.html">{tx("ads.see")}{ICON["arr"]}</a></div></div>
</div><div class="ads-strip rv" tabindex="0" aria-label="Criativos para tráfego pago">{cards}</div></section>'''


def motion_videos(pre):
    from PIL import Image
    figs = ""
    for c in CASES:
        for gi, g in enumerate(c["groups"]):
            if g["kind"] != "video":
                continue
            key = f"vg.{c['slug']}.{gi}"
            lab = lt(key, g["label"])
            for v in g["items"]:
                w, h = Image.open(os.path.join(SITE, f"assets/video/{v}-poster.jpg")).size
                cls = ' class="wide"' if w > h else ""
                figs += (f'<figure{cls}><video controls playsinline preload="none" poster="{pre}assets/video/{v}-poster.jpg" aria-label="{e(c["client"])} - {e(g["label"]["pt"])}">'
                         f'<source src="{pre}assets/video/{v}.mp4" type="video/mp4"></video>'
                         f'<figcaption><a href="{pre}trabalhos/{c["slug"]}.html">{client_name(c)}</a><span data-i18n="{key}">{lab}</span></figcaption></figure>')
    return f'<div class="ix-vids" id="ix-vids" hidden><p class="ix-vids-note">{tx("work.videos", "span")}</p>{figs}</div>'


def home_v2(pre):
    rows = ""
    prev_imgs = ""
    for i, c in enumerate(CASES):
        rows += (f'<li class="rv" style="--d:{i*50}ms" data-tags="{tags(c)}"><a href="{pre}trabalhos/{c["slug"]}.html" data-preview-item="{c["slug"]}">'
                 f'<span class="ix-n">{i+1:02d}</span><span class="ix-c">{client_name(c)}</span>'
                 f'<span class="ix-s">{seg_name(c["segment"])}</span><span class="ix-d">{deliver_line(c)}</span>'
                 f'<span class="ix-t">{pic(c["cover"], pre, "120px", alt="")}</span><span class="ix-a">{ICON["ne"]}</span></a></li>')
        m = MAN[c["cover"]]
        prev_imgs += f'<img data-k="{c["slug"]}" src="{pre}{m["base"]}-{m["w"][0]}.webp" alt="" loading="lazy" decoding="async">'
    ph = MAN[PHOTOS[0]]
    photo = pic(PHOTOS[0], pre, "(max-width:860px) 100vw, 50vw", alt="Foto de Alan Veloso no centro de São Paulo", eager=True, cls="hero-photo")
    return f'''<main id="main">
<section class="hero" aria-label="Apresentação"><div class="wrap hero-grid">
<div class="hero-pic">{photo}</div>
{star_svg("estrela-1", "star st-burst")}{star_svg("estrela-2", "star st-cluster")}
<h1 class="hero-name script-name" aria-label="Alan Veloso">{script_name()}</h1>
<div class="hero-copy rv" style="--d:300ms">
<p class="hero-role">{tx("role", "span")}</p>
<p class="hero-tag">{tx("tagline", "span")}</p>
<div class="btn-row">{cta_whats("btn light")}<span class="avail">{tx("available")}</span></div>
</div>
</div></section>
{sec_about(pre)}
{marquee()}
<section class="sec v2-work" id="trabalhos" aria-labelledby="h-work"><div class="wrap">
<div class="sec-head"><h2 class="sec-title rv" id="h-work">{tx("work.title", "span")}</h2>{cat_chips("#ix")}</div>
<ol class="ix" id="ix">{rows}</ol>
{motion_videos(pre)}
<p class="ix-empty" hidden>{tx("work.empty", "span")}</p>
</div><div class="ix-prev" data-preview aria-hidden="true">{prev_imgs}</div></section>
{sec_ads(pre)}{sec_services()}{sec_process()}{sec_contact()}
</main>'''


# ---------- Case pages ----------

def case_page(c, nxt):
    pre = "../"
    s = c["slug"]
    title = lt(f"ct.{s}", c["title"])
    intro = lt(f"ci.{s}", c["intro"])
    groups = ""
    for gi, g in enumerate(c["groups"]):
        lab = lt(f"cg.{s}.{gi}", g["label"])
        n = len(g["items"])
        if g["kind"] == "video":
            vids = "".join(
                f'<div class="vid"><video data-auto muted loop playsinline preload="none" poster="{pre}assets/video/{v}-poster.jpg" aria-label="{e(g["label"]["pt"])}"><source src="{pre}assets/video/{v}.mp4" type="video/mp4"></video>'
                f'<button class="icon-btn" type="button" data-sound aria-pressed="false" aria-label="{T["sound"]["pt"]}" data-i18n-attr="aria-label:sound">{ICON["snd"]}</button></div>'
                for v in g["items"])
            body = f'<div class="g-vid">{vids}</div>'
        elif g["kind"] in ("carousel", "kit"):
            slides = "".join(pic(it, pre, "(max-width:600px) 78vw, 420px", alt=f'{c["client"]} — {g["label"]["pt"]} {k+1}', zoom=True, cap=g["label"]["pt"]) for k, it in enumerate(g["items"]))
            body = (f'<div class="car" data-car data-zoom-group><div class="car-track" tabindex="0" aria-label="{e(g["label"]["pt"])}">{slides}</div>'
                    f'<div class="car-bar"><div class="car-meter"><i></i></div><span class="car-count tnum"></span>'
                    f'<div class="car-btns"><button class="icon-btn" type="button" aria-label="{T["prev"]["pt"]}" data-i18n-attr="aria-label:prev">{ICON["l"]}</button>'
                    f'<button class="icon-btn" type="button" aria-label="{T["next"]["pt"]}" data-i18n-attr="aria-label:next">{ICON["r"]}</button></div></div></div>')
        elif g["kind"] == "wide":
            body = '<div class="g-wide" data-zoom-group>' + "".join(pic(it, pre, "(max-width:720px) 100vw, 50vw" if k else "100vw", alt=f'{c["client"]} — {g["label"]["pt"]} {k+1}', zoom=True, cap=g["label"]["pt"]) for k, it in enumerate(g["items"])) + "</div>"
        else:
            body = '<div class="g-grid" data-zoom-group>' + "".join(pic(it, pre, "(max-width:720px) 50vw, 33vw", alt=f'{c["client"]} — {k+1}', zoom=True, cap=c["client"]) for k, it in enumerate(g["items"])) + "</div>"
        hid = f' id="kit-{g["slug"]}"' if g["kind"] == "kit" else ""
        dots = ""
        if g["kind"] == "kit":
            dots = '<span class="kit-dots" aria-hidden="true">' + "".join(f'<i style="background:{col}"></i>' for col in palette(g["items"])) + "</span>"
        unit = "slides" if g["kind"] in ("carousel", "kit") else None
        cnt = f'{n:02d} {tx(unit)}' if unit else f"{n:02d}"
        groups += f'<section class="group rv"{hid}><div class="group-head"><h2 class="kit-head">{dots}<span data-i18n="cg.{s}.{gi}">{lab}</span></h2><span>{cnt}</span></div>{body}</section>'
    credit = f'<p class="credit" data-i18n="credit.ns">{e(c["credit"]["pt"])}</p>' if c["credit"] else ""
    if c["credit"]:
        I18N["credit.ns"] = c["credit"]["en"]
    cover = f'<div class="case-banner rv">{pic(c["banner"], pre, "100vw", alt=c["client"], eager=True)}</div>' if c.get("banner") else ""
    body = f'''<body>
{header(pre, pre)}
<main id="main"><div class="wrap">
<section class="case-hero">
<p class="case-crumb"><a href="{pre}#trabalhos">{tx("case.back")}</a><span>/</span><span>{client_name(c)}</span></p>
<h1 class="case-title rv" data-i18n="ct.{s}">{title}</h1>
<dl class="case-meta rv"><div><dt>{tx("case.client")}</dt><dd>{client_name(c)}</dd></div><div><dt>{tx("case.segment")}</dt><dd>{seg_name(c["segment"])}</dd></div><div><dt>{tx("case.deliver")}</dt><dd>{deliver_line(c)}</dd></div></dl>
<div class="case-intro rv"><div>{credit}</div><p data-i18n="ci.{s}">{intro}</p></div>
{sec_palettes(pre) if s == "kits-odonto" else ""}
</section>
{cover}
{groups}
<div class="case-cta rv"><p>{tx("case.cta", "span")}</p><div class="btn-row">{cta_whats()}</div></div>
<a class="case-next" href="{nxt["slug"]}.html"><small>{tx("case.next")}</small><strong>{client_name(nxt)}{ICON["arr"]}</strong></a>
</div></main>
{footer(pre)}'''
    desc = c["intro"]["pt"][:155]
    return head(f'{c["client"]} — Alan Veloso', desc, pre, ["base"]) + body


def brl(v):
    return "R$ " + f"{v:,}".replace(",", ".")


def price_txt(key, v):
    if isinstance(v, dict):
        return f'<span data-i18n="{key}">{lt(key, v)}</span>'
    return f'<span>{brl(v)}</span>'


def plans_page():
    from urllib.parse import quote
    pre = ""
    # formas de contratar
    modes = ""
    for k, name, desc in MODES:
        modes += (f'<a class="mode-card rv" href="#{k}"><strong data-i18n="md.{k}">{lt(f"md.{k}", name)}</strong>'
                  f'<span data-i18n="md.d.{k}">{lt(f"md.d.{k}", desc)}</span>{ICON["arr"]}</a>')
    # planos
    cols = ""
    labels = [("static", "pl.static1", "pl.static"), ("carousel", "pl.carousel1", "pl.carousel"), ("stories", "pl.stories", "pl.stories"),
              ("reels", "pl.reels1", "pl.reels1"), ("ads", "pl.ads", "pl.ads")]
    for p_ in PLANS:
        k = p_["key"]; g = p_["grid"]
        I18N[f"plan.{k}"] = p_["name"]["en"]; I18N[f"plan.for.{k}"] = p_["for"]["en"]
        li = ""
        for key, one, many in labels:
            n = g[key]
            if n:
                li += f'<li><strong class="tnum">{n}</strong> {tx(one if n == 1 else many)}</li>'
        if g["plan"]:
            li += f'<li><strong>{tx("pl.planning")}</strong></li>'
        wa = f"https://wa.me/{WHATSAPP}?text=" + quote(f"Oi, Alan! Tenho interesse no plano {p_['name']['pt']} ({brl(p_['price'])}/mês).")
        cols += f'''<article class="plan rv">
<h3 class="plan-name" data-i18n="plan.{k}">{e(p_["name"]["pt"])}</h3>
<p class="plan-price"><span class="tnum">{brl(p_["price"])}</span><small>{tx("plans.month")}</small></p>
<p class="plan-for" data-i18n="plan.for.{k}">{e(p_["for"]["pt"])}</p>
<ul class="plan-list">{li}</ul>
<p class="plan-save"><span>{tx("plans.single")} <s class="tnum">{brl(p_["single"])}</s></span><span class="plan-off tnum">{p_["off"]}% {tx("plans.off")}</span></p>
<a class="btn" href="{wa}" target="_blank" rel="noopener">{ICON["wa"]}{tx("plans.cta")}</a>
</article>'''
    rules = "".join(f'<li data-i18n="rule.{i}">{lt(f"rule.{i}", r)}</li>' for i, r in enumerate(PLAN_RULES))
    heads = ["pl.plan", "pl.h.static", "pl.h.carousel", "pl.h.stories", "pl.h.reels", "pl.h.ads", "pl.h.plan", "pl.h.single", "pl.h.off", "pl.h.month"]
    th = "".join(f'<th scope="col">{tx(h)}</th>' for h in heads)
    rows = ""
    dash = '<span class="mute">—</span>'
    for p_ in PLANS:
        g = p_["grid"]
        cell = lambda n: f'<td class="tnum">{n}</td>' if n else f"<td>{dash}</td>"
        rows += (f'<tr><th scope="row" data-i18n="plan.{p_["key"]}">{e(p_["name"]["pt"])}</th>{cell(g["static"])}{cell(g["carousel"])}{cell(g["stories"])}{cell(g["reels"])}{cell(g["ads"])}'
                 f'<td>{tx("pl.yes") if g["plan"] else dash}</td><td class="tnum mute">{brl(p_["single"])}</td><td class="tnum">{p_["off"]}%</td><td class="tnum"><strong>{brl(p_["price"])}</strong></td></tr>')
    # tabela avulsa
    cat = ""
    for gi, (gname, items) in enumerate(CATALOG):
        lis = ""
        for ii, (name, note, price) in enumerate(items):
            key = f"ct.{gi}.{ii}"
            pid = "projetos" if gi == len(CATALOG) - 1 and ii == 0 else ""
            lis += (f'<li><span><span data-i18n="{key}">{lt(key, name)}</span><span class="mute" data-i18n="{key}.n">{lt(key + ".n", note)}</span></span>'
                    f'<span class="tnum">{price_txt(key + ".p", price)}</span></li>')
        gid = ' id="projetos"' if gi == len(CATALOG) - 1 else ""
        cat += f'<div class="cat-group"{gid}><h3 data-i18n="cg.{gi}">{lt(f"cg.{gi}", gname)}</h3><ul class="singles">{lis}</ul></div>'
    body = f'''<body>
{header(pre, "./")}
<main id="main"><div class="wrap">
<section class="case-hero">
<h1 class="case-title rv">{tx("plans.title", "span")}</h1>
<p class="plans-lede rv">{tx("plans.lede", "span")}</p>
</section>
<nav class="modes" aria-label="{T["plans.how"]["pt"]}">{modes}</nav>

<section class="group rv" id="planos" aria-labelledby="h-pl"><div class="group-head"><h2 id="h-pl">{tx("plans.monthly", "span")}</h2><span>{tx("plans.monthly.note", "span")}</span></div>
<div class="plans">{cols}</div>
<div class="rules"><h3>{tx("plans.rules", "span")}</h3><ul>{rules}</ul></div>
<div class="table-wrap" tabindex="0"><table class="cmp"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>
<p class="plans-foot">{tx("plans.foot", "span")}</p></section>

<section class="group rv" id="avulso" aria-labelledby="h-sg"><div class="group-head"><h2 id="h-sg">{tx("plans.singles", "span")}</h2><span>{tx("plans.singles.note", "span")}</span></div>
{cat}</section>

<div class="case-cta rv"><p>{tx("plans.custom", "span")}</p><div class="btn-row"><a class="btn" href="./#contato">{tx("plans.custom.cta")}{ICON["arr"]}</a></div></div>
</div></main>
<div style="height:clamp(56px,8vw,112px)"></div>
{footer(pre)}'''
    return head("Planos e valores — Alan Veloso", "Planos mensais e tabela avulsa: social media, criativos para tráfego pago, peças gráficas, documentos e projetos de identidade visual.", pre, ["base"]) + body


def write(path, html):
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(html)


DESC = "Alan Veloso, designer em São Paulo. Social media, criativos para tráfego pago, identidade visual e motion para marcas e agências."

page = head("Alan Veloso — Social media e branding", DESC, "", ["base", "home"]) + "<body>" + header("", "./") + home_v2("") + footer("")
write("index.html", page)
write("planos.html", plans_page())


for i, c in enumerate(CASES):
    write(f"trabalhos/{c['slug']}.html", case_page(c, CASES[(i + 1) % len(CASES)]))

open(os.path.join(SITE, "assets/js/i18n.js"), "w", encoding="utf-8").write("window.I18N=" + json.dumps(I18N, ensure_ascii=False) + ";")

print("ok", len(I18N), "strings EN")
