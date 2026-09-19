from pathlib import Path

path = Path('index.html')
text = path.read_text()

# Update only the Day 10 map block.
map_start = text.index("  'day-10': {")
map_end = text.index("  'day-11': {", map_start)
map_block = text[map_start:map_end]
old_map = "13:40 E4 · 14:50 GT Cup"
new_map = "13:40 E4 · 14:50 GT3"
if old_map in map_block:
    map_block = map_block.replace(old_map, new_map)
elif new_map not in map_block:
    raise SystemExit('Day 10 map race label not found')
text = text[:map_start] + map_block + text[map_end:]

# Update only the Day 10 itinerary block.
day_start = text.index("      id: 'day-10', number: 10, date: '2026-10-11'")
day_end = text.index("      id: 'day-11', number: 11, date: '2026-10-12'", day_start)
day_block = text[day_start:day_end]
wrong = "C.I. Gran Turismo Sprint GT Cup"
correct = "Italian GT Sprint GT3"
if wrong in day_block:
    day_block = day_block.replace(wrong, correct)
elif correct not in day_block:
    raise SystemExit('Day 10 GT race name not found')

if 'GT Cup' in day_block:
    raise SystemExit('GT Cup still remains in Day 10 after patch')

text = text[:day_start] + day_block + text[day_end:]
path.write_text(text)
