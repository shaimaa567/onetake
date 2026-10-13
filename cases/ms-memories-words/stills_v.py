import asyncio, io, os, sys
from PIL import Image, ImageDraw
from playwright.async_api import async_playwright
async def main(times, out, cols=6):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1080,"height":1920})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
        await pg.goto("file://"+os.path.abspath("comp.html")); await pg.evaluate("window.__ready")
        tiles=[]
        for t in times:
            await pg.evaluate(f"window.__seek({t})"); await pg.wait_for_timeout(30)
            im=Image.open(io.BytesIO(await pg.screenshot())).resize((360,640)); ImageDraw.Draw(im).text((6,6),f"t={t}",fill=(200,0,0)); tiles.append(im)
        await b.close()
    rows=(len(tiles)+cols-1)//cols; sh=Image.new("RGB",(360*cols,640*rows),(255,255,255))
    for i,im in enumerate(tiles): sh.paste(im,((i%cols)*360,(i//cols)*640))
    sh.save(out); print("wrote",out,"errors:",errs[:5] or "none")
ts=[float(x) for x in sys.argv[1].split(",")]; asyncio.run(main(ts, sys.argv[2], int(sys.argv[3]) if len(sys.argv)>3 else 6))
