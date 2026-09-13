from pathlib import Path

p = Path('index.html')
s = p.read_text()

if "id: 'dolomiti-exclusive-night1'" in s:
    raise SystemExit(0)

# Exact property map point from the verified 55 Strada Dolomites listing.
coord_anchor = "  pozza: { lat: 46.4297, lng: 11.6876 },"
coord_new = "  pozza: { lat: 46.4297, lng: 11.6876 },\n  dolomitiExclusive: { lat: 46.42775, lng: 11.682784 },"
if coord_anchor not in s:
    raise SystemExit('Pozza coordinate anchor not found')
s = s.replace(coord_anchor, coord_new, 1)

# Update daily maps for Oct 8-10 only.
map_start = s.index("  'day-7': {")
map_end = s.index("  'day-10': {", map_start)
new_maps = """  'day-7': {
    points: [
      { name: 'Post Residence · San Candido', label: '08:00 · יציאה מערבה', ...coords.postResidence },
      { name: 'Passo Sella · חניה', label: '≈09:25–09:35 · מכאן ממשיכים ברגל', ...coords.passoSella },
      { name: 'Rifugio Friedrich August', label: '≈09:50–11:00 · TO VERIFY', ...coords.friedrichAugust },
      { name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', label: 'Pozza di Fassa · הגעה סביב 11:50–12:10 · לילה 1 מתוך 2', ...coords.dolomitiExclusive },
    ],
    routePath: [coords.postResidence, coords.passoSella, coords.friedrichAugust, coords.passoSella, coords.dolomitiExclusive],
  },
  'day-8': {
    points: [
      { name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', label: 'בסיס לינה · Pozza di Fassa', ...coords.dolomitiExclusive },
      { name: 'Lago di Carezza · אופציונלי', label: 'כ־16–20 דק׳ מהמלון', ...coords.carezza },
      { name: 'QC Terme Dolomiti', label: 'ערב · כ־2–5 דק׳ נסיעה מהמלון', ...coords.pozza },
      { name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', label: 'חזרה אחרי הספא · לילה 2 מתוך 2', ...coords.dolomitiExclusive },
    ],
    routePath: [coords.dolomitiExclusive, coords.carezza, coords.pozza, coords.dolomitiExclusive],
  },
  'day-9': {
    points: [
      { name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', label: '10.10 · צ׳ק־אאוט ויציאה לצפון Lake Garda', ...coords.dolomitiExclusive },
      { name: 'Parco Grotta Cascata Varone', label: 'כ־1:50–2:05 שעות · יעד הגעה ≈09:00', ...coords.varone },
      { name: 'Riva del Garda', label: 'חניה + שמירת מזוודות · טיול בעיירה', ...coords.riva },
      { name: 'Limone sul Garda', label: 'הגעה בשייט או באוטובוס · עדיין בתכנון', ...coords.limone },
      { name: 'Milan / Sesto San Giovanni · אזור לינה משוער', label: 'נסיעה אחרי החזרה ל־Riva ואיסוף המזוודות', ...coords.sesto },
    ],
    routePath: [coords.dolomitiExclusive, coords.varone, coords.riva, coords.limone, coords.riva, coords.sesto],
  },
"""
s = s[:map_start] + new_maps + s[map_end:]

# Day 7: hotel becomes the actual arrival / overnight point.
d7_start = s.index("      id: 'day-7', number: 7, date: '2026-10-08'")
d7_end = s.index("      id: 'day-8', number: 8, date: '2026-10-09'", d7_start)
d7 = s[d7_start:d7_end]
for old, new in {
"      routeLabel: 'Post Residence, San Candido → Passo Sella → Rifugio Friedrich August → Pozza di Fassa / Val di Fassa',": "      routeLabel: 'Post Residence, San Candido → Passo Sella → Rifugio Friedrich August → DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE, Pozza di Fassa',",
"      overnight: 'Pozza di Fassa / Val di Fassa · לילה 1 מתוך 2',": "      overnight: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · לילה 1 מתוך 2',",
}.items():
    if old not in d7:
        raise SystemExit(f'Day 7 header anchor missing: {old}')
    d7 = d7.replace(old, new, 1)

