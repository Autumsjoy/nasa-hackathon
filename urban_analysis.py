import json
import os
import pandas as pd
from config import Config
from nasa_data_integration import NASADataIntegration

class UrbanAnalysis:
    def __init__(self):
        self.config = Config()
        self.nasa_integration = NASADataIntegration()
        self.areas_data = self.load_areas_data()
    
    def load_areas_data(self):
        """Load Bhopal areas data with NASA integration"""
        try:
            with open(self.config.BHOPAL_DATA_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.generate_nasa_integrated_data()
    
    def generate_nasa_integrated_data(self):
        """Generate NASA-integrated urban data for Bhopal"""
        areas = {
            "old_bhopal": {
                "id": "old_bhopal",
                "name": "Old Bhopal",
                "type": "Mixed Use",
                "coordinates": [23.2599, 77.4126],
                "nasa_metrics": {
                    "surface_temperature": 35.8,
                    "urban_heat_index": 8.2,
                    "vegetation_health": 0.35,
                    "air_quality_index": 156
                },
                "environmental_data": {
                    "temperature": 35.8,
                    "population_density": 12000,
                    "green_cover": 15.0,
                    "pollution_index": 82,
                    "sustainability_score": 45
                },
                "energy_consumption": {
                    "grid_electricity": 72,
                    "solar_energy": 15,
                    "battery_storage": 8,
                    "generator_backup": 5,
                    "carbon_footprint": 8.5
                },
                "transportation": {
                    "private_vehicles": 45,
                    "public_transport": 30,
                    "two_wheelers": 15,
                    "walking_cycling": 10,
                    "congestion_level": "High"
                },
                "key_concerns": [
                    "High urban heat island effect",
                    "Low green cover",
                    "Traffic congestion",
                    "Air pollution"
                ],
                "nasa_insights": [
                    "High surface temperature detected",
                    "Low vegetation index",
                    "Poor air quality"
                ]
            },
            "new_bhopal": {
                "id": "new_bhopal",
                "name": "New Bhopal", 
                "type": "Residential/Commercial",
                "coordinates": [23.2183, 77.4010],
                "nasa_metrics": {
                    "surface_temperature": 32.5,
                    "urban_heat_index": 5.1,
                    "vegetation_health": 0.52,
                    "air_quality_index": 89
                },
                "environmental_data": {
                    "temperature": 32.5,
                    "population_density": 8500,
                    "green_cover": 28.0,
                    "pollution_index": 56,
                    "sustainability_score": 68
                },
                "energy_consumption": {
                    "grid_electricity": 65,
                    "solar_energy": 22,
                    "battery_storage": 10,
                    "generator_backup": 3,
                    "carbon_footprint": 6.2
                },
                "transportation": {
                    "private_vehicles": 40,
                    "public_transport": 35,
                    "two_wheelers": 15,
                    "walking_cycling": 10,
                    "congestion_level": "Moderate"
                },
                "key_concerns": [
                    "Moderate pollution",
                    "Urban sprawl",
                    "Infrastructure development"
                ],
                "nasa_insights": [
                    "Moderate surface temperature",
                    "Average vegetation health",
                    "Moderate air quality"
                ]
            },
            "shahpura": {
                "id": "shahpura",
                "name": "Shahpura",
                "type": "Residential",
                "coordinates": [23.2456, 77.4321],
                "nasa_metrics": {
                    "surface_temperature": 33.2,
                    "urban_heat_index": 6.8,
                    "vegetation_health": 0.41,
                    "air_quality_index": 112
                },
                "environmental_data": {
                    "temperature": 33.2,
                    "population_density": 9200,
                    "green_cover": 22.5,
                    "pollution_index": 68,
                    "sustainability_score": 58
                },
                "energy_consumption": {
                    "grid_electricity": 70,
                    "solar_energy": 18,
                    "battery_storage": 8,
                    "generator_backup": 4,
                    "carbon_footprint": 7.1
                },
                "transportation": {
                    "private_vehicles": 42,
                    "public_transport": 32,
                    "two_wheelers": 16,
                    "walking_cycling": 10,
                    "congestion_level": "High"
                },
                "key_concerns": [
                    "Water scarcity",
                    "Traffic congestion", 
                    "Air pollution"
                ],
                "nasa_insights": [
                    "Elevated surface temperature",
                    "Below average vegetation",
                    "Poor air quality periods"
                ]
            },
            "kolar": {
                "id": "kolar",
                "name": "Kolar",
                "type": "Suburban/Residential",
                "coordinates": [23.1654, 77.3854],
                "nasa_metrics": {
                    "surface_temperature": 31.8,
                    "urban_heat_index": 4.2,
                    "vegetation_health": 0.68,
                    "air_quality_index": 75
                },
                "environmental_data": {
                    "temperature": 31.8,
                    "population_density": 6500,
                    "green_cover": 35.0,
                    "pollution_index": 48,
                    "sustainability_score": 78
                },
                "energy_consumption": {
                    "grid_electricity": 60,
                    "solar_energy": 28,
                    "battery_storage": 9,
                    "generator_backup": 3,
                    "carbon_footprint": 5.4
                },
                "transportation": {
                    "private_vehicles": 38,
                    "public_transport": 38,
                    "two_wheelers": 14,
                    "walking_cycling": 10,
                    "congestion_level": "Low"
                },
                "key_concerns": [
                    "Urban sprawl",
                    "Public transport connectivity"
                ],
                "nasa_insights": [
                    "Lower surface temperature",
                    "Good vegetation coverage", 
                    "Better air quality"
                ]
            },
            "indrapuri": {
                "id": "indrapuri", 
                "name": "Indrapuri",
                "type": "Residential",
                "coordinates": [23.2287, 77.4456],
                "nasa_metrics": {
                    "surface_temperature": 32.0,
                    "urban_heat_index": 4.8,
                    "vegetation_health": 0.58,
                    "air_quality_index": 85
                },
                "environmental_data": {
                    "temperature": 32.0,
                    "population_density": 7800,
                    "green_cover": 30.5,
                    "pollution_index": 52,
                    "sustainability_score": 72
                },
                "energy_consumption": {
                    "grid_electricity": 62,
                    "solar_energy": 25,
                    "battery_storage": 10,
                    "generator_backup": 3,
                    "carbon_footprint": 5.8
                },
                "transportation": {
                    "private_vehicles": 35,
                    "public_transport": 40,
                    "two_wheelers": 15,
                    "walking_cycling": 10,
                    "congestion_level": "Moderate"
                },
                "key_concerns": [
                    "Parking issues",
                    "Waste management"
                ],
                "nasa_insights": [
                    "Moderate temperature",
                    "Healthy vegetation",
                    "Acceptable air quality"
                ]
            },
            "bhopal_lake": {
                "id": "bhopal_lake",
                "name": "Bhopal Lake Area",
                "type": "Recreational/Residential", 
                "coordinates": [23.2599, 77.4065],
                "nasa_metrics": {
                    "surface_temperature": 30.2,
                    "urban_heat_index": 2.1,
                    "vegetation_health": 0.82,
                    "air_quality_index": 45
                },
                "environmental_data": {
                    "temperature": 30.2,
                    "population_density": 5200,
                    "green_cover": 40.5,
                    "pollution_index": 32,
                    "sustainability_score": 88
                },
                "energy_consumption": {
                    "grid_electricity": 55,
                    "solar_energy": 35,
                    "battery_storage": 8,
                    "generator_backup": 2,
                    "carbon_footprint": 4.2
                },
                "transportation": {
                    "private_vehicles": 30,
                    "public_transport": 45,
                    "two_wheelers": 10,
                    "walking_cycling": 15,
                    "congestion_level": "Low"
                },
                "key_concerns": [
                    "Lake conservation",
                    "Tourist management"
                ],
                "nasa_insights": [
                    "Coolest area in city",
                    "Excellent vegetation",
                    "Best air quality"
                ]
            },
            "industrial_area": {
                "id": "industrial_area",
                "name": "Industrial Area",
                "type": "Industrial",
                "coordinates": [23.1987, 77.4567],
                "nasa_metrics": {
                    "surface_temperature": 37.5,
                    "urban_heat_index": 12.8,
                    "vegetation_health": 0.18,
                    "air_quality_index": 245
                },
                "environmental_data": {
                    "temperature": 37.5,
                    "population_density": 3800,
                    "green_cover": 12.5,
                    "pollution_index": 95,
                    "sustainability_score": 28
                },
                "energy_consumption": {
                    "grid_electricity": 80,
                    "solar_energy": 8,
                    "battery_storage": 5,
                    "generator_backup": 7,
                    "carbon_footprint": 12.3
                },
                "transportation": {
                    "private_vehicles": 50,
                    "public_transport": 25,
                    "two_wheelers": 15,
                    "walking_cycling": 10,
                    "congestion_level": "Moderate"
                },
                "key_concerns": [
                    "Severe pollution",
                    "Industrial waste",
                    "Worker safety"
                ],
                "nasa_insights": [
                    "Highest surface temperature",
                    "Very poor vegetation",
                    "Critical air quality"
                ]
            }
        }
        
        # Calculate sustainability scores with NASA data
        for area_id, area_data in areas.items():
            area_data['environmental_data']['sustainability_score'] = \
                self.nasa_integration.calculate_urban_sustainability_score(area_data['environmental_data'])
        
        # Save to file
        os.makedirs('data', exist_ok=True)
        with open(self.config.BHOPAL_DATA_FILE, 'w') as f:
            json.dump(areas, f, indent=2)
            
        return areas
    
    def get_area_analysis(self, area_id):
        """Get comprehensive analysis for a specific area"""
        area_data = self.areas_data.get(area_id)
        if not area_data:
            return {"error": "Area not found"}
        
        nasa_data = self.nasa_integration.get_urban_heat_island_data()
        
        analysis = {
            "area_info": area_data,
            "nasa_analysis": {
                "satellite_data": nasa_data,
                "urban_heat_island": self.analyze_heat_island(area_data),
                "environmental_impact": self.analyze_environmental_impact(area_data),
                "sustainability_metrics": self.calculate_sustainability_metrics(area_data)
            },
            "recommendations": self.generate_nasa_recommendations(area_data)
        }
        
        return analysis
    
    def analyze_heat_island(self, area_data):
        """Analyze urban heat island effect using NASA data"""
        temp = area_data['nasa_metrics']['surface_temperature']
        heat_index = area_data['nasa_metrics']['urban_heat_index']
        
        return {
            "effect_level": "Severe" if heat_index > 8 else "High" if heat_index > 5 else "Moderate",
            "temperature_impact": f"+{heat_index}°C above rural areas",
            "mitigation_potential": "High" if heat_index > 6 else "Medium"
        }
    
    def analyze_environmental_impact(self, area_data):
        """Analyze environmental impact using NASA metrics"""
        vegetation = area_data['nasa_metrics']['vegetation_health']
        air_quality = area_data['nasa_metrics']['air_quality_index']
        
        return {
            "vegetation_status": "Healthy" if vegetation > 0.6 else "Moderate" if vegetation > 0.4 else "Poor",
            "air_quality_status": "Good" if air_quality < 50 else "Moderate" if air_quality < 100 else "Unhealthy",
            "carbon_footprint": area_data['energy_consumption']['carbon_footprint']
        }
    
    def calculate_sustainability_metrics(self, area_data):
        """Calculate NASA-inspired sustainability metrics"""
        env_data = area_data['environmental_data']
        nasa_metrics = area_data['nasa_metrics']
        
        return {
            "overall_score": env_data['sustainability_score'],
            "climate_resilience": max(0, 100 - nasa_metrics['urban_heat_index'] * 8),
            "environmental_health": (nasa_metrics['vegetation_health'] * 100 + (100 - nasa_metrics['air_quality_index'] / 3)) / 2,
            "energy_efficiency": 100 - env_data['energy_consumption']['grid_electricity']
        }
    
    def generate_nasa_recommendations(self, area_data):
        """Generate NASA-data-driven recommendations"""
        recommendations = []
        nasa_metrics = area_data['nasa_metrics']
        
        # Heat island mitigation
        if nasa_metrics['urban_heat_index'] > 6:
            recommendations.extend([
                "Implement cool roof technologies using NASA-reflective materials",
                "Increase urban greenery based on NASA vegetation analysis",
                "Create ventilation corridors using wind pattern data"
            ])
        
        # Air quality improvements
        if nasa_metrics['air_quality_index'] > 100:
            recommendations.extend([
                "Deploy NASA-inspired air purification systems",
                "Promote electric mobility using renewable energy",
                "Implement green barriers using NASA vegetation data"
            ])
        
        # Energy efficiency
        if area_data['energy_consumption']['solar_energy'] < 25:
            recommendations.extend([
                "Install rooftop solar panels using NASA solar irradiance data",
                "Implement smart grid technologies",
                "Promote energy-efficient building designs"
            ])
        
        # Transportation
        if area_data['transportation']['private_vehicles'] > 40:
            recommendations.extend([
                "Develop NASA-inspired public transport optimization",
                "Create pedestrian-friendly infrastructure",
                "Implement smart traffic management systems"
            ])
        
        return recommendations
    
    def get_comparative_analysis(self):
        """Get comparative analysis across all areas"""
        comparison_data = {}
        
        for area_id, area_data in self.areas_data.items():
            comparison_data[area_id] = {
                "name": area_data["name"],
                "sustainability_score": area_data["environmental_data"]["sustainability_score"],
                "nasa_metrics": area_data["nasa_metrics"],
                "environmental_data": area_data["environmental_data"]
            }
        
        return comparison_data