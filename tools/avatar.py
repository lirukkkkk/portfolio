# -*- coding: utf-8 -*-
"""Separa as pupilas do autorretrato para animar (piscar / olhar).
Gera: site/assets/avatar/alan-lines.png (traço sem pupilas),
      site/assets/avatar/eyes-mask.png (área interna dos olhos) e tools/avatar.json (geometria)."""
import os, json
import numpy as np
from collections import deque
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
im = Image.open(os.path.join(ROOT, "Icon Alan.JPG")).convert("L")
a = np.array(im).astype(float)
dark = a < 110
H, W = dark.shape

def flood(mask, seeds):
    m = np.zeros_like(mask); q = deque()
    for s in seeds:
        if mask[s]: m[s] = 1; q.append(s)
    while q:
        y, x = q.popleft()
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny, nx = y+dy, x+dx
            if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not m[ny, nx]:
                m[ny, nx] = 1; q.append((ny, nx))
    return m.astype(bool)

def erode(mask, n):
    img = Image.fromarray((mask*255).astype("uint8"))
    for _ in range(n): img = img.filter(ImageFilter.MinFilter(3))
    return np.array(img) > 0

def box_soft(y0, y1, x0, x1):
    b = np.zeros_like(dark); b[y0:y1+1, x0:x1+1] = True; return b

eyes = []
pupil_all = np.zeros_like(dark); interior_all = np.zeros_like(dark)
for seed in [(700, 465), (680, 705)]:
    comp = flood(dark, [seed])
    ys, xs = np.nonzero(comp); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    # pupila = região mais grossa do traço
    k, last = 0, comp
    while True:
        e = erode(comp, k+1)
        if not e.any(): break
        k += 1; last = e
    py, px = np.nonzero(last); cy, cx = py.mean(), px.mean(); r = k + 1.5
    # espessura do traço: erosões até os traços finos sumirem (fora da pupila)
    yy, xx = np.mgrid[0:H, 0:W]
    far = ((yy-cy)**2 + (xx-cx)**2) > (r+6)**2
    t = 0
    while erode(comp & far, t+1).any(): t += 1
    stroke = 2*t + 1
    # topo da pálpebra por coluna
    lidtop = {}
    for x in range(x0, x1+1):
        col = np.nonzero(comp[:, x])[0]
        if len(col): lidtop[x] = col.min()
    pupil = np.zeros_like(dark)
    sy, sx = np.nonzero((a < 238) & box_soft(y0 - 4, y1 + 4, x0 - 4, x1 + 4))
    for y, x in zip(sy, sx):
        if x not in lidtop or y <= lidtop[x] + stroke - 1:
            continue
        d2 = (y - cy) ** 2 + (x - cx) ** 2
        if d2 <= (r + 7.5) ** 2 or (d2 <= (r + 11) ** 2 and a[y, x] >= 110):
            pupil[y, x] = True
    # interior: claro não alcançável a partir da borda da caixa
    pad = 6
    box = np.zeros_like(dark); box[y0-pad:y1+pad+1, x0-pad:x1+pad+1] = True
    light = box & ~comp
    border = [(y, x) for y in (y0-pad, y1+pad) for x in range(x0-pad, x1+pad+1)] + [(y, x) for x in (x0-pad, x1+pad) for y in range(y0-pad, y1+pad+1)]
    outside = flood(light, border)
    interior = (light & ~outside) | pupil
    interior = np.array(Image.fromarray((interior*255).astype("uint8")).filter(ImageFilter.MaxFilter(3))) > 0
    iy, ix = np.nonzero(interior)
    print("eye", seed, "pupil", round(cx), round(cy), round(r), "stroke", stroke, "interior px", interior.sum(), "box", ix.min(), iy.min(), ix.max(), iy.max())
    pupil_all |= pupil; interior_all |= interior
    eyes.append({"cx": round(cx, 1), "cy": round(cy, 1), "r": round(r + 6, 1), "stroke": stroke,
                 "x": int(ix.min()), "y": int(iy.min()), "w": int(ix.max()-ix.min()+1), "h": int(iy.max()-iy.min()+1)})

# traço sem pupilas
ink = np.clip((235 - a) / (235 - 40), 0, 1)
pd = np.array(Image.fromarray((pupil_all*255).astype("uint8")).filter(ImageFilter.MaxFilter(3))) > 0
ink[pd & ~erode(~pd, 0)] = 0
ink[pd] = 0
crop = (150, 150, 1050, 1050)
out = Image.fromarray((ink*255).astype("uint8")).crop(crop).resize((600, 600), Image.LANCZOS)
la = Image.new("LA", out.size); la.putdata([(0, v) for v in np.array(out).flatten().tolist()])
d = os.path.join(ROOT, "site/assets/avatar"); la.save(os.path.join(d, "alan-lines.png"), optimize=True)
m = Image.fromarray((interior_all*255).astype("uint8")).crop(crop).resize((600, 600), Image.LANCZOS)
m.save(os.path.join(d, "eyes-mask.png"), optimize=True)
json.dump(eyes, open(os.path.join(ROOT, "tools/avatar.json"), "w"), indent=1)
