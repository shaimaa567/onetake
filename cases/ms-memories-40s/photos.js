// Ms. Memories · procedural "photographs" — landscapes, celebrations, still lifes. No faces, deterministic, no image files.
// PHOTO.make(i) → 300×400 canvas for photo i (0..23). 14 scenes; 14+ are the same scenes re-seeded, flipped and re-graded.
(function () {
  const W = 300, H = 400;
  const mulberry = a => () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const lin = (c, y0, y1, stops, x0 = 0, x1 = 0) => { const g = c.createLinearGradient(x0, y0, x1, y1); stops.forEach(s => g.addColorStop(s[0], s[1])); return g; };
  const glow = (c, x, y, r, col, a = 1) => { const g = c.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, col.replace('A', a)); g.addColorStop(1, col.replace('A', 0)); c.fillStyle = g; c.fillRect(x - r, y - r, r * 2, r * 2); };
  const poly = (c, pts, fill) => { c.beginPath(); pts.forEach((p, i) => i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1])); c.closePath(); c.fillStyle = fill; c.fill(); };

  const S = [];
  S[0] = (c, r) => {                                                    // sunset beach
    const hz = H * 0.56; c.fillStyle = lin(c, 0, hz, [[0, '#2b2a5e'], [.38, '#c0476a'], [.75, '#ffb06b'], [1, '#ffe2a0']]); c.fillRect(0, 0, W, hz);
    glow(c, W * .55, hz - 4, 150, 'rgba(255,214,140,A)', .85); c.fillStyle = '#fff4cf'; c.beginPath(); c.arc(W * .55, hz - 8, 30, 0, 7); c.fill();
    c.fillStyle = lin(c, hz, H * .8, [[0, '#f0905c'], [1, '#4d3366']]); c.fillRect(0, hz, W, H * .24);
    for (let i = 0; i < 22; i++) { const y = hz + 4 + i * 4.5, w = 70 - i * 2 + r() * 20; c.fillStyle = `rgba(255,232,170,${.7 - i * .028})`; c.fillRect(W * .55 - w / 2 + (r() - .5) * 8, y, w, 1.6); }
    c.fillStyle = lin(c, H * .8, H, [[0, '#6b4638'], [1, '#2c1b24']]); c.beginPath(); c.moveTo(0, H * .8); c.quadraticCurveTo(W * .5, H * .76, W, H * .82); c.lineTo(W, H); c.lineTo(0, H); c.fill();
    c.strokeStyle = '#1c1118'; c.lineWidth = 5; c.beginPath(); c.moveTo(34, H); c.quadraticCurveTo(44, H * .66, 70, H * .52); c.stroke();
    c.lineWidth = 3; for (let k = 0; k < 7; k++) { const a = -2.6 + k * .62; c.beginPath(); c.moveTo(70, H * .52); c.quadraticCurveTo(70 + Math.cos(a) * 30, H * .52 + Math.sin(a) * 30 - 10, 70 + Math.cos(a) * 62, H * .52 + Math.sin(a) * 52 + 18); c.stroke(); }
  };
  S[1] = (c, r) => {                                                    // mountains over a lake
    c.fillStyle = lin(c, 0, H * .55, [[0, '#8fbfe6'], [1, '#f6e8d2']]); c.fillRect(0, 0, W, H * .55);
    const ridge = (base, amp, col, seed) => { const rr = mulberry(seed); const pts = [[0, H * .55]]; for (let x = 0; x <= W; x += 20) pts.push([x, base - amp * (0.4 + rr() * .6) * Math.abs(Math.sin(x / 55 + seed))]); pts.push([W, H * .55]); poly(c, pts, col); };
    ridge(H * .38, 90, '#8aa7c9', 3); ridge(H * .44, 80, '#56789f', 8); ridge(H * .5, 55, '#304f73', 5);
    c.fillStyle = lin(c, H * .55, H, [[0, '#7aaccc'], [1, '#2a5273']]); c.fillRect(0, H * .55, W, H * .45);
    c.save(); c.globalAlpha = .35; c.translate(0, H * 1.1); c.scale(1, -1); c.drawImage(c.canvas, 0, 0, W, H * .55, 0, 0, W, H * .55); c.restore();
    c.fillStyle = '#12261d'; for (let i = 0; i < 14; i++) { const x = r() * W, h = 36 + r() * 40, y = H - 6; poly(c, [[x, y - h], [x - 9, y], [x + 9, y]], '#12261d'); }
  };
  S[2] = (c, r) => {                                                    // city at night
    c.fillStyle = lin(c, 0, H * .72, [[0, '#0a0e2e'], [.6, '#3a2a5c'], [1, '#c26b6e']]); c.fillRect(0, 0, W, H);
    glow(c, W * .72, H * .16, 60, 'rgba(255,240,210,A)', .5); c.fillStyle = '#fff6df'; c.beginPath(); c.arc(W * .72, H * .16, 14, 0, 7); c.fill();
    for (let x = 0; x < W; x += 6 + r() * 20) { const w = 14 + r() * 22, h = 70 + r() * 170; c.fillStyle = '#0d1024'; c.fillRect(x, H * .8 - h, w, h + 30);
      for (let k = 0; k < h / 11; k++) for (let m = 0; m < w / 7; m++) if (r() > .55) { c.fillStyle = r() > .5 ? '#ffd783' : '#ffb26a'; c.fillRect(x + 3 + m * 7, H * .8 - h + 5 + k * 11, 3, 4); } }
    c.fillStyle = lin(c, H * .8, H, [[0, '#2a2347'], [1, '#0a0b1e']]); c.fillRect(0, H * .8, W, H * .2);
    for (let i = 0; i < 30; i++) { c.fillStyle = `rgba(255,200,120,${r() * .35})`; c.fillRect(r() * W, H * .81 + r() * 60, 2 + r() * 8, 1.5); }
  };
  S[3] = (c, r) => {                                                    // dunes, golden hour
    c.fillStyle = lin(c, 0, H, [[0, '#f5d29c'], [.5, '#fdeccc'], [1, '#f6c98c']]); c.fillRect(0, 0, W, H);
    glow(c, W * .3, H * .3, 110, 'rgba(255,250,225,A)', .9);
    const dune = (y0, a, col, ph) => { c.beginPath(); c.moveTo(0, H); for (let x = 0; x <= W; x += 6) c.lineTo(x, y0 - a * Math.sin(x / 70 + ph) - a * .4 * Math.sin(x / 31 + ph * 2)); c.lineTo(W, H); c.closePath(); c.fillStyle = col; c.fill(); };
    dune(H * .55, 26, '#e3a863', 1); dune(H * .68, 34, '#c98040', 2.4); dune(H * .84, 30, '#8e4f26', 4);
    c.strokeStyle = 'rgba(80,35,15,.35)'; c.lineWidth = 1.4; for (let i = 0; i < 20; i++) { const y = H * .88 + i * 4; c.beginPath(); c.moveTo(0, y); c.bezierCurveTo(80, y - 5, 200, y + 6, W, y - 2); c.stroke(); }
  };
  S[4] = (c, r) => {                                                    // flower field
    c.fillStyle = lin(c, 0, H * .5, [[0, '#9fd0f2'], [1, '#eaf4e0']]); c.fillRect(0, 0, W, H);
    glow(c, W * .8, H * .15, 90, 'rgba(255,255,220,A)', .8);
    const hill = (y0, a, col) => { c.beginPath(); c.moveTo(0, H); for (let x = 0; x <= W; x += 8) c.lineTo(x, y0 - a * Math.sin(x / 80 + y0)); c.lineTo(W, H); c.fillStyle = col; c.fill(); };
    hill(H * .52, 18, '#79ad5c'); hill(H * .62, 20, '#4f9040');
    const cols = ['#ff7aa8', '#ffd84a', '#ffffff', '#b98bff', '#ff9b5a'];
    for (let i = 0; i < 420; i++) { const y = H * .58 + Math.pow(r(), .7) * H * .42, s = 1.2 + (y - H * .58) / H * 7; c.fillStyle = cols[(r() * cols.length) | 0]; c.beginPath(); c.arc(r() * W, y, s, 0, 7); c.fill(); }
  };
  S[5] = (c, r) => {                                                    // graduation caps in the air
    c.fillStyle = lin(c, 0, H, [[0, '#3f86de'], [1, '#cbe6ff']]); c.fillRect(0, 0, W, H);
    for (let i = 0; i < 3; i++) glow(c, r() * W, r() * H * .5, 70, 'rgba(255,255,255,A)', .5);
    for (let i = 0; i < 8; i++) { const x = 30 + r() * 240, y = 40 + r() * 280, s = .8 + r() * .8, a = (r() - .5) * 1.1;
      c.save(); c.translate(x, y); c.rotate(a); c.scale(s, s); c.fillStyle = '#16181f'; c.beginPath(); c.ellipse(0, 6, 15, 7, 0, 0, 7); c.fill();
      poly(c, [[0, -13], [34, -2], [0, 9], [-34, -2]], '#1d2029'); c.strokeStyle = '#d9b44a'; c.lineWidth = 1.6; c.beginPath(); c.moveTo(0, -2); c.lineTo(26, 6); c.lineTo(26, 17); c.stroke(); c.fillStyle = '#d9b44a'; c.fillRect(24, 16, 4, 7); c.restore(); }
    const cc = ['#ff5a7a', '#ffd23f', '#ffffff', '#7ae0ff']; for (let i = 0; i < 90; i++) { c.save(); c.translate(r() * W, r() * H); c.rotate(r() * 6); c.fillStyle = cc[(r() * 4) | 0]; c.fillRect(0, 0, 4, 2); c.restore(); }
    c.fillStyle = '#2f6a3a'; c.fillRect(0, H * .92, W, H * .08);
  };
  S[6] = (c, r) => {                                                    // family table, from above
    c.fillStyle = '#6b3b22'; c.fillRect(0, 0, W, H); c.strokeStyle = 'rgba(30,12,6,.35)'; c.lineWidth = 1; for (let i = 0; i < 40; i++) { c.beginPath(); c.moveTo(0, i * 10 + r() * 6); c.bezierCurveTo(100, i * 10 + 8, 200, i * 10 - 6, W, i * 10 + r() * 6); c.stroke(); }
    c.fillStyle = '#f4ecdc'; c.fillRect(0, H * .3, W, H * .38);
    const plate = (x, y, rad, food) => { c.fillStyle = 'rgba(0,0,0,.25)'; c.beginPath(); c.arc(x + 4, y + 5, rad, 0, 7); c.fill(); c.fillStyle = '#fff'; c.beginPath(); c.arc(x, y, rad, 0, 7); c.fill(); c.strokeStyle = '#d8cfbd'; c.lineWidth = 2; c.beginPath(); c.arc(x, y, rad * .72, 0, 7); c.stroke();
      for (let k = 0; k < 5; k++) { c.fillStyle = food[k % food.length]; c.beginPath(); c.arc(x + (r() - .5) * rad, y + (r() - .5) * rad, 5 + r() * 8, 0, 7); c.fill(); } };
    plate(80, H * .38, 40, ['#d9533a', '#8cbf4a', '#f2c84b']); plate(220, H * .38, 40, ['#c6482c', '#f0d070']); plate(80, H * .58, 40, ['#8cbf4a', '#e08a3a']); plate(220, H * .58, 40, ['#f2c84b', '#c6482c', '#7a9f3a']); plate(150, H * .48, 28, ['#e9b44a']);
    for (let i = 0; i < 6; i++) { const x = 30 + i * 48, y = H * .72; c.fillStyle = 'rgba(255,255,255,.55)'; c.beginPath(); c.arc(x, y, 14, 0, 7); c.fill(); c.strokeStyle = 'rgba(255,255,255,.9)'; c.lineWidth = 2; c.stroke(); c.fillStyle = 'rgba(170,40,70,.6)'; c.beginPath(); c.arc(x, y, 8, 0, 7); c.fill(); }
    [[60, 40], [240, 50], [150, H - 40]].forEach(p => glow(c, p[0], p[1], 70, 'rgba(255,190,100,A)', .75));
  };
  S[7] = (c, r) => {                                                    // a road trip
    const hz = H * .52; c.fillStyle = lin(c, 0, hz, [[0, '#35418a'], [.5, '#e5708a'], [1, '#ffc27a']]); c.fillRect(0, 0, W, hz); glow(c, W * .5, hz, 130, 'rgba(255,225,160,A)', .8);
    c.fillStyle = '#2a2236'; c.fillRect(0, hz, W, H - hz); poly(c, [[W * .48, hz], [W * .52, hz], [W * 1.05, H], [-W * .05, H]], '#3b3347');
    for (let i = 0; i < 9; i++) { const k = i / 9, y = hz + 8 + k * k * (H - hz), w = 2 + k * 9; c.fillStyle = '#f7d98a'; c.fillRect(W / 2 - w / 2, y, w, 4 + k * 18); }
    poly(c, [[0, hz], [60, hz - 22], [130, hz - 6], [190, hz - 28], [260, hz - 8], [W, hz - 18], [W, hz], [0, hz]], '#2a1f3a');
    c.strokeStyle = '#1a1424'; c.lineWidth = 3; c.beginPath(); c.moveTo(30, hz + 40); c.lineTo(30, hz - 60); c.moveTo(14, hz - 46); c.lineTo(46, hz - 46); c.stroke();
  };
  S[8] = (c, r) => {                                                    // sailboat
    c.fillStyle = lin(c, 0, H * .45, [[0, '#cfeeff'], [1, '#f6fbff']]); c.fillRect(0, 0, W, H); c.fillStyle = lin(c, H * .45, H, [[0, '#76d6d6'], [1, '#17718f']]); c.fillRect(0, H * .45, W, H * .55);
    for (let i = 0; i < 40; i++) { c.fillStyle = `rgba(255,255,255,${.1 + r() * .35})`; c.fillRect(r() * W, H * .47 + r() * H * .5, 8 + r() * 24, 1.5); }
    poly(c, [[150, H * .12], [150, H * .56], [70, H * .56]], '#ffffff'); poly(c, [[158, H * .2], [158, H * .56], [228, H * .56]], '#fdf3e3'); poly(c, [[60, H * .58], [236, H * .58], [212, H * .64], [84, H * .64]], '#9e2b3a');
    c.fillStyle = 'rgba(255,255,255,.35)'; c.fillRect(70, H * .65, 150, 3);
  };
  S[9] = (c, r) => {                                                    // hot-air balloons
    c.fillStyle = lin(c, 0, H, [[0, '#76bff0'], [1, '#fcead2']]); c.fillRect(0, 0, W, H);
    for (let i = 0; i < 6; i++) { c.fillStyle = 'rgba(255,255,255,.7)'; c.beginPath(); c.ellipse(r() * W, H * .6 + r() * H * .35, 50 + r() * 30, 14 + r() * 8, 0, 0, 7); c.fill(); }
    const cols = ['#e34a5f', '#f4b73a', '#3f8fd9', '#7bc86c', '#c85ad8'];
    for (let i = 0; i < 5; i++) { const x = 50 + r() * 200, y = 70 + r() * 220, s = .6 + r() * .7; c.save(); c.translate(x, y); c.scale(s, s);
      c.fillStyle = cols[i % 5]; c.beginPath(); c.ellipse(0, 0, 30, 38, 0, 0, 7); c.fill(); c.fillStyle = 'rgba(255,255,255,.55)'; c.beginPath(); c.ellipse(0, 0, 11, 38, 0, 0, 7); c.fill();
      c.strokeStyle = '#4a2f1e'; c.lineWidth = 1; c.beginPath(); c.moveTo(-14, 34); c.lineTo(-7, 56); c.moveTo(14, 34); c.lineTo(7, 56); c.stroke(); c.fillStyle = '#6a4326'; c.fillRect(-9, 56, 18, 12); c.restore(); }
  };
  S[10] = (c, r) => {                                                   // lanterns
    c.fillStyle = lin(c, 0, H, [[0, '#080b28'], [1, '#2a1a45']]); c.fillRect(0, 0, W, H); for (let i = 0; i < 60; i++) { c.fillStyle = `rgba(255,255,255,${r() * .8})`; c.fillRect(r() * W, r() * H * .6, 1.4, 1.4); }
    for (let i = 0; i < 26; i++) { const x = r() * W, y = r() * H, s = .5 + r() * 1.3; glow(c, x, y, 34 * s, 'rgba(255,170,70,A)', .8); c.fillStyle = '#ffd08a'; c.beginPath(); c.roundRect ? c.roundRect(x - 7 * s, y - 9 * s, 14 * s, 18 * s, 4 * s) : c.rect(x - 7 * s, y - 9 * s, 14 * s, 18 * s); c.fill(); }
  };
  S[11] = (c, r) => {                                                   // old town street
    c.fillStyle = lin(c, 0, H * .3, [[0, '#18255a'], [1, '#e8a06a']]); c.fillRect(0, 0, W, H);
    const bld = (x, w, y, col) => { c.fillStyle = col; c.fillRect(x, y, w, H - y); for (let k = 0; k < (H - y) / 58; k++) for (let m = 0; m < w / 38; m++) { const wx = x + 8 + m * 38, wy = y + 14 + k * 58; c.fillStyle = r() > .4 ? '#ffd58a' : '#3b2a2a'; c.beginPath(); c.moveTo(wx, wy + 26); c.lineTo(wx, wy + 8); c.arc(wx + 10, wy + 8, 10, Math.PI, 0); c.lineTo(wx + 20, wy + 26); c.fill(); } };
    bld(0, 110, H * .22, '#b5603f'); bld(110, 90, H * .3, '#d3925a'); bld(200, 100, H * .18, '#9f4e38');
    for (let i = 0; i < 18; i++) { const x = i * 18, y = H * .46 + Math.sin(i * .9) * 10; glow(c, x, y, 18, 'rgba(255,214,120,A)', .9); }
    c.fillStyle = '#3a2823'; c.fillRect(0, H * .9, W, H * .1);
  };
  S[12] = (c, r) => {                                                   // a tower at dusk
    c.fillStyle = lin(c, 0, H, [[0, '#3a2f6e'], [.55, '#e0707e'], [1, '#ffcf8a']]); c.fillRect(0, 0, W, H);
    for (let i = 0; i < 7; i++) { c.fillStyle = 'rgba(255,255,255,.18)'; c.beginPath(); c.ellipse(r() * W, 40 + r() * 220, 60 + r() * 50, 12 + r() * 8, 0, 0, 7); c.fill(); }
    c.strokeStyle = '#1b1426'; c.fillStyle = '#1b1426'; poly(c, [[150, 50], [168, 220], [196, H * .86], [226, H * .86], [186, 250], [150, 120]], '#1b1426'); poly(c, [[150, 50], [132, 220], [104, H * .86], [74, H * .86], [114, 250], [150, 120]], '#1b1426');
    c.fillStyle = '#ffcf8a'; poly(c, [[134, 250], [166, 250], [172, 300], [128, 300]], '#ffcf8a'); c.fillStyle = '#1b1426'; c.fillRect(112, 232, 76, 10); c.fillRect(100, 300, 100, 8);
    c.fillStyle = '#17101f'; c.fillRect(0, H * .86, W, H * .14);
  };
  S[13] = (c, r) => {                                                   // a celebration
    c.fillStyle = lin(c, 0, H, [[0, '#35102a'], [1, '#a2345a']]); c.fillRect(0, 0, W, H);
    for (let i = 0; i < 40; i++) { glow(c, r() * W, r() * H * .65, 14 + r() * 28, `rgba(${r() > .5 ? '255,200,120' : '255,140,170'},A)`, .55); }
    c.fillStyle = '#f7e6d1'; c.fillRect(70, H * .66, 160, 70); c.fillStyle = '#ee7fa3'; c.fillRect(70, H * .66, 160, 18); c.fillStyle = '#f7e6d1'; c.fillRect(95, H * .52, 110, 60); c.fillStyle = '#ee7fa3'; c.fillRect(95, H * .52, 110, 14);
    for (let i = 0; i < 5; i++) { const x = 108 + i * 21; c.fillStyle = '#ffffff'; c.fillRect(x, H * .52 - 22, 4, 22); glow(c, x + 2, H * .52 - 28, 20, 'rgba(255,200,90,A)', .95); c.fillStyle = '#ffd76a'; c.beginPath(); c.ellipse(x + 2, H * .52 - 28, 3, 6, 0, 0, 7); c.fill(); }
    c.fillStyle = '#3a1020'; c.fillRect(0, H * .86, W, H * .14);
    const cc = ['#ffd23f', '#ff7aa8', '#7ae0ff', '#ffffff']; for (let i = 0; i < 100; i++) { c.save(); c.translate(r() * W, r() * H); c.rotate(r() * 6); c.fillStyle = cc[(r() * 4) | 0]; c.fillRect(0, 0, 4, 2); c.restore(); }
  };

  function make(i) {
    const cv = document.createElement('canvas'); cv.width = W; cv.height = H; const c = cv.getContext('2d'); const base = i % 14, r = mulberry(1000 + i * 77);
    if (i < 14) S[base](c, r);
    else { const t = document.createElement('canvas'); t.width = W; t.height = H; const tc = t.getContext('2d'); S[base](tc, r);
      c.save(); c.filter = `hue-rotate(${(i % 3 - 1) * 22}deg) saturate(${1.05 + (i % 2) * .15}) brightness(${.95 + (i % 4) * .03})`; c.translate(W, 0); c.scale(-1, 1); c.drawImage(t, 0, 0); c.restore(); }
    const rr = mulberry(i * 31 + 5); for (let k = 0; k < 1500; k++) { c.fillStyle = `rgba(${rr() > .5 ? '255,255,255' : '0,0,0'},${rr() * .07})`; c.fillRect(rr() * W, rr() * H, 1.3, 1.3); }
    const v = c.createRadialGradient(W / 2, H / 2, H * .3, W / 2, H / 2, H * .75); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(20,6,10,.34)'); c.fillStyle = v; c.fillRect(0, 0, W, H);
    c.fillStyle = 'rgba(255,196,140,.07)'; c.fillRect(0, 0, W, H);
    return cv;
  }
  window.PHOTO = { make, W, H, mulberry };
})();
