from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")

if "id: 'elena-walch'" in s and "id: 'loacker-twenty'" in s:
    print("Day 3 is already updated")
    raise SystemExit(0)


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


s = replace_once(
    s,
    "  menaggio: { lat: 46.0202, lng: 9.2387 },\n  santaMaddalena: { lat: 46.6410, lng: 11.7160 },",
    "  menaggio: { lat: 46.0202, lng: 9.2387 },\n  elenaWalch: { lat: 46.338670, lng: 11.238610 },\n  loackerTwenty: { lat: 46.486521, lng: 11.336929 },\n  santaMaddalena: { lat: 46.6410, lng: 11.7160 },",
    "coordinates",
)

old_map = """  'day-3': {
    points: [
      { name: 'Bellano / Varenna · בסיס לינה', label: 'יציאה 08:00–08:30', ...coords.bellano },
      { name: 'Val di Funes / Santa Maddalena', label: 'כ־4 שעות נסיעה · 12:30–15:00', ...coords.santaMaddalena },
      { name: 'Ortisei / Santa Cristina · בסיס לינה משוער', label: '30–45 דק׳ · הגעה ≈16:00', ...coords.ortisei },
    ],
    routePath: [coords.bellano, coords.santaMaddalena, coords.ortisei],
  },"""
new_map = """  'day-3': {
    points: [
      { name: 'Bellano / Varenna · בסיס לינה', label: 'יציאה 08:00 · דרך צפון Lake Garda', ...coords.bellano },
      { name: 'Elena Walch · אופציונלי', label: '≈12:00–13:00 · יקב / ביסטרו', ...coords.elenaWalch },
      { name: 'Loacker Café Bozen Twenty · אופציונלי', label: '≈13:30–14:00 · קפה / חנות', ...coords.loackerTwenty },
      { name: 'Val di Funes / Santa Maddalena', label: '≈14:50–16:30 · תצפיות והליכה קלה', ...coords.santaMaddalena },
      { name: 'Ortisei / Santa Cristina · בסיס לינה משוער', label: 'הגעה ≈17:15–17:30', ...coords.ortisei },
    ],
    routePath: [coords.bellano, coords.riva, coords.elenaWalch, coords.loackerTwenty, coords.santaMaddalena, coords.ortisei],
  },"""
s = replace_once(s, old_map, new_map, "day 3 map")

replacements = [
    ("      title: 'Lake Como → Val di Funes → Ortisei',", "      title: 'Lake Como → Elena Walch → Val di Funes → Ortisei',", "title"),
    ("      routeLabel: 'Bellano → Val di Funes / Santa Maddalena → Ortisei',", "      routeLabel: 'Bellano → North Lake Garda → Elena Walch → Loacker Twenty → Val di Funes → Ortisei',", "route label"),
    ("      drivingTime: 'כ־4.5–5 שעות',", "      drivingTime: 'כ־5.5–6 שעות נהיגה נטו',", "driving time"),
    ("      walking: 'עד שעה הליכה קלה',", "      walking: 'עד 1–1.5 שעות הליכה קלה',", "walking time"),
    ("      highlights: ['Val di Funes / Santa Maddalena', 'Ortisei'],", "      highlights: ['Elena Walch · אופציונלי', 'Loacker Café Twenty · אופציונלי', 'Val di Funes / Santa Maddalena', 'Ortisei'],", "highlights"),
]
for old, new, label in replacements:
    s = replace_once(s, old, new, label)

old_option = """      areaOptions: [
        {
          id: 'loacker-bolzano-walther',
          name: 'Loacker Café Bolzano Piazza Walther',
          category: 'קפה וחנות',
          description: 'בית קפה וחנות רשמית של המותג. לשמור רק אם המסלול הסופי עובר דרך Bolzano — לא לעשות סטייה מיוחדת בשבילו.',
          details: {
            openingHours: 'ב׳–ש׳ 07:30–19:00 · א׳ 09:00–19:00',
            price: 'אין דמי כניסה · תשלום לפי הזמנה או קנייה',
            address: 'Piazza Walther 11, 39100 Bolzano BZ, Italy',
            notes: 'מתאים כאפשרות ביום המעבר מ־Lake Como לדולומיטים, רק אם הדרך הסופית עוברת באופן טבעי באזור.',
            website: 'https://www.loacker.com/int/en/experience-loacker/loacker-cafe/loacker-cafes/loacker-cafe-bolzano-piazza-walther.html',
          },
        },
      ],
"""
s = replace_once(s, old_option, "", "old Loacker area option")

