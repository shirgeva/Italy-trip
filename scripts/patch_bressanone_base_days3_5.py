from pathlib import Path

p = Path('index.html')
s = p.read_text()

if "id: 'echo-bressanone-day3'" in s:
    raise SystemExit(0)

# Add the selected Bressanone accommodation as a map coordinate.
coord_anchor = "  santaMaddalena: { lat: 46.6410, lng: 11.7160 },\n  ortisei: { lat: 46.5743, lng: 11.6714 },"
coord_replacement = "  santaMaddalena: { lat: 46.6410, lng: 11.7160 },\n  echoBressanone: { lat: 46.7050, lng: 11.6587 },\n  ortisei: { lat: 46.5743, lng: 11.6714 },"
if coord_anchor not in s:
    raise SystemExit('Coordinate anchor not found')
s = s.replace(coord_anchor, coord_replacement, 1)

# Maps: update Days 3-5 only.
map_start = s.index("  'day-3': {")
map_end = s.index("  'day-6': {", map_start)
new_maps = """  'day-3': {
    points: [
      { name: 'Ca’ del Lasco – Tulipano · Bellano', label: '08:00 · צ׳ק־אאוט ויציאה לכיוון הדולומיטים', ...coords.caDelLasco },
      { name: 'Elena Walch · אופציונלי', label: '≈12:00–13:00 · יקב / ביסטרו', ...coords.elenaWalch },
      { name: 'Loacker Café Bozen Twenty · אופציונלי', label: '≈13:30–14:00 · קפה / חנות', ...coords.loackerTwenty },
      { name: 'Val di Funes / Santa Maddalena', label: '≈14:50–16:30 · תצפיות והליכה קלה', ...coords.santaMaddalena },
      { name: 'ecHo Apartments & SPA · Bressanone', label: '≈16:50–17:00 · לילה 1 מתוך 2', ...coords.echoBressanone },
    ],
    routePath: [coords.caDelLasco, coords.riva, coords.elenaWalch, coords.loackerTwenty, coords.santaMaddalena, coords.echoBressanone],
  },
  'day-4': {
    points: [
      { name: 'ecHo Apartments & SPA · Bressanone', label: '07:45–08:00 · יציאה ברכב', ...coords.echoBressanone },
      { name: 'Ortisei / Seceda parking', label: '≈08:20–08:35 · חניה ועלייה לרכבל', ...coords.ortisei },
      { name: 'Seceda', label: '09:00–14:00 · רכבל + הליכה קצרה', ...coords.seceda },
      { name: 'Ortisei', label: '14:30 והלאה · זמן חופשי', ...coords.ortisei },
      { name: 'ecHo Apartments & SPA · Bressanone', label: 'חזרה כשמסיימים ב־Ortisei · לילה 2 מתוך 2', ...coords.echoBressanone },
    ],
    routePath: [coords.echoBressanone, coords.ortisei, coords.seceda, coords.ortisei, coords.echoBressanone],
  },
  'day-5': {
    points: [
      { name: 'ecHo Apartments & SPA · Bressanone', label: '07:15–07:30 · צ׳ק־אאוט ויציאה', ...coords.echoBressanone },
      { name: 'Alpe di Siusi / Compatsch', label: '≈08:00–08:15 · 08:15–11:00 ביקור', ...coords.alpeSiusi },
      { name: 'Passo Gardena · עצירת נוף', label: '≈11:45–12:00 · ממשיכים ישירות מזרחה', ...coords.passoGardena },
      { name: 'Cortina d’Ampezzo / San Vito · בסיס לינה משוער', label: '≈13:00–13:30 + מרווח לעצירות נוף', ...coords.cortina },
    ],
    routePath: [coords.echoBressanone, coords.alpeSiusi, coords.passoGardena, coords.cortina],
  },
"""
s = s[:map_start] + new_maps + s[map_end:]

