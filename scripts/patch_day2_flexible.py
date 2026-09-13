from pathlib import Path

p = Path('index.html')
s = p.read_text()

if "id: 'villa-carlotta-day2'" in s:
    raise SystemExit(0)

# Add a map coordinate for the Tremezzo / Villa Carlotta stop.
coords_anchor = "  menaggio: { lat: 46.0202, lng: 9.2387 },"
coords_replacement = "  menaggio: { lat: 46.0202, lng: 9.2387 },\n  tremezzo: { lat: 45.9869, lng: 9.2301 },"
if coords_anchor not in s:
    raise SystemExit('Day 2 coordinate anchor not found')
s = s.replace(coords_anchor, coords_replacement, 1)

# Replace only the Day 2 block. Everything else stays untouched.
start = s.index("      id: 'day-2', number: 2, date: '2026-10-03'")
end = s.index("      id: 'day-3', number: 3, date: '2026-10-04'", start)

new_block = """      id: 'day-2', number: 2, date: '2026-10-03',
      startBase: 'Varenna',
      title: 'Varenna + Bellagio · יום גמיש',
      overviewPoint: 'Varenna + Bellagio',
      area: 'Lake Como',
      routeLabel: 'Varenna → Bellagio → Villa Carlotta / Tremezzo → Menaggio → Varenna · מסלול גמיש',
      overnight: 'Varenna · לילה 2 מתוך 2',
      drivingTime: 'ללא נהיגה מתוכננת · מעבורות בלבד',
      walking: 'גמיש לפי הקצב והחשק',
      highlights: ['Varenna + Bellagio · עדיפות / חובה', 'Villa Carlotta · אופציונלי מומלץ', 'Menaggio · אופציונלי · עדיפות אחרונה'],
      areaOptions: [
        {
          id: 'villa-monastero',
          name: 'Villa Monastero',
          category: 'Varenna · אופציונלי בתשלום',
          description: 'וילה היסטורית וגנים בוטניים ארוכים על שפת Lake Como. אפשר לשלב אם רוצים אטרקציה בתשלום כבר ב־Varenna.',
          details: {
            openingHours: '3.10.2026 · 10:00–18:00',
            price: 'כניסה בתשלום',
            address: 'Viale Giovanni Polvani 4, 23829 Varenna LC, Italy',
            notes: 'מרכז Varenna, הטיילת והרחובות עצמם חינם. אין צורך במעבורת — אנחנו ישנים ב־Varenna.',
            website: 'https://www.villamonastero.eu/en/opening-hours-ticket/',
          },
        },
        {
          id: 'villa-melzi-day2',
          name: 'Villa Melzi Gardens',
          category: 'Bellagio · אופציונלי בתשלום',
          description: 'גנים מטופחים על שפת האגם ב־Bellagio. אופציה טובה אם מתחשק לשלב גנים בזמן השיטוט בעיר.',
          details: {
            price: 'כניסה בתשלום',
            notes: 'מרכז Bellagio, הרחובות, החנויות והטיילת חינם.',
          },
        },
        {
          id: 'villa-carlotta-day2',
          name: 'Villa Carlotta',
          category: 'Tremezzo · אופציונלי מומלץ',
          description: 'וילה היסטורית עם גנים בוטניים גדולים ותצפיות על Lake Como. זו אופציית האטרקציה המרכזית אם רוצים משהו מעבר לשיטוט בעיירות.',
          details: {
            openingHours: '3.10.2026 · 10:00–19:00',
            price: 'כניסה בתשלום',
            address: 'Via Statale 5605, 22016 Tremezzina CO, Italy',
            notes: 'מגיעים במעבורת לאזור Tremezzo / Villa Carlotta. אופציונלי אבל מומלץ יותר מ־Menaggio אם צריך לבחור.',
            website: 'https://www.villacarlotta.it/en/visit/',
          },
        },
      ],
      alerts: [
        'יום גמיש: Varenna + Bellagio הן העדיפות / חובה. Villa Carlotta אופציונלית אבל מומלצת אם רוצים אטרקציה; Menaggio בעדיפות האחרונה וקל לוותר עליה.',
        'מעבורות מרכז Lake Como מחברות בין Varenna, Bellagio, Menaggio ואזור Tremezzo / Villa Carlotta. נקנה כרטיסים באותו יום, נגיע בערך 20–30 דקות לפני המעבורת ונחליט לפי הקצב. אם נשארים יותר במקום שאוהבים — פשוט מדלגים על אחת העצירות האופציונליות.',
      ],
      stops: [
        place({ id: 'varenna', name: 'Varenna · עדיפות / חובה', time: 'מתחילים כאן · ללא שעה קבועה', duration: 'גמיש', coordinates: coords.varenna, details: { price: 'מרכז העיירה חינם', notes: 'טיילת על האגם, סמטאות צרות, בתי קפה ונוף. אנחנו ישנים כאן ולכן אין צורך במעבורת כדי להתחיל את היום. Villa Monastero והגנים הם אופציה בתשלום.' } }),
        place({ id: 'ferry-varenna-bellagio', type: 'ferry', name: 'Varenna → Bellagio', time: 'כשמתאים במהלך היום', duration: 'לפי לוח המעבורות', coordinates: coords.bellagio, details: { notes: 'Bellagio היא יעד המעבורת המרכזי והעצירה השנייה בעדיפות. קונים כרטיסים באותו יום ונשארים גמישים.' } }),
        place({ id: 'bellagio', name: 'Bellagio · עדיפות / חובה', time: 'ללא שעה קבועה', duration: 'גמיש', coordinates: coords.bellagio, details: { price: 'מרכז העיירה חינם', notes: 'המרכז ההיסטורי, הרחובות המדורגים, חנויות, מסעדות וטיילת על האגם. Villa Melzi Gardens היא אופציה בתשלום.' } }),
        transfer('ferry-bellagio-tremezzo', 'Bellagio → Tremezzo / Villa Carlotta', 'מעבורת · אופציונלי', 'אם רוצים אטרקציה', { notes: 'המשך אופציונלי. אם רוצים אטרקציה בתשלום מעבר לשיטוט בעיירות, זו הבחירה המומלצת.' }),
        place({ id: 'villa-carlotta-stop-day2', type: 'attraction', name: 'Villa Carlotta / Tremezzo · אופציונלי מומלץ', time: 'ללא שעה קבועה', duration: 'לפי הקצב', status: 'optional', coordinates: coords.tremezzo, details: { price: 'כניסה בתשלום', notes: 'וילה היסטורית וגנים בוטניים גדולים מול האגם. אם היום מתקדם לאט אפשר לבחור בה ולוותר על Menaggio.' } }),
        transfer('ferry-tremezzo-menaggio', 'Tremezzo / Villa Carlotta → Menaggio', 'מעבורת · אופציונלי', 'רק אם נשאר זמן', { notes: 'Menaggio היא העצירה בעדיפות האחרונה. אפשר לדלג עליה בלי לפגוע ביום.' }),
        place({ id: 'menaggio', name: 'Menaggio · אופציונלי · עדיפות אחרונה', time: 'רק אם נשאר זמן וחשק', duration: 'כ־שעה', status: 'optional', coordinates: coords.menaggio, details: { price: 'מרכז העיירה חינם', notes: 'עיירה נעימה עם כיכר מרכזית וטיילת על האגם. מתאימה לעצירה קצרה בלבד.' } }),
        place({ id: 'return-varenna', type: 'ferry', name: 'חזרה ל־Varenna', nameDirection: 'rtl', time: 'לפי הקצב ולוח המעבורות', status: 'planned', coordinates: coords.varenna, details: { notes: 'אין שעה קשיחה. חוזרים ל־Varenna כשהרגשנו שמיצינו את היום.' } }),
      ],
    },
    {
"""

