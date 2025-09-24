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

# Urban Planning Prediction Model
class UrbanPlanningPredictor:
    def __init__(self):
        self.feature_names = ['vegetation', 'built_area', 'water', 'population']
    
    def predict_temperature(self, features):
        """Predict urban temperature based on landscape features"""
        vegetation, built_area, water, population = features
        
        # Physics-based calculations
        base_temp = 22.0
        
        temperature_effect = (
            -8.0 * vegetation +
            10.0 * built_area +
            -6.0 * water +
            0.0003 * population +
            2.0 * (built_area ** 2)
        )
        
        predicted_temp = base_temp + temperature_effect
        return max(15.0, min(45.0, round(predicted_temp, 1)))
    
    def get_feature_importance(self):
        return {
            "vegetation": 0.35,
            "built_area": 0.30,
            "water": 0.20,
            "population": 0.15
        }
    
    def analyze_urban_health(self, temperature, features):
        vegetation, built_area, water, population = features
        
        # Calculate health score
        temp_score = max(0, 100 - abs(temperature - 22) * 4)
        veg_score = min(100, vegetation * 200)
        water_score = min(100, water * 300)
        built_score = max(0, 100 - built_area * 100)
        
        health_score = (temp_score * 0.4 + veg_score * 0.3 + water_score * 0.2 + built_score * 0.1)
        
        # Generate recommendations
        recommendations = []
        
        if vegetation < 0.15:
            recommendations.append("🌳 CRITICAL: Green cover below 15% - implement emergency afforestation")
        elif vegetation < 0.25:
            recommendations.append("🌿 LOW: Increase green spaces to 25-30% for better cooling")
        
        if built_area > 0.65:
            recommendations.append("🏢 HIGH: Built area exceeding 65% - implement cool roof technologies")
        
        if water < 0.03:
            recommendations.append("💧 CRITICAL: Water bodies below 3% - create artificial water features")
        
        if temperature > 33:
            recommendations.append("🔥 EXTREME HEAT: Implement emergency cooling measures")
        elif temperature > 28:
            recommendations.append("⚠️ MODERATE HEAT: Improve urban design for better ventilation")
        
        risk_level = "high" if temperature > 32 else "moderate" if temperature > 28 else "low"
        
        return {
            "health_score": round(health_score),
            "recommendations": recommendations,
            "risk_level": risk_level
        }

# Global predictor instance
predictor = UrbanPlanningPredictor()

# City data
CITY_DATA = {
    'Bhopal': {
        'problems': [
            {'id': 1, 'problem': 'Water Pollution', 'suggestion': 'Install water treatment plants', 'severity': 'high', 'coordinates': [23.25, 77.41]},
            {'id': 2, 'problem': 'Waste Management', 'suggestion': 'Improve segregation and recycling', 'severity': 'medium', 'coordinates': [23.26, 77.43]},
            {'id': 3, 'problem': 'Air Quality', 'suggestion': 'Promote public transportation', 'severity': 'high', 'coordinates': [23.24, 77.42]},
            {'id': 4, 'problem': 'Urban Heat Island', 'suggestion': 'Increase green cover', 'severity': 'medium', 'coordinates': [23.27, 77.40]}
        ],
        'center_coordinates': [23.2599, 77.4126],
        'temperature': 32.5
    },
    'Delhi': {
        'problems': [
            {'id': 1, 'problem': 'Air Pollution', 'suggestion': 'Strict emission controls', 'severity': 'very high', 'coordinates': [28.61, 77.20]},
            {'id': 2, 'problem': 'Traffic Congestion', 'suggestion': 'Develop metro infrastructure', 'severity': 'high', 'coordinates': [28.62, 77.22]}
        ],
        'center_coordinates': [28.6139, 77.2090],
        'temperature': 35.2
    },
    'Mumbai': {
        'problems': [
            {'id': 1, 'problem': 'Flooding', 'suggestion': 'Improve drainage systems', 'severity': 'high', 'coordinates': [19.07, 72.87]},
            {'id': 2, 'problem': 'Overpopulation', 'suggestion': 'Develop satellite cities', 'severity': 'medium', 'coordinates': [19.08, 72.88]}
        ],
        'center_coordinates': [19.0760, 72.8777],
        'temperature': 33.8
    }
}

