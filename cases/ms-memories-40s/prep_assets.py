#!/usr/bin/env python3
"""Builds the static assets for the Ms. Memories ad: textures, the logo (ink + gold foil), a QR matrix, inlined Amiri."""
import base64, json, os, sys
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = sys.argv[1]; FONTS = sys.argv[2]
rng = np.random.default_rng(11)

def noise(h, w, sigma):                                   # tileable band-limited noise, 0..1
    n = gaussian_filter(rng.standard_normal((h, w)), sigma, mode="wrap"); n -= n.min(); return n / n.max()

def save(arr, name, q=90):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(os.path.join(HERE, name), quality=q)

# ── ivory linen table (tileable 768²) ──
S = 768; y, x = np.mgrid[0:S, 0:S]
weave = 0.5 + 0.25 * np.sin(x * 2 * np.pi / 6) * np.sin(y * 2 * np.pi / 6 + 1.0)
fiber = noise(S, S, 1.2) * 0.6 + noise(S, S, 6) * 0.4
base = np.array([243, 235, 221], float)
lum = (weave * 0.35 + fiber * 0.65 - 0.5) * 22
save(base[None, None, :] + lum[..., None] + noise(S, S, 60)[..., None] * 6, "table.jpg")

# ── burgundy leather (tileable 640²) ──
S = 640
pores = noise(S, S, 1.0) * 0.55 + noise(S, S, 2.4) * 0.45
grain = (pores - 0.5) * 34 + (noise(S, S, 40) - 0.5) * 30
b = np.array([104, 24, 40], float)
save(b[None, None, :] + grain[..., None] * np.array([1.0, 0.45, 0.55])[None, None, :], "leather.jpg")

# ── cream paper (tileable 512²) ──
S = 512
p = noise(S, S, 0.9) * 0.5 + noise(S, S, 3.0) * 0.5
save(np.array([250, 246, 237], float)[None, None, :] + ((p - 0.5) * 9)[..., None], "paper.jpg", 92)

# ── logo: the ink becomes alpha; one black copy, one gold-foil copy ──
im = Image.open(LOGO).convert("RGBA"); bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
g = np.asarray(bg.convert("L"), float); a = np.clip((255 - g) / 255 * 1.15, 0, 1)
ys, xs = np.where(a > 0.08); pad = 12
y0, y1, x0, x1 = max(ys.min() - pad, 0), ys.max() + pad, max(xs.min() - pad, 0), xs.max() + pad
a = a[y0:y1, x0:x1]; h, w = a.shape
ink = np.zeros((h, w, 4), np.uint8); ink[..., 0:3] = (28, 12, 16); ink[..., 3] = (a * 255).astype(np.uint8)
Image.fromarray(ink).save(os.path.join(HERE, "logo-ink.png"))
gy = np.linspace(0, 1, h)[:, None]; gx = np.linspace(0, 1, w)[None, :]
t = np.clip(0.55 * gy + 0.45 * np.sin(gx * 7 + gy * 3) * 0.5 + 0.35, 0, 1)
c0 = np.array([236, 208, 134], float); c1 = np.array([176, 132, 44], float)
gold = np.zeros((h, w, 4), np.uint8); gold[..., 0:3] = (c0[None, None, :] * (1 - t[..., None]) + c1[None, None, :] * t[..., None]).astype(np.uint8); gold[..., 3] = (a * 255).astype(np.uint8)
Image.fromarray(gold).save(os.path.join(HERE, "logo-gold.png"))
print("logo", w, h)

# ── QR matrix (a placeholder link; the real one is the client's) ──
qr = segno.make("https://example.com/memory/0427", error="m", boost_error=False)
m = [[1 if c else 0 for c in row] for row in qr.matrix]
json.dump(m, open(os.path.join(HERE, "qr.json"), "w")); print("qr", len(m))

# ── Amiri, inlined ──
out = []
for sub, rng_ in (("arabic", "U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF,U+200C-200F,U+060C,U+061B,U+061F"), ("latin", "U+0000-00FF,U+2000-206F,U+2026")):
    for w_ in (400, 700):
        data = base64.b64encode(open(f"{FONTS}/amiri-{sub}-{w_}-normal.woff2", "rb").read()).decode()
        out.append(f"@font-face{{font-family:'Amiri';font-weight:{w_};src:url(data:font/woff2;base64,{data}) format('woff2');unicode-range:{rng_};}}")
open(os.path.join(HERE, "fonts.css"), "w").write("\n".join(out)); print("fonts ok")
