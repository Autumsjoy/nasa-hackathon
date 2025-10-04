from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for, send_from_directory, Response
import json
import pandas as pd
import io
import base64
import os
import numpy as np
import traceback
from datetime import datetime

# Set environment variable to avoid matplotlib issues
os.environ['MPLBACKEND'] = 'Agg'

# Import utility modules with error handling
try:
    from utils.nasa_api import NASAAPI
    from utils.data_processing import BhopalDataProcessor
    from utils.visualization_plotly import DataVisualizerPlotly
    from config.nasa_config import NASAConfig
    print("✅ Utility modules imported successfully")
except ImportError as e:
    print(f"⚠️ Some utility imports failed: {e}")
    # Create fallback classes
    class NASAAPI:
        def get_urban_heat_island_data(self): return {}
        def calculate_urban_sustainability_score(self, data): return 50
    
    class BhopalDataProcessor:
        def generate_area_analysis(self, nasa_api): 
            return {
                'old_bhopal': {
                    'name': 'Old Bhopal Heritage',
                    'sustainability_score': 45.0,
                    'transport_index': 4.2,
                    'pollution_index': 7.8,
                    'energy_index': 3.5,
                    'vegetation_index': 0.35,
                    'urbanization_index': 0.85,
                    'temperature': 35.8,
                    'population_density': 12000,
                    'green_cover': 15.0,
                    'solar_potential': 5.2,
                    'type': 'Heritage & Commercial'
                },
                'new_bhopal': {
                    'name': 'New Bhopal Development',
                    'sustainability_score': 65.0,
                    'transport_index': 7.2,
                    'pollution_index': 4.5,
                    'energy_index': 6.8,
                    'vegetation_index': 0.52,
                    'urbanization_index': 0.62,
                    'temperature': 32.5,
                    'population_density': 8500,
                    'green_cover': 28.0,
                    'solar_potential': 5.8,
                    'type': 'Residential & Commercial'
                }
            }
    
    class DataVisualizerPlotly:
        def generate_sustainability_chart(self, data): return "<div>Chart placeholder - Sustainability</div>"
        def generate_comparison_chart(self, data): return "<div>Chart placeholder - Comparison</div>"
        def generate_satellite_analysis_chart(self, data): return "<div>Chart placeholder - Satellite</div>"
        def generate_vegetation_analysis_chart(self, data): return "<div>Chart placeholder - Vegetation</div>"
        def generate_satellite_data_comparison(self, data): return "<div>Chart placeholder - Satellite Comparison</div>"
        def generate_interactive_map(self, data): return "<div>Map placeholder</div>"
        def generate_radar_chart_comparison(self, data): return "<div>Chart placeholder - Radar</div>"
        def generate_correlation_matrix(self, data): return "<div>Chart placeholder - Correlation</div>"
        def generate_trend_analysis(self, data): return "<div>Chart placeholder - Trend</div>"
        def generate_radar_chart(self, data): return "<div>Chart placeholder - Radar Single</div>"
        def generate_energy_breakdown_chart(self, data): return "<div>Chart placeholder - Energy</div>"
        def generate_transportation_chart(self, data): return "<div>Chart placeholder - Transport</div>"
        def generate_area_sustainability_chart(self, data): return "<div>Chart placeholder - Area Sustainability</div>"
        def generate_performance_indicators(self, data): return "<div>Chart placeholder - Performance</div>"
        def generate_area_comparison_chart(self, data, all_data): return "<div>Chart placeholder - Area Comparison</div>"
        def generate_benchmark_comparison_chart(self, data, all_data): return "<div>Chart placeholder - Benchmark</div>"
        def generate_heat_map(self, data, metric): return "<div>Heatmap placeholder</div>"
        def generate_cesium_map(self, data): return "<div>3D Map placeholder</div>"

# Solution imports with comprehensive error handling
SOLUTION_MODULES = {}
try:
    from solutions.urban_health_solutions import get_urban_health_solutions
    SOLUTION_MODULES['urban_health'] = get_urban_health_solutions
    print("✅ urban_health_solutions loaded")
