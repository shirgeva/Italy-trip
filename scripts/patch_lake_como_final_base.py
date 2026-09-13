from pathlib import Path

p = Path('index.html')
s = p.read_text()

if "id: 'ca-del-lasco-day1'" in s:
    raise SystemExit(0)

# Precise Lake Como base + station coordinates.
coord_anchor = "  bellano: { lat: 46.0448, lng: 9.3023 },\n  varenna: { lat: 46.0108, lng: 9.2837 },"
coord_replacement = "  bellano: { lat: 46.0448, lng: 9.3023 },\n  caDelLasco: { lat: 46.04096, lng: 9.30424 },\n  bellanoStation: { lat: 46.03951, lng: 9.30260 },\n  varennaStation: { lat: 46.01505, lng: 9.28639 },\n  varenna: { lat: 46.0108, lng: 9.2837 },"
if coord_anchor not in s:
    raise SystemExit('Lake Como coordinate anchor not found')
s = s.replace(coord_anchor, coord_replacement, 1)

# Update daily maps for Days 1–3 only.
map_start = s.index("  'day-1': {")
map_end = s.index("  'day-4': {", map_start)
new_maps = """  'day-1': {
    points: [
      { name: 'Milan Malpensa Airport · Terminal 1', label: '14:05 נחיתה · איסוף מזוודות ורכב', ...coords.malpensa },
      { name: 'Ca’ del Lasco – Tulipano', label: 'הגעה משוערת 16:30–17:15 · לינה מאושרת', ...coords.caDelLasco },
      { name: 'Bellano · מרכז / אגם', label: 'ערב רגוע ברגל אחרי הצ׳ק־אין', ...coords.bellano },
    ],
    routePath: [coords.malpensa, coords.caDelLasco, coords.bellano, coords.caDelLasco],
  },
  'day-2': {
    points: [
      { name: 'Ca’ del Lasco – Tulipano', label: '08:40–08:45 · יציאה ברגל', ...coords.caDelLasco },
      { name: 'Orrido di Bellano', label: '09:00 · בוקר קבוע', ...coords.bellano },
      { name: 'Bellano-Tartavalle Terme', label: 'אחרי Orrido · הרכבת הראשונה שנוחה', ...coords.bellanoStation },
      { name: 'Varenna-Esino', label: 'רכבת מ־Bellano · כ־4–7 דקות', ...coords.varennaStation },
      { name: 'Varenna Ferry Terminal / Imbarcadero di Varenna', label: 'תחילת חלק המעבורות הגמיש', ...coords.varenna },
      { name: 'Bellagio', label: 'מתוכנן · זמן גמיש', ...coords.bellagio },
      { name: 'Villa Carlotta / Tremezzo · אופציונלי', label: 'רק אם החיבור נוח ומתחשק', ...coords.tremezzo },
      { name: 'Menaggio', label: 'מתוכנן · זמן גמיש', ...coords.menaggio },
      { name: 'Varenna · ערב', label: 'שיטוט / קפה / ארוחת ערב בקצב שלנו', ...coords.varenna },
      { name: 'Bellano-Tartavalle Terme', label: 'רכבת חזרה בסוף הערב', ...coords.bellanoStation },
      { name: 'Ca’ del Lasco – Tulipano', label: 'לילה 2 מתוך 2', ...coords.caDelLasco },
    ],
    routePath: [coords.caDelLasco, coords.bellano, coords.bellanoStation, coords.varennaStation, coords.varenna, coords.bellagio, coords.menaggio, coords.varenna, coords.varennaStation, coords.bellanoStation, coords.caDelLasco],
  },
  'day-3': {
    points: [
      { name: 'Ca’ del Lasco – Tulipano · Bellano', label: '08:00 · צ׳ק־אאוט ויציאה לכיוון הדולומיטים', ...coords.caDelLasco },
      { name: 'Elena Walch · אופציונלי', label: '≈12:00–13:00 · יקב / ביסטרו', ...coords.elenaWalch },
      { name: 'Loacker Café Bozen Twenty · אופציונלי', label: '≈13:30–14:00 · קפה / חנות', ...coords.loackerTwenty },
      { name: 'Val di Funes / Santa Maddalena', label: '≈14:50–16:30 · תצפיות והליכה קלה', ...coords.santaMaddalena },
      { name: 'Ortisei / Santa Cristina · בסיס לינה משוער', label: 'הגעה ≈17:15–17:30', ...coords.ortisei },
    ],
    routePath: [coords.caDelLasco, coords.riva, coords.elenaWalch, coords.loackerTwenty, coords.santaMaddalena, coords.ortisei],
  },
"""
s = s[:map_start] + new_maps + s[map_end:]

