#!/usr/bin/env python3
"""score.py — the film's sound, synthesised from nothing (no samples, no voice): a soft cinematic bed in D minor → D major,
a plucked-piano arpeggio, and sound effects timed from the composition's own window.__events().
  python3 score.py            → score.wav (44.1 kHz stereo, 30 s)
"""
import asyncio, json, os, sys
import numpy as np
from scipy.signal import lfilter, fftconvolve
from scipy.io import wavfile

SR = 44100; DUR = 30.0; N = int(SR * DUR); rng = np.random.default_rng(7)
here = os.path.dirname(os.path.abspath(__file__))

async def get_events():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await (await br.new_context(viewport={"width": 1080, "height": 1920})).new_page()
        await pg.goto("file://" + os.path.join(here, "comp.html")); await pg.evaluate("window.__ready")
        ev = await pg.evaluate("window.__events()"); await br.close(); return ev["events"]
events = asyncio.run(get_events()); json.dump(events, open(os.path.join(here, "events.json"), "w"))

L = np.zeros(N); R = np.zeros(N)
def put(sig, t, gain=1.0, pan=0.0, bus=None):
    i = int(t * SR);
    if i >= N or i < 0: return
    s = sig[: N - i] * gain; a = np.sqrt((1 - pan) / 2) * np.sqrt(2) / np.sqrt(2); b = np.sqrt((1 + pan) / 2)
    (bus or (L, R))[0][i:i + len(s)] += s * a; (bus or (L, R))[1][i:i + len(s)] += s * b
def tt(d): return np.arange(int(SR * d)) / SR
def midi(m): return 440.0 * 2 ** ((m - 69) / 12)
def lp(x, fc, order=1):
    a = np.exp(-2 * np.pi * fc / SR)
    for _ in range(order): x = lfilter([1 - a], [1, -a], x)
    return x
def hp(x, fc): return x - lp(x, fc)
def bp(x, f0, f1): return hp(lp(x, f1, 2), f0)
def env(n, a, r):
    e = np.ones(n); na = max(1, int(a * SR)); nr = max(1, int(r * SR)); e[:na] = np.linspace(0, 1, na) ** 1.5; e[-nr:] *= np.linspace(1, 0, nr) ** 1.5; return e

# ───────────── music bus (kept apart so the effects can sit on top) ─────────────
ML = np.zeros(N); MR = np.zeros(N); mus = (ML, MR)
BAR = 4 * 60 / 76
CH = [  # (root midi, chord tones)
    (38, [50, 53, 57, 62]), (34, [46, 50, 53, 57]), (41, [53, 57, 60, 64]), (36, [48, 52, 55, 60]),
    (38, [50, 53, 57, 62]), (34, [46, 50, 53, 57]), (43, [55, 58, 62, 67]), (45, [57, 61, 64, 69]),
    (34, [46, 50, 53, 62]), (38, [50, 54, 57, 62, 66])]
def saw(f, d, det=(0.997, 1.0, 1.003)):
    t = tt(d); x = np.zeros_like(t)
    for dt in det:
        for h in range(1, 14): x += np.sin(2 * np.pi * f * dt * h * t + h) / h * (0.8 if h > 1 else 1)
    return x / len(det)
for b, (root, tones) in enumerate(CH):
    t0 = b * BAR; d = BAR + 1.6
    for k, m in enumerate(tones):
        x = lp(saw(midi(m - 12 if k == 0 else m), d), 700 + 500 * (b / 10), 2) * env(int(SR * d), 1.1, 1.6)
        put(x, t0, .075, (k - 1.5) * .35, mus)
    s = np.sin(2 * np.pi * midi(root) * tt(d)) * env(int(SR * d), .4, 1.2); put(s, t0, .22, 0, mus)
def pluck(f, d=2.4, bright=1.0):
    t = tt(d); x = np.zeros_like(t)
    for h in range(1, 9): x += np.sin(2 * np.pi * f * h * t * (1 + 0.0004 * h * h)) / (h ** 1.4) * np.exp(-t * (1.6 + .9 * h) / bright)
    x[: int(.004 * SR)] += rng.normal(0, .15, int(.004 * SR)); return x * np.minimum(1, t * 400)
PAT = [0, 2, 1, 3, 2, 3, 1, 2]
for b, (root, tones) in enumerate(CH):
    step = 60 / 76 / 2
    for k in range(8):
        t = b * BAR + k * step + .5 * (b == 0)
        if t < 0.8 or t > 29.4: continue
        sparse = t < 9.0 or (t > 23.0 and t < 27)
        if sparse and k % 2: continue
        m = tones[PAT[k] % len(tones)] + 12 * (1 if k % 4 == 3 else 0)
        put(pluck(midi(m)), t, .09 + .03 * (k == 0), np.sin(k) * .4, mus)
for i, m in enumerate([81, 78, 74, 78, 81, 86]):             # a high bell phrase that lands with the wordmark
    put(pluck(midi(m), 3.2, 1.6), 27.1 + i * .32, .1, (i - 2.5) * .12, mus)
put(pluck(midi(62 + 12), 4, 1.8), 27.15, .09, 0, mus)

# ───────────── effects bus ─────────────
SL = np.zeros(N); SRr = np.zeros(N); sfx = (SL, SRr)
def noise(d): return rng.normal(0, 1, int(SR * d))
def whoosh(d=1.1, up=True):
    n = noise(d); out = np.zeros_like(n); parts = 14; seg = len(n) // parts
    for p in range(parts):
        u = p / (parts - 1); fc = 300 + 3600 * (u if up else 1 - u) ** 1.5
        out[p * seg:(p + 1) * seg] = bp(n, fc * .6, fc * 1.4)[p * seg:(p + 1) * seg]
    return out * np.sin(np.linspace(0, np.pi, len(out))) ** 2
