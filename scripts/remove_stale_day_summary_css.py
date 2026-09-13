from pathlib import Path

path = Path('index.html')
text = path.read_text()

text = text.replace("  .day-summary { display: flex; overflow-x: auto; }\n  .day-summary > div { min-width: 118px; }\n  .empty-summary { white-space: normal; }\n", "", 1)
text = text.replace("  .day-summary { border-radius: 12px; }\n", "", 1)

path.write_text(text)
