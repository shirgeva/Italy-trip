from pathlib import Path

p = Path('index.html')
s = p.read_text()

if "function getGoogleMapsApiKey()" in s:
    raise SystemExit(0)

# 1) Add transport-mode metadata to the EXISTING routePath arrays only.
#    Coordinates, points, stop names, ordering and itinerary content stay untouched.
route_modes = {
    "routePath: [coords.malpensa, coords.caDelLasco, coords.bellano, coords.caDelLasco],":
        "routePath: [coords.malpensa, coords.caDelLasco, coords.bellano, coords.caDelLasco],\n    routeModes: ['DRIVING', 'WALKING', 'WALKING'],",
    "routePath: [coords.caDelLasco, coords.bellano, coords.bellanoStation, coords.varennaStation, coords.varenna, coords.bellagio, coords.menaggio, coords.varenna, coords.varennaStation, coords.bellanoStation, coords.caDelLasco],":
        "routePath: [coords.caDelLasco, coords.bellano, coords.bellanoStation, coords.varennaStation, coords.varenna, coords.bellagio, coords.menaggio, coords.varenna, coords.varennaStation, coords.bellanoStation, coords.caDelLasco],\n    routeModes: ['WALKING', 'WALKING', 'TRANSIT', 'WALKING', 'FERRY', 'FERRY', 'FERRY', 'WALKING', 'TRANSIT', 'WALKING'],",
    "routePath: [coords.caDelLasco, coords.riva, coords.elenaWalch, coords.loackerTwenty, coords.santaMaddalena, coords.echoBressanone],":
        "routePath: [coords.caDelLasco, coords.riva, coords.elenaWalch, coords.loackerTwenty, coords.santaMaddalena, coords.echoBressanone],\n    routeModes: ['DRIVING', 'DRIVING', 'DRIVING', 'DRIVING', 'DRIVING'],",
    "routePath: [coords.echoBressanone, coords.ortisei, coords.seceda, coords.ortisei, coords.echoBressanone],":
        "routePath: [coords.echoBressanone, coords.ortisei, coords.seceda, coords.ortisei, coords.echoBressanone],\n    routeModes: ['DRIVING', 'CABLE', 'CABLE', 'DRIVING'],",
    "routePath: [coords.echoBressanone, coords.alpeSiusi, coords.passoGardena, coords.postResidence],":
        "routePath: [coords.echoBressanone, coords.alpeSiusi, coords.passoGardena, coords.postResidence],\n    routeModes: ['DRIVING', 'DRIVING', 'DRIVING'],",
    "routePath: [coords.postResidence, coords.treCime, coords.misurina, coords.braies, coords.postResidence, coords.sanCandido, coords.postResidence],":
        "routePath: [coords.postResidence, coords.treCime, coords.misurina, coords.braies, coords.postResidence, coords.sanCandido, coords.postResidence],\n    routeModes: ['DRIVING', 'DRIVING', 'DRIVING', 'DRIVING', 'WALKING', 'WALKING'],",
    "routePath: [coords.postResidence, coords.passoSella, coords.friedrichAugust, coords.passoSella, coords.dolomitiExclusive],":
        "routePath: [coords.postResidence, coords.passoSella, coords.friedrichAugust, coords.passoSella, coords.dolomitiExclusive],\n    routeModes: ['DRIVING', 'WALKING', 'WALKING', 'DRIVING'],",
    "routePath: [coords.dolomitiExclusive, coords.vidor, coords.baitaCascate, coords.vidor, coords.dolomitiExclusive, coords.qcSpa, coords.dolomitiExclusive],":
        "routePath: [coords.dolomitiExclusive, coords.vidor, coords.baitaCascate, coords.vidor, coords.dolomitiExclusive, coords.qcSpa, coords.dolomitiExclusive],\n    routeModes: ['DRIVING', 'SHUTTLE', 'SHUTTLE', 'DRIVING', 'WALKING', 'WALKING'],",
    "routePath: [coords.dolomitiExclusive, coords.varone, coords.riva, coords.capoReamol, coords.limone, coords.abacusHotel],":
        "routePath: [coords.dolomitiExclusive, coords.varone, coords.riva, coords.capoReamol, coords.limone, coords.abacusHotel],\n    routeModes: ['DRIVING', 'DRIVING', 'DRIVING', 'DRIVING', 'DRIVING'],",
    "routePath: [coords.abacusHotel, coords.monza, coords.abacusHotel, coords.milan, coords.abacusHotel],":
        "routePath: [coords.abacusHotel, coords.monza, coords.abacusHotel, coords.milan, coords.abacusHotel],\n    routeModes: ['DRIVING', 'DRIVING', 'TRANSIT', 'TRANSIT'],",
    "routePath: [coords.abacusHotel, coords.malpensa],":
        "routePath: [coords.abacusHotel, coords.malpensa],\n    routeModes: ['DRIVING'],",
}
for old, new in route_modes.items():
    if old not in s:
        raise SystemExit(f'Route path anchor missing: {old}')
    s = s.replace(old, new, 1)

