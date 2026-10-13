"""Ms. Memories · one line — the sound score on onetake's palette: pen, paper, glass. One room, few events, a real rest."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from sfx_palette import Score, air, glass, wood, sub, bubble
import numpy as np
rng = np.random.default_rng(5)
s = Score(dur=15.0, T60=1.2); place = s.place
# 0.45–1.75 · the pen draws (soft hiss that follows the stroke), nothing else
place(air(1.3, 3200, 5200, 2.0, 0.5), 0.45, 0.10, -0.5, 0.25, pan_to=0.5)
# 1.75 · the line closes into a phone
place(wood(210, 0.10), 1.95, 0.20, 0.0, 0.25)
place(glass(659, 0.9, 0.6), 1.95, 0.14, 0.0, 0.45)                    # «ذكرياتك…»
for i in (0, 2, 4, 5): place(bubble(380 + 55 * i, 0.18), 2.47 + i * 0.10, 0.11, -0.2 + 0.08 * i, 0.3)   # photos land
place(glass(784, 0.9, 0.6), 2.87, 0.14, 0.0, 0.45)                    # «محفوظة في الهاتف»
# 4.0 · the phone opens into a book; the photos travel
place(air(0.6, 300, 2400, 1.2, 0.45), 4.0, 0.30, -0.2, 0.45, pan_to=0.2)
for t in (4.62, 4.78, 4.94): place(wood(200 + rng.uniform(-20, 20), 0.08), t, 0.11, rng.uniform(-0.3, 0.3), 0.25)
place(glass(587, 1.0, 0.5), 4.37, 0.14, 0.0, 0.5)                     # «كتاب يشبهك»
# 5.5 / 6.15 · two page turns
for t in (5.5, 6.15):
    place(air(0.45, 900, 3600, 1.0, 0.4), t, 0.30, 0.3, 0.4, pan_to=-0.3)
    place(wood(130, 0.07), t + 0.56, 0.16, -0.25, 0.3)
# 7.0 · the book becomes a QR; modules tick in, the scan sweeps, the frame becomes the video
place(air(0.5, 2400, 300, 1.3, 0.35), 7.0, 0.25, 0.0, 0.45)
for i, t in enumerate(np.linspace(7.45, 8.2, 7)): place(wood(240 + 18 * i, 0.05), t, 0.07, rng.uniform(-0.2, 0.2), 0.2)
place(glass(784, 0.9, 0.5), 7.72, 0.12, 0.0, 0.5)                     # «وفيديو يعيش بين صفحاته»
place(air(0.65, 400, 4200, 2.0, 0.75), 8.55, 0.22, 0.0, 0.45)
place(glass(1318, 1.3, 0.5), 9.15, 0.14, 0.0, 0.6)
place(bubble(520, 0.24), 9.47, 0.20, 0.0, 0.3)                        # play button opens
place(wood(240, 0.07), 9.95, 0.16, 0.0, 0.2)                          # play
# 10.3 · the video folds back into the line — then REST: no events from here until 12.0
place(air(0.7, 2200, 250, 1.2, 0.35), 10.3, 0.24, 0.0, 0.40)
# 12.0 · the line goes under the name, the name is written, the end
place(air(0.6, 300, 2200, 1.2, 0.5), 12.0, 0.22, 0.0, 0.45)
place(air(1.4, 3000, 5200, 2.0, 0.5), 12.55, 0.10, -0.4, 0.25, pan_to=0.4)
place(sub(55, 1.0), 13.95, 0.22, 0.0, 0.35)
place(glass(659, 1.6, 0.5), 13.97, 0.15, 0.0, 0.6); place(glass(988, 1.8, 0.4), 14.02, 0.12, 0.0, 0.6)
place(glass(1318, 2.0, 0.3), 14.35, 0.09, 0.0, 0.7)
s.write(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sfx.wav"))
