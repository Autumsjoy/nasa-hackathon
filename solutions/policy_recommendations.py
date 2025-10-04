def generate_policy_recommendations(analysis_data):
    """Generate policy recommendations based on urban analytics"""
    
    recommendations = {
        'high_priority': [],
        'medium_priority': [], 
        'long_term': []
    }
    
    for area_key, area_data in analysis_data.items():
        area_name = area_data.get('name', area_key)
        
        # High priority recommendations
        if area_data.get('sustainability_score', 0) < 25:
            recommendations['high_priority'].append({
                'area': area_name,
                'issue': f"Critical sustainability deficit (Score: {area_data.get('sustainability_score', 0)})",
                'recommendation': 'Immediate green infrastructure investment and pollution control measures',
                'metrics': f"Sustainability: {area_data.get('sustainability_score', 0)}, Pollution: {area_data.get('pollution_index', 0)}",
                'timeline': '0-6 months',
                'budget_estimate': 'High'
            })
        
        # Medium priority recommendations  
        if area_data.get('vegetation_index', 0) < 0.35:
            recommendations['medium_priority'].append({
                'area': area_name,
                'issue': f"Inadequate green cover (NDVI: {area_data.get('vegetation_index', 0):.2f})",
                'recommendation': 'Urban forestry program and green space development',
                'metrics': f"Vegetation Index: {area_data.get('vegetation_index', 0):.2f}",
                'timeline': '6-18 months',
                'budget_estimate': 'Medium'
            })
        
        if area_data.get('transport_index', 0) < 5:
            recommendations['medium_priority'].append({
                'area': area_name,
                'issue': f"Poor transportation infrastructure (Index: {area_data.get('transport_index', 0)})",
                'recommendation': 'Public transport optimization and pedestrian infrastructure',
                'metrics': f"Transport Index: {area_data.get('transport_index', 0)}",
                'timeline': '6-12 months', 
                'budget_estimate': 'Medium'
            })
        
        # Long term recommendations
        if area_data.get('energy_index', 0) < 5:
            recommendations['long_term'].append({
                'area': area_name,
                'issue': f"Low energy efficiency (Index: {area_data.get('energy_index', 0)})",
                'recommendation': 'Renewable energy integration and smart grid development',
                'metrics': f"Energy Index: {area_data.get('energy_index', 0)}, Solar Potential: {area_data.get('solar_potential', 0)}",
                'timeline': '18-36 months',
                'budget_estimate': 'High'
            })
    
    # City-wide recommendations
    avg_sustainability = sum(data.get('sustainability_score', 0) for data in analysis_data.values()) / len(analysis_data)
    if avg_sustainability < 35:
        recommendations['high_priority'].append({
            'area': 'City-wide',
            'issue': f'Low overall urban sustainability (Average: {avg_sustainability:.1f})',
            'recommendation': 'Comprehensive sustainable urban development plan',
            'metrics': f'Average Sustainability Score: {avg_sustainability:.1f}',
            'timeline': '0-12 months',
            'budget_estimate': 'Very High'
        })
    
    return recommendations