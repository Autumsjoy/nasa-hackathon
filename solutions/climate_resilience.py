def get_climate_solutions(analysis_data):
    """Generate climate resilience solutions based on environmental data"""
    
    solutions = {}
    
    for area_key, area_data in analysis_data.items():
        area_solutions = []
        
        # Heat resilience solutions
        if area_data.get('temperature', 0) > 32:
            area_solutions.append({
                'type': 'heat_resilience',
                'problem': f"High urban heat (Temperature: {area_data.get('temperature', 0)}°C)",
                'actions': [
                    'Install cool roofing materials',
                    'Increase tree canopy cover by 20%',
                    'Create public cooling centers',
                    'Implement reflective pavement technologies'
                ],
                'priority': 'High' if area_data.get('temperature', 0) > 34 else 'Medium',
                'nasa_data': 'MODIS Land Surface Temperature'
            })
        
        # Air quality solutions
        if area_data.get('pollution_index', 0) > 6:
            area_solutions.append({
                'type': 'air_quality',
                'problem': f"Poor air quality (Pollution index: {area_data.get('pollution_index', 0)})",
                'actions': [
                    'Implement traffic restrictions during peak hours',
                    'Install air purification systems in public spaces',
                    'Create green barriers along major roads',
                    'Promote electric vehicle adoption'
                ],
                'priority': 'High' if area_data.get('pollution_index', 0) > 8 else 'Medium',
                'nasa_data': 'MODIS Aerosol Optical Depth'
            })
        
        # Water management solutions
        if area_data.get('vegetation_index', 0) < 0.3:
            area_solutions.append({
                'type': 'water_management',
                'problem': f"Low vegetation cover (NDVI: {area_data.get('vegetation_index', 0):.2f})",
                'actions': [
                    'Implement rainwater harvesting systems',
                    'Create permeable surfaces to reduce runoff',
                    'Develop water-efficient landscaping',
                    'Install smart irrigation systems'
                ],
                'priority': 'Medium',
                'nasa_data': 'Landsat NDVI, MODIS Evapotranspiration'
            })
        
        if area_solutions:
            solutions[area_key] = {
                'area_name': area_data.get('name', area_key),
                'solutions': area_solutions
            }
    
    return solutions