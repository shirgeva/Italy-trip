from pathlib import Path

p = Path('index.html')
s = p.read_text()

if "id: 'post-residence-day5'" in s:
    raise SystemExit(0)

# Exact booking-address map point for Post Residence.
coord_anchor = "  sanCandido: { lat: 46.7324, lng: 12.2796 },"
coord_new = "  sanCandido: { lat: 46.7324, lng: 12.2796 },\n  postResidence: { lat: 46.732206, lng: 12.282275 },"
if coord_anchor not in s:
    raise SystemExit('San Candido coordinate anchor not found')
s = s.replace(coord_anchor, coord_new, 1)

# Replace daily map configurations for Days 5-7 only.
map_start = s.index("  'day-5': {")
map_end = s.index("  'day-8': {", map_start)
new_maps = """  'day-5': {
    points: [
      { name: 'ecHo Apartments & SPA · Bressanone', label: '07:15–07:30 · צ׳ק־אאוט ויציאה', ...coords.echoBressanone },
      { name: 'Alpe di Siusi / Compatsch', label: '≈08:00–08:15 · 08:15–11:00 ביקור', ...coords.alpeSiusi },
      { name: 'Passo Gardena · עצירת נוף', label: '≈11:45–12:00 · 20–30 דק׳', ...coords.passoGardena },
      { name: 'Post Residence - Home of Memories - Dolomites', label: 'San Candido · הגעה משוערת ≈13:30–14:15 · לילה 1 מתוך 2', ...coords.postResidence },
    ],
    routePath: [coords.echoBressanone, coords.alpeSiusi, coords.passoGardena, coords.postResidence],
  },
  'day-6': {
    points: [
      { name: 'Post Residence · San Candido', label: '08:00 · יציאה', ...coords.postResidence },
      { name: 'Tre Cime di Lavaredo / Rifugio Auronzo', label: '≈08:40 · 08:40–11:30', ...coords.treCime },
      { name: 'Lago di Misurina', label: '≈11:45–12:15 · עצירת נוף קצרה', ...coords.misurina },
      { name: 'Lago di Braies', label: '≈13:00–14:15/14:30 · גמיש', ...coords.braies },
      { name: 'Post Residence · San Candido', label: '≈14:35–14:50 · חניה במלון', ...coords.postResidence },
      { name: 'Monte Baranci / Funbob', label: '≈15:00–16:30/17:00 · כ־5 דק׳ הליכה מהמלון', ...coords.sanCandido },
    ],
    routePath: [coords.postResidence, coords.treCime, coords.misurina, coords.braies, coords.postResidence, coords.sanCandido, coords.postResidence],
  },
  'day-7': {
    points: [
      { name: 'Post Residence · San Candido', label: '08:00 · יציאה מערבה', ...coords.postResidence },
      { name: 'Passo Sella · חניה', label: '≈09:25–09:35 · מכאן ממשיכים ברגל', ...coords.passoSella },
      { name: 'Rifugio Friedrich August', label: '≈09:50–11:00 · TO VERIFY', ...coords.friedrichAugust },
      { name: 'Pozza di Fassa / Val di Fassa', label: '≈11:50–12:10 · בסיס לינה', ...coords.pozza },
    ],
    routePath: [coords.postResidence, coords.passoSella, coords.friedrichAugust, coords.passoSella, coords.pozza],
  },
"""
s = s[:map_start] + new_maps + s[map_end:]

