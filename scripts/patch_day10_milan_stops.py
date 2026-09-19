from pathlib import Path
import re

path = Path('index.html')
text = path.read_text()

# Add map coordinates for the two newly mapped fixed stops.
anchor = "  spunDuomo: { lat: 45.4637229, lng: 9.1872327 },\n"
addition = (
    "  spunDuomo: { lat: 45.4637229, lng: 9.1872327 },\n"
    "  venchiMengoni: { lat: 45.465458, lng: 9.189050 },\n"
    "  gelateriaUmberto: { lat: 45.4618935, lng: 9.2065548 },\n"
)
if "venchiMengoni:" not in text:
    if anchor not in text:
        raise SystemExit('Spun coordinate anchor missing')
    text = text.replace(anchor, addition, 1)

# Replace only Day 10 map route.
map_start = text.index("  'day-10': {")
map_end = text.index("  'day-11': {", map_start)
new_map = """  'day-10': {
    points: [
      { name: 'Abacus Hotel · Sesto San Giovanni', label: '≈07:50–08:00 · יוצאים ל־M1', ...coords.abacusHotel },
      { name: 'Starbucks Reserve Roastery Milano', label: '08:30–09:00 · קפה / ארוחת בוקר קצרה', ...coords.starbucksRoastery },
      { name: 'Primark Milano – Via Torino', label: '≈09:10–09:50 · שופינג', ...coords.primarkTorino },
      { name: 'Spùn Tiramisù – Duomo', label: '≈10:00 · עצירת טירמיסו קצרה / אופציונלית', ...coords.spunDuomo },
      { name: 'Venchi Milano Mengoni', label: '≈10:10 · שוקולד / גלידה קצר / אופציונלי', ...coords.venchiMengoni },
      { name: 'Ferrari Flagship Store Milano', label: '≈10:20–10:40 · עצירת עדיפות', ...coords.ferrariMilano },
      { name: 'Abacus Hotel · Sesto San Giovanni', label: '≈11:35–11:45 · לוקחים את הרכב', ...coords.abacusHotel },
      { name: 'Autodromo Nazionale Monza', label: '13:40 E4 · 14:50 Italian GT Sprint GT3', ...coords.monza },
      { name: 'Abacus Hotel · Sesto San Giovanni', label: '≈16:30–16:45 · מחזירים את הרכב', ...coords.abacusHotel },
      { name: 'Milano: Handmade Pasta & Iconic Dessert Making Class', label: '18:15 הגעה · 18:30–21:00 · הוזמן', ...coords.cookingClassMilan },
      { name: 'Gelateria Umberto 1934 Milano', label: 'אחרי הסדנה · affogato אם עוד לא היינו בערב הקודם', ...coords.gelateriaUmberto },
      { name: 'Milan center · Duomo / Galleria', label: 'ערב אחרון · הליכה / שופינג / אווירה', ...coords.milan },
      { name: 'Abacus Hotel · Sesto San Giovanni', label: 'חזרה ב־M1 · לילה 2 מתוך 2', ...coords.abacusHotel },
    ],
    routePath: [coords.abacusHotel, coords.starbucksRoastery, coords.primarkTorino, coords.spunDuomo, coords.venchiMengoni, coords.ferrariMilano, coords.abacusHotel, coords.monza, coords.abacusHotel, coords.cookingClassMilan, coords.gelateriaUmberto, coords.milan, coords.abacusHotel],
    routeModes: ['TRANSIT', 'WALKING', 'WALKING', 'WALKING', 'WALKING', 'TRANSIT', 'DRIVING', 'DRIVING', 'TRANSIT', 'WALKING', 'WALKING', 'TRANSIT'],
  },
"""
text = text[:map_start] + new_map + text[map_end:]

