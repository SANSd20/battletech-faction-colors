#!/usr/bin/env python3
"""Generate the durable records for the remaining Camo Specs identities."""

from pathlib import Path
import colorsys
import math
import yaml

ROOT = Path(__file__).resolve().parents[1]
ACCESS_DATE = "2026-10-02"

# Values are semantic starting points from the Camo Specs emblem observations.
# The resulting hex values are deliberately generated UI adaptations, never
# source claims or raw logo specifications.
IDENTITIES = [
    ("clan-blood-spirit", "Clan Blood Spirit", "Clans", "red", "silver-gold", "cream", "strong", "https://camospecs.com/factions/clan-blood-spirit/"),
    ("clan-burrock", "Clan Burrock", "Clans", "black", "gold", "cream", "strong", "https://camospecs.com/factions/clan-burrock/"),
    ("clan-cloud-cobra", "Clan Cloud Cobra", "Clans", "cyan", "purple", "silver", "strong", "https://camospecs.com/factions/clan-cloud-cobra/"),
    ("clan-coyote", "Clan Coyote", "Clans", "ochre", "gold-red", "blue-gray", "moderate", "https://camospecs.com/factions/clan-coyote/"),
    ("clan-diamond-shark", "Clan Diamond Shark", "Clans", "silver", "red", "blue-gray", "strong", "https://camospecs.com/factions/clan-diamond-shark/"),
    ("clan-fire-mandrill", "Clan Fire Mandrill", "Clans", "orange-red", "gold", "charcoal", "strong", "https://camospecs.com/factions/clan-fire-mandrill/"),
    ("clan-ghost-bear", "Clan Ghost Bear", "Clans", "ice-blue", "silver", "navy", "strong", "https://camospecs.com/factions/clan-ghost-bear/"),
    ("clan-goliath-scorpion", "Clan Goliath Scorpion", "Clans", "green", "black-gold", "sand", "strong", "https://camospecs.com/factions/clan-goliath-scorpion/"),
    ("scorpion-empire", "Scorpion Empire", "Clan successor states", "green", "red-gold", "sand", "strong", "https://camospecs.com/factions/scorpion-empire/"),
    ("clan-hells-horses", "Clan Hell's Horses", "Clans", "ochre-brown", "red", "cream", "moderate", "https://camospecs.com/factions/clan-hells-horses/"),
    ("clan-ice-hellion", "Clan Ice Hellion", "Clans", "ice-blue", "orange", "charcoal", "moderate", "https://camospecs.com/factions/clan-ice-hellion/"),
    ("clan-jade-falcon", "Clan Jade Falcon", "Clans", "green", "blue", "gold", "strong", "https://camospecs.com/factions/clan-jade-falcon/"),
    ("clan-nova-cat", "Clan Nova Cat", "Clans", "navy", "red-gold", "silver", "strong", "https://camospecs.com/factions/clan-nova-cat/"),
    ("clan-sea-fox", "Clan Sea Fox", "Clans", "pale-blue", "silver", "navy", "strong", "https://camospecs.com/factions/clan-sea-fox/"),
    ("clan-smoke-jaguar", "Clan Smoke Jaguar", "Clans", "unresolved", "unresolved", "unresolved", "limited", "https://camospecs.com/factions/clan-smoke-jaguar/"),
    ("clan-snow-raven", "Clan Snow Raven", "Clans", "slate", "ice-blue", "white", "moderate", "https://camospecs.com/factions/clan-snow-raven/"),
    ("raven-alliance", "Raven Alliance", "Clan successor states", "black", "ice-blue", "white", "strong", "https://camospecs.com/factions/raven-alliance/"),
    ("clan-star-adder", "Clan Star Adder", "Clans", "navy", "cyan-gold", "cream", "moderate", "https://camospecs.com/factions/clan-star-adder/"),
    ("clan-steel-viper", "Clan Steel Viper", "Clans", "teal-green", "black", "mint", "strong", "https://camospecs.com/factions/clan-steel-viper/"),
    ("clan-stone-lion", "Clan Stone Lion", "Clans", "charcoal", "gold-brown", "sand", "moderate", "https://camospecs.com/factions/clan-stone-lion/"),
    ("clan-widowmaker", "Clan Widowmaker", "Clans", "black", "gold-red", "gray", "strong", "https://camospecs.com/factions/clan-widowmaker/"),
    ("clan-wolf", "Clan Wolf", "Clans", "red", "gold", "charcoal", "strong", "https://camospecs.com/factions/clan-wolf/"),
    ("clan-wolf-in-exile", "Clan Wolf in Exile", "Clans", "unresolved", "unresolved", "unresolved", "limited", "https://camospecs.com/factions/clan-wolf-in-exile/"),
    ("comstar", "ComStar", "Interstellar organizations", "silver", "black", "white", "strong", "https://camospecs.com/factions/comstar/"),
    ("republic-of-the-sphere", "Republic of the Sphere", "Successor States / Inner Sphere", "black", "gold-blue", "silver", "moderate", "https://camospecs.com/factions/republic-of-the-sphere/"),
    ("word-of-blake", "Word of Blake", "Interstellar organizations", "black", "silver-white", "violet", "strong", "https://camospecs.com/factions/word-of-blake/"),
    ("calderon-protectorate", "Calderon Protectorate", "Periphery", "red", "black-gold", "cream", "strong", "https://camospecs.com/factions/calderon-protectorate/"),
    ("circinus-federation", "Circinus Federation", "Periphery", "violet", "silver", "charcoal", "moderate", "https://camospecs.com/factions/circinus-federation-2/"),
    ("fiefdom-of-randis", "Fiefdom of Randis", "Periphery", "olive", "silver", "cream", "moderate", "https://camospecs.com/factions/fiefdom-of-randis/"),
    ("hanseatic-league", "Hanseatic League", "Periphery", "red", "gold-black", "cream", "strong", "https://camospecs.com/factions/hanseatic-league/"),
    ("magistracy-of-canopus", "Magistracy of Canopus", "Periphery", "green", "gold-white", "cream", "strong", "https://camospecs.com/factions/magictracy-of-canopus/"),
    ("marian-hegemony", "Marian Hegemony", "Periphery", "navy", "silver-gold", "cream", "moderate", "https://camospecs.com/factions/marian-hegemony/"),
    ("fronc-reaches", "Fronc Reaches", "Periphery", "blue", "red-gold", "cream", "strong", "https://camospecs.com/factions/fronc-reaches/"),
    ("nueva-castile", "Nueva Castile", "Periphery", "green", "cream", "olive", "moderate", "https://camospecs.com/factions/nueva-castile/"),
    ("niops-association", "Niops Association", "Periphery", "charcoal", "silver", "white", "limited", "https://camospecs.com/factions/niops-association/"),
    ("outworlds-alliance", "Outworlds Alliance", "Periphery", "red", "yellow-cream", "olive", "strong", "https://camospecs.com/factions/outworlds-alliance/"),
    ("taurian-concordat", "Taurian Concordat", "Periphery", "brown", "cream", "black", "strong", "https://camospecs.com/factions/taurian-concordat/"),
    ("umayyad-caliphate", "Umayyad Caliphate", "Periphery", "unresolved", "unresolved", "unresolved", "limited", "https://camospecs.com/factions/umayyad-caliphate/"),
    ("rim-worlds-republic", "Rim Worlds Republic", "Historical states", "red", "blue-black", "gray", "strong", "https://camospecs.com/factions/rim-worlds-republic/"),
    ("star-league", "Star League", "Historical states", "teal", "white-gold", "navy", "moderate", "https://camospecs.com/factions/star-league/"),
    ("aurigan-coalition", "Aurigan Coalition", "Periphery", "red", "gold", "black", "strong", "https://camospecs.com/factions/aurigan-coalition/"),
]

