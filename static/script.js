// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize sliders
    initializeSliders();
    
    // Initialize map
    initializeMap();
    
    // Initialize event listeners
    initializeEventListeners();
    
    // Load initial data
    loadInitialData();
}

function initializeSliders() {
    const sliders = ['vegetation', 'builtArea', 'water', 'population'];
    sliders.forEach(sliderId => {
        const slider = document.getElementById(sliderId);
        if (slider) {
            slider.addEventListener('input', updateSliderValue);
            // Set initial values
            updateSliderValue({ target: slider });
        }
    });
}

function initializeMap() {
    // Initialize Leaflet map centered on India
    window.map = L.map('map').setView([20.5937, 78.9629], 5);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(window.map);
    
    // Load heat map data
    loadHeatMapData();
}

function initializeEventListeners() {
    // Photo upload handler
    const photoUpload = document.getElementById('photoUpload');
    if (photoUpload) {
        photoUpload.addEventListener('change', handlePhotoUpload);
    }
    
    // City selection buttons
    const cityButtons = document.querySelectorAll('.city-btn');
    cityButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            cityButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
        });
    });
}

function loadInitialData() {
    // Load initial city data
    selectCity('Bhopal');
}

function updateSliderValue(e) {
    const slider = e.target;
    const value = slider.value;
    const valueElement = document.getElementById(slider.id + 'Value');
    
    if (valueElement) {
        if (slider.id === 'population') {
            valueElement.textContent = parseInt(value).toLocaleString();
        } else {
            valueElement.textContent = value + '%';
        }
    }
}

async function predictTemperature() {
    const vegetation = document.getElementById('vegetation').value / 100;
    const builtArea = document.getElementById('builtArea').value / 100;
    const water = document.getElementById('water').value / 100;
    const population = document.getElementById('population').value;

    // Show loading state
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<p class="loading">Calculating prediction...</p>';
    resultsDiv.classList.add('pulse');

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ 
                vegetation, 
                built_area: builtArea, 
                water, 
                population 
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            throw new Error(data.error || 'Unknown error occurred');
        }
    } catch (error) {
        console.error('Prediction error:', error);
        displayError('Prediction failed: ' + error.message);
    } finally {
        resultsDiv.classList.remove('pulse');
    }
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    const healthDiv = document.getElementById('healthScore');
    const recDiv = document.getElementById('recommendations');
    const factorsDiv = document.getElementById('impactFactors');

    // Temperature results
    resultsDiv.innerHTML = `
        <div class="fade-in">
            <h3>🌡️ ${data.prediction}°C</h3>
            <p class="temperature-interpretation">${data.interpretation}</p>
        </div>
    `;

    // Health score
    healthDiv.innerHTML = `
        <div class="fade-in">
            <h4>🏥 Urban Health Score</h4>
            <div class="score-display">
                <span class="score-value">${data.health_analysis.health_score}/100</span>
                <span class="risk-level ${data.health_analysis.risk_level}">${data.health_analysis.risk_level.toUpperCase()} RISK</span>
            </div>
        </div>
    `;

    // Recommendations
    recDiv.innerHTML = `
        <h4>💡 Recommendations</h4>
        <div class="fade-in">
            ${data.health_analysis.recommendations.map(rec => 
                `<div class="problem-item recommendation-item">${rec}</div>`
            ).join('')}
        </div>
    `;

    // Impact factors
    factorsDiv.innerHTML = `
        <h4>📈 Impact Factors</h4>
        <div class="fade-in">
            ${Object.entries(data.feature_importance).map(([factor, importance]) => `
                <div class="factor-item">
                    <span class="factor-name">${factor.replace('_', ' ')}:</span>
                    <span class="factor-value">${(importance * 100).toFixed(1)}%</span>
                    <div class="factor-bar">
                        <div class="factor-bar-fill" style="width: ${importance * 100}%"></div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;

    // Add CSS for new elements
    addDynamicStyles();
}