# Day 10 metadata/hero: concise hierarchy only.
replacements = {
    "      title: 'Milan → Monza → Cooking class → Milan',": "      title: 'Milan (shopping) → Monza → Milan',",
    "      overviewPoint: 'Milan + Monza + cooking class',": "      overviewPoint: 'Milan shopping + Monza + cooking class',",
    "      routeLabel: 'Abacus Hotel → M1 / Cordusio → Starbucks → Primark → Ferrari → M1 → Abacus Hotel → Autodromo Nazionale Monza → Abacus Hotel → M1 / San Babila → Viale Premuda 13 → Duomo / Galleria → M1 → Abacus Hotel',": "      routeLabel: 'Morning shopping in Milan · Monza races · Cooking class · Final evening in Milan',",
    "      highlights: ['Starbucks Reserve · 08:30', 'Primark + Ferrari', 'E4 Championship · 13:40', 'Italian GT Sprint GT3 · 14:50', 'Cooking class · 18:30 · הוזמן', 'Milan · ערב אחרון'],": "      highlights: ['Milan · shopping', 'Monza · E4 + Italian GT Sprint GT3', 'Cooking class · 18:30 · הוזמן', 'Milan · ערב אחרון'],",
}
for old, new in replacements.items():
    if old not in text:
        raise SystemExit(f'Day 10 metadata anchor missing: {old}')
    text = text.replace(old, new, 1)

# Fixed-route stops no longer need duplicate cards in the Milan area-options section.
for option_id in [
    'venchi-mengoni',
    'ferrari-store-milan',
    'primark-via-torino',
    'starbucks-roastery',
    'spun-tiramisu-duomo',
    'gelateria-umberto',
]:
    pattern = re.compile(r"\n        \{\n          id: '" + re.escape(option_id) + r"',.*?\n        \},", re.S)
    text, count = pattern.subn('', text, count=1)
    if count != 1:
        raise SystemExit(f'Expected one area-option block for {option_id}, found {count}')

# Replace only the detailed Day 10 stop list.
day10_start = text.index("      id: 'day-10', number: 10, date: '2026-10-11'")
stops_start = text.index("      stops: [", day10_start)
day11_start = text.index("      id: 'day-11', number: 11, date: '2026-10-12'", stops_start)
stops_end = text.rfind("      ],\n    },\n    {", stops_start, day11_start)
if stops_end == -1:
    raise SystemExit('Could not locate Day 10 stops end')