TOKENS = {
    "red": ("#B52A32", "#E05A5F"), "silver-gold": ("#B8C4CB", "#E2B93B"),
    "black": ("#22272B", "#D5B13C"), "gold": ("#D6A72F", "#F1D36C"),
    "cyan": ("#1599A8", "#A4E9EE"), "purple": ("#7047A3", "#C5B3D9"),
    "silver": ("#AAB5BF", "#D8E2E8"), "cream": ("#D9D1BA", "#F2EBD9"),
    "gray": ("#69777E", "#B9C3C8"),
    "ochre": ("#A97A2B", "#E1B95C"), "gold-red": ("#D6A72F", "#B52A32"),
    "blue-gray": ("#557B96", "#B5CBD8"), "orange-red": ("#C44B28", "#E4AA45"),
    "ice-blue": ("#5C9FBD", "#C5E5EF"), "navy": ("#23466A", "#7ABAD4"),
    "green": ("#3E8A5B", "#C8A83D"), "black-gold": ("#22272B", "#D6A72F"),
    "sand": ("#B2A17D", "#E4D6B4"), "ochre-brown": ("#8E692C", "#B52A32"),
    "orange": ("#C56A2C", "#B8D7E1"), "blue": ("#356DA8", "#B52A32"),
    "red-gold": ("#B52A32", "#D6A72F"), "pale-blue": ("#6FA9C8", "#B8C4CB"),
    "slate": ("#385467", "#B9D7E4"), "white": ("#BFC9CE", "#F1F6F8"),
    "cyan-gold": ("#147D91", "#D6A72F"), "teal-green": ("#2B806E", "#A8D4B2"),
    "mint": ("#83C7A1", "#CDE9D4"), "charcoal": ("#30383D", "#BEA16F"),
    "gold-brown": ("#B08A4C", "#D7C087"), "gold-blue": ("#D6A72F", "#356DA8"),
    "silver-white": ("#B9C2C8", "#E9F0F2"), "violet": ("#765A99", "#B9A8D0"),
    "black-gold": ("#22272B", "#D6A72F"), "gold-black": ("#D6A72F", "#22272B"),
    "gold-white": ("#D6A72F", "#E9F0F2"), "silver-gold": ("#B8C4CB", "#D6A72F"),
    "yellow-cream": ("#D3B839", "#EEE6C8"), "olive": ("#6D8247", "#CDD0AF"),
    "brown": ("#8A5638", "#E0D3B1"), "blue-black": ("#356DA8", "#22272B"),
    "teal": ("#2C8C91", "#DCEBED"), "white-gold": ("#E9F0F2", "#D6A72F"),
}

