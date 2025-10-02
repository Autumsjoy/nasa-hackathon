// NASA Urban Analysis Dashboard - Main JavaScript
class NASAUrbanDashboard {
    constructor() {
        this.currentArea = 'old_bhopal';
        this.currentTab = 'nasa-overview';
        this.charts = {};
        this.areasData = {};
        this.init();
    }

    async init() {
        await this.loadNASAData();
        this.setupEventListeners();
        await this.loadAreaAnalysis(this.currentArea);
        await this.loadComparativeAnalysis();
        this.generateNASAHeatMap();
    }

    async loadNASAData() {
        try {
            // Load areas data
            const areasResponse = await fetch('/api/areas');
            this.areasData = await areasResponse.json();
            this.renderAreaCards();
            
            // Load NASA urban heat data
            const nasaResponse = await fetch('/api/nasa/urban-heat');
            this.nasaData = await nasaResponse.json();
            
        } catch (error) {
            console.error('Error loading NASA data:', error);
            this.showError('Failed to load NASA satellite data');
        }
    }

    renderAreaCards() {
        const container = document.querySelector('.area-selector');
        let html = '<h2><i class="fas fa-satellite"></i> Urban Areas</h2>';
        
        Object.entries(this.areasData).forEach(([id, area]) => {
            const sustainabilityScore = area.environmental_data.sustainability_score;
            const scoreColor = this.getSustainabilityColor(sustainabilityScore);
            
            html += `
                <div class="area-card ${id === this.currentArea ? 'active' : ''}" data-area="${id}">
                    <div class="area-title">
                        <i class="fas fa-${this.getAreaIcon(id)}"></i> ${area.name}
                    </div>
                    <div class="area-type">${area.type}</div>
                    
                    <div class="area-stats">
                        <div class="stat">
                            <span class="stat-value">${area.nasa_metrics.surface_temperature}°C</span>
                            <span class="stat-label">Surface Temp</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">${area.nasa_metrics.vegetation_health.toFixed(2)}</span>
                            <span class="stat-label">Vegetation</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">${area.environmental_data.green_cover}%</span>
                            <span class="stat-label">Green Cover</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value" style="color: ${scoreColor}">${sustainabilityScore}</span>
                            <span class="stat-label">NASA Score</span>
                        </div>
                    </div>
                    
                    <div class="nasa-metrics">
                        <div class="metric-item">
                            <span>Heat Index:</span>
                            <span class="metric-value">+${area.nasa_metrics.urban_heat_index}°C</span>
                        </div>
                        <div class="metric-item">
                            <span>Air Quality:</span>
                            <span class="metric-value">${area.nasa_metrics.air_quality_index} AQI</span>
                        </div>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
        
        // Add event listeners
        document.querySelectorAll('.area-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const areaId = e.currentTarget.dataset.area;
                this.selectArea(areaId);
            });
        });
    }

    getAreaIcon(areaId) {
        const icons = {
            'old_bhopal': 'building',
            'new_bhopal': 'city',
            'shahpura': 'home',
            'kolar': 'subway',
            'indrapuri': 'tree-city',
            'bhopal_lake': 'water',
            'industrial_area': 'industry'
        };
        return icons[areaId] || 'map-marker-alt';
    }

    getSustainabilityColor(score) {
        if (score >= 80) return '#4CAF50';
        if (score >= 60) return '#FFC107';
        if (score >= 40) return '#FF9800';
        return '#F44336';
    }

    async selectArea(areaId) {
        this.currentArea = areaId;
        
        // Update UI
        document.querySelectorAll('.area-card').forEach(card => {
            card.classList.remove('active');
        });
        document.querySelector(`[data-area="${areaId}"]`).classList.add('active');
        
        // Load area analysis
        await this.loadAreaAnalysis(areaId);
    }

    async loadAreaAnalysis(areaId) {
        this.showNASALoading('analysis-content');
        
        try {
            const response = await fetch(`/api/area/${areaId}`);
            const analysis = await response.json();
            
            if (analysis.error) {
                this.showError(analysis.error);
                return;
            }
            
            this.renderAreaAnalysis(analysis);
            this.updatePanelHeader(analysis.area_info);
            
        } catch (error) {
            console.error('Error loading area analysis:', error);
            this.showError('Failed to load area analysis data');
        }
    }

    updatePanelHeader(areaInfo) {
        document.querySelector('.panel-title').innerHTML = `
            <i class="fas fa-satellite-dish"></i> ${areaInfo.name} - NASA Analysis
        `;
    }

    renderAreaAnalysis(analysis) {
        const areaInfo = analysis.area_info;
        
        // Update all tabs
        this.renderNASAOverview(analysis);
        this.renderHeatIslandAnalysis(analysis);
        this.renderEnvironmentalImpact(analysis);
        this.renderEnergyAnalysis(analysis);
        this.renderTransportationAnalysis(analysis);
        this.renderNASARecommendations(analysis);
        
        // Show current tab
        this.showTab(this.currentTab);
    }

    renderNASAOverview(analysis) {
        const container = document.getElementById('nasa-overview-tab');
        const areaInfo = analysis.area_info;
        const nasaAnalysis = analysis.nasa_analysis;
        
        let html = `
            <div class="nasa-stats-grid">
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-temperature-high"></i>
                    </div>
                    <div class="nasa-stat-value">${areaInfo.nasa_metrics.surface_temperature}°C</div>
                    <div class="nasa-stat-label">Surface Temperature</div>
                </div>
                
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-leaf"></i>
                    </div>
                    <div class="nasa-stat-value">${(areaInfo.nasa_metrics.vegetation_health * 100).toFixed(0)}%</div>
                    <div class="nasa-stat-label">Vegetation Health</div>
                </div>
                
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-wind"></i>
                    </div>
                    <div class="nasa-stat-value">${areaInfo.nasa_metrics.air_quality_index}</div>
                    <div class="nasa-stat-label">Air Quality Index</div>
                </div>
                
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <div class="nasa-stat-value" style="color: ${this.getSustainabilityColor(areaInfo.environmental_data.sustainability_score)}">
                        ${areaInfo.environmental_data.sustainability_score}
                    </div>
                    <div class="nasa-stat-label">NASA Sustainability Score</div>
                </div>
            </div>

            <div class="nasa-chart-container">
                <canvas id="nasaOverviewChart"></canvas>
            </div>

            <h3><i class="fas fa-satellite"></i> NASA Satellite Insights</h3>
            <div class="nasa-insights">
                ${areaInfo.nasa_insights.map(insight => `
                    <div class="nasa-recommendation-card">
                        <div class="rec-icon">
                            <i class="fas fa-rocket"></i>
                        </div>
                        <div class="rec-title">Satellite Observation</div>
                        <div class="rec-desc">${insight}</div>
                    </div>
                `).join('')}
            </div>

            <div class="nasa-data-source">
                <p><i class="fas fa-database"></i> <strong>Data Source:</strong> ${this.nasaData.source}</p>
                <p><i class="fas fa-clock"></i> <strong>Last Updated:</strong> ${new Date(this.nasaData.last_updated).toLocaleDateString()}</p>
            </div>
        `;
        
        container.innerHTML = html;
        this.createNASAOverviewChart(areaInfo);
    }

    createNASAOverviewChart(areaInfo) {
        const ctx = document.getElementById('nasaOverviewChart').getContext('2d');
        
        if (this.charts.overview) {
            this.charts.overview.destroy();
        }
        
        this.charts.overview = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Temperature', 'Vegetation', 'Air Quality', 'Energy', 'Transport', 'Sustainability'],
                datasets: [{
                    label: `${areaInfo.name} Metrics`,
                    data: [
                        (40 - areaInfo.nasa_metrics.surface_temperature) * 3,
                        areaInfo.nasa_metrics.vegetation_health * 100,
                        100 - (areaInfo.nasa_metrics.air_quality_index / 3),
                        areaInfo.energy_consumption.solar_energy,
                        100 - areaInfo.transportation.private_vehicles,
                        areaInfo.environmental_data.sustainability_score
                    ],
                    backgroundColor: 'rgba(252, 61, 33, 0.2)',
                    borderColor: '#FC3D21',
                    pointBackgroundColor: '#FC3D21',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#FC3D21'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'NASA Urban Sustainability Metrics',
                        color: '#fff',
                        font: { size: 16 }
                    },
                    legend: {
                        labels: { color: '#fff' }
                    }
                },
                scales: {
                    r: {
                        angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        pointLabels: { color: '#4facfe' },
                        ticks: { 
                            color: '#fff',
                            backdropColor: 'transparent'
                        }
                    }
                }
            }
        });
    }

    renderHeatIslandAnalysis(analysis) {
        const container = document.getElementById('heat-island-tab');
        const areaInfo = analysis.area_info;
        const heatAnalysis = analysis.nasa_analysis.urban_heat_island;
        
        let html = `
            <div class="nasa-stats-grid">
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-thermometer-full"></i>
                    </div>
                    <div class="nasa-stat-value">${heatAnalysis.effect_level}</div>
                    <div class="nasa-stat-label">Heat Island Effect</div>
                </div>
                
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-arrow-up"></i>
                    </div>
                    <div class="nasa-stat-value">${heatAnalysis.temperature_impact}</div>
                    <div class="nasa-stat-label">Temperature Impact</div>
                </div>
                
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-seedling"></i>
                    </div>
                    <div class="nasa-stat-value">${heatAnalysis.mitigation_potential}</div>
                    <div class="nasa-stat-label">Mitigation Potential</div>
                </div>
                
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-sun"></i>
                    </div>
                    <div class="nasa-stat-value">${areaInfo.nasa_metrics.urban_heat_index}°C</div>
                    <div class="nasa-stat-label">Urban Heat Index</div>
                </div>
            </div>

            <div class="nasa-chart-container">
                <canvas id="heatIslandChart"></canvas>
            </div>

            <h3><i class="fas fa-fire"></i> Heat Island Analysis</h3>
            <p>NASA satellite data reveals significant urban heat island effect in ${areaInfo.name}. 
            The area experiences temperatures ${heatAnalysis.temperature_impact} compared to surrounding rural areas.</p>
            
            <div class="nasa-recommendations">
                <div class="nasa-recommendation-card">
                    <div class="rec-icon">
                        <i class="fas fa-paint-roller"></i>
                    </div>
                    <div class="rec-title">Cool Roof Implementation</div>
                    <div class="rec-desc">Deploy NASA-developed reflective materials to reduce heat absorption by 40%</div>
                </div>
                
                <div class="nasa-recommendation-card">
                    <div class="rec-icon">
                        <i class="fas fa-tree"></i>
                    </div>
                    <div class="rec-title">Urban Greening</div>
                    <div class="rec-desc">Increase green cover based on NASA vegetation analysis to create cooling corridors</div>
                </div>
                
                <div class="nasa-recommendation-card">
                    <div class="rec-icon">
                        <i class="fas fa-water"></i>
                    </div>
                    <div class="rec-title">Water Features</div>
                    <div class="rec-desc">Implement evaporative cooling systems using NASA hydrological data</div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
        this.createHeatIslandChart(areaInfo);
    }

    createHeatIslandChart(areaInfo) {
        const ctx = document.getElementById('heatIslandChart').getContext('2d');
        
        if (this.charts.heatIsland) {
            this.charts.heatIsland.destroy();
        }
        
        this.charts.heatIsland = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['6 AM', '9 AM', '12 PM', '3 PM', '6 PM', '9 PM'],
                datasets: [{
                    label: `${areaInfo.name} Temperature`,
                    data: [26, 30, areaInfo.nasa_metrics.surface_temperature, 36, 32, 28],
                    backgroundColor: 'rgba(252, 61, 33, 0.8)',
                    borderColor: '#FC3D21',
                    borderWidth: 2
                }, {
                    label: 'Rural Reference',
                    data: [24, 27, 29, 30, 28, 25],
                    backgroundColor: 'rgba(79, 172, 254, 0.8)',
                    borderColor: '#4facfe',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Urban vs Rural Temperature Comparison',
                        color: '#fff'
                    },
                    legend: {
                        labels: { color: '#fff' }
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#fff' }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#fff' },
                        title: {
                            display: true,
                            text: 'Temperature (°C)',
                            color: '#fff'
                        }
                    }
                }
            }
        });
    }

    renderEnvironmentalImpact(analysis) {
        const container = document.getElementById('environmental-tab');
        const areaInfo = analysis.area_info;
        const envAnalysis = analysis.nasa_analysis.environmental_impact;
        
        let html = `
            <div class="nasa-stats-grid">
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-tree"></i>
                    </div>
                    <div class="nasa-stat-value">${envAnalysis.vegetation_status}</div>
                    <div class="nasa-stat-label">Vegetation Status</div>
                </div>
                
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-wind"></i>
                    </div>
                    <div class="nasa-stat-value">${envAnalysis.air_quality_status}</div>
                    <div class="nasa-stat-label">Air Quality</div>
                </div>
                
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-footprint"></i>
                    </div>
                    <div class="nasa-stat-value">${envAnalysis.carbon_footprint}t</div>
                    <div class="nasa-stat-label">Carbon Footprint</div>
                </div>
                
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-recycle"></i>
                    </div>
                    <div class="nasa-stat-value">${areaInfo.environmental_data.green_cover}%</div>
                    <div class="nasa-stat-label">Green Cover</div>
                </div>
            </div>

            <div class="nasa-chart-container">
                <canvas id="environmentalChart"></canvas>
            </div>

            <h3><i class="fas fa-globe-americas"></i> Environmental Impact Assessment</h3>
            <p>NASA environmental monitoring shows ${areaInfo.name} has ${envAnalysis.vegetation_status.toLowerCase()} vegetation 
            and ${envAnalysis.air_quality_status.toLowerCase()} air quality.</p>
        `;
        
        container.innerHTML = html;
        this.createEnvironmentalChart(areaInfo);
    }

    createEnvironmentalChart(areaInfo) {
        const ctx = document.getElementById('environmentalChart').getContext('2d');
        
        if (this.charts.environmental) {
            this.charts.environmental.destroy();
        }
        
        this.charts.environmental = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Green Areas', 'Built-up Areas', 'Water Bodies', 'Barren Land'],
                datasets: [{
                    data: [
                        areaInfo.environmental_data.green_cover,
                        100 - areaInfo.environmental_data.green_cover - 5,
                        3,
                        2
                    ],
                    backgroundColor: [
                        '#4CAF50',
                        '#FF9800',
                        '#2196F3',
                        '#795548'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Land Use Distribution',
                        color: '#fff'
                    },
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#fff',
                            padding: 20
                        }
                    }
                }
            }
        });
    }

    renderEnergyAnalysis(analysis) {
        const container = document.getElementById('energy-tab');
        const areaInfo = analysis.area_info;
        
        let html = `
            <div class="nasa-stats-grid">
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-bolt"></i>
                    </div>
                    <div class="nasa-stat-value">${areaInfo.energy_consumption.grid_electricity}%</div>
                    <div class="nasa-stat-label">Grid Electricity</div>
                </div>
                
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-solar-panel"></i>
                    </div>
                    <div class="nasa-stat-value">${areaInfo.energy_consumption.solar_energy}%</div>
                    <div class="nasa-stat-label">Solar Energy</div>
                </div>
                
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-car-battery"></i>
                    </div>
                    <div class="nasa-stat-value">${areaInfo.energy_consumption.battery_storage}%</div>
                    <div class="nasa-stat-label">Storage</div>
                </div>
                
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-smog"></i>
                    </div>
                    <div class="nasa-stat-value">${areaInfo.energy_consumption.carbon_footprint}t</div>
                    <div class="nasa-stat-label">CO2/Year</div>
                </div>
            </div>

            <div class="nasa-chart-container">
                <canvas id="energyChart"></canvas>
            </div>

            <h3><i class="fas fa-charging-station"></i> Energy Consumption Analysis</h3>
            <p>Current energy mix shows ${areaInfo.energy_consumption.solar_energy}% renewable energy usage with 
            a carbon footprint of ${areaInfo.energy_consumption.carbon_footprint} tons CO2 equivalent annually.</p>
        `;
        
        container.innerHTML = html;
        this.createEnergyChart(areaInfo);
    }

    createEnergyChart(areaInfo) {
        const ctx = document.getElementById('energyChart').getContext('2d');
        
        if (this.charts.energy) {
            this.charts.energy.destroy();
        }
        
        this.charts.energy = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Grid Electricity', 'Solar Energy', 'Battery Storage', 'Generator Backup'],
                datasets: [{
                    data: [
                        areaInfo.energy_consumption.grid_electricity,
                        areaInfo.energy_consumption.solar_energy,
                        areaInfo.energy_consumption.battery_storage,
                        areaInfo.energy_consumption.generator_backup
                    ],
                    backgroundColor: [
                        '#FF9800',
                        '#FFC107',
                        '#4CAF50',
                        '#F44336'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Energy Consumption Sources',
                        color: '#fff'
                    },
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#fff',
                            padding: 20
                        }
                    }
                }
            }
        });
    }

    renderTransportationAnalysis(analysis) {
        const container = document.getElementById('transportation-tab');
        const areaInfo = analysis.area_info;
        
        let html = `
            <div class="nasa-stats-grid">
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-car"></i>
                    </div>
                    <div class="nasa-stat-value">${areaInfo.transportation.private_vehicles}%</div>
                    <div class="nasa-stat-label">Private Vehicles</div>
                </div>
                
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-bus"></i>
                    </div>
                    <div class="nasa-stat-value">${areaInfo.transportation.public_transport}%</div>
                    <div class="nasa-stat-label">Public Transport</div>
                </div>
                
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-bicycle"></i>
                    </div>
                    <div class="nasa-stat-value">${areaInfo.transportation.walking_cycling}%</div>
                    <div class="nasa-stat-label">Active Mobility</div>
                </div>
                
                <div class="nasa-stat-card">
                    <div class="nasa-stat-icon">
                        <i class="fas fa-traffic-light"></i>
                    </div>
                    <div class="nasa-stat-value">${areaInfo.transportation.congestion_level}</div>
                    <div class="nasa-stat-label">Congestion</div>
                </div>
            </div>

            <div class="nasa-chart-container">
                <canvas id="transportationChart"></canvas>
            </div>

            <h3><i class="fas fa-route"></i> Transportation Analysis</h3>
            <p>Current transportation patterns show ${areaInfo.transportation.private_vehicles}% dependency on private vehicles 
            with ${areaInfo.transportation.congestion_level.toLowerCase()} traffic congestion levels.</p>
        `;
        
        container.innerHTML = html;
        this.createTransportationChart(areaInfo);
    }

    createTransportationChart(areaInfo) {
        const ctx = document.getElementById('transportationChart').getContext('2d');
        
        if (this.charts.transportation) {
            this.charts.transportation.destroy();
        }
        
        this.charts.transportation = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Private Vehicles', 'Public Transport', 'Two-wheelers', 'Walking/Cycling'],
                datasets: [{
                    label: 'Mode Share (%)',
                    data: [
                        areaInfo.transportation.private_vehicles,
                        areaInfo.transportation.public_transport,
                        areaInfo.transportation.two_wheelers,
                        areaInfo.transportation.walking_cycling
                    ],
                    backgroundColor: [
                        '#FC3D21',
                        '#4facfe',
                        '#FFC107',
                        '#4CAF50'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Transportation Mode Distribution',
                        color: '#fff'
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#fff' }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#fff' },
                        max: 100
                    }
                }
            }
        });
    }

    renderNASARecommendations(analysis) {
        const container = document.getElementById('recommendations-tab');
        const recommendations = analysis.recommendations;
        
        let html = `
            <h3><i class="fas fa-rocket"></i> NASA-Recommended Solutions</h3>
            <p>Based on satellite data analysis and urban sustainability metrics, the following interventions are recommended:</p>
            
            <div class="nasa-recommendations">
                ${recommendations.map((rec, index) => `
                    <div class="nasa-recommendation-card">
                        <div class="rec-icon">
                            <i class="fas fa-${this.getRecommendationIcon(rec)}"></i>
                        </div>
                        <div class="rec-title">Solution ${index + 1}</div>
                        <div class="rec-desc">${rec}</div>
                    </div>
                `).join('')}
            </div>
            
            <div class="nasa-implementation-timeline">
                <h4><i class="fas fa-calendar-alt"></i> Implementation Timeline</h4>
                <div class="timeline">
                    <div class="timeline-item">
                        <div class="timeline-date">Short-term (0-6 months)</div>
                        <div class="timeline-content">Immediate heat mitigation and awareness campaigns</div>
                    </div>
                    <div class="timeline-item">
                        <div class="timeline-date">Medium-term (6-18 months)</div>
                        <div class="timeline-content">Infrastructure upgrades and renewable energy deployment</div>
                    </div>
                    <div class="timeline-item">
                        <div class="timeline-date">Long-term (18+ months)</div>
                        <div class="timeline-content">Sustainable urban transformation and smart city integration</div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    getRecommendationIcon(recommendation) {
        if (recommendation.includes('roof') || recommendation.includes('cool')) return 'paint-roller';
        if (recommendation.includes('solar') || recommendation.includes('energy')) return 'solar-panel';
        if (recommendation.includes('transport') || recommendation.includes('vehicle')) return 'bus';
        if (recommendation.includes('green') || recommendation.includes('tree')) return 'tree';
        if (recommendation.includes('air') || recommendation.includes('purification')) return 'wind';
        return 'lightbulb';
    }

    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('.nasa-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const tabName = e.currentTarget.dataset.tab;
                this.showTab(tabName);
            });
        });
    }

    showTab(tabName) {
        this.currentTab = tabName;
        
        // Update active tab
        document.querySelectorAll('.nasa-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        
        // Show corresponding content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
    }

    async loadComparativeAnalysis() {
        try {
            const response = await fetch('/api/comparison');
            this.comparisonData = await response.json();
            this.createComparisonChart();
            this.updateComparisonTable();
        } catch (error) {
            console.error('Error loading comparative data:', error);
        }
    }

    createComparisonChart() {
        const ctx = document.getElementById('comparisonChart').getContext('2d');
        
        if (this.charts.comparison) {
            this.charts.comparison.destroy();
        }
        
        const areas = Object.values(this.comparisonData).slice(0, 4);
        
        this.charts.comparison = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: areas.map(area => area.name),
                datasets: [
                    {
                        label: 'Sustainability Score',
                        data: areas.map(area => area.environmental_data.sustainability_score),
                        backgroundColor: 'rgba(252, 61, 33, 0.8)',
                        borderColor: '#FC3D21',
                        borderWidth: 2
                    },
                    {
                        label: 'Green Cover (%)',
                        data: areas.map(area => area.environmental_data.green_cover),
                        backgroundColor: 'rgba(76, 175, 80, 0.8)',
                        borderColor: '#4CAF50',
                        borderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Urban Area Comparison - NASA Metrics',
                        color: '#fff'
                    },
                    legend: {
                        labels: { color: '#fff' }
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#fff' }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#fff' },
                        max: 100
                    }
                }
            }
        });
    }

    updateComparisonTable() {
        const container = document.getElementById('comparison-table-body');
        let html = '';
        
        Object.values(this.comparisonData).forEach(area => {
            html += `
                <tr>
                    <td>${area.name}</td>
                    <td>${area.nasa_metrics.surface_temperature}°C</td>
                    <td>${area.environmental_data.green_cover}%</td>
                    <td>${area.nasa_metrics.air_quality_index}</td>
                    <td>${area.environmental_data.sustainability_score}</td>
                    <td>${this.getTransportScore(area)}</td>
                    <td>
                        <span style="color: ${this.getSustainabilityColor(area.environmental_data.sustainability_score)}">
                            ${this.getRating(area.environmental_data.sustainability_score)}
                        </span>
                    </td>
                </tr>
            `;
        });
        
        container.innerHTML = html;
    }

    getTransportScore(area) {
        return 100 - area.transportation.private_vehicles;
    }

    getRating(score) {
        if (score >= 80) return 'Excellent';
        if (score >= 60) return 'Good';
        if (score >= 40) return 'Fair';
        return 'Poor';
    }

    generateNASAHeatMap() {
        // This would integrate with a proper mapping library
        console.log('NASA Heat Map generated with urban temperature data');
    }

    showNASALoading(containerId) {
        const container = document.getElementById(containerId);
        container.innerHTML = `
            <div class="nasa-loading">
                <div class="nasa-spinner"></div>
                <p>Loading NASA Satellite Data...</p>
            </div>
        `;
    }

    showError(message) {
        const container = document.querySelector('.analysis-content');
        container.innerHTML = `
            <div class="nasa-error" style="text-align: center; padding: 60px;">
                <i class="fas fa-exclamation-triangle" style="font-size: 4rem; color: #FC3D21; margin-bottom: 20px;"></i>
                <h3>NASA Data Connection Issue</h3>
                <p>${message}</p>
                <button onclick="location.reload()" class="nasa-btn" style="margin-top: 20px;">
                    <i class="fas fa-sync-alt"></i> Retry Connection
                </button>
            </div>
        `;
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    new NASAUrbanDashboard();
});