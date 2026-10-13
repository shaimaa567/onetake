"""Synthesizes the soundtrack (rising pad + plucks + synced SFX) from events.json.
Usage: python3 audio.py events.json out.wav
"""
import json, sys
import numpy as np

SR = 44100
ev = json.load(open(sys.argv[1]))
T = ev["T"]; END = T["end"]
N = int(END * SR)
rng = np.random.default_rng(5)
L = np.zeros(N); R = np.zeros(N)           # dry music + sfx bus
revL = np.zeros(N); revR = np.zeros(N)     # reverb send


def midi(n): return 440.0 * 2 ** ((n - 69) / 12)


def add(buf, sig, t0, gain=1.0):
    i = int(t0 * SR)
    if i >= N or i + len(sig) <= 0: return
    a = max(0, -i); b = min(len(sig), N - i)
    buf[i + a:i + b] += sig[a:b] * gain


def place(sig, t0, gain=1.0, pan=0.0, send=0.3):
    gl = gain * np.cos((pan + 1) * np.pi / 4); gr = gain * np.sin((pan + 1) * np.pi / 4)
    add(L, sig, t0, gl); add(R, sig, t0, gr)
    add(revL, sig, t0, gl * send); add(revR, sig, t0, gr * send)


def env_ad(n, a, d_tau):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d_tau)
    return e


def pluck(f, dur=1.4, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + .42 * bright * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 6) \
        + .18 * bright * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t * 9)
    return s * env_ad(n, .004, .38) * .5


def bell(f, dur=2.4):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d) for a, r, d in
            [(1, 1, 1.6), (.5, 2.76, 2.6), (.3, 5.4, 4.0), (.25, 1.5, 2.0)])
    return s * env_ad(n, .003, 10) * .35


def noise_band(dur, f0, f1):
    n = int(dur * SR); x = rng.standard_normal(n)
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(n, 1 / SR)
    m = np.clip((fr - f0) / max(f0 * .3, 50), 0, 1) * np.clip((f1 - fr) / max(f1 * .3, 50), 0, 1)
    return np.fft.irfft(X * m, n)


def whoosh(dur, f0=300, f1=5000, peak=.5, gain=.5, rev=True):
    n = int(dur * SR); t = np.arange(n) / SR / dur
    lo = noise_band(dur, f0, f0 * 3); hi = noise_band(dur, f1 * .4, f1)
    s = lo * (1 - t) + hi * t
    s /= np.max(np.abs(s)) + 1e-9
    e = np.where(t < peak, (t / peak) ** 2, ((1 - t) / (1 - peak)) ** 1.6)
    return s * e * gain


def click(f=2000, dur=.05):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) * .6 + rng.standard_normal(n) * .25) * np.exp(-t * 90) * .5


def thump(f0=130, f1=42, dur=.7):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 14)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 5) * 1.0