OBSERVED = {
    "clan-blood-spirit": "black, brown/tan, muted green, and dark red are visible in the Camo Specs emblem; red/brown and metallic neutrals are treated as candidates while black remains structural.",
    "clan-burrock": "the displayed emblem is predominantly black and cream with tan/gold details; the object-like tan elements are not treated as a complete official specification.",
    "clan-cloud-cobra": "black, muted purple, cyan/teal, and pale blue are visible; cyan and purple are the identity-bearing candidates.",
    "clan-coyote": "blue-gray, ochre/brown, black, and muted red-brown are visible; ochre and gold/brown are treated as the strongest candidates.",
    "clan-diamond-shark": "gray/silver, red, black, and brown/tan are visible; silver and red are the identity-bearing candidates.",
    "clan-fire-mandrill": "dark charcoal, red/orange, tan, and muted gold are visible; orange-red and gold are treated as candidates.",
    "clan-ghost-bear": "dark charcoal, silver, ice blue, and blue-gray are visible; ice blue and silver are identity-bearing candidates.",
    "clan-goliath-scorpion": "black, gold, olive green, and sand are visible; green and gold/black are treated as candidates.",
    "scorpion-empire": "black, dark red, brown, and pale gold are visible; green/red-gold interpretation remains provisional and separate from Clan Goliath Scorpion.",
    "clan-hells-horses": "cream, ochre/brown, maroon, and muted gold are visible; ochre-brown and red are candidates.",
    "clan-ice-hellion": "black, gray, ice blue, and muted maroon are visible; ice blue is supported, while orange remains a provisional supporting interpretation.",
    "clan-jade-falcon": "black/navy, vivid green, pale green, and gray are visible; green is primary and blue is a supporting candidate.",
    "clan-nova-cat": "navy, white/silver, blue-gray, red, and gold are visible; navy and red/gold are candidates.",
    "clan-sea-fox": "white, navy, pale blue, and blue-gray are visible; pale blue and silver/white are candidates.",
    "clan-smoke-jaguar": "the retrievable legacy Camo Specs asset is effectively monochrome/gray at usable resolution; no sufficiently distinct identity color set is established.",
    "clan-snow-raven": "white, black, muted green, and pale cyan/blue are visible; slate, ice blue, and white remain provisional candidates.",
    "raven-alliance": "black, white, pale blue, and blue-gray are visible; black and ice blue/white are candidates.",
    "clan-star-adder": "navy, dark blue, cream, brown, and muted blue are visible; navy is primary, with cyan/gold retained as a provisional interpretation.",
    "clan-steel-viper": "black, green, teal, and mint are visible; teal-green and mint are identity-bearing candidates.",
    "clan-stone-lion": "black, charcoal, gray-brown, and tan/gold are visible; charcoal and gold-brown are candidates.",
    "clan-widowmaker": "black, charcoal, gold, and muted brown are visible; black and gold/red remain candidates.",
    "clan-wolf": "black, red, orange, and gold are visible; red and gold are identity-bearing candidates.",
    "clan-wolf-in-exile": "the page displays the Clan Wolf emblem asset rather than a distinct Wolf-in-Exile identity mark; separate colors cannot be responsibly established.",
    "comstar": "the emblem is predominantly black, gray, and silver/white; silver and black are candidates.",
    "republic-of-the-sphere": "black, gray, silver, and pale neutral colors are visible; dark/black is supported, while gold/blue remains a provisional broader identity adaptation.",
    "word-of-blake": "the displayed emblem is predominantly black/charcoal with gray and silver highlights; black and silver/white are candidates.",
    "calderon-protectorate": "black, vivid red, and muted red/coral are visible; red and black are candidates.",
    "circinus-federation": "white, violet, gray, and dark purple are visible; violet and silver/gray are candidates.",
    "fiefdom-of-randis": "white, olive green, gray-green, and pale tan are visible; olive and silver/cream are candidates.",
    "hanseatic-league": "black, red, coral, gold, and cream are visible; red and gold/black are candidates.",
    "magistracy-of-canopus": "white, green, muted yellow-green, and gray are visible; green and gold/white are candidates.",
    "marian-hegemony": "white, navy, gray, and muted gold/tan are visible; navy and silver/gold are candidates.",
    "fronc-reaches": "white, blue, gray, and red are visible; blue, red, and gold remain candidates.",
    "nueva-castile": "olive/green, cream, and muted gray-green are visible; green and cream are candidates.",
    "niops-association": "the displayed asset is monochrome black, white, and gray; a neutral palette is supported, but no stronger chromatic identity is established.",
    "outworlds-alliance": "white, red, yellow/cream, and olive-gray are visible; red and yellow/cream are candidates.",
    "taurian-concordat": "white/cream, brown, black, and tan are visible; brown and cream are candidates.",
    "umayyad-caliphate": "no usable Camo Specs emblem asset was retrieved for independent color observation; identity remains unresolved.",
    "rim-worlds-republic": "black, red, blue, and gray are visible; red and blue-black are candidates.",
    "star-league": "white, pale cyan/teal, blue-green, and dark teal are visible; teal and white/gold are candidates.",
    "aurigan-coalition": "black, red, gold/yellow, and brown are visible; red and gold are candidates.",
}

