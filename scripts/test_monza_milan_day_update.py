from pathlib import Path
import re
import subprocess
import tempfile

html = Path('index.html').read_text()

# Day 10 must follow the new Milan -> hotel -> Monza -> hotel -> Milan flow.
map_block = re.search(r"'day-10': \{(.*?)\n  \},\n  'day-11':", html, flags=re.S)
assert map_block, 'Day 10 map block not found'
m = map_block.group(1)
for token in [
    "Milan center · Duomo / Brera",
    "Autodromo Nazionale Monza",
    "routePath: [coords.abacusHotel, coords.milan, coords.abacusHotel, coords.monza, coords.abacusHotel, coords.milan, coords.abacusHotel]",
    "routeModes: ['TRANSIT', 'TRANSIT', 'DRIVING', 'DRIVING', 'TRANSIT', 'TRANSIT']",
]:
    assert token in m, f'Missing Day 10 map token: {token}'

# Day 10 itinerary must contain the chosen races/times and two separate Milan blocks.
day10 = re.search(r"\{\n\s+id: 'day-10', number: 10, date: '2026-10-11',(.*?)\n\s+\},\n\s+\{\n\s+id: 'day-11'", html, flags=re.S)
assert day10, 'Day 10 itinerary block not found'
d = day10.group(1)
for token in [
    "Milan · בוקר רגוע במרכז",
    "13:40",
    "E4 Championship",
    "14:50",
    "C.I. Gran Turismo Sprint GT Cup",
    "Milan · ערב אחרון",
    "Sesto 1° Maggio FS",
    "הלו״ז הרשמי עדיין מוגדר provisional",
]:
    assert token in d, f'Missing Day 10 itinerary token: {token}'

# Old placeholder wording must be gone from Day 10.
for stale in [
    "שעות ייקבעו אחרי פרסום הלו״ז",
    "לוח המרוצים המפורט ליום ראשון עדיין לא פורסם",
    "נבחר את שעות המרוצים שנרצה לראות אחרי פרסום הלו״ז המלא",
]:
    assert stale not in d, f'Stale Monza wording remains: {stale}'

# Neighboring days retain their current anchors.
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

print('Monza + Milan Day 10 verification passed')
