from pathlib import Path

path = Path('index.html')
text = path.read_text()

# Remove only the October 7 / Day 6 Loacker optional stop.
loacker_block = """      areaOptions: [
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
"""
if loacker_block not in text:
    raise SystemExit('October 7 Loacker block not found exactly once')
text = text.replace(loacker_block, "      areaOptions: [],\n", 1)

# Mark both existing Lago di Carezza option cards as conditional and add the requested warning.
old_carezza = """        {
          id: 'carezza-option',
          name: 'Lago di Carezza',
          category: 'אגם / טבע',
          description: 'אגם אלפיני קטן בצבע טורקיז עם Latemar ברקע. קל ומהיר יחסית לשלב ברכב וללא צורך ברכבל.',
          details: { price: 'אין דמי כניסה לאגם · חניה בתשלום', duration: 'כ־45–60 דקות', notes: 'כ־15–20 דקות מ־Pozza di Fassa. אופציה ספונטנית טובה, אבל נשארת אופציונלית כי כבר יש לנו כמה אגמים בטיול.' },
        },
"""
warning = "⚠️ חשוב לבדוק לפני הנסיעה: באוקטובר מפלס המים ב-Lago di Carezza נמצא בדרך כלל בשפל השנתי, ולעיתים האגם נראה קטן משמעותית לעומת התמונות מהקיץ. כמה ימים לפני הביקור יש לבדוק מצלמה עדכנית / תמונות עדכניות ולוודא שיש מספיק מים וששווה להגיע. אם המפלס נמוך מאוד – לוותר על העצירה ולא לנסוע במיוחד."
new_carezza = f"""        {{
          id: 'carezza-option',
          name: 'Lago di Carezza',
          category: 'אגם / טבע · אופציונלי / מותנה',
          description: 'אגם אלפיני קטן בצבע טורקיז עם Latemar ברקע. קל ומהיר יחסית לשלב ברכב וללא צורך ברכבל.',
          details: {{ price: 'אין דמי כניסה לאגם · חניה בתשלום', duration: 'כ־45–60 דקות', notes: '{warning}' }},
        }},
"""
count = text.count(old_carezza)
if count != 2:
    raise SystemExit(f'Expected exactly 2 Lago di Carezza blocks, found {count}')
text = text.replace(old_carezza, new_carezza)

path.write_text(text)