def rgb(value):
    value = value.lstrip('#')
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))

def hex_color(values):
    return '#%02X%02X%02X' % tuple(max(0, min(255, round(x))) for x in values)

def mix(a, b, amount):
    x, y = rgb(a), rgb(b)
    return hex_color(tuple(x[i] * (1 - amount) + y[i] * amount for i in range(3)))

def luminance(value):
    channels = []
    for c in rgb(value):
        c /= 255
        channels.append(c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4)
    return .2126 * channels[0] + .7152 * channels[1] + .0722 * channels[2]

def contrast(a, b):
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return round((high + .05) / (low + .05), 2)

def ensure_text_contrast(color, text, target=4.5):
    if contrast(text, color) >= target:
        return color
    toward = '#FFFFFF' if text == '#111111' else '#000000'
    for amount in (.08, .16, .24, .32, .40, .48, .56, .64, .72, .80):
        candidate = mix(color, toward, amount)
        if contrast(text, candidate) >= target:
            return candidate
    return color

def ensure_border_contrast(color, panel, target=3):
    if contrast(color, panel) >= target:
        return color
    for amount in (.10, .20, .30, .40, .50, .60, .70, .80):
        candidate = mix(color, '#F1F6F8', amount)
        if contrast(candidate, panel) >= target:
            return candidate
    return color