old_drive = "        drive('drive-passo-sella-pozza', 'Passo Sella → Pozza di Fassa / Val di Fassa', 'כ־30–40 דקות · משוער', '≈11:20–11:50/12:00', { notes: 'מכאן ממשיכים לעמק ולבסיס הלינה הבא.' }),"
new_drive = "        drive('drive-passo-sella-pozza', 'Passo Sella → DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE, Pozza di Fassa', 'כ־25–30 דקות', '≈11:20–11:45/11:50', { notes: 'המלון נמצא בתוך Pozza di Fassa, ב־55 Strada Dolomites. זמן הנסיעה מ־Passo Sella למרכז Pozza הוא סביב 28 דקות, ולכן נשמור טווח של 25–30 דקות.' }),"
if old_drive not in d7:
    raise SystemExit('Day 7 final drive anchor missing')
d7 = d7.replace(old_drive, new_drive, 1)

old_arrivals = """        place({ id: 'pozza-arrival-day7', type: 'activity', name: 'Pozza di Fassa / Val di Fassa · הגעה לאזור', time: '≈11:50–12:10', status: 'planning', coordinates: coords.pozza, details: { notes: 'מגיעים לאזור סביב הצהריים. שאר האופציות שכבר שמרנו ליום הזה נשארות פתוחות לבחירה בהתאם למזג האוויר, אנרגיה ושעות הפעילות.' } }),
        place({ id: 'pozza-overnight-1', type: 'hotel', name: 'Pozza di Fassa / Val di Fassa · לילה 1 מתוך 2', time: 'ערב', status: 'to-book', coordinates: coords.pozza, details: { notes: 'זה הלילה הראשון מתוך שניים באזור הספא.' } }),"""
new_arrivals = """        place({ id: 'dolomiti-exclusive-arrival', type: 'hotel', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', time: '≈11:50–12:10', status: 'planning', coordinates: coords.dolomitiExclusive, details: { address: '55 Strada Dolomites, 38036 Pozza di Fassa, Italy', parking: 'חניה פרטית חינם במקום', notes: 'בסיס הלינה ל־8–10.10 · 2 לילות. המלון נמצא בתוך Pozza di Fassa. שאר האופציות שכבר שמרנו ליום הזה נשארות פתוחות לבחירה בהתאם למזג האוויר, אנרגיה ושעות הפעילות.' } }),
        place({ id: 'dolomiti-exclusive-night1', type: 'hotel', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · לילה 1 מתוך 2', time: 'ערב', status: 'planning', coordinates: coords.dolomitiExclusive, details: { address: '55 Strada Dolomites, 38036 Pozza di Fassa, Italy', notes: 'לילה ראשון מתוך שניים באזור Val di Fassa.' } }),"""
if old_arrivals not in d7:
    raise SystemExit('Day 7 arrival anchors missing')
d7 = d7.replace(old_arrivals, new_arrivals, 1)
s = s[:d7_start] + d7 + s[d7_end:]

# Day 8: make the hotel the clear start/end base while preserving all existing attractions/options.
d8_start = s.index("      id: 'day-8', number: 8, date: '2026-10-09'")
d8_end = s.index("      id: 'day-9', number: 9, date: '2026-10-10'", d8_start)
d8 = s[d8_start:d8_end]
for old, new in {
"      startBase: 'Pozza di Fassa / Val di Fassa',": "      startBase: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE, Pozza di Fassa',",
"      routeLabel: 'Val di Fassa / Pozza di Fassa → יום טיול באזור → QC Terme Dolomiti',": "      routeLabel: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → יום טיול באזור Val di Fassa → QC Terme Dolomiti → hotel',",
"      overnight: 'Pozza di Fassa / Val di Fassa · לילה 2 מתוך 2',": "      overnight: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · לילה 2 מתוך 2',",
"      drivingTime: 'ייקבע לפי המסלול שנבחר באזור',": "      drivingTime: 'אם משלבים Lago di Carezza: כ־35–45 דקות נהיגה מצטברת + נסיעה קצרה ל־QC Terme',",
}.items():
    if old not in d8:
        raise SystemExit(f'Day 8 header anchor missing: {old}')
    d8 = d8.replace(old, new, 1)