function displayError(message) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <div class="error-message">
            <h3>❌ Error</h3>
            <p>${message}</p>
        </div>
    `;
}

async function handlePhotoUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const analysisDiv = document.getElementById('photoAnalysis');
    analysisDiv.innerHTML = '<p class="loading">Analyzing image...</p>';

    try {
        const imageData = await readFileAsDataURL(file);
        
        const response = await fetch('/api/analyze-photo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: imageData })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.success) {
            displayPhotoAnalysis(data);
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
    } catch (error) {
        console.error('Photo analysis error:', error);
        analysisDiv.innerHTML = '<p class="error">Analysis failed. Please try another image.</p>';
    }
}

function readFileAsDataURL(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = e => resolve(e.target.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

function displayPhotoAnalysis(data) {
    const analysisDiv = document.getElementById('photoAnalysis');
    
    analysisDiv.innerHTML = `
        <div class="fade-in">
            <h4>📊 Photo Analysis Results</h4>
            <div class="analysis-grid">
                <div class="analysis-item">
                    <span class="analysis-label">Green Cover:</span>
                    <span class="analysis-value ${data.analysis.green_cover < 20 ? 'low' : 'good'}">
                        ${data.analysis.green_cover}%
                    </span>
                </div>
                <div class="analysis-item">
                    <span class="analysis-label">Built Area:</span>
                    <span class="analysis-value ${data.analysis.built_area > 60 ? 'high' : 'normal'}">
                        ${data.analysis.built_area}%
                    </span>
                </div>
                <div class="analysis-item">
                    <span class="analysis-label">Water Bodies:</span>
                    <span class="analysis-value ${data.analysis.water_cover < 5 ? 'low' : 'good'}">
                        ${data.analysis.water_cover}%
                    </span>
                </div>
            </div>
            
            <h5>💡 Suggestions:</h5>
            <div class="suggestions-list">
                ${data.suggestions.map(suggestion => 
                    `<div class="suggestion-item">${suggestion}</div>`
                ).join('')}
            </div>
        </div>
    `;
}

async function loadHeatMapData() {
    try {
        const response = await fetch('/api/heatmap-data');
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        
        if (data.success) {
            displayHeatMap(data.heatmap_data);
        }
    } catch (error) {
        console.error('Heat map loading failed:', error);
    }
}

function displayHeatMap(heatmapData) {
    // Clear existing markers
    window.map.eachLayer(layer => {
        if (layer instanceof L.CircleMarker) {
            window.map.removeLayer(layer);
        }
    });

    heatmapData.forEach(point => {
        const color = getColorForIntensity(point.intensity);
        const radius = point.intensity * 20 + 5;
        
        const marker = L.circleMarker([point.lat, point.lng], {
            color: color,
            fillColor: color,
            fillOpacity: 0.7,
            radius: radius
        }).addTo(window.map);

        let popupContent = '';
        if (point.city) {
            popupContent += `<strong>${point.city}</strong><br>`;
        }
        if (point.temperature) {
            popupContent += `Temperature: ${point.temperature}°C<br>`;
        }
        if (point.problem) {
            popupContent += `Problem: ${point.problem}<br>`;
            popupContent += `Severity: ${point.severity}`;
        }

        marker.bindPopup(popupContent);
    });
}

function getColorForIntensity(intensity) {
    if (intensity > 0.7) return '#ff4444'; // Red
    if (intensity > 0.4) return '#ffaa00'; // Orange
    return '#ffff00'; // Yellow
}

async function selectCity(cityName) {
    try {
        const response = await fetch(`/api/city-data/${cityName}`);
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        
        if (data.success) {
            displayCityProblems(cityName, data.data);
            // Center map on selected city
            window.map.setView(data.data.center_coordinates, 12);
        }
    } catch (error) {
        console.error('City data loading failed:', error);
    }
}

function displayCityProblems(cityName, cityData) {
    const problemsDiv = document.getElementById('cityProblems');
    
    problemsDiv.innerHTML = `
        <div class="fade-in">
            <div class="city-header">
                <h3>📍 ${cityName}</h3>
                <p class="city-temperature">Current Temperature: ${cityData.temperature}°C</p>
            </div>
            
            <div class="problems-stats">
                <span class="stat-item">${cityData.problems.length} Problems Identified</span>
                <span class="stat-item">Risk Level: ${cityData.health_analysis.risk_level}</span>
            </div>
            
            <div class="problems-list">
                ${cityData.problems.map(problem => `
                    <div class="problem-item severity-${problem.severity}">
                        <div class="problem-header">
                            <strong>${problem.problem}</strong>
                            <span class="severity-badge">${problem.severity}</span>
                        </div>
                        <p class="suggestion">${problem.suggestion}</p>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function addDynamicStyles() {
    // Add dynamic CSS for newly created elements
    if (!document.getElementById('dynamic-styles')) {
        const style = document.createElement('style');
        style.id = 'dynamic-styles';
        style.textContent = `
            .temperature-interpretation {
                font-size: 1.1em;
                font-weight: 600;
                margin-top: 10px;
            }
            
            .score-display {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 10px;
            }
            
            .score-value {
                font-size: 1.5em;
                font-weight: bold;
                color: #4CAF50;
            }
            
            .risk-level {
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.8em;
                font-weight: bold;
            }
            
            .risk-level.high { background: #ff4444; }
            .risk-level.moderate { background: #ffaa00; }
            .risk-level.low { background: #4CAF50; }
            
            .factor-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin: 8px 0;
            }
            
            .factor-bar {
                width: 100px;
                height: 6px;
                background: #ddd;
                border-radius: 3px;
                overflow: hidden;
            }
            
            .factor-bar-fill {
                height: 100%;
                background: var(--nasa-blue);
                transition: width 0.5s ease;
            }
            
            .analysis-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin: 15px 0;
            }
            
            .analysis-item {
                display: flex;
                justify-content: space-between;
            }
            
            .analysis-value.low { color: #ff4444; }
            .analysis-value.high { color: #ffaa00; }
            .analysis-value.good { color: #4CAF50; }
            .analysis-value.normal { color: var(--nasa-white); }
            
            .suggestions-list {
                margin-top: 10px;
            }
            
            .suggestion-item {
                background: rgba(11, 61, 145, 0.3);
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
                border-left: 3px solid var(--nasa-light-blue);
            }
            
            .problem-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
            }
            
            .severity-badge {
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 0.8em;
                font-weight: bold;
            }
            
            .city-header {
                margin-bottom: 15px;
            }
            
            .city-temperature {
                font-size: 1.1em;
                color: var(--nasa-light-blue);
            }
            
            .problems-stats {
                display: flex;
                gap: 20px;
                margin-bottom: 15px;
            }
            
            .stat-item {
                background: rgba(255, 255, 255, 0.1);
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 0.9em;
            }
            
            .loading {
                text-align: center;
                opacity: 0.7;
            }
            
            .error-message {
                color: #ff4444;
                text-align: center;
            }
        `;
        document.head.appendChild(style);
    }
}