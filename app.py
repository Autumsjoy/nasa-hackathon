from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for
import json
import pandas as pd
import io
import base64
import os

# Set environment variable to avoid matplotlib issues
os.environ['MPLBACKEND'] = 'Agg'

from utils.nasa_api import NASAAPI
from utils.data_processing import BhopalDataProcessor
from utils.visualization_plotly import DataVisualizerPlotly
from config.nasa_config import NASAConfig

app = Flask(__name__)

# Define area mappings based on your data_processing.py
AREA_MAPPINGS = {
    'old_bhopal': 'Old Bhopal',
    'new_bhopal': 'New Bhopal', 
    'shahpura': 'Shahpura',
    'kolar': 'Kolar',
    'indrapuri': 'Indrapuri',
    'bhopal_lake': 'Bhopal Lake Area',
    'industrial_area': 'Industrial Area'
}

@app.route('/')
def index():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    visualizer = DataVisualizerPlotly()
    
    # Get sample data for homepage
    analysis_data = processor.generate_area_analysis(nasa_api)
    
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
    
    # Get analysis data
    analysis_data = processor.generate_area_analysis(nasa_api)
    
    # Calculate city averages
    if analysis_data:
        transport_avg = sum(data.get('transport_index', 0) for data in analysis_data.values()) / len(analysis_data)
        pollution_avg = sum(data.get('pollution_index', 0) for data in analysis_data.values()) / len(analysis_data)
        energy_avg = sum(data.get('energy_index', 0) for data in analysis_data.values()) / len(analysis_data)
        sustainability_avg = sum(data.get('sustainability_score', 0) for data in analysis_data.values()) / len(analysis_data)
    else:
        transport_avg = pollution_avg = energy_avg = sustainability_avg = 0
    
    # Generate charts and maps
    sustainability_chart = visualizer.generate_sustainability_chart(analysis_data)
    satellite_chart = visualizer.generate_satellite_analysis_chart(analysis_data)
    comparison_chart = visualizer.generate_comparison_chart(analysis_data)
    vegetation_chart = visualizer.generate_vegetation_analysis_chart(analysis_data)
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
                         map_html=map_html,
                         top_areas=top_areas,
                         area_mappings=AREA_MAPPINGS)

@app.route('/heatmaps')
def heatmaps():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    visualizer = DataVisualizerPlotly()
    analysis_data = processor.generate_area_analysis(nasa_api)
    
    # Generate multiple heat maps
    sustainability_heatmap = visualizer.generate_heat_map(analysis_data, 'sustainability_score')
    pollution_heatmap = visualizer.generate_heat_map(analysis_data, 'pollution_index')
    transport_heatmap = visualizer.generate_heat_map(analysis_data, 'transport_index')
    vegetation_heatmap = visualizer.generate_heat_map(analysis_data, 'vegetation_index')
    
    return render_template('heatmaps.html',
                         data=analysis_data,
                         sustainability_heatmap=sustainability_heatmap,
                         pollution_heatmap=pollution_heatmap,
                         transport_heatmap=transport_heatmap,
                         vegetation_heatmap=vegetation_heatmap,
                         area_mappings=AREA_MAPPINGS)

@app.route('/analysis')
def analysis_page():
    """Main analysis page showing all areas"""
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    analysis_data = processor.generate_area_analysis(nasa_api)
    
    # Generate comparison charts
    visualizer = DataVisualizerPlotly()
    comparison_chart = visualizer.generate_comparison_chart(analysis_data)
    sustainability_chart = visualizer.generate_sustainability_chart(analysis_data)
    radar_chart = visualizer.generate_radar_chart_comparison(analysis_data)
    
    # Calculate statistics for the analysis page
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
            'type': area_data['type']
        }
        area_stats.append(stats)
    
    return render_template('analysis.html', 
                         data=analysis_data,
                         comparison_chart=comparison_chart,
                         sustainability_chart=sustainability_chart,
                         radar_chart=radar_chart,
                         area_stats=area_stats,
                         area_mappings=AREA_MAPPINGS)

@app.route('/analysis/<area_key>')
def area_analysis(area_key):
    """Detailed analysis for a specific area"""
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    analysis_data = processor.generate_area_analysis(nasa_api)
    
    if area_key in analysis_data:
        area_data = analysis_data[area_key]
        visualizer = DataVisualizerPlotly()
        
        # Generate all charts for this specific area
        radar_chart = visualizer.generate_radar_chart(area_data)
        energy_chart = visualizer.generate_energy_breakdown_chart(area_data)
        transport_chart = visualizer.generate_transportation_chart(area_data)
        sustainability_chart = visualizer.generate_area_sustainability_chart(area_data)
        
        # Generate comparison with other areas
        comparison_chart = visualizer.generate_area_comparison_chart(area_data, analysis_data)
        
        return render_template('area_analysis.html', 
                             area_data=area_data,
                             area_key=area_key,
                             area_name=AREA_MAPPINGS.get(area_key, area_data['name']),
                             radar_chart=radar_chart,
                             energy_chart=energy_chart,
                             transport_chart=transport_chart,
                             sustainability_chart=sustainability_chart,
                             comparison_chart=comparison_chart,
                             all_areas=analysis_data,
                             area_mappings=AREA_MAPPINGS)
    else:
        return "Area not found", 404

