from pathlib import Path

path = Path('index.html')
text = path.read_text()

replacements = {
    "overnight: 'Ca’ del Lasco, Bellano · לילה 1 מתוך 2'": "overnight: 'Ca’ del Lasco – Tulipano · Bellano · לילה 1 מתוך 2'",
    "overnight: 'Ca’ del Lasco, Bellano · לילה 2 מתוך 2'": "overnight: 'Ca’ del Lasco – Tulipano · Bellano · לילה 2 מתוך 2'",
    "overnight: 'ecHo Apartments & SPA · לילה 1 מתוך 2'": "overnight: 'ecHo Apartments & SPA · Bressanone · לילה 1 מתוך 2'",
    "overnight: 'ecHo Apartments & SPA · לילה 2 מתוך 2'": "overnight: 'ecHo Apartments & SPA · Bressanone · לילה 2 מתוך 2'",
    "overnight: 'Post Residence - Home of Memories - Dolomites · לילה 1 מתוך 2'": "overnight: 'Post Residence - Home of Memories - Dolomites · San Candido · לילה 1 מתוך 2'",
    "overnight: 'Post Residence - Home of Memories - Dolomites · לילה 2 מתוך 2'": "overnight: 'Post Residence - Home of Memories - Dolomites · San Candido · לילה 2 מתוך 2'",
    "overnight: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · לילה 1 מתוך 2'": "overnight: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · Pozza di Fassa · לילה 1 מתוך 2'",
    "overnight: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · לילה 2 מתוך 2'": "overnight: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · Pozza di Fassa · לילה 2 מתוך 2'",
    "overnight: 'Abacus Hotel · לילה 1 מתוך 2'": "overnight: 'Abacus Hotel · Sesto San Giovanni · לילה 1 מתוך 2'",
    "overnight: 'Abacus Hotel · לילה 2 מתוך 2'": "overnight: 'Abacus Hotel · Sesto San Giovanni · לילה 2 מתוך 2'",
}

for old, new in replacements.items():
    if old in text:
        text = text.replace(old, new, 1)
    elif new not in text:
        raise SystemExit(f'Missing overnight mapping anchor: {old}')

path.write_text(text)
