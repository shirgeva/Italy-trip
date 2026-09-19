from pathlib import Path

path = Path('index.html')
text = path.read_text()

# 1) Add exact Milan coordinates used only by the updated Day 10 map.
coords_anchor = "  abacusHotel: { lat: 45.5417357, lng: 9.2368135 },\n"
coords_add = """  abacusHotel: { lat: 45.5417357, lng: 9.2368135 },
  starbucksRoastery: { lat: 45.46493, lng: 9.18620 },
  primarkTorino: { lat: 45.46140, lng: 9.18554 },
  ferrariMilano: { lat: 45.4655554, lng: 9.1910485 },
  cookingClassMilan: { lat: 45.46486, lng: 9.20698 },
  spunDuomo: { lat: 45.4637229, lng: 9.1872327 },
"""
if "starbucksRoastery:" not in text:
    if coords_anchor not in text:
        raise SystemExit('Coordinate anchor missing')
    text = text.replace(coords_anchor, coords_add, 1)

# 2) Replace only Day 10 map data.
map_start = text.index("  'day-10': {")
map_end = text.index("  'day-11': {", map_start)
new_map = """  'day-10': {
    points: [
      { name: 'Abacus Hotel · Sesto San Giovanni', label: '≈07:50–08:00 · יוצאים ברגל ל־M1', ...coords.abacusHotel },
      { name: 'Starbucks Reserve Roastery Milano', label: '08:30–09:00 · קפה / ארוחת בוקר קצרה', ...coords.starbucksRoastery },
      { name: 'Primark Milano – Via Torino', label: 'מ־09:00 · עצירת השופינג העיקרית', ...coords.primarkTorino },
      { name: 'Ferrari Flagship Store Milano', label: 'מ־10:00 · עצירה קצרה', ...coords.ferrariMilano },
      { name: 'Abacus Hotel · Sesto San Giovanni', label: '≈11:30–11:45 · חוזרים ולוקחים את הרכב', ...coords.abacusHotel },
      { name: 'Autodromo Nazionale Monza', label: '13:40 E4 · 14:50 GT3', ...coords.monza },
      { name: 'Abacus Hotel · Sesto San Giovanni', label: '≈16:30–16:45 · מחזירים את הרכב ל־garage', ...coords.abacusHotel },
      { name: 'Milano: Handmade Pasta & Iconic Dessert Making Class', label: '18:15 הגעה · 18:30–21:00 · BOOKED', ...coords.cookingClassMilan },
      { name: 'Milan center · Duomo / Galleria', label: '≈21:25 והלאה · ערב אחרון רגוע', ...coords.milan },
      { name: 'Abacus Hotel · Sesto San Giovanni', label: 'חזרה בלילה · לילה 2 מתוך 2', ...coords.abacusHotel },
    ],
    routePath: [coords.abacusHotel, coords.starbucksRoastery, coords.primarkTorino, coords.ferrariMilano, coords.abacusHotel, coords.monza, coords.abacusHotel, coords.cookingClassMilan, coords.milan, coords.abacusHotel],
    routeModes: ['TRANSIT', 'WALKING', 'WALKING', 'TRANSIT', 'DRIVING', 'DRIVING', 'TRANSIT', 'WALKING', 'TRANSIT'],
  },
"""
text = text[:map_start] + new_map + text[map_end:]

# 3) Update only the Day 10 itinerary block.
day_start = text.index("      id: 'day-10', number: 10, date: '2026-10-11'")
day_end = text.index("      id: 'day-11', number: 11, date: '2026-10-12'", day_start)
day = text[day_start:day_end]

area_marker = "      areaOptions: "
if area_marker not in day:
    raise SystemExit('Day 10 areaOptions marker missing')
area_options_and_after = day.split(area_marker, 1)[1]

metadata = """      id: 'day-10', number: 10, date: '2026-10-11',
      startBase: 'Abacus Hotel, Sesto San Giovanni',
      title: 'Milan → Monza → Cooking class → Milan',
      overviewPoint: 'Milan + Monza + cooking class',
      area: 'Milan / Monza',
      routeLabel: 'Abacus Hotel → M1 / Cordusio → Starbucks → Primark → Ferrari → M1 → Abacus Hotel → Autodromo Nazionale Monza → Abacus Hotel → M1 / San Babila → Viale Premuda 13 → Duomo / Galleria → M1 → Abacus Hotel',
      overnight: 'Abacus Hotel · Sesto San Giovanni · לילה 2 מתוך 2',
      drivingTime: 'Monza: כ־30–50 דקות לכל כיוון ביום אירוע · Milan בתחבורה ציבורית וברגל',
      walking: 'מרכז Milan + הליכה מהתחנות + Monza',
      highlights: ['Starbucks Reserve · 08:30', 'Primark + Ferrari', 'E4 Championship · 13:40', 'Italian GT Sprint GT3 · 14:50', 'Cooking class · 18:30 · הוזמן', 'Milan · ערב אחרון'],
      areaOptions: """