# FIXED: Changed from '/satellite' to '/satellite-data' to avoid conflict
@app.route('/satellite-data')
def satellite_data():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    visualizer = DataVisualizerPlotly()
    analysis_data = processor.generate_area_analysis(nasa_api)
    
    # Generate satellite-specific charts
    satellite_chart = visualizer.generate_satellite_data_comparison(analysis_data)
    comparison_chart = visualizer.generate_comparison_chart(analysis_data)
    vegetation_chart = visualizer.generate_vegetation_analysis_chart(analysis_data)
    
    return render_template('satellite.html', 
                         data=analysis_data,
                         satellite_chart=satellite_chart,
                         comparison_chart=comparison_chart,
                         vegetation_chart=vegetation_chart,
                         area_mappings=AREA_MAPPINGS)

# FIXED: This is the main satellite analysis route - keep it as '/satellite'
@app.route('/satellite')
def satellite_analysis():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    visualizer = DataVisualizerPlotly()
    analysis_data = processor.generate_area_analysis(nasa_api)
    
    # Generate satellite-specific charts
    satellite_chart = visualizer.generate_satellite_data_comparison(analysis_data)
    comparison_chart = visualizer.generate_comparison_chart(analysis_data)
    vegetation_chart = visualizer.generate_vegetation_analysis_chart(analysis_data)
    
    return render_template('satellite.html', 
                         data=analysis_data,
                         satellite_chart=satellite_chart,
                         comparison_chart=comparison_chart,
                         vegetation_chart=vegetation_chart,
                         area_mappings=AREA_MAPPINGS)

@app.route('/satellite-3d')
def satellite_3d():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    visualizer = DataVisualizerPlotly()
    analysis_data = processor.generate_area_analysis(nasa_api)
    
    cesium_map = visualizer.generate_cesium_map(analysis_data)
    
    return render_template('satellite-3d.html', 
                         cesium_map=cesium_map,
                         data=analysis_data,
                         area_mappings=AREA_MAPPINGS)

# Update the existing area_detail route to redirect to analysis
@app.route('/area/<area_key>')
def area_detail(area_key):
    """Redirect to area analysis page"""
    return redirect(url_for('area_analysis', area_key=area_key))

# API routes
@app.route('/api/analysis')
def api_analysis():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    analysis_data = processor.generate_area_analysis(nasa_api)
    return jsonify(analysis_data)

@app.route('/api/area/<area_key>')
def api_area_data(area_key):
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    analysis_data = processor.generate_area_analysis(nasa_api)
    
    if area_key in analysis_data:
        return jsonify(analysis_data[area_key])
    
    return jsonify({'error': 'Area not found'}), 404

@app.route('/api/satellite/<area_key>')
def api_satellite_data(area_key):
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    analysis_data = processor.generate_area_analysis(nasa_api)
    
    if area_key in analysis_data:
        satellite_data = {
            'modis_vegetation': analysis_data[area_key].get('modis_vegetation', {}),
            'modis_land_cover': analysis_data[area_key].get('modis_land_cover', {}),
            'modis_temperature': analysis_data[area_key].get('modis_temperature', {}),
            'landsat_indices': analysis_data[area_key].get('landsat_indices', {}),
            'landsat_metadata': analysis_data[area_key].get('landsat_metadata', {})
        }
        return jsonify(satellite_data)
    
    return jsonify({'error': 'Area not found'}), 404

# Download routes
@app.route('/download/csv')
def download_csv():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    analysis_data = processor.generate_area_analysis(nasa_api)
    
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

@app.route('/download/geojson')
def download_geojson():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    analysis_data = processor.generate_area_analysis(nasa_api)
    geojson_data = processor.export_to_geojson(analysis_data)
    
    return jsonify(geojson_data)

@app.route('/download/satellite')
def download_satellite_data():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    analysis_data = processor.generate_area_analysis(nasa_api)
    
    # Create satellite data CSV
    satellite_data = []
    for area_key, data in analysis_data.items():
        row = {
            'area_name': data.get('name', ''),
            'ndvi': data.get('modis_vegetation', {}).get('ndvi', 0),
            'evi': data.get('modis_vegetation', {}).get('evi', 0),
            'vegetation_density': data.get('modis_vegetation', {}).get('vegetation_density', 0),
            'land_cover_type': data.get('modis_land_cover', {}).get('land_cover_type', ''),
            'land_surface_temperature': data.get('modis_temperature', {}).get('daytime_temperature', 0),
            'urban_heat_intensity': data.get('modis_temperature', {}).get('urban_heat_intensity', 0),
            'landsat_ndvi': data.get('landsat_indices', {}).get('ndvi', 0),
            'landsat_ndbi': data.get('landsat_indices', {}).get('ndbi', 0),
            'urbanization_level': data.get('landsat_indices', {}).get('urbanization_level', ''),
            'acquisition_date': data.get('landsat_metadata', {}).get('acquisition_date', '')
        }
        satellite_data.append(row)
    
    df = pd.DataFrame(satellite_data)
    
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='bhopal_satellite_data.csv'
    )

@app.route('/api/health')
def api_health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': pd.Timestamp.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)