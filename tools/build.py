# -*- coding: utf-8 -*-
"""Gera o site estático em /site. Uso: python3 tools/build.py"""
import os, sys, json, colorsys
from html import escape as e
sys.path.insert(0, os.path.dirname(__file__))
from content import *  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
MAN = json.load(open(os.path.join(ROOT, "tools/manifest.json")))
SITE_URL = "https://lirukkkkk.github.io/portfolio"
GA_ID = ""     # ex.: G-XXXXXXX
I18N = {k: v["en"] for k, v in T.items()}
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
    vivid = sorted([c for c in score if hsv(c)[1] > 0.35 and hsv(c)[2] > 0.3], key=lambda c: -score[c] * (0.3 + hsv(c)[1]))
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


AV = json.load(open(os.path.join(ROOT, "tools/avatar.json")))


def avatar(uid, pre):
    pupils = "".join(f'<circle class="pupil" cx="{e_["cx"]}" cy="{e_["cy"]}" r="{e_["r"]}"/>' for e_ in AV)
    lids = ""
    for e_ in AV:
        x, y, w, h, st = e_["x"] - 6, e_["y"], e_["w"] + 12, e_["h"], e_["stroke"]
        lids += (f'<g class="lidg" style="--h:{round(h * 0.78)}px"><rect x="{x}" y="{y - h - 12}" width="{w}" height="{h + 12}" fill="#f2f1ed"/>'
                 f'<rect x="{x}" y="{y - st + 1}" width="{w}" height="{st - 2}" rx="{st/2}" fill="currentColor"/></g>')
    return f'''<div class="avatar" role="img" aria-label="Autorretrato ilustrado de Alan Veloso">
<div class="avatar-lines"></div>
<svg viewBox="150 150 900 900" aria-hidden="true">
<defs><mask id="em{uid}" maskUnits="userSpaceOnUse" x="150" y="150" width="900" height="900"><image href="{pre}assets/avatar/eyes-mask.png" x="150" y="150" width="900" height="900"/></mask></defs>
<g mask="url(#em{uid})">{pupils}{lids}</g>
</svg></div>'''


def head(title, desc, pre, css, canonical=""):
    ga = ""
    if GA_ID:
        ga = f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}");</script>'
    og = f"{SITE_URL}/assets/og.jpg" if SITE_URL else f"{pre}assets/og.jpg"
    links = "".join(f'<link rel="stylesheet" href="{pre}assets/css/{c}.css">' for c in css)
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#f2f1ed">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og}">
<meta property="og:locale" content="pt_BR">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pre}assets/avatar/favicon.png" type="image/png">
<link rel="preload" href="{pre}assets/fonts/host-grotesk-latin.woff2" as="font" type="font/woff2" crossorigin>
<script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t;var l=localStorage.getItem("lang");if(l==="en")document.documentElement.lang="en"}}catch(e){{}}</script>
{links}
{ga}
</head>'''


def header(pre, home):
    home = home or "./"
    nav = [("nav.work", "trabalhos"), ("nav.services", "servicos"), ("nav.about", "sobre"), ("nav.contact", "contato")]
    links = "".join(f'<a href="{home}#{a}" >{tx(k)}</a>' for k, a in nav[:2])
    links += f'<a href="{home}planos.html">{tx("nav.plans")}</a>'
    links += "".join(f'<a href="{home}#{a}" >{tx(k)}</a>' for k, a in nav[2:])
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
<span><a href="{INSTAGRAM}" rel="noopener" target="_blank">Instagram</a> · <a href="{BEHANCE}" rel="noopener" target="_blank">Behance</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
</div></footer>
<dialog class="lb" aria-label="Imagem ampliada">
<div class="lb-bar"><span class="lb-cap"></span><button class="icon-btn" type="button" data-lb-close aria-label="{T["close"]["pt"]}" data-i18n-attr="aria-label:close">{ICON["x"]}</button></div>
<div class="lb-stage"><button class="icon-btn" type="button" data-lb-prev aria-label="{T["prev"]["pt"]}" data-i18n-attr="aria-label:prev">{ICON["l"]}</button><div class="lb-pic"></div><button class="icon-btn" type="button" data-lb-next aria-label="{T["next"]["pt"]}" data-i18n-attr="aria-label:next">{ICON["r"]}</button></div>
</dialog>
<script src="{pre}assets/js/i18n.js"></script>
<script src="{pre}assets/js/site.js" defer></script>
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
        cards += (f'<a class="pal rv" href="{pre}trabalhos/kits-odonto.html#kit-{g["slug"]}"><div class="pal-chips">{chips}</div>'
                  f'<div class="pal-name"><span data-i18n="kit.{g["slug"]}">{e(g["label"]["pt"])}</span><span>{len(g["items"]):02d}</span></div></a>')
    return f'''<section class="sec" aria-labelledby="h-pal"><div class="wrap">