except ImportError as e:
    print(f"⚠️ urban_health_solutions not available: {e}")
    SOLUTION_MODULES['urban_health'] = None

try:
    from solutions.climate_resilience import get_climate_solutions
    SOLUTION_MODULES['climate'] = get_climate_solutions
    print("✅ climate_resilience loaded")
except ImportError:
    print("⚠️ climate_resilience not available")
    SOLUTION_MODULES['climate'] = None

try:
    from solutions.policy_recommendations import generate_policy_recommendations
    SOLUTION_MODULES['policy'] = generate_policy_recommendations
    print("✅ policy_recommendations loaded")
except ImportError:
    print("⚠️ policy_recommendations not available")
    SOLUTION_MODULES['policy'] = None

try:
    from solutions.resilience_strategies import get_resilience_strategies
    SOLUTION_MODULES['resilience'] = get_resilience_strategies
    print("✅ resilience_strategies loaded")
except ImportError:
    print("⚠️ resilience_strategies not available")
    SOLUTION_MODULES['resilience'] = None

try:
    from solutions.urban_recommendations import get_urban_recommendations
    SOLUTION_MODULES['urban_recommendations'] = get_urban_recommendations
    print("✅ urban_recommendations loaded")
except ImportError:
    print("⚠️ urban_recommendations not available")
    SOLUTION_MODULES['urban_recommendations'] = None

# Fallback functions for missing modules
def fallback_urban_health_solutions(data):
    return {
        'green_infrastructure': {
            'problem': 'Urban heat islands and inadequate green spaces',
            'solution': 'Precision Greening Strategy',
            'actions': ['Increase urban canopy cover', 'Create green corridors'],
            'nasa_data_used': ['MODIS NDVI', 'Landsat LST'],
            'expected_impact': 'Reduce temperatures by 2-3°C'
        }
    }

def fallback_climate_solutions(data):
    return {
        'old_bhopal': {
            'area_name': 'Old Bhopal Heritage',
            'solutions': [{
                'type': 'heat_resilience',
                'problem': 'High urban heat (Temperature: 35.8°C)',
                'actions': ['Install cool roofing materials', 'Increase tree canopy cover by 20%'],
                'priority': 'High',
                'nasa_data': 'MODIS Land Surface Temperature'
            }]
        }
    }

def fallback_policy_recommendations(data):
    return {
        'high_priority': [{
            'area': 'Old Bhopal Heritage',
            'issue': 'Critical sustainability deficit (Score: 45.0)',
            'recommendation': 'Immediate green infrastructure investment and pollution control measures',
            'metrics': 'Sustainability: 45.0, Pollution: 7.8',
            'timeline': '0-6 months',
            'budget_estimate': 'High'
        }],
        'medium_priority': [], 
        'long_term': []
    }

def fallback_resilience_strategies(data):
    return {
        'old_bhopal': {
            'area_name': 'Old Bhopal Heritage',
            'primary_threat': 'heat',
            'primary_threat_description': 'Primary climate risk: Heat',
            'risk_level': 'High',
            'priority': 'High',
            'climate_threats': ['Urban Heat Island'],
            'resilience_actions': ['Install cool roofing materials', 'Increase tree canopy cover by 25%'],
            'nasa_data_sources': ['MODIS LST', 'Landsat NDVI'],
            'expected_impact': 'Reduce climate vulnerability by 30-40%'
        }
    }

def fallback_urban_recommendations(data):
    return {
        'infrastructure': [{
            'area': 'Old Bhopal Heritage',
            'issue': 'Inadequate public transport infrastructure',
            'recommendation': 'Develop integrated transport network with bus rapid transit',
            'priority': 'High',
            'timeline': '6-12 months',
            'budget': 'Medium'
        }],
        'land_use': [],
        'transportation': [],
        'environmental': []
    }

app = Flask(__name__)

