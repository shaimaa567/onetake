#!/usr/bin/env python3
"""Sound for the TS trade forex reel: original synthesised music (no third-party track) + effects from the comp's own events."""
import sys, os, json, asyncio, wave
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
import numpy as np
from scipy import signal
from sfx_palette import *
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__)); DUR = 30.0

async def events():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto("file://" + os.path.join(HERE, "comp.html")); await pg.evaluate("window.__ready")
        ev = await pg.evaluate("window.__events()"); await b.close(); return ev

def music(dur):
    """a soft electronic bed, 96 BPM: a four-chord pad, a plucked arpeggio, a low pulse; thin in the quiet stretches, full only at the end"""
    n = int(SR * dur); t = np.arange(n) / SR; bpm = 96; beat = 60 / bpm; bar = 4 * beat
    chords = [(57, 60, 64, 67), (53, 57, 60, 64), (48, 52, 55, 59), (55, 59, 62, 65)]   # Am7 · Fmaj7 · Cmaj7 · G
    mf = lambda m: 440 * 2 ** ((m - 69) / 12)
    out = np.zeros((n, 2))
    for b in range(int(dur / bar) + 1):
        t0 = b * bar; ch = chords[b % 4]; i0 = int(t0 * SR); i1 = min(n, int((t0 + bar + 0.6) * SR)); m = i1 - i0
        if m <= 0: break
        tt = np.arange(m) / SR; env = np.minimum(tt / 0.5, 1) * np.exp(-np.maximum(tt - bar, 0) * 6) * 0.55
        pad = sum(np.sin(2 * np.pi * mf(x) * tt) + 0.5 * np.sin(2 * np.pi * mf(x) * 1.003 * tt) for x in ch) / len(ch)
        out[i0:i1, 0] += lp(pad, 1800) * env * 0.5; out[i0:i1, 1] += lp(pad, 1800) * env * 0.5
        ro = np.sin(2 * np.pi * mf(ch[0] - 12) * tt) * np.minimum(tt / 0.05, 1) * np.exp(-np.maximum(tt - bar, 0) * 8) * 0.5
        out[i0:i1, 0] += ro; out[i0:i1, 1] += ro
        for s in range(8):                                                    # plucked eighths
            ts = t0 + s * beat / 2; j0 = int(ts * SR); L = int(0.5 * SR)
            if j0 + L > n: break
            note = ch[(0, 2, 1, 3, 2, 1, 3, 2)[s]] + 12; tp = np.arange(L) / SR
            pl = (np.sin(2 * np.pi * mf(note) * tp) + 0.3 * np.sin(4 * np.pi * mf(note) * tp)) * np.exp(-tp * 7)
            pan = (-0.4, 0.4)[s % 2]; out[j0:j0 + L, 0] += pl * 0.16 * (1 - pan) / 2; out[j0:j0 + L, 1] += pl * 0.16 * (1 + pan) / 2
    # section shape: air at the start, fullest 15-21 s, almost nothing for the pip hold and the first logo beat
    sh = np.interp(t, [0, 0.6, 5, 6, 12, 13.2, 15, 21, 22.5, 26.4, 27.2, 29, 30], [0.15, 0.55, 0.6, 0.85, 0.85, 0.35, 0.9, 1.0, 0.55, 0.45, 1.0, 0.9, 0.0])
    out *= sh[:, None]
    # low pulse on every beat from 15 s
    for k in range(int(15 / beat), int(26 / beat)):
        ts = k * beat; j0 = int(ts * SR); L = int(0.3 * SR); tp = np.arange(L) / SR
        kick = np.sin(2 * np.pi * (46 + 60 * np.exp(-tp * 30)) * tp) * np.exp(-tp * 11) * 0.5
        out[j0:j0 + L, 0] += kick * 0.35; out[j0:j0 + L, 1] += kick * 0.35
    return out