d8 = d8.replace(
"            notes: 'מ־Pozza di Fassa כ־16 דק׳ נסיעה. זו האופציה הפשוטה והזולה: רכב + חניה בלבד. אם נחליט להמשיך גם ל־Rosengarten הגבוה, שם כבר נכנס רכבל.'",
"            notes: 'מ־DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE כ־16–20 דק׳ נסיעה. זו האופציה הפשוטה והזולה: רכב + חניה בלבד. אם נחליט להמשיך גם ל־Rosengarten הגבוה, שם כבר נכנס רכבל.'",
1)

old_alert = "      alerts: ['זה הערב האחרון בדולומיטים: QC Terme Dolomiti נשאר לסוף היום, ואחריו ישנים שוב ליד הספא.'],"
new_alert = "      alerts: ['זה הערב האחרון בדולומיטים: QC Terme Dolomiti נשאר לסוף היום, ואחריו חוזרים ל־DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE. המלון נמצא פחות מקילומטר מהספא — בערך 2–5 דקות נסיעה, או הליכה קצרה אם נעדיף.'],"
if old_alert not in d8:
    raise SystemExit('Day 8 alert anchor missing')
d8 = d8.replace(old_alert, new_alert, 1)

old_stops = """      stops: [
        place({ id: 'val-di-fassa-day', type: 'activity', name: 'יום טיול באזור Val di Fassa · בתכנון', nameDirection: 'rtl', time: 'בוקר / צהריים', status: 'planning', coordinates: coords.pozza, details: { notes: 'נבחר בהמשך את האטרקציות המדויקות מתוך האפשרויות באזור.' } }),
        place({ id: 'qc-terme', type: 'activity', name: 'QC Terme Dolomiti', time: 'ערב', duration: 'בהתאם להזמנה', status: 'to-book', coordinates: coords.pozza, details: { reservation: 'כניסת ערב · שעה מדויקת תיקבע בעת ההזמנה', notes: 'הספא סוגר את פרק הדולומיטים בערב של 9.10.' } }),
        place({ id: 'pozza-overnight-2', type: 'hotel', name: 'Pozza di Fassa / Val di Fassa · לילה 2 מתוך 2', time: 'אחרי הספא', status: 'to-book', coordinates: coords.pozza, details: { notes: 'לינה ליד הספא; בבוקר 10.10 יוצאים לצפון Lake Garda.' } }),
      ],"""
new_stops = """      stops: [
        place({ id: 'dolomiti-exclusive-day8-start', type: 'hotel', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', time: 'בוקר', status: 'planning', coordinates: coords.dolomitiExclusive, details: { address: '55 Strada Dolomites, 38036 Pozza di Fassa, Italy', parking: 'חניה פרטית חינם במקום', notes: 'מתחילים את יום הטיול מתוך Pozza di Fassa. Lago di Carezza נמצא כ־16–20 דקות נסיעה.' } }),
        place({ id: 'val-di-fassa-day', type: 'activity', name: 'יום טיול באזור Val di Fassa · בתכנון', nameDirection: 'rtl', time: 'בוקר / צהריים', status: 'planning', coordinates: coords.pozza, details: { notes: 'נבחר בהמשך את האטרקציות המדויקות מתוך האפשרויות באזור. Lago di Carezza / Rosengarten נשארות האופציות הקיימות.' } }),
        place({ id: 'qc-terme', type: 'activity', name: 'QC Terme Dolomiti', time: 'ערב', duration: 'בהתאם להזמנה', status: 'to-book', coordinates: coords.pozza, details: { reservation: 'כניסת ערב · שעה מדויקת תיקבע בעת ההזמנה', address: 'Strada di Bagnes 21, 38036 Pozza di Fassa, Italy', notes: 'הספא נמצא פחות מקילומטר מהמלון: בערך 2–5 דקות ברכב. הספא סוגר את פרק הדולומיטים בערב של 9.10.' } }),
        place({ id: 'dolomiti-exclusive-night2', type: 'hotel', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · לילה 2 מתוך 2', time: 'אחרי הספא', status: 'planning', coordinates: coords.dolomitiExclusive, details: { address: '55 Strada Dolomites, 38036 Pozza di Fassa, Italy', notes: 'חזרה קצרה מהספא; בבוקר 10.10 יוצאים לצפון Lake Garda.' } }),
      ],"""
if old_stops not in d8:
    raise SystemExit('Day 8 stops block missing')
d8 = d8.replace(old_stops, new_stops, 1)
s = s[:d8_start] + d8 + s[d8_end:]

