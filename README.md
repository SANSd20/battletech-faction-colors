# BattleTech Faction Colors

Research and canonical color records for BattleTech faction identities.

## Architecture

- `research/` preserves source records, observations, claims, and provenance.
- `factions/` contains canonical faction identity records.
- `palettes/` contains consumer-specific adaptations.

Military identity is separate from government/faction identity. A color can be useful for a military paint scheme without being a government or faction identity color, and vice versa. The reusable military palette dataset is in `palettes/military-ui.yaml`; canonical claims are in `research/claims/military.yaml`, reviewed unresolved outcomes are in `research/claims/military-review.yaml`, and durable Shrapnel/Camo Specs evidence is normalized in `research/provenance/military-colors.yaml`.

## Evidence and approval

Evidence classification describes where a claim comes from. Approval status describes whether the project has accepted the claim for canonical use. They are independent fields.

Current evidence classifications include `ESTABLISHED`, `MILITARY-STANDARD_DERIVED`, `REPRESENTATIVE_DERIVED`, `HERALDRY_DERIVED`, `DIRECT_TEXTUAL`, `VISUAL_OBSERVATION`, `SECONDARY_REFERENCE`, and `UI_ADAPTATION` as applicable to the record. Approval/status fields remain separate and include states such as `RESEARCH_REQUIRED`, `PROVISIONAL`, `APPROVED`, `REJECTED`, `ESTABLISHED`, `INSUFFICIENT_EVIDENCE`, and `NO_UNIFIED_PALETTE` according to the data layer.

No exact hex values are canonical in the initial records. Hex values derived from artwork must be treated as UI adaptations, not official faction specifications.

## Initial scope

The repository accounts for 47 authoritative identities and provides 47 Government/Faction palettes. The initial six retain claim-level provenance in `research/claims/initial-six.yaml`; remaining identities are recorded separately in `research/claims/remaining-identities.yaml` and `factions/remaining-identities.yaml`. Military evidence is independent: 14 identities currently have reusable source-supported Military palettes, while reviewed unresolved outcomes remain explicitly `INSUFFICIENT_EVIDENCE` or `NO_UNIFIED_PALETTE` rather than receiving invented colors. Eligible Clan and Clan-successor unresolved identities may use an explicit Government-palette fallback in presentation; this does not change Military evidence. Clan Wolf in Exile remains a separate authoritative identity while sharing Clan Wolf's practical military treatment.

Clan Military Pass 2 deepens the Clan claims without merging successor identities. Hell's Horses now has a representative-derived black/red/gold Military palette based on Alpha Keshik evidence and *FM: Crusader Clans*. Smoke Jaguar remains pending because independently documented formations use materially different schemes; a single Clan-wide palette would overstate the evidence. Unresolved Clan records remain explicit in `research/claims/military.yaml` for the future blueprint presentation.

Military Research Pass 3 resolves ComStar and Word of Blake independently from Government/Faction heraldry. ComStar uses a white/light-gray organizational adaptation grounded in Com Guard evidence, while Word of Blake uses a distinct charcoal/light-gray/red synthesis grounded in Militia and Shadow Division evidence. Republic of the Sphere and Star League remain pending because their documented formations use multiple schemes without a defensible single reusable identity.

Military Research Pass 4 keeps most Periphery and historical identities pending because available Camo Specs evidence is formation-specific or materially varied. Umayyad Caliphate is the exception: its red-star-on-white common military identifying element is represented by a carefully labeled palette sharing the Government red/white UI values; this does not claim a universal uniform scheme. Magistracy of Canopus, Taurian Concordat, Outworlds Alliance, Marian Hegemony, and the remaining Pass 4 identities remain unresolved pending stronger organization-wide evidence. Later evidence promotion established Clan Jade Falcon and Aurigan Coalition Military palettes while preserving scoped exceptions and formation conflicts.

Military Color Provenance Consolidation records direct Shrapnel #01-#26 observations and normalized Camo Specs source chains in [`research/provenance/military-colors.yaml`](research/provenance/military-colors.yaml). The pass promotes Clan Jade Falcon to a green/yellow source-supported Military palette while retaining black Hazen/Mongol uniforms as scoped variation; formation, ceremonial, and conflicting evidence remains explicitly bounded.

The final unresolved review records a separate `research/claims/military-review.yaml` status layer. `RESEARCH_PENDING` means a concrete named lead remains; `INSUFFICIENT_EVIDENCE` means no currently accessible evidence supports a palette and no specific unreviewed lead remains; `NO_UNIFIED_PALETTE` means positive evidence shows that a single faction-wide palette would misrepresent documented formation variation. A mature Military dataset therefore need not contain 47 palettes.

For eligible Clan and Clan-successor identities marked `INSUFFICIENT_EVIDENCE`, the presentation layer may show the corresponding Government/Faction palette as an explicit practical `GOVERNMENT_PALETTE_FALLBACK`; this does not change the Military evidence status or apply to `NO_UNIFIED_PALETTE` or non-Clans.

## Presentation site

Consumer projects should follow [`docs/CONSUMING-PALETTES.md`](docs/CONSUMING-PALETTES.md) when selecting an identity context or handling unresolved Military evidence.

The project’s GitHub Pages site is the presentation layer for the reusable government/faction UI palettes:

<https://sansd20.github.io/battletech-faction-colors/>

The site reads `palettes/government-ui.yaml` at runtime. It is a visual reference, not an independent source of authority, and it does not establish military paint schemes or official hexadecimal color specifications.

Validation and accessibility: [`tools/audit-contrast.js`](tools/audit-contrast.js) checks reusable palette role backgrounds against the `foreground` and `ink` candidates using WCAG relative luminance.
