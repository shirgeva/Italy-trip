from pathlib import Path
import re
import subprocess
import tempfile

html = Path('index.html').read_text()

# October 7 / Day 6 must not contain any Loacker suggestion.
day6 = re.search(r"\{\n\s+id: 'day-6', number: 6, date: '2026-10-07',(.*?)\n\s+\},\n\s+\{\n\s+id: 'day-7'", html, flags=re.S)
assert day6, 'Day 6 / October 7 block not found'
assert 'Loacker' not in day6.group(1), 'Loacker still appears on October 7'
assert "id: 'loacker-olang'" not in day6.group(1), 'October 7 Loacker optional stop still exists'

# Day 3 Loacker plan must remain untouched.
day3 = re.search(r"\{\n\s+id: 'day-3', number: 3, date: '2026-10-04',(.*?)\n\s+\},\n\s+\{\n\s+id: 'day-4'", html, flags=re.S)
assert day3, 'Day 3 block not found'
for token in [
    "Loacker Café Bozen Twenty · אופציונלי",
    "id: 'loacker-twenty'",
    "drive-elena-loacker",
    "drive-loacker-funes",
]:
    assert token in day3.group(1), f'Day 3 Loacker content changed or missing: {token}'

# Every Lago di Carezza option in the itinerary must clearly be conditional/optional
# and display the requested warning text with an attention icon.
carezza_blocks = re.findall(
    r"\{\n\s+id: 'carezza-option',\n\s+name: 'Lago di Carezza',(.*?)\n\s+\},",
    html,
    flags=re.S,
)
assert len(carezza_blocks) == 2, f'Expected 2 Lago di Carezza option blocks, found {len(carezza_blocks)}'
warning = (
    '⚠️ חשוב לבדוק לפני הנסיעה: באוקטובר מפלס המים ב-Lago di Carezza נמצא בדרך כלל בשפל השנתי, '
    'ולעיתים האגם נראה קטן משמעותית לעומת התמונות מהקיץ. כמה ימים לפני הביקור יש לבדוק מצלמה עדכנית / '
    'תמונות עדכניות ולוודא שיש מספיק מים וששווה להגיע. אם המפלס נמוך מאוד – לוותר על העצירה ולא לנסוע במיוחד.'
)
for block in carezza_blocks:
    assert "category: 'אגם / טבע · אופציונלי / מותנה'" in block, 'Carezza is not marked optional/conditional'
    assert warning in block, 'Carezza warning text is missing or changed'

# Inline JavaScript must still parse.
inline_scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, flags=re.S | re.I)
assert inline_scripts, 'No inline JavaScript found'
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as tmp:
    tmp.write('\n'.join(inline_scripts))
    js_path = tmp.name
subprocess.run(['node', '--check', js_path], check=True)

print('Carezza + October 7 Loacker verification passed')
