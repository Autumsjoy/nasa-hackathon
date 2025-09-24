from flask import Flask, request, jsonify, render_template
import os
import logging
import base64
from PIL import Image
import io
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')

# Add CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response

from urban_model import predictor

# Enhanced city data with heat map coordinates
CITY_DATA = {
    'Bhopal': {
        'problems': [
            {'id': 1, 'problem': 'Water Pollution', 'suggestion': 'Install water treatment plants', 'severity': 'high', 'coordinates': [23.25, 77.41]},
            {'id': 2, 'problem': 'Waste Management', 'suggestion': 'Improve segregation and recycling', 'severity': 'medium', 'coordinates': [23.26, 77.43]},
            {'id': 3, 'problem': 'Air Quality', 'suggestion': 'Promote public transportation', 'severity': 'high', 'coordinates': [23.24, 77.42]},
            {'id': 4, 'problem': 'Urban Heat Island', 'suggestion': 'Increase green cover', 'severity': 'medium', 'coordinates': [23.27, 77.40]}
        ],
        'center_coordinates': [23.2599, 77.4126],
        'temperature': 32.5,
        'vegetation': 0.15,
        'built_area': 0.60,
        'water': 0.05,
        'population': 8000
    },
    'Delhi': {
        'problems': [
            {'id': 1, 'problem': 'Air Pollution', 'suggestion': 'Strict emission controls', 'severity': 'very high', 'coordinates': [28.61, 77.20]},
            {'id': 2, 'problem': 'Traffic Congestion', 'suggestion': 'Develop metro infrastructure', 'severity': 'high', 'coordinates': [28.62, 77.22]}
        ],
        'center_coordinates': [28.6139, 77.2090],
        'temperature': 35.2,
        'vegetation': 0.10,
        'built_area': 0.75,
        'water': 0.02,
        'population': 12000
    },
    'Mumbai': {
        'problems': [
            {'id': 1, 'problem': 'Flooding', 'suggestion': 'Improve drainage systems', 'severity': 'high', 'coordinates': [19.07, 72.87]},
            {'id': 2, 'problem': 'Overpopulation', 'suggestion': 'Develop satellite cities', 'severity': 'medium', 'coordinates': [19.08, 72.88]}
        ],
        'center_coordinates': [19.0760, 72.8777],
        'temperature': 33.8,
        'vegetation': 0.12,
        'built_area': 0.70,
        'water': 0.08,
        'population': 15000
    }
}

@app.route('/')
def home():
    """Serve the main dashboard"""
    return render_template('index.html')

