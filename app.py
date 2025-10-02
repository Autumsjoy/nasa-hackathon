from flask import Flask, render_template, jsonify, request, send_file
import json
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from utils.nasa_api import NASAAPI
from utils.data_processing import BhopalDataProcessor
from utils.visualization import DataVisualizer
from config.nasa_config import NASAConfig

app = Flask(__name__)

@app.route('/')
def index():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    visualizer = DataVisualizer()
    
    # Get sample data for homepage
    analysis_data = processor.generate_area_analysis(nasa_api)
    
    return render_template('index.html', data=analysis_data)

@app.route('/dashboard')
def dashboard():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    visualizer = DataVisualizer()
    
    # Get analysis data
    analysis_data = processor.generate_area_analysis(nasa_api)
    
    # Calculate city averages
    transport_avg = sum(data['transport_index'] for data in analysis_data.values()) / len(analysis_data)
    pollution_avg = sum(data['pollution_index'] for data in analysis_data.values()) / len(analysis_data)
    energy_avg = sum(data['energy_index'] for data in analysis_data.values()) / len(analysis_data)
    sustainability_avg = sum(data['sustainability_score'] for data in analysis_data.values()) / len(analysis_data)
    
    # Generate charts and maps
    sustainability_chart = visualizer.generate_sustainability_chart(analysis_data)
    satellite_chart = visualizer.generate_satellite_analysis_chart(analysis_data)
    map_html = visualizer.generate_interactive_map(analysis_data)
    
    return render_template('dashboard.html', 
                         data=analysis_data,
                         transport_avg=round(transport_avg, 2),
                         pollution_avg=round(pollution_avg, 2),
                         energy_avg=round(energy_avg, 2),
                         sustainability_avg=round(sustainability_avg, 2),
                         sustainability_chart=sustainability_chart,
                         satellite_chart=satellite_chart,
                         map_html=map_html)

@app.route('/heatmaps')
def heatmaps():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    visualizer = DataVisualizer()
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
                         vegetation_heatmap=vegetation_heatmap)

@app.route('/analysis')
def analysis_page():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    analysis_data = processor.generate_area_analysis(nasa_api)
    return render_template('analysis.html', data=analysis_data)

@app.route('/satellite')
def satellite_analysis():
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    visualizer = DataVisualizer()
    analysis_data = processor.generate_area_analysis(nasa_api)
    
    satellite_chart = visualizer.generate_satellite_data_comparison(analysis_data)
    comparison_chart = visualizer.generate_comparison_chart(analysis_data)
    
    return render_template('satellite.html', 
                         data=analysis_data,
                         satellite_chart=satellite_chart,
                         comparison_chart=comparison_chart)

@app.route('/area/<area_key>')
def area_detail(area_key):
    nasa_api = NASAAPI()
    processor = BhopalDataProcessor()
    analysis_data = processor.generate_area_analysis(nasa_api)
    
    if area_key in analysis_data:
        area_data = analysis_data[area_key]
        visualizer = DataVisualizer()
        radar_chart = visualizer.generate_radar_chart(area_data)
        energy_chart = visualizer.generate_energy_breakdown_chart(area_data)
        transport_chart = visualizer.generate_transportation_chart(area_data)
        sustainability_chart = visualizer.generate_area_sustainability_chart(area_data)
        
        return render_template('area_detail.html', 
                             area_data=area_data,
                             area_key=area_key,
                             radar_chart=radar_chart,
                             energy_chart=energy_chart,
                             transport_chart=transport_chart,
                             sustainability_chart=sustainability_chart)
    else:
        return "Area not found", 404

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
            'modis_vegetation': analysis_data[area_key]['modis_vegetation'],
            'modis_land_cover': analysis_data[area_key]['modis_land_cover'],
            'modis_temperature': analysis_data[area_key]['modis_temperature'],
            'landsat_indices': analysis_data[area_key]['landsat_indices'],
            'landsat_metadata': analysis_data[area_key]['landsat_metadata']
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
            'area_name': data['name'],
            'area_type': data['type'],
            'transport_index': data['transport_index'],
            'pollution_index': data['pollution_index'],
            'energy_index': data['energy_index'],
            'sustainability_score': data['sustainability_score'],
            'solar_potential': data['solar_potential'],
            'solar_percentage': data['solar_percentage'],
            'temperature': data['temperature'],
            'population_density': data['population_density'],
            'green_cover': data['green_cover'],
            'grid_dependency': data['grid_dependency'],
            'vegetation_index': data['vegetation_index'],
            'urbanization_index': data['urbanization_index'],
            'vegetation_health': data['vegetation_health'],
            'urbanization_level': data['urbanization_level']
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
            'area_name': data['name'],
            'ndvi': data['modis_vegetation']['ndvi'],
            'evi': data['modis_vegetation']['evi'],
            'vegetation_density': data['modis_vegetation']['vegetation_density'],
            'land_cover_type': data['modis_land_cover']['land_cover_type'],
            'land_surface_temperature': data['modis_temperature']['daytime_temperature'],
            'urban_heat_intensity': data['modis_temperature']['urban_heat_intensity'],
            'landsat_ndvi': data['landsat_indices']['ndvi'],
            'landsat_ndbi': data['landsat_indices']['ndbi'],
            'urbanization_level': data['landsat_indices']['urbanization_level'],
            'acquisition_date': data['landsat_metadata']['acquisition_date']
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)