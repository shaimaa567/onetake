# Ms. Memories — 30 s, 9:16, all digital illustration

Concept: **one memory object becomes the next.** A drawn phone full of drawn photos → the photos lift off and spiral into a
burgundy hardcover → the cover opens (Arabic book: spine on the right) and the leaves flip → the QR page is scanned by a
second drawn phone → the scan opens the *video* of the beach photo inside the phone → the book closes → wordmark.

Look: burgundy / ivory / soft gold. Reem Kufi for the Arabic lines, Cormorant Garamond italic for the wordmark (both OFL).
Nothing is a photograph or a bitmap: `art.js` draws every scene, the phone UI, the cover, the pages, the QR and the video.

| t (s) | beat | what carries into the next |
|---|---|---|
| 0–5 | phone with twelve illustrated photos, text 1 | the photos themselves lift off the screen |
| 5–9 | photos orbit, then spiral into one point, text 2 | the point is where the book appears; each arrival pulses the cover |
| 9–11.5 | closed book, cover swings open about the spine | the endpaper/title spread is the first page |
| 11.5–15.5 | four leaves flip (3-strip bend + shading), text 3 | the last spread holds the QR and the beach print |
| 15.5–20 | second phone enters, locks on the code, scans, text 4 | the scan opens a circular reveal on its own screen |
| 20–22.3 | the video plays in a phone that comes forward | the phone drops away, the book closes in reverse |
| 22.5–27 | leaves flip back, cover closes, text 5 | the closed book rises to make room |
| 27–30 | wordmark lands under the book | — |

Files: `comp.html` (the film, `window.__seek(t)`), `art.js`, `fonts.css` (built by `build_fonts.py`), `score.py` (music and
effects, synthesised; no voice), `shots.py` (full-frame stills).

Render: `python3 ../../scripts/render.py comp.html --out silent.mp4 --width 1080 --height 1920 --samples 4`, then
`python3 score.py` and mux (`ffmpeg … -af loudnorm=I=-16:TP=-3`).

The QR is an illustration and does not encode a URL; swap `QR_BITS` in `art.js` for a real code before publishing.