# Enhanced area mappings with detailed information
AREA_MAPPINGS = {
    'old_bhopal': {
        'name': 'Old Bhopal Heritage',
        'description': 'Historic city center with traditional architecture and cultural significance',
        'type': 'Heritage & Commercial',
        'coordinates': [23.2599, 77.4126]
    },
    'new_bhopal': {
        'name': 'New Bhopal Development',
        'description': 'Modern planned areas with contemporary infrastructure',
        'type': 'Residential & Commercial',
        'coordinates': [23.2278, 77.4357]
    },
    'shahpura': {
        'name': 'Shahpura Sector',
        'description': 'Mixed residential and commercial sector with good connectivity',
        'type': 'Mixed Use',
        'coordinates': [23.3000, 77.3667]
    },
    'kolar': {
        'name': 'Kolar Residential Zone',
        'description': 'Suburban residential area with growing infrastructure',
        'type': 'Residential',
        'coordinates': [23.1667, 77.4333]
    },
    'indrapuri': {
        'name': 'Indrapuri Housing',
        'description': 'Planned residential colony with green spaces',
        'type': 'Residential',
        'coordinates': [23.2800, 77.4200]
    },
    'bhopal_lake': {
        'name': 'Bhopal Lake Area',
        'description': 'Areas surrounding Upper and Lower Lakes, focus on environmental conservation',
        'type': 'Environmental & Recreational',
        'coordinates': [23.2667, 77.4000]
    },
    'industrial_area': {
        'name': 'Industrial Zone',
        'description': 'Manufacturing and industrial activities area',
        'type': 'Industrial',
        'coordinates': [23.2000, 77.4500]
    }
}

def get_enhanced_sample_data():
    """Generate enhanced sample data with comprehensive satellite information"""
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    base_data = processor.generate_area_analysis(nasa_api)
    
    # Enhance the data with detailed satellite information
    enhanced_data = {}
    
    for area_key, area_data in base_data.items():
        coords = AREA_MAPPINGS.get(area_key, {}).get('coordinates', [23.2599, 77.4126])
        enhanced_data[area_key] = {
            **area_data,
            'latitude': coords[0],
            'longitude': coords[1],
            # Enhanced satellite data
            'satellite_imagery': {
                'landsat_acquisition_date': '2024-01-15',
                'modis_acquisition_date': '2024-01-16',
                'resolution': '30m (Landsat) / 250m (MODIS)',
                'cloud_cover': f"{np.random.randint(5, 20)}%",
                'data_quality': 'Excellent'
            },
            'detailed_vegetation': {
                'ndvi_mean': area_data.get('vegetation_index', 0.5),
                'ndvi_std': 0.15,
                'vegetation_health': area_data.get('vegetation_health', 'Moderate'),
                'forest_cover': f"{np.random.randint(15, 60)}%",
                'agricultural_land': f"{np.random.randint(10, 40)}%",
                'green_spaces': f"{np.random.randint(5, 25)}%"
            },
            'urban_analysis': {
                'built_up_area': f"{np.random.randint(30, 85)}%",
                'population_density': area_data.get('population_density', 1000),
                'road_density': f"{np.random.randint(5, 20)} km/km²",
                'building_height_avg': f"{np.random.randint(8, 25)}m"
            },
            'environmental_metrics': {
                'air_quality_index': np.random.randint(50, 150),
                'water_quality_index': np.random.randint(60, 95),
                'noise_pollution': f"{np.random.randint(45, 80)} dB",
                'carbon_sequestration': f"{np.random.randint(50, 200)} tons/year"
            },
            'infrastructure_metrics': {
                'public_transport_coverage': f"{np.random.randint(40, 90)}%",
                'renewable_energy_capacity': f"{np.random.randint(5, 25)} MW",
                'waste_management_efficiency': f"{np.random.randint(50, 95)}%",
                'water_supply_coverage': f"{np.random.randint(70, 98)}%"
            },
            'historical_trends': {
                'vegetation_change_5yr': f"+{np.random.randint(1, 10)}%",
                'urbanization_growth_5yr': f"+{np.random.randint(5, 20)}%",
                'temperature_change_5yr': f"+{np.random.uniform(0.5, 2.1):.1f}°C",
                'sustainability_improvement': f"+{np.random.randint(5, 25)}%"
            }
        }
    
    return enhanced_data

