from pathlib import Path
import re

html = Path('index.html').read_text()

# Old stacked alert system must be gone.
for old in [
    "function renderDayAlerts",
    'class="day-alerts"',
    'class="day-alert"',
    ".day-alerts {",
    ".day-alert {",
]:
    assert old not in html, f'Old stacked day-alert UI returned: {old}'

# Critical alerts are intentionally rare: only Alpe di Siusi and Tre Cime.
assert html.count("criticalAlert: '") == 2
for token in [
    "Alpe di Siusi: צריך לעבור את מגבלת הכניסה לרכב פרטי ל־Compatsch לפני 09:00.",
    "Tre Cime: החניה הוזמנה ל־7.10. פתיחת הכביש באוקטובר עדיין תלויה במזג האוויר — לבדוק תנאים לפני היציאה.",
]:
    assert token in html, f'Missing critical alert: {token}'

# General notes are collapsed native details and live after the timeline.
assert html.count("dayNotes: [") == 4
assert '<details class="day-notes">' in html
assert '<details class="day-notes" open' not in html
assert "דגשים ליום" in html
assert "הערה אחת" in html

day_page = html.split("function renderDayPage", 1)[1].split("function renderFullMapPage", 1)[0]
weather_pos = day_page.index("${renderDayWeather(day)}")
critical_pos = day_page.index("${renderCriticalAlert(day)}")
timeline_pos = day_page.index("${renderTimeline(day.stops)}")
notes_pos = day_page.index("${renderDayNotes(day)}")
assert weather_pos < critical_pos < timeline_pos < notes_pos, "Day hierarchy must be weather -> critical -> timeline -> notes"

# Audited general notes retained only where useful.
for token in [
    "לוחות המעבורות ל־3.10 עדיין דורשים בדיקה סמוך למועד",
    "אם הנסיעה מ־Bellano מתעכבת, מקצרים קודם את השיטוט במרכז Bolzano",
    "אחרי Passo Sella בוחרים לכל היותר אופציה אחת",
    "Buffaure, Ciampac ו־Ciampedie כבר מחוץ לעונת הפעילות",
]:
    assert token in html, f'Missing compact day note: {token}'

# Duplicated / low-value top alerts must not return.
for old in [
    "בוקר קבוע: יוצאים מ־Ca’ del Lasco ברגל 08:40–08:45",
    "אחרי Orrido היום גמיש:",
    "הרכב נשאר כל היום בחניה הפרטית של Ca’ del Lasco. אחרי Orrido",
    "Ca’ del Lasco: check-out רשמי עד 10:00; אנחנו יוצאים כבר ב־08:00",
    "החלטת מזוודות — פתוחה / להחלטה סופית:",
    "הסדר החדש מכוון: Lago di Braies לפני Funbob",
    "כל היום ברכב השכור — אין מעבורת",
    "Ciclopista del Garda: עושים רק טעימה",
    "הסדנה ב־18:30 הוזמנה. צריך להיות ב־Viale Premuda 13",
]:
    assert old not in html, f'Duplicate planning-history alert returned: {old}'

# Detailed operational information remains in the relevant stop cards.
for token in [
    "רכב פרטי רשאי לעלות ל־Compatsch רק לפני 09:00",
    "פתיחת הכביש באוקטובר תלויה במזג האוויר",
    "חניה הוזמנה מראש ל־7.10.2026",
    "לוחית הרישוי עדיין לא הוזנה כי מדובר ברכב שכור",
    "Shuttle 29.5–11.10.2026 · 08:30–18:30",
    "איחור מרבי: 30 דקות",
    "המזוודות נשארות מוסתרות בתא המטען",
    "התוכנית עדיין אינה סופית ויש לבדוק שוב סמוך ל־11.10",
    "חובה להיות בנקודת המפגש עד 18:15",
    "כרטיס circular / day-type",
]:
    assert token in html, f'Operational detail was lost: {token}'

# Mobile critical strip and collapsed notes remain compact.
for token in [
    ".day-critical-alert {",
    "min-height: 44px;",
    ".day-notes {",
    ".day-notes > summary {",
]:
    assert token in html, f'Missing compact alert CSS: {token}'

# Live weather remains in the top hierarchy.
assert "const WEATHER_REFRESH_MS = 30 * 60 * 1000" in html
assert "${renderDayWeather(day)}" in day_page

print('Day alert hierarchy verification passed')
