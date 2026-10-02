# BattleTech Faction Colors

Research and canonical color records for BattleTech faction identities.

## Architecture

- `research/` preserves source records, observations, claims, and provenance.
- `factions/` contains canonical faction identity records.
- `palettes/` contains consumer-specific adaptations.

Military identity is separate from government/faction identity. A color can be useful for a military paint scheme without being a government or faction identity color, and vice versa.

## Evidence and approval

Evidence classification describes where a claim comes from. Approval status describes whether the project has accepted the claim for canonical use. They are independent fields.

Current classifications include `DIRECT_TEXTUAL`, `HERALDRY_DERIVED`, `VISUAL_OBSERVATION`, and `SECONDARY_REFERENCE`. Current approval states include `RESEARCH_REQUIRED`, `PROVISIONAL`, `APPROVED`, and `REJECTED`.

No exact hex values are canonical in the initial records. Hex values derived from artwork must be treated as UI adaptations, not official faction specifications.

## Initial scope

The initial records cover Federated Suns, Draconis Combine, Free Worlds League, Lyran Commonwealth, Capellan Confederation, and Free Rasalhague Republic. The government/faction candidates are provisional heraldry-derived interpretations of Camo Specs faction emblems and retain claim-level provenance in `research/claims/initial-six.yaml`.
