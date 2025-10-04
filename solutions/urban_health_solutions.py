def get_urban_health_solutions(analysis_data):
    """Generate urban health solutions based on NASA data analysis"""
    
    solutions = {
        'green_infrastructure': {
            'problem': 'Urban heat islands and inadequate green spaces',
            'solution': 'Precision Greening Strategy',
            'actions': [],
            'nasa_data_used': ['MODIS NDVI', 'Landsat Land Surface Temperature'],
            'expected_impact': 'Reduce temperatures by 2-3°C, improve air quality'
        },
        'sustainable_mobility': {
            'problem': 'High pollution from transportation',
            'solution': 'Smart Public Transport Optimization', 
            'actions': [],
            'nasa_data_used': ['MODIS Aerosol Optical Depth', 'Population density'],
            'expected_impact': 'Reduce PM2.5 by 15-20%'
        },
        'energy_efficiency': {
            'problem': 'High energy consumption and low renewable integration',
            'solution': 'Solar Energy Maximization',
            'actions': [],
            'nasa_data_used': ['NASA POWER Solar Data', 'Landsat Urban Mapping'],
            'expected_impact': 'Increase renewable energy share by 25%'
        }
    }
    
    # Generate area-specific actions
    for area_key, area_data in analysis_data.items():
        area_name = area_data.get('name', area_key)
        
        # Green infrastructure for areas with low vegetation
        if area_data.get('vegetation_index', 0) < 0.4:
            solutions['green_infrastructure']['actions'].append(
                f"Plant native trees in {area_name} (Current NDVI: {area_data.get('vegetation_index', 0):.2f})"
            )
        
        # Mobility solutions for high pollution areas
        if area_data.get('pollution_index', 0) > 6:
            solutions['sustainable_mobility']['actions'].append(
                f"Deploy electric buses in {area_name} (Pollution index: {area_data.get('pollution_index', 0)})"
            )
        
        # Energy solutions for areas with good solar potential
        if area_data.get('solar_potential', 0) > 5:
            solutions['energy_efficiency']['actions'].append(
                f"Install solar panels in {area_name} (Solar potential: {area_data.get('solar_potential', 0)})"
            )
    
    return solutions