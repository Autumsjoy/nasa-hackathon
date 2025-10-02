import os
from dotenv import load_dotenv

load_dotenv()

class NASAConfig:
    NASA_API_KEY = os.getenv('NASA_API_KEY', 'DEMO_KEY')
    
    # NASA APIs
    APIS = {
        'earth_imagery': 'https://api.nasa.gov/planetary/earth/imagery',
        'earth_assets': 'https://api.nasa.gov/planetary/earth/assets',
        'power': 'https://power.larc.nasa.gov/api/temporal/daily/point',
        'modis': 'https://modis.ornl.gov/rst/api/v1',
        'landsat': 'https://landsatlook.usgs.gov/sat-api/collections/landsat-c2l2-sr/items',
        'firms': 'https://firms.modaps.eosdis.nasa.gov/api/area/country'
    }
    
    # MODIS Products
    MODIS_PRODUCTS = {
        'vegetation': 'MOD13Q1',  # Vegetation Indices
        'land_temp': 'MOD11A2',   # Land Surface Temperature
        'land_cover': 'MCD12Q1',  # Land Cover Type
        'burned_area': 'MCD64A1', # Burned Area
        'urban_extent': 'MOD44W'  # Urban Extent
    }
    
    # Landsat Collections
    LANDSAT_COLLECTIONS = {
        'landsat_8': 'landsat-8-l1',
        'landsat_9': 'landsat-9-l1',
        'surface_reflectance': 'landsat-c2l2-sr'
    }
    
    # Bhopal bounding box
    BHOPAL_BOUNDS = {
        'north': 23.4000,
        'south': 23.1000,
        'east': 77.6000,
        'west': 77.3000
    }