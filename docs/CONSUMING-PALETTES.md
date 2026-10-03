# Consuming BattleTech Faction Colors

BattleTech Faction Colors is the shared durable faction-color authority for consumer projects. Always consult the current repository state; do not copy palette values into another project or rely on conversation memory.

## Authoritative sources

Reusable UI palettes live in:

- `palettes/government-ui.yaml`
- `palettes/military-ui.yaml`

Research and provenance records remain separate from reusable UI palettes. The GitHub Pages site is a presentation layer and is not an additional source of authority.

## Choose the identity context

Use Government / Faction for political affiliation, faction affiliation, faction selectors, character affiliation, political maps, faction headers, and general faction identity.

Use Military for military units, military formations, force-building interfaces, military organization, military-themed displays, and operational contexts. Government and Military colors are separate contexts and must not be assumed interchangeable.

## Military outcomes

### Supported Military palette

A reusable palette exists. Use `palettes/military-ui.yaml` as the palette basis and retain the faction and claim metadata when integrating it.

### `NO_UNIFIED_PALETTE`

Available evidence positively demonstrates materially different military schemes, so one faction-wide palette would misrepresent the documented formations. Do not invent a fallback palette or collapse the evidence into a single color. Keep the consumer state technical and visibly unresolved.

### `INSUFFICIENT_EVIDENCE`

Current evidence does not support a defensible reusable faction-wide Military palette. Do not treat a Government / Faction palette as a military fallback, and do not present placeholder colors as findings. Keep the consumer state visibly unresolved until the authoritative research state changes.

For a Clan or Clan-successor identity with `INSUFFICIENT_EVIDENCE`, consumers may use that identity's Government / Faction palette as the standard practical Military UI fallback. This is a `GOVERNMENT_PALETTE_FALLBACK` and remains a `UI_ADAPTATION`, not Military evidence; the underlying Military status stays `INSUFFICIENT_EVIDENCE`. Formation-specific evidence may be preferable for an exact consumer context. This fallback is forbidden for `NO_UNIFIED_PALETTE` and does not apply to non-Clans without a future project decision.

## Integration guidance

Resolve identities by their stable `faction_id`, read the current YAML files at integration time, and preserve the distinction between Government / Faction and Military. The presentation site may group records for readability—for example, Clan Wolf and Clan Wolf in Exile are shown together as `Clan Wolf / Clan Wolf in Exile`—but their authoritative records, IDs, claims, and palette entries remain separate.

When no supported Military palette exists, expose the recorded military status and explanation to users rather than silently substituting another identity context.

## Stable consumer baseline

`v1.0.0` was the first stable, reproducible consumer baseline. `v1.1.0` is the current stable consumer baseline. Consumers that need the current fixed contract should pin to the `v1.1.0` tag; consumers intentionally requiring the older contract may continue to pin `v1.0.0`. Consumers that intentionally follow the latest evolving authority may track `main`; tracking `main` is optional, not required.

Consumers representing political or faction affiliation generally use Government / Faction identity. Consumers representing military units, formations, service, or military organizations use Military identity. An individual consumer may use both contexts in different UI areas. Consumer-specific semantic roles remain local to the consuming project; new or conflicting faction-color evidence should be returned to this repository for authoritative review.
