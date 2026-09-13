from pathlib import Path

p = Path('index.html')
s = p.read_text()

if "id: 'abacus-hotel-day9'" in s:
    raise SystemExit(0)

# Verified hotel coordinates where the current site needed corrections/additions.
s = s.replace("  postResidence: { lat: 46.732206, lng: 12.282275 },", "  postResidence: { lat: 46.732145, lng: 12.282422 },", 1)
s = s.replace("  dolomitiExclusive: { lat: 46.42775, lng: 11.68278 },", "  dolomitiExclusive: { lat: 46.427757, lng: 11.682810 },", 1)
coord_anchor = "  sesto: { lat: 45.5345, lng: 9.2302 },"
if coord_anchor not in s:
    raise SystemExit('Sesto coordinate anchor missing')
s = s.replace(coord_anchor, coord_anchor + "\n  abacusHotel: { lat: 45.5417357, lng: 9.2368135 },", 1)

# Day maps 9-11: replace generic Sesto hotel with confirmed Abacus Hotel.
map_start = s.index("  'day-9': {")
map_end = s.index("}\n\nconst trip = {", map_start)
old_maps = s[map_start:map_end]
new_maps = """  'day-9': {
    points: [
      { name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', label: '10.10 · צ׳ק־אאוט ויציאה לצפון Lake Garda', ...coords.dolomitiExclusive },
      { name: 'Parco Grotta Cascata Varone', label: 'כ־1:50–2:05 שעות · יעד הגעה ≈09:00', ...coords.varone },
      { name: 'Riva del Garda', label: 'חניה + שמירת מזוודות · טיול בעיירה', ...coords.riva },
      { name: 'Limone sul Garda', label: 'הגעה בשייט או באוטובוס · עדיין בתכנון', ...coords.limone },
      { name: 'Abacus Hotel · Sesto San Giovanni', label: 'לילה 1 מתוך 2 · הוזמן', ...coords.abacusHotel },
    ],
    routePath: [coords.dolomitiExclusive, coords.varone, coords.riva, coords.limone, coords.riva, coords.abacusHotel],
  },
  'day-10': {
    points: [
      { name: 'Abacus Hotel · Sesto San Giovanni', label: 'בסיס לינה · garage included', ...coords.abacusHotel },
      { name: 'Autodromo Nazionale Monza', label: 'שעות ייקבעו אחרי פרסום לו״ז המרוצים', ...coords.monza },
      { name: 'Abacus Hotel · Sesto San Giovanni', label: 'חזרה אחרי Monza · משאירים את הרכב', ...coords.abacusHotel },
      { name: 'Milan center · Duomo / Brera', label: 'ערב · M1 מ־Sesto 1° Maggio FS', ...coords.milan },
    ],
    routePath: [coords.abacusHotel, coords.monza, coords.abacusHotel, coords.milan, coords.abacusHotel],
  },
  'day-11': {
    points: [
      { name: 'Abacus Hotel · Sesto San Giovanni', label: 'יציאה משוערת 08:30–09:00', ...coords.abacusHotel },
      { name: 'Milan Malpensa Airport · Terminal 1', label: 'כ־40–50 דק׳ + buffer · החזרת רכב + טיסה 13:05', ...coords.malpensa },
    ],
    routePath: [coords.abacusHotel, coords.malpensa],
  },
"""
s = s[:map_start] + new_maps + s[map_end:]

# Global route: all accommodation is now confirmed; use the exact final Sesto hotel point.
s = s.replace(
    "  routeSummary: 'Milan Malpensa → Bellano / Ca’ del Lasco → Bressanone / ecHo Apartments & SPA → Alpe di Siusi / Val Gardena → San Candido / Post Residence → Pozza di Fassa / DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → QC Terme Dolomiti → Varone Waterfall → Riva del Garda → Limone sul Garda → Milan / Sesto San Giovanni → Monza → Milan Malpensa',",
    "  routeSummary: 'Milan Malpensa → Bellano / Ca’ del Lasco → Bressanone / ecHo Apartments & SPA → Alpe di Siusi / Val Gardena → San Candido / Post Residence → Pozza di Fassa / DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → QC Terme Dolomiti → Varone Waterfall → Riva del Garda → Limone sul Garda → Abacus Hotel / Sesto San Giovanni → Monza → Milan → Abacus Hotel → Milan Malpensa',",
    1,
)
s = s.replace("    coords.sesto,\n    coords.monza,\n    coords.sesto,\n    coords.malpensa,", "    coords.abacusHotel,\n    coords.monza,\n    coords.abacusHotel,\n    coords.malpensa,", 1)

