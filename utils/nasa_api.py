import requests
from requests import exceptions
import pandas as pd
import time
import random
from datetime import datetime, timedelta
import json
from config.nasa_config import NASAConfig

class NASAAPI:
    def __init__(self):
        self.config = NASAConfig()
        self.session = requests.Session()
    
    def get_air_quality_data(self, lat, lon):
        """Get simulated air quality data"""
        try:
            time.sleep(0.1)
            
            base_pollution = 50
            if lat > 23.25:
                pollution_factor = random.uniform(1.2, 1.8)
            else:
                pollution_factor = random.uniform(0.8, 1.2)
            
            air_quality = {
                'pm25': round(random.uniform(15, 85) * pollution_factor, 2),
                'pm10': round(random.uniform(25, 120) * pollution_factor, 2),
                'no2': round(random.uniform(5, 45) * pollution_factor, 2),
                'so2': round(random.uniform(2, 25) * pollution_factor, 2),
                'o3': round(random.uniform(10, 60) * pollution_factor, 2),
                'aqi': round(random.uniform(30, 180) * pollution_factor, 2),
                'simulated': True,
                'source': 'NASA Simulation Model'
            }
            
            return air_quality
            
        except Exception as e:
            print(f"Error in air quality simulation: {e}")
            return self._get_fallback_air_quality()
    
    def get_satellite_imagery(self, lat, lon, dim=0.15):
        """Get satellite imagery"""
        try:
            imagery_data = {
                'old_bhopal': 'https://via.placeholder.com/400x300/0b3d91/ffffff?text=Old+Bhopal+Satellite',
                'new_bhopal': 'https://via.placeholder.com/400x300/1a6bc7/ffffff?text=New+Bhopal+Satellite',
                'shahpura': 'https://via.placeholder.com/400x300/0b3d91/ffffff?text=Shahpura+Satellite',
                'kolar': 'https://via.placeholder.com/400x300/1a6bc7/ffffff?text=Kolar+Satellite',
                'indrapuri': 'https://via.placeholder.com/400x300/0b3d91/ffffff?text=Indrapuri+Satellite',
                'bhopal_lake': 'https://via.placeholder.com/400x300/1a6bc7/ffffff?text=Lake+Area+Satellite',
                'industrial_area': 'https://via.placeholder.com/400x300/0b3d91/ffffff?text=Industrial+Satellite'
            }
            
            area_key = self._get_area_key(lat, lon)
            return imagery_data.get(area_key, 'https://via.placeholder.com/400x300?text=NASA+Satellite+Data')
            
        except Exception as e:
            print(f"Error getting satellite imagery: {e}")
            return 'https://via.placeholder.com/400x300?text=NASA+Satellite+Data'
    
    def get_solar_energy_data(self, lat, lon):
        """Get solar energy data from NASA POWER API"""
        try:
            params = {
                'parameters': 'ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN,T2M',
                'start': '20230101',
                'end': '20231231',
                'latitude': lat,
                'longitude': lon,
                'community': 'RE',
                'format': 'JSON'
            }
            
            response = self.session.get(
                self.config.APIS['power'], 
                params=params, 
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"Successfully fetched NASA POWER data for {lat}, {lon}")
                return data
            else:
                print(f"NASA POWER API error: {response.status_code}")
                return self._get_simulated_solar_data(lat, lon)
        except exceptions.Timeout:
            print(f"NASA POWER API timeout for {lat}, {lon}")
            return self._get_simulated_solar_data(lat, lon)
            return self._get_simulated_solar_data(lat, lon)
        except Exception as e:
            print(f"Error fetching solar data: {e}")
            return self._get_simulated_solar_data(lat, lon)
    
    def get_modis_vegetation_data(self, lat, lon):
        """Get MODIS vegetation index data"""
        try:
            vegetation_data = self._simulate_modis_vegetation(lat, lon)
            return vegetation_data
            
        except Exception as e:
            print(f"Error fetching MODIS vegetation data: {e}")
            return self._simulate_modis_vegetation(lat, lon)
    
    def get_modis_land_surface_temperature(self, lat, lon):
        """Get MODIS land surface temperature data"""
        try:
            base_temp = 25.0
            
            if self._is_urban_area(lat, lon):
                lst = base_temp + random.uniform(3.0, 8.0)
            else:
                lst = base_temp + random.uniform(1.0, 4.0)
            
            return {
                'daytime_temperature': round(lst, 2),
                'nighttime_temperature': round(lst - random.uniform(5.0, 10.0), 2),
                'urban_heat_intensity': round(lst - base_temp, 2),
                'source': 'MODIS MOD11A2',
                'simulated': True
            }
            
        except Exception as e:
            print(f"Error fetching MODIS temperature data: {e}")
            return {'daytime_temperature': 30.5, 'urban_heat_intensity': 5.5, 'simulated': True}
    
    def get_modis_land_cover(self, lat, lon):
        """Get MODIS land cover classification"""
        try:
            land_cover_types = {
                1: 'Evergreen Needleleaf Forest',
                2: 'Evergreen Broadleaf Forest', 
                3: 'Deciduous Needleleaf Forest',
                4: 'Deciduous Broadleaf Forest',
                5: 'Mixed Forests',
                6: 'Closed Shrublands',
                7: 'Open Shrublands',
                8: 'Woody Savannas',
                9: 'Savannas',
                10: 'Grasslands',
                11: 'Permanent Wetlands',
                12: 'Croplands',
                13: 'Urban and Built-up',
                14: 'Cropland/Natural Vegetation Mosaic',
                15: 'Snow and Ice',
                16: 'Barren or Sparsely Vegetated'
            }
            
            if self._is_urban_area(lat, lon):
                cover_type = 13
                confidence = random.uniform(0.8, 0.95)
            elif self._is_water_body(lat, lon):
                cover_type = 11
                confidence = random.uniform(0.7, 0.9)
            elif self._is_vegetated_area(lat, lon):
                cover_type = random.choice([5, 9, 10])
                confidence = random.uniform(0.6, 0.85)
            else:
                cover_type = 16
                confidence = random.uniform(0.5, 0.8)
            
            return {
                'land_cover_type': land_cover_types[cover_type],
                'land_cover_code': cover_type,
                'confidence': round(confidence, 3),
                'source': 'MODIS MCD12Q1',
                'simulated': True
            }
            
        except Exception as e:
            print(f"Error fetching MODIS land cover: {e}")
            return {'land_cover_type': 'Urban and Built-up', 'confidence': 0.8, 'simulated': True}
    
    def get_landsat_imagery_metadata(self, lat, lon):
        """Get Landsat imagery metadata"""
        try:
            landsat_data = self._simulate_landsat_metadata(lat, lon)
            return landsat_data
            
        except Exception as e:
            print(f"Error fetching Landsat metadata: {e}")
            return self._simulate_landsat_metadata(lat, lon)
    
    def get_landsat_vegetation_indices(self, lat, lon):
        """Calculate vegetation indices from Landsat data"""
        try:
            ndvi = self._calculate_ndvi_from_landsat(lat, lon)
            evi = self._calculate_evi_from_landsat(lat, lon)
            ndbi = self._calculate_ndbi_from_landsat(lat, lon)
            
            return {
                'ndvi': round(ndvi, 3),
                'evi': round(evi, 3),
                'ndbi': round(ndbi, 3),
                'vegetation_health': self._classify_vegetation_health(ndvi),
                'urbanization_level': self._classify_urbanization(ndbi),
                'source': 'Landsat 8/9',
                'simulated': True
            }
            
        except Exception as e:
            print(f"Error calculating Landsat indices: {e}")
            return {'ndvi': 0.5, 'ndbi': 0.3, 'vegetation_health': 'Moderate', 'simulated': True}
    
    def get_modis_fire_data(self, country='IND', days_back=30):
        """Get MODIS active fire data"""
        try:
            fire_data = self._simulate_fire_data()
            return fire_data
            
        except Exception as e:
            print(f"Error fetching MODIS fire data: {e}")
            return self._simulate_fire_data()
    
    # Helper methods
    def _simulate_modis_vegetation(self, lat, lon):
        base_ndvi = 0.3
        
        if self._is_vegetated_area(lat, lon):
            ndvi = base_ndvi + random.uniform(0.2, 0.5)
        elif self._is_urban_area(lat, lon):
            ndvi = base_ndvi + random.uniform(0.0, 0.2)
        else:
            ndvi = base_ndvi + random.uniform(0.1, 0.3)
        
        seasonal_factor = random.uniform(0.8, 1.2)
        ndvi = max(0.0, min(1.0, ndvi * seasonal_factor))
        
        return {
            'ndvi': round(ndvi, 3),
            'evi': round(ndvi * 1.2, 3),
            'vegetation_density': round(ndvi * 100, 1),
            'seasonal_trend': 'Increasing' if seasonal_factor > 1 else 'Decreasing',
            'source': 'MODIS MOD13Q1',
            'simulated': True
        }
    
    def _simulate_landsat_metadata(self, lat, lon):
        return {
            'scene_id': f'LC08_L1TP_143045_{datetime.now().strftime("%Y%m%d")}',
            'acquisition_date': datetime.now().strftime('%Y-%m-%d'),
            'cloud_cover': random.uniform(0, 20),
            'processing_level': 'L1TP',
            'sensor': 'OLI/TIRS',
            'satellite': 'Landsat-8',
            'download_url': '#',
            'simulated': True
        }
    
    def _calculate_ndvi_from_landsat(self, lat, lon):
        base = 0.4
        if self._is_vegetated_area(lat, lon):
            return base + random.uniform(0.2, 0.4)
        elif self._is_urban_area(lat, lon):
            return base + random.uniform(-0.1, 0.1)
        else:
            return base + random.uniform(0.0, 0.2)
    
    def _calculate_evi_from_landsat(self, lat, lon):
        ndvi = self._calculate_ndvi_from_landsat(lat, lon)
        return min(1.0, ndvi * 1.3)
    
    def _calculate_ndbi_from_landsat(self, lat, lon):
        if self._is_urban_area(lat, lon):
            return random.uniform(0.1, 0.4)
        else:
            return random.uniform(-0.2, 0.1)
    
    def _classify_vegetation_health(self, ndvi):
        if ndvi > 0.6: return 'Excellent'
        elif ndvi > 0.4: return 'Good'
        elif ndvi > 0.2: return 'Moderate'
        else: return 'Poor'
    
    def _classify_urbanization(self, ndbi):
        if ndbi > 0.3: return 'High Urbanization'
        elif ndbi > 0.1: return 'Moderate Urbanization'
        else: return 'Low Urbanization'
    
    def _simulate_fire_data(self):
        return {
            'active_fires': random.randint(0, 5),
            'fire_radiative_power': random.uniform(0, 100),
            'confidence': random.choice(['low', 'nominal', 'high']),
            'acquisition_date': datetime.now().strftime('%Y-%m-%d'),
            'source': 'MODIS Active Fires',
            'simulated': True
        }
    
    def _get_simulated_solar_data(self, lat, lon):
        base_radiation = 5.5
        seasonal_variation = {
            '01': 0.9, '02': 0.95, '03': 1.0, '04': 1.05,
            '05': 1.1, '06': 1.0, '07': 0.9, '08': 0.95,
            '09': 1.0, '10': 1.05, '11': 1.0, '12': 0.95
        }
        
        daily_data = {}
        for month in range(1, 13):
            month_key = f'2023{month:02d}01'
            variation = seasonal_variation.get(f'{month:02d}', 1.0)
            daily_data[month_key] = round(base_radiation * variation * random.uniform(0.95, 1.05), 2)
        
        return {
            'properties': {
                'parameter': {
                    'ALLSKY_SFC_SW_DWN': daily_data
                }
            },
            'simulated': True,
            'average_radiation': base_radiation
        }
    
    def _get_fallback_air_quality(self):
        return {
            'pm25': 45.0, 'pm10': 75.0, 'no2': 25.0, 'so2': 12.0,
            'o3': 35.0, 'aqi': 120.0, 'simulated': True, 'source': 'Fallback Data'
        }
    
    def _get_area_key(self, lat, lon):
        areas = {
            'old_bhopal': (23.2599, 77.4126),
            'new_bhopal': (23.2278, 77.4357),
            'shahpura': (23.3000, 77.3667),
            'kolar': (23.1667, 77.4333),
            'indrapuri': (23.2800, 77.4200),
            'bhopal_lake': (23.2667, 77.4000),
            'industrial_area': (23.2000, 77.4500)
        }
        
        closest_area = None
        min_distance = float('inf')
        
        for area, (area_lat, area_lon) in areas.items():
            distance = ((lat - area_lat) ** 2 + (lon - area_lon) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_area = area
        
        return closest_area
    
    def _is_urban_area(self, lat, lon):
        urban_areas = [
            (23.2599, 77.4126), (23.2278, 77.4357),
            (23.3000, 77.3667), (23.2800, 77.4200),
        ]
        return any(abs(lat - u_lat) < 0.02 and abs(lon - u_lon) < 0.02 for u_lat, u_lon in urban_areas)
    
    def _is_vegetated_area(self, lat, lon):
        vegetated_areas = [
            (23.2667, 77.4000), (23.1667, 77.4333),
        ]
        return any(abs(lat - v_lat) < 0.03 and abs(lon - v_lon) < 0.03 for v_lat, v_lon in vegetated_areas)
    
    def _is_water_body(self, lat, lon):
        water_bodies = [(23.2667, 77.4000)]
        return any(abs(lat - w_lat) < 0.01 and abs(lon - w_lon) < 0.01 for w_lat, w_lon in water_bodies)