s = s[:start] + new_block + s[end:]

old_map = """  'day-2': {
    points: [
      { name: 'Bellano · בסיס לינה משוער', label: 'יציאה בבוקר', ...coords.bellano },
      { name: 'Varenna', label: '09:00–11:30 · 0–15 דק׳ לפי הלינה', ...coords.varenna },
      { name: 'Bellagio', label: '12:00–15:30 · מעבורת מ־Varenna', ...coords.bellagio },
      { name: 'Menaggio · אופציונלי', label: '15:30–17:00 · רק אם יש כוח', ...coords.menaggio },
    ],
    routePath: [coords.bellano, coords.varenna, coords.bellagio, coords.menaggio, coords.varenna, coords.bellano],
  },"""
new_map = """  'day-2': {
    points: [
      { name: 'Varenna · עדיפות / חובה', label: 'מתחילים כאן · בסיס לינה', ...coords.varenna },
      { name: 'Bellagio · עדיפות / חובה', label: 'יעד המעבורת המרכזי', ...coords.bellagio },
      { name: 'Villa Carlotta / Tremezzo · אופציונלי מומלץ', label: 'האטרקציה המרכזית אם רוצים מעבר לשיטוט', ...coords.tremezzo },
      { name: 'Menaggio · אופציונלי', label: 'עדיפות אחרונה · כ־שעה אם נשאר זמן', ...coords.menaggio },
    ],
    routePath: [coords.varenna, coords.bellagio, coords.tremezzo, coords.menaggio, coords.varenna],
  },"""
if old_map not in s:
    raise SystemExit('Day 2 map anchor not found')
s = s.replace(old_map, new_map, 1)

p.write_text(s)
