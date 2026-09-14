from pathlib import Path

path = Path('index.html')
text = path.read_text()

old_block = """/* Day navigation tabs */
.day-tabs { display: flex; flex-wrap: wrap; gap: 8px; margin: 14px 0 22px; }
.day-tab { min-height: 42px; display: inline-flex; align-items: center; justify-content: center; padding: 8px 14px; border: 1px solid var(--border); border-radius: 999px; background: var(--surface); color: var(--muted); font-size: 16px; font-weight: 650; transition: .2s ease; }
.day-tab:nth-child(4n + 1), .day-tab:nth-child(4n + 2) { background: #F3E8DC; border-color: #DFCDBC; color: #5F5954; }
.day-tab:nth-child(4n + 3), .day-tab:nth-child(4n + 4) { background: #E1ECE4; border-color: #C9D9CE; color: #536058; }
.day-tab:hover { border-color: #CFC7BE; color: var(--ink); filter: brightness(.985); }
.day-tab.is-active { background: var(--green); border-color: var(--green); color: #fff; filter: none; }
"""
new_block = """/* Day navigation tabs */
.day-tabs { display: flex; flex-wrap: wrap; gap: 8px; margin: 14px 0 22px; }
.day-tab { min-height: 42px; display: inline-flex; align-items: center; justify-content: center; padding: 8px 14px; border: 1px solid var(--border); border-radius: 999px; background: var(--surface); color: var(--muted); font-size: 16px; font-weight: 650; transition: .2s ease; }
.day-tab:hover { border-color: #D7D3CE; background: var(--surface-2); color: var(--ink); }
.day-tab.is-active { background: #466653; border-color: #466653; color: #fff; }
"""

if old_block in text:
    text = text.replace(old_block, new_block, 1)
elif new_block not in text:
    raise SystemExit('Day tabs CSS block not found')

old_override = """/* Slightly quieter accent for active controls. */
.day-tab.is-active { background: #9A5B4A; border-color: #9A5B4A; }
"""
new_override = """/* Active day tab uses the existing deep site green. */
.day-tab.is-active { background: #466653; border-color: #466653; color: #fff; }
"""
if old_override in text:
    text = text.replace(old_override, new_override, 1)
elif new_override not in text:
    raise SystemExit('Day tab active override not found')

path.write_text(text)
