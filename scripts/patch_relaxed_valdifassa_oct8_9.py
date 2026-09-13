from pathlib import Path

p = Path('index.html')
s = p.read_text()

if "id: 'val-san-nicolo-core'" in s:
    raise SystemExit(0)

# Verified hotel coordinate + Val San Nicolò points.
old_coords = "  dolomitiExclusive: { lat: 46.42775, lng: 11.682784 },"
new_coords = "  dolomitiExclusive: { lat: 46.42775, lng: 11.68278 },\n  vidor: { lat: 46.428797, lng: 11.693390 },\n  baitaCascate: { lat: 46.415750, lng: 11.782365 },"
if old_coords not in s:
    raise SystemExit('Hotel coordinate anchor not found')
s = s.replace(old_coords, new_coords, 1)

# Let specific days visually label the option section as optional-only without changing other days.
old_renderer = """function renderAreaOptions(day) {
  const options = day.areaOptions ?? []
  if (!options.length) return ''
  const orderedOptions = [...options].sort((a, b) => (areaOptionTopicOrder[a.id] ?? 999) - (areaOptionTopicOrder[b.id] ?? 999))
  return `<section class=\"area-options-section\" aria-label=\"אפשרויות באזור\">
    <div class=\"section-heading compact\">
      <div><span class=\"eyebrow\">אם נשאר זמן</span><h2>אפשרויות באזור</h2></div>
      <span class=\"section-note\">${options.length} מקומות ששמרנו</span>
    </div>
    <div class=\"area-options-list\">${orderedOptions.map(renderAreaOption).join('')}</div>
  </section>`
}"""
new_renderer = """function renderAreaOptions(day) {
  const options = day.areaOptions ?? []
  if (!options.length) return ''
  const orderedOptions = [...options].sort((a, b) => (areaOptionTopicOrder[a.id] ?? 999) - (areaOptionTopicOrder[b.id] ?? 999))
  const title = day.areaOptionsTitle ?? 'אפשרויות באזור'
  const eyebrow = day.areaOptionsEyebrow ?? 'אם נשאר זמן'
  return `<section class=\"area-options-section\" aria-label=\"${esc(title)}\">
    <div class=\"section-heading compact\">
      <div><span class=\"eyebrow\">${esc(eyebrow)}</span><h2>${esc(title)}</h2></div>
      <span class=\"section-note\">${options.length} מקומות ששמרנו</span>
    </div>
    <div class=\"area-options-list\">${orderedOptions.map(renderAreaOption).join('')}</div>
  </section>`
}"""
if old_renderer not in s:
    raise SystemExit('Area options renderer anchor not found')
s = s.replace(old_renderer, new_renderer, 1)

# Days 7 and 8 map only. Oct 10 and later remain unchanged.
map_start = s.index("  'day-7': {")
map_end = s.index("  'day-9': {", map_start)
new_maps = """  'day-7': {
    points: [
      { name: 'Post Residence · San Candido', label: '08:00 · יציאה', ...coords.postResidence },
      { name: 'Passo Sella · חניה', label: '≈09:25–09:35 · תוכנית עיקרית', ...coords.passoSella },
      { name: 'Rifugio Friedrich August', label: '≈09:50–11:00 · TO VERIFY', ...coords.friedrichAugust },
      { name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', label: '≈12:00 · לינה מאושרת · אחר הצהריים למלון', ...coords.dolomitiExclusive },
    ],
    routePath: [coords.postResidence, coords.passoSella, coords.friedrichAugust, coords.passoSella, coords.dolomitiExclusive],
  },
  'day-8': {
    points: [
      { name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', label: 'בוקר איטי · בסיס לינה', ...coords.dolomitiExclusive },
      { name: 'Vidor · Val San Nicolò shuttle', label: 'סוף הבוקר · תוכנית עיקרית', ...coords.vidor },
      { name: 'Val San Nicolò / Baita alle Cascate', label: 'טיול רגוע · כ־2.5–3 שעות כולל השאטל', ...coords.baitaCascate },
      { name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', label: 'אחר הצהריים · wellness / מנוחה', ...coords.dolomitiExclusive },
      { name: 'QC Terme Dolomiti', label: 'אחה״צ מאוחר / ערב · לפי ההזמנה', ...coords.pozza },
      { name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', label: 'לילה 2 מתוך 2', ...coords.dolomitiExclusive },
    ],
    routePath: [coords.dolomitiExclusive, coords.vidor, coords.baitaCascate, coords.vidor, coords.dolomitiExclusive, coords.pozza, coords.dolomitiExclusive],
  },
"""
s = s[:map_start] + new_maps + s[map_end:]

