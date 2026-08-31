from pathlib import Path
import re

path = Path('index.html')
s = path.read_text(encoding='utf-8')


def sub_once(pattern, repl, label, flags=0):
    global s
    s2, n = re.subn(pattern, repl, s, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    s = s2


def insert_area_option(highlight_literal, block, label):
    global s
    if block.split("name: '", 1)[1].split("'", 1)[0] in s:
        return
    needle = re.escape(f"      highlights: {highlight_literal},\n") + r"(\s*)stops: \["
    replacement = f"      highlights: {highlight_literal},\n{block}\\1stops: ["
    sub_once(needle, replacement, label)


orrido = """      areaOptions: [
        {
          id: 'orrido-bellano',
          name: 'Orrido di Bellano',
          category: 'טבע / מפל',
          description: 'קניון טבעי בתוך Bellano עם מפלים, סלעים ושבילי עץ. ביקור קצר יחסית שמתאים אם נשאר זמן ליד מקום הלינה.',
          details: {
            openingHours: '2.10.2026 · 09:00–18:00 · כניסה אחרונה 20 דקות לפני הסגירה',
            price: '€8 לאדם',
            address: 'Orrido di Bellano, 23822 Bellano LC, Italy',
            notes: 'המסלול פשוט יחסית, אבל כולל מדרגות ומעברים צרים.',
            website: 'https://www.orridobellano.eu/it/orari-e-biglietti/',
          },
        },
      ],
"""
villa = """      areaOptions: [
        {
          id: 'villa-monastero',
          name: 'Villa Monastero',
          category: 'וילה / גנים',
          description: 'וילה היסטורית ב־Varenna עם בית מוזיאון וגן בוטני ארוך על שפת Lake Como. לשמור כאופציה אם נשאר זמן בתוך Varenna.',
          details: {
            openingHours: '3.10.2026 · 10:00–18:00',
            price: '€15 גן + בית מוזיאון · €13 גן בלבד',
            address: 'Viale Giovanni Polvani 4, 23829 Varenna LC, Italy',
            notes: 'הגן פתוח כל יום באוקטובר; בית המוזיאון סגור בימי שלישי בלבד.',
            website: 'https://www.villamonastero.eu/en/opening-hours-ticket/',
          },
        },
      ],
"""
insert_area_option("['Bellano / Varenna']", orrido, 'day 1 Orrido')
insert_area_option("['Varenna + Bellagio', 'Menaggio · אופציונלי']", villa, 'day 2 Villa')

s = s.replace('details[open] summary span { transform: rotate(45deg); }', 'details[open] summary > span { transform: rotate(45deg); }')
s = re.sub(r'\n\s*<p class="area-options-intro">.*?</p>', '', s, count=1)

if 'const areaOptionTopicOrder = {' not in s:
    order = """const areaOptionTopicOrder = {
  'ferrari-store-milan': 10,
  'kiko-passarella': 11,
  'primark-via-torino': 12,
  'venchi-mengoni': 20,
  'venchi-dante': 21,
  'lindt-via-dante': 22,
  'enrico-rizzi-factory': 23,
  'gianduiotto': 24,
  'gelateria-umberto': 25,
  'orsonero-coffee': 30,
  'cafezal-brera': 31,
  'nowhere-coffee': 32,
  'il-cafetero': 33,
  'starbucks-roastery': 34,
  'giusti-milan': 40,
}

"""
    s = s.replace('function renderAreaOptions(day) {', order + 'function renderAreaOptions(day) {', 1)
if 'const orderedOptions = [...options].sort' not in s:
    s = s.replace("  if (!options.length) return ''\n", "  if (!options.length) return ''\n  const orderedOptions = [...options].sort((a, b) => (areaOptionTopicOrder[a.id] ?? 999) - (areaOptionTopicOrder[b.id] ?? 999))\n", 1)
s = s.replace("${options.map(renderAreaOption).join('')}", "${orderedOptions.map(renderAreaOption).join('')}", 1)

if "'#/tasks': 'tasks'" not in s:
    s = s.replace("    '#/packing': 'packing',\n", "    '#/packing': 'packing',\n    '#/tasks': 'tasks',\n", 1)
if "['#/tasks', 'משימות'" not in s:
    s = s.replace("  ['#/packing', 'רשימת ציוד', 'ציוד', 'packing'],\n", "  ['#/packing', 'רשימת ציוד', 'ציוד', 'packing'],\n  ['#/tasks', 'משימות', 'משימות', 'tasks'],\n", 1)
s = s.replace("['#/hub', 'מרכז הטיול', 'מידע', 'hub']", "['#/hub', 'מרכז הטיול', 'מרכז', 'hub']")

if "tasks: '<svg" not in s:
    m = re.search(r"(\s+packing: '<svg.*?</svg>',\n)(\s+search:)", s)
    if not m:
        raise SystemExit('icons: packing/search anchor not found')
    insert = m.group(1) + "    tasks: '<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M9 6h11M9 12h11M9 18h11\"/><path d=\"m3.5 6 1.4 1.4L7.5 4.8M3.5 12l1.4 1.4 2.6-2.6M3.5 18l1.4 1.4 2.6-2.6\"/></svg>',\n    menu: '<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M4 6h16M4 12h16M4 18h16\"/></svg>',\n" + m.group(2)
    s = s[:m.start()] + insert + s[m.end():]

if 'function renderMobileUtilityBar(currentHash)' not in s:
    replacement = '''function renderMobileNav(currentHash) {
  const currentTop = currentHash.startsWith('#/day/') ? '#/itinerary' : currentHash
  const mobilePrimaryItems = navItems.filter(([href]) => ['#/overview', '#/itinerary', '#/map', '#/hub'].includes(href))
  return `<nav class="mobile-nav" aria-label="ניווט מובייל">
    ${mobilePrimaryItems.map(([href, , mobileLabel, icon]) => `<a class="mobile-nav-link ${active(currentTop, href)}" href="${href}"><span class="mobile-nav-icon" aria-hidden="true">${navIcon(icon)}</span><small>${mobileLabel}</small></a>`).join('')}
  </nav>`
}

function renderMobileUtilityBar(currentHash) {
  const currentTop = currentHash.startsWith('#/day/') ? '#/itinerary' : currentHash
  return `<div class="mobile-utility-bar" aria-label="כלים נוספים">
    <button class="mobile-utility-button mobile-menu-trigger" type="button" aria-label="פתיחת תפריט נוסף" aria-expanded="false">${navIcon('menu')}</button>
    <button class="mobile-utility-button search-trigger" type="button" aria-label="חיפוש באתר">${navIcon('search')}</button>
    <div class="mobile-more-menu" id="mobile-more-menu" aria-hidden="true">
      <a class="mobile-more-link ${active(currentTop, '#/packing')}" href="#/packing"><span>${navIcon('packing')}</span><strong>רשימת ציוד</strong></a>
      <a class="mobile-more-link ${active(currentTop, '#/tasks')}" href="#/tasks"><span>${navIcon('tasks')}</span><strong>משימות</strong></a>
    </div>
  </div>`
}

'''
    sub_once(r'function renderMobileNav\(currentHash\) \{.*?\n\}\n\n(?=function renderPageHeader)', replacement, 'mobile nav block', flags=re.S)

if 'function renderTasksPage(trip)' not in s:
    tasks = '''function renderTasksPage(trip) {
  const doneCount = trip.checklist.filter((item) => item.done).length
  return `<section class="page tasks-page">
    ${renderPageHeader('לפני הנסיעה', 'משימות', 'מה כבר סגור ומה עוד נשאר לעשות לפני הטיסה.')}
    <div class="section-heading compact"><div><span class="eyebrow">התקדמות</span><h2>${doneCount}/${trip.checklist.length} הושלמו</h2></div></div>
    <div class="checklist-card tasks-checklist">${trip.checklist.map((item) => `<label class="checklist-item ${item.done ? 'is-done' : ''}"><input type="checkbox" ${item.done ? 'checked' : ''}><span class="custom-check"></span><span>${esc(item.label)}</span></label>`).join('')}</div>
  </section>`
}

'''
    s = s.replace('function renderPackingPage(trip) {', tasks + 'function renderPackingPage(trip) {', 1)

if '${renderMobileUtilityBar(currentHash)}' not in s:
    s = s.replace('${renderSidebar(trip, currentHash)}<main', '${renderSidebar(trip, currentHash)}${renderMobileUtilityBar(currentHash)}<main', 1)
if "case 'tasks': return renderTasksPage(trip)" not in s:
    s = s.replace("    case 'packing': return renderPackingPage(trip)\n", "    case 'packing': return renderPackingPage(trip)\n    case 'tasks': return renderTasksPage(trip)\n", 1)
if "route.page === 'tasks' ? 'משימות'" not in s:
    s = s.replace("route.page === 'packing' ? 'רשימת ציוד' : route.page === 'map'", "route.page === 'packing' ? 'רשימת ציוד' : route.page === 'tasks' ? 'משימות' : route.page === 'map'", 1)

if 'function initMobileUtilityMenu()' not in s:
    utility = '''function initMobileUtilityMenu() {
  const trigger = document.querySelector('.mobile-menu-trigger')
  const menu = document.querySelector('#mobile-more-menu')
  if (!trigger || !menu) return
  const close = () => {
    menu.classList.remove('is-open')
    menu.setAttribute('aria-hidden', 'true')
    trigger.setAttribute('aria-expanded', 'false')
  }
  trigger.addEventListener('click', (event) => {
    event.stopPropagation()
    const willOpen = !menu.classList.contains('is-open')
    if (!willOpen) return close()
    menu.classList.add('is-open')
    menu.setAttribute('aria-hidden', 'false')
    trigger.setAttribute('aria-expanded', 'true')
    window.setTimeout(() => document.addEventListener('click', close, { once: true }), 0)
  })
  menu.addEventListener('click', (event) => event.stopPropagation())
  menu.querySelectorAll('a').forEach((link) => link.addEventListener('click', close))
}

'''
    s = s.replace('let countdownTimer = null\n', utility + 'let countdownTimer = null\n', 1)
if '  initMobileUtilityMenu()\n' not in s:
    s = s.replace('  initGlobalSearch(trip)\n', '  initGlobalSearch(trip)\n  initMobileUtilityMenu()\n', 1)

s = s.replace('שעה משוערת בלבד; תתעדכן אחרי בחירת המלון ותיקון שעת החזרת הרכב.', 'שעה משוערת בלבד; תתעדכן אחרי בחירת המלון.')

if '/* Mobile navigation cleanup */' not in s:
    css = r'''

/* Mobile navigation cleanup */
.mobile-utility-bar { display: none; }
@media (max-width: 720px) {
  .mobile-nav { grid-template-columns: repeat(4, 1fr); }
  .mobile-nav-link small { white-space: nowrap; }
  .mobile-utility-bar { position: fixed; z-index: 1300; top: 10px; right: 10px; display: flex; gap: 8px; direction: rtl; }
  .mobile-utility-button { width: 44px; height: 44px; display: grid; place-items: center; padding: 0; border: 1px solid var(--border); border-radius: 12px; background: rgba(255,255,255,.97); color: var(--ink); box-shadow: 0 6px 18px rgba(32,31,29,.08); backdrop-filter: blur(10px); cursor: pointer; }
  .mobile-utility-button svg { width: 21px; height: 21px; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
  .mobile-more-menu { position: absolute; top: 52px; right: 0; width: 210px; display: none; overflow: hidden; padding: 6px; border: 1px solid var(--border); border-radius: 14px; background: #fff; box-shadow: 0 16px 40px rgba(32,31,29,.16); }
  .mobile-more-menu.is-open { display: grid; }
  .mobile-more-link { min-height: 46px; display: flex; align-items: center; gap: 10px; padding: 8px 10px; border-radius: 10px; color: var(--ink); }
  .mobile-more-link.is-active { background: var(--surface-2); }
  .mobile-more-link > span { width: 24px; height: 24px; display: grid; place-items: center; color: var(--muted); }
  .mobile-more-link svg { width: 19px; height: 19px; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
  .mobile-more-link strong { font-size: 16px; font-weight: 600; }
  .page { padding-top: 76px; }
  .area-option-summary .ltr { transform: none !important; }
}
'''
    s = s.replace('\n</style>', css + '\n</style>', 1)

path.write_text(s, encoding='utf-8')