# Replace Days 5-7 only. Day 8 (Oct 9) and later remain untouched.
day_start = s.index("      id: 'day-5', number: 5, date: '2026-10-06'")
day_end = s.index("      id: 'day-8', number: 8, date: '2026-10-09'", day_start)
new_days = """      id: 'day-5', number: 5, date: '2026-10-06',
      startBase: 'ecHo Apartments & SPA, Bressanone',
      title: 'Alpe di Siusi → Passo Gardena → San Candido',
      overviewPoint: 'Alpe di Siusi → San Candido',
      area: 'Alpe di Siusi / San Candido',
      routeLabel: 'ecHo Apartments & SPA, Bressanone → Alpe di Siusi / Compatsch → Passo Gardena → Post Residence, San Candido',
      overnight: 'Post Residence - Home of Memories - Dolomites · לילה 1 מתוך 2',
      drivingTime: 'כ־2:35–3:10 שעות נהיגה נטו · בהתאם לכבישי ההרים',
      walking: '1–1.5 שעות בפועל',
      highlights: ['Alpe di Siusi', 'Passo Gardena', 'San Candido'],
      areaOptions: [
        {
          id: 'gostner-schwaige',
          name: 'Gostner Schwaige',
          category: 'מחלבת הרים / אוכל',
          description: 'Malga אמיתית ב־Alpe di Siusi עם ייצור עצמי של יוגורט וגבינות מחלב אלפיני. טובה לעצירה אם היא משתלבת בהליכה שלנו.',
          details: {
            openingHours: '29.5–29.10.2026 · סביב 09:00–17:30 · מטבח חם 11:00–16:30',
            price: 'אין דמי כניסה · משלמים על אוכל ומוצרים',
            address: 'Saltria 13, 39040 Alpe di Siusi / Seiser Alm, Italy',
            notes: 'לא מצאתי סדנת הכנת גבינה פעילה באוקטובר; זו בקתת הרים עם ייצור ומוצרים מקומיים.',
            website: 'https://www.seiseralm.it/en/info-service/current-information/information-a-z/E1B51F35362CDDEA97FFD47F074A6BEC-p-cheese-dairy-gostner-mountain-hut.html',
          },
        },
      ],
      alerts: [
        'חשוב: אם עולים ל־Alpe di Siusi / Compatsch ברכב פרטי, העלייה מותרת רק לפני 09:00 — לכן היציאה מ־Bressanone סביב 07:15–07:30 חשובה.',
        'החלטת מזוודות — פתוחה / TO FINALIZE: המסלול המועדף והיעיל הוא לעשות check-out מ־ecHo בבוקר, לקחת את המזוודות איתנו, להשאיר אותן מוסתרות בתא המטען בזמן Alpe di Siusi ולהמשיך משם ישירות ל־Passo Gardena ואז San Candido.',
        'חלופה פחות מועדפת: לבקש מ־ecHo לשמור את המזוודות ולחזור ל־Bressanone אחרי Alpe di Siusi. זו סטייה משמעותית ולכן לא מקבעים אותה במסלול.',
      ],
      stops: [
        place({ id: 'day5-checkout-luggage', type: 'hotel', name: 'ecHo Apartments & SPA · צ׳ק־אאוט + החלטת מזוודות', time: '07:15–07:30', status: 'planning', coordinates: coords.echoBressanone, details: { openingHours: 'Check-out עד 10:00', address: 'Via Millan 14a, 39042 Bressanone (BZ), Italy', notes: 'Preferred: לוקחים את המזוודות איתנו ומשאירים אותן מוסתרות בתא המטען בזמן Alpe di Siusi כדי להמשיך ישירות מזרחה. Alternative: לבקש שמירת מזוודות ולחזור ל־Bressanone — סטייה משמעותית ולא המסלול המועדף.' } }),
        drive('drive-echo-alpe', 'ecHo Apartments & SPA, Bressanone → Alpe di Siusi / Compatsch', 'כ־35–45 דקות', '07:15–07:30 יציאה', { notes: 'יעד הגעה: בערך 08:00–08:15, הרבה לפני סגירת העלייה לרכב פרטי ב־09:00.' }),
        place({ id: 'alpe-cable-up', type: 'planning', name: 'Alpe di Siusi / Compatsch · הגעה וחניה', time: '≈08:00–08:15', coordinates: coords.alpeSiusi, details: { price: 'רכב: P2 Compatsch €30 לרכב ליום · P1 Spitzbühl €15 לרכב + כ־30 דק׳ הליכה בעלייה | חלופה ברכבל מ־Ortisei: €41 לאדם הלוך־חזור · €82 לזוג', openingHours: 'רכב פרטי רשאי לעלות ל־Compatsch רק לפני 09:00; אפשר לרדת בכל שעה. רכבל Ortisei פועל 08:30–18:00 בתאריך שלנו.', parking: 'מ־29.6.2026 חובה להזמין מראש P1/P2 אונליין, עד 6 ימים לפני ההגעה.', notes: 'P2 Compatsch נשארת האפשרות המועדפת לנוחות. במסלול המועדף מגיעים ישירות מ־ecHo עם המזוודות מוסתרות ברכב ולא חוזרים ל־Bressanone אחרי הביקור. חלופת הרכבל מ־Ortisei נשארת כאפשרות בלבד.' } }),
        place({ id: 'alpe-siusi', name: 'Alpe di Siusi', time: '08:15–11:00', duration: 'כ־2.5–3 שעות באזור', coordinates: coords.alpeSiusi, details: { notes: 'אזור המרעה והנוף, הליכה קלה, נקודות תצפית ועצירה אופציונלית בבקתה. Gostner Schwaige נשארת כאופציה אם היא משתלבת בקצב.' } }),
        drive('drive-alpe-gardena', 'Alpe di Siusi / Compatsch → Passo Gardena · דרך Val Gardena', 'כ־45–55 דקות', '≈11:00–11:45/11:55', { notes: 'ממשיכים ישירות מזרחה דרך אזור Val Gardena; אין חזרה למלון.' }),
        place({ id: 'passo-gardena', type: 'activity', name: 'Passo Gardena · עצירת נוף', time: '≈11:45–12:00', duration: '20–30 דקות', status: 'optional', coordinates: coords.passoGardena, details: { notes: 'עצירה קצרה לנוף בלבד; לא מסלול הליכה. אפשר להוסיף עוד עצירות נוף קטנות בדרך.' } }),
        drive('drive-gardena-sancandido', 'Passo Gardena → Post Residence, San Candido', 'כ־1:15–1:30 שעות', 'אחרי עצירת הנוף', { notes: 'כביש הררי דרך Alta Badia / Val Pusteria. Corvara → San Candido לבדו הוא בערך שעה, ולכן משאירים טווח של 1:15–1:30 מ־Passo Gardena לפי תנועה ותנאי הדרך.' }),
        place({ id: 'post-residence-day5', type: 'hotel', name: 'Post Residence - Home of Memories - Dolomites', time: 'הגעה משוערת ≈13:30–14:15', status: 'planning', coordinates: coords.postResidence, details: { address: 'Benediktinerstraße 10c, 39038 San Candido, Italy', parking: 'Private parking available on site', notes: 'לינה נבחרת / מתוכננת ל־6–8.10, 2 לילות. Booking מציג את הכתובת Benediktinerstraße 10c; אתרי התיירות הרשמיים של האזור מציגים את אותו Post Residence גם כ־Piazza del Magistrato 5. המלון נמצא במרכז San Candido.' } }),
      ],
    },
    {
      id: 'day-6', number: 6, date: '2026-10-07',
      startBase: 'Post Residence, San Candido',
      title: 'San Candido → Tre Cime → Misurina → Lago di Braies → Funbob',
      overviewPoint: 'Tre Cime + Lago di Braies + Funbob',
      area: '3 Zinnen Dolomites / San Candido',
      routeLabel: 'San Candido → Tre Cime → Lago di Misurina → Lago di Braies → San Candido / Monte Baranci → Post Residence',
      overnight: 'Post Residence - Home of Memories - Dolomites · לילה 2 מתוך 2',
      drivingTime: 'כ־1:50–2:00 שעות נהיגה בסך הכול · Funbob בסוף היום ברגל מהמלון',
      walking: 'Tre Cime קצר + Lago di Braies + כ־5 דקות מהמלון ל־Monte Baranci',
      highlights: ['Tre Cime di Lavaredo', 'Lago di Braies', 'Funbob Monte Baranci'],
      areaOptions: [
        {
          id: 'loacker-olang',
          name: 'Loacker Café Olang / Valdaora',
          category: 'קפה וחנות',
          description: 'סניף רשמי באזור Pusteria, יחסית קרוב לאזור Lago di Braies. הוא דורש סטייה ולכן נשמר רק כאפשרות אם היום זורם.',
          details: {
            openingHours: 'ב׳–ש׳ 07:00–12:00 ו־14:00–17:00 · א׳ סגור',
            price: 'אין דמי כניסה · תשלום לפי הזמנה או קנייה',
            address: 'Bahnhofstraße 11 A, 39030 Olang (Valdaora) BZ, Italy',
            notes: 'לא לשנות את יום Tre Cime / Braies במיוחד בשביל הסניף.',
            website: 'https://www.loacker.com/int/en/experience-loacker/loacker-cafe/loacker-cafes/loacker-cafe-Olang---Valdaora.html',
          },
        },
      ],
      alerts: [
        'זה היום הכי תלוי במזג האוויר; אם התחזית לא טובה, עדיף להחליף אותו עם יום אחר בדולומיטים.',
        'הסדר החדש מכוון: Lago di Braies לפני Funbob. חוזרים ל־San Candido פעם אחת בלבד, מחנים ב־Post Residence ואז מסיימים את היום ב־Monte Baranci שנמצא בערך 5 דקות הליכה מהמלון.',
      ],
      stops: [
        drive('drive-post-tre-cime', 'Post Residence, San Candido → Rifugio Auronzo / Tre Cime', 'כ־40 דקות', '08:00 יציאה'),
        place({ id: 'tre-cime', name: 'Tre Cime di Lavaredo', time: '08:40–11:30', duration: '2–2.5 שעות', status: 'to-book', coordinates: coords.treCime, details: { price: '€40 לעלייה ברכב', reservation: 'נדרשת הזמנה מראש', notes: 'לא עושים את ההקפה המלאה: מהחניון לכיוון Rifugio Lavaredo / התצפיות וחזרה. פתיחת הכביש באוקטובר תלויה במזג האוויר.' } }),
        drive('drive-tre-cime-misurina', 'Tre Cime / Rifugio Auronzo → Lago di Misurina', '≈20 דקות', '≈11:30'),
        place({ id: 'misurina', name: 'Lago di Misurina', time: '11:45–12:15', duration: 'כ־30 דקות', coordinates: coords.misurina, details: { notes: 'עצירת נוף קצרה בלבד.' } }),
        drive('drive-misurina-braies', 'Lago di Misurina → Lago di Braies', 'כ־30–35 דקות', '≈12:15–12:45/12:50'),
        place({ id: 'braies', name: 'Lago di Braies', time: '≈13:00–14:15/14:30', duration: 'כ־1:15–1:30 שעות · גמיש', coordinates: coords.braies, details: { notes: 'נוף + הליכה רגועה לאורך חלק מהאגם. לא חייבים את ההקפה המלאה של כ־3.6 ק״מ.' } }),
        drive('drive-braies-post', 'Lago di Braies → Post Residence, San Candido', 'כ־20 דקות', '≈14:15/14:30–14:35/14:50', { notes: 'חוזרים ישירות למלון במרכז San Candido, משאירים את הרכב ואז ממשיכים ברגל ל־Monte Baranci / Funbob.' }),
        place({ id: 'post-parking-before-funbob', type: 'hotel', name: 'Post Residence · חניה והפסקה קצרה', time: '≈14:35–14:50', duration: 'קצר', status: 'planning', coordinates: coords.postResidence, details: { notes: 'Haunold / Monte Baranci נמצא בערך 5 דקות הליכה מה־Post Residence, ולכן אין צורך להזיז שוב את הרכב.' } }),
        place({ id: 'funbob-baranci', type: 'activity', name: 'Monte Baranci + Funbob', time: '≈15:00–16:30/17:00', duration: 'כ־1.5–2 שעות', coordinates: coords.sanCandido, details: { price: 'כיסא עלייה: €21.50 לאדם אונליין / €24 בקופה · Funbob ירידה אחת: €21.50 לאדם · כיסא ירידה: €10 אונליין / €11 בקופה · כיסא הלוך־חזור: €31.50 אונליין / €35 בקופה', openingHours: 'ב־7.10: Funbob 09:15–17:30', parking: 'Parking Baranci גדול ליד התחנה · חינם עם כרטיס רכבל תקף; במסלול שלנו עדיף להשאיר את הרכב ב־Post Residence וללכת כ־5 דקות.', notes: 'עולים בכיסא, נהנים מהנוף ואפשר לעצור לאוכל / מנוחה למעלה. שתי אופציות: (1) שניכם Funbob — כ־€86 לזוג אונליין כולל העלייה בכיסא; (2) אייל יורד Funbob ושיר יורדת בכיסא — כ־€74.50 לזוג אונליין. אפשר גם ששניכם תרדו בכיסא — €63 לזוג הלוך־חזור אונליין. אין צורך לסיים מוקדם במיוחד; יש מרווח עד הסגירה ב־17:30.' } }),
        place({ id: 'walk-funbob-post', type: 'activity', name: 'Monte Baranci → Post Residence · ברגל', time: 'אחרי Funbob', duration: 'כ־5 דקות', status: 'planned', coordinates: coords.postResidence, details: { notes: 'חזרה קצרה ברגל למלון; אין נהיגה משמעותית אחרי האטרקציה האחרונה.' } }),
        place({ id: 'post-residence-night2', type: 'hotel', name: 'Post Residence - Home of Memories - Dolomites · לילה 2 מתוך 2', time: 'ערב', status: 'planning', coordinates: coords.postResidence, details: { address: 'Benediktinerstraße 10c, 39038 San Candido, Italy', notes: 'לילה שני ואחרון ב־San Candido.' } }),
      ],
    },
    {
      id: 'day-7', number: 7, date: '2026-10-08',
      startBase: 'Post Residence, San Candido',
      title: 'San Candido → Passo Sella → Val di Fassa',
      overviewPoint: 'Rifugio Friedrich August → Val di Fassa',
      area: 'Passo Sella / Val di Fassa',
      routeLabel: 'Post Residence, San Candido → Passo Sella → Rifugio Friedrich August → Pozza di Fassa / Val di Fassa',
      overnight: 'Pozza di Fassa / Val di Fassa · לילה 1 מתוך 2',
      drivingTime: 'כ־2 שעות נהיגה מצטברות + עצירת בוקר ב־Passo Sella',
      walking: 'כ־30–40 דקות הליכה מצטברות לבקתה וחזרה',
      highlights: ['Rifugio Friedrich August', 'Val di Fassa'],
      areaOptions: [
        {
          id: 'passo-pordoi-option',
          name: 'Passo Pordoi',
          category: 'מעבר הרים / תצפית',
          description: 'מעבר הרים דרמטי שאפשר להגיע אליו ישירות ברכב. אם רוצים את התצפית הגבוהה של Sass Pordoi ממשיכים מכאן ברכבל.',
          details: { openingHours: 'Sass Pordoi בתאריך שלנו: 09:00–17:00', price: 'רכב עד Passo Pordoi: ללא כרטיס רכבל בדרך · החניה ליד התחנה בתשלום, אך התעריף לא מפורסם באתר הרשמי', notes: 'מ־Pozza di Fassa כ־28–32 דק׳ נסיעה. זה הכיוון החסכוני אם נבחר Sass Pordoi: רכב עד המעבר ואז רק הרכבל האחרון לפסגה.' },
        },
        {
          id: 'sass-pordoi-option',
          name: 'Sass Pordoi',
          category: 'רכבל / תצפית',
          description: 'תצפית בגובה כ־2,950 מ׳. אי אפשר להגיע לפסגה ברכב; הרכב מגיע עד Passo Pordoi ומשם הרכבל עולה לפסגה בכ־4 דקות.',
          details: { openingHours: '14.5–1.11.2026 · בתאריך שלנו 09:00–17:00', price: 'אופציה חסכונית: רכב ל־Passo Pordoi + רכבל אחרון €32 לאדם הלוך־חזור · €64 לזוג. אופציית רכבלים מ־Canazei/Alba: מסלול יום €47 לאדם · €94 לזוג.', notes: 'רכב מ־Pozza ל־Passo Pordoi כ־28–32 דק׳. באופציית הרכבלים מהעמק יש גם כ־30 דק׳ הליכה בירידה עד Passo Pordoi לפני העלייה האחרונה. כרגע זו אפשרות בלבד.' },
        },
      ],
      alerts: [
        'TO VERIFY: צריך לאשר ש־Rifugio Friedrich August פתוח ב־8.10.2026. ברשומת Val Gardena הרשמית כרגע עונת הקיץ של 2026 מופיעה עד 27.9 בלבד, לכן העצירה עדיין לא מאושרת.',
        'אם Friedrich August סגור בתאריך שלנו, פשוט מורידים את העצירה וממשיכים ישירות מ־Passo Sella לכיוון Pozza di Fassa / Val di Fassa.',
        'האטרקציות הנוספות ביום הזה עדיין פתוחות לבחירה; המעבר ל־Val di Fassa והלינה באזור נשארים כמתוכנן.',
      ],
      stops: [
        drive('drive-post-passo-sella', 'Post Residence, San Candido → Passo Sella', 'כ־1:25 שעות · משוער', '08:00–≈09:25/09:35', { notes: 'נסיעה הררית ארוכה יותר מהבסיס הקודם. משאירים מעט buffer לתנועה ולתנאי הכביש.' }),
        place({ id: 'passo-sella-parking-day7', type: 'activity', name: 'Passo Sella · חניה', time: '≈09:25–09:35', duration: 'עצירה לוגיסטית', status: 'planning', coordinates: coords.passoSella, details: { notes: 'לא נוסעים עם הרכב עד Rifugio Friedrich August. מחנים באזור Passo Sella וממשיכים לבקתה ברגל.' } }),
        place({ id: 'walk-passo-sella-friedrich', type: 'activity', name: 'Passo Sella → Rifugio Friedrich August · הליכה', time: '≈09:30–09:50', duration: 'כ־15–20 דקות', status: 'planning', coordinates: coords.friedrichAugust, details: { notes: 'הליכה קצרה מהחניה לכיוון הבקתה.' } }),
        place({ id: 'friedrich-august-day7', type: 'food', name: 'Rifugio Friedrich August', time: '≈09:50–11:00', duration: 'כ־1:10 שעות', status: 'planning', coordinates: coords.friedrichAugust, details: { openingHours: 'TO VERIFY ל־8.10.2026', notes: 'עצירת בוקר לנוף הררי, קפה / ארוחת בוקר, ואם זמין — ה־Krapfen המפורסם. כרגע אין אישור שהבקתה פתוחה ב־8.10; אם היא סגורה פשוט מדלגים וממשיכים ל־Val di Fassa.' } }),
        place({ id: 'walk-friedrich-passo-sella', type: 'activity', name: 'Rifugio Friedrich August → Passo Sella · חזרה לרכב', time: '11:00–11:20', duration: 'כ־15–20 דקות', status: 'planning', coordinates: coords.passoSella, details: { notes: 'חוזרים ברגל לאזור החניה ב־Passo Sella.' } }),
        drive('drive-passo-sella-pozza', 'Passo Sella → Pozza di Fassa / Val di Fassa', 'כ־30–40 דקות · משוער', '≈11:20–11:50/12:00', { notes: 'מכאן ממשיכים לעמק ולבסיס הלינה הבא.' }),
        place({ id: 'pozza-arrival-day7', type: 'activity', name: 'Pozza di Fassa / Val di Fassa · הגעה לאזור', time: '≈11:50–12:10', status: 'planning', coordinates: coords.pozza, details: { notes: 'מגיעים לאזור סביב הצהריים. שאר האופציות שכבר שמרנו ליום הזה נשארות פתוחות לבחירה בהתאם למזג האוויר, אנרגיה ושעות הפעילות.' } }),
        place({ id: 'pozza-overnight-1', type: 'hotel', name: 'Pozza di Fassa / Val di Fassa · לילה 1 מתוך 2', time: 'ערב', status: 'to-book', coordinates: coords.pozza, details: { notes: 'זה הלילה הראשון מתוך שניים באזור הספא.' } }),
      ],
    },
    {
"""
s = s[:day_start] + new_days + s[day_end:]

