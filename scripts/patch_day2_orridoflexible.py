from pathlib import Path

p = Path('index.html')
s = p.read_text()

if "id: 'orrido-day2-must'" in s:
    raise SystemExit(0)

# Add a dedicated MUST status badge used only by the new Day 2 plan.
css_anchor = ".status-booked { background: var(--green-soft); color: var(--green); }\n.status-to-book"
if css_anchor not in s:
    raise SystemExit('Status CSS anchor not found')
s = s.replace(
    css_anchor,
    ".status-booked { background: var(--green-soft); color: var(--green); }\n.status-must { background: var(--green-soft); color: var(--green); }\n.status-to-book",
    1,
)

label_anchor = "    booked: 'הוזמן',\n    'to-book': 'להזמין',"
if label_anchor not in s:
    raise SystemExit('Status label anchor not found')
s = s.replace(
    label_anchor,
    "    booked: 'הוזמן',\n    must: 'חובה',\n    'to-book': 'להזמין',",
    1,
)

# Replace the Day 2 map only. Villa Carlotta remains a marker, not part of the mandatory route line.
map_start = s.index("  'day-2': {")
map_end = s.index("  'day-3': {", map_start)
new_map = """  'day-2': {
    points: [
      { name: 'Varenna · בסיס / ferry hub', label: 'לינה + רכב + יציאה וחזרה למעבורות', ...coords.varenna },
      { name: 'Orrido di Bellano · חובה', label: '09:00 · בוקר קבוע', ...coords.bellano },
      { name: 'Bellagio · חובה', label: 'אחרי החזרה ל־Varenna · זמן גמיש', ...coords.bellagio },
      { name: 'Menaggio · חובה', label: 'זמן גמיש · לפי המעבורת הבאה', ...coords.menaggio },
      { name: 'Villa Carlotta / Tremezzo · אופציונלי', label: 'רק אם מתאים בזמן, בחשק ובחיבורי המעבורת', ...coords.tremezzo },
    ],
    routePath: [coords.varenna, coords.bellano, coords.varenna, coords.bellagio, coords.menaggio, coords.varenna],
  },
"""
s = s[:map_start] + new_map + s[map_end:]

# Replace Day 2 content only. Do not modify any other day.
start = s.index("      id: 'day-2', number: 2, date: '2026-10-03'")
end = s.index("      id: 'day-3', number: 3, date: '2026-10-04'", start)

