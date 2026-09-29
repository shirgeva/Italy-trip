from pathlib import Path
import re

html = Path('index.html').read_text()
packing = html.split('  packing: [', 1)[1].split('\n  ],', 1)[0]
groups = re.findall(r"\{ title: '([^']+)', items: \[([^\]]+)\] \}", packing)
assert len(groups) == 8, f'Expected 8 packing categories, found {len(groups)}'

labels = [label for _, items in groups for label in re.findall(r"'([^']+)'", items)]
assert len(labels) == len(set(labels)), 'Duplicate packing labels'

required = {
    'בגדים ונעליים': ['בגדים נוחים ליום יום', 'מעיל', 'נעליים לשטח', 'כפפות דקות', 'מעיל גשם / שכבה נגד רוח'],
    'רחצה וטיפוח': ['סבונים', 'קרם הגנה לפנים', 'ערכת ציפורניים'],
    'מסמכים וכסף': ['דרכון', 'מזומן שקלים למונית', 'כרטיס אשראי על שם אייל', 'אישורי טיסות, רכב ומלונות'],
    'אלקטרוניקה': ['מטען לפלאפון', 'כבל טעינה לרכב', 'מתאם חשמל', 'מעמד לטלפון ברכב'],
    'משקפיים ואביזרים': ['משקפי ראייה ספייר', 'תיק גב', 'תיק קטן ליום'],
    'דברים לדרך / כביסה / היגיינה': ['דפי מנטה', 'שקיות לבגדים מלוכלכים', 'בקבוק מים'],
    'פנאי': ['קינדל', 'תשבצים + סודוקו + עט'],
    'תרופות ועזרה ראשונה': ['גלולות + ספייר', 'כל התרופות החדשות של אייל', 'פניסטיל'],
}
for category, items in required.items():
    group_items = next((content for title, content in groups if title == category), '')
    assert group_items, f'Missing category: {category}'
    for item in items:
        assert f"'{item}'" in group_items, f'Missing item in {category}: {item}'

for token in ['<details class="packing-card', '<summary class="packing-summary"', 'packing-progress',
              'localStorage.getItem(PACKING_STORAGE_KEY)', 'localStorage.setItem(PACKING_STORAGE_KEY',
              'initPackingChecklist()', 'data-packing-item']:
    assert token in html, f'Missing packing behavior: {token}'

assert 'רשימה בסיסית להתחלה' not in html
print('Packing categories, preserved items, accordion, and persistence wiring verified')