# Overall trip route now includes the San Candido base.
old_summary = "  routeSummary: 'Milan Malpensa → Bellano / Ca’ del Lasco → Bressanone / ecHo Apartments & SPA → Val Gardena / Dolomites → Pozza di Fassa / QC Terme Dolomiti → Varone Waterfall → Riva del Garda → Limone sul Garda → Milan / Sesto San Giovanni → Monza → Milan Malpensa',"
new_summary = "  routeSummary: 'Milan Malpensa → Bellano / Ca’ del Lasco → Bressanone / ecHo Apartments & SPA → Alpe di Siusi / Val Gardena → San Candido / Post Residence → Pozza di Fassa / QC Terme Dolomiti → Varone Waterfall → Riva del Garda → Limone sul Garda → Milan / Sesto San Giovanni → Monza → Milan Malpensa',"
if old_summary not in s:
    raise SystemExit('Trip summary anchor not found')
s = s.replace(old_summary, new_summary, 1)

old_route_seq = "    coords.seceda,\n    coords.alpeSiusi,\n    coords.treCime,\n    coords.pozza,"
new_route_seq = "    coords.seceda,\n    coords.alpeSiusi,\n    coords.postResidence,\n    coords.treCime,\n    coords.pozza,"
if old_route_seq not in s:
    raise SystemExit('Global route path anchor not found')