# Ca' del Lasco: operational online check-in note only; no private codes.
old_ca = "place({ id: 'ca-del-lasco-day1', type: 'hotel', name: 'Ca’ del Lasco – Tulipano', time: 'הגעה משוערת 16:30–17:15', status: 'booked', coordinates: coords.caDelLasco, details: { address: 'Via per Taceno 19, 23822 Bellano (LC), Italy', parking: 'חניה פרטית חינם במקום', openingHours: 'Self check-in · check-in 16:00–21:00 · check-out עד 10:00', notes: 'הוזמן ל־2 לילות, 2–4.10.2026. Bellano-Tartavalle Terme נמצאת כ־300 מ׳ / כ־4–5 דקות הליכה. סופרמרקטים ושירותים בסיסיים נמצאים במרחק הליכה.' } })"
new_ca = "place({ id: 'ca-del-lasco-day1', type: 'hotel', name: 'Ca’ del Lasco – Tulipano', time: 'הגעה משוערת 16:30–17:15', status: 'booked', coordinates: coords.caDelLasco, details: { address: 'Via per Taceno 19, 23822 Bellano (LC), Italy', parking: 'חניה פרטית חינם במקום', openingHours: 'Check-in 16:00–21:00 · check-out עד 10:00', notes: 'הוזמן ל־2 לילות, 2–4.10.2026 · Tulipano – Romantic apartment with private dehor. הצ׳ק־אין מתבצע אונליין וחובה להשלים אותו לפני ההגעה, כולל זיהוי אורחים ותשלום מס תיירות. אין אפשרות לצ׳ק־אין אחרי 21:00. ההגעה המתוכננת 16:30–17:15 נמצאת בבטחה בתוך החלון. Bellano-Tartavalle Terme כ־300 מ׳ / 4–5 דקות הליכה.' } })"
if old_ca not in s:
    raise SystemExit('Ca del Lasco card anchor missing')
s = s.replace(old_ca, new_ca, 1)

# ecHo: confirmed booking, official address formatting, no false 19:00 deadline.
s = s.replace("'ecHo Apartments & SPA: check-in 14:00–19:00. ההגעה המתוכננת סביב 16:50–17:00 משאירה מרווח טוב לפני סגירת הצ׳ק־אין.'", "'ecHo Apartments & SPA: הוזמן. Check-in החל מ־14:00 עם digital/contactless access; check-out עד 10:00. אין באישור מגבלת 19:00 קשיחה.'", 1)
old_echo_day3 = "place({ id: 'echo-bressanone-day3', type: 'hotel', name: 'ecHo Apartments & SPA', time: '≈16:50–17:00', status: 'planning', coordinates: coords.echoBressanone, details: { address: 'Via Millan 14a, 39042 Bressanone (BZ), Italy', parking: 'חניה פרטית חינם במקום', openingHours: 'Check-in 14:00–19:00 · check-out עד 10:00', notes: 'לינה נבחרת / מתוכננת ל־4–6.10, 2 לילות. דירה עם מטבח; private / self check-in זמין. עדיין לא מסומן כהוזמן.' } })"
new_echo_day3 = "place({ id: 'echo-bressanone-day3', type: 'hotel', name: 'ecHo Apartments & SPA', time: '≈16:50–17:00', status: 'booked', coordinates: coords.echoBressanone, details: { address: 'Via Millan 14/A, 39042 Bressanone (BZ), Italy', parking: 'חניה פרטית חינם · monitored · uncovered', openingHours: 'Check-in החל מ־14:00 · digital/contactless access · check-out עד 10:00', notes: 'הוזמן ל־4–6.10, 2 לילות · Junior Suite - Rust · מטבח ו־Wi-Fi כלולים. Insured100% rate: ההחזר כפוף לאירועים מכוסים ומתועדים לפי תנאי הביטוח; לא מדובר ב־free cancellation. תזכורת פרטית: לוודא ששני הנוסעים רשומים בביטוח.' } })"
if old_echo_day3 not in s:
    raise SystemExit('ecHo day3 anchor missing')
