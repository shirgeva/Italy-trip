from pathlib import Path

path = Path('index.html')
text = path.read_text()

# Update ONLY the October 11 daily map.
map_start = text.index("  'day-10': {")
map_end = text.index("  'day-11': {", map_start)
new_map = """  'day-10': {
    points: [
      { name: 'Abacus Hotel · Sesto San Giovanni', label: 'בוקר · יוצאים ל־M1', ...coords.abacusHotel },
      { name: 'Milan center · Duomo / Brera', label: '≈09:00–11:15 · אוכל / קפה / שופינג / טיול קל', ...coords.milan },
      { name: 'Abacus Hotel · Sesto San Giovanni', label: '≈12:00 · חוזרים ולוקחים את הרכב', ...coords.abacusHotel },
      { name: 'Autodromo Nazionale Monza', label: '13:40 E4 · 14:50 GT Cup', ...coords.monza },
      { name: 'Abacus Hotel · Sesto San Giovanni', label: 'אחרי המרוצים · מחזירים את הרכב ל־garage', ...coords.abacusHotel },
      { name: 'Milan center · Duomo / Brera', label: 'ערב אחרון · אוכל / שופינג / אווירה', ...coords.milan },
      { name: 'Abacus Hotel · Sesto San Giovanni', label: 'חזרה מאוחרת · לילה 2 מתוך 2', ...coords.abacusHotel },
    ],
    routePath: [coords.abacusHotel, coords.milan, coords.abacusHotel, coords.monza, coords.abacusHotel, coords.milan, coords.abacusHotel],
    routeModes: ['TRANSIT', 'TRANSIT', 'DRIVING', 'DRIVING', 'TRANSIT', 'TRANSIT'],
  },
"""
text = text[:map_start] + new_map + text[map_end:]

# Update ONLY Day 10 itinerary content.
day_start = text.index("      id: 'day-10', number: 10, date: '2026-10-11'")
day_end = text.index("      id: 'day-11', number: 11, date: '2026-10-12'", day_start)

old_prefix = text[day_start:day_end]