s = s.replace(old_route_seq, new_route_seq, 1)

# Accommodation / reservation overview: selected/planned, not booked unless confirmed later.
res_anchor = "    { id: 'hotel-bressanone', name: 'ecHo Apartments & SPA · Bressanone', category: 'Hotels', date: '2026-10-04', status: 'planning' },\n    { id: 'hotels-remaining', name: 'שאר הלינות לאורך המסלול', category: 'Hotels', status: 'to-book' },"
res_new = "    { id: 'hotel-bressanone', name: 'ecHo Apartments & SPA · Bressanone', category: 'Hotels', date: '2026-10-04', status: 'planning' },\n    { id: 'hotel-san-candido', name: 'Post Residence - Home of Memories - Dolomites · San Candido', category: 'Hotels', date: '2026-10-06', status: 'planning' },\n    { id: 'hotels-remaining', name: 'שאר הלינות לאורך המסלול', category: 'Hotels', status: 'to-book' },"
if res_anchor not in s:
    raise SystemExit('Accommodation reservation anchor not found')
s = s.replace(res_anchor, res_new, 1)

# Ensure the old Oct 6-8 lodging placeholder is gone, without touching unrelated later-day Cortina text if any.
for old in [
    "overnight: 'Cortina / San Vito di Cadore · לילה 1 מתוך 2'",
    "overnight: 'Cortina / San Vito di Cadore · לילה 2 מתוך 2'",
    "startBase: 'Cortina / San Vito di Cadore'",
    "startBase: 'Cortina / San Vito di Cadore'",
]:
    if old in s[day_start:day_end]:
        raise SystemExit('Old Cortina/San Vito accommodation reference remains in Days 5-7')

p.write_text(s)