s = s.replace(old_echo_day3, new_echo_day3, 1)
s = s.replace("place({ id: 'echo-bressanone-night2', type: 'hotel', name: 'ecHo Apartments & SPA · לילה 2 מתוך 2', time: 'ערב', status: 'planning', coordinates: coords.echoBressanone, details: { address: 'Via Millan 14a, 39042 Bressanone (BZ), Italy', parking: 'חניה פרטית חינם במקום', notes: 'לילה שני ואחרון; check-out למחרת עד 10:00, אבל התכנון הוא לצאת מוקדם.' } })",
              "place({ id: 'echo-bressanone-night2', type: 'hotel', name: 'ecHo Apartments & SPA · לילה 2 מתוך 2', time: 'ערב', status: 'booked', coordinates: coords.echoBressanone, details: { address: 'Via Millan 14/A, 39042 Bressanone (BZ), Italy', parking: 'חניה פרטית חינם · monitored · uncovered', openingHours: 'Check-out עד 10:00', notes: 'לילה שני ואחרון; התכנון הוא לצאת מוקדם.' } })", 1)
s = s.replace("status: 'planning', coordinates: coords.echoBressanone, details: { openingHours: 'Check-out עד 10:00', address: 'Via Millan 14a, 39042 Bressanone (BZ), Italy'", "status: 'booked', coordinates: coords.echoBressanone, details: { openingHours: 'Check-out עד 10:00', address: 'Via Millan 14/A, 39042 Bressanone (BZ), Italy'", 1)

# Post Residence: confirmed address/parking/status + early-arrival and cancellation notes.
old_post_day5 = "place({ id: 'post-residence-day5', type: 'hotel', name: 'Post Residence - Home of Memories - Dolomites', time: 'הגעה משוערת ≈13:30–14:15', status: 'planning', coordinates: coords.postResidence, details: { address: 'Benediktinerstraße 10c, 39038 San Candido, Italy', parking: 'Private parking available on site', notes: 'לינה נבחרת / מתוכננת ל־6–8.10, 2 לילות. Booking מציג את הכתובת Benediktinerstraße 10c; אתרי התיירות הרשמיים של האזור מציגים את אותו Post Residence גם כ־Piazza del Magistrato 5. המלון נמצא במרכז San Candido.' } })"
new_post_day5 = "place({ id: 'post-residence-day5', type: 'hotel', name: 'Post Residence - Home of Memories - Dolomites', time: 'הגעה משוערת ≈13:30–14:15', status: 'booked', coordinates: coords.postResidence, details: { address: 'Via dei Benedettini 11/C, 39038 Innichen / S. Candido, Italy', parking: 'חניה פרטית מוזמנת · €10 ליום', openingHours: 'Check-in 15:00–23:00 · check-out 07:30–10:00', notes: 'הוזמן ל־6–8.10, 2 לילות · Apartment Love. אם נגיע לפני 15:00, נבדוק אפשרות להשאיר רכב / מזוודות במלון ובינתיים נאכל או נסתובב מעט ב־San Candido; שמירה מוקדמת אינה מובטחת. ביטול: עד 15 ימים לפני ההגעה ללא עמלת ביטול נוספת; בתוך 14 ימים 100% חיוב. ל־6.10: 21.9 הוא בערך היום האחרון מחוץ לחלון הקנס, ומ־22.9 חל חיוב 100%; אין בכך קביעה לגבי החזר של תשלום שכבר בוצע.' } })"
if old_post_day5 not in s:
    raise SystemExit('Post day5 anchor missing')