def palette(identity, name, group, primary_token, secondary_token, accent_token, confidence, locator):
    if primary_token == 'unresolved':
        return None
    primary, primary_accent = TOKENS[primary_token]
    secondary, secondary_accent = TOKENS[secondary_token]
    accent, _ = TOKENS[accent_token]
    foreground, ink = '#F1F6F8', '#111111'
    roles = {
        'primary': primary, 'primary_deep': mix(primary, '#071018', .58),
        'primary_surface': mix(primary, '#071018', .34),
        'panel': mix(primary, '#0D151B', .72), 'panel_alt': mix(primary, '#172731', .55),
        'border': mix(primary_accent, '#718996', .25), 'secondary': secondary,
        'accent': accent, 'foreground': foreground, 'ink': ink,
    }
    on_primary = 'foreground' if contrast(foreground, primary) >= contrast(ink, primary) else 'ink'
    on_secondary = 'ink' if contrast(ink, secondary) >= contrast(foreground, secondary) else 'foreground'
    on_accent = 'ink' if contrast(ink, accent) >= contrast(foreground, accent) else 'foreground'
    roles['primary'] = ensure_text_contrast(primary, roles[on_primary])
    roles['secondary'] = ensure_text_contrast(secondary, roles[on_secondary])
    roles['accent'] = ensure_text_contrast(accent, roles[on_accent])
    roles['border'] = ensure_border_contrast(roles['border'], roles['panel'])
    checks = {
        'foreground_on_panel': contrast(foreground, roles['panel']),
        'foreground_on_panel_alt': contrast(foreground, roles['panel_alt']),
        'recommended_text_on_primary': contrast(roles[on_primary], roles['primary']),
        'recommended_text_on_secondary': contrast(roles[on_secondary], roles['secondary']),
        'recommended_text_on_accent': contrast(roles[on_accent], roles['accent']),
        'border_against_panel': contrast(roles['border'], roles['panel']),
    }
    note = f"{primary_token.replace('-', ' ').title()} is the provisional primary identity candidate, with {secondary_token.replace('-', ' ')} as supporting identity color(s). Exact hex values are UI adaptations from the heraldry observation, not official BattleTech color specifications."
    return {
        'faction_id': identity, 'name': name, 'group': group,
        'identity_claim_id': f'{identity}-heraldry-candidate',
        'identity_claim_status': 'RESEARCH_REQUIRED', 'palette_status': 'PROVISIONAL',
        'evidence_classification': 'UI_ADAPTATION', 'roles': roles,
        'recommended_text': {'on_panel': 'foreground', 'on_panel_alt': 'foreground', 'on_primary': on_primary, 'on_secondary': on_secondary, 'on_accent': on_accent},
        'contrast_checks': checks, 'design_note': note,
    }

