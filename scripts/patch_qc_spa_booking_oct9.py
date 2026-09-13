from pathlib import Path

p = Path('index.html')
s = p.read_text()

if "qc-spa-booked-1700" in s:
    raise SystemExit(0)

# Exact QC Spa Dolomiti point from the official/partner listing.
coord_anchor = "  pozza: { lat: 46.4297, lng: 11.6876 },"
if coord_anchor not in s:
    raise SystemExit('Pozza coordinate anchor missing')
s = s.replace(coord_anchor, coord_anchor + "\n  qcSpa: { lat: 46.424776, lng: 11.687688 },", 1)

# Update only Oct 9 map labels/path.
map_start = s.index("  'day-8': {")
map_end = s.index("  'day-9': {", map_start)
new_map = """  'day-8': {
    points: [
      { name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', label: 'בוקר איטי · בסיס לינה', ...coords.dolomitiExclusive },
      { name: 'Vidor · Val San Nicolò shuttle', label: 'סוף הבוקר · תוכנית עיקרית', ...coords.vidor },
      { name: 'Val San Nicolò / Baita alle Cascate', label: 'טיול רגוע · כ־2.5–3 שעות כולל השאטל', ...coords.baitaCascate },
      { name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', label: 'אחר הצהריים · wellness / מנוחה', ...coords.dolomitiExclusive },
      { name: 'QC Spa Dolomiti', label: '16:40–16:50 הגעה · 17:00 כניסה הוזמנה', ...coords.qcSpa },
      { name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', label: 'חזרה אחרי הספא · לילה 2 מתוך 2', ...coords.dolomitiExclusive },
    ],
    routePath: [coords.dolomitiExclusive, coords.vidor, coords.baitaCascate, coords.vidor, coords.dolomitiExclusive, coords.qcSpa, coords.dolomitiExclusive],
  },
"""
s = s[:map_start] + new_map + s[map_end:]

# Update only Day 8 / Oct 9 content.
d8_start = s.index("      id: 'day-8', number: 8, date: '2026-10-09'")
d8_end = s.index("      id: 'day-9', number: 9, date: '2026-10-10'", d8_start)
d8 = s[d8_start:d8_end]

for old, new in {
"      title: 'Val San Nicolò + hotel + QC Terme Dolomiti',": "      title: 'Val San Nicolò + hotel + QC Spa Dolomiti',",
"      overviewPoint: 'Val San Nicolò + QC Terme Dolomiti',": "      overviewPoint: 'Val San Nicolò + QC Spa Dolomiti',",
"      routeLabel: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → Val San Nicolò → hotel / wellness → QC Terme Dolomiti → hotel',": "      routeLabel: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → Val San Nicolò → hotel / wellness → QC Spa Dolomiti → hotel',",
"      drivingTime: 'נהיגה מינימלית · כמה דקות ל־Vidor ול־QC Terme + shuttle ל־Val San Nicolò',": "      drivingTime: 'נהיגה מינימלית · כמה דקות ל־Vidor + shuttle ל־Val San Nicolò · QC Spa כ־8 דקות הליכה מהמלון',",
"      highlights: ['Val San Nicolò · תוכנית עיקרית', 'Hotel / wellness · זמן מכוון', 'QC Terme Dolomiti · תוכנית עיקרית'],": "      highlights: ['Val San Nicolò · תוכנית עיקרית', 'Hotel / wellness · זמן מכוון', 'QC Spa Dolomiti · 17:00 · הוזמן'],",
}.items():
    if old not in d8:
        raise SystemExit(f'Day 8 header anchor missing: {old}')
    d8 = d8.replace(old, new, 1)

d8 = d8.replace(
    "'יום רגוע בכוונה: חוויה אחת בטבע → זמן משמעותי במלון → QC Terme Dolomiti. אין אטרקציה קבועה נוספת בין Val San Nicolò לספא.'",
    "'יום רגוע בכוונה: חוויה אחת בטבע → זמן משמעותי במלון → QC Spa Dolomiti ב־17:00. אין אטרקציה קבועה נוספת בין Val San Nicolò לספא.'",
    1,
)

old_relax = "place({ id: 'hotel-relax-day8', type: 'activity', name: 'זמן מלון / wellness / מנוחה', nameDirection: 'rtl', time: 'אחר הצהריים', duration: 'בלוק זמן משמעותי', status: 'planned', coordinates: coords.dolomitiExclusive, details: { notes: 'זמן מכוון ליהנות מה־suite, sauna / spa facilities, אזורי המנוחה והמלון עצמו. לא מוסיפים כאן אטרקציה קבועה.' } })"
new_relax = "place({ id: 'hotel-relax-day8', type: 'activity', name: 'זמן מלון / wellness / מנוחה', nameDirection: 'rtl', time: 'אחר הצהריים · עד היציאה לספא', duration: 'בלוק זמן משמעותי', status: 'planned', coordinates: coords.dolomitiExclusive, details: { notes: 'זמן מכוון ליהנות מה־suite, sauna / spa facilities, אזורי המנוחה והמלון עצמו. לא מוסיפים כאן אטרקציה קבועה. לקראת 16:30–16:40 מתחילים להתארגן ליציאה כדי להגיע ל־QC בנחת לפני 17:00.' } })"
if old_relax not in d8:
    raise SystemExit('Hotel relax block missing')