<div class="sec-head"><h2 class="sec-title rv" id="h-pal">{tx("palettes.title", "span")}</h2><p class="sec-note rv">{tx("palettes.text", "span")}</p></div>
<div class="pals">{cards}</div></div></section>'''


# (case, índice da peça contando todas as imagens do case)
ARCHIVE = [
    ("next-step", 11), ("brenda-seda", 0), ("breno-lima", 0), ("kits-odonto", 9), ("raggaclubberz", 0), ("cop", 0),
    ("next-step", 2), ("breno-lima", 23), ("kits-odonto", 24), ("brenda-seda", 3), ("raggaclubberz", 1), ("kits-odonto", 14),
    ("breno-lima", 8), ("cop", 3), ("next-step", 13), ("kits-odonto", 39), ("brenda-seda", 5), ("breno-lima", 12), ("raggaclubberz", 2), ("kits-odonto", 0),
]


def sec_archive(pre):
    items = ""
    for slug, gi in ARCHIVE:
        c = BY[slug]
        flat = [it for x in c["groups"] if x["kind"] != "video" for it in x["items"]]
        src = flat[gi % len(flat)]
        items += (f'<a href="{pre}trabalhos/{slug}.html" data-seg="{c["segment"]}"><figure>{pic(src, pre, "(max-width:600px) 50vw, 25vw", alt=c["client"])}'
                  f'<figcaption><span>{client_name(c)}</span><span>{seg_name(c["segment"])}</span></figcaption></figure></a>')
    chips = f'<button class="chip" type="button" data-seg="all" aria-pressed="true">{tx("archive.all")}</button>'
    for s in SEGMENTS:
        chips += f'<button class="chip" type="button" data-seg="{s}" aria-pressed="false">{seg_name(s)}</button>'
    return f'''<section class="sec" id="arquivo" aria-labelledby="h-arc"><div class="wrap">
<div class="sec-head"><h2 class="sec-title rv" id="h-arc">{tx("archive.title", "span")}</h2><div class="filters" data-filter="#arch" role="group" aria-label="Filtrar por segmento">{chips}</div></div>
<div class="arch" id="arch">{items}</div></div></section>'''


def sec_about(pre, uid="a"):
    return f'''<section class="sec" id="sobre" aria-labelledby="h-ab"><div class="wrap about">
<div class="rv">{avatar(uid, pre)}</div>
<div class="about-copy"><h2 class="sec-title rv" id="h-ab" style="margin-bottom:32px">{tx("about.title", "span")}</h2>{tx("about.p1", "p", "rv")}{tx("about.p2", "p", "rv")}</div>
</div></section>'''


def sec_contact():
    opts = "".join(f'<option value="{k}" data-i18n="opt.{k}">{e(T["opt." + k]["pt"])}</option>' for k in ["monthly", "identity", "pieces", "motion", "agency", "other"])
    return f'''<section class="sec contact" id="contato" aria-labelledby="h-ct"><div class="wrap contact-grid">
<div>
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

