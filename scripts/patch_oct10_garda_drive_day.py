from pathlib import Path

p = Path('index.html')
s = p.read_text()

if "id: 'ciclopista-reamol'" in s:
    raise SystemExit(0)

# Add a precise map point for the official cycle-path parking / Capo Reamol access area.
coord_anchor = "  ponale: { lat: 45.8842, lng: 10.8320 },"
if coord_anchor not in s:
    raise SystemExit('Ponale coordinate anchor missing')
s = s.replace(coord_anchor, coord_anchor + "\n  capoReamol: { lat: 45.825557, lng: 10.814022 },", 1)

# Update ONLY the October 10 map.
map_start = s.index("  'day-9': {")
map_end = s.index("  'day-10': {", map_start)
new_map = """  'day-9': {
    points: [
      { name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', label: '08:00 · יציאה מ־Pozza di Fassa', ...coords.dolomitiExclusive },
      { name: 'Parco Grotta Cascata Varone', label: '10:00–11:00 · מפל', ...coords.varone },
      { name: 'Riva del Garda', label: '11:10–13:00 · טיילת + מרכז + צהריים', ...coords.riva },
      { name: 'Ciclopista del Garda – Capo Reamol', label: '13:15–14:00 · קטע תלוי קצר הלוך־חזור', ...coords.capoReamol },
      { name: 'Limone sul Garda', label: '14:10–16:00 · שיטוט רגוע', ...coords.limone },
      { name: 'Abacus Hotel · Sesto San Giovanni', label: '≈18:15–18:45 · לילה 1 מתוך 2', ...coords.abacusHotel },
    ],
    routePath: [coords.dolomitiExclusive, coords.varone, coords.riva, coords.capoReamol, coords.limone, coords.abacusHotel],
  },
"""
s = s[:map_start] + new_map + s[map_end:]