d8 = d8.replace(old_relax, new_relax, 1)

old_qc = "place({ id: 'qc-terme', type: 'activity', name: 'QC Terme Dolomiti', time: 'אחה״צ מאוחר / ערב · לפי ההזמנה', duration: 'בהתאם להזמנה', status: 'to-book', coordinates: coords.pozza, details: { reservation: 'שעה מדויקת תיקבע בעת ההזמנה', address: 'Strada di Bagnes 21, 38036 Pozza di Fassa, Italy', notes: 'תוכנית עיקרית. הספא קרוב מאוד למלון; לא מקבעים שעה לפני שההזמנה מאושרת.' } })"
new_qc = "place({ id: 'qc-terme', type: 'activity', name: 'QC Spa Dolomiti', time: '17:00', duration: 'Evening Spa Entrance', status: 'booked', coordinates: coords.qcSpa, details: { reservation: 'הוזמן ל־9.10.2026 · 17:00 · 2 מבוגרים', address: 'Strada di Bagnes 21, Pozza di Fassa, Sèn Jan di Fassa (TN), Italy', parking: 'אפשרות 1: הליכה מהמלון — כ־700 מ׳ / כ־8 דקות. אפשרות 2: חניה חינמית מומלצת באישור: Strada de la Veisc 75, Pozza di Fassa; משם חוצים את הגשר ל־QC.', notes: 'qc-spa-booked-1700 · להגיע ל־reception בערך 16:40–16:50 כדי להשאיר buffer להליכה / חניה / החלפה. הגישה מובטחת לשעת הכניסה שנבחרה; איחור מרבי: 30 דקות. מקבלים חלוק, מגבת, כפכפים ומוצרי courtesy — צריך להביא רק בגדי ים. Evening admission כולל Aperiterme. יש לצאת מהבריכות ואזורי ה־wellness 30 דקות לפני סגירת הספא. ביטול ללא קנס עד שעה לפני הכניסה; ביטול מאוחר / no-show עשויים לגרור חיוב מלא של השירות.' } })"
if old_qc not in d8:
    raise SystemExit('QC activity block missing')
d8 = d8.replace(old_qc, new_qc, 1)

old_return = "drive('drive-qc-hotel-day8', 'QC Terme Dolomiti → DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', 'כ־2–5 דקות', 'אחרי הספא')"
new_return = "place({ id: 'qc-spa-arrival-buffer', type: 'transfer', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → QC Spa Dolomiti', time: 'יציאה סביב 16:30–16:40', duration: 'כ־8 דקות הליכה · או נסיעה קצרה לחניה המומלצת', status: 'planned', coordinates: coords.qcSpa, details: { parking: 'Free parking: Strada de la Veisc 75, Pozza di Fassa', notes: 'המטרה היא להגיע ל־reception סביב 16:40–16:50, לא בדיוק ב־17:00. אם מזג האוויר נעים, ההליכה הישירה מהמלון היא כ־700 מ׳.' } }),\n        place({ id: 'qc-spa-return-hotel', type: 'transfer', name: 'QC Spa Dolomiti → DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', time: 'אחרי הספא', duration: 'כ־8 דקות הליכה · או חזרה לרכב', status: 'planned', coordinates: coords.dolomitiExclusive, details: { notes: 'אין שעת סיום קשיחה באתר — חוזרים ישירות למלון אחרי שסיימנו.' } })"
if old_return not in d8:
    raise SystemExit('QC return segment missing')
d8 = d8.replace(old_return, new_return, 1)

s = s[:d8_start] + d8 + s[d8_end:]

# Global trip route naming only; no itinerary changes elsewhere.
s = s.replace('→ QC Terme Dolomiti →', '→ QC Spa Dolomiti →', 1)

# Reservations/status section.
old_res = "{ id: 'qc-terme', name: 'QC Terme Dolomiti · כניסת ערב', category: 'Activity', date: '2026-10-09', status: 'to-book' },"
new_res = "{ id: 'qc-terme', name: 'QC Spa Dolomiti · Evening Spa Entrance · 17:00', category: 'Activity', date: '2026-10-09', status: 'booked' },"
if old_res not in s:
    raise SystemExit('QC reservation row missing')
s = s.replace(old_res, new_res, 1)

# Checklist.
old_check = "{ id: 'qc', label: 'להזמין QC Terme Dolomiti', done: false },"
new_check = "{ id: 'qc', label: 'QC Spa Dolomiti · הוזמן ל־9.10 בשעה 17:00', done: true },"
if old_check not in s:
    raise SystemExit('QC checklist row missing')
s = s.replace(old_check, new_check, 1)

# Guardrails: no stale QC booking wording may remain.
for stale in [
    "QC Terme Dolomiti · כניסת ערב",
    "להזמין QC Terme Dolomiti",
    "time according to reservation",
    "שעה מדויקת תיקבע בעת ההזמנה",
    "אחה״צ מאוחר / ערב · לפי ההזמנה",
]:
    if stale in s:
        raise SystemExit(f'Stale QC wording remains: {stale}')

p.write_text(s)