day = metadata + area_options_and_after

# Make the Milan options reflect the new priorities without making optional places mandatory.
day = day.replace(
    "description: 'סניף מרכזי ממש ליד Duomo, ולכן נוח במיוחד אם אנחנו כבר מסתובבים במרכז העיר.',\n          details: {\n            openingHours: 'סביב 10:30–19:30 · לבדוק שוב סמוך לטיול',",
    "description: 'שוקולד + גלידה ממש ליד Duomo. אופציה קלה אם נשאר זמן בבוקר או בערב, לא עצירה חובה.',\n          details: {\n            openingHours: 'א׳ מ־09:00 · לבדוק שוב סמוך לטיול',",
    1,
)
day = day.replace(
    "description: 'הסניף הרשמי שמצאתי שמתאים למסלול במרכז Milan.',\n          details: {\n            openingHours: 'סביב 10:00–19:30 · לבדוק שוב סמוך לטיול',",
    "description: 'אופציית שוקולד נוספת ב־Via Dante. לא בעדיפות בבוקר כי נפתח מאוחר יותר.',\n          details: {\n            openingHours: 'א׳ מ־10:30 · לבדוק שוב סמוך לטיול',",
    1,
)
day = day.replace(
    "description: 'חנות הדגל של Ferrari עם מרצ׳נדייז ותצוגות, כולל תצוגת רכב בסגנון Formula 1.',",
    "description: 'חנות הדגל של Ferrari עם מרצ׳נדייז ותצוגת F1. עצירה קצרה מתוכננת אחרי הפתיחה ב־10:00; זו חנות ולא מוזיאון.',",
    1,
)
day = day.replace(
    "description: 'סניף מרכזי גדול, נוח יחסית לאזור Duomo.',",
    "description: 'עצירת השופינג העיקרית של הבוקר. נפתח ב־09:00 ולכן נכנסים אחרי Starbucks.',",
    1,
)
day = day.replace(
    "description: 'הרוסטרי הגדול ב־Piazza Cordusio, במרחק הליכה קצר מ־Duomo.',",
    "description: 'עצירת הבוקר הקבועה ל־08:30: קפה / ארוחת בוקר קצרה לפני השופינג.',",
    1,
)

# Add Spùn Tiramisù as a flexible Milan option if it is not already present.
if "id: 'spun-tiramisu-duomo'" not in day:
    insert_before = """        {
          id: 'gelateria-umberto',
"""
    spun = """        {
          id: 'spun-tiramisu-duomo',
          name: 'Spùn Tiramisù – Duomo',
          category: 'Tiramisù / dessert / trendy food stop',
          description: 'טירמיסו to-go פופולרי במילאנו, מזוהה עם הקופסאות האדומות־לבנות. אופציה גמישה בלבד לבוקר אם נשאר זמן או לערב אחרי הסדנה.',
          details: {
            openingHours: 'א׳ 12:00–23:30 · לבדוק שוב סמוך לטיול',
            price: 'לפי הזמנה',
            address: 'Via Victor Hugo 3, 20123 Milano',
            notes: 'קרוב מאוד ל־Duomo. טעמים כוללים classic, pistachio, Nutella, hazelnut, salted caramel ועוד. לא עצירת חובה.',
          },
        },
"""
    if insert_before not in day:
        raise SystemExit('Spun insertion anchor missing')
    day = day.replace(insert_before, spun + insert_before, 1)

# Replace Day 10 alerts and stops, preserving the areaOptions above exactly except for the focused changes.
alerts_start = day.index("      alerts:")
stops_end = day.rfind("      ],\n    },\n    {")
if stops_end == -1:
    raise SystemExit('Day 10 closing anchor missing')
prefix = day[:alerts_start]
suffix = day[stops_end + len("      ],\n    },\n    {"):]