def home_v2(pre):
    rows = ""
    prev_imgs = ""
    for i, c in enumerate(CASES):
        rows += (f'<li class="rv" style="--d:{i*50}ms"><a href="{pre}trabalhos/{c["slug"]}.html" data-preview-item="{c["slug"]}">'
                 f'<span class="ix-n">{i+1:02d}</span><span class="ix-c">{client_name(c)}</span>'
                 f'<span class="ix-s">{seg_name(c["segment"])}</span><span class="ix-d">{deliver_line(c)}</span>'
                 f'<span class="ix-t">{pic(c["cover"], pre, "120px", alt="")}</span><span class="ix-a">{ICON["ne"]}</span></a></li>')
        m = MAN[c["cover"]]
        prev_imgs += f'<img data-k="{c["slug"]}" src="{pre}{m["base"]}-{m["w"][0]}.webp" alt="" loading="lazy" decoding="async">'
    return f'''<main id="main">
<section class="v2-hero"><div class="wrap">
<p class="v2-role rv">{tx("role", "span")}<span class="avail">{tx("available")}</span></p>
<h1 class="v2-name rv" style="--d:60ms">Alan<br>Veloso</h1>
<div class="v2-row rv" style="--d:120ms"><p class="v2-tag">{tx("tagline", "span")}</p><div class="btn-row">{cta_whats()}</div></div>
</div></section>
{sec_about(pre)}
<section class="sec v2-work" id="trabalhos" aria-labelledby="h-work"><div class="wrap">
<div class="sec-head"><h2 class="sec-title rv" id="h-work">{tx("work.title", "span")}</h2><p class="sec-note rv">{tx("tagline.short", "span")}</p></div>
<ol class="ix">{rows}</ol>
</div><div class="ix-prev" data-preview aria-hidden="true">{prev_imgs}</div></section>
{sec_services()}{sec_process()}{sec_palettes(pre)}{sec_archive(pre)}{sec_contact()}
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
    cover = ""
    body = f'''<body>
{header(pre, pre)}
<main id="main"><div class="wrap">
<section class="case-hero">
<p class="case-crumb"><a href="{pre}#trabalhos">{tx("case.back")}</a><span>/</span><span>{client_name(c)}</span></p>
<h1 class="case-title rv" data-i18n="ct.{s}">{title}</h1>
<dl class="case-meta rv"><div><dt>{tx("case.client")}</dt><dd>{client_name(c)}</dd></div><div><dt>{tx("case.segment")}</dt><dd>{seg_name(c["segment"])}</dd></div><div><dt>{tx("case.deliver")}</dt><dd>{deliver_line(c)}</dd></div></dl>
<div class="case-intro rv"><div>{credit}</div><p data-i18n="ci.{s}">{intro}</p></div>
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