def shimmer(d=2.4, base=79):
    out = np.zeros(int(SR * d))
    for i, m in enumerate([0, 4, 7, 12, 16, 19, 24]):
        n = pluck(midi(base + m), 1.6, 1.4); o = int(i * .07 * SR); out[o:o + len(n)] += n[: len(out) - o] * (1 - i * .08)
    return out
def thump(d=.9): t = tt(d); return np.sin(2 * np.pi * (46 + 40 * np.exp(-t * 12)) * t) * np.exp(-t * 5) + .25 * lp(noise(d), 300) * np.exp(-t * 14)
def flip(d=.42):
    n = noise(d); t = tt(d); sw = bp(n, 1500, 7000) * np.exp(-((t - .12) / .09) ** 2) * 1.0; r = bp(noise(d), 300, 1800) * np.exp(-t * 18) * .5
    return (sw + r + .3 * np.sin(2 * np.pi * 90 * t) * np.exp(-t * 30))
def chime(f, d=1.4): return pluck(f, d, 1.7)
def pop(): t = tt(.18); return np.sin(2 * np.pi * (500 + 700 * np.exp(-t * 40)) * t) * np.exp(-t * 28) * .5 + .3 * bp(noise(.18), 2500, 6000) * np.exp(-t * 60)
def absorb(i=0): return chime(midi(86 + [0, 2, 4, 7, 9][i % 5]), .9) * .8 + .2 * hp(noise(.3), 4000)[: int(.9 * SR)].repeat(1)[:0].sum() if False else chime(midi(86 + [0, 2, 4, 7, 9][i % 5]), .9)

absorbs = 0
for e in events:
    t, k, v, pan = e["t"], e["kind"], e["v"], e["pan"]
    if k == "swell":  put(lp(noise(5), 800, 2) * env(int(5 * SR), 3, 1.5), t, .35, 0, sfx)
    elif k == "whoosh": put(whoosh(1.2, True), t, .30 * v, pan, sfx)
    elif k == "pop":  put(pop(), t, .22 * v, pan, sfx)
    elif k == "shimmer": put(shimmer(2.4), t, .16 * v, 0, sfx)
    elif k == "absorb": put(absorb(absorbs), t, .13 * v, pan, sfx); absorbs += 1
    elif k == "thump": put(thump(), t, .55 * v, 0, sfx)
    elif k == "cover": put(thump(1.1), t, .4 * v, 0, sfx); put(whoosh(.7, False), t, .22, 0, sfx)
    elif k == "flip": put(flip(), t, .55 * v, pan, sfx)
    elif k == "lock": put(chime(midi(88), .9), t, .22 * v, .2, sfx); put(chime(midi(95), .9), t + .09, .16 * v, .2, sfx)
    elif k == "scan": put(bp(noise(.7), 1200, 3200) * np.sin(np.linspace(0, np.pi, int(.7 * SR))) ** 2, t, .09 * v, 0, sfx)
    elif k == "success":
        for i, m in enumerate([76, 83, 88, 95]): put(chime(midi(m), 2.0), t + i * .06, .2 * v, (i - 1.5) * .25, sfx)
        put(whoosh(.9, True), t, .22, 0, sfx)
    elif k == "close": put(thump(1.2), t, .65 * v, 0, sfx); put(flip(.5), t - .05, .5, 0, sfx)
    elif k == "logo": put(thump(1.4), t, .3, 0, sfx); put(shimmer(3), t, .2, 0, sfx)

# ───────────── the room: one reverb for everything, a little more on the music ─────────────
def room(x, seconds=2.4, decay=3.2):
    t = tt(seconds); ir = rng.normal(0, 1, (2, len(t))) * np.exp(-t * decay) * (1 - np.exp(-t * 60))
    ir = np.stack([lp(ir[0], 5200, 1), lp(ir[1], 5200, 1)]); ir /= np.abs(ir).sum() / 14
    return fftconvolve(x[0], ir[0])[:N], fftconvolve(x[1], ir[1])[:N]
mw = room(mus); sw_ = room(sfx, 2.0, 3.6)
musL = ML * .75 + mw[0] * .55; musR = MR * .75 + mw[1] * .55
sfxL = SL * .85 + sw_[0] * .5; sfxR = SRr * .85 + sw_[1] * .5
# the music ducks a little under the effects
duck = lp(np.abs(sfxL + sfxR) * 6, 6, 1); duck = 1 - np.clip(duck / (duck.max() + 1e-9), 0, 1) * .25
outL = musL * duck + sfxL; outR = musR * duck + sfxR
fade = np.ones(N); fade[:int(.6 * SR)] = np.linspace(0, 1, int(.6 * SR)); fade[-int(1.8 * SR):] = np.linspace(1, 0, int(1.8 * SR)) ** 1.5
st = np.stack([outL * fade, outR * fade], 1); st = hp(st[:, 0], 28)[:, None].repeat(2, 1) * 0 + np.stack([hp(st[:, 0], 28), hp(st[:, 1], 28)], 1)
st *= 0.7 / np.abs(st).max()
wavfile.write(os.path.join(here, "score.wav"), SR, (st * 32767).astype(np.int16)); print("score.wav", st.shape, "peak", np.abs(st).max())
