import numpy as np

class UrbanPlanningPredictor:
    def __init__(self):
        self.feature_names = ['vegetation', 'built_area', 'water', 'population']
    
    def predict_temperature(self, features):
        """Predict urban temperature based on landscape features"""
        vegetation, built_area, water, population = features
        
        # Enhanced physics-based calculations
        base_temp = 22.0  # Ideal base temperature
        
        temperature_effect = (
            -8.0 * vegetation +           # Vegetation cooling effect
            10.0 * built_area +           # Built area heating effect
            -6.0 * water +                # Water cooling effect
            0.0003 * population +         # Population density effect
            2.0 * (built_area ** 2)       # Non-linear urban heat island effect
        )
        
        predicted_temp = base_temp + temperature_effect
        return max(15.0, min(45.0, round(predicted_temp, 1)))  # Realistic bounds
    
    def get_feature_importance(self):
        """Return feature importance based on urban research"""
        return {
            "vegetation": 0.35,
            "built_area": 0.30, 
            "water": 0.20,
            "population": 0.15
        }
    
    def analyze_urban_health(self, temperature, features):
        """Enhanced urban health analysis"""
        vegetation, built_area, water, population = features
        
        # Multi-factor health score
        temp_score = max(0, 100 - abs(temperature - 22) * 4)
        veg_score = min(100, vegetation * 200)
        water_score = min(100, water * 300)
        built_score = max(0, 100 - built_area * 100)
        
        health_score = (temp_score * 0.4 + veg_score * 0.3 + water_score * 0.2 + built_score * 0.1)
        
        # Generate detailed recommendations
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
        
        # Enhanced risk assessment
        risk_factors = []
        if vegetation < 0.2: risk_factors.append("low_green_cover")
        if built_area > 0.6: risk_factors.append("high_urbanization") 
        if temperature > 30: risk_factors.append("heat_risk")
        
        risk_level = "high" if len(risk_factors) >= 2 else "moderate" if risk_factors else "low"
        
        return {
            "health_score": round(health_score),
            "recommendations": recommendations,
            "risk_level": risk_level,
            "risk_factors": risk_factors
        }

# Global instance
predictor = UrbanPlanningPredictor()