stops_end += len("      ],\n    },\n    {")
new_stops = """      stops: [
        place({ id: 'abacus-hotel-day10-start', type: 'hotel', name: 'Abacus Hotel', time: '≈07:50–08:00', status: 'booked', coordinates: coords.abacusHotel, details: { address: 'Via Monte Grappa 39, 20099 Sesto San Giovanni MI, Italy', parking: 'Garage כלול בהזמנה', notes: 'יוצאים ברגל כ־4 דקות ל־Sesto 1° Maggio FS. הרכב נשאר במלון.' } }),
        transfer('metro-sesto-cordusio-morning', 'Sesto 1° Maggio FS → Cordusio', 'כ־25–30 דקות', '≈08:00–08:30', { notes: 'M1 ישיר. יורדים ב־Cordusio, ממש ליד Starbucks Reserve Roastery.' }),
        place({ id: 'starbucks-roastery-morning', type: 'activity', name: 'Starbucks Reserve Roastery Milano', time: '08:30–09:00', duration: 'כ־30 דקות', status: 'planned', coordinates: coords.starbucksRoastery, details: { openingHours: 'א׳ 07:30–22:30', address: 'Piazza Cordusio 1, 20123 Milano', notes: 'קפה / ארוחת בוקר קצרה. נקודת הפתיחה הקבועה של הבוקר.' } }),
        transfer('walk-starbucks-primark', 'Starbucks Reserve Roastery → Primark Milano – Via Torino', 'כ־7–10 דקות ברגל', '≈09:00'),
        place({ id: 'primark-morning', type: 'activity', name: 'Primark Milano – Via Torino', time: '≈09:10–09:50', duration: 'כ־40 דקות · גמיש', status: 'planned', coordinates: coords.primarkTorino, details: { openingHours: 'א׳ 09:00–22:00', address: 'Via Torino 45, 20123 Milano', notes: 'עצירת השופינג העיקרית של הבוקר. אם אנחנו מסיימים מהר — ממשיכים הלאה ולא מושכים זמן בכוח.' } }),
        place({ id: 'via-torino-shopping', type: 'activity', name: 'Via Torino · שופינג בדרך', time: '≈09:50–10:00', duration: 'כ־10 דקות · תוך כדי ההליכה', status: 'planned', details: { notes: 'לא עצירה נפרדת ארוכה — פשוט מסתכלים בחנויות שמעניינות אותנו בדרך חזרה לכיוון Duomo.' } }),
        transfer('walk-via-torino-spun', 'Via Torino → Spùn Tiramisù – Duomo', 'כ־5–7 דקות ברגל', '≈10:00'),
        place({ id: 'spun-tiramisu-morning', type: 'activity', name: 'Spùn Tiramisù – Duomo', time: '≈10:00–10:08', duration: 'כ־5–10 דקות', status: 'optional', coordinates: coords.spunDuomo, details: { openingHours: 'האתר הרשמי מציג פתיחה ב־10:00 · לבדוק שוב סמוך לטיול', address: 'Via Victor Hugo 3, 20123 Milano', notes: 'עצירת tiramisu-to-go קצרה עם הקופסאות האדומות־לבנות. אופציונלי ומהיר — לא נותנים לזה לעכב את Ferrari.' } }),
        transfer('walk-spun-venchi', 'Spùn Tiramisù – Duomo → Venchi Milano Mengoni', 'כ־3–5 דקות ברגל', '≈10:08'),
        place({ id: 'venchi-mengoni-morning', type: 'activity', name: 'Venchi Milano Mengoni', time: '≈10:10–10:18', duration: 'כ־5–10 דקות', status: 'optional', coordinates: coords.venchiMengoni, details: { address: 'Via Giuseppe Mengoni 1, 20121 Milano', notes: 'שוקולד / גלידה ממש ליד Duomo. עצירה קצרה ואופציונלית בלבד; Ferrari נשאר בעדיפות.' } }),
        transfer('walk-venchi-ferrari', 'Venchi Milano Mengoni → Ferrari Flagship Store Milano', 'כ־3–5 דקות ברגל', '≈10:18'),
        place({ id: 'ferrari-store-morning', type: 'activity', name: 'Ferrari Flagship Store Milano', time: '≈10:20–10:40', duration: 'כ־20 דקות', status: 'planned', coordinates: coords.ferrariMilano, details: { openingHours: 'א׳ 10:00–20:00', address: 'Via Berchet 2, 20121 Milano', notes: 'אחת משלוש עצירות העדיפות של הבוקר. חנות הדגל עם תצוגת F1 — לא מוזיאון.' } }),
        transfer('metro-milan-sesto-before-monza', 'Milan center → Sesto 1° Maggio FS → Abacus Hotel', 'כ־30–40 דקות', '≈10:50–11:35/11:45', { notes: 'אחרי Ferrari ממשיכים לתחנת M1 הקרובה וחוזרים בזמן למלון כדי לקחת את הרכב בלי לחץ לפני Monza.' }),
        place({ id: 'abacus-car-pickup-monza', type: 'hotel', name: 'Abacus Hotel · לוקחים את הרכב', time: '≈11:45–12:10', status: 'booked', coordinates: coords.abacusHotel, details: { parking: 'Garage כלול בהזמנה', notes: 'התארגנות קצרה ויציאה ל־Autodromo. שומרים את ה־buffer שכבר תכננו לתנועת אירוע וחניה.' } }),
        drive('drive-abacus-monza', 'Abacus Hotel → Autodromo Nazionale Monza', 'כ־30–50 דקות ביום אירוע', '≈12:10–≈13:00', { notes: 'המלון נמצא כ־9 ק״מ מה־Autodromo. שומרים buffer לתנועת אירוע, חניה והליכה כדי לא להגיע בלחץ למרוץ של 13:40.' }),
        place({ id: 'monza-event', type: 'activity', name: 'ACI Racing Weekend 2 · Autodromo Nazionale Monza', time: '≈13:00–15:40', duration: 'שני המרוצים שבחרנו', status: 'planning', coordinates: coords.monza, details: { reservation: 'כרטיסים / חניה עדיין במעקב', notes: '13:40 · E4 Championship. 14:50 · Italian GT Sprint GT3. נשארים רק לשני המרוצים שמעניינים אותנו ולא לכל יום האירוע. התוכנית עדיין provisional ויש לבדוק שוב סמוך ל־11.10.', website: 'https://www.acisport.it/en/ACI-SPORT/home' } }),
        drive('drive-monza-abacus', 'Autodromo Nazionale Monza → Abacus Hotel', 'כ־30–50 דקות ביום אירוע', 'אחרי המרוץ השני · ≈15:40–16:30/16:45', { notes: 'לוקחים בחשבון יציאה מהחניון ותנועת אירוע. חוזרים למלון ומחזירים את הרכב ל־garage.' }),
        place({ id: 'abacus-before-cooking-class', type: 'hotel', name: 'Abacus Hotel · מחזירים את הרכב', time: '≈16:30–16:45', status: 'booked', coordinates: coords.abacusHotel, details: { parking: 'Garage כלול בהזמנה', notes: 'משאירים את הרכב, מתארגנים בקצרה ויוצאים שוב למטרו סביב 17:15–17:25.' } }),
        transfer('metro-sesto-cooking-class', 'Abacus Hotel → Sesto 1° Maggio FS → San Babila → Viale Premuda 13', 'כ־40–50 דקות כולל הליכה', '≈17:15–17:25 → ≈18:00–18:10', { notes: 'הליכה קצרה מהמלון לתחנה, M1 עד San Babila ואז הליכה ל־Viale Premuda 13. היעד הוא להגיע 18:00–18:10; חובה להיות בנקודת המפגש עד 18:15.' }),
        place({ id: 'cooking-class-milan', type: 'activity', name: 'Milano: Handmade Pasta & Iconic Dessert Making Class', time: '18:15 הגעה · 18:30–21:00', duration: '2.5 שעות', status: 'booked', coordinates: coords.cookingClassMilan, details: { reservation: 'BOOKED · 2 adults · English', address: 'Viale Premuda 13, 20129 Milano MI, Italy', notes: 'Provider: Cook & Walk Srl. מכינים fresh ravioli, fettuccine ו־classic tiramisu, ואז אוכלים את מה שהכנו עם local wine או soft drink. המתכונים נשלחים אחרי הסדנה. הפעילות מתחילה ומסתיימת באותה כתובת.' } }),
        transfer('walk-class-umberto', 'Viale Premuda 13 → Gelateria Umberto 1934 Milano', 'כ־5–8 דקות ברגל', '21:00–≈21:08'),
        place({ id: 'gelateria-umberto-evening', type: 'activity', name: 'Gelateria Umberto 1934 Milano', time: '≈21:08–21:20', duration: 'עצירת affogato קצרה', status: 'optional', coordinates: coords.gelateriaUmberto, details: { openingHours: 'א׳ 12:00–23:00 לפי האתר הרשמי · לבדוק שוב סמוך לטיול', address: 'Piazza Cinque Giornate 4, 20129 Milano MI, Italy', notes: 'affogato — אם עוד לא היינו כאן בערב הקודם. המטרה היא רק שלא נשכח; אם כבר ביקרנו ב־10.10, מדלגים וממשיכים למרכז.' } }),
        transfer('walk-umberto-duomo', 'Gelateria Umberto 1934 → San Babila → Corso Vittorio Emanuele II → Duomo / Galleria', 'כ־20–25 דקות ברגל', '≈21:20–21:45', { notes: 'ממשיכים ברגל לתוך המרכז אחרי האפוגטו.' }),
        place({ id: 'milan-evening', type: 'activity', name: 'Milan · ערב אחרון', time: '≈21:45–לילה', duration: 'פתוח וגמיש', status: 'planned', coordinates: coords.milan, details: { notes: 'אין צורך במסעדה — אוכלים בסדנה. ממשיכים לטייל ב־Duomo / Galleria / מרכז Milan, שופינג אם משהו עוד פתוח, וקצת אווירה של העיר בלי לדחוס עוד אטרקציות.' } }),
        transfer('metro-milan-sesto', 'Milan center → Sesto 1° Maggio FS', 'כ־25–30 דקות', 'בסוף הערב', { notes: 'חזרה ב־M1 ואז כ־4 דקות הליכה ל־Abacus Hotel.' }),
        place({ id: 'abacus-night2', type: 'hotel', name: 'Abacus Hotel · לילה 2 מתוך 2', time: 'לילה', status: 'booked', coordinates: coords.abacusHotel, details: { address: 'Via Monte Grappa 39, 20099 Sesto San Giovanni MI, Italy', parking: 'Garage כלול בהזמנה', openingHours: 'Check-out למחרת לפני 12:00' } }),
      ],
    },
    {
"""
text = text[:stops_start] + new_stops + text[stops_end:]

path.write_text(text)
