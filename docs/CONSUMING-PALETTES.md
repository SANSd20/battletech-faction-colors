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

## Integration guidance

Resolve identities by their stable `faction_id`, read the current YAML files at integration time, and preserve the distinction between Government / Faction and Military. The presentation site may group records for readability—for example, Clan Wolf and Clan Wolf in Exile are shown together as `Clan Wolf / Clan Wolf in Exile`—but their authoritative records, IDs, claims, and palette entries remain separate.

When no supported Military palette exists, expose the recorded military status and explanation to users rather than silently substituting another identity context.