# Urban area configurations
URBAN_LAYERS = {
    'residential': {'vegetation': 0.25, 'built_area': 0.45, 'water': 0.08, 'population': 6000},
    'commercial': {'vegetation': 0.10, 'built_area': 0.75, 'water': 0.03, 'population': 8000},
    'industrial': {'vegetation': 0.08, 'built_area': 0.80, 'water': 0.05, 'population': 3000},
    'mixed_use': {'vegetation': 0.20, 'built_area': 0.60, 'water': 0.06, 'population': 7000},
    'green_space': {'vegetation': 0.70, 'built_area': 0.10, 'water': 0.15, 'population': 1000},
    'water_body': {'vegetation': 0.05, 'built_area': 0.02, 'water': 0.90, 'population': 500}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze-location', methods=['POST'])
def analyze_location():
    try:
        data = request.get_json()
        lat = data.get('lat', 23.2599)
        lng = data.get('lng', 77.4126)
        area_type = data.get('area_type', 'auto_detect')
        
        # Auto-detect area type or use specified one
        if area_type == 'auto_detect':
            area_type = 'residential'  # Simple detection for demo
            
        base_values = URBAN_LAYERS.get(area_type, URBAN_LAYERS['residential']).copy()
        
        # Add some variation
        for key in base_values:
            if key != 'population':
                base_values[key] = max(0.01, min(0.99, base_values[key] + np.random.uniform(-0.05, 0.05)))
            else:
                base_values[key] = max(1000, base_values[key] + np.random.uniform(-1000, 1000))
        
        analysis = {
            'area_type': area_type,
            'coordinates': [lat, lng],
            'vegetation': round(base_values['vegetation'], 3),
            'built_area': round(base_values['built_area'], 3),
            'water': round(base_values['water'], 3),
            'population': int(base_values['population']),
            'confidence': round(np.random.uniform(0.7, 0.95), 2)
        }
        
        suggestions = generate_area_suggestions(analysis)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'suggestions': suggestions
        })
        
    except Exception as e:
        logger.error(f"Location analysis error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

def generate_area_suggestions(analysis):
    suggestions = []
    vegetation = analysis['vegetation']
    built_area = analysis['built_area']
    area_type = analysis['area_type']
    
    if vegetation < 0.2:
        suggestions.append("🌳 Increase green spaces to reduce heat island effect")
    if built_area > 0.6:
        suggestions.append("🏗️ Optimize building density for better ventilation")
    if area_type == 'commercial' and vegetation < 0.15:
        suggestions.append("🌿 Add green roofs and vertical gardens")
    
    return suggestions

@app.route('/api/urban-layers')
def get_urban_layers():
    return jsonify({
        'success': True,
        'layers': URBAN_LAYERS,
        'cities': list(CITY_DATA.keys())
    })

@app.route('/api/analyze-photo', methods=['POST'])
def analyze_photo():
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Simple image analysis
        image = Image.open(io.BytesIO(image_bytes))
        width, height = image.size
        
        # Mock analysis for demo
        analysis = {
            'green_cover': round(np.random.uniform(10, 40), 1),
            'built_area': round(np.random.uniform(30, 70), 1),
            'water_cover': round(np.random.uniform(2, 10), 1),
            'image_size': f"{width}x{height}"
        }
        
        suggestions = []
        if analysis['green_cover'] < 20:
            suggestions.append("🌳 Low green cover detected - consider planting more trees")
        if analysis['built_area'] > 60:
            suggestions.append("🏢 High urbanization - recommend green infrastructure")
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'suggestions': suggestions
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/city-data/<city_name>')
def get_city_data(city_name):
    city = CITY_DATA.get(city_name)
    if not city:
        return jsonify({'success': False, 'error': 'City not found'}), 404
    
    return jsonify({
        'success': True,
        'city': city_name,
        'data': city
    })

@app.route('/api/heatmap-data')
def get_heatmap_data():
    heatmap_points = []
    
    for city_name, data in CITY_DATA.items():
        heatmap_points.append({
            'lat': data['center_coordinates'][0],
            'lng': data['center_coordinates'][1],
            'intensity': data['temperature'] / 40,
            'city': city_name,
            'temperature': data['temperature']
        })
        
        for problem in data['problems']:
            heatmap_points.append({
                'lat': problem['coordinates'][0],
                'lng': problem['coordinates'][1],
                'intensity': 0.7 if problem['severity'] == 'high' else 0.4,
                'problem': problem['problem'],
                'severity': problem['severity']
            })
    
    return jsonify({
        'success': True,
        'heatmap_data': heatmap_points
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        vegetation = float(data.get('vegetation', 0.25))
        built_area = float(data.get('built_area', 0.45))
        water = float(data.get('water', 0.08))
        population = float(data.get('population', 6000))
        
        features = [vegetation, built_area, water, population]
        temperature = predictor.predict_temperature(features)
        importance = predictor.get_feature_importance()
        health_analysis = predictor.analyze_urban_health(temperature, features)
        
        interpretation = get_temperature_interpretation(temperature)
        
        return jsonify({
            'success': True,
            'prediction': temperature,
            'feature_importance': importance,
            'health_analysis': health_analysis,
            'interpretation': interpretation
        })
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

def get_temperature_interpretation(temp):
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
    return jsonify({'status': 'healthy', 'service': 'NASA Urban Planner'})

@app.route('/api/model-info')
def model_info():
    return jsonify({
        'model_name': 'NASA Urban Temperature Predictor',
        'features': predictor.feature_names
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🚀 NASA Urban Planner starting on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)