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
s2, s3, s4, s5 = T["s2"], T["s3"], T["s4"], T["s5"]
chords = [  # A minor -> F -> C -> G -> F -> C add9
    (0.0, s2 + .3, [45, 52, 57, 60, 64]),
    (s2, s3 + .3, [41, 48, 53, 57, 60]),
    (s3, s4 + .3, [48, 55, 60, 64, 67]),
    (s4 - .3, s4 + 2.6, [43, 50, 55, 59, 62]),
    (s4 + 2.3, s5 + .3, [41, 48, 53, 57, 60, 64]),
    (s5, END + .6, [48, 55, 60, 64, 67, 71, 74]),
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
            seg += (np.sin(2 * np.pi * ff * tt) + .12 * np.sin(2 * np.pi * 2 * ff * tt)) * (1 / (1 + (m - 40) / 18))
    pad[i0:i1] += seg * env
pad /= np.max(np.abs(pad))
# slow swell: rising across the whole film
swell = .35 + .65 * np.clip(t_all / (T["s5"] + .3), 0, 1) ** 1.3
swell *= np.clip((END - t_all) / .7, 0, 1)
# tremolo-ish breathing
breath = 1 + .08 * np.sin(2 * np.pi * t_all / 3.0)
pad *= swell * breath * .55
L += pad * .95; R += pad * 1.0
revL += pad * .35; revR += pad * .35

# ---------------- plucked arpeggio (rhythm builds) ----------------
arp_chords = [(0.0, [57, 60, 64, 69]), (s2, [53, 57, 60, 65]), (s3, [55, 60, 64, 67]), (s4, [55, 59, 62, 67]),
              (s4 + 2.4, [53, 57, 60, 64]), (s5, [60, 64, 67, 71, 74])]
def chord_at(t):
    c = arp_chords[0][1]
    for s, ch in arp_chords:
        if t >= s: c = ch
    return c

def arpeggio(t0, t1, step, gain, pat=(0, 1, 2, 3, 2, 1)):
    t = t0; k = 0
    while t < t1:
        ch = chord_at(t)
        m = ch[pat[k % len(pat)] % len(ch)]
        place(pluck(midi(m), 1.6, .15), t, gain * (.8 + .2 * ((k % 3) == 0)), pan=np.sin(k * 1.3) * .5, send=.45)
        t += step; k += 1

arpeggio(s2 + .3, ev["SP1"], 1.2, .10, (0, 2, 1, 3))
arpeggio(s3 + 3.0, s4 - .3, 1.2, .08, (0, 2, 1, 3))
arpeggio(s4 + .3, s5, 1.2, .10, (0, 2, 1, 3))
arpeggio(s5 + .5, END - .5, 1.2, .10, (0, 2, 4, 3))

# ---------------- SFX synced to the picture ----------------
# Scene 1: three word entrances
for t0, m in [(.15, 69), (1.2, 72), (2.25, 76)]:
    place(whoosh(.9, 150, 900, .6, .10), t0 - .15, 1, pan=0, send=.3)
    place(pluck(midi(m - 12), 2.0, .1), t0 + .1, .30, send=.6)
# bounce on the third word
# Scene 2: line in + wheel ticks (ascending pentatonic) + stop
place(whoosh(.7, 150, 900, .6, .10), T["s2"] + .0, 1)
scale = [69, 72, 74, 76, 79, 81, 84, 86, 88, 91, 93, 96, 98, 100]
for k, tk in enumerate(ev["ticks"]):
    f = midi(scale[min(k, len(scale) - 1)] - 12)
    place(click(800 + 25 * k, .04) * .5, tk, .22, pan=((k % 2) - .5) * .4, send=.15)
t_stop = ev["SP1"]
place(thump(120, 45, 1.0), t_stop, .5, send=.3)
place(bell(midi(81), 2.6), t_stop, .22, send=.6)
# Scene 3: shimmer, morph riser, boom
place(whoosh(.9, 150, 900, .5, .10), T["s3"] + .0, 1)
M0, M1 = ev["M0"], ev["M1"]
rise = whoosh(M1 - M0 + .1, 200, 2800, .92, .30)
place(rise, M0 - .05, 1, pan=0, send=.5)
place(sparkle(M1 - M0, 14, 1500, 3500, .10), M0, 1, pan=0, send=.6)
place(thump(100, 38, 1.4), M1, .5, send=.3)
place(bell(midi(76), 3), M1, .25, send=.7)
# Scene 4: three word hits, gather, page flip, book
for k, tw_ in enumerate(ev["words4"]):
    place(whoosh(.6, 150, 900, .6, .09), tw_ - .1, 1)
    place(pluck(midi([60, 64, 67][k]), 1.8, .1), tw_ + .1, .30, send=.6)
G0 = ev["G0"]
place(whoosh(.85, 200, 1800, .7, .16), G0 - .1, 1)
place(whoosh(.5, 800, 3000, .5, .10), G0 + .25, 1, pan=.2)  # page flip
place(bell(midi(72), 2.4), G0 + .8, .22, send=.7)
place(pluck(midi(67), 1.8, .1), T["s4"] + 3.5, .28, send=.6)
# Scene 5: wipe, logo write, tagline, handle
w0 = T["s5"]
place(whoosh(.8, 120, 1600, .55, .30), w0 - .05, 1, send=.4)
place(thump(100, 34, 1.8), w0 + .05, .55, send=.3)
place(bell(midi(72), 4), w0 + .75, .22, send=.8)
place(sparkle(1.15, 12, 1500, 3500, .08), w0 + .85, 1, send=.7)
place(bell(midi(79), 4), w0 + 1.95, .22, send=.8)
place(pluck(midi(67), 2.0, .1), w0 + 2.05, .28, send=.6)

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