@app.route('/api/analyze-photo', methods=['POST'])
def analyze_photo():
    """Analyze uploaded photo for urban issues"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        analysis = analyze_urban_image(image_bytes)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'suggestions': generate_suggestions(analysis)
        })
        
    except Exception as e:
        logger.error(f"Photo analysis error: {e}")
        return jsonify({'success': False, 'error': 'Image processing failed'}), 500

def analyze_urban_image(image_bytes):
    """Enhanced image analysis for urban planning"""
    image = Image.open(io.BytesIO(image_bytes))
    width, height = image.size
    rgb_image = image.convert('RGB')
    pixels = np.array(rgb_image)
    
    # Advanced color analysis
    green_pixels = np.sum((pixels[:,:,1] > pixels[:,:,0]) & (pixels[:,:,1] > pixels[:,:,2]))
    gray_pixels = np.sum(np.std(pixels, axis=2) < 30)  # Low color variance = built area
    blue_pixels = np.sum(pixels[:,:,2] > pixels[:,:,0] + 20)  # Blue dominant = water
    
    total_pixels = width * height
    
    green_cover = (green_pixels / total_pixels) * 100
    built_area = (gray_pixels / total_pixels) * 100
    water_cover = (blue_pixels / total_pixels) * 100
    
    return {
        'green_cover': round(green_cover, 1),
        'built_area': round(built_area, 1),
        'water_cover': round(water_cover, 1),
        'image_size': f"{width}x{height}",
        'analysis_quality': 'advanced_urban_assessment'
    }

def generate_suggestions(analysis):
    """Generate suggestions based on image analysis"""
    suggestions = []
    green_cover = analysis['green_cover']
    built_area = analysis['built_area']
    water_cover = analysis['water_cover']
    
    if green_cover < 20:
        suggestions.append("🌳 Critical: Green cover below 20% - urgent need for afforestation")
    elif green_cover < 30:
        suggestions.append("🌿 Low green cover - implement green infrastructure programs")
    
    if built_area > 60:
        suggestions.append("🏢 High urbanization - recommend cool roof technologies")
    
    if water_cover < 5:
        suggestions.append("💧 Water bodies insufficient - create artificial lakes/ponds")
    
    return suggestions

@app.route('/api/city-data/<city_name>')
def get_city_data(city_name):
    """Get detailed data for a specific city"""
    city = CITY_DATA.get(city_name)
    if not city:
        return jsonify({'success': False, 'error': 'City not found'}), 404
    
    # Predict temperature for this city's features
    features = [city['vegetation'], city['built_area'], city['water'], city['population']]
    predicted_temp = predictor.predict_temperature(features)
    health_analysis = predictor.analyze_urban_health(predicted_temp, features)
    
    city['predicted_temperature'] = predicted_temp
    city['health_analysis'] = health_analysis
    
    return jsonify({
        'success': True,
        'city': city_name,
        'data': city
    })

@app.route('/api/heatmap-data')
def get_heatmap_data():
    """Generate heat map data for all cities"""
    heatmap_points = []
    
    for city_name, data in CITY_DATA.items():
        # Add city center point
        heatmap_points.append({
            'lat': data['center_coordinates'][0],
            'lng': data['center_coordinates'][1],
            'intensity': data['temperature'] / 40,  # Normalize to 0-1
            'city': city_name,
            'temperature': data['temperature']
        })
        
        # Add problem points around the city
        for problem in data['problems']:
            heatmap_points.append({
                'lat': problem['coordinates'][0],
                'lng': problem['coordinates'][1],
                'intensity': 0.7 if problem['severity'] == 'high' else 0.4,
                'type': 'problem',
                'problem': problem['problem'],
                'severity': problem['severity']
            })
    
    return jsonify({
        'success': True,
        'heatmap_data': heatmap_points,
        'cities': list(CITY_DATA.keys())
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        vegetation = float(data.get('vegetation', 0.15))
        built_area = float(data.get('built_area', 0.6))
        water = float(data.get('water', 0.05))
        population = float(data.get('population', 8000))
        
        features = [vegetation, built_area, water, population]
        
        if any(f < 0 for f in features[:3]) or population < 0:
            return jsonify({'success': False, 'error': 'Invalid values'}), 400
        
        if vegetation > 1 or built_area > 1 or water > 1:
            return jsonify({'success': False, 'error': 'Percentages must be between 0 and 1'}), 400
        
        temperature = predictor.predict_temperature(features)
        importance = predictor.get_feature_importance()
        health_analysis = predictor.analyze_urban_health(temperature, features)
        
        logger.info(f"Prediction: {temperature}°C for urban area")
        
        return jsonify({
            'success': True,
            'prediction': temperature,
            'feature_importance': importance,
            'health_analysis': health_analysis,
            'interpretation': get_temperature_interpretation(temperature)
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'error': 'Invalid number format'}), 400
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'success': False, 'error': 'Server error'}), 500

def get_temperature_interpretation(temp):
    """Get human-readable temperature interpretation"""
    if temp < 24:
        return "Cool - Excellent urban planning"
    elif temp < 28:
        return "Comfortable - Good urban health"
    elif temp < 32:
        return "Warm - Needs improvement"
    else:
        return "Hot - Critical intervention needed"

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'NASA Urban Planning API',
        'version': '1.0'
    })

@app.route('/api/model-info')
def model_info():
    """Model information endpoint"""
    return jsonify({
        'model_name': 'NASA Urban Temperature Predictor',
        'version': '1.0',
        'feature_names': predictor.feature_names,
        'description': 'Urban heat island prediction for sustainable planning'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🚀 Starting Enhanced NASA Urban Planner on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)