# Replace ONLY Day 9 / October 10 itinerary data. Keep all later days byte-for-byte intact.
day_start = s.index("      id: 'day-9', number: 9, date: '2026-10-10'")
day_end = s.index("      id: 'day-10', number: 10, date: '2026-10-11'", day_start)
new_day = """      id: 'day-9', number: 9, date: '2026-10-10',
      startBase: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE, Pozza di Fassa',
      title: 'Varone → Riva → Ciclopista del Garda → Limone → Sesto',
      overviewPoint: 'North Lake Garda · Varone / Riva / Capo Reamol / Limone',
      area: 'North Lake Garda / Sesto San Giovanni',
      routeLabel: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → Cascata del Varone → Riva del Garda → Ciclopista del Garda – Capo Reamol → Limone sul Garda → Abacus Hotel, Sesto San Giovanni',
      overnight: 'Abacus Hotel · לילה 1 מתוך 2',
      drivingTime: 'כ־4:30–5:00 שעות נהיגה מצטברת · כולל הכביש הארוך מהדולומיטים והמשך ל־Sesto',
      walking: 'Varone + Riva + כ־1–1.6 ק״מ בקטע התלוי + Limone',
      highlights: ['Parco Grotta Cascata Varone', 'Riva del Garda', 'Ciclopista del Garda – Capo Reamol', 'Limone sul Garda'],
      areaOptions: [
        {
          id: 'limonaia-castel',
          name: 'Limonaia del Castèl',
          category: 'מוזיאון / לימונים · אופציונלי',
          description: 'בית לימון היסטורי במרכז Limone. רק אם הוא משתלב באופן טבעי בזמן השיטוט ולא הופך את העצירה לעמוסה.',
          details: {
            openingHours: '10.10.2026 · 10:00–18:00',
            price: '€2 לאדם',
            address: 'Via Orti 9, 25010 Limone sul Garda BS, Italy',
            notes: 'לא חלק מהלו״ז הקבוע; העדיפות היא לעיירה, האגם והאווירה.',
            website: 'https://www.visitlimonesulgarda.com/en/museums/the-limonaia-del-castel/',
          },
        },
        {
          id: 'omkafe-arco',
          name: 'Omkafè',
          category: 'קפה / מוזיאון · אופציונלי',
          description: 'מוזיאון קפה, חנות וטעימה ב־Arco. נשאר כאופציה קיימת בלבד ולא משנים את סדר היום בשבילו.',
          details: {
            openingHours: 'ב׳–ש׳ 08:30–12:30 ו־14:00–18:00 · א׳ סגור',
            price: 'כניסה למוזיאון חינם',
            address: 'Via Aldo Moro 7, 38062 Arco TN, Italy',
            notes: 'רק אם נוצר זמן ספייר אמיתי; לא לסטות מהמסלול החדש במיוחד בשבילו.',
            website: 'https://www.omkafe.com/en/visita-omkafe',
          },
        },
      ],
      alerts: [
        'כל היום ברכב השכור — אין מעבורת ואין תחבורה ציבורית בין Riva ל־Limone.',
        'המזוודות נשארות ברכב לאורך היום: לשמור הכול מוסתר בתא המטען הסגור ולהעדיף חניונים ציבוריים / רשמיים. לא להשאיר שום דבר גלוי בתא הנוסעים.',
        'Ciclopista del Garda: עושים רק טעימה מהקטע הפנורמי התלוי ליד Capo Reamol — לא את המסלול המלא. השביל המפורסם לא ממשיך כיום עד Riva del Garda; הוא מסתיים בגבול Lombardia / Trentino, ולכן הולכים 500–800 מ׳, מסתובבים וחוזרים באותו שביל.',
      ],
      stops: [
        place({ id: 'dolomiti-exclusive-checkout-day9', type: 'hotel', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · צ׳ק־אאוט ויציאה', time: '08:00', status: 'booked', coordinates: coords.dolomitiExclusive, details: { address: 'Strada Dolomites 55/A int.1, 38036 Sèn Jan di Fassa (TN), Italy', notes: 'יציאה ישירה לכיוון Lake Garda. זו הנסיעה הארוכה של הבוקר מהדולומיטים לצפון האגם.' } }),
        drive('drive-pozza-varone-day9', 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → Parco Grotta Cascata Varone', 'כ־1:50–2:05 שעות', '08:00–≈10:00', { notes: 'נסיעת הבוקר הארוכה מהדולומיטים לכיוון Lake Garda. היעד הוא להגיע סביב 10:00, בלי צורך לצאת ב־07:00.' }),
        place({ id: 'varone-waterfall', type: 'activity', name: 'Parco Grotta Cascata Varone', time: '10:00–11:00', duration: 'כ־45–60 דקות', status: 'planned', coordinates: coords.varone, details: { openingHours: 'באוקטובר: 09:00–17:00', price: '€7 לאדם', address: 'Località le Foci 3, 38060 Tenno (TN), Italy', notes: 'ביקור במפל ובמערות. משתמשים בחניה המסומנת למבקרים לפי השילוט במקום; המזוודות נשארות מוסתרות בתא המטען.' } }),
        drive('drive-varone-riva-day9', 'Parco Grotta Cascata Varone → Riva del Garda', 'כ־10 דקות', '11:00–11:10'),
        place({ id: 'riva-day', type: 'activity', name: 'Riva del Garda', time: '11:10–13:00', duration: 'כ־1:50 שעות', status: 'planned', coordinates: coords.riva, details: { parking: 'לחנות בחניון ציבורי / רשמי ולהשאיר את המזוודות מוסתרות בתא המטען', notes: 'עצירה רגועה: הליכה קצרה לאורך האגם, המרכז / העיר העתיקה וזמן לארוחת צהריים. לא בונים רשימת אטרקציות נפרדת.' } }),
        drive('drive-riva-reamol-day9', 'Riva del Garda → Capo Reamol / Ciclopista del Garda', 'כ־10–15 דקות', '13:00–13:15', { notes: 'ממשיכים עם הרכב דרומה לאורך Gardesana לכיוון הקטע הפנורמי.' }),
        place({ id: 'ciclopista-reamol', type: 'activity', name: 'Ciclopista del Garda – Capo Reamol', time: '13:15–14:00', duration: 'כ־30–45 דקות', status: 'planned', coordinates: coords.capoReamol, details: { address: 'Ciclopista del Garda – Capo Reamol, Limone sul Garda BS, Italy', parking: 'בחירה ראשונה: Parcheggio all’inizio della ciclopedonale — עד 2 שעות, 9 מקומות, נגיש משני הכיוונים · 45.824151, 10.810157. בחירה שנייה: Parcheggio presso la ciclopedonale — עד 2 שעות, 4 מקומות, נגיש רק כשמגיעים מכיוון Riva · 45.825557, 10.814022.', notes: 'לא עושים את כל המסלול. הולכים בערך 500–800 מ׳ על הקטע התלוי, מצטלמים, מסתובבים וחוזרים לרכב באותו שביל. סה״כ כ־1–1.6 ק״מ. אם שני החניונים הקטנים מלאים — לא מבזבזים זמן בהמתנה; ממשיכים ל־Limone ומחליטים שם אם בכלל לחזור לרעיון. אין השכרת אופניים בתכנון.' , website: 'https://www.visitlimonesulgarda.com/it/parcheggi-a-limone-sul-garda.html' } }),
        drive('drive-reamol-limone-day9', 'Capo Reamol → Limone sul Garda', 'כ־5–10 דקות', '14:00–14:10'),
        place({ id: 'limone', type: 'activity', name: 'Limone sul Garda', time: '14:10–16:00', duration: 'כ־1:50 שעות', status: 'planned', coordinates: coords.limone, details: { parking: 'חניה ציבורית רשמית במרכז. אופציות גדולות: Multipiano via Caldogno או Multipiano Lungolago.', notes: 'עצירה רגועה אחרי השביל: טיילת האגם, הרחובות הישנים, הנמל / waterfront, אווירת עיירת הלימונים וקפה אם מתחשק. לא מוסיפים פעילות ארוכה נוספת.' } }),
        drive('drive-limone-abacus-day9', 'Limone sul Garda → Abacus Hotel, Sesto San Giovanni', 'להקצות כ־2:15–2:45 שעות', '≈16:00–≈18:15/18:45', { notes: 'זמן הנהיגה הבסיסי ל־Sesto הוא סביב שעתיים; בפועל שומרים buffer לתנועה של שבת אחה״צ וליציאה מאזור Garda.' }),
        place({ id: 'abacus-hotel-day9', type: 'hotel', name: 'Abacus Hotel', time: 'הגעה משוערת ≈18:15–18:45', status: 'booked', coordinates: coords.abacusHotel, details: { address: 'Via Monte Grappa 39, 20099 Sesto San Giovanni MI, Italy', parking: 'Garage כלול בהזמנה', openingHours: 'Check-in מ־14:00 · check-out לפני 12:00', notes: 'לילה 1 מתוך 2. נכנסים עם הרכב ישירות ל־garage של המלון.' } }),
      ],
    },
    {
"""
s = s[:day_start] + new_day + s[day_end:]

p.write_text(s)