options = """[
        {
          id: 'passo-pordoi-option',
          name: 'Passo Pordoi + Sass Pordoi',
          category: 'תצפית גבוהה / רכבל',
          description: 'Passo Pordoi נגיש ברכב; משם רכבל Sass Pordoi עולה כמעט ל־3,000 מ׳ עם תצפית פנורמית. זו האופציה הגדולה והחזקה ביותר אם פתאום מתחשק לנו עוד חוויית הרים.',
          details: { openingHours: '9.10.2026 · Sass Pordoi 09:00–17:00', price: '€32 למבוגר הלוך־חזור', notes: 'אופציונלי בלבד. לא לשלב אוטומטית עם Col Rodella או עם רכבל הרים גדול נוסף באותו יום.', website: 'https://www.sasspordoi.it/en/info-times-and-prices/' },
        },
        {
          id: 'col-rodella-option',
          name: 'Col Rodella',
          category: 'רכבל / תצפית',
          description: 'רכבל מ־Campitello di Fassa לתצפיות על Sassolungo, Sella והדולומיטים מסביב. חלופה ל־Sass Pordoi, לא תוספת חובה אליו.',
          details: { openingHours: '9.10.2026 · 08:30–17:30 · עונת 2026 עד 11.10', price: '€30 למבוגר הלוך־חזור', notes: 'לבחור בו במקום Sass Pordoi אם נרצה יום תצפיות ברכבל; לא צריך לעשות את שניהם.', website: 'https://www.fassa.com/en/ski-lifts-slopes/lift-facilities-open-in-autumn' },
        },
        {
          id: 'carezza-option',
          name: 'Lago di Carezza',
          category: 'אגם / טבע',
          description: 'אגם אלפיני קטן בצבע טורקיז עם Latemar ברקע. קל ומהיר יחסית לשלב ברכב וללא צורך ברכבל.',
          details: { price: 'אין דמי כניסה לאגם · חניה בתשלום', duration: 'כ־45–60 דקות', notes: 'כ־15–20 דקות מ־Pozza di Fassa. אופציה ספונטנית טובה, אבל נשארת אופציונלית כי כבר יש לנו כמה אגמים בטיול.' },
        },
        {
          id: 'rosengarten-option',
          name: 'Carezza / Rosengarten / Catinaccio',
          category: 'רכס הרים / תצפיות',
          description: 'אפשר ליהנות מהרכס מהכביש ומאזור Carezza, או להוסיף רכבל אם נרצה עוד תצפית גבוהה.',
          details: { openingHours: '9.10.2026 · König Laurin ו־Paolina עד 17:45', price: 'רכבל הלוך־חזור סטנדרטי כ־€26 למבוגר', notes: 'הגרסה המורחבת של ביקור ב־Lago di Carezza. לא לשלב אוטומטית עם Sass Pordoi או Col Rodella.', website: 'https://carezza.it/en/lift-systems/lift-systems/lift-systems-on%20the-rosengarten-massif' },
        },
        {
          id: 'fuciade-option',
          name: 'Passo San Pellegrino + Fuciade',
          category: 'טבע / הליכה',
          description: 'אזור אלפיני פתוח עם אחו, בקתות והרים דרמטיים. מתאים אם מתחשק לנו ללכת במקום לעשות עוד רכבל.',
          details: { duration: 'המסלול הקל הרשמי: כ־7.5 ק״מ · כ־2:30 שעות', notes: 'הליכה קלה יחסית מ־Passo San Pellegrino לכיוון Fuciade ובחזרה. לוקח יותר זמן מהמלון ולכן נשאר אופציונלי.', website: 'https://www.fassa.com/en/routes-trails/san-pellegrino-pass-fuciade-san-pellegrino-pass' },
        },
        {
          id: 'fedaia-option',
          name: 'Passo Fedaia + Lago di Fedaia',
          category: 'Marmolada / נסיעה נופית',
          description: 'נסיעה נופית מתחת ל־Marmolada עם Lago di Fedaia, הסכר ותצפיות קרובות להר.',
          details: { notes: 'מתאים לנסיעה עם עצירות קצרות ולא דורש מסלול הליכה ארוך. נשאר אופציונלי.', website: 'https://www.fassa.com/en/discover-val-di-fassa/dolomite-passes/pass-fedaia' },
        },
        {
          id: 'canazei-option',
          name: 'Canazei',
          category: 'עיירה / אוכל / קפה',
          description: 'עיירת הנופש המרכזית בחלק העליון של Val di Fassa, עם מסעדות, בתי קפה, חנויות ואווירת הרים.',
          details: { notes: 'לא אטרקציה מרכזית. מתאים לעצירה קצרה לאוכל / קפה אם כבר נמצאים באזור.' },
        },
        {
          id: 'moena-option',
          name: 'Moena',
          category: 'עיירה / אוכל / שיטוט',
          description: 'עיירה נעימה בדרום Val di Fassa עם מרכז יפה, מסעדות ובתי קפה.',
          details: { notes: 'עדיפות נמוכה עבורנו כי שיטוט בעיירות הוא לא המוקד. רק אם זה נופל טוב על הדרך ומתחשק.' },
        },
      ]"""

