from pathlib import Path
import re
import subprocess
import tempfile

html = Path('index.html').read_text()

# Day 10 map must follow:
# hotel -> Starbucks -> Primark -> Spùn -> Venchi -> Ferrari -> UNIQLO -> hotel -> Monza -> hotel
# -> cooking class -> Gelateria Umberto -> central Milan -> hotel.
map_block = re.search(r"'day-10': \{(.*?)\n  \},\n  'day-11':", html, flags=re.S)
assert map_block, 'Day 10 map block not found'
m = map_block.group(1)
for token in [
    "Starbucks Reserve Roastery Milano",
    "Primark Milano – Via Torino",
    "Spùn Tiramisù – Duomo",
    "Venchi Milano Mengoni",
    "Ferrari Flagship Store Milano",
    "UNIQLO Piazza Cordusio",
    "Autodromo Nazionale Monza",
    "Milano: Handmade Pasta & Iconic Dessert Making Class",
    "Gelateria Umberto 1934 – affogato",
    "routePath: [coords.abacusHotel, coords.starbucksRoastery, coords.primarkTorino, coords.spunDuomo, coords.venchiMengoni, coords.ferrariMilano, coords.uniqloCordusio, coords.abacusHotel, coords.monza, coords.abacusHotel, coords.cookingClassMilan, coords.gelateriaUmberto, coords.milan, coords.abacusHotel]",
    "routeModes: ['TRANSIT', 'WALKING', 'WALKING', 'WALKING', 'WALKING', 'WALKING', 'TRANSIT', 'DRIVING', 'DRIVING', 'TRANSIT', 'WALKING', 'WALKING', 'TRANSIT']",
]:
    assert token in m, f'Missing Day 10 map token: {token}'

# Exact/new Milan coordinates used by the Day 10 map.
for token in [
    "starbucksRoastery: { lat: 45.46493, lng: 9.18620 }",
    "primarkTorino: { lat: 45.46140, lng: 9.18554 }",
    "ferrariMilano: { lat: 45.4655554, lng: 9.1910485 }",
    "cookingClassMilan: { lat: 45.46486, lng: 9.20698 }",
    "spunDuomo: { lat: 45.4637229, lng: 9.1872327 }",
    "venchiMengoni:",
    "uniqloCordusio:",
    "gelateriaUmberto: { lat: 45.4618935, lng: 9.2065548 }",
]:
    assert token in html, f'Missing coordinate token: {token}'

# Hero must be concise, not a duplicate of the timeline.
day10 = re.search(r"\{\n\s+id: 'day-10', number: 10, date: '2026-10-11',(.*?)\n\s+\},\n\s+\{\n\s+id: 'day-11'", html, flags=re.S)
assert day10, 'Day 10 itinerary block not found'
d = day10.group(1)
assert "title: 'Milan (שופינג) → Monza → Milan'" in d
assert "routeLabel: 'שופינג בבוקר ב־Milan · מרוצים ב־Monza · סדנת בישול · ערב אחרון ב־Milan'" in d

# Detailed timeline remains the source of truth.
for token in [
    "≈07:50–08:00",
    "Starbucks Reserve Roastery Milano",
    "08:30–08:55",
    "Primark Milano – Via Torino",
    "≈09:05–09:55",
    "Spùn Tiramisù – Duomo",
    "Via Victor Hugo 3, 20123 Milano",
    "Venchi Milano Mengoni",
    "Via Giuseppe Mengoni 1, 20121 Milano",
    "Ferrari Flagship Store Milano",
    "UNIQLO Piazza Cordusio",
    "Via Cordusio 2, 20123 Milano MI, Italy",
    "≈10:50–11:15",
    "13:40",
    "E4 Championship",
    "14:50",
    "Italian GT Sprint GT3",
    "≈17:15–17:25",
    "San Babila",
    "Milano: Handmade Pasta & Iconic Dessert Making Class",
    "18:15",
    "18:30–21:00",
    "Cook & Walk Srl",
    "Viale Premuda 13, 20129 Milano MI, Italy",
    "Gelateria Umberto 1934 – affogato",
    "אם לא היינו כאן כבר בערב של 10.10",
    "Milan · ערב אחרון",
    "התוכנית עדיין אינה סופית ויש לבדוק שוב סמוך ל־11.10",
]:
    assert token in d, f'Missing Day 10 itinerary token: {token}'

# Fixed-route food stops should not also be duplicated as area-option cards.
for fixed_option_id in [
    "id: 'venchi-mengoni'",
    "id: 'spun-tiramisu-duomo'",
    "id: 'gelateria-umberto'",
    "id: 'uniqlo-cordusio'",
]:
    assert fixed_option_id not in d, f'Fixed Day 10 stop still duplicated in area options: {fixed_option_id}'

# UNIQLO remains a planned timeline stop. Morning flexibility now lives in the relevant stop notes,
# rather than a duplicated top-of-day alert.
assert "id: 'uniqlo-cordusio-morning'" in d
assert "status: 'planned'" in d
assert "אם כבר היינו כאן בערב 10.10 פשוט מדלגים וממשיכים במסלול." in d
assert "אם כבר היינו כאן בערב 10.10 פשוט מדלגים וממשיכים." in d
assert "אם לא היינו כאן כבר בערב של 10.10" in d

# Lindt and Enrico Rizzi remain area options only.
for option_id in ["id: 'lindt-via-dante'", "id: 'enrico-rizzi-factory'"]:
    assert option_id in d, f'Required Milan area option missing: {option_id}'

# Cooking class remains booked globally, without private references.
assert "{ id: 'cooking-class-milan', name: 'Milano: Handmade Pasta & Iconic Dessert Making Class', category: 'Activity', date: '2026-10-11', status: 'booked' }" in html
for private_token in ["booking reference", "reservation number", "PIN"]:
    assert private_token not in d.lower(), f'Private booking data wording leaked: {private_token}'

# Incorrect GT Cup naming must stay gone.
assert "GT Cup" not in d, 'Incorrect GT Cup naming still appears in Day 10'

# Neighboring days remain intact.
for sentinel in [
    "id: 'day-9', number: 9, date: '2026-10-10'",
    "id: 'day-11', number: 11, date: '2026-10-12'",
    "drive-limone-abacus-day9",
    "drive-abacus-mxp",
]:
    assert sentinel in html, f'Neighboring itinerary sentinel missing: {sentinel}'

# Inline JS still parses.
inline_scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, flags=re.S | re.I)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as tmp:
    tmp.write('\n'.join(inline_scripts))
    js_path = tmp.name
subprocess.run(['node', '--check', js_path], check=True)

print('Day 10 Milan + Monza + cooking class verification passed')
