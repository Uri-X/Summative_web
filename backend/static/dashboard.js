// ── Helpers ──────────────────────────────────────────────────────────────────

function showError(sectionId, message) {
    const el = document.getElementById(sectionId);
    if (el) el.innerHTML = `<p style="color:red;padding:10px;">⚠️ ${message}</p>`;
}

// ── 1. Summary KPI Cards ──────────────────────────────────────────────────────

fetch('/trips/summary')
    .then(res => res.json())
    .then(data => {
        document.getElementById('val-total').textContent =
            Number(data.total_trips).toLocaleString();
        document.getElementById('val-fare').textContent =
            '$' + data.avg_fare;
        document.getElementById('val-distance').textContent =
            data.avg_distance + ' mi';
        document.getElementById('val-duration').textContent =
            data.avg_duration + ' min';
        document.getElementById('val-speed').textContent =
            data.avg_speed !== null ? data.avg_speed + ' mph' : 'N/A';
    })
    .catch(() => showError('summary-cards', 'Could not load summary data.'));


// ── 2. Trips by Hour (Line Chart) ─────────────────────────────────────────────

fetch('/trips/by-hour')
    .then(res => res.json())
    .then(data => {
        const labels = data.map(d => d.hour + ':00');
        const counts = data.map(d => d.trip_count);
        const fares  = data.map(d => d.avg_fare);

        const ctx = document.getElementById('hourChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels,
                datasets: [
                    {
                        label: 'Number of Trips',
                        data: counts,
                        borderColor: '#e94560',
                        backgroundColor: 'rgba(233,69,96,0.1)',
                        yAxisID: 'y',
                        tension: 0.4,
                        fill: true,
                    },
                    {
                        label: 'Avg Fare ($)',
                        data: fares,
                        borderColor: '#1a1a2e',
                        backgroundColor: 'rgba(26,26,46,0.08)',
                        yAxisID: 'y1',
                        tension: 0.4,
                        fill: false,
                    }
                ]
            },
            options: {
                responsive: true,
                interaction: { mode: 'index', intersect: false },
                scales: {
                    y:  { type: 'linear', position: 'left',  title: { display: true, text: 'Trip Count' } },
                    y1: { type: 'linear', position: 'right', title: { display: true, text: 'Avg Fare ($)' }, grid: { drawOnChartArea: false } }
                }
            }
        });
    })
    .catch(() => showError('hourChart', 'Could not load hourly data.'));


// ── 3. Trips by Borough (Bar Chart) ──────────────────────────────────────────

fetch('/trips/by-borough')
    .then(res => res.json())
    .then(data => {
        const labels   = data.map(d => d.Borough);
        const counts   = data.map(d => d.trip_count);
        const avgFares = data.map(d => d.avg_fare);

        const colors = ['#e94560','#0f3460','#533483','#e94560','#16213e','#1a1a2e'];

        const ctx = document.getElementById('boroughChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels,
                datasets: [
                    {
                        label: 'Trip Count',
                        data: counts,
                        backgroundColor: colors,
                        yAxisID: 'y',
                    },
                    {
                        label: 'Avg Fare ($)',
                        data: avgFares,
                        type: 'line',
                        borderColor: '#e94560',
                        backgroundColor: 'transparent',
                        yAxisID: 'y1',
                        tension: 0.4,
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y:  { title: { display: true, text: 'Trip Count' } },
                    y1: { position: 'right', title: { display: true, text: 'Avg Fare ($)' }, grid: { drawOnChartArea: false } }
                }
            }
        });
    })
    .catch(() => showError('boroughChart', 'Could not load borough data.'));


// ── 4. Top 10 Pickup Zones (Horizontal Bar) ───────────────────────────────────

fetch('/trips/top-zones')
    .then(res => res.json())
    .then(data => {
        const labels = data.map(d => d.Zone);
        const counts = data.map(d => d.trip_count);

        const ctx = document.getElementById('zonesChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: 'Trip Count',
                    data: counts,
                    backgroundColor: 'rgba(233,69,96,0.75)',
                    borderColor: '#e94560',
                    borderWidth: 1,
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    x: { title: { display: true, text: 'Number of Trips' } }
                }
            }
        });
    })
    .catch(() => showError('zonesChart', 'Could not load zone data.'));


// ── 5. Leaflet Map with Zone Markers ─────────────────────────────────────────

fetch('/zones')
    .then(res => res.json())
    .then(zones => {
        const map = L.map('zones-map').setView([40.7128, -74.0060], 10);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Borough centre coordinates for rough positioning
        const boroughCoords = {
            'Manhattan':    [40.7831, -73.9712],
            'Brooklyn':     [40.6782, -73.9442],
            'Queens':       [40.7282, -73.7949],
            'Bronx':        [40.8448, -73.8648],
            'Staten Island':[40.5795, -74.1502],
            'EWR':          [40.6895, -74.1745],
        };

        const boroughColors = {
            'Manhattan': '#e94560',
            'Brooklyn':  '#0f3460',
            'Queens':    '#533483',
            'Bronx':     '#16213e',
            'Staten Island': '#1a1a2e',
            'EWR':       '#888',
        };

        // Group zones by borough and add one marker per borough with a popup listing zones
        const byBorough = {};
        zones.forEach(z => {
            const b = z.Borough || 'Unknown';
            if (!byBorough[b]) byBorough[b] = [];
            byBorough[b].push(z.Zone);
        });

        Object.entries(byBorough).forEach(([borough, zoneList]) => {
            const coords = boroughCoords[borough];
            if (!coords) return;

            const color = boroughColors[borough] || '#888';
            const marker = L.circleMarker(coords, {
                radius: 14,
                fillColor: color,
                color: '#fff',
                weight: 2,
                opacity: 1,
                fillOpacity: 0.85
            }).addTo(map);

            const zoneItems = zoneList.slice(0, 15).map(z => `<li>${z}</li>`).join('');
            const more = zoneList.length > 15 ? `<li>...and ${zoneList.length - 15} more</li>` : '';
            marker.bindPopup(`
                <strong>${borough}</strong><br>
                ${zoneList.length} zones:<br>
                <ul style="padding-left:16px;margin-top:4px;max-height:150px;overflow-y:auto;">
                    ${zoneItems}${more}
                </ul>
            `);

            marker.bindTooltip(borough, { permanent: true, direction: 'top', className: 'borough-label' });
        });
    })
    .catch(() => showError('zones-map', 'Could not load map data.'));