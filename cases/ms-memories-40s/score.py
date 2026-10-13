#!/usr/bin/env python3
"""Ms. Memories · sound. No voice. Original synthesised piano + strings (D major, 66 BPM) and effects timed from the comp's own events."""
import sys, os, wave, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
import numpy as np
from scipy import signal
from sfx_palette import *
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__)); DUR = 42.0
rng = np.random.default_rng(3)
mf = lambda m: 440.0 * 2 ** ((m - 69) / 12)

async def events():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto("file://" + os.path.join(HERE, "comp.html")); await pg.evaluate("window.__ready")
        ev = await pg.evaluate("window.__events()"); await b.close(); return ev

# ── instruments ──
def piano(f, dur=3.0, vel=0.8):
    n = int(SR * dur); t = np.arange(n) / SR; base = 0.7 + f / 500.0; s = np.zeros(n)
    for h in range(1, 9):
        fh = f * h * (1 + 0.00035 * h * h)
        if fh > 9000: break
        s += (1.0 / h ** 1.15) * np.sin(2 * np.pi * fh * t + h) * np.exp(-t * base * (1 + 0.7 * (h - 1)))
    s += 0.12 * np.sin(2 * np.pi * f * 1.003 * t) * np.exp(-t * base)                       # slight beating, like two strings
    ham = lp(rng.standard_normal(n), 2400) * np.exp(-t * 260) * 0.10
    env = np.minimum(t / 0.003, 1) * np.exp(-np.maximum(t - dur + 0.4, 0) * 9)
    out = (s + ham) * env; return out / (np.abs(out).max() + 1e-9) * vel
def strings(freqs, dur, att=1.2, rel=1.6):
    n = int(SR * (dur + rel)); t = np.arange(n) / SR; out = np.zeros(n)
    for f in freqs:
        for dt in (-0.0025, 0.0, 0.0030):
            ff = f * (1 + dt); ph = 2 * np.pi * ff * t
            out += (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.28 * np.sin(3 * ph) + 0.14 * np.sin(4 * ph)) * (1 + 0.12 * np.sin(2 * np.pi * 5.2 * t + ff))
    out = lp(out, 2600) * np.minimum(t / att, 1) * np.where(t < dur, 1.0, np.exp(-(t - dur) / (rel / 4)))
    return out / (np.abs(out).max() + 1e-9)
def paper(dur=0.38, f0=1400, f1=4200, rev=False):
    n = int(SR * dur); x = sweep_bp(rng.standard_normal(n), f1 if rev else f0, f0 if rev else f1, 0.8)
    t = np.linspace(0, 1, n); e = np.sin(np.pi * t) ** 1.2 * (0.6 + 0.4 * rng.random(n)); x = hp(x * e, 700); return x / (np.abs(x).max() + 1e-9)
def thump(f=70, dur=0.5): return sub(f, dur)

# ── the score ──
BEAT = 60 / 66.0; BAR = 4 * BEAT
CH = [dict(root=38, tones=(50, 57, 62, 66)), dict(root=35, tones=(47, 54, 59, 62)), dict(root=43, tones=(50, 55, 59, 62)), dict(root=45, tones=(52, 57, 61, 64))]   # D · Bm · G · A
def music(s):
    nb = int(DUR / BAR) + 1
    # dynamic shape, 0..1
    dyn = lambda t: float(np.interp(t, [0, 3, 7, 12, 13, 21, 22.5, 28, 31, 34, 36, 39, 41, 42], [.30, .40, .55, .80, .85, .85, .45, .50, .90, 1.0, .70, .50, .30, 0]))
    for b in range(nb):
        t0 = b * BAR; c = CH[b % 4]
        if t0 >= DUR - 1.2: break
        d = dyn(t0)
        s.place(piano(mf(c["root"]), 3.6, .85), t0, .20 * (.6 + d * .6), pan=-.15, send=.35)
        sparse = 21.8 < t0 < 28.4
        pat = (0, 2, 1, 3, 2, 3, 1, 2) if not sparse else (0, None, 2, None, 1, None, 3, None)
        for k, ix in enumerate(pat):
            ts = t0 + k * BEAT / 2
            if ix is None or ts < 1.4 or ts >= DUR - 1.4: continue
            s.place(piano(mf(c["tones"][ix] + (12 if d > .7 else 0)), 1.8, .8), ts, .13 * (.5 + d * .75), pan=(-.35, .35)[k % 2], send=.45)
        if t0 >= 6.5 and t0 < DUR - 3:
            fr = [mf(m) for m in c["tones"][:3]]; s.place(strings(fr, BAR, 1.4, 1.8), t0, .11 * d, pan=0, send=.6)
    # melody: sparse, singing, over the strong sections
    mel = [(14.5, 78), (16.4, 81), (18.2, 78), (20.0, 74), (22.5, 73), (24.3, 74), (26.0, 78), (28.6, 81),
           (30.0, 85), (31.7, 83), (33.3, 81), (35.0, 78), (36.8, 74), (38.2, 78)]
    for tm, n in mel: s.place(piano(mf(n), 2.6, .85), tm, .20, pan=.1, send=.55)
    # last chord: D major, held, then the single high D, then silence
    s.place(strings([mf(50), mf(57), mf(62), mf(66)], 3.2, .8, 2.0), 37.2, .13, send=.7)
    s.place(piano(mf(86), 3.0, .9), 38.6, .16, send=.75)