def analysis_data_to_dataframe(analysis_data):
    """Convert analysis data dictionary to pandas DataFrame for correlation matrix"""
    df_data = []
    for area_key, area_data in analysis_data.items():
        row = {
            'area_key': area_key,
            'area_name': area_data.get('name', ''),
            'transport_index': area_data.get('transport_index', 0),
            'pollution_index': area_data.get('pollution_index', 0),
            'energy_index': area_data.get('energy_index', 0),
            'sustainability_score': area_data.get('sustainability_score', 0),
            'vegetation_index': area_data.get('vegetation_index', 0),
            'urbanization_index': area_data.get('urbanization_index', 0),
            'temperature': area_data.get('temperature', 0),
            'population_density': area_data.get('population_density', 0),
            'green_cover': area_data.get('green_cover', 0),
            'solar_potential': area_data.get('solar_potential', 0)
        }
        df_data.append(row)
    
    return pd.DataFrame(df_data)

def get_solution_data(solution_type, analysis_data):
    """Get solution data with fallback handling"""
    solution_func = SOLUTION_MODULES.get(solution_type)
    
    if solution_func:
        try:
            return solution_func(analysis_data)
        except Exception as e:
            print(f"Error in {solution_type} solution: {e}")
    
    # Return fallback data
    fallbacks = {
        'urban_health': fallback_urban_health_solutions,
        'climate': fallback_climate_solutions,
        'policy': fallback_policy_recommendations,
        'resilience': fallback_resilience_strategies,
        'urban_recommendations': fallback_urban_recommendations
    }
    return fallbacks.get(solution_type, lambda x: {})(analysis_data)

# Route definitions
@app.route('/')
def index():
    """Homepage with overview and key metrics"""
    try:
        nasa_api = NASAAPI()
        processor = BhopalDataProcessor()
        visualizer = DataVisualizerPlotly()
        
        # Get enhanced sample data for homepage
        analysis_data = get_enhanced_sample_data()
        
        # Generate a simple chart for homepage
        sustainability_chart = visualizer.generate_sustainability_chart(analysis_data)
        
        # Calculate overall statistics
        total_areas = len(analysis_data)
        avg_sustainability = sum(data['sustainability_score'] for data in analysis_data.values()) / total_areas
        best_area = max(analysis_data.values(), key=lambda x: x['sustainability_score'])
        worst_area = min(analysis_data.values(), key=lambda x: x['sustainability_score'])
        
        return render_template('index.html', 
                             data=analysis_data, 
                             area_mappings=AREA_MAPPINGS,
                             sustainability_chart=sustainability_chart,
                             total_areas=total_areas,
                             avg_sustainability=round(avg_sustainability, 1),
                             best_area=best_area,
                             worst_area=worst_area)
    except Exception as e:
        return f"Error loading homepage: {str(e)}", 500

# ADD THE MISSING ROUTE
@app.route('/solutions')
def solutions_page():
    """Main solutions page - redirect to overview"""
    return redirect(url_for('solutions_overview'))

# Keep all your existing routes (dashboard, analysis, satellite, etc.) as they are
# ... [ALL YOUR EXISTING ROUTES REMAIN THE SAME] ...

# Error Handlers with better error messages
@app.errorhandler(404)
def not_found(error):
    try:
        return render_template('404.html'), 404
    except:
        return "Page not found - 404 Error", 404

@app.errorhandler(500)
def internal_error(error):
    try:
        return render_template('500.html'), 500
    except:
        return "Internal server error - 500 Error", 500

@app.route('/favicon.ico')
def favicon():
    return Response(status=204)

if __name__ == '__main__':
    print("🚀 Starting NASA Urban Planning Application...")
    print("📁 Current directory:", os.getcwd())
    print("✅ All routes initialized")
    
    # Enable debug mode for development
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)