from pathlib import Path
import re

path = Path('index.html')
s = path.read_text(encoding='utf-8')

# Overview anchors: remove "extra day" wording and put the spa on 9.10.
s = s.replace(
    "    { id: 'day-7-map', dayNumber: 7, href: '#/day/day-7', name: 'Val di Fassa / QC Terme Dolomiti', label: 'יום 7 · 8.10', ...coords.pozza },",
    "    { id: 'day-7-map', dayNumber: 7, href: '#/day/day-7', name: 'Val di Fassa / Pozza di Fassa', label: 'יום 7 · 8.10', ...coords.pozza },",
    1,
)
s = s.replace(
    "    { id: 'day-8-map', dayNumber: 8, href: '#/day/day-8', name: 'Val di Fassa · יום נוסף', label: 'יום 8 · 9.10', ...coords.pozza },",
    "    { id: 'day-8-map', dayNumber: 8, href: '#/day/day-8', name: 'Val di Fassa / QC Terme Dolomiti', label: 'יום 8 · 9.10', ...coords.pozza },",
    1,
)

# Day-map summaries.
map_pattern = re.compile(r"  'day-7': \{.*?\n  \},\n  'day-8': \{.*?\n  \},\n  'day-9': \{", re.S)
map_replacement = """  'day-7': {
    points: [
      { name: 'Cortina / San Vito di Cadore', label: 'יציאה לכיוון Val di Fassa', ...coords.cortina },
      { name: 'Pozza di Fassa / Val di Fassa', label: 'בסיס לינה · לילה 1 מתוך 2', ...coords.pozza },
    ],
    routePath: [coords.cortina, coords.pozza],
  },
  'day-8': {
    points: [
      { name: 'Val di Fassa / Pozza di Fassa', label: 'יום טיול באזור · QC Terme Dolomiti בערב · לילה 2 מתוך 2', ...coords.pozza },
    ],
    routePath: [coords.pozza],
  },
  'day-9': {"""
s, n = map_pattern.subn(map_replacement, s, count=1)
if n != 1:
    raise SystemExit(f'Expected one day-map replacement, got {n}')

# Correct the booking date for the spa.
old_booking = "    { id: 'qc-terme', name: 'QC Terme Dolomiti · כניסת ערב', category: 'Activity', date: '2026-10-08', status: 'to-book' },"
new_booking = "    { id: 'qc-terme', name: 'QC Terme Dolomiti · כניסת ערב', category: 'Activity', date: '2026-10-09', status: 'to-book' },"
if old_booking not in s:
    raise SystemExit('Expected QC booking date line not found')
s = s.replace(old_booking, new_booking, 1)

