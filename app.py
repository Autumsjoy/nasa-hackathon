from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for
import json
import pandas as pd
import io
import base64
import os
import numpy as np

# Set environment variable to avoid matplotlib issues
os.environ['MPLBACKEND'] = 'Agg'

from utils.nasa_api import NASAAPI
from utils.data_processing import BhopalDataProcessor
from utils.visualization_plotly import DataVisualizerPlotly
from config.nasa_config import NASAConfig

app = Flask(__name__)

# Enhanced area mappings with detailed information
AREA_MAPPINGS = {
    'old_bhopal': {
        'name': 'Old Bhopal Heritage',
        'description': 'Historic city center with traditional architecture and cultural significance',
        'type': 'Heritage & Commercial'
    },
    'new_bhopal': {
        'name': 'New Bhopal Development',
        'description': 'Modern planned areas with contemporary infrastructure',
        'type': 'Residential & Commercial'
    },
    'shahpura': {
        'name': 'Shahpura Sector',
        'description': 'Mixed residential and commercial sector with good connectivity',
        'type': 'Mixed Use'
    },
    'kolar': {
        'name': 'Kolar Residential Zone',
        'description': 'Suburban residential area with growing infrastructure',
        'type': 'Residential'
    },
    'indrapuri': {
        'name': 'Indrapuri Housing',
        'description': 'Planned residential colony with green spaces',
        'type': 'Residential'
    },
    'bhopal_lake': {
        'name': 'Bhopal Lake Area',
        'description': 'Areas surrounding Upper and Lower Lakes, focus on environmental conservation',
        'type': 'Environmental & Recreational'
    },
    'industrial_area': {
        'name': 'Industrial Zone',
        'description': 'Manufacturing and industrial activities area',
        'type': 'Industrial'
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
        enhanced_data[area_key] = {
            **area_data,
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

@app.route('/')
def index():
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

@app.route('/dashboard')
def dashboard():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    visualizer = DataVisualizerPlotly()
    
    # Get enhanced analysis data
    analysis_data = get_enhanced_sample_data()
    
    # Calculate city averages
    if analysis_data:
        transport_avg = sum(data.get('transport_index', 0) for data in analysis_data.values()) / len(analysis_data)
        pollution_avg = sum(data.get('pollution_index', 0) for data in analysis_data.values()) / len(analysis_data)
        energy_avg = sum(data.get('energy_index', 0) for data in analysis_data.values()) / len(analysis_data)
        sustainability_avg = sum(data.get('sustainability_score', 0) for data in analysis_data.values()) / len(analysis_data)
    else:
        transport_avg = pollution_avg = energy_avg = sustainability_avg = 0
    
    # Generate comprehensive charts and maps
    sustainability_chart = visualizer.generate_sustainability_chart(analysis_data)
    satellite_chart = visualizer.generate_satellite_analysis_chart(analysis_data)
    comparison_chart = visualizer.generate_comparison_chart(analysis_data)
    vegetation_chart = visualizer.generate_vegetation_analysis_chart(analysis_data)
    satellite_comparison_chart = visualizer.generate_satellite_data_comparison(analysis_data)
    map_html = visualizer.generate_interactive_map(analysis_data)
    
    # Get top performing areas
    sorted_areas = sorted(analysis_data.values(), key=lambda x: x['sustainability_score'], reverse=True)
    top_areas = sorted_areas[:3]
    
    return render_template('dashboard.html', 
                         data=analysis_data,
                         transport_avg=round(transport_avg, 2),
                         pollution_avg=round(pollution_avg, 2),
                         energy_avg=round(energy_avg, 2),
                         sustainability_avg=round(sustainability_avg, 2),
                         sustainability_chart=sustainability_chart,
                         satellite_chart=satellite_chart,
                         comparison_chart=comparison_chart,
                         vegetation_chart=vegetation_chart,
                         satellite_comparison_chart=satellite_comparison_chart,
                         map_html=map_html,
                         top_areas=top_areas,
                         area_mappings=AREA_MAPPINGS)

@app.route('/heatmaps')
def heatmaps():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    visualizer = DataVisualizerPlotly()
    analysis_data = get_enhanced_sample_data()
    
    # Generate multiple heat maps
    sustainability_heatmap = visualizer.generate_heat_map(analysis_data, 'sustainability_score')
    pollution_heatmap = visualizer.generate_heat_map(analysis_data, 'pollution_index')
    transport_heatmap = visualizer.generate_heat_map(analysis_data, 'transport_index')
    vegetation_heatmap = visualizer.generate_heat_map(analysis_data, 'vegetation_index')
    urbanization_heatmap = visualizer.generate_heat_map(analysis_data, 'urbanization_index')
    
    return render_template('heatmaps.html',
                         data=analysis_data,
                         sustainability_heatmap=sustainability_heatmap,
                         pollution_heatmap=pollution_heatmap,
                         transport_heatmap=transport_heatmap,
                         vegetation_heatmap=vegetation_heatmap,
                         urbanization_heatmap=urbanization_heatmap,
                         area_mappings=AREA_MAPPINGS)

@app.route('/analysis')
def analysis_page():
    """Main analysis page showing all areas"""
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    analysis_data = get_enhanced_sample_data()
    
    # Generate comprehensive comparison charts
    visualizer = DataVisualizerPlotly()
    comparison_chart = visualizer.generate_comparison_chart(analysis_data)
    sustainability_chart = visualizer.generate_sustainability_chart(analysis_data)
    radar_chart = visualizer.generate_radar_chart_comparison(analysis_data)
    correlation_matrix = visualizer.generate_correlation_matrix(analysis_data)
    trend_analysis = visualizer.generate_trend_analysis(analysis_data)
    
    # Calculate detailed statistics for the analysis page
    area_stats = []
    for area_key, area_data in analysis_data.items():
        stats = {
            'name': area_data['name'],
            'key': area_key,
            'sustainability_score': area_data['sustainability_score'],
            'transport_index': area_data['transport_index'],
            'pollution_index': area_data['pollution_index'],
            'energy_index': area_data['energy_index'],
            'vegetation_index': area_data['vegetation_index'],
            'urbanization_index': area_data['urbanization_index'],
            'type': area_data['type'],
            'population_density': area_data.get('population_density', 0),
            'solar_potential': area_data.get('solar_potential', 0),
            'detailed_info': AREA_MAPPINGS.get(area_key, {})
        }
        area_stats.append(stats)
    
    # Sort by sustainability score
    area_stats.sort(key=lambda x: x['sustainability_score'], reverse=True)
    
    return render_template('analysis.html', 
                         data=analysis_data,
                         comparison_chart=comparison_chart,
                         sustainability_chart=sustainability_chart,
                         radar_chart=radar_chart,
                         correlation_matrix=correlation_matrix,
                         trend_analysis=trend_analysis,
                         area_stats=area_stats,
                         area_mappings=AREA_MAPPINGS)

@app.route('/analysis/<area_key>')
def area_analysis(area_key):
    """Detailed analysis for a specific area"""
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    analysis_data = get_enhanced_sample_data()
    
    if area_key in analysis_data:
        area_data = analysis_data[area_key]
        area_info = AREA_MAPPINGS.get(area_key, {})
        visualizer = DataVisualizerPlotly()
        
        # Generate all charts for this specific area
        radar_chart = visualizer.generate_radar_chart(area_data)
        energy_chart = visualizer.generate_energy_breakdown_chart(area_data)
        transport_chart = visualizer.generate_transportation_chart(area_data)
        sustainability_chart = visualizer.generate_area_sustainability_chart(area_data)
        performance_indicators = visualizer.generate_performance_indicators(area_data)
        
        # Generate comparison with other areas
        comparison_chart = visualizer.generate_area_comparison_chart(area_data, analysis_data)
        benchmark_chart = visualizer.generate_benchmark_comparison_chart(area_data, analysis_data)
        
        return render_template('area_analysis.html', 
                             area_data=area_data,
                             area_key=area_key,
                             area_name=area_info.get('name', area_data['name']),
                             area_description=area_info.get('description', ''),
                             area_type=area_info.get('type', ''),
                             radar_chart=radar_chart,
                             energy_chart=energy_chart,
                             transport_chart=transport_chart,
                             sustainability_chart=sustainability_chart,
                             performance_indicators=performance_indicators,
                             comparison_chart=comparison_chart,
                             benchmark_chart=benchmark_chart,
                             all_areas=analysis_data,
                             area_mappings=AREA_MAPPINGS)
    else:
        return "Area not found", 404

@app.route('/satellite')
def satellite_analysis():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    visualizer = DataVisualizerPlotly()
    analysis_data = get_enhanced_sample_data()
    
    # Generate comprehensive satellite-specific charts
    satellite_chart = visualizer.generate_satellite_data_comparison(analysis_data)
    comparison_chart = visualizer.generate_comparison_chart(analysis_data)
    vegetation_chart = visualizer.generate_vegetation_analysis_chart(analysis_data)
    satellite_analysis_chart = visualizer.generate_satellite_analysis_chart(analysis_data)
    
    # Generate MODIS data for each area
    modis_data = {}
    for area_key, area_data in analysis_data.items():
        modis_data[area_key] = {
            'vegetation': {
                'ndvi': area_data.get('vegetation_index', 0.5),
                'evi': area_data.get('vegetation_index', 0.5) + 0.1,  # Simulated EVI
                'source': 'MODIS Terra/Aqua'
            },
            'temperature': {
                'daytime_temperature': area_data.get('temperature', 25),
                'urban_heat_intensity': area_data.get('urban_heat_intensity', 2.0)
            },
            'land_cover': {
                'land_cover_type': area_data.get('type', 'Urban'),
                'confidence': 0.85 + (area_data.get('vegetation_index', 0.5) * 0.15)
            }
        }
    
    return render_template('satellite.html', 
                         data=analysis_data,
                         satellite_chart=satellite_chart,
                         comparison_chart=comparison_chart,
                         vegetation_chart=vegetation_chart,
                         satellite_analysis_chart=satellite_analysis_chart,
                         modis_data=modis_data,
                         area_mappings=AREA_MAPPINGS)
@app.route('/satellite-3d')
def satellite_3d():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    visualizer = DataVisualizerPlotly()
    analysis_data = get_enhanced_sample_data()
    
    cesium_map = visualizer.generate_cesium_map(analysis_data)
    
    return render_template('satellite-3d.html', 
                         cesium_map=cesium_map,
                         data=analysis_data,
                         area_mappings=AREA_MAPPINGS)

# API routes (keep existing)
@app.route('/api/analysis')
def api_analysis():
    analysis_data = get_enhanced_sample_data()
    return jsonify(analysis_data)

@app.route('/api/area/<area_key>')
def api_area_data(area_key):
    analysis_data = get_enhanced_sample_data()
    
    if area_key in analysis_data:
        return jsonify(analysis_data[area_key])
    
    return jsonify({'error': 'Area not found'}), 404

# Download routes (keep existing)
@app.route('/download/csv')
def download_csv():
    analysis_data = get_enhanced_sample_data()
    
    # Convert to DataFrame
    df_data = []
    for area_key, data in analysis_data.items():
        row = {
            'area_key': area_key,
            'area_name': data.get('name', ''),
            'area_type': data.get('type', ''),
            'transport_index': data.get('transport_index', 0),
            'pollution_index': data.get('pollution_index', 0),
            'energy_index': data.get('energy_index', 0),
            'sustainability_score': data.get('sustainability_score', 0),
            'solar_potential': data.get('solar_potential', 0),
            'solar_percentage': data.get('solar_percentage', 0),
            'temperature': data.get('temperature', 0),
            'population_density': data.get('population_density', 0),
            'green_cover': data.get('green_cover', 0),
            'grid_dependency': data.get('grid_dependency', 0),
            'vegetation_index': data.get('vegetation_index', 0),
            'urbanization_index': data.get('urbanization_index', 0),
            'vegetation_health': data.get('vegetation_health', ''),
            'urbanization_level': data.get('urbanization_level', ''),
            'renewable_capacity': data.get('renewable_capacity', '')
        }
        df_data.append(row)
    
    df = pd.DataFrame(df_data)
    
    # Create CSV
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='bhopal_urban_planning_analysis.csv'
    )

@app.route('/api/health')
def api_health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': pd.Timestamp.now().isoformat(),
        'version': '1.0.0',
        'areas_available': len(AREA_MAPPINGS)
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)