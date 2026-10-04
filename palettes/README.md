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

Government/Faction palettes may include an optional `tertiary` role when the canonical identity record supports a source-grounded third identity color such as trim or support. This is distinct from `accent`, which remains a UI construction role. The website displays only primary, secondary, and supported tertiary identity roles; it does not display UI construction colors.

The exact hexadecimal values are `UI_ADAPTATION` design choices, not official BattleTech digital color specifications. Underlying claims may be heraldry-derived, direct textual, military-standard-derived, representative-derived, or otherwise scoped by their evidence records; palette approval/status is tracked separately and remains explicit in each palette record.

Consumers include BattleTech interfaces, faction selectors, political/strategic maps, charts, and documents. Each consumer maps this reusable palette onto its own semantic UI roles and accessibility requirements without redefining the underlying faction identity.

The [visual preview](government-ui-preview.html) is a development/reference artifact, not evidence authority.

Consumer-specific palettes are adaptations for a defined use, such as maps, interfaces, or print. They must reference an approved faction identity or explicitly state that they are provisional. A UI hex sampled from emblem artwork is an adaptation, not an official color specification.
