from flask import Flask, render_template, jsonify
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')

class UrbanPlanningPredictor:
    def __init__(self):
        self.feature_names = ['vegetation', 'built_area', 'water', 'population']
    
    def predict_temperature(self, features):
        vegetation, built_area, water, population = features
        
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
        
        temp_score = max(0, 100 - abs(temperature - 22) * 4)
        veg_score = min(100, vegetation * 200)
        water_score = min(100, water * 300)
        built_score = max(0, 100 - built_area * 100)
        
        health_score = (temp_score * 0.4 + veg_score * 0.3 + water_score * 0.2 + built_score * 0.1)
        
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

predictor = UrbanPlanningPredictor()

# Bhopal-specific data
BHOPAL_DATA = {
    "name": "Bhopal",
    "population": "2.5 million",
    "area": "285 km²",
    "temperature_range": "15°C - 40°C",
    "current_temperature": 32.5,
    "center_coordinates": [23.2599, 77.4126],
    
    "urban_areas": [
        {
            "name": "New Bhopal (Arera Colony)",
            "coordinates": [23.2456, 77.4037],
            "type": "residential",
            "vegetation": 0.30,
            "built_area": 0.45,
            "water": 0.08,
            "population_density": 5500,
            "temperature": 30.2,
            "concerns": ["Good green cover", "Moderate density", "Well planned"],
            "color": "#4ECDC4"
        },
        {
            "name": "Old Bhopal",
            "coordinates": [23.2650, 77.4030],
            "type": "mixed_use",
            "vegetation": 0.15,
            "built_area": 0.70,
            "water": 0.03,
            "population_density": 12000,
            "temperature": 35.8,
            "concerns": ["High density", "Low green cover", "Traffic congestion", "Air pollution"],
            "color": "#FF6B6B"
        },
        {
            "name": "MP Nagar (Commercial)",
            "coordinates": [23.2350, 77.4150],
            "type": "commercial",
            "vegetation": 0.10,
            "built_area": 0.75,
            "water": 0.02,
            "population_density": 8000,
            "temperature": 34.5,
            "concerns": ["Urban heat island", "High traffic", "Low vegetation", "Parking issues"],
            "color": "#FFA726"
        },
        {
            "name": "Shahpura Lake Area",
            "coordinates": [23.2286, 77.4382],
            "type": "green_space",
            "vegetation": 0.60,
            "built_area": 0.20,
            "water": 0.15,
            "population_density": 3000,
            "temperature": 28.5,
            "concerns": ["Water pollution", "Encroachment", "Maintenance needed"],
            "color": "#66BB6A"
        },
        {
            "name": "Bhopal Railway Station",
            "coordinates": [23.2696, 77.4350],
            "type": "industrial",
            "vegetation": 0.08,
            "built_area": 0.80,
            "water": 0.04,
            "population_density": 6000,
            "temperature": 36.2,
            "concerns": ["Air pollution", "Noise pollution", "Traffic congestion", "Waste management"],
            "color": "#6C63FF"
        },
        {
            "name": "Bhadbhada Road (Industrial)",
            "coordinates": [23.2200, 77.4250],
            "type": "industrial",
            "vegetation": 0.05,
            "built_area": 0.85,
            "water": 0.03,
            "population_density": 4000,
            "temperature": 37.1,
            "concerns": ["Industrial pollution", "Low green cover", "Water contamination risk"],
            "color": "#9575CD"
        }
    ],
    
    "major_problems": [
        {
            "id": 1,
            "problem": "Water Pollution in Upper Lake",
            "severity": "high",
            "coordinates": [23.2583, 77.4125],
            "description": "Contamination from urban runoff and industrial waste",
            "impact": "Affects drinking water supply and aquatic life",
            "solutions": ["Install water treatment plants", "Prevent sewage discharge", "Create buffer zones"]
        },
        {
            "id": 2,
            "problem": "Urban Heat Island Effect",
            "severity": "high",
            "coordinates": [23.2550, 77.4080],
            "description": "Temperature 5-7°C higher than surrounding rural areas",
            "impact": "Increased energy consumption, health risks",
            "solutions": ["Increase green cover", "Use cool roofing materials", "Create urban forests"]
        },
        {
            "id": 3,
            "problem": "Traffic Congestion in City Center",
            "severity": "medium",
            "coordinates": [23.2599, 77.4126],
            "description": "Peak hour traffic jams affecting mobility",
            "impact": "Air pollution, time loss, economic impact",
            "solutions": ["Improve public transport", "Develop bypass roads", "Promote cycling"]
        },
        {
            "id": 4,
            "problem": "Waste Management Issues",
            "severity": "medium",
            "coordinates": [23.2500, 77.4200],
            "description": "Inefficient waste collection and disposal systems",
            "impact": "Health hazards, environmental pollution",
            "solutions": ["Improve segregation systems", "Increase recycling", "Public awareness campaigns"]
        },
        {
            "id": 5,
            "problem": "Air Quality Deterioration",
            "severity": "high",
            "coordinates": [23.2450, 77.4150],
            "description": "PM2.5 and PM10 levels exceeding safe limits",
            "impact": "Respiratory diseases, environmental damage",
            "solutions": ["Strict emission controls", "Promote electric vehicles", "Industrial regulations"]
        },
        {
            "id": 6,
            "problem": "Groundwater Depletion",
            "severity": "medium",
            "coordinates": [23.2400, 77.4100],
            "description": "Over-extraction leading to falling water tables",
            "impact": "Water scarcity, land subsidence risk",
            "solutions": ["Rainwater harvesting", "Water conservation", "Artificial recharge"]
        }
    ],
    
    "heatmap_data": [
        {"lat": 23.2456, "lng": 77.4037, "intensity": 0.4, "type": "residential", "temperature": 30.2},
        {"lat": 23.2650, "lng": 77.4030, "intensity": 0.8, "type": "mixed_use", "temperature": 35.8},
        {"lat": 23.2350, "lng": 77.4150, "intensity": 0.7, "type": "commercial", "temperature": 34.5},
        {"lat": 23.2286, "lng": 77.4382, "intensity": 0.2, "type": "green_space", "temperature": 28.5},
        {"lat": 23.2696, "lng": 77.4350, "intensity": 0.9, "type": "industrial", "temperature": 36.2},
        {"lat": 23.2200, "lng": 77.4250, "intensity": 1.0, "type": "industrial", "temperature": 37.1}
    ]
}