# Day 3 header and final leg only; keep all existing attractions/timing before Santa Maddalena unchanged.
replacements = {
"      title: 'Bellano → Elena Walch → Val di Funes → Ortisei',": "      title: 'Bellano → Elena Walch → Val di Funes → Bressanone',",
"      routeLabel: 'Ca’ del Lasco / Bellano → North Lake Garda → Elena Walch → Loacker Twenty → Val di Funes → Ortisei',": "      routeLabel: 'Ca’ del Lasco / Bellano → North Lake Garda → Elena Walch → Loacker Twenty → Val di Funes → ecHo Apartments & SPA, Bressanone',",
"      overnight: 'Ortisei / Santa Cristina · לילה 1 מתוך 2',": "      overnight: 'ecHo Apartments & SPA · לילה 1 מתוך 2',",
"      drivingTime: 'כ־5.5–6 שעות נהיגה נטו',": "      drivingTime: 'כ־5:30–5:50 שעות נהיגה נטו',",
"      highlights: ['Ca’ del Lasco · צ׳ק־אאוט 08:00', 'Elena Walch · אופציונלי', 'Loacker Café Twenty · אופציונלי', 'Val di Funes / Santa Maddalena', 'Ortisei'],": "      highlights: ['Ca’ del Lasco · צ׳ק־אאוט 08:00', 'Elena Walch · אופציונלי', 'Loacker Café Twenty · אופציונלי', 'Val di Funes / Santa Maddalena', 'ecHo Apartments & SPA · Bressanone'],",
"      alerts: ['Ca’ del Lasco: check-out רשמי עד 10:00; אנחנו יוצאים כבר ב־08:00 לפי התכנון הקיים.'],": "      alerts: ['Ca’ del Lasco: check-out רשמי עד 10:00; אנחנו יוצאים כבר ב־08:00 לפי התכנון הקיים.', 'ecHo Apartments & SPA: check-in 14:00–19:00. ההגעה המתוכננת סביב 16:50–17:00 משאירה מרווח טוב לפני סגירת הצ׳ק־אין.'],",
"        drive('drive-funes-ortisei', 'Santa Maddalena → Ortisei', '30–45 דקות', '≈16:30'),": "        drive('drive-funes-echo', 'Santa Maddalena → ecHo Apartments & SPA, Bressanone', 'כ־20–25 דקות', '≈16:30', { notes: 'הנסיעה מ־Santa Maddalena ל־Bressanone היא בערך 20 דקות; לכתובת המלון ב־Millan נשמור טווח של 20–25 דקות.' }),",
"        place({ id: 'ortisei-arrival', type: 'hotel', name: 'Ortisei / Santa Cristina', time: '≈17:15–17:30', status: 'to-book', coordinates: coords.ortisei, details: { notes: 'צ׳ק־אין וערב רגוע. Ortisei עדיפות; Santa Cristina אם המחירים טובים יותר.' } }),": "        place({ id: 'echo-bressanone-day3', type: 'hotel', name: 'ecHo Apartments & SPA', time: '≈16:50–17:00', status: 'planning', coordinates: coords.echoBressanone, details: { address: 'Via Millan 14a, 39042 Bressanone (BZ), Italy', parking: 'חניה פרטית חינם במקום', openingHours: 'Check-in 14:00–19:00 · check-out עד 10:00', notes: 'לינה נבחרת / מתוכננת ל־4–6.10, 2 לילות. דירה עם מטבח; private / self check-in זמין. עדיין לא מסומן כהוזמן.' } }),",
}
for old, new in replacements.items():
    if old not in s:
        raise SystemExit(f'Day 3 anchor not found: {old[:60]}')
    s = s.replace(old, new, 1)

# Day 4 header: Bressanone is the hotel base; Ortisei remains the activity location.
day4_header_replacements = {
"      startBase: 'Ortisei / Santa Cristina',": "      startBase: 'ecHo Apartments & SPA, Bressanone',",
"      title: 'Seceda',": "      title: 'Seceda + Ortisei',",
"      routeLabel: 'Ortisei → Seceda → Ortisei',": "      routeLabel: 'ecHo Apartments & SPA, Bressanone → Ortisei / Seceda → Seceda → Ortisei → ecHo Apartments & SPA, Bressanone',",
"      overnight: 'Ortisei / Santa Cristina · לילה 2 מתוך 2',": "      overnight: 'ecHo Apartments & SPA · לילה 2 מתוך 2',",
"      drivingTime: 'אפס / מינימלית',": "      drivingTime: 'כ־50–70 דקות נהיגה בסך הכול · הלוך־חזור מ־Bressanone',",
"      highlights: ['Seceda'],": "      highlights: ['Seceda', 'Ortisei'],",
}
# Apply only inside Day 4 section.
d4_start = s.index("      id: 'day-4', number: 4, date: '2026-10-05'")
d4_end = s.index("      id: 'day-5', number: 5, date: '2026-10-06'", d4_start)
d4 = s[d4_start:d4_end]
for old, new in day4_header_replacements.items():
    if old not in d4:
        raise SystemExit(f'Day 4 header anchor not found: {old}')
    d4 = d4.replace(old, new, 1)

