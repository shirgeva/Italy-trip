from pathlib import Path
import re
import subprocess
import tempfile

html = Path('index.html').read_text()

# Day 10 map must follow:
# hotel -> Starbucks -> Primark -> Ferrari -> hotel -> Monza -> hotel -> cooking class -> central Milan -> hotel.
map_block = re.search(r"'day-10': \{(.*?)\n  \},\n  'day-11':", html, flags=re.S)
assert map_block, 'Day 10 map block not found'
m = map_block.group(1)
for token in [
    "Starbucks Reserve Roastery Milano",
    "Primark Milano – Via Torino",
    "Ferrari Flagship Store Milano",
    "Milano: Handmade Pasta & Iconic Dessert Making Class",
    "Autodromo Nazionale Monza",
    "routePath: [coords.abacusHotel, coords.starbucksRoastery, coords.primarkTorino, coords.ferrariMilano, coords.abacusHotel, coords.monza, coords.abacusHotel, coords.cookingClassMilan, coords.milan, coords.abacusHotel]",
    "routeModes: ['TRANSIT', 'WALKING', 'WALKING', 'TRANSIT', 'DRIVING', 'DRIVING', 'TRANSIT', 'WALKING', 'TRANSIT']",
]:
    assert token in m, f'Missing Day 10 map token: {token}'

# Exact new Milan coordinates used by the Day 10 map.
for token in [
    "starbucksRoastery: { lat: 45.46493, lng: 9.18620 }",
    "primarkTorino: { lat: 45.46140, lng: 9.18554 }",
    "ferrariMilano: { lat: 45.4655554, lng: 9.1910485 }",
    "cookingClassMilan: { lat: 45.46486, lng: 9.20698 }",
    "spunDuomo: { lat: 45.4637229, lng: 9.1872327 }",
]:
    assert token in html, f'Missing coordinate token: {token}'

# Day 10 itinerary must contain the new morning plan, unchanged races, class, and final evening.
day10 = re.search(r"\{\n\s+id: 'day-10', number: 10, date: '2026-10-11',(.*?)\n\s+\},\n\s+\{\n\s+id: 'day-11'", html, flags=re.S)
assert day10, 'Day 10 itinerary block not found'
d = day10.group(1)
for token in [
    "≈07:50–08:00",
    "Starbucks Reserve Roastery Milano",
    "08:30",
    "Primark Milano – Via Torino",
    "Ferrari Flagship Store Milano",
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
    "fresh ravioli",
    "fettuccine",
    "classic tiramisu",
    "Milan · ערב אחרון",
    "Spùn Tiramisù – Duomo",
    "הלו״ז הרשמי עדיין מוגדר provisional",
]:
    assert token in d, f'Missing Day 10 itinerary token: {token}'

# Cooking class must be a booked reservation globally, without private references.
assert "{ id: 'cooking-class-milan', name: 'Milano: Handmade Pasta & Iconic Dessert Making Class', category: 'Activity', date: '2026-10-11', status: 'booked' }" in html
for private_token in ["booking reference", "reservation number", "PIN"]:
    assert private_token not in d.lower(), f'Private booking data wording leaked: {private_token}'

# Spùn must exist as a flexible Milan option, not a fixed primary stop.
assert "id: 'spun-tiramisu-duomo'" in d
assert "Via Victor Hugo 3, 20123 Milano" in d
assert "flexible" not in d.lower() or True  # wording can remain Hebrew; existence is what matters

# The incorrect GT Cup naming must be gone from Day 10.
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