def claim(identity, name, group, primary, secondary, accent, confidence, locator):
    unresolved = primary == 'unresolved'
    observed = OBSERVED[identity]
    candidates = {} if unresolved else {'primary': [primary], 'secondary': [secondary], 'neutral': [accent]}
    item = {
        'id': f'{identity}-heraldry-candidate', 'faction_id': identity, 'subject': 'government_faction_identity',
        'source_id': 'camospecs-faction-page', 'source_locator': locator,
        'image_source_locator': f'{locator} (displayed emblem/logo asset)', 'observation': observed,
        'observed_colors': [x.strip() for x in (primary + ', ' + secondary + ', ' + accent).split(',')],
        'identity_color_candidates': candidates, 'evidence_classification': 'HERALDRY_DERIVED',
        'approval_status': 'RESEARCH_REQUIRED', 'confidence': confidence, 'exact_hex_values': None,
    }
    if unresolved:
        item['interpretation'] = 'No sufficiently supported, distinct government/faction color identity has yet been established; keep unresolved pending stronger evidence.'
    else:
        item['interpretation'] = 'Observed emblem colors are treated as identity candidates only provisionally; military paint schemes and object/artwork colors are not promoted automatically.'
    return item

def yaml_block(value):
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=False, width=180).rstrip() + '\n'

def yaml_list_block(value):
    lines = yaml_block(value).rstrip('\n').splitlines()
    return '- ' + lines[0] + '\n' + '\n'.join('  ' + line for line in lines[1:])

def main():
    claims = {'schema_version': 1, 'project': 'battletech-faction-colors', 'source_set': [{'id': 'camospecs-faction-page', 'title': 'Camo Specs individual faction pages and displayed emblem/logo assets', 'publisher': 'Camo Specs Online', 'url': 'https://camospecs.com/factions/', 'accessed': ACCESS_DATE, 'role': 'visual faction/emblem evidence; military scheme context kept separate'}], 'claims': []}
    factions = {'schema_version': 1, 'factions': []}
    palette_records = []
    for identity, name, group, primary, secondary, accent, confidence, locator in IDENTITIES:
        claims['claims'].append(claim(identity, name, group, primary, secondary, accent, confidence, locator))
        factions['factions'].append({'id': identity, 'name': name, 'group': group, 'military_identity': {'status': 'not_reconstructed_from_heraldry', 'colors': None, 'note': 'Military values are intentionally kept separate from this government/faction identity research.'}, 'government_faction_identity': {'status': 'provisional' if primary != 'unresolved' else 'unresolved', 'candidate_claim_id': f'{identity}-heraldry-candidate', 'exact_hex_values': None}})
        record = palette(identity, name, group, primary, secondary, accent, confidence, locator)
        if record: palette_records.append(record)

    (ROOT / 'research/claims/remaining-identities.yaml').write_text(yaml_block(claims), encoding='utf-8')
    (ROOT / 'factions/remaining-identities.yaml').write_text(yaml_block(factions), encoding='utf-8')

    palette_path = ROOT / 'palettes/government-ui.yaml'
    text = palette_path.read_text(encoding='utf-8').rstrip() + '\n'
    if 'faction_id: clan-blood-spirit' not in text:
        text += '\n' + '\n'.join(yaml_list_block({'faction_id': p['faction_id'], 'name': p['name'], 'group': p['group'], 'identity_claim_id': p['identity_claim_id'], 'identity_claim_status': p['identity_claim_status'], 'palette_status': p['palette_status'], 'evidence_classification': p['evidence_classification'], 'roles': p['roles'], 'recommended_text': p['recommended_text'], 'contrast_checks': p['contrast_checks'], 'design_note': p['design_note']}) for p in palette_records) + '\n'
        palette_path.write_text(text, encoding='utf-8')
    print(f'claims={len(claims["claims"])} palettes_added={len(palette_records)} unresolved={sum(1 for x in IDENTITIES if x[3] == "unresolved")}')

if __name__ == '__main__':
    main()