# Replace Days 7-8 only.
day_start = s.index("      id: 'day-7', number: 7, date: '2026-10-08'")
day_end = s.index("      id: 'day-9', number: 9, date: '2026-10-10'", day_start)
new_days = f"""      id: 'day-7', number: 7, date: '2026-10-08',
      startBase: 'Post Residence, San Candido',
      title: 'San Candido → Passo Sella → hotel',
      overviewPoint: 'Passo Sella + Rifugio Friedrich August',
      area: 'Passo Sella / Val di Fassa',
      routeLabel: 'Post Residence, San Candido → Passo Sella → Rifugio Friedrich August → DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE',
      overnight: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · לילה 1 מתוך 2',
      drivingTime: 'כ־1:55–2:10 שעות נהיגה נטו · כבישי הרים',
      walking: 'כ־30–40 דקות הליכה מצטברת לבקתה וחזרה',
      highlights: ['Passo Sella + Rifugio Friedrich August · תוכנית עיקרית', 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · אחר הצהריים למנוחה'],
      areaOptionsTitle: 'אפשרויות נוספות באזור',
      areaOptionsEyebrow: 'אופציונלי בלבד',
      areaOptions: {options},
      alerts: [
        'הפילוסופיה של היום: בוקר נופי אחד משמעותי → המלון → מנוחה. לא מוסיפים אוטומטית עוד אטרקציה גדולה אחרי ההגעה ל־Pozza di Fassa.',
        'TO VERIFY: צריך עדיין לאשר ש־Rifugio Friedrich August פתוח ב־8.10.2026. אם הוא סגור, מדלגים על הבקתה וממשיכים מ־Passo Sella למלון.',
        'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE הוזמן ל־8–10.10. כתובת רשמית: Strada Dolomites 55 A, 38036 Pozza di Fassa. Check-in שמופיע כרגע ב־Booking: 15:00–21:30; אם נגיע סביב הצהריים נבקש להשאיר מזוודות / רכב אם אפשר, נאכל משהו או נעשה פעילות קטנה בלבד עד שהחדר מוכן.',
      ],
      stops: [
        drive('drive-post-passo-sella', 'Post Residence, San Candido → Passo Sella', 'כ־1:20–1:30 שעות', '08:00–≈09:25/09:35', {{ notes: 'נסיעה הררית; משאירים מעט buffer לתנועה ולתנאי הכביש.' }}),
        place({{ id: 'passo-sella-parking-day7', type: 'activity', name: 'Passo Sella · חניה', time: '≈09:25–09:35', duration: 'עצירה לוגיסטית', status: 'planned', coordinates: coords.passoSella, details: {{ notes: 'תוכנית עיקרית. מחנים באזור Passo Sella וממשיכים לבקתה ברגל.' }} }}),
        place({{ id: 'walk-passo-sella-friedrich', type: 'activity', name: 'Passo Sella → Rifugio Friedrich August · הליכה', time: '≈09:30–09:50', duration: 'כ־15–20 דקות', status: 'planned', coordinates: coords.friedrichAugust, details: {{ notes: 'הליכה קצרה מהחניה לבקתה.' }} }}),
        place({{ id: 'friedrich-august-day7', type: 'food', name: 'Rifugio Friedrich August', time: '≈09:50–11:00', duration: 'כ־1:10 שעות', status: 'planning', coordinates: coords.friedrichAugust, details: {{ openingHours: 'TO VERIFY ל־8.10.2026', notes: 'תוכנית עיקרית אם פתוח: נוף הררי, קפה / אוכל ועצירה רגועה. אם סגור — פשוט מדלגים.' }} }}),
        place({{ id: 'walk-friedrich-passo-sella', type: 'activity', name: 'Rifugio Friedrich August → Passo Sella · חזרה לרכב', time: '11:00–11:20', duration: 'כ־15–20 דקות', status: 'planned', coordinates: coords.passoSella }}),
        drive('drive-passo-sella-hotel', 'Passo Sella → DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', 'כ־30–40 דקות', '≈11:20–≈12:00', {{ notes: 'Passo Sella → Pozza di Fassa הוא כ־27–28 דקות נטו; לכתובת המדויקת ולכביש הררי שומרים טווח מעשי של 30–40 דקות.' }}),
        place({{ id: 'dolomiti-exclusive-arrival', type: 'hotel', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', time: '≈12:00 · לפני check-in', status: 'booked', coordinates: coords.dolomitiExclusive, details: {{ address: 'Strada Dolomites 55 A, 38036 Pozza di Fassa, Italy', parking: 'חניה פרטית חינם במקום', openingHours: 'Check-in כרגע מופיע 15:00–21:30 · check-out עד 10:00', notes: 'הוזמן ל־8–10.10, 2 לילות. אם החדר עדיין לא מוכן: מבקשים להשאיר מזוודות / רכב אם אפשר, אוכלים צהריים או עושים משהו קטן ורגוע בלבד.' }} }}),
        place({{ id: 'hotel-relax-day7', type: 'activity', name: 'זמן מלון / wellness / מנוחה', nameDirection: 'rtl', time: 'אחר הצהריים', duration: 'בכוונה ללא לו״ז קשיח', status: 'planned', coordinates: coords.dolomitiExclusive, details: {{ notes: 'המלון הוא חלק מהחוויה: suite, sauna / wellness, אזורי מנוחה ונוף הרים. זה זמן מתוכנן, לא “חור” בלו״ז.' }} }}),
        place({{ id: 'dolomiti-exclusive-night1', type: 'hotel', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · לילה 1 מתוך 2', time: 'ערב', status: 'booked', coordinates: coords.dolomitiExclusive, details: {{ address: 'Strada Dolomites 55 A, 38036 Pozza di Fassa, Italy' }} }}),
      ],
    }},
    {{
      id: 'day-8', number: 8, date: '2026-10-09',
      startBase: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE, Pozza di Fassa',
      title: 'Val San Nicolò + hotel + QC Terme Dolomiti',
      overviewPoint: 'Val San Nicolò + QC Terme Dolomiti',
      area: 'Val di Fassa / Pozza di Fassa',
      routeLabel: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → Val San Nicolò → hotel / wellness → QC Terme Dolomiti → hotel',
      overnight: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · לילה 2 מתוך 2',
      drivingTime: 'נהיגה מינימלית · כמה דקות ל־Vidor ול־QC Terme + shuttle ל־Val San Nicolò',
      walking: 'Val San Nicolò: יציאה רגועה של כ־2.5–3 שעות כולל shuttle והליכה',
      highlights: ['Val San Nicolò · תוכנית עיקרית', 'Hotel / wellness · זמן מכוון', 'QC Terme Dolomiti · תוכנית עיקרית'],
      areaOptionsTitle: 'אפשרויות נוספות באזור',
      areaOptionsEyebrow: 'אופציונלי בלבד',
      areaOptions: {options},
      alerts: [
        'יום רגוע בכוונה: חוויה אחת בטבע → זמן משמעותי במלון → QC Terme Dolomiti. אין אטרקציה קבועה נוספת בין Val San Nicolò לספא.',
        'Val San Nicolò shuttle מאומת ל־9.10.2026: בלוח הרשמי של Comune di San Giovanni di Fassa השירות פועל 29.5–11.10, 08:30–18:30. המחיר €7 לכיוון והשירות בערך כל 30 דקות. עם Val di Fassa Guest Card יש נסיעת הלוך־חזור חינם בתקופת הסתיו 7.9–11.10, בכפוף להצגת הכרטיס.',
        'לא בונים את היום סביב Buffaure, Ciampac או Ciampedie: לפי לוחות 2026 הרשמיים הם כבר מחוץ לעונת הפעילות בתאריך שלנו.',
      ],
      stops: [
        place({{ id: 'dolomiti-exclusive-day8-start', type: 'hotel', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · בוקר איטי', time: 'בוקר', status: 'booked', coordinates: coords.dolomitiExclusive, details: {{ address: 'Strada Dolomites 55 A, 38036 Pozza di Fassa, Italy', notes: 'לא ממהרים לצאת. ארוחת בוקר / חדר / wellness בקצב רגוע.' }} }}),
        drive('drive-hotel-vidor', 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → Vidor / Val San Nicolò shuttle', 'כ־2–5 דקות', 'סוף הבוקר', {{ notes: 'נסיעה קצרה בתוך Pozza di Fassa לכיוון Strada de Meida / Vidor. מחנים באזור Vidor; לא נוסעים ברכב פרטי לעמק העליון.' }}),
        place({{ id: 'val-san-nicolo-core', type: 'activity', name: 'Val San Nicolò', time: 'סוף הבוקר / צהריים', duration: 'כ־2.5–3 שעות כולל shuttle והליכה', status: 'planned', coordinates: coords.baitaCascate, details: {{ price: 'Shuttle: €7 לכיוון · Val di Fassa Guest Card: נסיעת הלוך־חזור חינם בתקופת הסתיו לפי התנאים הרשמיים', openingHours: 'Shuttle 29.5–11.10.2026 · 08:30–18:30 · בערך כל 30 דקות', parking: 'Parking / ticket area ב־Vidor', notes: 'תוכנית עיקרית: shuttle לכיוון Saùch → הליכה קלה ורגועה בעמק → ממשיכים לכיוון Baita alle Cascate / המפלים לפי הקצב → חוזרים. לא הופכים את זה לטרק ארוך.' , website: 'https://www.fassa.com/en/services/val-san-nicolo-transport' }} }}),
        drive('drive-vidor-hotel', 'Vidor → DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', 'כ־2–5 דקות', 'אחרי החזרה מהעמק'),
        place({{ id: 'hotel-relax-day8', type: 'activity', name: 'זמן מלון / wellness / מנוחה', nameDirection: 'rtl', time: 'אחר הצהריים', duration: 'בלוק זמן משמעותי', status: 'planned', coordinates: coords.dolomitiExclusive, details: {{ notes: 'זמן מכוון ליהנות מה־suite, sauna / spa facilities, אזורי המנוחה והמלון עצמו. לא מוסיפים כאן אטרקציה קבועה.' }} }}),
        place({{ id: 'qc-terme', type: 'activity', name: 'QC Terme Dolomiti', time: 'אחה״צ מאוחר / ערב · לפי ההזמנה', duration: 'בהתאם להזמנה', status: 'to-book', coordinates: coords.pozza, details: {{ reservation: 'שעה מדויקת תיקבע בעת ההזמנה', address: 'Strada di Bagnes 21, 38036 Pozza di Fassa, Italy', notes: 'תוכנית עיקרית. הספא קרוב מאוד למלון; לא מקבעים שעה לפני שההזמנה מאושרת.' }} }}),
        drive('drive-qc-hotel-day8', 'QC Terme Dolomiti → DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', 'כ־2–5 דקות', 'אחרי הספא'),
        place({{ id: 'dolomiti-exclusive-night2', type: 'hotel', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · לילה 2 מתוך 2', time: 'לילה', status: 'booked', coordinates: coords.dolomitiExclusive, details: {{ address: 'Strada Dolomites 55 A, 38036 Pozza di Fassa, Italy', notes: 'לילה שני ואחרון. 10.10 נשאר ללא שינוי.' }} }}),
      ],
    }},
    {{
"""
s = s[:day_start] + new_days + s[day_end:]

# Booking status and official address wording. Do not alter Oct 10+ day content.
old_res = "    { id: 'hotel-pozza', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · Pozza di Fassa', category: 'Hotels', date: '2026-10-08', status: 'planning' },"
new_res = "    { id: 'hotel-pozza', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · Pozza di Fassa · 8–10.10', category: 'Hotels', date: '2026-10-08', status: 'booked' },"
if old_res not in s:
    raise SystemExit('Pozza reservation row not found')
s = s.replace(old_res, new_res, 1)

# Standardize hotel address in the edited dates only and remove the old 55-without-A form globally where it names this property.
s = s.replace('55 Strada Dolomites, 38036 Pozza di Fassa, Italy', 'Strada Dolomites 55 A, 38036 Pozza di Fassa, Italy')

p.write_text(s)