def main():
    ev = asyncio.run(events()); s = Score(dur=DUR, T60=1.7)
    music(s)
    pent = [74, 76, 78, 81, 83, 86]
    for e in ev:
        t, k = e["t"], e["k"]
        if k == "tap":    s.place(wood(520, .04), t, .20, pan=.1, send=.15); s.place(glass(1760, .3, .3), t + .01, .03, send=.4)
        elif k == "lift": s.place(glass(mf(pent[e["j"] % 6] + 12 * (e["j"] // 6 % 2)), .9, .7), t, .045, pan=((e["j"] % 5) - 2) * .22, send=.7)
        elif k == "whoosh": s.place(air(.9, 250, 3600, 1.2, .5), t - .1, .30, send=.55, pan=-.3, pan_to=.3)
        elif k == "land": s.place(wood(150 + 6 * e["j"], .09), t, .10, pan=((e["j"] % 5) - 2) * .12, send=.35)
        elif k == "fall": s.place(air(.8, 3200, 260, 1.2, .6), t, .35, send=.5)
        elif k == "magic":
            s.place(thump(58, .9), t, .55, send=.45)
            for i, f in enumerate((1318, 1760, 2093, 2637, 3136)): s.place(glass(f, 1.8, .9), t + .02 + i * .05, .10, send=.8, pan=(i - 2) * .25)
            s.place(air(1.1, 400, 5200, 1.1, .6), t, .30, send=.6)
        elif k == "cover": s.place(thump(52, .7), t + .05, .30, send=.4); s.place(lp(rng.standard_normal(int(SR * .9)), 700) * np.sin(np.linspace(0, np.pi, int(SR * .9))) * .6, t, .12, send=.3)
        elif k == "flip": s.place(paper(.42, 1400, 4600, e["dir"] < 0), t, .30, pan=.15 * e["dir"], send=.4); s.place(wood(120, .1), t + .38, .10, send=.3)
        elif k == "close": s.place(thump(48, .9), t, .5, send=.45); s.place(wood(110, .15), t, .25, send=.35)
        elif k == "phoneIn": s.place(air(.8, 300, 2400, 1.2, .5), t, .22, send=.4, pan=.4)
        elif k == "scan": [s.place(glass(1175, .5, .6), t + i * .8, .08, send=.6, pan=.2) for i in range(2)]
        elif k == "lock": s.place(glass(1568, 1.4, .8), t, .16, send=.7); s.place(glass(2349, 1.4, .8), t + .04, .10, send=.7); s.place(thump(80, .35), t, .18, send=.3)
        elif k == "chip": s.place(bubble(560, .22), t, .25, send=.4)
        elif k == "video": s.place(air(.7, 300, 5000, 1.1, .4), t - .1, .25, send=.5); s.place(glass(1760, 1.6, .9), t + .05, .10, send=.8)
        elif k == "phrase": s.place(thump(62, 1.2), t, .30, send=.5)
        elif k == "logo": s.place(air(1.4, 600, 6000, 1.1, .7), t, .22, send=.6)
        elif k == "tag": s.place(glass(1760, 1.8, .9), t + .05, .09, send=.8)
    sfx = s.mix(peak_db=-3.5)
    n = len(sfx); mix = sfx.copy()
    # master: gentle tape-ish saturation, then fade to true silence over the last 1.4 s
    mix = np.tanh(mix * 2.2) / np.tanh(2.2); mix = mix / np.abs(mix).max() * 10 ** (-3.5 / 20)
    tt = np.arange(n) / SR; fade = np.clip((DUR - tt) / 1.4, 0, 1) ** 1.5; mix *= fade[:, None]
    out = os.path.join(HERE, "sfx.wav")
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    print("wrote", out, len(ev), "events")

if __name__ == "__main__":
    main()
