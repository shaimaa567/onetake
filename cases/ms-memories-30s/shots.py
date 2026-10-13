#!/usr/bin/env python3
"""shots.py comp.html t1,t2,… outdir — one full-frame PNG per time (the contact sheet in stills.py crops to 16:9)."""
import asyncio, sys, os
from playwright.async_api import async_playwright
async def main(comp, times, out):
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        br = await p.chromium.launch(args=["--force-color-profile=srgb"]); pg = await (await br.new_context(viewport={"width":1080,"height":1920})).new_page()
        logs=[]; pg.on("pageerror", lambda e: logs.append(str(e))); pg.on("console", lambda m: logs.append(m.text) if m.type=="error" else None)
        await pg.goto("file://"+os.path.abspath(comp)); await pg.evaluate("window.__ready")
        for t in times:
            await pg.evaluate(f"window.__seek({t})"); await pg.screenshot(path=f"{out}/t{t:05.2f}.png")
        print("errors:", logs or "none"); await br.close()
asyncio.run(main(sys.argv[1], [float(x) for x in sys.argv[2].split(",")], sys.argv[3]))