def sparkle(dur, density=60, lo=2500, hi=6500, gain=.2):
    out = np.zeros(int(dur * SR) + SR // 2)
    for _ in range(int(dur * density)):
        t0 = rng.random() * dur; f = rng.uniform(lo, hi)
        s = pluck(f, .35, .3) * (0.3 + .7 * (t0 / dur))
        i = int(t0 * SR); out[i:i + len(s)] += s[:len(out) - i] * gain
    return out


# ---------------- music pad ----------------
chords = [  # (start, end, midi notes)  A minor -> F -> C -> G -> F -> Am/C add9
    (0.0, 3.6, [45, 52, 57, 60, 64]),
    (3.3, 6.9, [41, 48, 53, 57, 60]),
    (6.6, 10.3, [48, 55, 60, 64, 67]),
    (10.0, 12.9, [43, 50, 55, 59, 62]),
    (12.6, 15.0, [41, 48, 53, 57, 60, 64]),
    (14.7, END + .6, [48, 55, 60, 64, 67, 71, 74]),
]
t_all = np.arange(N) / SR
pad = np.zeros(N)
for (a, b, notes) in chords:
    i0 = int(a * SR); i1 = min(N, int(b * SR)); n = i1 - i0
    if n <= 0: continue
    tt = np.arange(n) / SR; dur = b - a
    env = np.minimum(1, tt / 1.0) * np.minimum(1, (dur - tt) / 1.3).clip(0, 1)
    seg = np.zeros(n)
    for m in notes:
        f = midi(m)
        for det in (-.0045, .0, .0045):
            ff = f * (1 + det)
            seg += (np.sin(2 * np.pi * ff * tt) + .35 * np.sin(2 * np.pi * 2 * ff * tt) + .12 * np.sin(2 * np.pi * 3 * ff * tt)) * (1 / (1 + (m - 40) / 18))
    pad[i0:i1] += seg * env
pad /= np.max(np.abs(pad))
# slow swell: rising across the whole film
swell = .22 + .78 * np.clip(t_all / (T["s5"] + .3), 0, 1) ** 1.1
swell *= np.clip((END - t_all) / .7, 0, 1)
# tremolo-ish breathing
breath = 1 + .08 * np.sin(2 * np.pi * t_all / 3.0)
pad *= swell * breath * .5
L += pad * .95; R += pad * 1.0
revL += pad * .35; revR += pad * .35

# ---------------- plucked arpeggio (rhythm builds) ----------------
arp_chords = [(0.0, [57, 60, 64, 69]), (3.3, [53, 57, 60, 65]), (6.9, [55, 60, 64, 67]), (10.3, [55, 59, 62, 67]),
              (12.7, [53, 57, 60, 64]), (14.7, [60, 64, 67, 71, 74])]
def chord_at(t):
    c = arp_chords[0][1]
    for s, ch in arp_chords:
        if t >= s: c = ch
    return c

def arpeggio(t0, t1, step, gain, pat=(0, 1, 2, 3, 2, 1)):
    t = t0; k = 0
    while t < t1:
        ch = chord_at(t)
        m = ch[pat[k % len(pat)] % len(ch)] + 12
        place(pluck(midi(m), 1.2, .8), t, gain * (.8 + .2 * ((k % 3) == 0)), pan=np.sin(k * 1.3) * .5, send=.45)
        t += step; k += 1

arpeggio(3.4, 6.1, .3, .14)
arpeggio(6.9, 8.4, .6, .09, (0, 2, 1, 3))
arpeggio(10.4, 12.7, .3, .15)
arpeggio(12.7, 14.7, .15, .12)
arpeggio(15.0, 17.7, .3, .13, (0, 2, 4, 3, 2, 1))

# ---------------- SFX synced to the picture ----------------
# Scene 1: three word entrances
for t0, m in [(.15, 69), (1.2, 72), (2.25, 76)]:
    place(whoosh(.7, 250, 3500, .6, .22), t0 - .12, 1, pan=0, send=.3)
    place(pluck(midi(m), 1.6, 1), t0 + .12, .45, send=.5)
# bounce on the third word
for k, tt in enumerate([2.62, 2.8, 2.92]):
    place(thump(160, 70, .25), tt, .2 / (k + 1), send=.1)
# Scene 2: line in + wheel ticks (ascending pentatonic) + stop
place(whoosh(.6, 400, 4000, .6, .18), T["s2"] + .0, 1)
place(click(1500), T["s2"] + .4, .4)
scale = [69, 72, 74, 76, 79, 81, 84, 86, 88, 91, 93, 96, 98, 100]
for k, tk in enumerate(ev["ticks"]):
    f = midi(scale[min(k, len(scale) - 1)] - 12)
    place(click(2200 + 120 * k) * .6, tk, .5, pan=((k % 2) - .5) * .5, send=.2)
    place(pluck(f, .4, .5), tk, .12, send=.4)
t_stop = ev["SP1"]
place(thump(150, 45, 1.0), t_stop, .85, send=.3)
place(bell(midi(93), 2.6), t_stop, .5, send=.6)
place(bell(midi(88), 2.6), t_stop + .02, .3, send=.6)
# Scene 3: shimmer, morph riser, boom
place(whoosh(.9, 300, 3000, .5, .2), T["s3"] + .0, 1)
place(pluck(midi(69), 2, .6), T["s3"] + .15, .3, send=.6)
place(click(1800), T["s3"] + .6, .3)
place(click(2400), T["s3"] + 1.0, .3)
M0, M1 = ev["M0"], ev["M1"]
rise = whoosh(M1 - M0 + .1, 500, 9000, .92, .6)
place(rise, M0 - .05, 1, pan=0, send=.5)
place(sparkle(M1 - M0, 90, 2500, 7500, .22), M0, 1, pan=0, send=.6)
place(thump(120, 38, 1.4), M1, .95, send=.3)
place(bell(midi(88), 3), M1, .5, send=.7)
place(bell(midi(81), 3), M1 + .03, .35, send=.7)
# Scene 4: three word hits, gather, page flip, book
for k, tw_ in enumerate(ev["words4"]):
    place(whoosh(.45, 600, 4500, .6, .22), tw_ - .1, 1)
    place(click(1300 + 250 * k), tw_ + .1, .55)
    place(pluck(midi([72, 76, 79][k]), 1.5, 1), tw_ + .12, .42, send=.5)
G0 = ev["G0"]
place(whoosh(.85, 500, 6500, .7, .35), G0 - .1, 1)
place(whoosh(.55, 1800, 7000, .5, .3), G0 + .25, 1, pan=.2)  # page flip
place(click(900), G0 + .75, .4)
place(bell(midi(84), 2.4), G0 + .8, .4, send=.7)
place(sparkle(.8, 40, 3500, 8000, .15), G0 + .6, 1, send=.7)
place(whoosh(.5, 500, 3500, .6, .22), T["s4"] + 3.35, 1)
place(pluck(midi(76), 1.6, 1), T["s4"] + 3.5, .4, send=.6)
# Scene 5: wipe, logo write, tagline, handle
w0 = T["s5"]
place(whoosh(.8, 150, 4500, .55, .75), w0 - .05, 1, send=.4)
place(thump(110, 34, 1.8), w0 + .05, 1.0, send=.3)
place(bell(midi(72), 4), w0 + .75, .4, send=.8)
place(sparkle(1.15, 70, 3000, 8500, .2), w0 + .85, 1, send=.7)
place(whoosh(1.1, 800, 8000, .85, .3), w0 + .8, 1, send=.5)
place(bell(midi(84), 4), w0 + 1.95, .45, send=.8)
place(bell(midi(79), 4), w0 + 1.97, .3, send=.8)
place(pluck(midi(76), 1.8, 1), w0 + 2.05, .45, send=.6)
place(click(1600), w0 + 2.55, .5)
place(bell(midi(88), 3.5), w0 + 2.6, .35, send=.8)

# ---------------- reverb ----------------
def make_ir(seed, dur=2.2):
    g = np.random.default_rng(seed); n = int(dur * SR); t = np.arange(n) / SR
    ir = g.standard_normal(n) * np.exp(-t * 2.6)
    ir *= np.clip(t / .02, 0, 1)
    X = np.fft.rfft(ir); fr = np.fft.rfftfreq(n, 1 / SR)
    return np.fft.irfft(X * (1 / (1 + (fr / 4500) ** 2)), n)

def conv(x, ir):
    n = len(x) + len(ir)
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[:len(x)]

wetL = conv(revL, make_ir(1)); wetR = conv(revR, make_ir(2))
wetL /= np.max(np.abs(make_ir(1))) * 12; wetR /= np.max(np.abs(make_ir(2))) * 12
outL = L + wetL * .9; outR = R + wetR * .9

# fade in/out + normalize
fade = np.clip(t_all / .25, 0, 1) * np.clip((END - t_all) / .6, 0, 1)
outL *= fade; outR *= fade
peak = max(np.max(np.abs(outL)), np.max(np.abs(outR)))
outL *= .89 / peak; outR *= .89 / peak
import wave
pcm = (np.stack([outL, outR], 1) * 32767).astype('<i2')
with wave.open(sys.argv[2], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', END, 's')