# Keep all existing parking/cable/wood-carving info; only update logistics and outdated nearby-hotel wording.
old_stops_anchor = "      stops: [\n        place({ id: 'seceda-cable-up'"
new_stops_anchor = "      stops: [\n        drive('drive-echo-ortisei-day4', 'ecHo Apartments & SPA, Bressanone → Ortisei / Seceda parking', 'כ־25–35 דקות', '07:45–08:00 יציאה', { notes: 'מ־Bressanone ל־Ortisei זמן הנהיגה הטיפוסי הוא סביב 27 דקות; שומרים טווח 25–35 דקות לפי תנועה והחניון שנבחר. יעד הגעה: בערך 08:20–08:35.' }),\n        place({ id: 'seceda-cable-up'"
if old_stops_anchor not in d4:
    raise SystemExit('Day 4 stops anchor not found')
d4 = d4.replace(old_stops_anchor, new_stops_anchor, 1)
d4 = d4.replace("time: '08:15–09:00'", "time: '08:30–09:00'", 1)
old_note = "אפשרות רכב: נוסעים רק עד תחנת הרכבל ב־Ortisei וחונים שם; אין כביש שמגיע לפסגת Seceda ולכן הרכב לא מחליף את הרכבל. אפשרות חסכונית יותר לחניה: להגיע לתחנה ברגל/תחבורה מקומית מהמלון אם נלון קרוב. זמן העלייה המתוכנן כולל חניה + שני מקטעי הרכבל Ortisei–Furnes–Seceda."
new_note = "מגיעים ברכב מ־ecHo Apartments & SPA ל־Ortisei וחונים באחת מאפשרויות החניה שכבר שמורות בדף. אין כביש שמגיע לפסגת Seceda ולכן הרכב לא מחליף את הרכבל. זמן העלייה המתוכנן כולל חניה + שני מקטעי הרכבל Ortisei–Furnes–Seceda."
if old_note not in d4:
    raise SystemExit('Day 4 Seceda note anchor not found')
d4 = d4.replace(old_note, new_note, 1)
old_end_stop = "        place({ id: 'ortisei-afternoon', type: 'activity', name: 'אחר הצהריים חופשי ב־Ortisei', nameDirection: 'rtl', time: '14:30 והלאה', status: 'optional', coordinates: coords.ortisei }),\n      ],"
new_end_stop = "        place({ id: 'ortisei-afternoon', type: 'activity', name: 'אחר הצהריים חופשי ב־Ortisei', nameDirection: 'rtl', time: '14:30 והלאה', status: 'optional', coordinates: coords.ortisei, details: { notes: 'שיטוט במרכז, בתי קפה, חנויות וזמן חופשי. אין שעת יציאה קבועה.' } }),\n        drive('drive-ortisei-echo-day4', 'Ortisei → ecHo Apartments & SPA, Bressanone', 'כ־25–35 דקות', 'כשמסיימים ב־Ortisei', { notes: 'חוזרים ברכב ל־Bressanone כשמרגישים שמיצינו את אחר הצהריים; אין שעת חזרה קשיחה.' }),\n        place({ id: 'echo-bressanone-night2', type: 'hotel', name: 'ecHo Apartments & SPA · לילה 2 מתוך 2', time: 'ערב', status: 'planning', coordinates: coords.echoBressanone, details: { address: 'Via Millan 14a, 39042 Bressanone (BZ), Italy', parking: 'חניה פרטית חינם במקום', notes: 'לילה שני ואחרון; check-out למחרת עד 10:00, אבל התכנון הוא לצאת מוקדם.' } }),\n      ],"
if old_end_stop not in d4:
    raise SystemExit('Day 4 end anchor not found')
d4 = d4.replace(old_end_stop, new_end_stop, 1)
s = s[:d4_start] + d4 + s[d4_end:]

# Day 5: switch start to Bressanone, keep Alpe/Passo/Cortina attractions and verified parking/cable info.
d5_start = s.index("      id: 'day-5', number: 5, date: '2026-10-06'")
d5_end = s.index("      id: 'day-6', number: 6, date: '2026-10-07'", d5_start)
d5 = s[d5_start:d5_end]
for old, new in {
"      startBase: 'Ortisei / Santa Cristina',": "      startBase: 'ecHo Apartments & SPA, Bressanone',",
"      routeLabel: 'Ortisei / Santa Cristina → Alpe di Siusi / Compatsch → Ortisei / Santa Cristina → Passo Gardena → Cortina d’Ampezzo / San Vito di Cadore',": "      routeLabel: 'ecHo Apartments & SPA, Bressanone → Alpe di Siusi / Compatsch → Passo Gardena → Cortina d’Ampezzo / San Vito di Cadore',",
"      drivingTime: 'כ־2.5–3 שעות נהיגה מצטברות · מפוצלות לאורך היום',": "      drivingTime: 'כ־2:15–2:45 שעות נהיגה מצטברות במסלול המועדף · ללא חזרה ל־Bressanone',",
}.items():
    if old not in d5:
        raise SystemExit(f'Day 5 header anchor not found: {old}')
    d5 = d5.replace(old, new, 1)
