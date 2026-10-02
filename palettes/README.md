# Reusable UI palettes

`government-ui.yaml` contains the reusable dark-UI adaptations for the currently supported government/faction identities. The initial six are:

- Federated Suns
- Draconis Combine
- Free Worlds League
- Lyran Commonwealth
- Capellan Confederation
- Free Rasalhague Republic

The remaining expansion records are grouped as Clans, Clan successor states, Successor States / Inner Sphere, Periphery, interstellar organizations, and historical states. Identities without sufficient evidence remain in the research records as unresolved and do not receive placeholder palette values.

The palette roles are application-neutral. They describe faction-themed surfaces, borders, identity colors, supporting colors, and foreground choices. They do not assign application semantics such as `danger`, `success`, `dead`, `disabled`, or `warning`.

The exact hexadecimal values are `UI_ADAPTATION` design choices, not official BattleTech digital color specifications. The underlying identity claims remain `HERALDRY_DERIVED` and `RESEARCH_REQUIRED`, so the reusable UI palettes remain `PROVISIONAL`.

Known peer consumers include Combat Infantry and the A Time of War (AToW) Character Creator, along with future BattleTech interfaces, faction selectors, political/strategic maps, charts, and documents. Each consumer maps this reusable palette onto its own semantic UI roles and accessibility requirements without redefining the underlying faction identity.

The [visual preview](government-ui-preview.html) is a development/reference artifact, not evidence authority.

Consumer-specific palettes are adaptations for a defined use, such as maps, interfaces, or print. They must reference an approved faction identity or explicitly state that they are provisional. A UI hex sampled from emblem artwork is an adaptation, not an official color specification.