@app.route('/')
def home():
    return render_template('index.html', bhopal_data=BHOPAL_DATA)

@app.route('/api/analyze-area/<area_name>')
def analyze_area(area_name):
    area = next((a for a in BHOPAL_DATA["urban_areas"] if a["name"] == area_name), None)
    if not area:
        return jsonify({"success": False, "error": "Area not found"})
    
    features = [area["vegetation"], area["built_area"], area["water"], area["population_density"]]
    temperature = predictor.predict_temperature(features)
    importance = predictor.get_feature_importance()
    health_analysis = predictor.analyze_urban_health(temperature, features)
    
    return jsonify({
        "success": True,
        "area": area,
        "prediction": temperature,
        "feature_importance": importance,
        "health_analysis": health_analysis,
        "interpretation": get_temperature_interpretation(temperature)
    })

@app.route('/api/bhopal-data')
def get_bhopal_data():
    return jsonify({"success": True, "data": BHOPAL_DATA})

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = {
            "vegetation": 0.25,
            "built_area": 0.45, 
            "water": 0.08,
            "population": 6000
        }
        
        features = [data["vegetation"], data["built_area"], data["water"], data["population"]]
        temperature = predictor.predict_temperature(features)
        importance = predictor.get_feature_importance()
        health_analysis = predictor.analyze_urban_health(temperature, features)
        
        return jsonify({
            "success": True,
            "prediction": temperature,
            "feature_importance": importance,
            "health_analysis": health_analysis,
            "interpretation": get_temperature_interpretation(temperature)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def get_temperature_interpretation(temp):
    if temp < 24:
        return "Cool - Excellent urban planning"
    elif temp < 28:
        return "Comfortable - Good urban health"
    elif temp < 32:
        return "Warm - Needs improvement"
    else:
        return "Hot - Critical intervention needed"

if __name__ == '__main__':
    port = 10000
    logger.info(f"🚀 Bhopal Urban Planning Dashboard starting on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)