# Replace Days 1–3 only.
day_start = s.index("      id: 'day-1', number: 1, date: '2026-10-02'")
day_end = s.index("      id: 'day-4', number: 4, date: '2026-10-05'", day_start)
new_days = """      id: 'day-1', number: 1, date: '2026-10-02',
      startBase: 'Milan Malpensa Airport',
      title: 'Milan Malpensa Airport → Ca’ del Lasco, Bellano',
      overviewPoint: 'Ca’ del Lasco, Bellano',
      area: 'Bellano / Lake Como',
      routeLabel: 'Milan Malpensa Airport → Ca’ del Lasco, Bellano',
      overnight: 'Ca’ del Lasco, Bellano · לילה 1 מתוך 2',
      drivingTime: 'כ־1:20–1:45 שעות מהשדה · תלוי בתנועה',
      walking: 'ערב רגוע ברגל ב־Bellano',
      highlights: ['Ca’ del Lasco – Tulipano · הוזמן', 'Bellano · ערב רגוע'],
      areaOptions: [],
      alerts: [
        'אחרי הנחיתה לא מתכננים עצירת sightseeing בדרך — אוספים מזוודות ורכב ונוסעים ישירות ל־Ca’ del Lasco ב־Bellano.',
        'אחרי הצ׳ק־אין משאירים את הרכב בחניה הפרטית של מקום הלינה ויורדים ברגל למרכז Bellano ולאגם. בחזרה יש הליכה בעלייה ל־Ca’ del Lasco.',
      ],
      stops: [
        place({ id: 'arrival-mxp', type: 'flight', name: 'Milan Malpensa Airport · Terminal 1', time: '14:05', status: 'booked', coordinates: coords.malpensa, details: { notes: 'נחיתה ב־Milan Malpensa Airport. אחרי הנחיתה: איסוף מזוודות ואז איסוף הרכב.' } }),
        place({ id: 'rental-pickup', type: 'car', name: 'SIXT · Milano Malpensa Airport · Terminal 1', time: 'אחרי איסוף המזוודות', status: 'booked', coordinates: coords.malpensa, details: { notes: 'איסוף הרכב לפי השובר. יעד יציאה משוער מהשדה: 15:00–15:30, בהתאם לזמן המזוודות וההשכרה.' } }),
        drive('drive-mxp-ca-del-lasco', 'Milan Malpensa Airport → Ca’ del Lasco, Bellano', 'כ־1:20–1:45 שעות', 'יציאה משוערת 15:00–15:30', { notes: 'נסיעה ישירה למקום הלינה ללא עצירות sightseeing מתוכננות בדרך.' }),
        place({ id: 'ca-del-lasco-day1', type: 'hotel', name: 'Ca’ del Lasco – Tulipano', time: 'הגעה משוערת 16:30–17:15', status: 'booked', coordinates: coords.caDelLasco, details: { address: 'Via per Taceno 19, 23822 Bellano (LC), Italy', parking: 'חניה פרטית חינם במקום', openingHours: 'Self check-in · check-in 16:00–21:00 · check-out עד 10:00', notes: 'הוזמן ל־2 לילות, 2–4.10.2026. Bellano-Tartavalle Terme נמצאת כ־300 מ׳ / כ־4–5 דקות הליכה. סופרמרקטים ושירותים בסיסיים נמצאים במרחק הליכה.' } }),
        place({ id: 'bellano-evening-day1', type: 'activity', name: 'Bellano · ערב רגוע', time: 'אחרי הצ׳ק־אין', duration: 'לפי החשק', status: 'planned', coordinates: coords.bellano, details: { price: 'חינם, מלבד אוכל / קפה', notes: 'יורדים ברגל לכיוון מרכז Bellano והאגם: טיילת על שפת האגם, המרכז ההיסטורי / הרחובות הקטנים, ארוחת ערב ובית קפה אם מתחשק. בלי אטרקציה רשמית ובלי לו״ז קשיח. אחר כך חוזרים ברגל בעלייה ל־Ca’ del Lasco.' } }),
      ],
    },
    {
      id: 'day-2', number: 2, date: '2026-10-03',
      startBase: 'Ca’ del Lasco, Bellano',
      title: 'Orrido di Bellano → Bellagio → Menaggio → Varenna',
      overviewPoint: 'Orrido di Bellano + Bellagio + Menaggio + Varenna',
      area: 'Lake Como',
      routeLabel: 'Ca’ del Lasco → Orrido di Bellano → Bellano-Tartavalle Terme → Varenna-Esino → Lake Como ferries → Bellagio → Menaggio → Varenna → Bellano → Ca’ del Lasco',
      overnight: 'Ca’ del Lasco, Bellano · לילה 2 מתוך 2',
      drivingTime: 'הרכב נשאר בחניה ב־Ca’ del Lasco כל היום',
      walking: 'הליכות קצרות לתחנות / מעבורת + שיטוט גמיש בעיירות',
      highlights: ['Orrido di Bellano · 09:00 קבוע', 'Bellagio · מתוכנן', 'Menaggio · מתוכנן', 'Varenna · ערב', 'Villa Carlotta / Tremezzo · אופציונלי'],
      areaOptions: [
        {
          id: 'villa-carlotta-day2',
          name: 'Villa Carlotta',
          category: 'Tremezzo · אופציונלי בלבד',
          description: 'וילה היסטורית ב־Tremezzo עם גנים בוטניים גדולים ונוף ל־Lake Como. מוסיפים רק אם מתאים לנו בזמן ובחיבורי המעבורת.',
          details: {
            openingHours: '3.10.2026 · 10:00–19:00 · כרטיס אחרון 18:00 · המוזיאון נסגר 18:30',
            price: '€17.50 למבוגר',
            address: 'Via Statale 5605, 22016 Tremezzina, Italy',
            duration: 'ביקור עצמאי טיפוסי: כ־45–90 דקות',
            notes: 'המיקום הטבעי במסלול הוא בין Bellagio ל־Menaggio. עדיפות לסירה של Navigazione Laghi שעוצרת ב־Tremezzo – Villa Carlotta; התחנה כ־400 מ׳ מהכניסה. אם החיבור הישיר לא נוח אפשר לבדוק Cadenabbia והמשך מקומי / הליכה. אם זה מסרבל את היום — מדלגים.',
            website: 'https://www.villacarlotta.it/en/visit/',
          },
        },
      ],
      alerts: [
        'בוקר קבוע: יוצאים מ־Ca’ del Lasco ברגל 08:40–08:45 ומגיעים ל־Orrido di Bellano לפתיחה ב־09:00.',
        'אחרי Orrido היום גמיש: Bellagio ו־Menaggio מתוכננות; Villa Carlotta / Tremezzo היא העצירה היחידה שמוגדרת אופציונלית.',
        'הרכב נשאר כל היום בחניה הפרטית של Ca’ del Lasco. אחרי Orrido ממשיכים ישירות ברגל ל־Bellano-Tartavalle Terme ולא חוזרים למלון.',
        'מעבורות: 3.10 עדיין בתוך לוח הקיץ 2026. קונים כרטיסים באותו יום, משתדלים להגיע לקופה כ־20 דקות לפני, ובודקים את המעבורת הבאה במקום לעבוד לפי לו״ז קשיח. בקופה לבדוק גם אם כרטיס circular / day-type משתלם יותר מכרטיסים בודדים למסלול שנבחר בפועל.',
      ],
      stops: [
        place({ id: 'leave-ca-del-lasco-day2', type: 'activity', name: 'Ca’ del Lasco → Orrido di Bellano · ברגל', time: '08:40–08:45', duration: 'כ־10 דקות', status: 'planned', coordinates: coords.caDelLasco, details: { notes: 'יורדים ברגל מהמלון לכיוון Orrido. אין צורך להזיז את הרכב.' } }),
        place({ id: 'orrido-day2-final', type: 'attraction', name: 'Orrido di Bellano', time: '09:00', duration: 'כ־45–60 דקות', status: 'must', coordinates: coords.bellano, details: { openingHours: 'שבת 3.10.2026 · 09:00–19:00 · כניסה אחרונה 20 דקות לפני הסגירה', price: '€8 למבוגר · Orrido בלבד', address: 'Piazza S. Giorgio, 23822 Bellano LC, Italy', reservation: 'אין צורך בהזמנה מראש למבקרים יחידים', notes: 'ערוץ טבע עם מפלים, קירות סלע צרים, שבילים מוגבהים ומדרגות. יש מחיר €5 עם כרטיס רכבת או lake-navigation תקף, אבל מכיוון שאנחנו מבקרים לפני הנסיעה הראשונה באותו בוקר לא מניחים שנקבל את ההנחה אלא אם כבר יהיה לנו כרטיס תחבורה תקף.' } }),
        place({ id: 'walk-orrido-bellano-station', type: 'transfer', name: 'Orrido di Bellano → Bellano-Tartavalle Terme · ברגל', time: '≈10:00', duration: 'כ־8–10 דקות', status: 'planned', coordinates: coords.bellanoStation, details: { notes: 'אחרי Orrido ממשיכים ישירות לתחנה — לא חוזרים ל־Ca’ del Lasco.' } }),
        place({ id: 'train-bellano-varenna-day2', type: 'transfer', name: 'Bellano-Tartavalle Terme → Varenna-Esino', time: 'הרכבת הראשונה שנוחה אחרי Orrido', duration: 'כ־4–7 דקות', status: 'planned', coordinates: coords.varennaStation, details: { price: 'כ־€2 לאדם לכל כיוון · מחיר משוער בלבד, לבדוק בעת הקנייה', notes: 'לא מקבעים רכבת ספציפית עד שלוח 3.10.2026 מאושר.' } }),
        place({ id: 'walk-varenna-station-ferry', type: 'transfer', name: 'Varenna-Esino → Varenna Ferry Terminal / Imbarcadero di Varenna', time: 'אחרי הירידה מהרכבת', duration: 'כ־5–10 דקות ברגל', status: 'planned', coordinates: coords.varenna, details: { notes: 'בשלב הזה לא עושים בלוק sightseeing ב־Varenna; יורדים ישירות לכיוון המעבורות ומתחילים את החלק הגמיש של היום.' } }),
        place({ id: 'bellagio-day2-final', name: 'Bellagio', time: 'גמיש · ללא שעה קבועה', duration: 'נשארים עד שמרגישים שמיצינו', status: 'planned', coordinates: coords.bellagio, details: { price: 'העיירה עצמה חינם', notes: 'עיירת Lake Como קלאסית עם רחובות היסטוריים מדורגים, קו מים, בתי קפה, מסעדות, חנויות ונוף לאגם. מגיעים במעבורת מ־Varenna; כשמסיימים פשוט בודקים את החיבור הבא שנוח.' } }),
        place({ id: 'villa-carlotta-flex-day2-final', type: 'attraction', name: 'Villa Carlotta / Tremezzo', time: 'אופציונלי · בין Bellagio ל־Menaggio אם נוח', duration: 'כ־45–90 דקות אם נכנסים', status: 'optional', coordinates: coords.tremezzo, details: { openingHours: '3.10.2026 · 10:00–19:00 · כרטיס אחרון 18:00 · מוזיאון עד 18:30', price: '€17.50 למבוגר', address: 'Via Statale 5605, 22016 Tremezzina, Italy', notes: 'מוסיפים רק אם החיבור במעבורת נוח ומתחשק לנו גנים / וילה. לא נותנים לזה לקצר את Bellagio או Menaggio.' } }),
        place({ id: 'menaggio-day2-final', name: 'Menaggio', time: 'גמיש · ללא שעה קבועה', duration: 'לפי החשק', status: 'planned', coordinates: coords.menaggio, details: { price: 'העיירה עצמה חינם', notes: 'עיירת אגם רגועה עם כיכר מרכזית, טיילת, בתי קפה ונוף פתוח ל־Lake Como. מגיעים לפי חיבור המעבורת / הסירה שנוח באותו יום.' } }),
        place({ id: 'varenna-evening-day2', type: 'activity', name: 'Varenna · ערב גמיש', time: 'אחרי החזרה במעבורת', duration: 'ללא שעת סיום', status: 'planned', coordinates: coords.varenna, details: { price: 'חינם, מלבד אוכל / קפה', notes: 'הפעם כן מקדישים זמן ל־Varenna: טיילת על האגם, רחובות היסטוריים, בתי קפה / ארוחת ערב ושיטוט בקצב שלנו. נשארים עד שמרגישים שסיימנו.' } }),
        place({ id: 'train-varenna-bellano-evening', type: 'transfer', name: 'Varenna-Esino → Bellano-Tartavalle Terme', time: 'כשמחליטים לסיים את הערב', duration: 'כ־4–7 דקות', status: 'planned', coordinates: coords.bellanoStation, details: { price: 'כ־€2 לאדם · מחיר משוער, לבדוק בעת הקנייה', notes: 'מהטיילת / אזור המעבורות הולכים חזרה ל־Varenna-Esino ולוקחים רכבת ל־Bellano.' } }),
        place({ id: 'walk-bellano-station-hotel', type: 'transfer', name: 'Bellano-Tartavalle Terme → Ca’ del Lasco · ברגל', time: 'בסוף הערב', duration: 'כ־4–5 דקות · כ־300 מ׳', status: 'planned', coordinates: coords.caDelLasco, details: { notes: 'הליכה קצרה בעלייה חזרה למקום הלינה.' } }),
        place({ id: 'ca-del-lasco-night2', type: 'hotel', name: 'Ca’ del Lasco – Tulipano · לילה 2 מתוך 2', time: 'לילה', status: 'booked', coordinates: coords.caDelLasco, details: { address: 'Via per Taceno 19, 23822 Bellano (LC), Italy', parking: 'הרכב נשאר בחניה הפרטית החינמית כל היום', notes: 'לילה שני ואחרון. צ׳ק־אאוט למחרת עד 10:00; בפועל מתוכננת יציאה כבר ב־08:00.' } }),
      ],
    },
    {
      id: 'day-3', number: 3, date: '2026-10-04',
      startBase: 'Ca’ del Lasco / Bellano',
      title: 'Bellano → Elena Walch → Val di Funes → Ortisei',
      overviewPoint: 'Val di Funes / Santa Maddalena',
      area: 'Val di Funes / Val Gardena',
      routeLabel: 'Ca’ del Lasco / Bellano → North Lake Garda → Elena Walch → Loacker Twenty → Val di Funes → Ortisei',
      overnight: 'Ortisei / Santa Cristina · לילה 1 מתוך 2',
      drivingTime: 'כ־5.5–6 שעות נהיגה נטו',
      walking: 'עד 1–1.5 שעות הליכה קלה',
      highlights: ['Ca’ del Lasco · צ׳ק־אאוט 08:00', 'Elena Walch · אופציונלי', 'Loacker Café Twenty · אופציונלי', 'Val di Funes / Santa Maddalena', 'Ortisei'],
      alerts: ['Ca’ del Lasco: check-out רשמי עד 10:00; אנחנו יוצאים כבר ב־08:00 לפי התכנון הקיים.'],
      stops: [
        drive('drive-como-elena-walch', 'Ca’ del Lasco / Bellano → Elena Walch · דרך צפון Lake Garda', 'כ־4 שעות', '08:00 יציאה', { notes: 'צ׳ק־אאוט מ־Ca’ del Lasco לפני היציאה. שאר המסלול נשאר ללא שינוי: עוברים מצפון ל־Lake Garda דרך Riva / Rovereto / Trento. Riva היא נקודת ניתוב בלבד, לא עצירה מתוכננת.' }),
        place({ id: 'elena-walch', type: 'food', name: 'Elena Walch · Winery & Bistro', time: '12:00–13:00', duration: 'כ־שעה', status: 'optional', coordinates: coords.elenaWalch, details: { openingHours: 'יום א׳ 10:00–18:30', address: 'Via Andreas Hofer 1, 39040 Termeno sulla Strada del Vino BZ, Italy', parking: 'חניה במקום', notes: 'עצירה אופציונלית ליין בכוס / ביסטרו. לא מתכננים סיור יקב; אם עייפים או מתעכבים פשוט מדלגים.', website: 'https://www.elenawalch.com/en-GB/vinotheque-tramin' } }),
        drive('drive-elena-loacker', 'Elena Walch → Loacker Café Bozen Twenty', 'כ־25–30 דקות', '≈13:00'),
        place({ id: 'loacker-twenty', type: 'food', name: 'Loacker Café Bozen Twenty', time: '13:30–14:00', duration: '30–40 דקות', status: 'optional', coordinates: coords.loackerTwenty, details: { openingHours: 'יום א׳ 09:00–19:30', address: 'Via G. Galilei 20, 39100 Bolzano BZ, Italy', notes: 'קומה 2 ב־Twenty Shopping Center. קפה / משהו מתוק / חנות. אופציונלי — אם אין כוח או זמן ממשיכים ישר ל־Val di Funes.', website: 'https://www.loacker.com/arabia/en/experience-loacker/loacker-cafe/loacker-cafes/loacker-cafe-bolzano-twenty.html' } }),
        drive('drive-loacker-funes', 'Loacker Café Bozen Twenty → Val di Funes / Santa Maddalena', 'כ־45–55 דקות', '≈14:00'),
        place({ id: 'val-di-funes', name: 'Val di Funes / Santa Maddalena', time: '14:50–16:30', duration: '1.5–2 שעות', coordinates: coords.santaMaddalena, details: { notes: 'תצפיות, הכנסייה והליכה קלה. אפשר לקצר אם הגענו מאוחר יותר בגלל העצירות האופציונליות.' } }),
        drive('drive-funes-ortisei', 'Santa Maddalena → Ortisei', '30–45 דקות', '≈16:30'),
        place({ id: 'ortisei-arrival', type: 'hotel', name: 'Ortisei / Santa Cristina', time: '≈17:15–17:30', status: 'to-book', coordinates: coords.ortisei, details: { notes: 'צ׳ק־אין וערב רגוע. Ortisei עדיפות; Santa Cristina אם המחירים טובים יותר.' } }),
      ],
    },
    {
"""
s = s[:day_start] + new_days + s[day_end:]