new_block = """      id: 'day-2', number: 2, date: '2026-10-03',
      startBase: 'Varenna',
      title: 'Orrido di Bellano + Bellagio + Menaggio',
      overviewPoint: 'Orrido di Bellano + Bellagio + Menaggio',
      area: 'Lake Como',
      routeLabel: 'Varenna → Bellano → Varenna → Lake Como ferries → Bellagio → Menaggio → Varenna',
      overnight: 'Varenna · לילה 2 מתוך 2',
      drivingTime: 'בוקר: 5–10 דק׳ לכל כיוון אם נוסעים ברכב · אחר כך מעבורות',
      walking: 'Orrido כ־45–60 דק׳ + שיטוט גמיש ב־Bellagio וב־Menaggio',
      highlights: ['Orrido di Bellano · חובה', 'Bellagio · חובה', 'Menaggio · חובה', 'Villa Carlotta / Tremezzo · אופציונלי'],
      areaOptions: [
        {
          id: 'orrido-car-option-day2',
          name: 'Option A — Car',
          category: 'Orrido di Bellano · אפשרות מועדפת',
          description: 'הדרך המועדפת לבוקר: נסיעה קצרה מ־Varenna, ביקור עם הפתיחה וחזרה למלון כדי להשאיר את הרכב שם לפני יום המעבורות.',
          details: {
            address: 'Piazza S. Giorgio, 23822 Bellano LC, Italy',
            parking: 'לנסות קודם חניה באזור מרכז Bellano / Piazza San Giorgio. אם מלא, להשתמש באזור החניה ליד Bellano-Tartavalle Terme וללכת כ־10 דקות.',
            price: 'חניה: לבדוק תעריף ושילוט בהגעה — לא מציגים מחיר לא מאומת.',
            notes: 'יציאה מ־Varenna בערך 08:40–08:45 · נסיעה כ־5–10 דק׳ · יעד חניה סביב 08:50 · אחרי הביקור חוזרים למקום הלינה ב־Varenna ומשאירים שם את הרכב להמשך היום. יעד חזרה משוער: 10:10–10:30.',
            website: 'https://www.comune.bellano.lc.it/amministrazione/documenti_e_dati/documenti_tecnici_di_supporto/documento_89.html',
          },
        },
        {
          id: 'orrido-train-option-day2',
          name: 'Option B — Train',
          category: 'Orrido di Bellano · חלופה',
          description: 'משאירים את הרכב במקום הלינה ונוסעים ישירות ברכבת Varenna-Esino → Bellano-Tartavalle Terme.',
          details: {
            price: 'כ־€2 לאדם לכל כיוון · מחיר משוער בלבד, לבדוק בעת הקנייה',
            notes: 'הנסיעה עצמה כ־4–7 דקות, ואז כ־10 דקות הליכה ל־Orrido. לבחור רכבת בוקר שמביאה ל־Bellano בזמן להגיע לכניסה לפני 09:00. לא מקבעים רכבת ספציפית עד שלוח 3.10.2026 מאושר. עם כרטיס תחבורה ציבורית תקף מחיר הכניסה ל־Orrido יורד מ־€8 ל־€5 לאדם.',
          },
        },
        {
          id: 'villa-carlotta-day2',
          name: 'Villa Carlotta',
          category: 'Tremezzo · אופציונלי בלבד',
          description: 'וילה היסטורית ב־Tremezzo עם גנים בוטניים גדולים ונוף ל־Lake Como. יפה, אבל לא על חשבון Bellagio או Menaggio.',
          details: {
            openingHours: '3.10.2026 · 10:00–19:00 · כרטיס אחרון 18:00',
            price: '€17.50 למבוגר',
            notes: 'מחליטים באותו יום לפי זמן, חיבורי מעבורת, מצב רוח והאם באמת מתחשק לנו ביקור בגנים. אפשר לשלב במקום שנוח לפי לוח המעבורות — אין סדר חובה.',
            website: 'https://www.villacarlotta.it/en/visit/',
          },
        },
      ],
      alerts: [
        'בוקר קבוע: 09:00 Orrido di Bellano. זו אטרקציית חובה עבורנו כי טבע ומפלים מעניינים אותנו יותר מווילות וגנים.',
        'אחרי Orrido היום הופך לגמיש: Bellagio חובה · Menaggio חובה · Villa Carlotta / Tremezzo אופציונלי בלבד.',
        'Varenna היא בסיס / מקום הלינה / חניית הרכב / נקודת יציאה וחזרה למעבורות — לא עצירת sightseeing מתוכננת ביום הזה. נטייל בה בערב יום 1 ובאופן טבעי שוב בערב יום 2.',
        'אסטרטגיית מעבורות: קונים כרטיסים באותו יום, בודקים את המעבורת הבאה ולא עובדים לפי לו״ז קשיח. כשאפשר מגיעים 20–30 דקות לפני. לבדוק בקופה את המחיר המדויק לכל מסלול וגם האם כרטיס day / free-circulation משתלם יותר מהזמנות בודדות.',
      ],
      stops: [
        place({ id: 'orrido-day2-must', type: 'attraction', name: 'Orrido di Bellano', time: '09:00 · הגעה / כניסה', duration: 'כ־45–60 דקות', status: 'must', coordinates: coords.bellano, details: { openingHours: 'שבת 3.10.2026 · 09:00–19:00 · כניסה אחרונה 20 דקות לפני הסגירה', price: '€8 למבוגר · €5 עם כרטיס תחבורה ציבורית תקף, כולל רכבת או Lake Como navigation', address: 'Piazza S. Giorgio, 23822 Bellano LC, Italy', reservation: 'אין צורך בהזמנה מראש למבקרים יחידים', notes: 'ערוץ טבע דרמטי שנחצב על ידי נהר Pioverna, עם מפלים, קירות סלע צרים, מדרגות ושבילי הליכה מוגבהים.' } }),
        place({ id: 'return-varenna-after-orrido', type: 'planning', name: 'חזרה ל־Varenna + השארת הרכב', nameDirection: 'rtl', time: '≈10:10–10:30', duration: 'לפי אמצעי ההגעה', status: 'planned', coordinates: coords.varenna, details: { notes: 'ברכב: חוזרים למקום הלינה ומשאירים את הרכב שם להמשך היום. ברכבת: חוזרים מ־Bellano-Tartavalle Terme ל־Varenna-Esino. מכאן מתחיל חלק המעבורות הגמיש.' } }),
        place({ id: 'varenna-ferry-hub-day2', type: 'ferry', name: 'Varenna · base / ferry hub', time: 'מכאן והלאה', status: 'planned', coordinates: coords.varenna, details: { notes: 'לא מקדישים ל־Varenna בלוק sightseeing ביום הזה. היא משמשת כבסיס לינה, חניית רכב ונקודת יציאה / חזרה למעבורות. זמן פנוי בין פעילויות אפשר כמובן להעביר כאן.' } }),
        place({ id: 'bellagio-day2-must', name: 'Bellagio', time: 'גמיש · ללא שעה קבועה', duration: 'נשארים כל עוד נהנים', status: 'must', coordinates: coords.bellagio, details: { price: 'מרכז העיירה חינם', notes: 'העיירה הקלאסית והאיקונית ביותר ב־Lake Como: רחובות היסטוריים מדורגים, נוף לאגם, חנויות, בתי קפה, מסעדות וטיילת יפה. מגיעים במעבורת מ־Varenna.' } }),
        place({ id: 'menaggio-day2-must', name: 'Menaggio', time: 'גמיש · ללא שעה קבועה', duration: 'לפי החשק באותו יום', status: 'must', coordinates: coords.menaggio, details: { price: 'מרכז העיירה חינם', notes: 'עיירת אגם רגועה עם כיכר מרכזית, טיילת, בתי קפה ונוף פתוח על Lake Como. מגיעים במעבורת; לא מקבעים מראש כמה זמן נשארים.' } }),
        place({ id: 'villa-carlotta-flex-day2', type: 'attraction', name: 'Villa Carlotta / Tremezzo', time: 'אופציונלי · איפה שנוח לפי המעבורות', duration: 'רק אם מתחשק ויש זמן', status: 'optional', coordinates: coords.tremezzo, details: { openingHours: '3.10.2026 · 10:00–19:00 · כרטיס אחרון 18:00', price: '€17.50 למבוגר', notes: 'לא חייבים להגיע בסדר מסוים. מוסיפים רק אם חיבור המעבורת נוח ואם זה לא מקצר את Bellagio או Menaggio.' } }),
        place({ id: 'return-varenna-day2', type: 'ferry', name: 'חזרה ל־Varenna', nameDirection: 'rtl', time: 'לפי המעבורת והקצב', status: 'planned', coordinates: coords.varenna, details: { notes: 'אין שעת חזרה קשיחה. בוחרים את המעבורת המתאימה אחרי שמיצינו את Bellagio ו־Menaggio.' } }),
      ],
    },
    {
"""

s = s[:start] + new_block + s[end:]

# Update the Day 2 anchor shown on the trip-level map/overview, without touching other days.
old_anchor = "    { id: 'day-2-map', dayNumber: 2, href: '#/day/day-2', name: 'Bellagio', label: 'יום 2 · 3.10', ...coords.bellagio },"
new_anchor = "    { id: 'day-2-map', dayNumber: 2, href: '#/day/day-2', name: 'Orrido di Bellano + Bellagio + Menaggio', label: 'יום 2 · 3.10', ...coords.bellano },"
if old_anchor not in s:
    raise SystemExit('Day 2 route anchor not found')
s = s.replace(old_anchor, new_anchor, 1)

p.write_text(s)