# Day 9: checkout from the exact hotel and recalculate the first drive.
d9_start = s.index("      id: 'day-9', number: 9, date: '2026-10-10'")
d9_end = s.index("      id: 'day-10', number: 10, date: '2026-10-11'", d9_start)
d9 = s[d9_start:d9_end]
for old, new in {
"      startBase: 'Pozza di Fassa / QC Terme Dolomiti',": "      startBase: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE, Pozza di Fassa',",
"      routeLabel: 'Pozza di Fassa → Varone Waterfall → Riva del Garda ⇄ Limone sul Garda → Milan / Sesto San Giovanni',": "      routeLabel: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → Varone Waterfall → Riva del Garda ⇄ Limone sul Garda → Milan / Sesto San Giovanni',",
}.items():
    if old not in d9:
        raise SystemExit(f'Day 9 header anchor missing: {old}')
    d9 = d9.replace(old, new, 1)

old_first_drive = "        drive('drive-pozza-varone', 'Pozza di Fassa → Parco Grotta Cascata Varone', 'כ־2 שעות · משוער', 'יציאה מוקדמת', { notes: 'המטרה היא להגיע לפתיחה סביב 09:00.' }),"
new_first_drive = "        drive('drive-pozza-varone', 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → Parco Grotta Cascata Varone', 'כ־1:50–2:05 שעות', 'יציאה סביב 07:00 אם מכוונים לפתיחה', { notes: 'Pozza di Fassa → Riva del Garda היא בערך שעתיים ברכב, ו־Varone נמצא מעט לפני / מעל Riva. אם המטרה נשארת להגיע לפתיחה סביב 09:00, כדאי לצאת מהמלון בערך ב־07:00 ולהשאיר מעט מרווח לכביש.' }),"
if old_first_drive not in d9:
    raise SystemExit('Day 9 first drive anchor missing')
d9 = d9.replace(old_first_drive, new_first_drive, 1)
s = s[:d9_start] + d9 + s[d9_end:]

# Overview / accommodation consistency.
old_summary = "  routeSummary: 'Milan Malpensa → Bellano / Ca’ del Lasco → Bressanone / ecHo Apartments & SPA → Alpe di Siusi / Val Gardena → San Candido / Post Residence → Pozza di Fassa / QC Terme Dolomiti → Varone Waterfall → Riva del Garda → Limone sul Garda → Milan / Sesto San Giovanni → Monza → Milan Malpensa',"
new_summary = "  routeSummary: 'Milan Malpensa → Bellano / Ca’ del Lasco → Bressanone / ecHo Apartments & SPA → Alpe di Siusi / Val Gardena → San Candido / Post Residence → Pozza di Fassa / DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → QC Terme Dolomiti → Varone Waterfall → Riva del Garda → Limone sul Garda → Milan / Sesto San Giovanni → Monza → Milan Malpensa',"
if old_summary not in s:
    raise SystemExit('Route summary anchor missing')
s = s.replace(old_summary, new_summary, 1)

old_global_seq = "    coords.treCime,\n    coords.pozza,\n    coords.pozza,\n    coords.varone,"
new_global_seq = "    coords.treCime,\n    coords.dolomitiExclusive,\n    coords.dolomitiExclusive,\n    coords.varone,"
if old_global_seq not in s:
    raise SystemExit('Global route sequence anchor missing')
s = s.replace(old_global_seq, new_global_seq, 1)

res_anchor = "    { id: 'hotel-san-candido', name: 'Post Residence - Home of Memories - Dolomites · San Candido', category: 'Hotels', date: '2026-10-06', status: 'planning' },\n    { id: 'hotels-remaining', name: 'שאר הלינות לאורך המסלול', category: 'Hotels', status: 'to-book' },"
res_new = "    { id: 'hotel-san-candido', name: 'Post Residence - Home of Memories - Dolomites · San Candido', category: 'Hotels', date: '2026-10-06', status: 'planning' },\n    { id: 'hotel-pozza', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · Pozza di Fassa', category: 'Hotels', date: '2026-10-08', status: 'planning' },\n    { id: 'hotels-remaining', name: 'שאר הלינות לאורך המסלול', category: 'Hotels', status: 'to-book' },"
if res_anchor not in s:
    raise SystemExit('Reservation anchor missing')
s = s.replace(res_anchor, res_new, 1)

p.write_text(s)
