import pandas as pd
import numpy as np
import json
from datetime import datetime

class BhopalDataProcessor:
    def __init__(self):
        self.areas = {
            "old_bhopal": {
                "name": "Old Bhopal",
                "lat": 23.2599, "lon": 77.4126,
                "type": "Mixed Use", "temperature": 35.8,
                "population_density": 12000, "green_cover": 15.0,
                "pollution_index": 82,
                "energy_consumption": {
                    "grid_electricity": 72, "solar_energy": 15,
                    "battery_storage": 8, "generator_backup": 5
                },
                "transportation": {
                    "private_vehicles": 45, "public_transport": 30,
                    "two_wheelers": 15, "walking_cycling": 10
                },
                "key_concerns": [
                    "High density", "Low green cover",
                    "Traffic congestion", "Air pollution"
                ]
            },
            "new_bhopal": {
                "name": "New Bhopal",
                "lat": 23.2278, "lon": 77.4357,
                "type": "Residential/Commercial", "temperature": 32.5,
                "population_density": 8500, "green_cover": 28.0,
                "pollution_index": 56,
                "energy_consumption": {
                    "grid_electricity": 65, "solar_energy": 22,
                    "battery_storage": 10, "generator_backup": 3
                },
                "transportation": {
                    "private_vehicles": 40, "public_transport": 35,
                    "two_wheelers": 15, "walking_cycling": 10
                },
                "key_concerns": [
                    "Moderate pollution", "Infrastructure development",
                    "Waste management"
                ]
            },
            "shahpura": {
                "name": "Shahpura",
                "lat": 23.3000, "lon": 77.3667,
                "type": "Residential", "temperature": 33.2,
                "population_density": 9200, "green_cover": 22.5,
                "pollution_index": 68,
                "energy_consumption": {
                    "grid_electricity": 70, "solar_energy": 18,
                    "battery_storage": 8, "generator_backup": 4
                },
                "transportation": {
                    "private_vehicles": 42, "public_transport": 32,
                    "two_wheelers": 16, "walking_cycling": 10
                },
                "key_concerns": [
                    "Water scarcity", "Traffic congestion", "Air pollution"
                ]
            },
            "kolar": {
                "name": "Kolar",
                "lat": 23.1667, "lon": 77.4333,
                "type": "Suburban/Residential", "temperature": 31.8,
                "population_density": 6500, "green_cover": 35.0,
                "pollution_index": 48,
                "energy_consumption": {
                    "grid_electricity": 60, "solar_energy": 28,
                    "battery_storage": 9, "generator_backup": 3
                },
                "transportation": {
                    "private_vehicles": 38, "public_transport": 38,
                    "two_wheelers": 14, "walking_cycling": 10
                },
                "key_concerns": [
                    "Urban sprawl", "Public transport connectivity"
                ]
            },
            "indrapuri": {
                "name": "Indrapuri",
                "lat": 23.2800, "lon": 77.4200,
                "type": "Residential", "temperature": 32.0,
                "population_density": 7800, "green_cover": 30.5,
                "pollution_index": 52,
                "energy_consumption": {
                    "grid_electricity": 62, "solar_energy": 25,
                    "battery_storage": 10, "generator_backup": 3
                },
                "transportation": {
                    "private_vehicles": 35, "public_transport": 40,
                    "two_wheelers": 15, "walking_cycling": 10
                },
                "key_concerns": [
                    "Parking issues", "Waste management"
                ]
            },
            "bhopal_lake": {
                "name": "Bhopal Lake Area",
                "lat": 23.2667, "lon": 77.4000,
                "type": "Recreational/Residential", "temperature": 30.2,
                "population_density": 5200, "green_cover": 40.5,
                "pollution_index": 32,
                "energy_consumption": {
                    "grid_electricity": 55, "solar_energy": 35,
                    "battery_storage": 8, "generator_backup": 2
                },
                "transportation": {
                    "private_vehicles": 30, "public_transport": 45,
                    "two_wheelers": 10, "walking_cycling": 15
                },
                "key_concerns": [
                    "Lake conservation", "Tourist management"
                ]
            },
            "industrial_area": {
                "name": "Industrial Area",
                "lat": 23.2000, "lon": 77.4500,
                "type": "Industrial", "temperature": 37.5,
                "population_density": 3800, "green_cover": 12.5,
                "pollution_index": 95,
                "energy_consumption": {
                    "grid_electricity": 80, "solar_energy": 8,
                    "battery_storage": 5, "generator_backup": 7
                },
                "transportation": {
                    "private_vehicles": 50, "public_transport": 25,
                    "two_wheelers": 15, "walking_cycling": 10
                },
                "key_concerns": [
                    "Severe pollution", "Industrial waste", "Worker safety"
                ]
            }
        }
    
    def calculate_transport_index(self, area_data):
        transport = area_data.get('transportation', {})
        public_transport = transport.get('public_transport', 0)
        walking_cycling = transport.get('walking_cycling', 0)
        private_vehicles = transport.get('private_vehicles', 0)
        
        transport_index = (
            public_transport * 0.4 +
            walking_cycling * 0.3 +
            (100 - private_vehicles) * 0.3
        )
        
        return min(100, max(0, transport_index))
    
    def calculate_pollution_index(self, area_data, nasa_air_data=None):
        base_pollution = area_data.get('pollution_index', 50)
        
        if nasa_air_data and not nasa_air_data.get('simulated', True):
            try:
                nasa_pollution = (
                    nasa_air_data.get('pm25', 0) * 0.3 +
                    nasa_air_data.get('pm10', 0) * 0.3 +
                    nasa_air_data.get('no2', 0) * 0.2 +
                    nasa_air_data.get('so2', 0) * 0.2
                )
                pollution_index = (base_pollution * 0.7 + nasa_pollution * 0.3)
            except:
                pollution_index = base_pollution
        else:
            pollution_index = base_pollution
        
        green_cover = area_data.get('green_cover', 0)
        pollution_adjustment = (100 - green_cover) / 2
        pollution_index = min(100, pollution_index + pollution_adjustment / 10)
        
        return min(100, max(0, pollution_index))
    
    def calculate_energy_index(self, area_data, nasa_solar_data=None):
        energy_consumption = area_data.get('energy_consumption', {})
        solar_energy = energy_consumption.get('solar_energy', 0)
        battery_storage = energy_consumption.get('battery_storage', 0)
        grid_electricity = energy_consumption.get('grid_electricity', 0)
        generator_backup = energy_consumption.get('generator_backup', 0)
        
        renewable_score = solar_energy + battery_storage
        non_renewable_score = grid_electricity + generator_backup
        
        energy_index = (
            renewable_score * 0.7 +
            (100 - non_renewable_score) * 0.3
        )
        
        if nasa_solar_data and not nasa_solar_data.get('simulated', True):
            try:
                solar_radiation = nasa_solar_data.get('properties', {}).get('parameter', {})
                if 'ALLSKY_SFC_SW_DWN' in solar_radiation:
                    radiation_values = list(solar_radiation['ALLSKY_SFC_SW_DWN'].values())
                    if radiation_values:
                        avg_radiation = np.mean(list(radiation_values)[:30])
                        solar_boost = min(20, (avg_radiation - 4) * 5)
                        energy_index += solar_boost
            except:
                pass
        
        return min(100, max(0, energy_index))
    
    def calculate_sustainability_score(self, transport_idx, pollution_idx, energy_idx):
        sustainability_score = (
            transport_idx * 0.25 +
            (100 - pollution_idx) * 0.40 +
            energy_idx * 0.35
        )
        
        return min(100, max(0, sustainability_score))
    
    def calculate_enhanced_sustainability_score(self, transport_idx, pollution_idx, energy_idx, modis_vegetation, landsat_indices):
        base_score = (
            transport_idx * 0.25 +
            (100 - pollution_idx) * 0.35 +
            energy_idx * 0.30
        )
        
        vegetation_boost = modis_vegetation.get('ndvi', 0.5) * 10
        urbanization_penalty = landsat_indices.get('ndbi', 0) * 5
        
        enhanced_score = base_score + vegetation_boost - urbanization_penalty
        
        return min(100, max(0, enhanced_score))
    
    def analyze_energy_resources(self, area_data, nasa_solar_data):
        energy_consumption = area_data.get('energy_consumption', {})
        solar_percentage = energy_consumption.get('solar_energy', 0)
        
        if nasa_solar_data and not nasa_solar_data.get('simulated', False):
            try:
                solar_radiation = nasa_solar_data.get('properties', {}).get('parameter', {})
                if 'ALLSKY_SFC_SW_DWN' in solar_radiation:
                    radiation_values = list(solar_radiation['ALLSKY_SFC_SW_DWN'].values())
                    if radiation_values:
                        avg_radiation = np.mean(list(radiation_values)[:30])
                    else:
                        avg_radiation = 5.2
                else:
                    avg_radiation = 5.2
            except:
                avg_radiation = 5.2
        else:
            avg_radiation = 5.2
        
        solar_potential_score = (avg_radiation / 8) * 100
        
        if solar_potential_score >= 75 and solar_percentage >= 25:
            capacity = 'Excellent'
        elif solar_potential_score >= 65 and solar_percentage >= 20:
            capacity = 'Very High'
        elif solar_potential_score >= 55 and solar_percentage >= 15:
            capacity = 'High'
        elif solar_potential_score >= 45 and solar_percentage >= 10:
            capacity = 'Medium'
        elif solar_potential_score >= 35 and solar_percentage >= 5:
            capacity = 'Low'
        else:
            capacity = 'Very Low'
        
        return {
            'solar_potential': round(avg_radiation, 2),
            'solar_percentage': solar_percentage,
            'renewable_capacity': capacity,
            'grid_dependency': energy_consumption.get('grid_electricity', 0)
        }
    
    def generate_area_analysis(self, nasa_api):
        analysis_results = {}
        
        for area_key, area_data in self.areas.items():
            print(f"Processing {area_data['name']} with MODIS and Landsat data...")
            
            coords = {'lat': area_data['lat'], 'lon': area_data['lon']}
            
            # Get all NASA data sources
            air_quality = nasa_api.get_air_quality_data(area_data['lat'], area_data['lon'])
            solar_data = nasa_api.get_solar_energy_data(area_data['lat'], area_data['lon'])
            modis_vegetation = nasa_api.get_modis_vegetation_data(area_data['lat'], area_data['lon'])
            modis_temperature = nasa_api.get_modis_land_surface_temperature(area_data['lat'], area_data['lon'])
            modis_land_cover = nasa_api.get_modis_land_cover(area_data['lat'], area_data['lon'])
            landsat_metadata = nasa_api.get_landsat_imagery_metadata(area_data['lat'], area_data['lon'])
            landsat_indices = nasa_api.get_landsat_vegetation_indices(area_data['lat'], area_data['lon'])
            satellite_img = nasa_api.get_satellite_imagery(area_data['lat'], area_data['lon'])
            
            # Calculate indices
            transport_idx = self.calculate_transport_index(area_data)
            pollution_idx = self.calculate_pollution_index(area_data, air_quality)
            energy_idx = self.calculate_energy_index(area_data, solar_data)
            energy_analysis = self.analyze_energy_resources(area_data, solar_data)
            
            # Enhanced sustainability score
            sustainability_score = self.calculate_enhanced_sustainability_score(
                transport_idx, pollution_idx, energy_idx, modis_vegetation, landsat_indices
            )
            
            analysis_results[area_key] = {
                'name': area_data['name'],
                'type': area_data['type'],
                'coordinates': coords,
                'transport_index': round(transport_idx, 2),
                'pollution_index': round(pollution_idx, 2),
                'energy_index': round(energy_idx, 2),
                'sustainability_score': round(sustainability_score, 2),
                'solar_potential': energy_analysis['solar_potential'],
                'solar_percentage': energy_analysis['solar_percentage'],
                'renewable_capacity': energy_analysis['renewable_capacity'],
                'grid_dependency': energy_analysis['grid_dependency'],
                'temperature': modis_temperature['daytime_temperature'],
                'urban_heat_intensity': modis_temperature['urban_heat_intensity'],
                'population_density': area_data['population_density'],
                'green_cover': area_data['green_cover'],
                
                # MODIS Data
                'modis_vegetation': modis_vegetation,
                'modis_land_cover': modis_land_cover,
                'modis_temperature': modis_temperature,
                
                # Landsat Data
                'landsat_indices': landsat_indices,
                'landsat_metadata': landsat_metadata,
                
                'vegetation_index': landsat_indices['ndvi'],
                'urbanization_index': landsat_indices['ndbi'],
                'vegetation_health': landsat_indices['vegetation_health'],
                'urbanization_level': landsat_indices['urbanization_level'],
                
                'air_quality_data': air_quality,
                'key_concerns': area_data['key_concerns'],
                'transportation_breakdown': area_data['transportation'],
                'energy_breakdown': area_data['energy_consumption'],
                'satellite_image': satellite_img,
                'data_sources': {
                    'air_quality': air_quality.get('source', 'Simulated'),
                    'solar_data': 'NASA POWER API' if not solar_data.get('simulated', True) else 'Simulated',
                    'modis_vegetation': modis_vegetation.get('source', 'MODIS'),
                    'modis_land_cover': modis_land_cover.get('source', 'MODIS'),
                    'modis_temperature': modis_temperature.get('source', 'MODIS'),
                    'landsat_indices': landsat_indices.get('source', 'Landsat'),
                }
            }
            
            print(f"Completed {area_data['name']} - Score: {sustainability_score}")
        
        return analysis_results
    
    def export_to_geojson(self, analysis_data):
        features = []
        
        for area_key, data in analysis_data.items():
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [data['coordinates']['lon'], data['coordinates']['lat']]
                },
                'properties': {
                    'area': data['name'],
                    'type': data['type'],
                    'transport_index': data['transport_index'],
                    'pollution_index': data['pollution_index'],
                    'energy_index': data['energy_index'],
                    'sustainability_score': data['sustainability_score'],
                    'solar_potential': data['solar_potential'],
                    'temperature': data['temperature'],
                    'population_density': data['population_density'],
                    'green_cover': data['green_cover'],
                    'vegetation_index': data['vegetation_index'],
                    'urbanization_index': data['urbanization_index']
                }
            }
            features.append(feature)
        
        return {
            'type': 'FeatureCollection',
            'features': features
        }