s = s.replace(old_post_day5, new_post_day5, 1)
s = s.replace("place({ id: 'post-parking-before-funbob', type: 'hotel', name: 'Post Residence · חניה והפסקה קצרה', time: '≈14:35–14:50', duration: 'קצר', status: 'planning', coordinates: coords.postResidence, details: { notes: 'Haunold / Monte Baranci נמצא בערך 5 דקות הליכה מה־Post Residence, ולכן אין צורך להזיז שוב את הרכב.' } })",
              "place({ id: 'post-parking-before-funbob', type: 'hotel', name: 'Post Residence · חניה והפסקה קצרה', time: '≈14:35–14:50', duration: 'קצר', status: 'booked', coordinates: coords.postResidence, details: { parking: 'חניה פרטית מוזמנת · €10 ליום', notes: 'Haunold / Monte Baranci נמצא בערך 5 דקות הליכה מה־Post Residence, ולכן אין צורך להזיז שוב את הרכב.' } })", 1)
s = s.replace("place({ id: 'post-residence-night2', type: 'hotel', name: 'Post Residence - Home of Memories - Dolomites · לילה 2 מתוך 2', time: 'ערב', status: 'planning', coordinates: coords.postResidence, details: { address: 'Benediktinerstraße 10c, 39038 San Candido, Italy', notes: 'לילה שני ואחרון ב־San Candido.' } })",
              "place({ id: 'post-residence-night2', type: 'hotel', name: 'Post Residence - Home of Memories - Dolomites · לילה 2 מתוך 2', time: 'ערב', status: 'booked', coordinates: coords.postResidence, details: { address: 'Via dei Benedettini 11/C, 39038 Innichen / S. Candido, Italy', parking: 'חניה פרטית מוזמנת · €10 ליום', openingHours: 'Check-out 07:30–10:00', notes: 'לילה שני ואחרון ב־San Candido.' } })", 1)

# Dolomiti Exclusive: confirmed address/unit/board/status/cancellation. Keep prior check-in window.
s = s.replace("Strada Dolomites 55 A, 38036 Pozza di Fassa, Italy", "Strada Dolomites 55/A int.1, 38036 Sèn Jan di Fassa (TN), Italy")
s = s.replace("address: 'Strada Dolomites 55/A int.1, 38036 Sèn Jan di Fassa (TN), Italy', parking: 'חניה פרטית חינם במקום', openingHours: 'Check-in כרגע מופיע 15:00–21:30 · check-out עד 10:00', notes: 'הוזמן ל־8–10.10, 2 לילות. אם החדר עדיין לא מוכן: מבקשים להשאיר מזוודות / רכב אם אפשר, אוכלים צהריים או עושים משהו קטן ורגוע בלבד.'",
              "address: 'Strada Dolomites 55/A int.1, 38036 Sèn Jan di Fassa (TN), Italy', parking: 'חניה פרטית חינם במקום', openingHours: 'Check-in כרגע מופיע 15:00–21:30 · check-out עד 10:00', notes: 'הוזמן ל־8–10.10, 2 לילות · Garden · Bed & Breakfast · welcome drink included. אם החדר עדיין לא מוכן: מבקשים להשאיר מזוודות / רכב אם אפשר, אוכלים צהריים או עושים משהו קטן ורגוע בלבד. ביטול: עד 22.9 23:59 — 30%; לאחר מכן 70%; אחרי 4.10 23:59 או no-show — 100%.'", 1)

