from pathlib import Path
import re
import subprocess
import tempfile

html = Path('index.html').read_text()
workflow = Path('.github/workflows/static.yml').read_text()

required_html = [
    "__GOOGLE_MAPS_API_KEY__",
    "const GOOGLE_MAPS_PLACEHOLDER_PREFIX = '__GOOGLE_MAPS_'",
    "function getGoogleMapsApiKey()",
    "function loadGoogleMaps()",
    "async function createGoogleMap(",
    "async function enhanceMapsWithGoogle(",
    "async function enhanceMaps(trip)",
    "function googleMapsDirectionsUrlsForDay(",
    "function renderGoogleMapsRouteButtons(",
    "פתח מסלול ב-Google Maps",
    "routeModes:",
    "gestureHandling: 'cooperative'",
    "await google.maps.importLibrary('marker')",
    "enhanceMaps(trip)",
]
missing = [token for token in required_html if token not in html]
assert not missing, f"Missing Google Maps migration features: {missing}"

required_workflow = [
    "GOOGLE_MAPS_API_KEY: ${{ secrets.GOOGLE_MAPS_API_KEY }}",
    "__GOOGLE_MAPS_API_KEY__",
]
missing_workflow = [token for token in required_workflow if token not in workflow]
assert not missing_workflow, f"Missing deploy-time key injection: {missing_workflow}"

# Leaflet must remain available as the fallback until Google Maps is activated.
assert "function loadLeaflet()" in html
assert "async function enhanceMapsWithLeaflet(trip)" in html
assert "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" in html

# Never commit a real Google Maps browser key into the public source.
assert "AIza" not in html

# The placeholder sentinel must not become equal to the injected key at deploy time.
assert "const GOOGLE_MAPS_PLACEHOLDER = '__GOOGLE_MAPS_API_KEY__'" not in html
assert "raw === GOOGLE_MAPS_PLACEHOLDER" not in html

# Latest itinerary route decisions must remain unchanged by the map migration.
route_sentinels = [
    "routePath: [coords.echoBressanone, coords.alpeSiusi, coords.passoGardena, coords.postResidence]",
    "routePath: [coords.postResidence, coords.treCime, coords.misurina, coords.braies, coords.postResidence, coords.sanCandido, coords.postResidence]",
    "routePath: [coords.postResidence, coords.passoSella, coords.friedrichAugust, coords.passoSella, coords.dolomitiExclusive]",
    "routePath: [coords.dolomitiExclusive, coords.vidor, coords.baitaCascate, coords.vidor, coords.dolomitiExclusive, coords.qcSpa, coords.dolomitiExclusive]",
    "routePath: [coords.dolomitiExclusive, coords.varone, coords.riva, coords.capoReamol, coords.limone, coords.abacusHotel]",
    "routePath: [coords.abacusHotel, coords.starbucksRoastery, coords.primarkTorino, coords.spunDuomo, coords.venchiMengoni, coords.ferrariMilano, coords.abacusHotel, coords.monza, coords.abacusHotel, coords.cookingClassMilan, coords.gelateriaUmberto, coords.milan, coords.abacusHotel]",
    "routePath: [coords.abacusHotel, coords.malpensa]",
]
missing_routes = [token for token in route_sentinels if token not in html]
assert not missing_routes, f"Itinerary route data changed unexpectedly: {missing_routes}"

# Mixed-mode days must explicitly prevent walking/transit legs from becoming driving routes.
mode_sentinels = [
    "routeModes: ['DRIVING', 'DRIVING', 'DRIVING', 'DRIVING', 'WALKING', 'WALKING']",
    "routeModes: ['DRIVING', 'WALKING', 'WALKING', 'DRIVING']",
    "routeModes: ['DRIVING', 'SHUTTLE', 'SHUTTLE', 'DRIVING', 'WALKING', 'WALKING']",
    "routeModes: ['TRANSIT', 'WALKING', 'WALKING', 'WALKING', 'WALKING', 'TRANSIT', 'DRIVING', 'DRIVING', 'TRANSIT', 'WALKING', 'WALKING', 'TRANSIT']",
]
missing_modes = [token for token in mode_sentinels if token not in html]
assert not missing_modes, f"Missing mixed-transport route metadata: {missing_modes}"

# Every daily map has route-mode metadata, so map rendering and external navigation share one route source.
daily_routes_block = html.split("const dailyMapRoutes = {", 1)[1].split("const trip = {", 1)[0]
assert daily_routes_block.count("routePath:") == 11, "Expected routePath for all 11 days"
assert daily_routes_block.count("routeModes:") == 11, "Expected routeModes for all 11 days"

# Route buttons and map containers need touch-friendly/responsive styling.
for css_token in [".google-route-button", ".map-actions", "min-height: 44px", "@media (max-width: 760px)"]:
    assert css_token in html, f"Missing responsive map UI token: {css_token}"

# Parse-check all inline JavaScript so a malformed map migration cannot be deployed.
inline_scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, flags=re.S | re.I)
assert inline_scripts, "No inline JavaScript found"
with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as tmp:
    tmp.write("\n".join(inline_scripts))
    js_path = tmp.name
subprocess.run(["node", "--check", js_path], check=True)

print('Google Maps migration verification passed')
