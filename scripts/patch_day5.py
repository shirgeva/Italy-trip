from pathlib import Path
p = Path("index.html")
s = p.read_text()

if "id: 'day5-checkout-luggage'" in s:
    raise SystemExit(0)

start = s.index("      id: 'day-5', number: 5, date: '2026-10-06'")
end = s.index("      id: 'day-6', number: 6, date: '2026-10-07'", start)
block = s[start:end]

block = block.replace(
    "      routeLabel: 'Ortisei → Alpe di Siusi → Passo Gardena → Cortina d’Ampezzo',",
    "      routeLabel: 'Ortisei / Santa Cristina → Alpe di Siusi / Compatsch → Ortisei / Santa Cristina → Passo Gardena → Cortina d’Ampezzo / San Vito di Cadore',"
)
block = block.replace(
    "      drivingTime: 'כ־2 שעות עם עצירות',",
    "      drivingTime: 'כ־2.5–3 שעות נהיגה מצטברות · מפוצלות לאורך היום',"
)

old_marker = "      ],\n      stops: ["
if old_marker not in block:
    raise SystemExit("Day 5 areaOptions/stops marker not found")
block = block.replace(
    old_marker,
    """      ],
      alerts: [
        'חשוב: אם עולים ל־Alpe di Siusi / Compatsch ברכב פרטי, העלייה מותרת רק לפני 09:00 — לכן היציאה המוקדמת מהמלון חשובה.',
        'תוכנית מזוודות: אחרי הצ׳ק־אאוט נבקש מהמלון לשמור את המזוודות לכמה שעות, ניסע ל־Alpe di Siusi בלי המטען, נחזור לאסוף אותו ואז נמשיך מזרחה. אם המלון לא מאפשר שמירת מזוודות, משאירים הכול בתא המטען וממשיכים אחרי Alpe di Siusi ישירות לכיוון Passo Gardena / Cortina בלי עצירת האיסוף.',
      ],
      stops: [""",
    1
)