old_alerts = """      alerts: [
        'חשוב: אם עולים ל־Alpe di Siusi / Compatsch ברכב פרטי, העלייה מותרת רק לפני 09:00 — לכן היציאה המוקדמת מהמלון חשובה.',
        'תוכנית מזוודות: אחרי הצ׳ק־אאוט נבקש מהמלון לשמור את המזוודות לכמה שעות, ניסע ל־Alpe di Siusi בלי המטען, נחזור לאסוף אותו ואז נמשיך מזרחה. אם המלון לא מאפשר שמירת מזוודות, משאירים הכול בתא המטען וממשיכים אחרי Alpe di Siusi ישירות לכיוון Passo Gardena / Cortina בלי עצירת האיסוף.',
      ],"""
new_alerts = """      alerts: [
        'חשוב: אם עולים ל־Alpe di Siusi / Compatsch ברכב פרטי, העלייה מותרת רק לפני 09:00 — לכן היציאה מ־Bressanone סביב 07:15–07:30 חשובה.',
        'החלטת מזוודות — פתוחה / TO FINALIZE: המסלול המועדף והיעיל הוא לעשות check-out מ־ecHo בבוקר, לקחת את המזוודות איתנו, להשאיר אותן מוסתרות בתא המטען בזמן Alpe di Siusi ולהמשיך משם ישירות ל־Passo Gardena.',
        'חלופה פחות מועדפת: לבקש מ־ecHo לשמור את המזוודות ולחזור ל־Bressanone אחרי Alpe di Siusi. זו סטייה משמעותית ולכן לא מקבעים אותה במסלול כרגע.',
      ],"""
if old_alerts not in d5:
    raise SystemExit('Day 5 alerts anchor not found')
d5 = d5.replace(old_alerts, new_alerts, 1)

old_stops = """      stops: [
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
      ],"""
new_stops = """      stops: [
        place({ id: 'day5-checkout-luggage', type: 'hotel', name: 'ecHo Apartments & SPA · צ׳ק־אאוט + החלטת מזוודות', time: '07:15–07:30', status: 'planning', coordinates: coords.echoBressanone, details: { openingHours: 'Check-out עד 10:00', address: 'Via Millan 14a, 39042 Bressanone (BZ), Italy', notes: 'Preferred: לוקחים את המזוודות איתנו ומשאירים אותן מוסתרות בתא המטען בזמן Alpe di Siusi כדי להמשיך ישירות מזרחה. Alternative: לבקש שמירת מזוודות ולחזור ל־Bressanone — סטייה משמעותית ולא המסלול המועדף.' } }),
        drive('drive-echo-alpe', 'ecHo Apartments & SPA, Bressanone → Alpe di Siusi / Compatsch', 'כ־35–45 דקות', '07:15–07:30 יציאה', { notes: 'מ־Bressanone ל־Seiser Alm / Compatsch זמן הנהיגה הטיפוסי סביב 38–39 דקות. יעד הגעה: בערך 08:00–08:15, הרבה לפני סגירת העלייה לרכב פרטי ב־09:00.' }),
        place({ id: 'alpe-cable-up', type: 'planning', name: 'Alpe di Siusi / Compatsch · הגעה וחניה', time: '≈08:00–08:15', coordinates: coords.alpeSiusi, details: { price: 'רכב: P2 Compatsch €30 לרכב ליום · P1 Spitzbühl €15 לרכב + כ־30 דק׳ הליכה בעלייה | חלופה ברכבל מ־Ortisei: €41 לאדם הלוך־חזור · €82 לזוג', openingHours: 'רכב פרטי רשאי לעלות ל־Compatsch רק לפני 09:00; אפשר לרדת בכל שעה. רכבל Ortisei פועל 08:30–18:00 בתאריך שלנו.', parking: 'מ־29.6.2026 חובה להזמין מראש P1/P2 אונליין, עד 6 ימים לפני ההגעה.', notes: 'P2 Compatsch נשארת האפשרות המועדפת לנוחות. במסלול המועדף מגיעים ישירות מ־ecHo עם המזוודות מוסתרות ברכב ולא חוזרים ל־Bressanone אחרי הביקור. חלופת הרכבל מ־Ortisei נשארת כאפשרות בלבד.' } }),
        place({ id: 'alpe-siusi', name: 'Alpe di Siusi', time: '08:15–11:00', duration: 'כ־2.5–3 שעות באזור', coordinates: coords.alpeSiusi, details: { notes: 'אזור המרעה והנוף, הליכה קלה, נקודות תצפית ועצירה אופציונלית בבקתה. Gostner Schwaige נשארת כאופציה אם היא משתלבת בקצב.' } }),
        drive('drive-alpe-gardena', 'Alpe di Siusi / Compatsch → Passo Gardena · דרך Val Gardena', 'כ־45–55 דקות', '≈11:00–11:45/11:55', { notes: 'המסלול המועדף ממשיך ישירות מזרחה דרך אזור Val Gardena. Compatsch → Ortisei הוא בערך 25 דקות ו־Ortisei → Passo Gardena בערך 23 דקות, לכן שומרים טווח 45–55 דקות.' }),
        place({ id: 'passo-gardena', type: 'activity', name: 'Passo Gardena · עצירת נוף', time: '≈11:45–12:00', duration: '20–30 דקות', status: 'optional', coordinates: coords.passoGardena, details: { notes: 'עצירה קצרה לנוף בלבד; לא מסלול הליכה. אפשר להוסיף עוד עצירות נוף קטנות בדרך.' } }),
        drive('drive-gardena-cortina', 'Passo Gardena → Cortina d’Ampezzo / San Vito di Cadore', 'כ־45–60 דקות', 'אחרי העצירה', { notes: 'Passo Gardena → Cortina הוא כ־45–46 דקות נהיגה; ל־San Vito צריך מעט יותר. להשאיר מרווח לעצירות תצפית קצרות בדרך.' }),
        place({ id: 'cortina-arrival', type: 'hotel', name: 'Cortina d’Ampezzo / San Vito di Cadore', time: '≈13:00–13:30 · לפני עצירות נוספות בדרך', status: 'to-book', coordinates: coords.cortina, details: { notes: 'הגעה משוערת לאזור במסלול הישיר המועדף. אם נעצור לעוד תצפיות / ארוחה בדרך, ההגעה למלון תהיה מאוחרת יותר. יום 6 נשאר ללא שינוי.' } }),
      ],"""
