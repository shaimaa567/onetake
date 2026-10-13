"""Ms. Memories · words — the score on onetake's palette. Few events; hard cut at 8.78 is a felt hit; rest from 17.6."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from sfx_palette import Score, air, glass, wood, sub, bubble
import numpy as np
rng = np.random.default_rng(9)
s = Score(dur=18.0, T60=1.2); place = s.place
for t, f in ((0.30, 659), (0.95, 784), (1.55, 587)): place(glass(f, 0.8, 0.6), t, 0.10, 0.0, 0.45)          # the opening words
place(wood(210, 0.09), 2.88, 0.18, 0.0, 0.25)                                                                # «حوّل»
for i, t in enumerate((3.15, 3.51, 3.87, 4.23)): place(wood(200 + 22 * i, 0.07), t, 0.13, 0.0, 0.2)         # the roll, one tick a word
place(glass(988, 1.0, 0.5), 4.50, 0.13, 0.0, 0.5)                                                            # the last word lands
place(glass(659, 0.9, 0.6), 4.92, 0.11, 0.0, 0.45); place(glass(784, 0.9, 0.6), 5.62, 0.11, 0.0, 0.45)      # the sentence
place(air(0.7, 250, 2600, 1.2, 0.5), 6.55, 0.32, -0.2, 0.45, pan_to=0.2)                                    # the book arrives
place(sub(60, 0.7), 7.05, 0.28, 0.0, 0.3)
for t, f in ((7.35, 1046), (7.60, 1175), (7.85, 1318)): place(glass(f, 0.6, 0.7), t, 0.12, 0.0, 0.4)         # ticks
place(air(0.45, 300, 4200, 1.6, 0.9), 8.33, 0.40, 0.0, 0.3)                                                  # the dive
place(sub(48, 1.1), 8.78, 0.52, 0.0, 0.3)                                                                    # the cut
for i in range(5): place(bubble(420 + 35 * i, 0.18), 9.32 + i * 0.26, 0.11, -0.3 + 0.15 * i, 0.3)            # photos pulled in
place(wood(240, 0.07), 9.75, 0.2, 0.0, 0.2); place(wood(260, 0.07), 10.45, 0.2, 0.0, 0.2)
place(glass(784, 1.2, 0.5), 11.15, 0.15, 0.0, 0.6); place(glass(1175, 1.4, 0.4), 11.17, 0.11, 0.0, 0.6)    # ✓ ready
for t in (11.4, 11.7, 12.0): place(air(0.5, 300, 2400, 1.2, 0.5), t - 0.05, 0.18, 0.0, 0.4)                  # the books rise
place(sub(55, 0.8), 11.95, 0.2, 0.0, 0.3)
place(air(0.6, 250, 3000, 1.3, 0.7), 13.15, 0.30, 0.0, 0.45); place(sub(45, 1.0), 13.78, 0.30, 0.0, 0.35)  # the fill, the iris
place(air(1.0, 3000, 5200, 2.0, 0.5), 14.2, 0.10, -0.4, 0.25, pan_to=0.4)                                   # the name is written
place(glass(988, 1.8, 0.4), 15.02, 0.12, 0.0, 0.6); place(glass(1318, 2.0, 0.3), 15.5, 0.08, 0.0, 0.6)   # «كل ذكرى تستحق أن تبقى»
place(wood(220, 0.08), 16.47, 0.22, 0.0, 0.2); place(bubble(520, 0.2), 16.5, 0.12, 0.0, 0.3)               # the button
for i in range(10): place(wood(260 + rng.uniform(-20, 20), 0.04), 16.97 + i * 0.062, 0.06, 0.0, 0.15)      # the handle, typed
s.write(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sfx.wav"))