stops_start = block.index("      stops: [")
stops_end_marker = "\n      ],\n    },"
stops_end = block.index(stops_end_marker, stops_start)
new_stops = """      stops: [
        place({ id: 'day5-checkout-luggage', type: 'hotel', name: 'צ׳ק־אאוט + השארת מזוודות במלון', nameDirection: 'rtl', time: '07:30–07:45', status: 'planning', coordinates: coords.ortisei, details: { notes: 'אחרי הצ׳ק־אאוט לבקש מהמלון לשמור את המזוודות לכמה שעות. כך הביקור ב־Alpe di Siusi נעשה בלי כל המטען ברכב.' } }),
        drive('drive-ortisei-alpe', 'Ortisei / Santa Cristina → Alpe di Siusi / Compatsch', 'כ־30 דקות', '07:45–08:15', { notes: 'היעד הוא להגיע ל־Compatsch מספיק מוקדם. רכב פרטי רשאי לעלות לכיוון Alpe di Siusi רק לפני 09:00.' }),
        place({ id: 'alpe-cable-up', type: 'planning', name: 'Alpe di Siusi / Compatsch · הגעה וחניה', time: '≈08:15', coordinates: coords.alpeSiusi, details: { price: 'רכב: P2 Compatsch €30 לרכב ליום · P1 Spitzbühl €15 לרכב + כ־30 דק׳ הליכה בעלייה | חלופה ברכבל מ־Ortisei: €41 לאדם הלוך־חזור · €82 לזוג', openingHours: 'רכב פרטי רשאי לעלות ל־Compatsch רק לפני 09:00; אפשר לרדת בכל שעה. רכבל Ortisei פועל 08:30–18:00 בתאריך שלנו.', parking: 'מ־29.6.2026 חובה להזמין מראש P1/P2 אונליין, עד 6 ימים לפני ההגעה.', notes: 'התוכנית המועדפת ליום הזה היא להגיע ברכב ל־Compatsch אחרי שהמזוודות נשארו במלון. חלופת הרכבל נשארת כאפשרות אם נשנה את התכנון.' } }),
        place({ id: 'alpe-siusi', name: 'Alpe di Siusi', time: '08:15–11:00', duration: 'כ־2.5–3 שעות באזור', coordinates: coords.alpeSiusi, details: { notes: 'אזור המרעה והנוף, הליכה קלה, נקודות תצפית ועצירה אופציונלית בבקתה. Gostner Schwaige נשארת כאופציה אם היא משתלבת בקצב.' } }),
        drive('drive-alpe-back-ortisei', 'Alpe di Siusi / Compatsch → Ortisei / Santa Cristina', 'כ־30 דקות', '11:00–11:30', { notes: 'חוזרים לאזור המלון רק כדי לאסוף את המזוודות לפני שממשיכים מזרחה.' }),
        place({ id: 'day5-pickup-luggage', type: 'hotel', name: 'איסוף המזוודות מהמלון', nameDirection: 'rtl', time: '11:30–11:45', duration: 'כ־15 דקות', status: 'planning', coordinates: coords.ortisei, details: { notes: 'אוספים את המזוודות ששמר המלון ומעמיסים לרכב. מכאן ממשיכים לכיוון Passo Gardena ולא חוזרים שוב ל־Ortisei.' } }),
        drive('drive-ortisei-gardena', 'Ortisei / Santa Cristina → Passo Gardena', '≈35–45 דקות', '≈11:45–12:30', { notes: 'מכאן כיוון הנסיעה הוא מזרחה אל Cortina. אפשר לעצור בנקודות תצפית בדרך אם מזג האוויר טוב.' }),
        place({ id: 'passo-gardena', type: 'activity', name: 'Passo Gardena · עצירת נוף', time: '≈12:30', duration: '20–30 דקות', status: 'optional', coordinates: coords.passoGardena, details: { notes: 'עצירה קצרה לנוף בלבד; לא מסלול הליכה. אפשר להוסיף עוד עצירות נוף קטנות בדרך.' } }),
        drive('drive-gardena-cortina', 'Passo Gardena → Cortina d’Ampezzo / San Vito di Cadore', '≈50–60 דקות', 'אחרי העצירה', { notes: 'ממשיכים מזרחה למלון הבא. להשאיר מרווח לעצירות תצפית קצרות בדרך.' }),
        place({ id: 'cortina-arrival', type: 'hotel', name: 'Cortina d’Ampezzo / San Vito di Cadore', time: 'אחה״צ · בערך 14:00–15:00', status: 'to-book', coordinates: coords.cortina, details: { notes: 'צ׳ק־אין במלון הבא. Cortina לנוחות; San Vito di Cadore יכול להיות זול משמעותית.' } }),
      ]"""
block = block[:stops_start] + new_stops + block[stops_end + len("\n      ]"):]

s = s[:start] + block + s[end:]

replacements = {
    "{ name: 'Ortisei / Santa Cristina · בסיס לינה', label: 'יציאה ≈08:30', ...coords.ortisei }":
    "{ name: 'Ortisei / Santa Cristina · בסיס לינה', label: '07:30 צ׳ק־אאוט + מזוודות · 11:30 חזרה לאיסוף', ...coords.ortisei }",
    "{ name: 'Alpe di Siusi', label: '09:00–12:30 · רכבל + הליכה רגועה', ...coords.alpeSiusi }":
    "{ name: 'Alpe di Siusi / Compatsch', label: '08:15–11:00 · הליכה קלה + תצפיות', ...coords.alpeSiusi }",
    "{ name: 'Passo Gardena · עצירת נוף', label: 'עצירה קצרה בדרך ל־Cortina', ...coords.passoGardena }":
    "{ name: 'Passo Gardena · עצירת נוף', label: 'אחרי איסוף המזוודות · ממשיכים מזרחה', ...coords.passoGardena }",
    "{ name: 'Cortina d’Ampezzo / San Vito · בסיס לינה משוער', label: 'הגעה אחה״צ', ...coords.cortina }":
    "{ name: 'Cortina d’Ampezzo / San Vito · בסיס לינה משוער', label: 'צ׳ק־אין אחה״צ · לילה 1 מתוך 2', ...coords.cortina }",
}
for old, new in replacements.items():
    if old not in s:
        raise SystemExit(f"Map anchor not found: {old}")
    s = s.replace(old, new, 1)

p.write_text(s)
