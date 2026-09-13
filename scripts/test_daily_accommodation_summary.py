from pathlib import Path
import re
import subprocess
import tempfile

html = Path('index.html').read_text()

# Checklist: only the accommodation-bases task changes from its current false state.
assert "{ id: 'hotels', label: 'לסגור את בסיסי הלינה לאורך המסלול', done: true }" in html, \
    'Hotel-bases checklist item is not marked done'

# The old top-level metrics must not be rendered by the daily summary component.
match = re.search(r"function dailySummary\(day\) \{(.*?)\n\}\n\nfunction stopTypeLabel", html, flags=re.S)
assert match, 'dailySummary function not found'
summary_source = match.group(1)
for forbidden in ["יוצאים מ־", "נהיגה", "עצירות", "הליכה", "destinationCount"]:
    assert forbidden not in summary_source, f'Old daily summary metric still rendered: {forbidden}'

# Day 11 has no overnight value, so the summary function must omit the card entirely.
assert "if (!day.overnight) return ''" in summary_source

# Days 1–10 must retain the exact requested accommodation/night mapping in their existing overnight fields.
expected = [
    "overnight: 'Ca’ del Lasco – Tulipano · Bellano · לילה 1 מתוך 2'",
    "overnight: 'Ca’ del Lasco – Tulipano · Bellano · לילה 2 מתוך 2'",
    "overnight: 'ecHo Apartments & SPA · Bressanone · לילה 1 מתוך 2'",
    "overnight: 'ecHo Apartments & SPA · Bressanone · לילה 2 מתוך 2'",
    "overnight: 'Post Residence - Home of Memories - Dolomites · San Candido · לילה 1 מתוך 2'",
    "overnight: 'Post Residence - Home of Memories - Dolomites · San Candido · לילה 2 מתוך 2'",
    "overnight: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · Pozza di Fassa · לילה 1 מתוך 2'",
    "overnight: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · Pozza di Fassa · לילה 2 מתוך 2'",
    "overnight: 'Abacus Hotel · Sesto San Giovanni · לילה 1 מתוך 2'",
    "overnight: 'Abacus Hotel · Sesto San Giovanni · לילה 2 מתוך 2'",
    "overnight: null",
]
for token in expected:
    assert token in html, f'Missing expected overnight mapping: {token}'

# Compact accommodation presentation only: secondary label + strong hotel name + night count.
for token in [
    'class="day-lodging-card"',
    'class="day-lodging-label">לינה',
    'class="day-lodging-hotel"',
    'class="day-lodging-night"',
    '.day-lodging-card',
    'font-size: 16px',
]:
    assert token in html, f'Missing compact lodging UI token: {token}'

# Old day-summary markup/classes should be gone from the production HTML/CSS.
assert 'class="day-summary' not in html
assert '.day-summary {' not in html
assert '.empty-summary' not in html

# Inline JS must still parse after the UI refactor.
inline_scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, flags=re.S | re.I)
assert inline_scripts, 'No inline JavaScript found'
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as tmp:
    tmp.write('\n'.join(inline_scripts))
    js_path = tmp.name
subprocess.run(['node', '--check', js_path], check=True)

print('Daily accommodation summary verification passed')