# 2) Add responsive map/button styling at the end of the existing stylesheet.
style_insert = r'''
/* Google Maps migration: Google is primary only when a restricted key is configured. */
.map-canvas { height: 470px; }
.map-canvas-mini { height: 430px; }
.map-canvas-large { height: 640px; }
.map-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 12px 14px 14px;
  border-top: 1px solid var(--border);
  background: #fff;
}
.google-route-button {
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 15px;
  border: 1px solid #D7D3CE;
  border-radius: 11px;
  background: var(--ink);
  color: #fff;
  font-size: 16px;
  font-weight: 700;
  line-height: 1.2;
  cursor: pointer;
  transition: transform .18s ease, box-shadow .18s ease;
}
.google-route-button:hover { transform: translateY(-1px); box-shadow: 0 5px 14px rgba(32,31,29,.12); }
.google-route-button svg { width: 17px; height: 17px; flex: 0 0 auto; }
.google-route-note { width: 100%; color: var(--muted); font-size: 16px; line-height: 1.45; }
.google-map-info { min-width: 170px; max-width: 250px; color: #292826; font: 14px/1.35 Arial, sans-serif; text-align: left; direction: ltr; }
.google-map-info strong { display: block; font-size: 15px; margin-bottom: 4px; }
.google-map-info span { display: block; color: #6E6B67; }
.google-map-info a { display: inline-block; margin-top: 7px; color: #466653; font-weight: 700; }
@media (max-width: 760px) {
  .map-canvas { height: 380px; min-height: 330px; }
  .map-canvas-mini { height: 360px; min-height: 330px; }
  .map-canvas-large { height: 420px; min-height: 360px; }
  .map-actions { padding: 11px 12px 13px; }
  .google-route-button { width: 100%; min-height: 48px; }
}
'''
if '</style>' not in s:
    raise SystemExit('Style closing tag missing')
s = s.replace('</style>', style_insert + '\n</style>', 1)

# 3) Daily map gets route button(s), generated from the SAME dailyMapRoutes config.
old_day_map = '''        <div class="map-card sticky-card"><div class="map-heading"><span>המפה של היום</span><small>${hasCoordinates ? 'מסלול משוער · לפי סדר היום' : 'תתמלא עם המסלול'}</small></div><div id="day-map" class="map-canvas" data-map-kind="day" data-day-id="${esc(day.id)}"></div></div>'''
new_day_map = '''        <div class="map-card sticky-card"><div class="map-heading"><span>המפה של היום</span><small>${hasCoordinates ? 'מסלול משוער · לפי סדר היום' : 'תתמלא עם המסלול'}</small></div><div id="day-map" class="map-canvas" data-map-kind="day" data-day-id="${esc(day.id)}"></div>${renderGoogleMapsRouteButtons(day)}</div>'''
if old_day_map not in s:
    raise SystemExit('Day map markup anchor missing')
s = s.replace(old_day_map, new_day_map, 1)