# Day 9 (Oct 10): exact Abacus Hotel as final destination.
d9_start = s.index("      id: 'day-9', number: 9, date: '2026-10-10'")
d9_end = s.index("      id: 'day-10', number: 10, date: '2026-10-11'", d9_start)
d9 = s[d9_start:d9_end]
d9 = d9.replace("      routeLabel: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → Varone Waterfall → Riva del Garda ⇄ Limone sul Garda → Milan / Sesto San Giovanni',", "      routeLabel: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → Varone Waterfall → Riva del Garda ⇄ Limone sul Garda → Abacus Hotel, Sesto San Giovanni',")
d9 = d9.replace("      overnight: 'Milan / Sesto San Giovanni area · לילה 1 מתוך 2',", "      overnight: 'Abacus Hotel · לילה 1 מתוך 2',")
d9 = d9.replace("      drivingTime: 'כ־4–5 שעות בסה״כ, בהתאם לתנועה',", "      drivingTime: 'כ־4–4.5 שעות נהיגה מצטברת, בהתאם לתנועה ולכבישי Garda',")
d9 = d9.replace("        drive('drive-riva-milan', 'Riva del Garda → Milan / Sesto San Giovanni area', 'כ־2.5–3 שעות · בהתאם לתנועה', 'אחר הצהריים / ערב', { notes: 'היעד הוא להגיע למלון בערב ולישון באזור Milan לפני Monza.' }),\n        place({ id: 'milan-hotel', type: 'hotel', name: 'Milan / Sesto San Giovanni · אזור לינה משוער', time: 'ערב', status: 'to-book', coordinates: coords.sesto, details: { notes: 'אותו מלון ישמש גם לקראת יום Monza ב־11.10. Sesto San Giovanni הוא בסיס העבודה כרגע עד סגירת המלון.' } }),",
"        drive('drive-riva-abacus', 'Riva del Garda → Abacus Hotel, Sesto San Giovanni', 'כ־2:05–2:30 שעות · בהתאם לתנועה', 'אחר הצהריים / ערב', { notes: 'זמן בסיס ל־Sesto הוא סביב 2:06 שעות; משאירים buffer לתנועה. היעד המדויק: Via Monte Grappa 39.' }),\n        place({ id: 'abacus-hotel-day9', type: 'hotel', name: 'Abacus Hotel', time: 'ערב', status: 'booked', coordinates: coords.abacusHotel, details: { address: 'Via Monte Grappa 39, 20099 Sesto San Giovanni MI, Italy', parking: 'Garage כלול בהזמנה', openingHours: 'Check-in מ־14:00 · check-out לפני 12:00', notes: 'הוזמן ל־10–12.10, 2 לילות · Exclusive King Double Room · Room only. ביטול / שינוי חינם עד 15 ימים לפני ההגעה; 25.9 הוא היום האחרון בחלון החינמי. מ־26.9 ההזמנה אינה ניתנת להחזר או שינוי.' } }),")
s = s[:d9_start] + d9 + s[d9_end:]