def plans_page():
    pre = ""
    cols = ""
    for p_ in PLANS:
        k = p_["key"]; it = p_["items"]
        I18N[f"plan.{k}"] = p_["name"]["en"]; I18N[f"plan.for.{k}"] = p_["for"]["en"]
        li = ""
        if it["identity"]:
            li += f'<li><strong>{tx("pl.identity")}</strong> <span class="mute">{tx("pl.identity.when")}</span></li>'
        for key, one, many in (("static", "pl.static1", "pl.static"), ("carousel", "pl.carousel1", "pl.carousel"), ("reels", "pl.reels1", "pl.reels1"), ("stories", "pl.stories", "pl.stories")):
            n = it[key]
            if n:
                li += f'<li><strong class="tnum">{n}</strong> {tx(one if n == 1 else many)}</li>'
        from urllib.parse import quote
        wa = f"https://wa.me/{WHATSAPP}?text=" + quote(f"Oi, Alan! Tenho interesse no plano {p_['name']['pt']} ({brl(p_['price'])}/mês).")
        cols += f'''<article class="plan rv">
<h2 class="plan-name" data-i18n="plan.{k}">{e(p_["name"]["pt"])}</h2>
<p class="plan-price"><span class="tnum">{brl(p_["price"])}</span><small>{tx("plans.month")}</small></p>
<p class="plan-for" data-i18n="plan.for.{k}">{e(p_["for"]["pt"])}</p>
<ul class="plan-list">{li}</ul>
<p class="plan-save"><span>{tx("plans.single")} <s class="tnum">{brl(p_["single"])}</s></span><span class="plan-off tnum">{p_["off"]}% {tx("plans.off")}</span></p>
<a class="btn" href="{wa}" target="_blank" rel="noopener">{ICON["wa"]}{tx("plans.cta")}</a>
</article>'''
    heads = ["pl.plan", "pl.h.static", "pl.h.carousel", "pl.h.reels", "pl.h.stories", "pl.h.identity", "pl.h.single", "pl.h.off", "pl.h.month"]
    th = "".join(f'<th scope="col">{tx(h)}</th>' for h in heads)
    rows = ""
    for p_ in PLANS:
        it = p_["items"]; dash = '<span class="mute">—</span>'
        cell = lambda n: f'<td class="tnum">{n}</td>' if n else f"<td>{dash}</td>"
        ident = f'<td>{tx("pl.firstmonth")}</td>' if it["identity"] else f"<td>{dash}</td>"
        rows += (f'<tr><th scope="row" data-i18n="plan.{p_["key"]}">{e(p_["name"]["pt"])}</th>{cell(it["static"])}{cell(it["carousel"])}{cell(it["reels"])}{cell(it["stories"])}{ident}'
                 f'<td class="tnum mute">{brl(p_["single"])}</td><td class="tnum">{p_["off"]}%</td><td class="tnum"><strong>{brl(p_["price"])}</strong></td></tr>')
    singles = ""
    for i, (name, note, price) in enumerate(SINGLES):
        n = lt(f"sg.{i}", name)
        nt = f' <span class="mute" data-i18n="sg.n{i}">{lt(f"sg.n{i}", note)}</span>' if note else ""
        singles += f'<li><span><span data-i18n="sg.{i}">{n}</span>{nt}</span><span class="tnum">{brl(price)}</span></li>'
    body = f'''<body>
{header(pre, "./")}
<main id="main"><div class="wrap">
<section class="case-hero">
<h1 class="case-title rv">{tx("plans.title", "span")}</h1>
<p class="plans-lede rv">{tx("plans.lede", "span")}</p>
</section>
<div class="plans">{cols}</div>
<section class="group rv" aria-labelledby="h-cmp"><div class="group-head"><h2 id="h-cmp">{tx("plans.compare", "span")}</h2></div>
<div class="table-wrap" tabindex="0"><table class="cmp"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>
<p class="plans-foot">{tx("plans.foot", "span")}</p></section>
<section class="group rv" aria-labelledby="h-sg"><div class="group-head"><h2 id="h-sg">{tx("plans.singles", "span")}</h2><span>{tx("plans.singles.note", "span")}</span></div>
<ul class="singles">{singles}</ul></section>
<div class="case-cta rv"><p>{tx("plans.custom", "span")}</p><div class="btn-row"><a class="btn" href="./#contato">{tx("plans.custom.cta")}{ICON["arr"]}</a></div></div>
</div></main>
<div style="height:clamp(56px,8vw,112px)"></div>
{footer(pre)}'''
    return head("Planos e valores — Alan Veloso", "Planos mensais de social media e valores de peças avulsas: estático, carrossel, reels, stories e identidade visual.", pre, ["base"]) + body


def write(path, html):
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(html)


DESC = "Alan Veloso, designer de social media e branding em São Paulo. Feed, identidade visual, carrosséis, motion e artes de evento para marcas e agências."

page = head("Alan Veloso — Social media e branding", DESC, "", ["base", "home"]) + "<body>" + header("", "./") + home_v2("") + footer("")
write("index.html", page)
write("planos.html", plans_page())


for i, c in enumerate(CASES):
    write(f"trabalhos/{c['slug']}.html", case_page(c, CASES[(i + 1) % len(CASES)]))

open(os.path.join(SITE, "assets/js/i18n.js"), "w", encoding="utf-8").write("window.I18N=" + json.dumps(I18N, ensure_ascii=False) + ";")

print("ok", len(I18N), "strings EN")
