let bhopalMap = null;
let currentArea = null;

document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    initializeEventListeners();
});

function initializeMap() {
    // Initialize map centered on Bhopal
    bhopalMap = L.map('bhopal-map').setView([23.2599, 77.4126], 12);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(bhopalMap);

    // Add Bhopal urban areas to map
    addUrbanAreasToMap();
}

function addUrbanAreasToMap() {
    // This would be populated from the backend data
    const urbanAreas = [
        {name: "New Bhopal", coords: [23.2456, 77.4037], type: "residential", color: "#4ECDC4"},
        {name: "Old Bhopal", coords: [23.2650, 77.4030], type: "mixed_use", color: "#FF6B6B"},
        {name: "MP Nagar", coords: [23.2350, 77.4150], type: "commercial", color: "#FFA726"},
        {name: "Shahpura Lake", coords: [23.2286, 77.4382], type: "green_space", color: "#66BB6A"},
        {name: "Railway Station", coords: [23.2696, 77.4350], type: "industrial", color: "#6C63FF"},
        {name: "Bhadbhada Road", coords: [23.2200, 77.4250], type: "industrial", color: "#9575CD"}
    ];

    urbanAreas.forEach(area => {
        L.circleMarker(area.coords, {
            color: area.color,
            fillColor: area.color,
            fillOpacity: 0.7,
            radius: 10
        }).addTo(bhopalMap)
        .bindPopup(`
            <strong>${area.name}</strong><br>
            Type: ${area.type.replace('_', ' ').toUpperCase()}<br>
            <button onclick="analyzeArea('${area.name}')">Analyze Area</button>
        `);
    });
}

function initializeEventListeners() {
    // Add click listeners to area cards
    document.querySelectorAll('.area-card').forEach(card => {
        card.addEventListener('click', function() {
            const areaName = this.getAttribute('data-area');
            analyzeArea(areaName);
        });
    });
}

async function analyzeArea(areaName) {
    // Show loading state
    showAnalysisLoading(true);
    
    try {
        const response = await fetch(`/api/analyze-area/${encodeURIComponent(areaName)}`);
        const data = await response.json();
        
        if (data.success) {
            displayAnalysisResults(data);
            currentArea = data.area;
            
            // Center map on selected area
            if (data.area.coordinates) {
                bhopalMap.setView(data.area.coordinates, 14);
            }
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Analysis error:', error);
        alert('Analysis failed: ' + error.message);
    } finally {
        showAnalysisLoading(false);
    }
}

function displayAnalysisResults(data) {
    const resultsDiv = document.getElementById('analysis-results');
    const placeholder = document.querySelector('.placeholder');
    
    placeholder.classList.add('hidden');
    resultsDiv.classList.remove('hidden');
    
    // Update temperature display
    document.getElementById('predicted-temp').textContent = data.prediction + '°C';
    document.getElementById('temp-interpretation').textContent = data.interpretation;
    
    // Update health score
    document.getElementById('health-score').textContent = data.health_analysis.health_score;
    
    // Update risk level
    const riskLevelElement = document.getElementById('risk-level');
    riskLevelElement.textContent = data.health_analysis.risk_level.toUpperCase();
    riskLevelElement.className = 'risk-' + data.health_analysis.risk_level;
    
    // Update recommendations
    const recommendationsList = document.getElementById('recommendations-list');
    recommendationsList.innerHTML = data.health_analysis.recommendations
        .map(rec => `<div class="recommendation-item">${rec}</div>`)
        .join('');
}

function showAnalysisLoading(show) {
    const resultsContainer = document.getElementById('results-container');
    if (show) {
        resultsContainer.innerHTML = '<div class="placeholder"><p>🔍 Analyzing area...</p></div>';
    }
}

// Add some interactive effects
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to area cards
    const areaCards = document.querySelectorAll('.area-card');
    areaCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.3)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
    
    // Add animation to heat points
    const heatPoints = document.querySelectorAll('.heat-point');
    heatPoints.forEach(point => {
        point.style.transition = 'all 0.3s ease';
        point.addEventListener('mouseenter', function() {
            this.style.transform = 'translate(-50%, -50%) scale(1.2)';
        });
        point.addEventListener('mouseleave', function() {
            this.style.transform = 'translate(-50%, -50%) scale(1)';
        });
    });
});

// Simple temperature prediction for demonstration
function quickPredict(vegetation, builtArea, water, population) {
    // Simple formula for demonstration
    const baseTemp = 22;
    const effect = (-6 * vegetation) + (8 * builtArea) + (-4 * water) + (population * 0.0002);
    return Math.max(15, Math.min(45, baseTemp + effect));
}