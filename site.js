/*
 * Presentation data is loaded from the repository's authoritative palette file.
 * This intentionally uses a small parser for the project's dependency-free,
 * stable YAML shape instead of introducing a framework or CDN dependency.
 */
const PALETTE_SOURCE = 'palettes/government-ui.yaml';

const esc = (value) => String(value)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#039;');

function scalar(value) {
  const trimmed = value.trim();
  if ((trimmed.startsWith("'") && trimmed.endsWith("'")) || (trimmed.startsWith('"') && trimmed.endsWith('"'))) {
    return trimmed.slice(1, -1);
  }
  if (trimmed === 'true') return true;
  if (trimmed === 'false') return false;
  if (/^-?\d+(\.\d+)?$/.test(trimmed)) return Number(trimmed);
  return trimmed;
}

function flowMap(value) {
  const result = {};
  const body = value.trim().replace(/^\{\s*|\s*\}$/g, '');
  const pattern = /([a-z_]+):\s*(?:'([^']*)'|"([^"]*)"|([^,}]+))/g;
  for (const match of body.matchAll(pattern)) result[match[1]] = scalar(match[2] ?? match[3] ?? match[4]);
  return result;
}

function parsePaletteYaml(text) {
  const lines = text.split(/\r?\n/);
  const palettes = [];
  let current = null;
  let activeMap = null;
  for (const line of lines) {
    const faction = line.match(/^\- faction_id:\s*(.+)$/);
    if (faction) {
      current = { faction_id: scalar(faction[1]) };
      palettes.push(current);
      activeMap = null;
      continue;
    }
    if (!current) continue;
    if (activeMap) {
      const nested = line.match(/^ {4}([a-z_]+):\s*(.+)$/);
      if (nested) {
        current[activeMap][nested[1]] = scalar(nested[2]);
        continue;
      }
      if (line.trim() && !line.startsWith('    ')) activeMap = null;
    }
    const field = line.match(/^  ([a-z_]+):\s*(.*)$/);
    if (!field) continue;
    const [, key, value] = field;
    if (['roles', 'recommended_text', 'contrast_checks'].includes(key)) {
      current[key] = value.trim() ? flowMap(value) : {};
      activeMap = value.trim() ? null : key;
    }
    else if (key !== 'notes') current[key] = scalar(value);
  }
  if (!palettes.length || palettes.some((palette) => !palette.name || !palette.roles)) throw new Error('No usable palettes found.');
  return palettes;
}

const labelFor = {
  primary: 'Primary', secondary: 'Secondary', primary_surface: 'Surface', panel: 'Panel',
  panel_alt: 'Panel alt', border: 'Border', accent: 'Accent', foreground: 'Foreground', ink: 'Ink'
};

function swatch(key, palette) {
  const value = palette.roles[key];
  const textRole = key === 'primary' ? palette.recommended_text.on_primary
    : key === 'secondary' ? palette.recommended_text.on_secondary
    : key === 'accent' ? palette.recommended_text.on_accent
    : ['primary_surface', 'panel', 'panel_alt', 'border'].includes(key) ? 'foreground' : 'ink';
  return `<div class="swatch" style="background:${esc(value)};color:${esc(palette.roles[textRole])}"><span class="swatch-label">${esc(labelFor[key])}</span><code>${esc(value)}</code></div>`;
}

function card(palette) {
  const r = palette.roles;
  const rootVars = Object.entries(r).map(([key, value]) => `--${key.replaceAll('_', '-')}:${value}`).join(';');
  const primaryText = r[palette.recommended_text.on_primary];
  const secondaryText = r[palette.recommended_text.on_secondary];
  const contrast = palette.contrast_checks;
  const swatches = ['primary', 'secondary', 'primary_surface', 'panel', 'panel_alt', 'border', 'accent', 'foreground', 'ink'].map((key) => swatch(key, palette)).join('');
  return `<article class="palette-card" style="${rootVars}">
    <div class="palette-hero">
      <h3>${esc(palette.name)}</h3>
      <div class="palette-hero-meta"><span class="color-dot" style="background:${esc(r.primary)}"></span>${esc(palette.group || 'Government / faction identity')} · <code>${esc(palette.identity_claim_status)}</code></div>
    </div>
    <div class="palette-body">
      <div class="palette-labels">
        <div class="identity-chip primary-chip"><span>Primary identity</span><code>${esc(r.primary)}</code></div>
        <div class="identity-chip secondary-chip"><span>Secondary / support</span><code>${esc(r.secondary)}</code></div>
      </div>
      <div class="swatch-grid">${swatches}</div>
      <div class="sample-row">
        <div class="text-sample primary-sample" style="--primary-text:${esc(primaryText)}"><strong>Primary text</strong>Readable sample</div>
        <div class="text-sample secondary-sample" style="--secondary-text:${esc(secondaryText)}"><strong>Secondary text</strong>Readable sample</div>
      </div>
      <p class="note">Recommended text contrast: primary <code>${esc(contrast.recommended_text_on_primary)}</code> · secondary <code>${esc(contrast.recommended_text_on_secondary)}</code> · accent <code>${esc(contrast.recommended_text_on_accent)}</code></p>
      <p class="note">${esc(palette.design_note)}</p>
    </div>
  </article>`;
}

function parsePendingFactions(text) {
  return text.split(/\n(?=- id:)/).slice(1).map((block) => {
    const name = block.match(/\n\s+name: (.+)/)?.[1]?.trim();
    const status = block.match(/government_faction_identity:\s*\n\s+status: (.+)/)?.[1]?.trim();
    return name && status === 'unresolved' ? name : null;
  }).filter(Boolean);
}

async function loadPalettes() {
  const grid = document.querySelector('#palette-grid');
  const pending = document.querySelector('#pending-identities');
  try {
    const [paletteResponse, factionResponse] = await Promise.all([
      fetch(PALETTE_SOURCE, { cache: 'no-cache' }),
      fetch('factions/remaining-identities.yaml', { cache: 'no-cache' })
    ]);
    if (!paletteResponse.ok || !factionResponse.ok) throw new Error(`HTTP ${paletteResponse.status}/${factionResponse.status}`);
    const [paletteText, factionText] = await Promise.all([paletteResponse.text(), factionResponse.text()]);
    const palettes = parsePaletteYaml(paletteText);
    document.querySelector('#palette-count').textContent = palettes.length;
    grid.innerHTML = palettes.map(card).join('');
    const unresolved = parsePendingFactions(factionText);
    if (unresolved.length) {
      pending.innerHTML = `<div class="pending-heading"><div><p class="eyebrow">Evidence boundary</p><h2>Research Pending</h2></div><p>These identities remain visible as part of the expansion scope, but no placeholder colors are presented as findings.</p></div><div class="pending-list">${unresolved.map((name) => `<span>${esc(name)} <b>Research required</b></span>`).join('')}</div>`;
    }
  } catch (error) {
    grid.innerHTML = `<div class="error-card"><strong>Palette data could not be loaded.</strong><br><span>Open <code>${esc(PALETTE_SOURCE)}</code> directly or visit the repository to inspect the authoritative source.</span></div>`;
    console.error(error);
  }
}

loadPalettes();