old_stops = """        drive('drive-como-funes', 'Bellano → Val di Funes / Santa Maddalena', 'כ־4 שעות', '08:00–08:30 יציאה', { notes: 'כולל מרווח קטן לעצירה בדרך.' }),
        place({ id: 'val-di-funes', name: 'Val di Funes / Santa Maddalena', time: '12:30–15:00', duration: '2–2.5 שעות', coordinates: coords.santaMaddalena, details: { notes: 'תצפיות, הכנסייה והליכה קלה. אפשר מסלול מעגלי קל של כ־3.2 ק״מ וכשעה.' } }),
        drive('drive-funes-ortisei', 'Santa Maddalena → Ortisei', '30–45 דקות', '≈15:00'),
        place({ id: 'ortisei-arrival', type: 'hotel', name: 'Ortisei / Santa Cristina', time: '≈16:00', status: 'to-book', coordinates: coords.ortisei, details: { notes: 'צ׳ק־אין והסתובבות קצרה בכפר. Ortisei עדיפות; Santa Cristina אם המחירים טובים יותר.' } }),"""
new_stops = """        drive('drive-como-elena-walch', 'Bellano → Elena Walch · דרך צפון Lake Garda', 'כ־4 שעות', '08:00 יציאה', { notes: 'המסלול המועדף עובר מצפון ל־Lake Garda דרך Riva / Rovereto / Trento. Riva היא נקודת ניתוב בלבד, לא עצירה מתוכננת.' }),
        place({ id: 'elena-walch', type: 'food', name: 'Elena Walch · Winery & Bistro', time: '12:00–13:00', duration: 'כ־שעה', status: 'optional', coordinates: coords.elenaWalch, details: { openingHours: 'יום א׳ 10:00–18:30', address: 'Via Andreas Hofer 1, 39040 Termeno sulla Strada del Vino BZ, Italy', parking: 'חניה במקום', notes: 'עצירה אופציונלית ליין בכוס / ביסטרו. לא מתכננים סיור יקב; אם עייפים או מתעכבים פשוט מדלגים.', website: 'https://www.elenawalch.com/en-GB/vinotheque-tramin' } }),
        drive('drive-elena-loacker', 'Elena Walch → Loacker Café Bozen Twenty', 'כ־25–30 דקות', '≈13:00'),
        place({ id: 'loacker-twenty', type: 'food', name: 'Loacker Café Bozen Twenty', time: '13:30–14:00', duration: '30–40 דקות', status: 'optional', coordinates: coords.loackerTwenty, details: { openingHours: 'יום א׳ 09:00–19:30', address: 'Via G. Galilei 20, 39100 Bolzano BZ, Italy', notes: 'קומה 2 ב־Twenty Shopping Center. קפה / משהו מתוק / חנות. אופציונלי — אם אין כוח או זמן ממשיכים ישר ל־Val di Funes.', website: 'https://www.loacker.com/arabia/en/experience-loacker/loacker-cafe/loacker-cafes/loacker-cafe-bolzano-twenty.html' } }),
        drive('drive-loacker-funes', 'Loacker Café Bozen Twenty → Val di Funes / Santa Maddalena', 'כ־45–55 דקות', '≈14:00'),
        place({ id: 'val-di-funes', name: 'Val di Funes / Santa Maddalena', time: '14:50–16:30', duration: '1.5–2 שעות', coordinates: coords.santaMaddalena, details: { notes: 'תצפיות, הכנסייה והליכה קלה. אפשר לקצר אם הגענו מאוחר יותר בגלל העצירות האופציונליות.' } }),
        drive('drive-funes-ortisei', 'Santa Maddalena → Ortisei', '30–45 דקות', '≈16:30'),
        place({ id: 'ortisei-arrival', type: 'hotel', name: 'Ortisei / Santa Cristina', time: '≈17:15–17:30', status: 'to-book', coordinates: coords.ortisei, details: { notes: 'צ׳ק־אין וערב רגוע. Ortisei עדיפות; Santa Cristina אם המחירים טובים יותר.' } }),"""
s = replace_once(s, old_stops, new_stops, "day 3 stops")

required = [
    "elenaWalch: { lat: 46.338670, lng: 11.238610 }",
    "loackerTwenty: { lat: 46.486521, lng: 11.336929 }",
    "id: 'elena-walch'",
    "id: 'loacker-twenty'",
    "Bellano → North Lake Garda → Elena Walch → Loacker Twenty → Val di Funes → Ortisei",
    "time: '14:50–16:30'",
    "time: '≈17:15–17:30'",
]
missing = [item for item in required if item not in s]
if missing:
    raise SystemExit(f"Missing expected day 3 content: {missing}")
if "Loacker Café Bolzano Piazza Walther" in s:
    raise SystemExit("Old Piazza Walther option is still present")

p.write_text(s, encoding="utf-8")
print("Day 3 update and verification passed")
