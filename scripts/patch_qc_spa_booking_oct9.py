from pathlib import Path

p = Path('index.html')
s = p.read_text()

arrival = "        place({ id: 'qc-spa-arrival-buffer', type: 'transfer', name: 'DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE → QC Spa Dolomiti', time: 'יציאה סביב 16:30–16:40', duration: 'כ־8 דקות הליכה · או נסיעה קצרה לחניה המומלצת', status: 'planned', coordinates: coords.qcSpa, details: { parking: 'Free parking: Strada de la Veisc 75, Pozza di Fassa', notes: 'המטרה היא להגיע ל־reception סביב 16:40–16:50, לא בדיוק ב־17:00. אם מזג האוויר נעים, ההליכה הישירה מהמלון היא כ־700 מ׳.' } }),"
qc = "        place({ id: 'qc-terme', type: 'activity', name: 'QC Spa Dolomiti', time: '17:00', duration: 'Evening Spa Entrance', status: 'booked', coordinates: coords.qcSpa, details: { reservation: 'הוזמן ל־9.10.2026 · 17:00 · 2 מבוגרים', address: 'Strada di Bagnes 21, Pozza di Fassa, Sèn Jan di Fassa (TN), Italy', parking: 'אפשרות 1: הליכה מהמלון — כ־700 מ׳ / כ־8 דקות. אפשרות 2: חניה חינמית מומלצת באישור: Strada de la Veisc 75, Pozza di Fassa; משם חוצים את הגשר ל־QC.', notes: 'qc-spa-booked-1700 · להגיע ל־reception בערך 16:40–16:50 כדי להשאיר buffer להליכה / חניה / החלפה. הגישה מובטחת לשעת הכניסה שנבחרה; איחור מרבי: 30 דקות. מקבלים חלוק, מגבת, כפכפים ומוצרי courtesy — צריך להביא רק בגדי ים. Evening admission כולל Aperiterme. יש לצאת מהבריכות ואזורי ה־wellness 30 דקות לפני סגירת הספא. ביטול ללא קנס עד שעה לפני הכניסה; ביטול מאוחר / no-show עשויים לגרור חיוב מלא של השירות.' } }),"
ret = "        place({ id: 'qc-spa-return-hotel', type: 'transfer', name: 'QC Spa Dolomiti → DOLOMITI EXCLUSIVE YOUR MOUNTAIN SUITE', time: 'אחרי הספא', duration: 'כ־8 דקות הליכה · או חזרה לרכב', status: 'planned', coordinates: coords.dolomitiExclusive, details: { notes: 'אין שעת סיום קשיחה באתר — חוזרים ישירות למלון אחרי שסיימנו.' } }),"

wrong = qc + "\n" + arrival + "\n" + ret
right = arrival + "\n" + qc + "\n" + ret

if right in s:
    raise SystemExit(0)
if wrong not in s:
    raise SystemExit('QC timeline sequence not found')

s = s.replace(wrong, right, 1)
p.write_text(s)
