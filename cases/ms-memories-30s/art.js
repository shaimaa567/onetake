/* Ms. Memories · art.js — every picture in the film is drawn here, with canvas paths and gradients. No photographs,
 * no bitmaps: memories, phone UI, book cover, pages, QR code and the "video" are all digital illustration.
 * Each scene draws in a 300×400 unit space and is scaled to whatever canvas it is given. Pure functions: same
 * arguments, same picture (OM.rng for anything that looks random). */
(function (root) {
  'use strict';
  const P = {
    w0: '#22050f', w1: '#3f0b1c', w2: '#5e1229', w3: '#7f1d38', w4: '#a2334f',
    rose: '#c9677a', blush: '#e7a39f', peach: '#f4c7a1', sand: '#ead2ac',
    ivory: '#f7ecda', cream: '#fff7e8',
    g0: '#9a6a26', g1: '#c99a4b', g2: '#e9c982', g3: '#fbeabf',
  };
  const TAU = Math.PI * 2;

  function rr(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
  function lg(c, x0, y0, x1, y1, stops) { const g = c.createLinearGradient(x0, y0, x1, y1); stops.forEach(([o, col]) => g.addColorStop(o, col)); return g; }
  function rg(c, x, y, r0, r1, stops) { const g = c.createRadialGradient(x, y, r0, x, y, r1); stops.forEach(([o, col]) => g.addColorStop(o, col)); return g; }
  function glow(c, x, y, r, col, a = 1) { c.save(); c.globalAlpha = a; c.fillStyle = rg(c, x, y, 0, r, [[0, col], [1, 'rgba(0,0,0,0)']]); c.fillRect(x - r, y - r, r * 2, r * 2); c.restore(); }
  function blob(c, x, y, rx, ry, fill) { c.beginPath(); c.ellipse(x, y, rx, ry, 0, 0, TAU); c.fillStyle = fill; c.fill(); }

  // A little person, drawn as a rounded silhouette with a head. (x, y) is the feet; h the height.
  function person(c, x, y, h, body, skin, { dress = false, arm = 0, hair = P.w0 } = {}) {
    const hw = h * 0.17;
    c.fillStyle = body;
    c.beginPath();
    if (dress) { c.moveTo(x - hw * 0.8, y - h * 0.62); c.quadraticCurveTo(x - hw * 2.0, y - h * 0.1, x - hw * 2.3, y); c.lineTo(x + hw * 2.3, y); c.quadraticCurveTo(x + hw * 2.0, y - h * 0.1, x + hw * 0.8, y - h * 0.62); }
    else { c.moveTo(x - hw, y - h * 0.62); c.lineTo(x - hw * 0.9, y); c.lineTo(x - hw * 0.1, y); c.lineTo(x, y - h * 0.3); c.lineTo(x + hw * 0.1, y); c.lineTo(x + hw * 0.9, y); c.lineTo(x + hw, y - h * 0.62); }
    c.closePath(); c.fill();
    rr(c, x - hw * 1.05, y - h * 0.84, hw * 2.1, h * 0.28, hw * 0.9); c.fill();                 // shoulders / torso
    c.save(); c.translate(x + hw * 0.9, y - h * 0.78); c.rotate(-arm); c.fillRect(0, -hw * 0.28, h * 0.3, hw * 0.55); c.restore();   // raised arm
    blob(c, x, y - h * 0.92, hw * 0.78, hw * 0.88, skin);
    c.fillStyle = hair; c.beginPath(); c.ellipse(x, y - h * 0.95, hw * 0.82, hw * 0.78, 0, Math.PI, TAU); c.fill();
  }

  function sunDisc(c, x, y, r) { glow(c, x, y, r * 4, 'rgba(255,226,170,.55)'); c.beginPath(); c.arc(x, y, r, 0, TAU); c.fillStyle = lg(c, x, y - r, x, y + r, [[0, P.g3], [1, P.peach]]); c.fill(); }
  function stars(c, n, seed, y0, y1, w = 300) { const R = root.OM.rng(seed); for (let i = 0; i < n; i++) { const x = R() * w, y = y0 + R() * (y1 - y0), r = 0.6 + R() * 1.3; c.globalAlpha = 0.5 + R() * 0.5; c.fillStyle = P.g3; c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill(); } c.globalAlpha = 1; }
  function hills(c, y, amp, col, seed, w = 300, h = 400, k = 0.012) { const R = root.OM.rng(seed), a = R() * 6, b = R() * 6; c.beginPath(); c.moveTo(0, h); for (let x = 0; x <= w; x += 6) c.lineTo(x, y - Math.sin(x * k + a) * amp - Math.sin(x * k * 2.3 + b) * amp * 0.4); c.lineTo(w, h); c.closePath(); c.fillStyle = col; c.fill(); }

  const SCENES = [
    // 0 · beach sunset, a couple holding hands
    (c) => {
      c.fillStyle = lg(c, 0, 0, 0, 400, [[0, P.w3], [0.35, P.rose], [0.6, P.peach], [0.64, P.g2], [0.64, P.w3], [1, P.w1]]); c.fillRect(0, 0, 300, 400);
      sunDisc(c, 150, 232, 46);
      c.fillStyle = lg(c, 0, 250, 0, 330, [[0, 'rgba(255,214,150,.0)'], [1, 'rgba(0,0,0,0)']]);
      for (let i = 0; i < 9; i++) { c.fillStyle = `rgba(255,226,170,${0.55 - i * 0.05})`; rr(c, 150 - (36 - i * 3), 252 + i * 8, (36 - i * 3) * 2, 2.4, 1.2); c.fill(); }
      hills(c, 318, 6, P.w2, 11); hills(c, 345, 5, '#e2b98a', 12);
      c.fillStyle = '#d4a574'; c.fillRect(0, 352, 300, 48);
      person(c, 128, 352, 92, P.w0, '#3a1117', { dress: false }); person(c, 164, 352, 84, P.w0, '#3a1117', { dress: true });
      c.strokeStyle = P.w0; c.lineWidth = 4; c.beginPath(); c.moveTo(138, 308); c.lineTo(152, 312); c.stroke();
      c.fillStyle = 'rgba(255,240,210,.18)'; c.beginPath(); c.arc(60, 66, 26, 0, TAU); c.fill();
    },
    // 1 · birthday cake in warm candlelight
    (c) => {
      c.fillStyle = lg(c, 0, 0, 0, 400, [[0, P.w1], [1, P.w3]]); c.fillRect(0, 0, 300, 400);
      const R = root.OM.rng(5); for (let i = 0; i < 16; i++) glow(c, R() * 300, 30 + R() * 190, 14 + R() * 26, i % 2 ? 'rgba(244,199,161,.5)' : 'rgba(201,103,122,.5)', 0.8);
      c.strokeStyle = P.g2; c.lineWidth = 1.6; c.beginPath(); c.moveTo(-10, 34); c.quadraticCurveTo(150, 82, 310, 30); c.stroke();
      for (let i = 0; i < 7; i++) { const x = 20 + i * 43, y = 34 + Math.sin((i / 6) * Math.PI) * 38 + 14; c.fillStyle = [P.blush, P.g2, P.rose][i % 3]; c.beginPath(); c.moveTo(x, y); c.lineTo(x + 11, y + 26); c.lineTo(x - 11, y + 26); c.closePath(); c.fill(); }
      c.fillStyle = lg(c, 0, 296, 0, 400, [[0, P.w2], [1, P.w0]]); c.fillRect(0, 296, 300, 104);
      blob(c, 150, 302, 104, 16, 'rgba(0,0,0,.35)');
      c.fillStyle = P.ivory; rr(c, 86, 238, 128, 64, 10); c.fill();
      c.fillStyle = lg(c, 0, 0, 0, 1, [[0, P.blush], [1, P.blush]]); rr(c, 86, 238, 128, 16, 8); c.fill();
      c.fillStyle = P.rose; rr(c, 108, 192, 84, 48, 10); c.fill(); c.fillStyle = P.g2; rr(c, 108, 192, 84, 11, 6); c.fill();
      c.fillStyle = P.g2; for (let i = 0; i < 6; i++) { c.beginPath(); c.arc(98 + i * 21, 262, 5, 0, TAU); c.fill(); }
      for (let i = 0; i < 3; i++) { const x = 126 + i * 24; c.fillStyle = P.cream; c.fillRect(x - 2, 164, 4, 30); glow(c, x, 156, 34, 'rgba(255,205,120,.9)'); c.fillStyle = '#ffd58a'; c.beginPath(); c.ellipse(x, 156, 4, 9, 0, 0, TAU); c.fill(); }
      c.strokeStyle = P.cream; c.lineWidth = 1.2; [[236, 120, P.blush], [256, 150, P.g2], [48, 130, P.rose]].forEach(([x, y, col]) => { c.beginPath(); c.moveTo(x, y + 26); c.quadraticCurveTo(x - 8, y + 90, 150, 232); c.stroke(); blob(c, x, y, 17, 21, col); glow(c, x - 6, y - 8, 12, 'rgba(255,255,255,.55)'); });
    },
    // 2 · road trip at golden hour
    (c) => {
      c.fillStyle = lg(c, 0, 0, 0, 400, [[0, P.w2], [0.4, P.blush], [0.62, P.peach], [0.62, P.w2], [1, P.w1]]); c.fillRect(0, 0, 300, 400);
      sunDisc(c, 205, 196, 38); hills(c, 236, 22, P.w3, 21); hills(c, 258, 16, P.w2, 22); hills(c, 282, 10, P.w1, 23);
      c.fillStyle = '#45172a'; c.beginPath(); c.moveTo(150, 270); c.lineTo(110, 400); c.lineTo(230, 400); c.closePath(); c.fill();
      c.strokeStyle = P.g2; c.lineWidth = 3; c.setLineDash([10, 12]); c.beginPath(); c.moveTo(150, 274); c.lineTo(168, 400); c.stroke(); c.setLineDash([]);
      c.fillStyle = P.w0; rr(c, 142, 322, 62, 22, 8); c.fill(); rr(c, 154, 308, 38, 20, 8); c.fill(); c.fillStyle = P.g2; c.fillRect(160, 313, 26, 9);
      blob(c, 156, 346, 8, 8, '#000'); blob(c, 194, 346, 8, 8, '#000'); glow(c, 140, 334, 22, 'rgba(255,220,150,.8)');
    },
    // 3 · family dinner under lanterns
    (c) => {
      c.fillStyle = lg(c, 0, 0, 0, 400, [[0, P.w0], [1, P.w2]]); c.fillRect(0, 0, 300, 400);
      [[60, 70, 30], [150, 40, 36], [240, 78, 28]].forEach(([x, y, r]) => { c.strokeStyle = P.g1; c.lineWidth = 1.5; c.beginPath(); c.moveTo(x, 0); c.lineTo(x, y - r); c.stroke(); glow(c, x, y, r * 3.4, 'rgba(255,196,110,.75)'); c.fillStyle = lg(c, x - r, y, x + r, y, [[0, P.g1], [0.5, P.g3], [1, P.g1]]); c.beginPath(); c.ellipse(x, y, r * 0.62, r, 0, 0, TAU); c.fill(); c.strokeStyle = P.g0; c.lineWidth = 1.4; for (let k = -1; k <= 1; k++) { c.beginPath(); c.ellipse(x, y, r * 0.62 * Math.abs(k) * 0.9 + 0.1, r, 0, 0, TAU); c.stroke(); } });
      const faces = [[58, '#d9a07c'], [118, '#e3b293'], [182, '#c98f6c'], [242, '#e3b293']];
      faces.forEach(([x, col], i) => { c.fillStyle = [P.w4, P.rose, P.w3, P.blush][i]; rr(c, x - 28, 238 + (i % 2) * 6, 56, 80, 22); c.fill(); blob(c, x, 216 + (i % 2) * 6, 17, 19, col); c.fillStyle = P.w0; c.beginPath(); c.ellipse(x, 211 + (i % 2) * 6, 18, 14, 0, Math.PI, TAU); c.fill(); });
      c.fillStyle = lg(c, 0, 296, 0, 400, [[0, P.ivory], [1, P.sand]]); rr(c, -10, 296, 320, 120, 4); c.fill();
      c.fillStyle = P.rose; blob(c, 88, 330, 34, 9, P.cream); blob(c, 210, 334, 34, 9, P.cream); blob(c, 88, 328, 18, 4, P.g2); blob(c, 210, 332, 18, 4, P.g2);
      glow(c, 150, 290, 90, 'rgba(255,190,110,.35)');
    },
    // 4 · wedding arch
    (c) => {
      c.fillStyle = lg(c, 0, 0, 0, 400, [[0, P.blush], [0.7, P.cream], [1, P.sand]]); c.fillRect(0, 0, 300, 400);
      glow(c, 150, 170, 190, 'rgba(255,240,215,.9)');
      c.strokeStyle = P.g1; c.lineWidth = 6; c.beginPath(); c.moveTo(60, 380); c.lineTo(60, 160); c.arc(150, 160, 90, Math.PI, 0); c.lineTo(240, 380); c.stroke();
      const R = root.OM.rng(8); for (let i = 0; i < 44; i++) { const a = Math.PI + R() * Math.PI, x = 150 + Math.cos(a) * 90 + (R() - 0.5) * 18, y = 160 + Math.sin(a) * 90 + (R() - 0.5) * 18; blob(c, x, y, 7 + R() * 7, 7 + R() * 7, [P.rose, P.blush, P.w4, P.ivory][i % 4]); }
      for (let i = 0; i < 12; i++) { const y = 160 + R() * 200, s = i % 2 ? 60 : 240; blob(c, s + (R() - 0.5) * 12, y, 7 + R() * 5, 7 + R() * 5, [P.rose, P.blush, P.ivory][i % 3]); }
      c.fillStyle = '#e4cfa8'; c.fillRect(0, 352, 300, 48);
      person(c, 126, 360, 130, P.w1, '#c98f6c'); person(c, 176, 360, 120, P.ivory, '#c98f6c', { dress: true, hair: P.w1 });
      c.fillStyle = 'rgba(255,255,255,.55)'; c.beginPath(); c.moveTo(176, 262); c.quadraticCurveTo(210, 300, 226, 360); c.lineTo(214, 360); c.quadraticCurveTo(196, 306, 176, 270); c.fill();
    },
    // 5 · a child, a kite, a hill
    (c) => {
      c.fillStyle = lg(c, 0, 0, 0, 400, [[0, P.rose], [0.55, P.peach], [1, P.sand]]); c.fillRect(0, 0, 300, 400);
      sunDisc(c, 70, 90, 26); hills(c, 300, 28, '#b5626d', 31, 300, 400, 0.01); hills(c, 330, 18, P.w3, 32, 300, 400, 0.013);
      person(c, 110, 346, 82, P.g1, '#e0a681', { arm: 0.9, hair: P.w1 });
      c.strokeStyle = P.cream; c.lineWidth = 1.3; c.beginPath(); c.moveTo(138, 300); c.quadraticCurveTo(190, 240, 214, 130); c.stroke();
      c.save(); c.translate(214, 108); c.rotate(0.35); c.fillStyle = P.w3; c.beginPath(); c.moveTo(0, -42); c.lineTo(26, 0); c.lineTo(0, 44); c.lineTo(-26, 0); c.closePath(); c.fill();
      c.fillStyle = P.g2; c.beginPath(); c.moveTo(0, -42); c.lineTo(26, 0); c.lineTo(0, 0); c.closePath(); c.fill(); c.fillStyle = P.blush; c.beginPath(); c.moveTo(0, 44); c.lineTo(-26, 0); c.lineTo(0, 0); c.closePath(); c.fill();
      c.strokeStyle = P.cream; c.lineWidth = 1.2; c.beginPath(); c.moveTo(0, 44); for (let i = 1; i <= 6; i++) c.lineTo(Math.sin(i * 1.4) * 9, 44 + i * 13); c.stroke(); c.restore();
    },
    // 6 · night city, crescent and lantern
    (c) => {
      c.fillStyle = lg(c, 0, 0, 0, 400, [[0, P.w0], [0.7, P.w2], [1, P.w3]]); c.fillRect(0, 0, 300, 400);
      stars(c, 36, 61, 0, 200); glow(c, 214, 78, 70, 'rgba(255,226,170,.5)');
      c.fillStyle = P.g3; c.beginPath(); c.arc(214, 78, 30, 0, TAU); c.fill(); c.globalCompositeOperation = 'destination-out'; c.beginPath(); c.arc(228, 70, 27, 0, TAU); c.fill(); c.globalCompositeOperation = 'source-over';
      const R = root.OM.rng(62); let x = -6;
      while (x < 300) { const w = 26 + R() * 30, h = 70 + R() * 130; c.fillStyle = lg(c, 0, 400 - h, 0, 400, [[0, P.w1], [1, P.w0]]); c.fillRect(x, 400 - h, w, h); if (R() > 0.55) { c.beginPath(); c.arc(x + w / 2, 400 - h, w / 2.4, Math.PI, 0); c.fill(); } for (let wy = 400 - h + 12; wy < 392; wy += 15) for (let wx = x + 6; wx < x + w - 6; wx += 11) if (R() > 0.5) { c.fillStyle = R() > 0.3 ? P.g2 : P.blush; c.globalAlpha = 0.8; c.fillRect(wx, wy, 5, 7); c.globalAlpha = 1; } x += w + 2; }
      c.strokeStyle = P.g1; c.lineWidth = 1.4; c.beginPath(); c.moveTo(70, 0); c.lineTo(70, 122); c.stroke(); glow(c, 70, 148, 52, 'rgba(255,196,110,.7)');
      c.fillStyle = lg(c, 54, 0, 86, 0, [[0, P.g1], [0.5, P.g3], [1, P.g1]]); rr(c, 54, 124, 32, 48, 12); c.fill();
    },
    // 7 · garden, flowers and a butterfly
    (c) => {
      c.fillStyle = lg(c, 0, 0, 0, 400, [[0, P.blush], [0.5, P.cream], [1, P.sand]]); c.fillRect(0, 0, 300, 400);
      hills(c, 300, 20, '#8b3a4c', 71, 300, 400, 0.011);
      const R = root.OM.rng(72); const fl = [[70, 220, 38, P.rose], [160, 150, 46, P.w4], [236, 236, 34, P.g2], [112, 296, 30, P.blush], [226, 130, 26, P.rose]];
      fl.forEach(([x, y, r, col]) => { c.strokeStyle = '#6a2a39'; c.lineWidth = 3; c.beginPath(); c.moveTo(x, y); c.quadraticCurveTo(x + 8, y + 70, x - 4, 400); c.stroke(); for (let i = 0; i < 8; i++) { const a = (i / 8) * TAU; blob(c, x + Math.cos(a) * r * 0.55, y + Math.sin(a) * r * 0.55, r * 0.42, r * 0.3, col); } blob(c, x, y, r * 0.26, r * 0.26, P.g2); });
      c.save(); c.translate(76, 86); c.rotate(-0.3); [[-1, P.g2], [1, P.g2]].forEach(([s, col]) => { c.fillStyle = col; c.beginPath(); c.ellipse(s * 16, -6, 16, 22, s * 0.5, 0, TAU); c.fill(); c.fillStyle = P.w3; c.beginPath(); c.ellipse(s * 13, 12, 10, 14, -s * 0.4, 0, TAU); c.fill(); }); c.fillStyle = P.w0; rr(c, -2, -14, 4, 34, 2); c.fill(); c.restore();
    },
    // 8 · desert night, tent and fire
    (c) => {
      c.fillStyle = lg(c, 0, 0, 0, 400, [[0, P.w0], [0.55, P.w2], [0.8, P.rose]]); c.fillRect(0, 0, 300, 400);
      stars(c, 70, 81, 0, 220); hills(c, 270, 28, '#7c2a3f', 82, 300, 400, 0.009); hills(c, 316, 22, '#4c1226', 83, 300, 400, 0.012); hills(c, 360, 14, P.w1, 84);
      c.fillStyle = P.sand; c.beginPath(); c.moveTo(70, 340); c.lineTo(112, 282); c.lineTo(154, 340); c.closePath(); c.fill(); c.fillStyle = P.w0; c.beginPath(); c.moveTo(112, 282); c.lineTo(100, 340); c.lineTo(124, 340); c.closePath(); c.fill();
      glow(c, 214, 338, 70, 'rgba(255,170,80,.8)'); c.fillStyle = '#ffd08a'; c.beginPath(); c.moveTo(214, 312); c.quadraticCurveTo(230, 332, 222, 346); c.lineTo(206, 346); c.quadraticCurveTo(198, 332, 214, 312); c.fill();
    },
    // 9 · mountains and a climber
    (c) => {
      c.fillStyle = lg(c, 0, 0, 0, 400, [[0, P.w3], [0.45, P.rose], [0.7, P.peach], [1, P.cream]]); c.fillRect(0, 0, 300, 400);
      sunDisc(c, 220, 160, 30);
      [[110, 330, '#a85163'], [60, 300, '#8d3a4e'], [190, 280, '#6f2740']].forEach(([x, h, col], i) => { c.fillStyle = col; c.beginPath(); c.moveTo(x - 190 + i * 20, 400); c.lineTo(x, 400 - h); c.lineTo(x + 190 - i * 20, 400); c.closePath(); c.fill(); c.fillStyle = 'rgba(255,240,220,.78)'; c.beginPath(); c.moveTo(x, 400 - h); c.lineTo(x + 36, 400 - h + 62); c.lineTo(x + 12, 400 - h + 52); c.lineTo(x, 400 - h + 74); c.lineTo(x - 18, 400 - h + 54); c.lineTo(x - 36, 400 - h + 62); c.closePath(); c.fill(); });
      c.fillStyle = P.w1; c.fillRect(0, 372, 300, 28); person(c, 98, 372, 56, P.w0, '#3a1117', { arm: 1.1 });
    },
    // 10 · a boat on a rose sea
    (c) => {
      c.fillStyle = lg(c, 0, 0, 0, 400, [[0, P.w2], [0.3, P.blush], [0.5, P.cream], [0.5, P.rose], [1, P.w2]]); c.fillRect(0, 0, 300, 400);
      sunDisc(c, 150, 178, 40);
      for (let i = 0; i < 14; i++) { c.strokeStyle = `rgba(255,240,210,${0.6 - i * 0.03})`; c.lineWidth = 1.6; c.beginPath(); const y = 206 + i * 14; for (let x = 0; x <= 300; x += 8) c.lineTo(x, y + Math.sin(x * 0.07 + i) * (1 + i * 0.25)); c.stroke(); }
      c.fillStyle = P.w0; c.beginPath(); c.moveTo(96, 292); c.lineTo(214, 292); c.lineTo(194, 318); c.lineTo(116, 318); c.closePath(); c.fill(); c.fillRect(154, 214, 3, 80);
      c.fillStyle = P.ivory; c.beginPath(); c.moveTo(150, 218); c.lineTo(150, 286); c.lineTo(104, 286); c.closePath(); c.fill(); c.fillStyle = P.blush; c.beginPath(); c.moveTo(160, 226); c.lineTo(160, 286); c.lineTo(198, 286); c.closePath(); c.fill();
    },
    // 11 · a laughing portrait among flowers
    (c) => {
      c.fillStyle = lg(c, 0, 0, 0, 400, [[0, P.w3], [1, P.w1]]); c.fillRect(0, 0, 300, 400); glow(c, 150, 170, 190, 'rgba(244,199,161,.55)');
      const R = root.OM.rng(111); for (let i = 0; i < 18; i++) { const a = R() * TAU, d = 120 + R() * 70, x = 150 + Math.cos(a) * d, y = 190 + Math.sin(a) * d * 1.1; blob(c, x, y, 16 + R() * 14, 14 + R() * 10, [P.rose, P.blush, P.g2, P.w4][i % 4]); }
      c.fillStyle = P.ivory; rr(c, 84, 262, 132, 150, 50); c.fill(); c.fillStyle = P.g1; rr(c, 130, 250, 40, 24, 8); c.fill();
      c.fillStyle = '#ddb08e'; c.beginPath(); c.ellipse(150, 196, 58, 66, 0, 0, TAU); c.fill();
      c.fillStyle = P.w0; c.beginPath(); c.ellipse(150, 176, 66, 62, 0, Math.PI * 0.95, Math.PI * 2.05); c.fill(); rr(c, 86, 170, 22, 90, 10); c.fill(); rr(c, 192, 170, 22, 90, 10); c.fill();
      c.fillStyle = P.w0; c.beginPath(); c.arc(128, 196, 4, 0, TAU); c.arc(172, 196, 4, 0, TAU); c.fill();
      c.fillStyle = P.cream; c.strokeStyle = P.w2; c.lineWidth = 2.4; c.beginPath(); c.moveTo(124, 220); c.quadraticCurveTo(150, 254, 176, 220); c.closePath(); c.fill(); c.stroke();
      blob(c, 108, 214, 11, 7, 'rgba(201,103,122,.5)'); blob(c, 192, 214, 11, 7, 'rgba(201,103,122,.5)');
    },
  ];
  const SCENE_N = SCENES.length;

  // A memory picture: scene + soft light. Used for the gallery thumbnails, floating prints and album pages.
  function drawPhoto(canvas, id, { w, h } = {}) {
    w = w || canvas.width; h = h || canvas.height;
    const c = canvas.getContext('2d'); c.save(); c.scale(w / 300, h / 400); c.beginPath(); c.rect(0, 0, 300, 400); c.clip();
    SCENES[id % SCENE_N](c);
    c.fillStyle = rg(c, 150, 200, 120, 300, [[0, 'rgba(0,0,0,0)'], [1, 'rgba(34,5,15,.38)']]); c.fillRect(0, 0, 300, 400);      // vignette
    c.fillStyle = lg(c, 0, 0, 300, 400, [[0, 'rgba(255,246,225,.2)'], [0.35, 'rgba(255,246,225,0)']]); c.fillRect(0, 0, 300, 400);   // glass light
    c.restore();
  }

  // ───────────────────────────── phone, book cover, pages ─────────────────────────────
  function foil(c, x0, y0, x1, y1) { return lg(c, x0, y0, x1, y1, [[0, P.g0], [0.28, P.g3], [0.5, P.g1], [0.74, P.g3], [1, P.g0]]); }

  function ornamentLine(c, cx, y, w, col) {
    c.strokeStyle = col; c.fillStyle = col; c.lineWidth = 1.6;
    c.beginPath(); c.moveTo(cx - w / 2, y); c.lineTo(cx - 14, y); c.moveTo(cx + 14, y); c.lineTo(cx + w / 2, y); c.stroke();
    c.beginPath(); c.moveTo(cx, y - 7); c.lineTo(cx + 7, y); c.lineTo(cx, y + 7); c.lineTo(cx - 7, y); c.closePath(); c.fill();
  }
  function cornerFlourish(c, x, y, sx, sy, col, s = 1) {
    c.save(); c.translate(x, y); c.scale(sx * s, sy * s); c.strokeStyle = col; c.lineWidth = 1.8;
    c.beginPath(); c.moveTo(0, 46); c.quadraticCurveTo(0, 0, 46, 0); c.stroke();
    c.beginPath(); c.moveTo(10, 40); c.quadraticCurveTo(12, 12, 40, 10); c.stroke();
    c.fillStyle = col; c.beginPath(); c.arc(8, 8, 3.6, 0, TAU); c.fill(); c.beginPath(); c.arc(30, 4, 2, 0, TAU); c.arc(4, 30, 2, 0, TAU); c.fill();
    c.restore();
  }

  // The "Ms. Memories" mark: a gold ring holding an open book with a heart rising from the gutter.
  function drawEmblem(c, cx, cy, r, fill) {
    c.save(); c.translate(cx, cy); c.scale(r / 100, r / 100); c.strokeStyle = fill; c.fillStyle = fill; c.lineWidth = 5;
    c.beginPath(); c.arc(0, 0, 96, 0, TAU); c.stroke(); c.lineWidth = 2; c.beginPath(); c.arc(0, 0, 86, 0, TAU); c.stroke();
    c.lineWidth = 5; c.lineJoin = 'round';
    c.beginPath(); c.moveTo(0, 38); c.quadraticCurveTo(-34, 18, -66, 26); c.lineTo(-66, -30); c.quadraticCurveTo(-34, -38, 0, -14); c.quadraticCurveTo(34, -38, 66, -30); c.lineTo(66, 26); c.quadraticCurveTo(34, 18, 0, 38); c.closePath(); c.stroke();
    c.beginPath(); c.moveTo(0, -14); c.lineTo(0, 38); c.stroke();
    c.beginPath(); c.moveTo(0, -30); c.bezierCurveTo(-30, -66, -50, -38, -22, -52); c.bezierCurveTo(-8, -58, 0, -48, 0, -40); c.bezierCurveTo(0, -48, 8, -58, 22, -52); c.bezierCurveTo(50, -38, 30, -66, 0, -30); c.fill();
    c.restore();
  }
  function wordmark(c, cx, y, size, fill) {
    c.save(); c.font = `italic 600 ${size}px CG, 'Cormorant Garamond', Georgia, serif`; c.textAlign = 'center'; c.textBaseline = 'alphabetic'; c.fillStyle = fill; c.fillText('Ms. Memories', cx, y); c.restore();
  }

  function leatherTexture(c, w, h, seed, base) {
    const R = root.OM.rng(seed); c.fillStyle = base; c.fillRect(0, 0, w, h);
    for (let i = 0; i < 2600; i++) { const x = R() * w, y = R() * h; c.fillStyle = R() > 0.5 ? 'rgba(255,200,190,.045)' : 'rgba(10,0,4,.07)'; c.fillRect(x, y, 1 + R() * 2.4, 1 + R() * 2.4); }
  }

  function drawCover(canvas) {                      // 470×640 unit page, drawn at canvas scale
    const s = canvas.width / 470, c = canvas.getContext('2d'); c.save(); c.scale(s, s);
    leatherTexture(c, 470, 640, 301, P.w2);
    c.fillStyle = lg(c, 0, 0, 470, 640, [[0, 'rgba(255,170,170,.2)'], [0.45, 'rgba(0,0,0,0)'], [1, 'rgba(10,0,4,.5)']]); c.fillRect(0, 0, 470, 640);
    c.fillStyle = lg(c, 440, 0, 470, 0, [[0, 'rgba(0,0,0,0)'], [1, 'rgba(10,0,4,.55)']]); c.fillRect(440, 0, 30, 640);       // spine shadow
    c.strokeStyle = foil(c, 0, 0, 470, 640); c.lineWidth = 3; rr(c, 30, 30, 410, 580, 10); c.stroke(); c.lineWidth = 1.2; rr(c, 42, 42, 386, 556, 6); c.stroke();
    [[44, 44, 1, 1], [426, 44, -1, 1], [44, 596, 1, -1], [426, 596, -1, -1]].forEach(([x, y, sx, sy]) => cornerFlourish(c, x, y, sx, sy, P.g2, 1.1));
    c.shadowColor = 'rgba(0,0,0,.55)'; c.shadowBlur = 8; c.shadowOffsetY = 3;
    drawEmblem(c, 235, 244, 82, foil(c, 150, 160, 320, 330));
    c.shadowColor = 'transparent'; wordmark(c, 235, 428, 62, foil(c, 120, 380, 350, 440));
    ornamentLine(c, 235, 468, 230, P.g1);
    c.restore();
  }
  function drawEndpaper(canvas) {                   // inside of the front cover: ivory, a gold lattice
    const s = canvas.width / 470, c = canvas.getContext('2d'); c.save(); c.scale(s, s);
    c.fillStyle = lg(c, 0, 0, 470, 640, [[0, P.cream], [1, P.sand]]); c.fillRect(0, 0, 470, 640);
    c.strokeStyle = 'rgba(201,154,75,.5)'; c.lineWidth = 1;
    for (let i = -20; i < 40; i++) { c.beginPath(); c.moveTo(i * 30, 0); c.lineTo(i * 30 + 640, 640); c.stroke(); c.beginPath(); c.moveTo(i * 30 + 640, 0); c.lineTo(i * 30, 640); c.stroke(); }
    for (let y = 0; y < 640; y += 30) for (let x = 0; x < 470; x += 30) { c.fillStyle = 'rgba(154,106,38,.5)'; c.beginPath(); c.arc(x + (y / 30 % 2 ? 15 : 0), y, 2.4, 0, TAU); c.fill(); }
    c.fillStyle = P.cream; rr(c, 90, 190, 290, 260, 16); c.fill(); c.strokeStyle = P.g1; c.lineWidth = 2; rr(c, 90, 190, 290, 260, 16); c.stroke(); rr(c, 100, 200, 270, 240, 10); c.stroke();
    drawEmblem(c, 235, 292, 52, P.g0); wordmark(c, 235, 394, 40, P.g0);
    c.fillStyle = lg(c, 0, 0, 40, 0, [[0, 'rgba(60,20,10,.28)'], [1, 'rgba(0,0,0,0)']]); c.fillRect(0, 0, 40, 640);
    c.restore();
  }

  function paper(c, spineSide) {                     // ivory leaf with a quiet gutter shadow; spineSide 'r' (left page) or 'l' (right page)
    c.fillStyle = lg(c, 0, 0, 470, 640, [[0, P.cream], [1, '#f1e1c4']]); c.fillRect(0, 0, 470, 640);
    const R = root.OM.rng(spineSide === 'r' ? 41 : 42); for (let i = 0; i < 900; i++) { c.fillStyle = 'rgba(154,106,38,.05)'; c.fillRect(R() * 470, R() * 640, 1 + R() * 2, 1); }
    const x0 = spineSide === 'r' ? 470 : 0, x1 = spineSide === 'r' ? 400 : 70;
    c.fillStyle = lg(c, x0, 0, x1, 0, [[0, 'rgba(70,24,12,.34)'], [1, 'rgba(70,24,12,0)']]); c.fillRect(Math.min(x0, x1), 0, 70, 640);
  }
  function print(c, id, x, y, w, h, rot, { tape = true, caption = true } = {}) {   // a photo print glued to the page
    c.save(); c.translate(x + w / 2, y + h / 2); c.rotate(rot);
    c.shadowColor = 'rgba(60,20,10,.4)'; c.shadowBlur = 14; c.shadowOffsetY = 5; c.fillStyle = '#fffaf0'; c.fillRect(-w / 2 - 9, -h / 2 - 9, w + 18, h + 9 + (caption ? 34 : 9)); c.shadowColor = 'transparent';
    const t = document.createElement('canvas'); t.width = Math.round(w * 2); t.height = Math.round(h * 2); drawPhoto(t, id); c.drawImage(t, -w / 2, -h / 2, w, h);
    if (caption) { c.strokeStyle = P.g0; c.lineWidth = 2; c.lineCap = 'round'; c.beginPath(); c.moveTo(-w / 2 + 6, h / 2 + 20); c.bezierCurveTo(-w / 4, h / 2 + 10, 0, h / 2 + 30, w / 5, h / 2 + 18); c.stroke(); }
    if (tape) { c.fillStyle = 'rgba(233,201,130,.78)'; c.save(); c.translate(0, -h / 2 - 8); c.rotate(-0.06); c.fillRect(-30, -9, 60, 20); c.restore(); }
    c.restore();
  }
  function captionLines(c, x, y, w, n, seed) { const R = root.OM.rng(seed); c.strokeStyle = 'rgba(154,106,38,.55)'; c.lineWidth = 2.2; c.lineCap = 'round'; for (let i = 0; i < n; i++) { c.beginPath(); const L = w * (0.55 + R() * 0.45); c.moveTo(x + w - L, y + i * 20); c.bezierCurveTo(x + w - L * 0.7, y + i * 20 - 6, x + w - L * 0.4, y + i * 20 + 6, x + w, y + i * 20); c.stroke(); } }
  function sprig(c, x, y, s, rot) { c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); c.strokeStyle = '#8b3a4c'; c.lineWidth = 2; c.beginPath(); c.moveTo(0, 0); c.quadraticCurveTo(10, -40, 0, -90); c.stroke(); for (let i = 0; i < 5; i++) { blob(c, (i % 2 ? 9 : -9), -18 - i * 15, 9, 5, i % 2 ? P.rose : P.blush); } blob(c, 0, -92, 8, 8, P.g1); c.restore(); }

  const PAGES = {
    // title page
    L0f(c) { paper(c, 'r'); c.strokeStyle = P.g1; c.lineWidth = 2; rr(c, 34, 34, 402, 572, 8); c.stroke(); [[40, 40, 1, 1], [430, 40, -1, 1], [40, 600, 1, -1], [430, 600, -1, -1]].forEach(([x, y, sx, sy]) => cornerFlourish(c, x, y, sx, sy, P.g1, 0.9)); drawEmblem(c, 235, 230, 66, P.g0); wordmark(c, 235, 380, 56, P.g0); ornamentLine(c, 235, 418, 200, P.g1); captionLines(c, 120, 470, 230, 3, 9); },
    L0b(c) { paper(c, 'l'); print(c, 0, 62, 56, 230, 300, -0.05); print(c, 3, 262, 196, 150, 200, 0.07); print(c, 4, 70, 380, 150, 200, 0.04); captionLines(c, 260, 450, 170, 3, 12); sprig(c, 420, 620, 0.8, -0.2); },
    L1f(c) { paper(c, 'r'); print(c, 6, 44, 64, 340, 440, -0.025); captionLines(c, 80, 560, 300, 2, 14); sprig(c, 50, 620, 0.9, 0.2); },
    L1b(c) { paper(c, 'l'); print(c, 1, 70, 56, 150, 200, -0.06); print(c, 2, 252, 80, 150, 200, 0.05); print(c, 5, 80, 340, 150, 200, 0.04); print(c, 8, 258, 366, 150, 200, -0.04); },
    L2f(c) { paper(c, 'r'); print(c, 9, 60, 50, 250, 330, 0.03); print(c, 10, 220, 330, 170, 226, -0.05); captionLines(c, 60, 480, 140, 3, 15); sprig(c, 90, 620, 1, -0.1); },
    L2b(c) { paper(c, 'l'); print(c, 7, 64, 54, 330, 430, -0.02); print(c, 11, 270, 420, 130, 170, 0.08); captionLines(c, 70, 540, 170, 3, 17); },
    L3f(c) { paper(c, 'r'); print(c, 8, 70, 56, 170, 226, -0.05); print(c, 2, 230, 150, 170, 226, 0.05); print(c, 4, 120, 380, 200, 150, 0.02, { caption: true }); },
    // the page the video belongs to
    L3b(c) {
      paper(c, 'l'); print(c, 0, 48, 56, 356, 462, -0.02, { tape: true });
      c.save(); c.translate(228, 288); c.fillStyle = 'rgba(34,5,15,.5)'; c.beginPath(); c.arc(0, 0, 38, 0, TAU); c.fill(); c.strokeStyle = P.g2; c.lineWidth = 3; c.beginPath(); c.arc(0, 0, 38, 0, TAU); c.stroke(); c.fillStyle = P.g2; c.beginPath(); c.moveTo(-10, -16); c.lineTo(18, 0); c.lineTo(-10, 16); c.closePath(); c.fill(); c.restore();
      captionLines(c, 90, 580, 280, 2, 19);
    },
    // the QR page
    L4f(c) {
      paper(c, 'r'); c.strokeStyle = P.g1; c.lineWidth = 2; rr(c, 34, 34, 402, 572, 8); c.stroke();
      [[40, 40, 1, 1], [430, 40, -1, 1], [40, 600, 1, -1], [430, 600, -1, -1]].forEach(([x, y, sx, sy]) => cornerFlourish(c, x, y, sx, sy, P.g1, 0.9));
      c.fillStyle = '#fffaf0'; c.shadowColor = 'rgba(60,20,10,.35)'; c.shadowBlur = 20; c.shadowOffsetY = 8; rr(c, 82, 150, 306, 306, 22); c.fill(); c.shadowColor = 'transparent';
      c.strokeStyle = foil(c, 82, 150, 388, 456); c.lineWidth = 4; rr(c, 82, 150, 306, 306, 22); c.stroke();
      drawQR(c, 112, 180, 246, P.w1, '#fffaf0');
      ornamentLine(c, 235, 520, 220, P.g1); captionLines(c, 140, 548, 190, 2, 23);
    },
    L4b(c) { paper(c, 'l'); drawEmblem(c, 235, 300, 56, P.g1); ornamentLine(c, 235, 390, 160, P.g1); },
  };
  function drawPage(canvas, key) { const s = canvas.width / 470, c = canvas.getContext('2d'); c.save(); c.scale(s, s); PAGES[key](c); c.restore(); }

  // ───────────────────────────── QR (illustrated, 25×25 modules) ─────────────────────────────
  const QR_N = 25;
  const QR_BITS = (() => {
    const R = root.OM.rng(2024), m = []; for (let y = 0; y < QR_N; y++) { m.push([]); for (let x = 0; x < QR_N; x++) m[y].push(R() > 0.52 ? 1 : 0); }
    const clear = (x0, y0, n) => { for (let y = y0; y < y0 + n; y++) for (let x = x0; x < x0 + n; x++) if (x >= 0 && y >= 0 && x < QR_N && y < QR_N) m[y][x] = 0; };
    const finder = (x0, y0) => { clear(x0 - 1, y0 - 1, 9); for (let y = 0; y < 7; y++) for (let x = 0; x < 7; x++) m[y0 + y][x0 + x] = (x === 0 || y === 0 || x === 6 || y === 6 || (x >= 2 && x <= 4 && y >= 2 && y <= 4)) ? 1 : 0; };
    finder(0, 0); finder(QR_N - 7, 0); finder(0, QR_N - 7);
    clear(QR_N - 9, QR_N - 9, 5); for (let y = 0; y < 5; y++) for (let x = 0; x < 5; x++) m[QR_N - 9 + y][QR_N - 9 + x] = (x === 0 || y === 0 || x === 4 || y === 4 || (x === 2 && y === 2)) ? 1 : 0;
    for (let i = 8; i < QR_N - 8; i++) { m[6][i] = i % 2 ? 0 : 1; m[i][6] = i % 2 ? 0 : 1; }
    return m;
  })();
  function drawQR(c, x, y, size, ink, bg, reveal = 1) {
    const u = size / QR_N; c.fillStyle = bg; c.fillRect(x, y, size, size); c.fillStyle = ink;
    for (let j = 0; j < QR_N; j++) for (let i = 0; i < QR_N; i++) if (QR_BITS[j][i]) { const r = (c.canvas ? 0 : 0); c.beginPath(); const px = x + i * u, py = y + j * u; rr(c, px + u * 0.04, py + u * 0.04, u * 0.92, u * 0.92, u * 0.24); c.fill(); }
    // gold heart at the centre, the way a branded code carries its mark
    c.fillStyle = bg; rr(c, x + size / 2 - u * 2.6, y + size / 2 - u * 2.6, u * 5.2, u * 5.2, u * 1.2); c.fill();
    c.save(); c.translate(x + size / 2, y + size / 2 + u * 0.3); c.scale(u * 0.1, u * 0.1); c.fillStyle = P.w3; c.beginPath(); c.moveTo(0, 14); c.bezierCurveTo(-30, -6, -18, -30, 0, -14); c.bezierCurveTo(18, -30, 30, -6, 0, 14); c.fill(); c.restore();
  }

  // ───────────────────────────── the "video" that plays inside the phone ─────────────────────────────
  // The living version of memory 0: the same couple, the same shore, now with waves, birds and a wave of the hand.
  function drawVideo(c, w, h, tv) {
    c.save(); c.scale(w / 300, h / 400);
    const k = Math.min(1, tv / 5), push = 1 + 0.07 * (tv / 5);
    c.translate(150, 200); c.scale(push, push); c.translate(-150, -200);
    const sky = lg(c, 0, 0, 0, 260, [[0, k < 0.5 ? P.w3 : P.w2], [0.5, P.rose], [1, P.peach]]); c.fillStyle = sky; c.fillRect(-20, -20, 340, 300);
    const sunY = 214 + 24 * k; sunDisc(c, 150, sunY, 44);
    c.fillStyle = lg(c, 0, 250, 0, 400, [[0, P.w3], [1, P.w1]]); c.fillRect(-20, 252, 340, 160);
    for (let i = 0; i < 10; i++) { const y = 256 + i * 10; c.strokeStyle = `rgba(255,226,170,${0.7 - i * 0.06})`; c.lineWidth = 2; c.beginPath(); for (let x = -20; x <= 320; x += 6) c.lineTo(x, y + Math.sin(x * 0.06 + tv * 2.2 + i * 1.3) * (1.2 + i * 0.35)); c.stroke(); }
    const sh = '#d4a574'; c.fillStyle = sh; c.beginPath(); c.moveTo(-20, 360); for (let x = -20; x <= 320; x += 8) c.lineTo(x, 352 + Math.sin(x * 0.02 + tv * 0.8) * 2.4); c.lineTo(320, 420); c.lineTo(-20, 420); c.closePath(); c.fill();
    person(c, 120, 360, 98, P.w0, '#3a1117', { arm: 0.5 + 0.5 * Math.sin(tv * 5.2) * (tv > 1.2 ? 1 : 0.2) });
    person(c, 168, 360, 88, P.w0, '#3a1117', { dress: true });
    for (let i = 0; i < 5; i++) { const bx = ((tv * 26 + i * 70) % 380) - 40, by = 80 + i * 18 + Math.sin(tv * 3 + i) * 6; c.strokeStyle = P.w1; c.lineWidth = 2; c.beginPath(); c.moveTo(bx - 8, by + 3 * Math.sin(tv * 14 + i)); c.quadraticCurveTo(bx, by - 5, bx + 8, by + 3 * Math.sin(tv * 14 + i)); c.stroke(); }
    glow(c, 150, sunY, 160, 'rgba(255,226,170,.22)');
    c.fillStyle = rg(c, 150, 200, 110, 260, [[0, 'rgba(0,0,0,0)'], [1, 'rgba(34,5,15,.5)']]); c.fillRect(-20, -20, 340, 440);
    c.restore();
  }

  root.ART = { P, drawPhoto, drawCover, drawEndpaper, drawPage, drawQR, drawVideo, drawEmblem, wordmark, foil, rr, lg, rg, glow, SCENE_N, QR_N, ornamentLine };
})(window);
