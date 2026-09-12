from pathlib import Path

p = Path('index.html')
s = p.read_text()

if "id: 'friedrich-august-day7'" in s:
    raise SystemExit(0)

# Add map coordinates for Passo Sella and Rifugio Friedrich August.
coords_anchor = "  passoGardena: { lat: 46.5499, lng: 11.8087 },\n  cortina: { lat: 46.5405, lng: 12.1357 },"
coords_replacement = "  passoGardena: { lat: 46.5499, lng: 11.8087 },\n  passoSella: { lat: 46.50822, lng: 11.75825 },\n  friedrichAugust: { lat: 46.500711, lng: 11.745286 },\n  cortina: { lat: 46.5405, lng: 12.1357 },"
if coords_anchor not in s:
    raise SystemExit('Coordinates anchor not found')
s = s.replace(coords_anchor, coords_replacement, 1)

# Work only inside Day 7 so all existing area options remain untouched.
start = s.index("      id: 'day-7', number: 7, date: '2026-10-08'")
end = s.index("      id: 'day-8', number: 8, date: '2026-10-09'", start)
block = s[start:end]

block = block.replace(
    "      routeLabel: 'Cortina / San Vito di Cadore → Val di Fassa / Pozza di Fassa',",
    "      routeLabel: 'Cortina / San Vito → Passo Sella → Rifugio Friedrich August → Pozza di Fassa / Val di Fassa',"
)
block = block.replace(
    "      drivingTime: 'ייקבע לפי המסלול והעצירות שנבחר',",
    "      drivingTime: 'כ־2 שעות נהיגה מצטברות + עצירת בוקר ב־Passo Sella',"
)
block = block.replace(
    "      walking: 'יום טיול גמיש · בתכנון',",
    "      walking: 'כ־40–60 דקות הליכה מצטברות לבקתה וחזרה',"
)
block = block.replace(
    "      highlights: ['Val di Fassa'],",
    "      highlights: ['Rifugio Friedrich August', 'Val di Fassa'],"
)

old_alert = "      alerts: ['האטרקציות ביום הזה עדיין פתוחות לבחירה; מה שסגור כרגע הוא המעבר ל־Val di Fassa והלינה באזור.'],"
new_alert = """      alerts: [
        'TO VERIFY: צריך לאשר ש־Rifugio Friedrich August פתוח ב־8.10.2026. ברשומת Val Gardena הרשמית כרגע עונת הקיץ של 2026 מופיעה עד 27.9 בלבד, לכן העצירה עדיין לא מאושרת.',
        'אם Friedrich August סגור בתאריך שלנו, פשוט מורידים את העצירה וממשיכים ישירות מ־Passo Sella לכיוון Pozza di Fassa / Val di Fassa.',
        'האטרקציות הנוספות ביום הזה עדיין פתוחות לבחירה; המעבר ל־Val di Fassa והלינה באזור נשארים כמתוכנן.',
      ],"""
if old_alert not in block:
    raise SystemExit('Day 7 alert anchor not found')
block = block.replace(old_alert, new_alert, 1)

