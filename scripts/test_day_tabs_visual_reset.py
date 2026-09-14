from pathlib import Path
import re

html = Path('index.html').read_text()

# Day tabs should use one neutral style for all inactive days.
assert ".day-tab {" in html, "Day tab base style missing"
assert "background: var(--surface);" in html, "Inactive day tabs are not neutral white"
assert "color: var(--muted);" in html, "Inactive day tab text should stay muted"

# The old alternating pair colors must be completely removed.
for old in [
    ".day-tab:nth-child(4n + 1), .day-tab:nth-child(4n + 2)",
    ".day-tab:nth-child(4n + 3), .day-tab:nth-child(4n + 4)",
    "#F3E8DC",
    "#DFCDBC",
    "#E1ECE4",
    "#C9D9CE",
]:
    assert old not in html, f"Old alternating day-tab styling still present: {old}"

# Active day uses the site's existing deep green, not the old brown accent.
active_rules = re.findall(r"\.day-tab\.is-active\s*\{([^}]*)\}", html, flags=re.S)
assert active_rules, "Active day-tab rule missing"
active_css = "\n".join(active_rules)
assert "#466653" in active_css, "Active day tab is not using the approved deep green"
assert "#9A5B4A" not in active_css, "Old brown active color still used for day tabs"
assert "color: #fff" in active_css or "color: white" in active_css, "Active day tab text should be white"

print('Day tabs visual reset verification passed')
