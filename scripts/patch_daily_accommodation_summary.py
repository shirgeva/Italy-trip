from pathlib import Path

path = Path('index.html')
text = path.read_text()

# Checklist: mark only the accommodation-bases task as complete.
old_checklist = "{ id: 'hotels', label: 'לסגור את בסיסי הלינה לאורך המסלול', done: false }"
new_checklist = "{ id: 'hotels', label: 'לסגור את בסיסי הלינה לאורך המסלול', done: true }"
if old_checklist in text:
    text = text.replace(old_checklist, new_checklist, 1)
elif new_checklist not in text:
    raise SystemExit('Hotel checklist item not found')

# Replace the old multi-metric summary styling with a compact lodging-only card.
old_css = """.day-summary { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); margin-top: 15px; background: var(--surface); border: 1px solid var(--border); border-radius: 14px; overflow: hidden; }
.day-summary > div { padding: 12px 15px; border-left: 1px solid var(--border); }
.day-summary > div:last-child { border-left: 0; }
.day-summary small { display: block; color: var(--muted); font-size: 16px; }
.day-summary strong { display: block; margin-top: 2px; font-size: 16px; }
.empty-summary { display: flex; align-items: center; gap: 9px; padding: 12px 15px; color: var(--muted); }
.empty-summary span { color: var(--ink); font-size: 16px; font-weight: 600; }
.empty-summary small { font-size: 16px; }
"""
new_css = """.day-lodging-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: end;
  gap: 16px;
  margin-top: 15px;
  padding: 13px 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  box-shadow: 0 6px 20px rgba(32,31,29,.045);
}
.day-lodging-copy { min-width: 0; }
.day-lodging-label,
.day-lodging-night {
  color: var(--muted);
  font-size: 16px;
  line-height: 1.4;
}
.day-lodging-label { display: block; margin-bottom: 2px; }
.day-lodging-hotel {
  display: block;
  min-width: 0;
  font-size: 18px;
  line-height: 1.4;
  font-weight: 700;
  overflow-wrap: anywhere;
}
.day-lodging-night {
  white-space: nowrap;
  padding-bottom: 1px;
}
@media (max-width: 720px) {
  .day-lodging-card {
    grid-template-columns: 1fr;
    align-items: start;
    gap: 5px;
    padding: 12px 14px;
  }
  .day-lodging-hotel { font-size: 17px; }
  .day-lodging-night { white-space: normal; }
}
"""
if old_css in text:
    text = text.replace(old_css, new_css, 1)
elif '.day-lodging-card {' not in text:
    raise SystemExit('Old daily summary CSS not found')

# Remove the obsolete day-summary selector from the white-surface group.
text = text.replace('day-card,\n.overview-days-list,\n.itinerary-list,\n.day-summary,\n.stop-card,', 'day-card,\n.overview-days-list,\n.itinerary-list,\n.stop-card,', 1)

# Replace the daily summary renderer. Existing day.overnight values remain the source of truth.
old_function = """function dailySummary(day) {
  const facts = []
  if (day.startBase) facts.push(['יוצאים מ־', day.startBase])
  if (day.drivingTime) facts.push(['נהיגה', day.drivingTime])
  const destinationCount = day.stops.filter((stop) => !['planning', 'drive', 'transfer'].includes(stop.type)).length
  if (destinationCount) facts.push(['עצירות', `${destinationCount}`])
  if (day.walking) facts.push(['הליכה', day.walking])
  if (day.overnight) facts.push(['לינה', day.overnight])

  if (!facts.length) return `<div class="day-summary empty-summary"><span>היום עדיין בתכנון</span><small>נוסיף כאן זמני נסיעה, עצירות ולינה כשייסגרו.</small></div>`
  return `<div class="day-summary">${facts.map(([label, value]) => `<div><small>${esc(label)}</small><strong>${smartText(value)}</strong></div>`).join('')}</div>`
}
"""
new_function = """function dailySummary(day) {
  if (!day.overnight) return ''
  const overnight = String(day.overnight)
  const match = overnight.match(/^(.*) · (לילה \\d+ מתוך \\d+)$/)
  const hotelName = match ? match[1] : overnight
  const nightLabel = match ? match[2] : ''
  return `<div class="day-lodging-card" aria-label="לינה">
    <div class="day-lodging-copy">
      <span class="day-lodging-label">לינה</span>
      <strong class="day-lodging-hotel">${smartText(hotelName)}</strong>
    </div>
    ${nightLabel ? `<span class="day-lodging-night">${esc(nightLabel)}</span>` : ''}
  </div>`
}
"""
if old_function in text:
    text = text.replace(old_function, new_function, 1)
elif 'class="day-lodging-card"' not in text:
    raise SystemExit('Old dailySummary function not found')

path.write_text(text)