# 4) Replace only the map-engine implementation block. All itinerary data above stays untouched.
engine_start = s.index("const ITALY_GREEN = '#466653'")
engine_end = s.index('function initGlobalSearch(trip)', engine_start)
new_engine = r'''const ITALY_GREEN = '#466653'
const ITALY_RED = '#B97952'
const INK = '#292826'
const MAP_MUTED = '#6E6B67'
const MAP_LOGISTICS = '#77736E'
const MAP_AIRPORT = '#A86D58'
const GOOGLE_MAPS_PLACEHOLDER = '__GOOGLE_MAPS_API_KEY__'
window.ITALY_TRIP_CONFIG = window.ITALY_TRIP_CONFIG || { googleMapsApiKey: GOOGLE_MAPS_PLACEHOLDER }

let leafletLoadPromise = null
let googleMapsLoadPromise = null

function getGoogleMapsApiKey() {
  const raw = String(window.ITALY_TRIP_CONFIG?.googleMapsApiKey ?? '').trim()
  if (!raw || raw === GOOGLE_MAPS_PLACEHOLDER || raw.includes('__GOOGLE_MAPS_API_KEY__')) return ''
  return raw
}

function fallbackMarkup(points, compact = false) {
  if (!points?.length) {
    return `<div class="map-fallback map-fallback-empty"><span class="map-fallback-icon">MAP</span><strong>המפה תתמלא עם המסלול</strong><small>נוסיף נקודות כשנסגור את התכנון היומי.</small></div>`
  }
  return `<div class="map-fallback ${compact ? 'is-compact' : ''}">
    <div class="fallback-route-line"></div>
    ${points.map((point, index) => `${point.href ? `<a class="fallback-point" href="${point.href}">` : '<div class="fallback-point">'}<span>${compact ? '•' : (point.dayNumber ?? index + 1)}</span><div><strong dir="${point.direction ?? 'ltr'}">${point.name}</strong><small>${point.label ?? ''}</small></div>${point.href ? '</a>' : '</div>'}`).join('')}
  </div>`
}

function mapPointsForElement(element, trip) {
  const kind = element.dataset.mapKind
  if (kind === 'overview') {
    return { kind, points: trip.routeAnchors, compact: true, routeStart: trip.routeStart ?? null, routePath: trip.routePath ?? null, routeModes: [], highlightLast: false, day: null }
  }
  if (kind === 'full') {
    return { kind, points: trip.routeAnchors, compact: false, routeStart: trip.routeStart ?? null, routePath: trip.routePath ?? null, routeModes: [], highlightLast: false, day: null }
  }
  if (kind === 'day') {
    const dayId = element.dataset.dayId
    const config = dailyMapRoutes[dayId]
    if (!config) return { kind, points: [], compact: false, routePath: [], routeModes: [], highlightLast: false, day: null }
    return { kind, points: config.points, compact: false, routePath: config.routePath, routeModes: config.routeModes ?? [], highlightLast: false, day: getDayById(trip, dayId) }
  }
  return { kind, points: [], compact: false, routePath: [], routeModes: [], highlightLast: false, day: null }
}

function sameMapPoint(a, b) {
  return Boolean(a && b && Math.abs(a.lat - b.lat) < 0.0000001 && Math.abs(a.lng - b.lng) < 0.0000001)
}

function routeModeGroups(routePath = [], routeModes = []) {
  if (routePath.length < 2) return []
  const modes = routeModes.length === routePath.length - 1 ? routeModes : Array(routePath.length - 1).fill('DIRECT')
  const groups = []
  modes.forEach((mode, index) => {
    const from = routePath[index]
    const to = routePath[index + 1]
    const current = groups[groups.length - 1]
    if (current && current.mode === mode && sameMapPoint(current.points[current.points.length - 1], from)) {
      current.points.push(to)
    } else {
      groups.push({ mode, points: [from, to] })
    }
  })
  return groups
}

function mapStopMatchesPoint(stop, point) {
  return stop?.coordinates && sameMapPoint(stop.coordinates, point)
}

function markerKindForPoint(point, day = null) {
  const name = String(point.name ?? '')
  if (/אופציונלי/i.test(name)) return 'optional'
  if (/Airport/i.test(name)) return 'airport'
  const matches = day?.stops?.filter((stop) => mapStopMatchesPoint(stop, point)) ?? []
  if (matches.some((stop) => stop.reservationStatus === 'optional')) return 'optional'
  if (matches.some((stop) => stop.type === 'hotel') || /Hotel|Residence|Apartments|SUITE|Ca’ del Lasco/i.test(name)) return 'hotel'
  if (matches.some((stop) => ['parking', 'planning', 'car'].includes(stop.type)) || /parking|חניה/i.test(name)) return 'logistics'
  return 'attraction'
}

function markerCategoryLabel(kind) {
  return { hotel: 'Hotel', airport: 'Airport', logistics: 'Parking / logistics', optional: 'Optional', attraction: 'Attraction' }[kind] ?? 'Stop'
}

function markerColorForKind(kind) {
  return { hotel: ITALY_GREEN, airport: MAP_AIRPORT, logistics: MAP_LOGISTICS, optional: '#A8A39E', attraction: INK }[kind] ?? INK
}

function numberedIcon(L, number, color = ITALY_GREEN) {
  return L.divIcon({
    className: 'trip-map-marker-wrap',
    html: `<div class="trip-map-marker" style="--marker-color:${color}">${number}</div>`,
    iconSize: [30, 30],
    iconAnchor: [15, 15],
  })
}

function dotIcon(L, color = ITALY_GREEN) {
  return L.divIcon({
    className: 'trip-map-marker-wrap',
    html: `<div class="trip-map-dot" style="--marker-color:${color}"></div>`,
    iconSize: [13, 13],
    iconAnchor: [6.5, 6.5],
  })
}

function createLeafletMap(element, points, { compact = false, showLine = true, routeStart = null, routePath = null, highlightLast = false } = {}) {
  const L = window.L
  if (element._leaflet_id) return
  const map = L.map(element, {
    zoomControl: !compact,
    scrollWheelZoom: false,
    attributionControl: !compact,
  })

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap',
  }).addTo(map)

  const markerLatLngs = points.map((point) => [point.lat, point.lng])
  const explicitRouteLatLngs = (routePath ?? []).map((point) => [point.lat, point.lng])
  const lineLatLngs = explicitRouteLatLngs.length
    ? explicitRouteLatLngs
    : routeStart
      ? [[routeStart.lat, routeStart.lng], ...markerLatLngs]
      : markerLatLngs

  points.forEach((point, index) => {
    const markerColor = highlightLast && index === points.length - 1 && points.length > 1 ? ITALY_RED : ITALY_GREEN
    const markerIcon = compact ? dotIcon(L, markerColor) : numberedIcon(L, point.dayNumber ?? index + 1, markerColor)
    const marker = L.marker([point.lat, point.lng], { icon: markerIcon }).addTo(map)
    marker.bindPopup(`<div class="map-popup"><strong dir="${point.direction ?? 'ltr'}">${point.name}</strong>${point.label ? `<span>${point.label}</span>` : ''}${point.href ? `<a href="${point.href}">ליום המלא ←</a>` : ''}</div>`)
  })

  if (showLine && lineLatLngs.length > 1) {
    L.polyline(lineLatLngs, { color: INK, weight: compact ? 2 : 2.5, opacity: 0.48, dashArray: '7 8' }).addTo(map)
  }

  if (lineLatLngs.length === 1) map.setView(lineLatLngs[0], 11)
  else map.fitBounds(lineLatLngs, { padding: compact ? [18, 18] : [36, 36] })
}

function initMapFallbacks(trip) {
  document.querySelectorAll('[data-map-kind]').forEach((element) => {
    const { points, compact } = mapPointsForElement(element, trip)
    element.innerHTML = fallbackMarkup(points, compact)
  })
}

function loadLeaflet() {
  if (window.L) return Promise.resolve(window.L)
  if (leafletLoadPromise) return leafletLoadPromise
  leafletLoadPromise = new Promise((resolve, reject) => {
    const css = document.createElement('link')
    css.rel = 'stylesheet'
    css.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
    document.head.append(css)

    const script = document.createElement('script')
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
    script.async = true
    script.onload = () => resolve(window.L)
    script.onerror = () => reject(new Error('Leaflet could not load'))
    document.head.append(script)
    window.setTimeout(() => reject(new Error('Leaflet load timeout')), 3500)
  })
  return leafletLoadPromise
}

async function enhanceMapsWithLeaflet(trip) {
  try {
    await loadLeaflet()
  } catch {
    return
  }

  document.querySelectorAll('[data-map-kind]').forEach((element) => {
    const { points, compact, routeStart, routePath, highlightLast } = mapPointsForElement(element, trip)
    if (!points.length || !document.body.contains(element)) return
    try {
      element.innerHTML = ''
      createLeafletMap(element, points, { compact, routeStart, routePath, highlightLast })
    } catch (error) {
      console.warn('Map unavailable, keeping fallback.', error)
      element.innerHTML = fallbackMarkup(points, compact)
    }
  })
}

function loadGoogleMaps() {
  const key = getGoogleMapsApiKey()
  if (!key) return Promise.reject(new Error('Google Maps API key is not configured'))
  if (window.google?.maps?.importLibrary) return Promise.resolve(window.google.maps)
  if (googleMapsLoadPromise) return googleMapsLoadPromise

  googleMapsLoadPromise = new Promise((resolve, reject) => {
    const callbackName = '__italyTripGoogleMapsReady'
    const script = document.createElement('script')
    const timeout = window.setTimeout(() => reject(new Error('Google Maps load timeout')), 10000)
    window[callbackName] = () => {
      window.clearTimeout(timeout)
      delete window[callbackName]
      resolve(window.google.maps)
    }
    script.async = true
    script.defer = true
    script.src = `https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(key)}&v=weekly&loading=async&language=he&region=IT&callback=${callbackName}`
    script.onerror = () => {
      window.clearTimeout(timeout)
      delete window[callbackName]
      reject(new Error('Google Maps could not load'))
    }
    document.head.append(script)
  })
  return googleMapsLoadPromise
}

function googleMapMarkerIcon(kind) {
  const optional = kind === 'optional'
  return {
    path: google.maps.SymbolPath.CIRCLE,
    fillColor: markerColorForKind(kind),
    fillOpacity: optional ? 0.52 : 1,
    strokeColor: optional ? '#6E6B67' : '#FFFFFF',
    strokeOpacity: 1,
    strokeWeight: 2,
    scale: 14,
  }
}

function addGoogleMarkers(map, points, { compact = false, day = null } = {}) {
  const infoWindow = new google.maps.InfoWindow()
  points.forEach((point, index) => {
    const kind = markerKindForPoint(point, day)
    const marker = new google.maps.Marker({
      map,
      position: { lat: point.lat, lng: point.lng },
      title: point.name,
      icon: googleMapMarkerIcon(kind),
      label: compact
        ? { text: String(point.dayNumber ?? index + 1), color: '#FFFFFF', fontWeight: '700', fontSize: '11px' }
        : { text: String(point.dayNumber ?? index + 1), color: '#FFFFFF', fontWeight: '700', fontSize: '12px' },
      zIndex: 1000 + index,
    })
    marker.addListener('click', () => {
      const meta = compact && point.dayNumber ? `יום ${point.dayNumber}` : markerCategoryLabel(kind)
      const content = `<div class="google-map-info"><strong>${esc(point.name)}</strong><span>${esc(meta)}${point.label ? ` · ${esc(point.label)}` : ''}</span>${point.href ? `<a href="${esc(point.href)}">ליום המלא ←</a>` : ''}</div>`
      infoWindow.setContent(content)
      infoWindow.open({ map, anchor: marker })
    })
  })
}

function addDirectGooglePolyline(map, points, mode = 'DIRECT', compact = false) {
  if (!points || points.length < 2) return
  const isWalking = mode === 'WALKING'
  const isDrive = mode === 'DRIVING'
  const lineColor = isDrive ? INK : (isWalking ? ITALY_GREEN : MAP_MUTED)
  if (isDrive || isWalking) {
    new google.maps.Polyline({ map, path: points, strokeColor: lineColor, strokeOpacity: 0.58, strokeWeight: compact ? 2 : 3, geodesic: false })
    return
  }
  const dashSymbol = { path: 'M 0,-1 0,1', strokeOpacity: 0.56, strokeColor: lineColor, scale: 3 }
  new google.maps.Polyline({ map, path: points, strokeOpacity: 0, icons: [{ icon: dashSymbol, offset: '0', repeat: compact ? '12px' : '10px' }], geodesic: true })
}

async function addGoogleRouteGroup(map, group, compact = false) {
  if (!['DRIVING', 'WALKING'].includes(group.mode) || group.points.length < 2) {
    addDirectGooglePolyline(map, group.points, group.mode, compact)
    return
  }
  try {
    const { Route } = await google.maps.importLibrary('routes')
    const request = {
      origin: group.points[0],
      destination: group.points[group.points.length - 1],
      travelMode: group.mode,
      fields: ['path'],
    }
    const intermediatePoints = group.points.slice(1, -1)
    if (intermediatePoints.length) request.intermediates = intermediatePoints.map((location) => ({ location }))
    const { routes } = await Route.computeRoutes(request)
    if (!routes?.[0]?.path?.length) throw new Error('No Google route returned')
    new google.maps.Polyline({
      map,
      path: routes[0].path,
      strokeColor: group.mode === 'DRIVING' ? INK : ITALY_GREEN,
      strokeOpacity: 0.72,
      strokeWeight: compact ? 2.5 : 4,
    })
  } catch (error) {
    console.warn(`Google ${group.mode.toLowerCase()} route unavailable; using direct map connection.`, error)
    addDirectGooglePolyline(map, group.points, group.mode, compact)
  }
}

async function createGoogleMap(element, points, { kind = 'day', compact = false, routeStart = null, routePath = null, routeModes = [], day = null } = {}) {
  await loadGoogleMaps()
  const { Map } = await google.maps.importLibrary('maps')
  const first = points[0] ?? routePath?.[0] ?? routeStart ?? { lat: 46.1, lng: 11.2 }
  element.innerHTML = ''
  const map = new Map(element, {
    center: { lat: first.lat, lng: first.lng },
    zoom: compact ? 6 : 10,
    gestureHandling: 'cooperative',
    mapTypeControl: false,
    streetViewControl: false,
    fullscreenControl: !compact,
    clickableIcons: true,
    keyboardShortcuts: false,
  })

  addGoogleMarkers(map, points, { compact, day })

  const explicitPath = routePath?.length ? routePath : (routeStart ? [routeStart, ...points] : points)
  if (kind === 'day') {
    const groups = routeModeGroups(explicitPath, routeModes)
    for (const group of groups) await addGoogleRouteGroup(map, group, compact)
  } else {
    addDirectGooglePolyline(map, explicitPath, 'OVERVIEW', compact)
  }

  const bounds = new google.maps.LatLngBounds()
  points.forEach((point) => bounds.extend(point))
  explicitPath.forEach((point) => bounds.extend(point))
  if (points.length === 1 && explicitPath.length <= 1) map.setZoom(compact ? 9 : 12)
  else if (!bounds.isEmpty()) map.fitBounds(bounds, compact ? 24 : 48)
  return map
}

async function enhanceMapsWithGoogle(trip) {
  await loadGoogleMaps()
  const elements = [...document.querySelectorAll('[data-map-kind]')]
  for (const element of elements) {
    const config = mapPointsForElement(element, trip)
    if (!config.points.length || !document.body.contains(element)) continue
    await createGoogleMap(element, config.points, config)
  }
}

async function enhanceMaps(trip) {
  if (getGoogleMapsApiKey()) {
    try {
      await enhanceMapsWithGoogle(trip)
      return
    } catch (error) {
      console.warn('Google Maps unavailable; falling back to Leaflet.', error)
    }
  }
  await enhanceMapsWithLeaflet(trip)
}

function coordinateString(point) {
  return `${Number(point.lat).toFixed(6)},${Number(point.lng).toFixed(6)}`
}

function navigationGroupsForMode(config, mode) {
  const path = config?.routePath ?? []
  const modes = config?.routeModes ?? []
  if (path.length < 2 || modes.length !== path.length - 1) return []
  const groups = []
  modes.forEach((edgeMode, index) => {
    if (edgeMode !== mode) return
    const from = path[index]
    const to = path[index + 1]
    const current = groups[groups.length - 1]
    if (current && sameMapPoint(current.points[current.points.length - 1], from)) {
      if (!sameMapPoint(current.points[current.points.length - 1], to)) current.points.push(to)
    } else {
      groups.push({ mode, points: [from, to] })
    }
  })
  return groups
}

function navigationGroupsForConfig(config) {
  const driving = navigationGroupsForMode(config, 'DRIVING')
  if (driving.length) return driving
  const transit = navigationGroupsForMode(config, 'TRANSIT')
  if (transit.length) return transit
  return navigationGroupsForMode(config, 'WALKING')
}

function splitNavigationGroup(group, maxWaypoints = 3) {
  const maxPoints = maxWaypoints + 2
  if (group.points.length <= maxPoints) return [group]
  const chunks = []
  let start = 0
  while (start < group.points.length - 1) {
    const points = group.points.slice(start, Math.min(start + maxPoints, group.points.length))
    chunks.push({ mode: group.mode, points })
    if (start + maxPoints >= group.points.length) break
    start += maxPoints - 1
  }
  return chunks
}

function googleMapsDirectionsUrl(group) {
  if (!group?.points?.length || group.points.length < 2) return ''
  const params = new URLSearchParams({
    api: '1',
    origin: coordinateString(group.points[0]),
    destination: coordinateString(group.points[group.points.length - 1]),
    travelmode: group.mode === 'TRANSIT' ? 'transit' : group.mode === 'WALKING' ? 'walking' : 'driving',
    dir_action: 'navigate',
  })
  const waypoints = group.points.slice(1, -1)
  if (waypoints.length) params.set('waypoints', waypoints.map(coordinateString).join('|'))
  return `https://www.google.com/maps/dir/?${params.toString()}`
}

function googleMapsDirectionsUrlsForDay(dayId) {
  const config = dailyMapRoutes[dayId]
  if (!config) return []
  const chunks = navigationGroupsForConfig(config).flatMap((group) => splitNavigationGroup(group, 3))
  const valid = chunks.map((group) => ({ group, url: googleMapsDirectionsUrl(group) })).filter((item) => item.url)
  if (valid.length === 1) return [{ ...valid[0], label: 'פתח מסלול ב-Google Maps' }]
  return valid.map((item, index) => ({ ...item, label: `חלק ${index + 1} ב-Google Maps` }))
}

function googleMapsButtonIcon() {
  return '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a7.5 7.5 0 0 0-7.5 7.5c0 5.3 7.5 12.5 7.5 12.5s7.5-7.2 7.5-12.5A7.5 7.5 0 0 0 12 2Zm0 10.1a2.6 2.6 0 1 1 0-5.2 2.6 2.6 0 0 1 0 5.2Z"/></svg>'
}

function renderGoogleMapsRouteButtons(day) {
  const routes = googleMapsDirectionsUrlsForDay(day.id)
  if (!routes.length) return ''
  return `<div class="map-actions" aria-label="פתיחת המסלול ב-Google Maps">${routes.map((route) => `<a class="google-route-button" href="${esc(route.url)}" target="_blank" rel="noreferrer external">${googleMapsButtonIcon()}<span>${esc(route.label)} ↗</span></a>`).join('')}<small class="google-route-note">הקישור נבנה אוטומטית מנתוני המסלול של היום ומציג את קטעי הניווט הרלוונטיים בלי להפוך הליכה / מעבורת / רכבל לנסיעה ברכב.</small></div>`
}


'''
s = s[:engine_start] + new_engine + s[engine_end:]

# 5) Switch the active-view enhancer to Google-first / Leaflet fallback.
old_init = "  enhanceMapsWithLeaflet(trip)"
new_init = "  enhanceMaps(trip)"
if old_init not in s:
    raise SystemExit('renderApp map enhancer anchor missing')
s = s.replace(old_init, new_init, 1)

p.write_text(s)
