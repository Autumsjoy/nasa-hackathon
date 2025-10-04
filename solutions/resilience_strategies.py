def get_resilience_strategies(analysis_data):
    """Generate climate resilience strategies based on environmental data"""
    
    strategies = {}
    
    for area_key, area_data in analysis_data.items():
        area_name = area_data.get('name', area_key)
        temperature = area_data.get('temperature', 0)
        pollution_index = area_data.get('pollution_index', 0)
        vegetation_index = area_data.get('vegetation_index', 0)
        
        # Determine primary threat
        primary_threat = 'heat'
        risk_level = 'Medium'
        
        if temperature > 34:
            primary_threat = 'heat'
            risk_level = 'High'
        elif pollution_index > 8:
            primary_threat = 'air_quality'
            risk_level = 'High'
        elif vegetation_index < 0.3:
            primary_threat = 'water'
            risk_level = 'Medium'
        
        # Generate strategies based on threats
        climate_threats = []
        resilience_actions = []
        
        if temperature > 32:
            climate_threats.append('Urban Heat Island')
            resilience_actions.extend([
                'Install cool roofing materials',
                'Increase tree canopy cover by 25%',
                'Create shaded public spaces',
                'Implement reflective pavement'
            ])
        
        if pollution_index > 6:
            climate_threats.append('Air Pollution')
            resilience_actions.extend([
                'Establish low-emission zones',
                'Install air purification systems',
                'Create green barriers along roads',
                'Promote electric vehicle infrastructure'
            ])
        
        if vegetation_index < 0.4:
            climate_threats.append('Green Cover Deficit')
            resilience_actions.extend([
                'Urban afforestation program',
                'Green roof installations',
                'Community garden development',
                'Permeable surface implementation'
            ])
        
        # Add default threats if none identified
        if not climate_threats:
            climate_threats = ['General Climate Vulnerability']
            resilience_actions = [
                'Climate resilience planning',
                'Infrastructure hardening',
                'Community awareness programs',
                'Early warning systems'
            ]
        
        strategies[area_key] = {
            'area_name': area_name,
            'primary_threat': primary_threat,
            'primary_threat_description': f"Primary climate risk: {primary_threat.replace('_', ' ').title()}",
            'risk_level': risk_level,
            'priority': 'High' if risk_level == 'High' else 'Medium',
            'climate_threats': climate_threats,
            'resilience_actions': resilience_actions,
            'nasa_data_sources': ['MODIS LST', 'Landsat NDVI', 'MODIS Aerosol'],
            'expected_impact': 'Reduce climate vulnerability by 30-40%'
        }
    
    return strategies