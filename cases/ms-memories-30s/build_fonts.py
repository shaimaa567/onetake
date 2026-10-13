#!/usr/bin/env python3
"""Inline the OFL faces the film sets (Reem Kufi for the Arabic lines, Cormorant Garamond for the Latin wordmark)
into fonts.css as data: URIs, so the file:// render gets real type. Faces come from the @fontsource npm packages:
  npm pack @fontsource/reem-kufi @fontsource/cormorant-garamond   (then untar; pass the folder as argv[1])
"""
import base64, sys, pathlib
src = pathlib.Path(sys.argv[1]); out = pathlib.Path(__file__).with_name("fonts.css")
ARABIC = "U+0600-06FF,U+200C-200E,U+2010-2011,U+204F,U+2E41,U+FB50-FDFF,U+FE80-FEFC"
LATIN = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
faces = [
  ("RK", "reem-kufi", "reem-kufi-arabic-600-normal.woff2", 600, "normal", ARABIC),
  ("RK", "reem-kufi", "reem-kufi-latin-600-normal.woff2", 600, "normal", LATIN),
  ("RK", "reem-kufi", "reem-kufi-arabic-500-normal.woff2", 500, "normal", ARABIC),
  ("RK", "reem-kufi", "reem-kufi-latin-500-normal.woff2", 500, "normal", LATIN),
  ("CG", "cormorant-garamond", "cormorant-garamond-latin-600-italic.woff2", 600, "italic", LATIN),
  ("CG", "cormorant-garamond", "cormorant-garamond-latin-500-normal.woff2", 500, "normal", LATIN),
]
css = []
for fam, pkg, fn, w, st, ur in faces:
    b = base64.b64encode((src / f"fontsource-{pkg}-5.3.0/package/files/{fn}").read_bytes()).decode()
    css.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};src:url(data:font/woff2;base64,{b}) format('woff2');unicode-range:{ur}}}")
out.write_text("\n".join(css)); print(out, out.stat().st_size // 1024, "KB")
