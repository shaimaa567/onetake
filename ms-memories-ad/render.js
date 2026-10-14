// Usage: node render.js stills out_dir t1 t2 ...   |   node render.js video out_dir [fps]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [mode, outDir, ...rest] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('console', m => console.log('[page]', m.text()));
  page.on('pageerror', e => console.log('[pageerror]', e.message));
  await page.goto('http://127.0.0.1:8765/ad.html');
  await page.evaluate(() => window.ready);
  const grab = async t => page.evaluate(t => { window.draw(t); return document.getElementById('c').toDataURL('image/jpeg', 0.95).split(',')[1]; }, t);
  if (mode === 'stills') {
    for (const t of rest.map(Number)) fs.writeFileSync(`${outDir}/s_${t.toFixed(2)}.jpg`, Buffer.from(await grab(t), 'base64'));
  } else {
    const fps = Number(rest[0] || 30), end = await page.evaluate(() => window.T.end), n = Math.round(end * fps);
    for (let i = 0; i < n; i++) {
      fs.writeFileSync(`${outDir}/f_${String(i).padStart(4, '0')}.jpg`, Buffer.from(await grab(i / fps), 'base64'));
      if (i % 60 === 0) console.log('frame', i, '/', n);
    }
    const ev = await page.evaluate(() => ({ T: window.T, ticks: window.tickTimes(), SP1: window.SP1, M0: window.M0, M1: window.M1, B2T: window.B2T, G0: window.G0, words4: window.WORDS4.map(w => w.t) }));
    fs.writeFileSync(`${outDir}/events.json`, JSON.stringify(ev));
  }
  await browser.close();
})();