new_tail = """      alerts: [
        'לפי הלו״ז הזמני שאנחנו עובדים לפיו כרגע: E4 Championship ב־13:40 ו־Italian GT Sprint GT3 ב־14:50. הלו״ז הרשמי עדיין מוגדר provisional ולכן בודקים שוב סמוך לאירוע.',
        'הסדנה ב־18:30 הוזמנה. צריך להיות ב־Viale Premuda 13 עד 18:15; מכוונים להגיע סביב 18:00–18:10 כדי להשאיר buffer לעיכוב קטן ביציאה מ־Monza.',
        'לא נוסעים עם הרכב למרכז Milan: משאירים אותו ב־garage של Abacus Hotel ונוסעים ב־M1. Day 10 evening נשאר גמיש כי ייתכן שכבר נגיע למרכז גם בערב 10.10.',
      ],
      stops: [
        place({ id: 'abacus-hotel-day10-start', type: 'hotel', name: 'Abacus Hotel', time: '≈07:50–08:00', status: 'booked', coordinates: coords.abacusHotel, details: { address: 'Via Monte Grappa 39, 20099 Sesto San Giovanni MI, Italy', parking: 'Garage כלול בהזמנה', notes: 'יוצאים ברגל כ־4 דקות ל־Sesto 1° Maggio FS. הרכב נשאר במלון.' } }),
        transfer('metro-sesto-cordusio-morning', 'Sesto 1° Maggio FS → Cordusio', 'כ־25–30 דקות', '≈08:00–08:30', { notes: 'M1 ישיר. יורדים ב־Cordusio, ממש ליד Starbucks Reserve Roastery.' }),
        place({ id: 'starbucks-roastery-morning', type: 'activity', name: 'Starbucks Reserve Roastery Milano', time: '08:30–09:00', duration: 'כ־30 דקות', status: 'planned', coordinates: coords.starbucksRoastery, details: { openingHours: 'א׳ 07:30–22:30', address: 'Piazza Cordusio 1, 20123 Milano', notes: 'קפה / ארוחת בוקר קצרה. נקודת הפתיחה הקבועה של הבוקר.' } }),
        transfer('walk-starbucks-primark', 'Starbucks Reserve Roastery → Primark Milano – Via Torino', 'כ־7–10 דקות ברגל', '≈09:00'),
        place({ id: 'primark-morning', type: 'activity', name: 'Primark Milano – Via Torino', time: '≈09:10–09:55', duration: 'כ־45 דקות · גמיש', status: 'planned', coordinates: coords.primarkTorino, details: { openingHours: 'א׳ 09:00–22:00', address: 'Via Torino 45, 20123 Milano', notes: 'עצירת השופינג העיקרית של הבוקר. אם אנחנו מסיימים מהר — ממשיכים הלאה ולא מושכים זמן בכוח.' } }),
        transfer('walk-primark-ferrari', 'Primark Milano – Via Torino → Ferrari Flagship Store Milano', 'כ־8–10 דקות ברגל', '≈09:55–10:05'),
        place({ id: 'ferrari-store-morning', type: 'activity', name: 'Ferrari Flagship Store Milano', time: '≈10:05–10:30', duration: 'כ־20–25 דקות', status: 'planned', coordinates: coords.ferrariMilano, details: { openingHours: 'א׳ 10:00–20:00', address: 'Via Berchet 2, 20121 Milano', notes: 'עצירה קצרה בחנות הדגל עם תצוגת F1. זו חנות, לא מוזיאון.' } }),
        place({ id: 'milan-morning-flex', type: 'activity', name: 'Milan · חלון גמיש לפני החזרה למלון', time: '≈10:30–10:50', duration: 'עד כ־20 דקות', status: 'optional', coordinates: coords.milan, details: { notes: 'רק אם הזמן זורם: Venchi Mengoni או משהו ממש קרוב. לא מנסים להספיק הכול; Lindt נשאר אופציה משנית כי נפתח רק ב־10:30.' } }),
        transfer('metro-milan-sesto-before-monza', 'Milan center → Sesto 1° Maggio FS → Abacus Hotel', 'כ־30–40 דקות', '≈10:50–11:35/11:45', { notes: 'חוזרים בזמן למלון כדי לקחת את הרכב בלי לחץ לפני Monza.' }),
        place({ id: 'abacus-car-pickup-monza', type: 'hotel', name: 'Abacus Hotel · לוקחים את הרכב', time: '≈11:45–12:10', status: 'booked', coordinates: coords.abacusHotel, details: { parking: 'Garage כלול בהזמנה', notes: 'התארגנות קצרה ויציאה ל־Autodromo. שומרים את ה־buffer שכבר תכננו לתנועת אירוע וחניה.' } }),
        drive('drive-abacus-monza', 'Abacus Hotel → Autodromo Nazionale Monza', 'כ־30–50 דקות ביום אירוע', '≈12:10–≈13:00', { notes: 'המלון נמצא כ־9 ק״מ מה־Autodromo. שומרים buffer לתנועת אירוע, חניה והליכה כדי לא להגיע בלחץ למרוץ של 13:40.' }),
        place({ id: 'monza-event', type: 'activity', name: 'ACI Racing Weekend 2 · Autodromo Nazionale Monza', time: '≈13:00–15:40', duration: 'שני המרוצים שבחרנו', status: 'planning', coordinates: coords.monza, details: { reservation: 'כרטיסים / חניה עדיין במעקב', notes: '13:40 · E4 Championship. 14:50 · Italian GT Sprint GT3. נשארים רק לשני המרוצים שמעניינים אותנו ולא לכל יום האירוע. התוכנית עדיין provisional ויש לבדוק שוב סמוך ל־11.10.', website: 'https://www.acisport.it/en/ACI-SPORT/home' } }),
        drive('drive-monza-abacus', 'Autodromo Nazionale Monza → Abacus Hotel', 'כ־30–50 דקות ביום אירוע', 'אחרי המרוץ השני · ≈15:40–16:30/16:45', { notes: 'לוקחים בחשבון יציאה מהחניון ותנועת אירוע. חוזרים למלון ומחזירים את הרכב ל־garage.' }),
        place({ id: 'abacus-before-cooking-class', type: 'hotel', name: 'Abacus Hotel · מחזירים את הרכב', time: '≈16:30–16:45', status: 'booked', coordinates: coords.abacusHotel, details: { parking: 'Garage כלול בהזמנה', notes: 'משאירים את הרכב, מתארגנים בקצרה ויוצאים שוב למטרו סביב 17:15–17:25.' } }),
        transfer('metro-sesto-cooking-class', 'Abacus Hotel → Sesto 1° Maggio FS → San Babila → Viale Premuda 13', 'כ־40–50 דקות כולל הליכה', '≈17:15–17:25 → ≈18:00–18:10', { notes: 'הליכה קצרה מהמלון לתחנה, M1 עד San Babila ואז הליכה ל־Viale Premuda 13. היעד הוא להגיע 18:00–18:10; חובה להיות בנקודת המפגש עד 18:15.' }),
        place({ id: 'cooking-class-milan', type: 'activity', name: 'Milano: Handmade Pasta & Iconic Dessert Making Class', time: '18:15 הגעה · 18:30–21:00', duration: '2.5 שעות', status: 'booked', coordinates: coords.cookingClassMilan, details: { reservation: 'BOOKED · 2 adults · English', address: 'Viale Premuda 13, 20129 Milano MI, Italy', notes: 'Provider: Cook & Walk Srl. מכינים fresh ravioli, fettuccine ו־classic tiramisu, ואז אוכלים את מה שהכנו עם local wine או soft drink. המתכונים נשלחים אחרי הסדנה. הפעילות מתחילה ומסתיימת באותה כתובת.' } }),
        transfer('walk-class-duomo', 'Viale Premuda 13 → San Babila → Corso Vittorio Emanuele II → Duomo / Galleria', 'כ־20–25 דקות ברגל', '21:00–≈21:25', { notes: 'הליכה רגועה לתוך המרכז אחרי הסדנה.' }),
        place({ id: 'milan-evening', type: 'activity', name: 'Milan · ערב אחרון', time: '≈21:25–לילה', duration: 'פתוח וגמיש', status: 'planned', coordinates: coords.milan, details: { notes: 'אין צורך במסעדה — אוכלים בסדנה. מסתובבים ב־Duomo / Galleria / מרכז Milan ומשלימים רק מה שמתחשק ומה שעוד פתוח. אופציות גמישות: Primark עד 22:00, Starbucks Reserve עד 22:30, Venchi Mengoni ו־Spùn Tiramisù – Duomo. שום דבר כאן לא חובה.' } }),
        transfer('metro-milan-sesto', 'Milan center → Sesto 1° Maggio FS', 'כ־25–30 דקות', 'בסוף הערב', { notes: 'חזרה ב־M1 ואז כ־4 דקות הליכה ל־Abacus Hotel.' }),
        place({ id: 'abacus-night2', type: 'hotel', name: 'Abacus Hotel · לילה 2 מתוך 2', time: 'לילה', status: 'booked', coordinates: coords.abacusHotel, details: { address: 'Via Monte Grappa 39, 20099 Sesto San Giovanni MI, Italy', parking: 'Garage כלול בהזמנה', openingHours: 'Check-out למחרת לפני 12:00' } }),
      ],
    },
    {
"""

day = prefix + new_tail + suffix
text = text[:day_start] + day + text[day_end:]

# 4) Add the class to the global reservations list exactly once.
reservation = "    { id: 'cooking-class-milan', name: 'Milano: Handmade Pasta & Iconic Dessert Making Class', category: 'Activity', date: '2026-10-11', status: 'booked' },\n"
if "id: 'cooking-class-milan'" not in text[text.index("  reservations: ["):]:
    anchor = "    { id: 'monza', name: 'Monza · tickets / parking', category: 'Activity', date: '2026-10-11', status: 'planning' },\n"
    if anchor not in text:
        raise SystemExit('Reservation insertion anchor missing')
    text = text.replace(anchor, anchor + reservation, 1)

path.write_text(text)