# Global overview consistency for the now-confirmed Lake Como base.
s = s.replace(
    "  routeSummary: 'Milan Malpensa → Lake Como → Dolomites → Pozza di Fassa / QC Terme Dolomiti → Varone Waterfall → Riva del Garda → Limone sul Garda → Milan / Sesto San Giovanni → Monza → Milan Malpensa',",
    "  routeSummary: 'Milan Malpensa → Bellano / Ca’ del Lasco → Dolomites → Pozza di Fassa / QC Terme Dolomiti → Varone Waterfall → Riva del Garda → Limone sul Garda → Milan / Sesto San Giovanni → Monza → Milan Malpensa',",
    1,
)

anchor_old = "    { id: 'day-1-map', dayNumber: 1, href: '#/day/day-1', name: 'Bellano / Lake Como', label: 'יום 1 · 2.10', ...coords.bellano },\n    { id: 'day-2-map', dayNumber: 2, href: '#/day/day-2', name: 'Orrido di Bellano + Bellagio + Menaggio', label: 'יום 2 · 3.10', ...coords.bellano },"
anchor_new = "    { id: 'day-1-map', dayNumber: 1, href: '#/day/day-1', name: 'Ca’ del Lasco, Bellano', label: 'יום 1 · 2.10', ...coords.caDelLasco },\n    { id: 'day-2-map', dayNumber: 2, href: '#/day/day-2', name: 'Orrido di Bellano + Bellagio + Menaggio + Varenna', label: 'יום 2 · 3.10', ...coords.bellano },"
if anchor_old not in s:
    raise SystemExit('Route anchor block not found')
