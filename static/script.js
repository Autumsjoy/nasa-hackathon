let selectionMap = null;
let currentMarker = null;
let currentAnalysis = null;

document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    setupEventListeners();
});

function initializeMap() {
    selectionMap = L.map('selection-map').setView([23.2599, 77.4126], 6);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(selectionMap);

    selectionMap.on('click', function(e) {
        analyzeMapLocation(e.latlng.lat, e.latlng.lng);
    });
}

function setupEventListeners() {
    document.getElementById('citySelect').addEventListener('change', function() {
        const city = this.value;
        if (city) navigateToCity(city);
    });

    document.getElementById('photoUpload').addEventListener('change', handlePhotoUpload);
}

async function analyzeMapLocation(lat, lng) {
    const areaType = document.getElementById('areaTypeSelect').value;
    
    showAnalysisLoading(true);

    try {
        const response = await fetch('/api/analyze-location', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ lat, lng, area_type: areaType })
        });

        const data = await response.json();
        
        if (data.success) {
            displayLocationAnalysis(data.analysis, data.suggestions);
            addLocationMarker(lat, lng, data.analysis.area_type);
            currentAnalysis = data.analysis;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        alert('Analysis failed: ' + error.message);
    } finally {
        showAnalysisLoading(false);
    }
}

function addLocationMarker(lat, lng, areaType) {
    if (currentMarker) {
        selectionMap.removeLayer(currentMarker);
    }

    currentMarker = L.marker([lat, lng]).addTo(selectionMap)
        .bindPopup(`<b>${areaType.toUpperCase()}</b><br>Lat: ${lat.toFixed(4)}, Lng: ${lng.toFixed(4)}`)
        .openPopup();
}

function displayLocationAnalysis(analysis, suggestions) {
    const analysisDiv = document.getElementById('location-analysis');
    analysisDiv.classList.remove('hidden');

    document.getElementById('analyzed-area-type').textContent = analysis.area_type.toUpperCase();
    document.getElementById('analyzed-vegetation').textContent = (analysis.vegetation * 100).toFixed(1) + '%';
    document.getElementById('analyzed-built-area').textContent = (analysis.built_area * 100).toFixed(1) + '%';
    document.getElementById('analyzed-water').textContent = (analysis.water * 100).toFixed(1) + '%';
    document.getElementById('analyzed-population').textContent = analysis.population.toLocaleString() + '/km²';
    document.getElementById('analysis-confidence').textContent = (analysis.confidence * 100).toFixed(0) + '% confidence';

    const suggestionsDiv = document.getElementById('area-suggestions');
    suggestionsDiv.innerHTML = suggestions.map(s => `<div class="suggestion">${s}</div>`).join('');
}

function showAnalysisLoading(show) {
    const instruction = document.querySelector('.click-instruction');
    instruction.textContent = show ? '🔍 Analyzing location...' : '📍 Click anywhere on the map to analyze urban configuration';
}

async function predictFromMapAnalysis() {
    if (!currentAnalysis) {
        alert('Please analyze a location first!');
        return;
    }

    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<p>Predicting temperature impact...</p>';

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentAnalysis)
        });

        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        alert('Prediction failed: ' + error.message);
    }
}

function displayResults(data) {
    document.getElementById('results').innerHTML = `
        <h3>🌡️ ${data.prediction}°C</h3>
        <p>${data.interpretation}</p>
    `;

    document.getElementById('healthScore').innerHTML = `
        <h4>🏥 Urban Health Score: ${data.health_analysis.health_score}/100</h4>
        <p>Risk Level: ${data.health_analysis.risk_level}</p>
    `;

    document.getElementById('recommendations').innerHTML = `
        <h4>💡 Recommendations</h4>
        ${data.health_analysis.recommendations.map(r => `<div class="recommendation">${r}</div>`).join('')}
    `;
}

function navigateToCity(city) {
    const cities = {
        'Bhopal': [23.2599, 77.4126],
        'Delhi': [28.6139, 77.2090],
        'Mumbai': [19.0760, 72.8777]
    };

    const coords = cities[city];
    selectionMap.setView(coords, 12);
    
    setTimeout(() => analyzeMapLocation(coords[0], coords[1]), 500);
}

async function handlePhotoUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const analysisDiv = document.getElementById('photoAnalysis');
    analysisDiv.innerHTML = '<p>Analyzing photo...</p>';

    const reader = new FileReader();
    reader.onload = async function(e) {
        try {
            const response = await fetch('/api/analyze-photo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: e.target.result })
            });

            const data = await response.json();
            
            if (data.success) {
                analysisDiv.innerHTML = `
                    <h4>Photo Analysis</h4>
                    <p>Green Cover: ${data.analysis.green_cover}%</p>
                    <p>Built Area: ${data.analysis.built_area}%</p>
                    <p>Water Bodies: ${data.analysis.water_cover}%</p>
                    <h5>Suggestions:</h5>
                    ${data.suggestions.map(s => `<p>${s}</p>`).join('')}
                `;
            }
        } catch (error) {
            analysisDiv.innerHTML = '<p>Analysis failed</p>';
        }
    };
    reader.readAsDataURL(file);
}