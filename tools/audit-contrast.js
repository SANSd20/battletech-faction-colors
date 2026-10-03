const fs = require('node:fs');

const threshold = 4.5;
const hexes = /#[0-9a-f]{6}/gi;

function luminance(hex) {
  const channels = [0, 2, 4].map((offset) => parseInt(hex.slice(offset + 1, offset + 3), 16) / 255);
  return channels.map((channel) => channel <= 0.03928 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4)
    .reduce((sum, channel, index) => sum + channel * [0.2126, 0.7152, 0.0722][index], 0);
}

function contrast(background, foreground) {
  const light = Math.max(luminance(background), luminance(foreground));
  const dark = Math.min(luminance(background), luminance(foreground));
  return (light + 0.05) / (dark + 0.05);
}

function palettes(path) {
  const blocks = fs.readFileSync(path, 'utf8').split(/\n(?=- faction_id:)/).slice(1);
  return blocks.map((block) => ({
    id: block.match(/^- faction_id:\s*(.+)/)?.[1]?.trim() || 'unknown',
    foreground: block.match(/\bforeground:\s*['"]?(#[0-9a-f]{6})/i)?.[1],
    ink: block.match(/\bink:\s*['"]?(#[0-9a-f]{6})/i)?.[1],
    border: block.match(/\bborder:\s*['"]?(#[0-9a-f]{6})/i)?.[1],
    primarySurface: block.match(/\bprimary_surface:\s*['"]?(#[0-9a-f]{6})/i)?.[1],
    panel: block.match(/\bpanel:\s*['"]?(#[0-9a-f]{6})/i)?.[1],
    backgrounds: [...new Set((block.match(hexes) || []).map((hex) => hex.toUpperCase()))]
  }));
}

const files = process.argv.slice(2);
const failures = [];
let backgrounds = 0;
let minimum = Infinity;
for (const file of files) {
  for (const palette of palettes(file)) {
    const candidates = [palette.foreground, palette.ink].filter(Boolean);
    for (const background of palette.backgrounds.filter((background) => background !== palette.border && background !== palette.primarySurface)) {
      backgrounds += 1;
      const best = Math.max(...candidates.map((candidate) => contrast(background, candidate)));
      minimum = Math.min(minimum, best);
      if (best < threshold) failures.push(`${file}:${palette.id} ${background} best=${best.toFixed(2)}`);
    }
  }
}
console.log(`Audited ${backgrounds} palette-role backgrounds; minimum candidate contrast ${minimum.toFixed(2)}:1.`);
if (failures.length) { console.error(`${failures.length} contrast failures (<${threshold}:1):\n${failures.join('\n')}`); process.exitCode = 1; }
else console.log(`PASS: every audited palette-role background has a foreground or ink candidate at least ${threshold}:1.`);