# Day 10 (Oct 11): exact Abacus base, event-day buffers, car stays at hotel for Milan evening.
d10_start = s.index("      id: 'day-10', number: 10, date: '2026-10-11'")
d10_end = s.index("      id: 'day-11', number: 11, date: '2026-10-12'", d10_start)
d10 = s[d10_start:d10_end]
d10 = d10.replace("      startBase: 'Sesto San Giovanni · לינה משוערת',", "      startBase: 'Abacus Hotel, Sesto San Giovanni',")
d10 = d10.replace("      routeLabel: 'Sesto San Giovanni → Autodromo Nazionale Monza → Milan center → Sesto San Giovanni',", "      routeLabel: 'Abacus Hotel → Autodromo Nazionale Monza → Abacus Hotel → M1 → Milan center → M1 → Abacus Hotel',")
d10 = d10.replace("      overnight: 'Sesto San Giovanni · לינה משוערת · לילה 2 מתוך 2',", "      overnight: 'Abacus Hotel · לילה 2 מתוך 2',")
d10 = d10.replace("      drivingTime: 'כ־1.5–2 שעות כולל הגעה וחניה',", "      drivingTime: 'ל־Monza ובחזרה: להקצות כ־30–50 דקות לכל כיוון ביום אירוע · Milan בערב במטרו',")
d10 = d10.replace("        drive('drive-milan-monza', 'Sesto San Giovanni → Autodromo Nazionale Monza', '45–60 דקות ביום אירוע', 'השעה תיקבע לפי לו״ז המרוצים', { notes: 'כולל מרווח להגעה וחניה.' }),",
"        place({ id: 'abacus-hotel-day10-start', type: 'hotel', name: 'Abacus Hotel', time: 'בוקר', status: 'booked', coordinates: coords.abacusHotel, details: { address: 'Via Monte Grappa 39, 20099 Sesto San Giovanni MI, Italy', parking: 'Garage כלול בהזמנה', notes: 'נקודת היציאה ל־Monza.' } }),\n        drive('drive-abacus-monza', 'Abacus Hotel → Autodromo Nazionale Monza', 'כ־30–50 דקות ביום אירוע', 'השעה תיקבע לפי לו״ז המרוצים', { notes: 'המלון נמצא כ־9 ק״מ מה־Autodromo; בזמן רגיל הדרך קצרה משמעותית, אבל שומרים buffer לתנועת אירוע, כניסות וחניה.' }),", 1)
d10 = d10.replace("        drive('drive-monza-hotel', 'Monza → Sesto San Giovanni', '≈30–45 דקות', 'אחרי המרוצים', { notes: 'חזרה למלון לפני היציאה למרכז Milan.' }),\n        transfer('metro-sesto-milan', 'Sesto San Giovanni → Milan center', '≈20–30 דקות', 'אחרי החזרה למלון', { notes: 'מטרו M1; עדיף להשאיר את הרכב במלון ולא להיכנס איתו למרכז.' }),",
"        drive('drive-monza-abacus', 'Autodromo Nazionale Monza → Abacus Hotel', 'כ־30–50 דקות ביום אירוע', 'אחרי המרוצים', { notes: 'חוזרים למלון, משאירים את הרכב ב־garage הכלול ורק אז יוצאים למרכז Milan.' }),\n        place({ id: 'abacus-before-milan', type: 'hotel', name: 'Abacus Hotel · השארת הרכב', time: 'אחרי Monza', status: 'booked', coordinates: coords.abacusHotel, details: { parking: 'Garage כלול בהזמנה', notes: 'מכאן הולכים ל־Sesto 1° Maggio FS. התחנה כ־4 דקות הליכה מהמלון.' } }),\n        transfer('metro-sesto-milan', 'Sesto 1° Maggio FS → Milan center / Duomo', 'כ־25–30 דקות', 'אחרי החזרה למלון', { notes: 'M1 ישיר לכיוון מרכז Milan. לא נכנסים למרכז עם הרכב.' }),", 1)
d10 = d10.replace("        transfer('metro-milan-sesto', 'Milan center → Sesto San Giovanni', '≈20–30 דקות', 'בסוף הערב', { notes: 'חזרה במטרו M1 ללינה.' }),",
"        transfer('metro-milan-sesto', 'Milan center → Sesto 1° Maggio FS', 'כ־25–30 דקות', 'בסוף הערב', { notes: 'חזרה ב־M1 ואז כ־4 דקות הליכה ל־Abacus Hotel.' }),\n        place({ id: 'abacus-night2', type: 'hotel', name: 'Abacus Hotel · לילה 2 מתוך 2', time: 'לילה', status: 'booked', coordinates: coords.abacusHotel, details: { address: 'Via Monte Grappa 39, 20099 Sesto San Giovanni MI, Italy', parking: 'Garage כלול בהזמנה', openingHours: 'Check-out למחרת לפני 12:00' } }),", 1)
s = s[:d10_start] + d10 + s[d10_end:]