# Replace the two Val di Fassa days. Attractions remain options, not fixed stops.
days_pattern = re.compile(r"    \{\n      id: 'day-7'.*?\n    \},\n    \{\n      id: 'day-8'.*?\n    \},\n    \{\n      id: 'day-9'", re.S)
days_replacement = """    {
      id: 'day-7', number: 7, date: '2026-10-08',
      startBase: 'Cortina / San Vito di Cadore',
      title: 'Cortina → Val di Fassa',
      overviewPoint: 'Val di Fassa / Pozza di Fassa',
      area: 'Val di Fassa / Pozza di Fassa',
      routeLabel: 'Cortina / San Vito di Cadore → Val di Fassa / Pozza di Fassa',
      overnight: 'Pozza di Fassa / Val di Fassa · לילה 1 מתוך 2',
      drivingTime: 'ייקבע לפי המסלול והעצירות שנבחר',
      walking: 'יום טיול גמיש · בתכנון',
      highlights: ['Val di Fassa'],
      areaOptions: [
        {
          id: 'passo-pordoi-option',
          name: 'Passo Pordoi',
          category: 'מעבר הרים / תצפית',
          description: 'מעבר הרים דרמטי שמתאים לעצירת נוף בדרך או כחלק מהיום באזור. עדיין לא שובץ סופית בלו״ז.',
          details: { notes: 'אפשרות ל־8.10 בהתאם למזג האוויר ולמסלול שנבחר.' },
        },
        {
          id: 'sass-pordoi-option',
          name: 'Sass Pordoi',
          category: 'רכבל / תצפית',
          description: 'עלייה ברכבל לתצפית גבוהה מאוד על הדולומיטים, בלי צורך בטרק ארוך. עדיין לא שובץ סופית בלו״ז.',
          details: { notes: 'אפשר לשלב עם Passo Pordoi אם התנאים מתאימים.' },
        },
      ],
      alerts: ['האטרקציות ביום הזה עדיין פתוחות לבחירה; מה שסגור כרגע הוא המעבר ל־Val di Fassa והלינה באזור.'],
      stops: [
        drive('drive-cortina-val-di-fassa', 'Cortina / San Vito di Cadore → Val di Fassa / Pozza di Fassa', 'ייקבע לפי המסלול', 'במהלך היום', { notes: 'המסלול המדויק והעצירות בדרך ייקבעו בהמשך.' }),
        place({ id: 'pozza-overnight-1', type: 'hotel', name: 'Pozza di Fassa / Val di Fassa · לילה 1 מתוך 2', time: 'ערב', status: 'to-book', coordinates: coords.pozza, details: { notes: 'זה הלילה הראשון מתוך שניים באזור הספא.' } }),
      ],
    },
    {
      id: 'day-8', number: 8, date: '2026-10-09',
      startBase: 'Pozza di Fassa / Val di Fassa',
      title: 'Val di Fassa + QC Terme Dolomiti',
      overviewPoint: 'Val di Fassa / QC Terme Dolomiti',
      area: 'Val di Fassa / Pozza di Fassa',
      routeLabel: 'Val di Fassa / Pozza di Fassa → יום טיול באזור → QC Terme Dolomiti',
      overnight: 'Pozza di Fassa / Val di Fassa · לילה 2 מתוך 2',
      drivingTime: 'ייקבע לפי המסלול שנבחר באזור',
      walking: 'יום טיול גמיש + ספא בערב',
      highlights: ['Val di Fassa', 'QC Terme Dolomiti'],
      areaOptions: [
        {
          id: 'carezza-option',
          name: 'Lago di Carezza',
          category: 'אגם / טבע',
          description: 'אגם הררי קטן עם נוף לרכסים שמסביב. אפשרות ליום האחרון בדולומיטים לפני הספא.',
          details: { notes: 'עדיין לא שובץ סופית; נחליט בהמשך לפי מזג האוויר והקצב.' },
        },
        {
          id: 'rosengarten-option',
          name: 'Rosengarten / Catinaccio',
          category: 'רכס הרים / תצפיות',
          description: 'אזור נופי סביב רכס Rosengarten, שמתאים לשילוב עם Carezza או למסלול קצר באזור.',
          details: { notes: 'אפשרות בלבד; לא חלק סגור מהלו״ז כרגע.' },
        },
      ],
      alerts: ['זה הערב האחרון בדולומיטים: QC Terme Dolomiti נשאר לסוף היום, ואחריו ישנים שוב ליד הספא.'],
      stops: [
        place({ id: 'val-di-fassa-day', type: 'activity', name: 'יום טיול באזור Val di Fassa · בתכנון', nameDirection: 'rtl', time: 'בוקר / צהריים', status: 'planning', coordinates: coords.pozza, details: { notes: 'נבחר בהמשך את האטרקציות המדויקות מתוך האפשרויות באזור.' } }),
        place({ id: 'qc-terme', type: 'activity', name: 'QC Terme Dolomiti', time: 'ערב', duration: 'בהתאם להזמנה', status: 'to-book', coordinates: coords.pozza, details: { reservation: 'כניסת ערב · שעה מדויקת תיקבע בעת ההזמנה', notes: 'הספא סוגר את פרק הדולומיטים בערב של 9.10.' } }),
        place({ id: 'pozza-overnight-2', type: 'hotel', name: 'Pozza di Fassa / Val di Fassa · לילה 2 מתוך 2', time: 'אחרי הספא', status: 'to-book', coordinates: coords.pozza, details: { notes: 'לינה ליד הספא; בבוקר 10.10 יוצאים לצפון Lake Garda.' } }),
      ],
    },
    {
      id: 'day-9'"""
s, n = days_pattern.subn(days_replacement, s, count=1)
if n != 1:
    raise SystemExit(f'Expected one day-data replacement, got {n}')

# Ensure the unwanted label is gone from these days.
if 'Val di Fassa · יום נוסף' in s or "title: 'Val di Fassa · יום נוסף בדולומיטים'" in s:
    raise SystemExit('Unwanted extra-day wording still present')

path.write_text(s, encoding='utf-8')
