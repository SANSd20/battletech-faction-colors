const SOURCES = {
  government: 'palettes/government-ui.yaml',
  military: 'palettes/military-ui.yaml',
  factions: 'factions/remaining-identities.yaml',
  review: 'research/claims/military-review.yaml'
};

const esc = (value) => String(value ?? '')
  .replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;').replaceAll("'", '&#039;');

function scalar(value) {
  const trimmed = value.trim();
  if ((trimmed.startsWith("'") && trimmed.endsWith("'")) || (trimmed.startsWith('"') && trimmed.endsWith('"'))) return trimmed.slice(1, -1);
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
  const lines = text.split(/\r?\n/), palettes = [];
  let current = null, activeMap = null;
  for (const line of lines) {
    const faction = line.match(/^\- faction_id:\s*(.+)$/);
    if (faction) { current = { faction_id: scalar(faction[1]) }; palettes.push(current); activeMap = null; continue; }
    if (!current) continue;
    if (activeMap) {
      const nested = line.match(/^ {4}([a-z_]+):\s*(.+)$/);
      if (nested) { current[activeMap][nested[1]] = scalar(nested[2]); continue; }
      if (line.trim() && !line.startsWith('    ')) activeMap = null;
    }
    const field = line.match(/^  ([a-z_]+):\s*(.*)$/);
    if (!field) continue;
    const [, key, value] = field;
    if (['roles', 'recommended_text', 'contrast_checks'].includes(key)) {
      current[key] = value.trim() ? flowMap(value) : {};
      activeMap = value.trim() ? null : key;
    } else if (key !== 'notes') current[key] = scalar(value);
  }
  if (!palettes.length || palettes.some((palette) => !palette.name || !palette.roles)) throw new Error('No usable palettes found.');
  return palettes;
}

function parseReviewYaml(text) {
  const review = {};
  for (const block of text.split(/\n(?=- id:)/).slice(1)) {
    const id = block.match(/^- id: (.+)/)?.[1]?.trim();
    const status = block.match(/\n  review_status: (.+)/)?.[1]?.trim();
    const reason = block.match(/\n  reason: (.+)/)?.[1]?.trim();
    if (id) review[id] = { status, reason };
  }
  return review;
}

const labelFor = { primary: 'Primary', secondary: 'Secondary', primary_surface: 'Surface', panel: 'Panel', panel_alt: 'Panel alt', border: 'Border', accent: 'Accent', foreground: 'Foreground', ink: 'Ink' };
const stateCopy = {
  NO_UNIFIED_PALETTE: { label: 'No unified military palette', className: 'technical-state', text: 'Documented military formations use materially different schemes; a single faction-wide palette would be misleading.' },
  INSUFFICIENT_EVIDENCE: { label: 'Insufficient evidence', className: 'sketch-state', text: 'Available sources do not support a defensible reusable faction-wide Military palette.' }
};

function hexRgb(hex) { const value = hex.replace('#', ''); return [0, 2, 4].map((offset) => parseInt(value.slice(offset, offset + 2), 16) / 255); }
function luminance(hex) { return hexRgb(hex).map((channel) => channel <= .03928 ? channel / 12.92 : ((channel + .055) / 1.055) ** 2.4).reduce((sum, channel, index) => sum + channel * [0.2126, 0.7152, 0.0722][index], 0); }
function contrastRatio(background, foreground) { const light = Math.max(luminance(background), luminance(foreground)); const dark = Math.min(luminance(background), luminance(foreground)); return (light + .05) / (dark + .05); }
function chooseReadableText(background, palette) {
  const candidates = [palette.roles.foreground, palette.roles.ink].filter(Boolean);
  const best = candidates.sort((a, b) => contrastRatio(background, b) - contrastRatio(background, a))[0];
  if (!best || contrastRatio(background, best) < 4.5) throw new Error(`No readable text candidate for ${background}`);
  return best;
}

function swatch(key, palette) {
  const value = palette.roles[key];
  const background = ['border', 'primary_surface'].includes(key) && contrastRatio(value, palette.roles.foreground) < 4.5 && contrastRatio(value, palette.roles.ink) < 4.5 ? palette.roles.panel : value;
  const textColor = chooseReadableText(background, palette);
  const border = background !== value ? `;border:2px solid ${esc(value)}` : '';
  return `<div class="swatch" style="background:${esc(background)};color:${esc(textColor)}${border}"><span class="swatch-label">${esc(labelFor[key])}</span><code>${esc(value)}</code></div>`;
}