new_day = """      id: 'day-10', number: 10, date: '2026-10-11',
      startBase: 'Abacus Hotel, Sesto San Giovanni',
      title: 'Milan → Monza → Milan',
      overviewPoint: 'Milan + שני המרוצים שבחרנו ב־Monza',
      area: 'Milan / Monza',
      routeLabel: 'Abacus Hotel → M1 → Milan center → M1 → Abacus Hotel → Autodromo Nazionale Monza → Abacus Hotel → M1 → Milan center → M1 → Abacus Hotel',
      overnight: 'Abacus Hotel · Sesto San Giovanni · לילה 2 מתוך 2',
      drivingTime: 'Monza: כ־30–50 דקות לכל כיוון ביום אירוע · Milan במטרו M1 בבוקר ובערב',
      walking: 'מרכז Milan + הליכה במסלול / חניה ב־Monza',
      highlights: ['Milan · בוקר רגוע', 'E4 Championship · 13:40', 'C.I. Gran Turismo Sprint GT Cup · 14:50', 'Milan · ערב אחרון'],
      areaOptions: """ + old_prefix.split("      areaOptions: ",1)[1].split("      alerts:",1)[0].rstrip() + """
      alerts: [
        'לפי הלו״ז הזמני שאנחנו עובדים לפיו כרגע: E4 Championship ב־13:40 ו־C.I. Gran Turismo Sprint GT Cup ב־14:50. הלו״ז הרשמי עדיין מוגדר provisional ולכן בודקים שוב סמוך לאירוע.',
        'לא נוסעים עם הרכב למרכז Milan: בבוקר ובערב משאירים אותו ב־garage של Abacus Hotel ונוסעים ב־M1 מ־Sesto 1° Maggio FS.',
      ],
      stops: [
        place({ id: 'abacus-hotel-day10-start', type: 'hotel', name: 'Abacus Hotel', time: '≈08:30', status: 'booked', coordinates: coords.abacusHotel, details: { address: 'Via Monte Grappa 39, 20099 Sesto San Giovanni MI, Italy', parking: 'Garage כלול בהזמנה', notes: 'משאירים את הרכב במלון ויוצאים ברגל ל־Sesto 1° Maggio FS.' } }),
        transfer('metro-sesto-milan-morning', 'Abacus Hotel → Sesto 1° Maggio FS → Milan center / Duomo', 'כ־30–35 דקות כולל ההליכה לתחנה', '≈08:30–09:05', { notes: 'כ־4 דקות הליכה מהמלון לתחנה ואז M1 ישיר לכיוון מרכז Milan.' }),
        place({ id: 'milan-morning', type: 'activity', name: 'Milan · בוקר רגוע במרכז', time: '≈09:00–11:15', duration: 'כ־2 שעות', status: 'planned', coordinates: coords.milan, details: { notes: 'בוקר קליל של אוכל / קפה, Duomo ו־Galleria מבחוץ או בקצרה, וקצת שופינג כשהחנויות נפתחות. לא דוחסים אטרקציות.' } }),
        transfer('metro-milan-sesto-before-monza', 'Milan center → Sesto 1° Maggio FS → Abacus Hotel', 'כ־30–35 דקות', '≈11:15–12:00', { notes: 'חוזרים למלון כדי לקחת את הרכב לפני Monza.' }),
        place({ id: 'abacus-car-pickup-monza', type: 'hotel', name: 'Abacus Hotel · לוקחים את הרכב', time: '≈12:00–12:10', status: 'booked', coordinates: coords.abacusHotel, details: { parking: 'Garage כלול בהזמנה', notes: 'יציאה ל־Autodromo עם buffer לחניה ולהליכה לכניסה.' } }),
        drive('drive-abacus-monza', 'Abacus Hotel → Autodromo Nazionale Monza', 'כ־30–50 דקות ביום אירוע', '≈12:10–≈13:00', { notes: 'המלון נמצא כ־9 ק״מ מה־Autodromo. שומרים buffer לתנועת אירוע, חניה והליכה כדי לא להגיע בלחץ למרוץ של 13:40.' }),
        place({ id: 'monza-event', type: 'activity', name: 'ACI Racing Weekend 2 · Autodromo Nazionale Monza', time: '≈13:00–15:40', duration: 'שני המרוצים שבחרנו', status: 'planning', coordinates: coords.monza, details: { reservation: 'כרטיסים / חניה עדיין במעקב', notes: '13:40 · E4 Championship. 14:50 · C.I. Gran Turismo Sprint GT Cup. נשארים רק לשני המרוצים שמעניינים אותנו ולא לכל יום האירוע. התוכנית עדיין provisional ויש לבדוק שוב סמוך ל־11.10.', website: 'https://www.acisport.it/en/ACI-SPORT/home' } }),
        drive('drive-monza-abacus', 'Autodromo Nazionale Monza → Abacus Hotel', 'כ־30–50 דקות ביום אירוע', 'אחרי המרוץ השני · ≈15:40–16:30/16:45', { notes: 'לוקחים בחשבון גם יציאה מהחניון ותנועת סוף אירוע. חוזרים למלון ומחזירים את הרכב ל־garage.' }),
        place({ id: 'abacus-before-milan', type: 'hotel', name: 'Abacus Hotel · מחזירים את הרכב', time: '≈16:30–17:00', status: 'booked', coordinates: coords.abacusHotel, details: { parking: 'Garage כלול בהזמנה', notes: 'מכאן ממשיכים שוב למרכז Milan בלי הרכב.' } }),
        transfer('metro-sesto-milan-evening', 'Sesto 1° Maggio FS → Milan center / Duomo', 'כ־25–30 דקות', '≈17:00–17:30', { notes: 'M1 ישיר למרכז.' }),
        place({ id: 'milan-evening', type: 'activity', name: 'Milan · ערב אחרון', time: '≈17:30–לילה', duration: 'פתוח וגמיש', status: 'planned', coordinates: coords.milan, details: { notes: 'הערב האחרון של הטיול נשאר באיזי: אוכל טוב, שופינג, Duomo / Galleria / Brera לפי החשק וקצת אווירה של העיר. לא בונים מרוץ אטרקציות.' } }),
        transfer('metro-milan-sesto', 'Milan center → Sesto 1° Maggio FS', 'בסוף הערב', 'לפי הקצב', { notes: 'חזרה ב־M1 ואז כ־4 דקות הליכה ל־Abacus Hotel.' }),
        place({ id: 'abacus-night2', type: 'hotel', name: 'Abacus Hotel · לילה 2 מתוך 2', time: 'לילה', status: 'booked', coordinates: coords.abacusHotel, details: { address: 'Via Monte Grappa 39, 20099 Sesto San Giovanni MI, Italy', parking: 'Garage כלול בהזמנה', openingHours: 'Check-out למחרת לפני 12:00' } }),
      ],
    },
    {
"""

# Keep the original opening indentation/structure by replacing only the Day 10 slice.
text = text[:day_start] + new_day + text[day_end:]

path.write_text(text)
