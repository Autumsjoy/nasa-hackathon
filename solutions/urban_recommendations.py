def get_urban_recommendations(analysis_data):
    """Generate urban planning recommendations based on comprehensive analysis"""
    
    recommendations = {
        'infrastructure': [],
        'land_use': [],
        'transportation': [],
        'environmental': []
    }
    
    for area_key, area_data in analysis_data.items():
        area_name = area_data.get('name', area_key)
        
        # Infrastructure recommendations
        if area_data.get('transport_index', 0) < 5:
            recommendations['infrastructure'].append({
                'area': area_name,
                'issue': 'Inadequate public transport infrastructure',
                'recommendation': 'Develop integrated transport network with bus rapid transit',
                'priority': 'High',
                'timeline': '6-12 months',
                'budget': 'Medium'
            })
        
        if area_data.get('energy_index', 0) < 5:
            recommendations['infrastructure'].append({
                'area': area_name,
                'issue': 'Low energy efficiency and renewable integration',
                'recommendation': 'Implement smart grid and solar energy programs',
                'priority': 'Medium',
                'timeline': '12-24 months',
                'budget': 'High'
            })
        
        # Land use recommendations
        if area_data.get('vegetation_index', 0) < 0.4:
            recommendations['land_use'].append({
                'area': area_name,
                'issue': 'Insufficient green spaces and urban forestry',
                'recommendation': 'Create green corridors and increase urban canopy',
                'priority': 'Medium',
                'timeline': '6-18 months',
                'budget': 'Medium'
            })
        
        if area_data.get('urbanization_index', 0) > 0.8:
            recommendations['land_use'].append({
                'area': area_name,
                'issue': 'High urbanization density affecting livability',
                'recommendation': 'Implement mixed-use development and open space requirements',
                'priority': 'Medium',
                'timeline': '12-24 months',
                'budget': 'Medium'
            })
        
        # Transportation recommendations
        if area_data.get('pollution_index', 0) > 6:
            recommendations['transportation'].append({
                'area': area_name,
                'issue': 'High pollution from transportation sources',
                'recommendation': 'Promote electric vehicles and non-motorized transport',
                'priority': 'High',
                'timeline': '6-12 months',
                'budget': 'Medium'
            })
        
        # Environmental recommendations
        if area_data.get('temperature', 0) > 32:
            recommendations['environmental'].append({
                'area': area_name,
                'issue': 'Urban heat island effect',
                'recommendation': 'Implement cool surfaces and urban greening',
                'priority': 'Medium',
                'timeline': '12-18 months',
                'budget': 'Medium'
            })
    
    return recommendations