s = s.replace(anchor_old, anchor_new, 1)

route_path_old = "    coords.malpensa,\n    coords.bellano,\n    coords.bellagio,"
route_path_new = "    coords.malpensa,\n    coords.caDelLasco,\n    coords.bellagio,"
if route_path_old not in s:
    raise SystemExit('Global route path Lake Como anchor not found')
s = s.replace(route_path_old, route_path_new, 1)

# Reservations: confirmed Lake Como stay is booked; keep remaining lodging as still open.
res_old = "    { id: 'hotels', name: 'לינה לאורך המסלול', category: 'Hotels', status: 'to-book' },"
res_new = "    { id: 'hotel-lake-como', name: 'Ca’ del Lasco – Tulipano · Bellano', category: 'Hotels', date: '2026-10-02', status: 'booked' },\n    { id: 'hotels-remaining', name: 'שאר הלינות לאורך המסלול', category: 'Hotels', status: 'to-book' },"
if res_old not in s:
    raise SystemExit('Hotel reservation row not found')
s = s.replace(res_old, res_new, 1)

# Remove any remaining old ambiguous Lake Como base wording.
s = s.replace('Bellano / Varenna', 'Ca’ del Lasco, Bellano')
s = s.replace('Varenna · בסיס / ferry hub', 'Varenna · ferry hub')

p.write_text(s)