if old_stops not in d5:
    raise SystemExit('Day 5 stops block not found')
d5 = d5.replace(old_stops, new_stops, 1)
s = s[:d5_start] + d5 + s[d5_end:]

# Reservations / accommodation status: selected/planned, not booked.
res_anchor = "    { id: 'hotel-lake-como', name: 'Ca’ del Lasco – Tulipano · Bellano', category: 'Hotels', date: '2026-10-02', status: 'booked' },\n    { id: 'hotels-remaining', name: 'שאר הלינות לאורך המסלול', category: 'Hotels', status: 'to-book' },"
res_new = "    { id: 'hotel-lake-como', name: 'Ca’ del Lasco – Tulipano · Bellano', category: 'Hotels', date: '2026-10-02', status: 'booked' },\n    { id: 'hotel-bressanone', name: 'ecHo Apartments & SPA · Bressanone', category: 'Hotels', date: '2026-10-04', status: 'planning' },\n    { id: 'hotels-remaining', name: 'שאר הלינות לאורך המסלול', category: 'Hotels', status: 'to-book' },"
if res_anchor not in s:
    raise SystemExit('Reservation anchor not found')
s = s.replace(res_anchor, res_new, 1)

# Trip overview route: make Bressanone base visible.
old_summary = "  routeSummary: 'Milan Malpensa → Bellano / Ca’ del Lasco → Dolomites → Pozza di Fassa / QC Terme Dolomiti → Varone Waterfall → Riva del Garda → Limone sul Garda → Milan / Sesto San Giovanni → Monza → Milan Malpensa',"
new_summary = "  routeSummary: 'Milan Malpensa → Bellano / Ca’ del Lasco → Bressanone / ecHo Apartments & SPA → Val Gardena / Dolomites → Pozza di Fassa / QC Terme Dolomiti → Varone Waterfall → Riva del Garda → Limone sul Garda → Milan / Sesto San Giovanni → Monza → Milan Malpensa',"
if old_summary not in s:
    raise SystemExit('Route summary anchor not found')
s = s.replace(old_summary, new_summary, 1)

# Guardrail: no accommodation-base wording for Santa Cristina should remain.
if 'Ortisei / Santa Cristina' in s or 'Santa Cristina' in s:
    raise SystemExit('Old Ortisei / Santa Cristina accommodation wording still remains')

p.write_text(s)
