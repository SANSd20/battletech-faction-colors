# BattleTech Faction Colors

Research and canonical color records for BattleTech faction identities.

## Architecture

- `research/` preserves source records, observations, claims, and provenance.
- `factions/` contains canonical faction identity records.
- `palettes/` contains consumer-specific adaptations.

Military identity is separate from government/faction identity. A color can be useful for a military paint scheme without being a government or faction identity color, and vice versa. The reusable military palette dataset is in `palettes/military-ui.yaml`; its provenance claims are in `research/claims/military.yaml`.

## Evidence and approval

Evidence classification describes where a claim comes from. Approval status describes whether the project has accepted the claim for canonical use. They are independent fields.

Current classifications include `DIRECT_TEXTUAL`, `HERALDRY_DERIVED`, `VISUAL_OBSERVATION`, and `SECONDARY_REFERENCE`. Current approval states include `RESEARCH_REQUIRED`, `PROVISIONAL`, `APPROVED`, and `REJECTED`.

No exact hex values are canonical in the initial records. Hex values derived from artwork must be treated as UI adaptations, not official faction specifications.

## Initial scope

The initial records cover Federated Suns, Draconis Combine, Free Worlds League, Lyran Commonwealth, Capellan Confederation, and Free Rasalhague Republic. The government/faction candidates are provisional heraldry-derived interpretations of Camo Specs faction emblems and retain claim-level provenance in `research/claims/initial-six.yaml`. The remaining-identity expansion is recorded separately in `research/claims/remaining-identities.yaml` and `factions/remaining-identities.yaml`. Military evidence is recorded independently: eight identities currently have reusable military palettes, while the remaining identities are explicitly research-pending rather than receiving invented colors. Clan Wolf in Exile remains separate while sharing Clan Wolf's practical military treatment; Smoke Jaguar's supplied image remains government/representative evidence only until independent military evidence is established.

Clan Military Pass 2 deepens the Clan claims without merging successor identities. Hell's Horses now has a representative-derived black/red/gold Military palette based on Alpha Keshik evidence and *FM: Crusader Clans*. Smoke Jaguar remains pending because independently documented formations use materially different schemes; a single Clan-wide palette would overstate the evidence. Unresolved Clan records remain explicit in `research/claims/military.yaml` for the future blueprint presentation.

Military Research Pass 3 resolves ComStar and Word of Blake independently from Government/Faction heraldry. ComStar uses a white/light-gray organizational adaptation grounded in Com Guard evidence, while Word of Blake uses a distinct charcoal/light-gray/red synthesis grounded in Militia and Shadow Division evidence. Republic of the Sphere and Star League remain pending because their documented formations use multiple schemes without a defensible single reusable identity.

## Presentation site

The project’s GitHub Pages site is the presentation layer for the reusable government/faction UI palettes:

<https://sansd20.github.io/battletech-faction-colors/>

The site reads `palettes/government-ui.yaml` at runtime. It is a visual reference, not an independent source of authority, and it does not establish military paint schemes or official hexadecimal color specifications.