stops_start = block.index("      stops: [")
stops_end_marker = "\n      ],\n    },"
stops_end = block.index(stops_end_marker, stops_start)
new_stops = """      stops: [
        drive('drive-cortina-passo-sella', 'Cortina / San Vito di Cadore → Passo Sella', 'כ־1.5 שעות · משוער', '08:00–≈09:30', { notes: 'יציאה בבוקר לכיוון Passo Sella. זמן הנסיעה משוער ותלוי בכבישים ובמזג האוויר.' }),
        place({ id: 'passo-sella-parking-day7', type: 'activity', name: 'Passo Sella · חניה', time: '≈09:30', duration: 'עצירה לוגיסטית', status: 'planning', coordinates: coords.passoSella, details: { notes: 'לא נוסעים עם הרכב עד Rifugio Friedrich August. מחנים באזור Passo Sella וממשיכים לבקתה ברגל.' } }),
        place({ id: 'walk-passo-sella-friedrich', type: 'activity', name: 'Passo Sella → Rifugio Friedrich August · הליכה', time: '09:30–09:50', duration: 'כ־20–30 דקות', status: 'planning', coordinates: coords.friedrichAugust, details: { notes: 'הליכה קלה יחסית מהחניה לכיוון הבקתה. כדאי להשאיר מעט מרווח — מקורות מקומיים מציינים לעיתים כ־30 דקות הליכה מ־Passo Sella.' } }),
        place({ id: 'friedrich-august-day7', type: 'food', name: 'Rifugio Friedrich August', time: '09:50–11:00', duration: 'כ־1:10 שעות', status: 'planning', coordinates: coords.friedrichAugust, details: { openingHours: 'TO VERIFY ל־8.10.2026', notes: 'עצירת בוקר לנוף הררי, קפה / ארוחת בוקר, ואם זמין — ה־Krapfen המפורסם. כרגע אין אישור שהבקתה פתוחה ב־8.10; אם היא סגורה פשוט מדלגים וממשיכים ל־Val di Fassa.' } }),
        place({ id: 'walk-friedrich-passo-sella', type: 'activity', name: 'Rifugio Friedrich August → Passo Sella · חזרה לרכב', time: '11:00–11:20', duration: 'כ־20–30 דקות', status: 'planning', coordinates: coords.passoSella, details: { notes: 'חוזרים ברגל לאזור החניה ב־Passo Sella.' } }),
        drive('drive-passo-sella-pozza', 'Passo Sella → Pozza di Fassa / Val di Fassa', 'כ־30–40 דקות · משוער', '≈11:20–11:50/12:00', { notes: 'מכאן ממשיכים לעמק ולבסיס הלינה הבא.' }),
        place({ id: 'pozza-arrival-day7', type: 'activity', name: 'Pozza di Fassa / Val di Fassa · הגעה לאזור', time: '≈11:50–12:00', status: 'planning', coordinates: coords.pozza, details: { notes: 'מגיעים לאזור לקראת הצהריים. שאר האופציות שכבר שמרנו ליום הזה נשארות פתוחות לבחירה בהתאם למזג האוויר, אנרגיה ושעות הפעילות.' } }),
        place({ id: 'pozza-overnight-1', type: 'hotel', name: 'Pozza di Fassa / Val di Fassa · לילה 1 מתוך 2', time: 'ערב', status: 'to-book', coordinates: coords.pozza, details: { notes: 'זה הלילה הראשון מתוך שניים באזור הספא.' } }),
      ]"""
block = block[:stops_start] + new_stops + block[stops_end + len("\n      ]"):]

s = s[:start] + block + s[end:]

old_map = """  'day-7': {
    points: [
      { name: 'Cortina / San Vito di Cadore', label: 'יציאה לכיוון Val di Fassa', ...coords.cortina },
      { name: 'Pozza di Fassa / Val di Fassa', label: 'בסיס לינה · לילה 1 מתוך 2', ...coords.pozza },
    ],
    routePath: [coords.cortina, coords.pozza],
  },"""
new_map = """  'day-7': {
    points: [
      { name: 'Cortina / San Vito di Cadore', label: '08:00 · יציאה מערבה', ...coords.cortina },
      { name: 'Passo Sella · חניה', label: '≈09:30 · מכאן ממשיכים ברגל', ...coords.passoSella },
      { name: 'Rifugio Friedrich August', label: '09:50–11:00 · TO VERIFY', ...coords.friedrichAugust },
      { name: 'Pozza di Fassa / Val di Fassa', label: '≈11:50–12:00 · בסיס לינה', ...coords.pozza },
    ],
    routePath: [coords.cortina, coords.passoSella, coords.friedrichAugust, coords.passoSella, coords.pozza],
  },"""
if old_map not in s:
    raise SystemExit('Day 7 map anchor not found')
s = s.replace(old_map, new_map, 1)

p.write_text(s)
