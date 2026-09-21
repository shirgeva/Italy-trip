from pathlib import Path
import re

html = Path('index.html').read_text()

description_ids = [
    'bellano-evening-day1',
    'orrido-day2-final',
    'bellagio-day2-final',
    'villa-carlotta-flex-day2-final',
    'menaggio-day2-final',
    'varenna-evening-day2',
    'soprabolzano-day3',
    'bolzano-center-day3',
    'loacker-walther-day3',
    'val-di-funes',
    'seceda',
    'ortisei-afternoon',
    'alpe-cable-up',
    'gostner-schwaige-day5',
    'passo-gardena',
    'tre-cime',
    'misurina',
    'braies',
    'funbob-baranci',
    'passo-sella-parking-day7',
    'val-san-nicolo-core',
    'qc-terme',
    'varone-waterfall',
    'riva-day',
    'ciclopista-reamol',
    'limone',
    'starbucks-roastery-morning',
    'spun-tiramisu-morning',
    'venchi-mengoni-morning',
    'ferrari-store-morning',
    'monza-event',
    'cooking-class-milan',
    'gelateria-umberto-evening',
    'milan-evening',
]
for stop_id in description_ids:
    pattern = rf"place\(\{{ id: '{re.escape(stop_id)}'.*?description: '"
    assert re.search(pattern, html, flags=re.S), f'Missing visible description for {stop_id}'

assert "stop.description ? `<p class=\"stop-description\">" in html
assert ".stop-description {" in html

for token in [
    "אחד מסמלי הדולומיטים — קבוצת שלוש פסגות סלע דרמטיות",
    "רכס ונקודת תצפית גבוהה מעל Val Gardena",
    "מעבר הרים גבוה בין Val Gardena ל־Alta Badia",
    "מעבר הרים גבוה ומרשים בין Val Gardena ל־Val di Fassa",
    "עמק אלפיני ירוק ופתוח ב־Val di Fassa",
    "Funbob היא מגלשת הרים על מסילה",
    "מפל גבוה נופל בתוך ערוץ ומערה צרה בסלע",
    "שביל אופניים והולכי רגל התלוי על מצוק מעל Lake Garda",
    "מתחם ספא ו־wellness גדול ב־Pozza di Fassa",
]:
    assert token in html, f'Missing content-clarity token: {token}'

for name in [
    "Tre Cime di Lavaredo",
    "Seceda",
    "Passo Gardena",
    "Passo Sella",
    "Passo Pordoi + Sass Pordoi",
    "Agritur Agua Biencia",
    "Abbazia di Novacella / Kloster Neustift – Stiftskeller",
    "Hotel Weingut Pacherhof",
    "Monte Baranci + Funbob",
    "QC Spa Dolomiti",
    "UNIQLO Piazza Cordusio",
    "Ferrari Flagship Store Milano",
]:
    assert name in html, f'Proper place name changed or missing: {name}'

for bad in [
    "Historic abbey with its own wines",
    "Historic wine estate near Bressanone",
    "Drive from Passo Sella to Passo Pordoi",
    "Local agriturismo / farm near Pera di Fassa",
    "Main resort town in upper Val di Fassa",
    "Monitoring availability —",
    "Preferred: לוקחים",
    "Alternative: לבקש",
    "OPTIONAL / FLEXIBLE / WALK-IN",
    "TO VERIFY CLOSER TO DATE",
    "Morning Milan route is flexible",
    "BOOKED · 2 adults · English",
    "הלו״ז הרשמי עדיין מוגדר provisional",
]:
    assert bad not in html, f'Old English/mixed user-facing copy returned: {bad}'

for status in ["booked", "must", "to-book", "considering", "optional", "planning", "planned", "attention"]:
    assert f"'{status}'" in html or f"{status}:" in html

print('Content clarity + Hebrew copy verification passed')
