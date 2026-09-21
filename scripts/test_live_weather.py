from pathlib import Path
import re

html = Path('index.html').read_text()

# Live weather must come from Open-Meteo in the browser, never hard-coded forecast values.
for token in [
    "https://api.open-meteo.com/v1/forecast?",
    "forecast_days: '16'",
    "timezone: 'auto'",
    "temperature_unit: 'celsius'",
    "wind_speed_unit: 'kmh'",
    "precipitation_unit: 'mm'",
    "fetch(weatherApiUrl(), { cache: 'no-store' })",
]:
    assert token in html, f'Missing live weather API token: {token}'

for field in [
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_probability_max",
    "precipitation_sum",
    "snowfall_sum",
    "wind_speed_10m_max",
]:
    assert field in html, f'Missing requested weather field: {field}'

# Exactly 11 trip-day weather locations, using existing itinerary coordinates.
weather_block = html.split("const weatherLocations = [", 1)[1].split("]\n\nconst weatherState", 1)[0]
assert weather_block.count("dayId: 'day-") == 11, "Expected one weather location for each of 11 trip days"
for token in [
    "dayId: 'day-1', date: '2026-10-02', name: 'Bellano / Lake Como', coordinates: coords.bellano",
    "dayId: 'day-3', date: '2026-10-04', name: 'Val di Funes / Santa Maddalena', coordinates: coords.santaMaddalena",
    "dayId: 'day-4', date: '2026-10-05', name: 'Seceda', coordinates: coords.seceda",
    "dayId: 'day-5', date: '2026-10-06', name: 'Alpe di Siusi / Compatsch', coordinates: coords.alpeSiusi",
    "dayId: 'day-6', date: '2026-10-07', name: 'Tre Cime di Lavaredo', coordinates: coords.treCime",
    "dayId: 'day-7', date: '2026-10-08', name: 'Passo Sella', coordinates: coords.passoSella",
    "dayId: 'day-8', date: '2026-10-09', name: 'Val San Nicolò', coordinates: coords.baitaCascate",
    "dayId: 'day-9', date: '2026-10-10', name: 'Riva del Garda', coordinates: coords.riva",
    "dayId: 'day-10', date: '2026-10-11', name: 'Milan', coordinates: coords.milan",
    "dayId: 'day-11', date: '2026-10-12', name: 'Milan Malpensa', coordinates: coords.malpensa",
]:
    assert token in weather_block, f'Wrong or missing trip weather location: {token}'

# Session-memory cache only: no stale forecast persistence.
assert "localStorage" not in html
assert "WEATHER_REFRESH_MS = 30 * 60 * 1000" in html
assert html.count("weatherRefreshTimer = window.setInterval") == 1
assert "if (!weatherRefreshTimer)" in html
assert "if (weatherState.request) return weatherState.request" in html
assert "if (!force && weatherIsFresh()) return weatherState.byDay" in html

# Overview + day-page UI, loading/fallback/confidence states and accessible text labels.
for token in [
    'id="overview-weather-section"',
    'id="day-weather-summary"',
    "מזג האוויר בטיול",
    "תחזית חיה שמתעדכנת אוטומטית ככל שמתקרבים לתאריך",
    "עדיין מוקדם לתחזית",
    "התחזית תופיע אוטומטית כשנתקרב לתאריך.",
    "לא הצלחנו לטעון את התחזית כרגע",
    "תחזית מוקדמת — עוד עשויה להשתנות",
    "עודכן: היום ",
    "טוען תחזית…",
]:
    assert token in html, f'Missing weather UI state: {token}'

# WMO codes must map to human-readable Hebrew labels, not raw numbers.
for label in ["בהיר", "מעונן חלקית", "מעונן", "ערפל", "טפטוף", "גשם", "ממטרים", "שלג", "סופת רעמים"]:
    assert label in html, f'Missing WMO Hebrew label: {label}'

# Mobile weather must remain compact and horizontally scrollable.
assert ".weather-grid {" in html
assert "overflow-x: auto;" in html
assert "scroll-snap-type: x proximity;" in html

# Weather integrates with hash rendering without replacing the whole app after fetch.
assert "initWeatherRefresh()" in html
assert "function updateWeatherWidgets()" in html
assert "overview.outerHTML = renderWeatherOverviewSection(trip)" in html
assert "dayWeather.outerHTML = renderDayWeather(day)" in html

print('Live Open-Meteo weather verification passed')
