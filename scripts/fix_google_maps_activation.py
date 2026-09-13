from pathlib import Path

p = Path('index.html')
s = p.read_text()

old_config = """const GOOGLE_MAPS_PLACEHOLDER = '__GOOGLE_MAPS_API_KEY__'
window.ITALY_TRIP_CONFIG = window.ITALY_TRIP_CONFIG || { googleMapsApiKey: GOOGLE_MAPS_PLACEHOLDER }

let leafletLoadPromise = null"""
new_config = """const GOOGLE_MAPS_PLACEHOLDER_PREFIX = '__GOOGLE_MAPS_'
window.ITALY_TRIP_CONFIG = window.ITALY_TRIP_CONFIG || { googleMapsApiKey: '__GOOGLE_MAPS_API_KEY__' }

let leafletLoadPromise = null"""

if old_config in s:
    s = s.replace(old_config, new_config, 1)
elif new_config not in s:
    raise SystemExit('Google Maps configuration anchor not found')

old_check = """  if (!raw || raw === GOOGLE_MAPS_PLACEHOLDER || raw.includes('__GOOGLE_MAPS_API_KEY__')) return ''"""
new_check = """  if (!raw || raw.startsWith(GOOGLE_MAPS_PLACEHOLDER_PREFIX)) return ''"""
if old_check in s:
    s = s.replace(old_check, new_check, 1)
elif new_check not in s:
    raise SystemExit('Google Maps key check anchor not found')

old_map_import = """  const { Map } = await google.maps.importLibrary('maps')
  const first = points[0] ?? routePath?.[0] ?? routeStart ?? { lat: 46.1, lng: 11.2 }"""
new_map_import = """  const { Map } = await google.maps.importLibrary('maps')
  await google.maps.importLibrary('marker')
  const first = points[0] ?? routePath?.[0] ?? routeStart ?? { lat: 46.1, lng: 11.2 }"""
if old_map_import in s:
    s = s.replace(old_map_import, new_map_import, 1)
elif new_map_import not in s:
    raise SystemExit('Google marker library import anchor not found')

p.write_text(s)