function paletteCard(palette, mode, presentation = null) {
  const r = palette.roles, contrast = palette.contrast_checks;
  const rootVars = Object.entries(r).map(([key, value]) => `--${key.replaceAll('_', '-')}:${value}`).join(';');
  const swatches = ['primary', 'secondary', 'primary_surface', 'panel', 'panel_alt', 'border', 'accent', 'foreground', 'ink'].map((key) => swatch(key, palette)).join('');
  const headerText = chooseReadableText(r.primary, palette), primaryText = chooseReadableText(r.primary, palette), secondaryText = chooseReadableText(r.secondary, palette);
  const primaryChipText = chooseReadableText(r.primary, palette), secondaryChipText = chooseReadableText(r.secondary, palette);
  const presentationClass = presentation ? ' fallback-card' : '';
  const statusLabel = presentation ? 'GOVERNMENT PALETTE FALLBACK' : mode === 'military' ? 'MILITARY' : esc(palette.identity_claim_status);
  const statusNote = presentation ? 'Military-specific evidence is insufficient for a reusable Clan-wide palette. Government/Faction colors are shown as the approved practical UI fallback.' : palette.design_note;
  return `<article class="palette-card${presentationClass}" data-faction="${esc(palette.faction_id)}" style="${rootVars}">
    <div class="palette-hero" style="color:${esc(headerText)}"><h3>${esc(palette.name)}</h3><div class="palette-hero-meta"><span class="color-dot" style="background:${esc(r.primary)}"></span>${esc(palette.group || 'Identity')} · <code>${statusLabel}</code></div></div>
    <div class="palette-body"><div class="palette-labels"><div class="identity-chip primary-chip" style="color:${esc(primaryChipText)}"><span>Primary identity</span><code>${esc(r.primary)}</code></div><div class="identity-chip secondary-chip" style="color:${esc(secondaryChipText)}"><span>Secondary / support</span><code>${esc(r.secondary)}</code></div></div>
    <div class="swatch-grid">${swatches}</div><div class="sample-row"><div class="text-sample primary-sample" style="--primary-text:${esc(primaryText)}"><strong>Primary text</strong>Readable sample</div><div class="text-sample secondary-sample" style="--secondary-text:${esc(secondaryText)}"><strong>Secondary text</strong>Readable sample</div></div>
    <p class="note">Recommended text contrast: primary <code>${esc(contrast.recommended_text_on_primary)}</code> · secondary <code>${esc(contrast.recommended_text_on_secondary)}</code> · accent <code>${esc(contrast.recommended_text_on_accent)}</code></p><p class="note">${esc(statusNote)}</p></div></article>`;
}

function presentationPalettes(palettes) {
  const wolf = palettes.find((palette) => palette.faction_id === 'clan-wolf');
  const exile = palettes.find((palette) => palette.faction_id === 'clan-wolf-in-exile');
  return palettes.filter((palette) => palette.faction_id !== 'clan-wolf-in-exile').map((palette) => {
    if (palette.faction_id !== 'clan-wolf' || !exile) return palette;
    return { ...palette, name: 'Clan Wolf / Clan Wolf in Exile', faction_id: 'clan-wolf-presentation', design_note: `${palette.design_note} Presentation grouping: Clan Wolf in Exile remains a separate authoritative identity and is shown here alongside Clan Wolf.` };
  });
}

function blueprintCard(faction, state) {
  const copy = stateCopy[state.status];
  return `<article class="blueprint-card ${copy.className}" data-faction="${esc(faction.faction_id)}"><div class="blueprint-grid" aria-hidden="true"></div><div class="blueprint-content"><p class="blueprint-kicker">Military identity analysis</p><h3>${esc(faction.name)}</h3><div class="blueprint-status">${esc(copy.label)}</div><p>${esc(copy.text)}</p><div class="placeholder-swatches"><span>PRIMARY ?</span><span>SECONDARY ?</span><span>ACCENT ?</span></div><p class="blueprint-reason">${esc(state.reason)}</p></div></article>`;
}