def main():
    ev = asyncio.run(events()); s = Score(dur=DUR, T60=1.2)
    pent = [69, 72, 74, 76, 79, 81, 84, 86, 88, 91]            # A minor pentatonic, one note per pip
    for e in ev:
        t, k = e["t"], e["k"]
        if k == "sweep":   s.place(air(1.3, 200, 2800, 1.2, 0.8), t, 0.35, send=0.5, pan=-0.3, pan_to=0.3)
        elif k == "div":   s.place(wood(300 + 8 * e["i"], 0.05), t, 0.12, pan=(e["i"] / 16 - 0.5) * 1.0, send=0.2)
        elif k == "candle":s.place(wood(190 if e["bull"] else 120, 0.1), t, 0.30, pan=(e["i"] / 15 - 0.5) * 1.0, send=0.3); s.place(glass(880 if e["bull"] else 440, 0.5, 0.4), t, 0.07, send=0.5)
        elif k == "label": s.place(bubble(560 + 70 * e["i"], 0.2), t, 0.22, send=0.35, pan=0.2)
        elif k == "whoosh":s.place(air(0.55, 250, 3200, 1.3, 0.35), t - 0.05, 0.5, send=0.5, pan=-0.4, pan_to=0.4)
        elif k == "tag":   s.place(glass(1175, 0.7, 0.8), t, 0.18, send=0.5)
        elif k == "split": s.place(air(0.45, 300, 4200, 1.2, 0.3), t, 0.45, send=0.4, pan=-0.4, pan_to=0.4); s.place(sub(58, 0.8), t + 0.12, 0.55, send=0.4)
        elif k == "press": s.place(wood(170 if e["side"] == "buy" else 120, 0.14), t, 0.55, send=0.3); s.place(glass(659 if e["side"] == "buy" else 330, 0.9, 0.7), t + 0.02, 0.22, send=0.5, pan=0.25 if e["side"] == "buy" else -0.25)
        elif k == "pip":
            n = e["n"]; f = 440 * 2 ** ((pent[n - 1] - 69) / 12); s.place(glass(f, 0.7, 1.0), t, 0.16, send=0.55, pan=(n / 10 - 0.5) * 0.8); s.place(wood(260, 0.05), t, 0.12)
        elif k == "bracket": s.place(air(0.4, 400, 3800, 1.2, 0.3), t, 0.3, send=0.4); s.place(glass(1318, 1.0, 0.8), t + 0.3, 0.14, send=0.6)
        elif k == "gather":s.place(air(0.9, 3500, 300, 1.2, 0.7), t, 0.4, send=0.5)
        elif k == "logo":  s.place(sub(52, 1.6), t, 0.7, send=0.5); [s.place(glass(f, 1.8, 0.8), t + 0.05, 0.15, send=0.7, pan=p) for f, p in ((440, -0.3), (659, 0), (880, 0.3))]
    sfx = s.mix(peak_db=-4.0)
    m = music(DUR); m = m / (np.abs(m).max() + 1e-9) * 0.25                    # music sits ~ -12 dBFS under the effects
    # duck the music 4 dB for 0.25 s after every effect that is not a quiet tick
    duck = np.ones(len(m)); 
    for e in ev:
        if e["k"] in ("split", "press", "logo", "whoosh", "tag"):
            i0 = int(e["t"] * SR); L = int(0.35 * SR); env = 1 - 0.4 * np.exp(-np.arange(L) / (0.12 * SR)); duck[i0:i0 + L] = np.minimum(duck[i0:i0 + L], env[:len(duck[i0:i0 + L])])
    mix = sfx[:len(m)] + m * duck[:, None]
    mix = np.tanh(mix * 1.2) / np.tanh(1.2); mix = mix / np.abs(mix).max() * 10 ** (-3.5 / 20)    # keep the AAC render under -3 dBFS
    fade = np.minimum(1, (DUR - np.arange(len(mix)) / SR) / 1.0); mix *= fade[:, None]
    out = os.path.join(HERE, "sfx.wav")
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    print("wrote", out, len(ev), "events")

if __name__ == "__main__":
    main()