# Day 11 (Oct 12): exact hotel start and airport drive; preserve flight/rental details.
d11_start = s.index("      id: 'day-11', number: 11, date: '2026-10-12'")
d11_end = s.index("  ],\n  flights:", d11_start)
d11 = s[d11_start:d11_end]
d11 = d11.replace("      startBase: 'Sesto San Giovanni · לינה משוערת',", "      startBase: 'Abacus Hotel, Sesto San Giovanni',")
d11 = d11.replace("      title: 'Milan → טיסה חזרה',", "      title: 'Abacus Hotel → טיסה חזרה',")
d11 = d11.replace("      routeLabel: 'Sesto San Giovanni → Milan Malpensa Airport → Tel Aviv Airport',", "      routeLabel: 'Abacus Hotel → Milan Malpensa Airport → Tel Aviv Airport',")
d11 = d11.replace("      drivingTime: '≈50–60 דקות מ־Sesto · משוער',", "      drivingTime: 'כ־40–50 דקות מ־Abacus Hotel ל־Malpensa · לפני buffer',")
d11 = d11.replace("        place({ id: 'milan-departure', type: 'hotel', name: 'Sesto San Giovanni · יציאה מהלינה המשוערת', time: '≈08:30–09:00', status: 'optional', coordinates: coords.sesto, details: { notes: 'שעה משוערת בלבד; תתעדכן אחרי בחירת המלון.' } }),\n        drive('drive-milan-mxp', 'Sesto San Giovanni → Milan Malpensa Airport', '≈50–60 דקות', '≈08:30–09:00', { notes: 'הערכה לפי בסיס לינה ב־Sesto; תתעדכן לאחר סגירת המלון.' }),",
"        place({ id: 'abacus-departure', type: 'hotel', name: 'Abacus Hotel · צ׳ק־אאוט ויציאה', time: '≈08:30–09:00', status: 'booked', coordinates: coords.abacusHotel, details: { address: 'Via Monte Grappa 39, 20099 Sesto San Giovanni MI, Italy', openingHours: 'Check-out לפני 12:00', parking: 'Garage כלול בהזמנה' } }),\n        drive('drive-abacus-mxp', 'Abacus Hotel → Milan Malpensa Airport', 'כ־40–50 דקות', '≈08:30–09:00', { notes: 'זמן נהיגה נטו ממקורות מסלול הוא סביב 39–43 דקות; נשאיר buffer לתנועה ולהחזרת הרכב.' }),", 1)
s = s[:d11_start] + d11 + s[d11_end:]

# Reservation list: five hotels booked, no remaining lodging to book. Preserve unrelated activity statuses.
old_res = """    { id: 'hotel-lake-como', name: 'Ca’ del Lasco – Tulipano · Bellano', category: 'Hotels', date: '2026-10-02', status: 'booked' },
    { id: 'hotel-bressanone', name: 'ecHo Apartments & SPA · Bressanone', category: 'Hotels', date: '2026-10-04', status: 'planning' },
    { id: 'hotel-san-candido', name: 'Post Residence - Home of Memories - Dolomites · San Candido', category: 'Hotels', date: '2026-10-06', status: 'planning' },
    { id: 'hotel-pozza', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · Pozza di Fassa · 8–10.10', category: 'Hotels', date: '2026-10-08', status: 'booked' },
    { id: 'hotels-remaining', name: 'שאר הלינות לאורך המסלול', category: 'Hotels', status: 'to-book' },"""
new_res = """    { id: 'hotel-lake-como', name: 'Ca’ del Lasco – Tulipano · Bellano', category: 'Hotels', date: '2026-10-02', status: 'booked' },
    { id: 'hotel-bressanone', name: 'ecHo Apartments & SPA · Bressanone', category: 'Hotels', date: '2026-10-04', status: 'booked' },
    { id: 'hotel-san-candido', name: 'Post Residence - Home of Memories - Dolomites · San Candido', category: 'Hotels', date: '2026-10-06', status: 'booked' },
    { id: 'hotel-pozza', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE · Pozza di Fassa', category: 'Hotels', date: '2026-10-08', status: 'booked' },
    { id: 'hotel-sesto', name: 'Abacus Hotel · Sesto San Giovanni', category: 'Hotels', date: '2026-10-10', status: 'booked' },"""
if old_res not in s:
    raise SystemExit('Hotel reservation list anchor missing')
s = s.replace(old_res, new_res, 1)

# Update route overview path/labels to exact Abacus property.
s = s.replace("{ id: 'day-9-map', dayNumber: 9, href: '#/day/day-9', name: 'North Lake Garda · Varone / Riva / Limone', label: 'יום 9 · 10.10', ...coords.riva },", "{ id: 'day-9-map', dayNumber: 9, href: '#/day/day-9', name: 'North Lake Garda → Abacus Hotel', label: 'יום 9 · 10.10', ...coords.riva },", 1)
s = s.replace("{ id: 'day-10-map', dayNumber: 10, href: '#/day/day-10', name: 'Autodromo Nazionale Monza', label: 'יום 10 · 11.10', ...coords.monza },", "{ id: 'day-10-map', dayNumber: 10, href: '#/day/day-10', name: 'Monza + Milan · Abacus Hotel base', label: 'יום 10 · 11.10', ...coords.monza },", 1)

p.write_text(s)