function getMode() { return new URLSearchParams(location.search).get('identity') === 'military' ? 'military' : 'government'; }
function setMode(mode) { const url = new URL(location.href); url.searchParams.set('identity', mode); history.pushState({}, '', url); renderMode(mode); }

async function renderMode(mode) {
  const grid = document.querySelector('#palette-grid'), pending = document.querySelector('#pending-identities');
  document.body.dataset.identity = mode;
  document.querySelectorAll('[data-mode]').forEach((button) => { const active = button.dataset.mode === mode; button.classList.toggle('is-active', active); button.setAttribute('aria-pressed', String(active)); });
  document.querySelector('#mode-heading').textContent = mode === 'military' ? 'Military identity dark UI palettes' : 'Government / Faction dark UI palettes';
  document.querySelector('#mode-intro').textContent = mode === 'military' ? 'Military identity is researched separately from Government/Faction identity. Finished cards show supported reusable palettes; technical cards show documented variation or insufficient evidence.' : 'Political and heraldic faction identities expressed as reusable UI adaptations. Exact digital values are project choices, not official BattleTech color specifications.';
  document.querySelector('#mode-count-label').textContent = mode === 'military' ? 'finished Military palettes' : 'finished Government / faction palettes';
  try {
    const urls = mode === 'military' ? [SOURCES.government, SOURCES.military, SOURCES.review] : [SOURCES.government];
    const responses = await Promise.all(urls.map((url) => fetch(url, { cache: 'no-cache' })));
    if (responses.some((response) => !response.ok)) throw new Error('Palette data request failed.');
    const texts = await Promise.all(responses.map((response) => response.text()));
    const government = parsePaletteYaml(texts[0]);
    if (mode === 'government') { document.querySelector('#palette-count').textContent = government.length; grid.innerHTML = presentationPalettes(government).map((p) => paletteCard(p, mode)).join(''); pending.innerHTML = ''; return; }
    const military = parsePaletteYaml(texts[1]), review = parseReviewYaml(texts[2]), byFaction = Object.fromEntries(military.map((p) => [p.faction_id, p]));
    let fallbackCount = 0;
    const cards = presentationPalettes(government).map((faction) => { const state = review[`${faction.faction_id}-military-identity`]; const palette = byFaction[faction.faction_id] || (faction.faction_id === 'clan-wolf-presentation' ? { ...byFaction['clan-wolf'], name: faction.name, faction_id: faction.faction_id, design_note: `${byFaction['clan-wolf'].design_note} Presentation grouping: Clan Wolf in Exile remains a separate authoritative identity and is shown here alongside Clan Wolf.` } : null); if (palette) return paletteCard(palette, mode); if (state?.status === 'INSUFFICIENT_EVIDENCE' && ['Clans', 'Clan successor states'].includes(faction.group)) { fallbackCount += 1; return paletteCard({ ...faction, faction_id: faction.faction_id }, mode, true); } return state ? blueprintCard(faction, state) : ''; }).join('');
    const counts = Object.values(review).reduce((a, v) => { a[v.status] = (a[v.status] || 0) + 1; return a; }, {});
    document.querySelector('#palette-count').textContent = military.length; grid.innerHTML = cards; pending.innerHTML = `<div class="pending-heading"><div><p class="eyebrow">Evidence boundary</p><h2>Military research states</h2></div><p>${military.length} source-supported palettes · ${fallbackCount} Clan Government-palette fallbacks · ${counts.NO_UNIFIED_PALETTE || 0} technical conclusions · ${(counts.INSUFFICIENT_EVIDENCE || 0) - fallbackCount} non-Clan insufficient-evidence records.</p></div>`;
  } catch (error) { grid.innerHTML = `<div class="error-card"><strong>Identity data could not be loaded.</strong><br><span>${esc(error.message)}</span></div>`; pending.innerHTML = ''; console.error(error); }
}

document.querySelectorAll('[data-mode]').forEach((button) => button.addEventListener('click', () => setMode(button.dataset.mode)));
window.addEventListener('popstate', () => renderMode(getMode()));
renderMode(getMode());
