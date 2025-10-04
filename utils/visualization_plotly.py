import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp
import pandas as pd
import numpy as np
import folium
from folium import plugins
from branca.colormap import LinearColormap
import json

class DataVisualizerPlotly:
    def __init__(self):
        self.colors = {
            'primary': '#50589C',
            'primary_light': '#6A72B0',
            'primary_dark': '#404780',
            'secondary': '#FF6B35',
            'accent': '#4ECDC4',
            'dark': '#2C3E50',
            'light': '#F8F9FA',
            'success': '#27AE60',
            'warning': '#E67E22',
            'danger': '#E74C3C',
            'info': '#3498DB'
        }
    
    def generate_sustainability_chart(self, analysis_data):
        """Generate sustainability score chart using Plotly"""
        try:
            areas = [data.get('name', 'Unknown') for data in analysis_data.values()]
            scores = [data.get('sustainability_score', 50) for data in analysis_data.values()]
            
            # Create colors based on score ranges
            colors = []
            for score in scores:
                if score >= 70:
                    colors.append(self.colors['success'])
                elif score >= 50:
                    colors.append(self.colors['warning'])
                else:
                    colors.append(self.colors['danger'])
            
            fig = go.Figure(data=[
                go.Bar(
                    x=areas,
                    y=scores,
                    marker_color=colors,
                    text=[f'{score:.1f}' for score in scores],
                    textposition='auto',
                    marker_line=dict(color=self.colors['dark'], width=1),
                    hovertemplate='<b>%{x}</b><br>Sustainability Score: %{y:.1f}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title=dict(
                    text='Sustainability Scores by Area',
                    font=dict(size=16, color=self.colors['primary'])
                ),
                xaxis=dict(
                    title='Areas',
                    tickangle=45
                ),
                yaxis=dict(
                    title='Sustainability Score (0-100)',
                    range=[0, 100]
                ),
                plot_bgcolor=self.colors['light'],
                paper_bgcolor='white',
                font=dict(color=self.colors['dark']),
                showlegend=False,
                height=400,
                margin=dict(l=50, r=50, t=80, b=100)
            )
            
            return fig.to_html(include_plotlyjs='cdn', config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating sustainability chart: {e}")
            return self._generate_error_html("Sustainability Chart")
    
    def generate_satellite_analysis_chart(self, analysis_data):
        """Generate satellite data analysis chart"""
        try:
            areas = [data.get('name', 'Unknown') for data in analysis_data.values()]
            
            # Extract satellite data
            vegetation = [data.get('vegetation_index', 0.5) * 100 for data in analysis_data.values()]
            urbanization = [data.get('urbanization_index', 0.5) * 100 for data in analysis_data.values()]
            temperatures = [data.get('temperature', 25) for data in analysis_data.values()]
            
            fig = go.Figure()
            
            # Add vegetation data
            fig.add_trace(go.Scatter(
                x=areas,
                y=vegetation,
                mode='lines+markers',
                name='Vegetation Index',
                line=dict(color=self.colors['success'], width=3),
                marker=dict(size=8, color=self.colors['success']),
                hovertemplate='<b>%{x}</b><br>Vegetation: %{y:.1f}%<extra></extra>'
            ))
            
            # Add urbanization data
            fig.add_trace(go.Scatter(
                x=areas,
                y=urbanization,
                mode='lines+markers', 
                name='Urbanization Index',
                line=dict(color=self.colors['primary'], width=3),
                marker=dict(size=8, color=self.colors['primary']),
                hovertemplate='<b>%{x}</b><br>Urbanization: %{y:.1f}%<extra></extra>'
            ))
            
            # Add temperature data (secondary y-axis)
            fig.add_trace(go.Scatter(
                x=areas,
                y=temperatures,
                mode='lines+markers',
                name='Temperature (°C)',
                line=dict(color=self.colors['warning'], width=3, dash='dot'),
                marker=dict(size=8, color=self.colors['warning']),
                yaxis='y2',
                hovertemplate='<b>%{x}</b><br>Temperature: %{y:.1f}°C<extra></extra>'
            ))
            
            fig.update_layout(
                title=dict(
                    text='Satellite Data Analysis: Vegetation vs Urbanization vs Temperature',
                    font=dict(size=16, color=self.colors['primary'])
                ),
                xaxis=dict(
                    title='Areas',
                    tickangle=45
                ),
                yaxis=dict(
                    title='Vegetation/Urbanization Index (%)',
                    range=[0, 100]
                ),
                yaxis2=dict(
                    title='Temperature (°C)',
                    overlaying='y',
                    side='right',
                    range=[20, 40]
                ),
                plot_bgcolor=self.colors['light'],
                paper_bgcolor='white',
                font=dict(color=self.colors['dark']),
                height=500,
                margin=dict(l=50, r=50, t=80, b=100),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            return fig.to_html(include_plotlyjs=False, config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating satellite analysis chart: {e}")
            return self._generate_error_html("Satellite Analysis Chart")
    
    def generate_comparison_chart(self, analysis_data):
        """Generate multi-metric comparison chart"""
        try:
            areas = [data.get('name', 'Unknown') for data in analysis_data.values()]
            
            # Extract all metrics for comparison
            sustainability = [data.get('sustainability_score', 50) for data in analysis_data.values()]
            transport = [data.get('transport_index', 5) * 10 for data in analysis_data.values()]
            energy = [data.get('energy_index', 5) * 10 for data in analysis_data.values()]
            pollution_control = [(10 - data.get('pollution_index', 5)) * 10 for data in analysis_data.values()]
            
            fig = go.Figure()
            
            # Add all metrics as bars
            fig.add_trace(go.Bar(
                name='Sustainability',
                x=areas,
                y=sustainability,
                marker_color=self.colors['primary'],
                hovertemplate='<b>%{x}</b><br>Sustainability: %{y:.1f}<extra></extra>'
            ))
            
            fig.add_trace(go.Bar(
                name='Transport',
                x=areas,
                y=transport,
                marker_color=self.colors['accent'],
                hovertemplate='<b>%{x}</b><br>Transport: %{y:.1f}<extra></extra>'
            ))
            
            fig.add_trace(go.Bar(
                name='Energy',
                x=areas,
                y=energy,
                marker_color=self.colors['success'],
                hovertemplate='<b>%{x}</b><br>Energy: %{y:.1f}<extra></extra>'
            ))
            
            fig.add_trace(go.Bar(
                name='Pollution Control',
                x=areas,
                y=pollution_control,
                marker_color=self.colors['info'],
                hovertemplate='<b>%{x}</b><br>Pollution Control: %{y:.1f}<extra></extra>'
            ))
            
            fig.update_layout(
                title=dict(
                    text='Multi-Metric Area Comparison',
                    font=dict(size=16, color=self.colors['primary'])
                ),
                xaxis=dict(
                    title='Areas',
                    tickangle=45
                ),
                yaxis=dict(
                    title='Scores (0-100)',
                    range=[0, 100]
                ),
                barmode='group',
                plot_bgcolor=self.colors['light'],
                paper_bgcolor='white',
                font=dict(color=self.colors['dark']),
                height=500,
                margin=dict(l=50, r=50, t=80, b=100),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            return fig.to_html(include_plotlyjs=False, config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating comparison chart: {e}")
            return self._generate_error_html("Comparison Chart")
    
    def generate_vegetation_analysis_chart(self, analysis_data):
        """Generate detailed vegetation analysis chart"""
        try:
            areas = [data.get('name', 'Unknown') for data in analysis_data.values()]
            
            # Extract vegetation-related data
            ndvi_values = [data.get('vegetation_index', 0.5) for data in analysis_data.values()]
            green_cover = [data.get('green_cover', 0) for data in analysis_data.values()]
            vegetation_health_scores = []
            
            # Convert vegetation health to numerical scores
            health_mapping = {'Excellent': 100, 'Good': 75, 'Moderate': 50, 'Poor': 25}
            for data in analysis_data.values():
                health = data.get('vegetation_health', 'Moderate')
                vegetation_health_scores.append(health_mapping.get(health, 50))
            
            fig = go.Figure()
            
            # Add NDVI values
            fig.add_trace(go.Bar(
                name='NDVI Index',
                x=areas,
                y=ndvi_values,
                marker_color=self.colors['success'],
                hovertemplate='<b>%{x}</b><br>NDVI: %{y:.3f}<extra></extra>',
                yaxis='y'
            ))
            
            # Add green cover (secondary axis)
            fig.add_trace(go.Scatter(
                name='Green Cover %',
                x=areas,
                y=green_cover,
                mode='lines+markers',
                line=dict(color=self.colors['accent'], width=3),
                marker=dict(size=8, color=self.colors['accent']),
                hovertemplate='<b>%{x}</b><br>Green Cover: %{y:.1f}%<extra></extra>',
                yaxis='y2'
            ))
            
            # Add vegetation health (secondary axis)
            fig.add_trace(go.Scatter(
                name='Health Score',
                x=areas,
                y=vegetation_health_scores,
                mode='lines+markers',
                line=dict(color=self.colors['primary'], width=3, dash='dot'),
                marker=dict(size=8, color=self.colors['primary']),
                hovertemplate='<b>%{x}</b><br>Health Score: %{y:.0f}<extra></extra>',
                yaxis='y2'
            ))
            
            fig.update_layout(
                title=dict(
                    text='Vegetation Analysis: NDVI, Green Cover & Health Scores',
                    font=dict(size=16, color=self.colors['primary'])
                ),
                xaxis=dict(
                    title='Areas',
                    tickangle=45
                ),
                yaxis=dict(
                    title='NDVI Index',
                    range=[0, 1]
                ),
                yaxis2=dict(
                    title='Green Cover % & Health Score',
                    overlaying='y',
                    side='right',
                    range=[0, 100]
                ),
                plot_bgcolor=self.colors['light'],
                paper_bgcolor='white',
                font=dict(color=self.colors['dark']),
                height=500,
                margin=dict(l=50, r=50, t=80, b=100),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            return fig.to_html(include_plotlyjs=False, config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating vegetation analysis chart: {e}")
            return self._generate_error_html("Vegetation Analysis Chart")
    
    def generate_satellite_data_comparison(self, analysis_data):
        """Generate comprehensive satellite data comparison"""
        try:
            areas = [data.get('name', 'Unknown') for data in analysis_data.values()]
            
            # Extract multiple satellite-derived metrics
            ndvi_values = [data.get('vegetation_index', 0.5) for data in analysis_data.values()]
            ndbi_values = [data.get('urbanization_index', 0.5) for data in analysis_data.values()]
            temperatures = [data.get('temperature', 25) for data in analysis_data.values()]
            solar_potentials = [data.get('solar_potential', 5.5) for data in analysis_data.values()]
            
            # Create subplots
            fig = sp.make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Landsat NDVI - Vegetation Health',
                    'Landsat NDBI - Urbanization Level', 
                    'MODIS Temperature - Urban Heat',
                    'NASA POWER - Solar Potential'
                ),
                vertical_spacing=0.12,
                horizontal_spacing=0.1
            )
            
            # NDVI subplot
            fig.add_trace(
                go.Bar(
                    x=areas, y=ndvi_values,
                    marker_color=[self.colors['success'] if x > 0.5 else self.colors['warning'] for x in ndvi_values],
                    name='NDVI',
                    hovertemplate='<b>%{x}</b><br>NDVI: %{y:.3f}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # NDBI subplot
            fig.add_trace(
                go.Bar(
                    x=areas, y=ndbi_values,
                    marker_color=[self.colors['primary'] if x > 0.3 else self.colors['accent'] for x in ndbi_values],
                    name='NDBI',
                    hovertemplate='<b>%{x}</b><br>NDBI: %{y:.3f}<extra></extra>'
                ),
                row=1, col=2
            )
            
            # Temperature subplot
            fig.add_trace(
                go.Scatter(
                    x=areas, y=temperatures,
                    mode='lines+markers',
                    line=dict(color=self.colors['warning'], width=3),
                    marker=dict(size=8, color=self.colors['warning']),
                    name='Temperature',
                    hovertemplate='<b>%{x}</b><br>Temperature: %{y:.1f}°C<extra></extra>'
                ),
                row=2, col=1
            )
            
            # Solar potential subplot
            fig.add_trace(
                go.Scatter(
                    x=areas, y=solar_potentials,
                    mode='lines+markers', 
                    line=dict(color=self.colors['secondary'], width=3),
                    marker=dict(size=8, color=self.colors['secondary']),
                    name='Solar Potential',
                    hovertemplate='<b>%{x}</b><br>Solar: %{y:.1f} kWh/m²<extra></extra>'
                ),
                row=2, col=2
            )
            
            # Update layout
            fig.update_layout(
                title_text='Comprehensive Satellite Data Comparison',
                showlegend=False,
                plot_bgcolor=self.colors['light'],
                paper_bgcolor='white',
                font=dict(color=self.colors['dark']),
                height=600,
                margin=dict(l=50, r=50, t=100, b=100)
            )
            
            # Update axes
            fig.update_xaxes(tickangle=45)
            fig.update_yaxes(title_text="NDVI Value", range=[0, 1], row=1, col=1)
            fig.update_yaxes(title_text="NDBI Value", range=[0, 1], row=1, col=2)
            fig.update_yaxes(title_text="Temperature (°C)", range=[20, 40], row=2, col=1)
            fig.update_yaxes(title_text="Solar (kWh/m²)", range=[4, 7], row=2, col=2)
            
            return fig.to_html(include_plotlyjs=False, config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating satellite data comparison: {e}")
            return self._generate_error_html("Satellite Data Comparison")
    
    def generate_radar_chart_comparison(self, analysis_data):
        """Generate radar chart comparing all areas"""
        try:
            categories = ['Transport', 'Energy', 'Environment', 'Infrastructure', 'Sustainability']
            
            fig = go.Figure()
            
            # Add each area to radar chart
            for area_name, area_data in analysis_data.items():
                values = [
                    area_data.get('transport_index', 5) * 10,
                    area_data.get('energy_index', 5) * 10,
                    (100 - area_data.get('pollution_index', 5) * 10),
                    area_data.get('vegetation_index', 0.5) * 100,
                    area_data.get('sustainability_score', 50)
                ]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=area_data.get('name', area_name),
                    hovertemplate='<b>%{fullData.name}</b><br>%{theta}: %{r:.1f}<extra></extra>'
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                title=dict(
                    text='Comprehensive Area Comparison - Radar Chart',
                    font=dict(size=16, color=self.colors['primary'])
                ),
                showlegend=True,
                height=500,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            return fig.to_html(include_plotlyjs=False, config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating radar chart comparison: {e}")
            return self._generate_error_html("Radar Comparison Chart")
    
    def generate_area_comparison_chart(self, area_data, all_areas):
        """Generate comparison chart for specific area vs others"""
        try:
            current_area = area_data.get('name', 'Current Area')
            other_areas = [name for name, data in all_areas.items() if data.get('name') != current_area]
            
            current_score = area_data.get('sustainability_score', 50)
            other_scores = [data.get('sustainability_score', 50) for name, data in all_areas.items() if data.get('name') != current_area]
            
            avg_other_score = sum(other_scores) / len(other_scores) if other_scores else 50
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name=current_area,
                x=['Current Area'],
                y=[current_score],
                marker_color=self.colors['primary'],
                hovertemplate='<b>%{x}</b><br>Score: %{y:.1f}<extra></extra>'
            ))
            
            fig.add_trace(go.Bar(
                name='Other Areas Average',
                x=['Other Areas Avg'],
                y=[avg_other_score],
                marker_color=self.colors['accent'],
                hovertemplate='<b>%{x}</b><br>Average Score: %{y:.1f}<extra></extra>'
            ))
            
            fig.update_layout(
                title=dict(
                    text=f'{current_area} vs Other Areas - Sustainability Comparison',
                    font=dict(size=16, color=self.colors['primary'])
                ),
                yaxis=dict(
                    title='Sustainability Score',
                    range=[0, 100]
                ),
                plot_bgcolor=self.colors['light'],
                paper_bgcolor='white',
                font=dict(color=self.colors['dark']),
                height=400,
                showlegend=True
            )
            
            return fig.to_html(include_plotlyjs=False, config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating area comparison chart: {e}")
            return self._generate_error_html("Area Comparison Chart")
    
    def generate_heat_map(self, analysis_data, metric):
        """Generate heat map for specific metric"""
        try:
            areas = [data.get('name', 'Unknown') for data in analysis_data.values()]
            values = [data.get(metric, 0) for data in analysis_data.values()]
            
            # Create proper 2D array for heatmap
            z_values = [values]  # Single row for all areas
            
            fig = go.Figure(data=go.Heatmap(
                z=z_values,
                x=areas,
                y=[metric.replace('_', ' ').title()],
                colorscale='Viridis',
                showscale=True,
                hoverongaps=False,
                hovertemplate='<b>%{x}</b><br>%{y}: %{z:.1f}<extra></extra>'
            ))
            
            fig.update_layout(
                title=dict(
                    text=f'{metric.replace("_", " ").title()} Heat Map',
                    font=dict(size=16, color=self.colors['primary'])
                ),
                xaxis=dict(tickangle=45),
                height=300,
                margin=dict(l=50, r=50, t=80, b=100)
            )
            
            return fig.to_html(include_plotlyjs=False, config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating heat map for {metric}: {e}")
            return self._generate_error_html("Heat Map")

    def generate_transportation_chart(self, area_data):
        """Generate transportation analysis chart for individual area"""
        try:
            transport_data = area_data.get('transportation_breakdown', {})
            modes = list(transport_data.keys())
            percentages = list(transport_data.values())
            
            # Format mode names for better display
            formatted_modes = [mode.replace('_', ' ').title() for mode in modes]
            
            colors = [self.colors['primary'], self.colors['secondary'], 
                     self.colors['accent'], self.colors['success'], self.colors['warning']]
            
            fig = go.Figure(data=[go.Pie(
                labels=formatted_modes,
                values=percentages,
                hole=.4,
                marker_colors=colors,
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                title=dict(
                    text=f"Transportation Mode Distribution - {area_data.get('name', 'Area')}",
                    font=dict(size=16, color=self.colors['primary'])
                ),
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.1
                )
            )
            
            return fig.to_html(include_plotlyjs=False, config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating transportation chart: {e}")
            return self._generate_error_html("Transportation Chart")

    def generate_energy_breakdown_chart(self, area_data):
        """Generate energy breakdown pie chart"""
        try:
            energy_data = area_data.get('energy_breakdown', {})
            
            # If energy_breakdown is not available, create from available data
            if not energy_data:
                energy_data = {
                    'Solar Energy': area_data.get('solar_percentage', 25),
                    'Grid Electricity': area_data.get('grid_dependency', 60),
                    'Battery Storage': 8,
                    'Generator Backup': 5,
                    'Other Renewable': 2
                }
            
            labels = list(energy_data.keys())
            values = list(energy_data.values())
            
            colors = [self.colors['accent'], self.colors['primary'], 
                     self.colors['success'], self.colors['warning'], self.colors['info']]
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.3,
                marker_colors=colors,
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                title=dict(
                    text=f"Energy Source Breakdown - {area_data.get('name', 'Area')}",
                    font=dict(size=16, color=self.colors['primary'])
                ),
                height=400
            )
            
            return fig.to_html(include_plotlyjs=False, config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating energy breakdown chart: {e}")
            return self._generate_error_html("Energy Breakdown Chart")

    def generate_radar_chart(self, area_data):
        """Generate radar chart for individual area analysis"""
        try:
            categories = ['Transport Efficiency', 'Energy Performance', 'Environmental Quality', 
                         'Infrastructure', 'Sustainability']
            
            values = [
                area_data.get('transport_index', 5) * 10,
                area_data.get('energy_index', 5) * 10,
                (100 - area_data.get('pollution_index', 5) * 10),
                area_data.get('vegetation_index', 0.5) * 100,
                area_data.get('sustainability_score', 50)
            ]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                fillcolor=f'{self.colors["primary"]}80',
                line=dict(color=self.colors['primary'], width=2),
                name=area_data.get('name', 'Area'),
                hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}<extra></extra>'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                title=dict(
                    text=f"{area_data.get('name', 'Area')} - Comprehensive Analysis",
                    font=dict(size=16, color=self.colors['primary'])
                ),
                showlegend=False,
                height=400
            )
            
            return fig.to_html(include_plotlyjs=False, config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating radar chart: {e}")
            return self._generate_error_html("Radar Chart")

    def generate_area_sustainability_chart(self, area_data):
        """Generate area-specific sustainability chart"""
        try:
            metrics = ['Transport', 'Energy', 'Environment', 'Infrastructure', 'Overall']
            values = [
                area_data.get('transport_index', 5) * 10,
                area_data.get('energy_index', 5) * 10,
                (100 - area_data.get('pollution_index', 5) * 10),
                area_data.get('vegetation_index', 0.5) * 100,
                area_data.get('sustainability_score', 50)
            ]
            
            colors = [self.colors['primary'], self.colors['accent'], 
                     self.colors['success'], self.colors['warning'], self.colors['secondary']]
            
            fig = go.Figure(data=[go.Bar(
                x=metrics,
                y=values,
                marker_color=colors,
                text=[f'{v:.1f}' for v in values],
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Score: %{y:.1f}<extra></extra>'
            )])
            
            fig.update_layout(
                title=dict(
                    text=f"{area_data.get('name', 'Area')} - Sustainability Metrics",
                    font=dict(size=16, color=self.colors['primary'])
                ),
                xaxis_title='Sustainability Metrics',
                yaxis_title='Score (0-100)',
                yaxis=dict(range=[0, 100]),
                plot_bgcolor=self.colors['light'],
                paper_bgcolor='white',
                font=dict(color=self.colors['dark']),
                height=400,
                showlegend=False
            )
            
            return fig.to_html(include_plotlyjs=False, config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating area sustainability chart: {e}")
            return self._generate_error_html("Sustainability Metrics Chart")

    def generate_correlation_matrix(self, analysis_data):
        """Generate correlation matrix between different metrics"""
        try:
            # Extract metrics for correlation analysis
            metrics = ['sustainability_score', 'transport_index', 'energy_index', 
                      'pollution_index', 'vegetation_index', 'temperature']
            
            # Create correlation data
            data = {}
            for metric in metrics:
                data[metric] = [area_data.get(metric, 0) for area_data in analysis_data.values()]
            
            df = pd.DataFrame(data)
            
            # Calculate correlation matrix
            corr_matrix = df.corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=[metric.replace('_', ' ').title() for metric in corr_matrix.columns],
                y=[metric.replace('_', ' ').title() for metric in corr_matrix.index],
                colorscale='RdBu',
                zmid=0,
                text=[[f'{val:.2f}' for val in row] for row in corr_matrix.values],
                texttemplate="%{text}",
                textfont={"size": 12},
                hoverongaps=False,
                hovertemplate='<b>%{y} vs %{x}</b><br>Correlation: %{z:.3f}<extra></extra>'
            ))
            
            fig.update_layout(
                title=dict(
                    text='Metric Correlation Matrix',
                    font=dict(size=16, color=self.colors['primary'])
                ),
                height=500,
                margin=dict(l=50, r=50, t=80, b=100),
                xaxis=dict(tickangle=45)
            )
            
            return fig.to_html(include_plotlyjs=False, config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating correlation matrix: {e}")
            return self._generate_error_html("Correlation Matrix")

    def generate_interactive_map(self, analysis_data):
        """Generate interactive Folium map"""
        try:
            # Center map on Bhopal
            m = folium.Map(location=[23.2599, 77.4126], zoom_start=11, 
                          tiles='CartoDB positron')
            
            # Create color scale for sustainability scores
            colormap = LinearColormap(
                colors=[self.colors['danger'], self.colors['warning'], self.colors['success']],
                vmin=0, vmax=100,
                caption='Sustainability Score'
            )
            
            # Define area coordinates based on your data_processing.py
            area_coordinates = {
                'downtown': [23.2599, 77.4126],
                'suburban': [23.2278, 77.4357],
                'industrial': [23.2000, 77.4500]
            }
            
            # Add markers for each area
            for area_key, data in analysis_data.items():
                if area_key in area_coordinates:
                    coords = area_coordinates[area_key]
                    score = data.get('sustainability_score', 50)
                    
                    popup_text = f"""
                    <div style="min-width: 280px; font-family: Arial, sans-serif;">
                        <h4 style="color: {self.colors['primary']}; margin-bottom: 15px; border-bottom: 2px solid {self.colors['primary']}; padding-bottom: 5px;">
                            {data.get('name', 'Unknown Area')}
                        </h4>
                        <div style="background: {colormap(score)}; color: white; padding: 12px; border-radius: 8px; text-align: center; margin-bottom: 15px; font-weight: bold;">
                            Sustainability Score: {score}/100
                        </div>
                        <table style="width: 100%; font-size: 12px; border-collapse: collapse;">
                            <tr style="border-bottom: 1px solid #eee;">
                                <td style="padding: 8px 0;"><strong>Transport:</strong></td>
                                <td style="padding: 8px 0; text-align: right;"><strong>{data.get('transport_index', 5)}/10</strong></td>
                            </tr>
                            <tr style="border-bottom: 1px solid #eee;">
                                <td style="padding: 8px 0;"><strong>Pollution:</strong></td>
                                <td style="padding: 8px 0; text-align: right;"><strong>{data.get('pollution_index', 5)}/10</strong></td>
                            </tr>
                            <tr style="border-bottom: 1px solid #eee;">
                                <td style="padding: 8px 0;"><strong>Energy:</strong></td>
                                <td style="padding: 8px 0; text-align: right;"><strong>{data.get('energy_index', 5)}/10</strong></td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0;"><strong>Green Cover:</strong></td>
                                <td style="padding: 8px 0; text-align: right;"><strong>{data.get('green_cover', 0)}%</strong></td>
                            </tr>
                        </table>
                        <div style="margin-top: 12px; text-align: center;">
                            <a href="/analysis/{area_key}" style="background: {self.colors['primary']}; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; font-size: 12px;">
                                View Detailed Analysis
                            </a>
                        </div>
                    </div>
                    """
                    
                    folium.CircleMarker(
                        location=coords,
                        radius=20,
                        popup=folium.Popup(popup_text, max_width=350),
                        tooltip=f"{data.get('name', 'Unknown')} - Score: {score}",
                        color=colormap(score),
                        fillColor=colormap(score),
                        fillOpacity=0.7,
                        weight=2
                    ).add_to(m)
            
            # Add heatmap for sustainability scores
            heat_data = []
            for area_key, data in analysis_data.items():
                if area_key in area_coordinates:
                    coords = area_coordinates[area_key]
                    heat_data.append([coords[0], coords[1], data.get('sustainability_score', 50)])
            
            plugins.HeatMap(heat_data, 
                           gradient={0.4: self.colors['danger'], 0.65: self.colors['warning'], 1: self.colors['success']}, 
                           min_opacity=0.5, max_opacity=0.8, radius=25, blur=15).add_to(m)
            
            # Add colormap to map
            colormap.add_to(m)
            
            return m._repr_html_()
            
        except Exception as e:
            print(f"Error generating interactive map: {e}")
            return f"""
            <div class="alert alert-danger text-center p-4">
                <h5>🗺️ Map Not Available</h5>
                <p class="mb-0">Error generating interactive map: {str(e)}</p>
                <small>Please try refreshing the page.</small>
            </div>
            """

    def generate_cesium_map(self, analysis_data):
        """Generate Cesium JS 3D map HTML"""
        try:
            # Create area data for Cesium
            areas_data = []
            area_coordinates = {
                'downtown': [23.2599, 77.4126],
                'suburban': [23.2278, 77.4357],
                'industrial': [23.2000, 77.4500]
            }
            
            for area_key, data in analysis_data.items():
                if area_key in area_coordinates:
                    coords = area_coordinates[area_key]
                    areas_data.append({
                        'name': data.get('name', 'Unknown'),
                        'lat': coords[0],
                        'lon': coords[1],
                        'score': data.get('sustainability_score', 50),
                        'transport': data.get('transport_index', 5),
                        'pollution': data.get('pollution_index', 5),
                        'energy': data.get('energy_index', 5),
                        'vegetation': data.get('green_cover', 0)
                    })
            
            cesium_html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Bhopal 3D Satellite View - NASA Hackathon</title>
                <script src="https://cesium.com/downloads/cesiumjs/releases/1.109/Build/Cesium/Cesium.js"></script>
                <link href="https://cesium.com/downloads/cesiumjs/releases/1.109/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
                <style>
                    html, body, #cesiumContainer {{
                        width: 100%; height: 100%; margin: 0; padding: 0; overflow: hidden;
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    }}
                    .cesium-info {{
                        background: {self.colors['primary']};
                        color: white;
                        padding: 10px;
                        border-radius: 5px;
                    }}
                </style>
            </head>
            <body>
                <div id="cesiumContainer"></div>
                <script>
                    Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJlYWE1N2QxMy02MWZjLTQ3ODktODgyYS1jYjJkMjY0MWE1MWUiLCJpZCI6MjA0MzA2LCJpYXQiOjE3MTE4MTU5ODN9.8a3m9QuT3Xx1p1z0Y7W0vVQ6t6X3Y3Q2Q3X3Y3Q2Q3X3Y3Q2Q3X3Y3Q';
                    
                    const viewer = new Cesium.Viewer('cesiumContainer', {{
                        terrainProvider: Cesium.createWorldTerrain(),
                        baseLayerPicker: true,
                        homeButton: true,
                        sceneModePicker: true,
                        navigationHelpButton: false,
                        animation: false,
                        timeline: false,
                        fullscreenButton: true,
                        geocoder: true
                    }});
                    
                    // Set initial view to Bhopal
                    viewer.camera.setView({{
                        destination: Cesium.Cartesian3.fromDegrees(77.4126, 23.2599, 8000.0)
                    }});
                    
                    // Area data
                    const areas = {json.dumps(areas_data)};
                    
                    // Add areas as 3D points
                    areas.forEach(area => {{
                        const color = area.score >= 70 ? Cesium.Color.fromCssColorString('{self.colors['success']}') : 
                                     area.score >= 50 ? Cesium.Color.fromCssColorString('{self.colors['warning']}') : 
                                     Cesium.Color.fromCssColorString('{self.colors['danger']}');
                        
                        viewer.entities.add({{
                            name: area.name,
                            position: Cesium.Cartesian3.fromDegrees(area.lon, area.lat, 100),
                            point: {{
                                pixelSize: 15,
                                color: color,
                                outlineColor: Cesium.Color.WHITE,
                                outlineWidth: 2
                            }},
                            label: {{
                                text: area.name,
                                font: '14pt Arial',
                                fillColor: Cesium.Color.WHITE,
                                outlineColor: Cesium.Color.BLACK,
                                outlineWidth: 2,
                                pixelOffset: new Cesium.Cartesian2(0, -30)
                            }}
                        }});
                    }});
                </script>
            </body>
            </html>
            """
            return cesium_html
        except Exception as e:
            print(f"Error generating Cesium map: {e}")
            return f"""
            <div class="alert alert-danger text-center p-4">
                <h5>🌍 3D Map Not Available</h5>
                <p class="mb-0">Error generating 3D satellite view: {str(e)}</p>
                <small>Please try refreshing the page.</small>
            </div>
            """
    
    def generate_benchmark_comparison_chart(self, area_data, all_areas):
        """Generate benchmark comparison chart for area analysis"""
        try:
            areas = [data.get('name', 'Unknown') for data in all_areas.values()]
            current_area_name = area_data.get('name', 'Current Area')
            
            # Get sustainability scores
            scores = [data.get('sustainability_score', 50) for data in all_areas.values()]
            
            # Create colors - highlight current area
            colors = []
            for area in all_areas.values():
                if area.get('name') == current_area_name:
                    colors.append(self.colors['primary'])
                else:
                    colors.append(self.colors['accent'])
            
            fig = go.Figure(data=[
                go.Bar(
                    x=areas,
                    y=scores,
                    marker_color=colors,
                    text=[f'{score:.1f}' for score in scores],
                    textposition='auto',
                    marker_line=dict(color=self.colors['dark'], width=1),
                    hovertemplate='<b>%{x}</b><br>Sustainability Score: %{y:.1f}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title=dict(
                    text='Area Comparison - Sustainability Scores',
                    font=dict(size=16, color=self.colors['primary'])
                ),
                xaxis=dict(
                    title='Areas',
                    tickangle=45
                ),
                yaxis=dict(
                    title='Sustainability Score (0-100)',
                    range=[0, 100]
                ),
                plot_bgcolor=self.colors['light'],
                paper_bgcolor='white',
                font=dict(color=self.colors['dark']),
                showlegend=False,
                height=400,
                margin=dict(l=50, r=50, t=80, b=100)
            )
            
            return fig.to_html(include_plotlyjs=False, config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating benchmark comparison chart: {e}")
            return self._generate_error_html("Benchmark Comparison Chart")
        
    def generate_performance_indicators(self, area_data):
        """Generate performance indicators gauge chart for individual area"""
        try:
            # Create gauge charts for key metrics
            metrics = [
                ('sustainability_score', 'Sustainability', 100, self.colors['primary']),
                ('transport_index', 'Transport', 10, self.colors['accent']),
                ('energy_index', 'Energy', 10, self.colors['success']),
                ('pollution_control', 'Pollution Control', 10, self.colors['warning'])
            ]
            
            # Create subplots
            fig = self._create_gauge_subplots(area_data, metrics)
            
            return fig.to_html(include_plotlyjs=False, config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating performance indicators: {e}")
            return self._generate_error_html("Performance Indicators")

    def _create_gauge_subplots(self, area_data, metrics):
        """Create gauge subplots for performance indicators"""
        fig = sp.make_subplots(
            rows=2, cols=2,
            specs=[[{'type': 'indicator'}, {'type': 'indicator'}],
                   [{'type': 'indicator'}, {'type': 'indicator'}]],
            subplot_titles=['Sustainability', 'Transport', 'Energy', 'Pollution Control']
        )
        
        for i, (metric_key, metric_name, max_val, default_color) in enumerate(metrics):
            # Get value and adjust for pollution (lower is better)
            if metric_key == 'pollution_control':
                value = 10 - area_data.get('pollution_index', 5)
            else:
                value = area_data.get(metric_key, max_val/2)
            
            # Determine color based on performance
            gauge_color = self._get_gauge_color(metric_key, value, max_val, default_color)
            
            # Add gauge trace
            fig.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=value,
                title={'text': metric_name},
                gauge={
                    'axis': {'range': [0, max_val], 'tickwidth': 1},
                    'bar': {'color': gauge_color},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': self.colors['dark'],
                    'steps': [
                        {'range': [0, max_val*0.6], 'color': self.colors['light']},
                        {'range': [max_val*0.6, max_val*0.8], 'color': self.colors['warning'] + '40'},
                        {'range': [max_val*0.8, max_val], 'color': self.colors['success'] + '40'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': max_val * 0.8
                    }
                },
                delta={'reference': max_val * 0.6, 'relative': True}
            ), row=(i//2)+1, col=(i%2)+1)
        
        fig.update_layout(
            height=400,
            margin=dict(l=50, r=50, t=80, b=50),
            paper_bgcolor='white',
            font=dict(color=self.colors['dark']),
            title=dict(
                text=f"{area_data.get('name', 'Area')} - Performance Indicators",
                font=dict(size=16, color=self.colors['primary'])
            )
        )
        
        return fig

    def _get_gauge_color(self, metric_key, value, max_val, default_color):
        """Determine gauge color based on performance"""
        if metric_key == 'sustainability_score':
            threshold_good = 70
            threshold_medium = 50
        else:
            threshold_good = max_val * 0.8
            threshold_medium = max_val * 0.6
        
        if value >= threshold_good:
            return self.colors['success']
        elif value >= threshold_medium:
            return self.colors['warning']
        else:
            return self.colors['danger']     
    
    def generate_trend_analysis(self, analysis_data):
        """Generate trend analysis chart showing area progression"""
        try:
            areas = [data.get('name', 'Unknown') for data in analysis_data.values()]
            
            # Simulate trend data (in real scenario, this would come from historical data)
            current_scores = [data.get('sustainability_score', 50) for data in analysis_data.values()]
            previous_scores = [max(0, score - np.random.randint(5, 15)) for score in current_scores]
            
            fig = go.Figure()
            
            # Add previous scores
            fig.add_trace(go.Bar(
                name='Previous Period',
                x=areas,
                y=previous_scores,
                marker_color=self.colors['accent'],
                hovertemplate='<b>%{x}</b><br>Previous Score: %{y:.1f}<extra></extra>'
            ))
            
            # Add current scores
            fig.add_trace(go.Bar(
                name='Current Period',
                x=areas,
                y=current_scores,
                marker_color=self.colors['primary'],
                hovertemplate='<b>%{x}</b><br>Current Score: %{y:.1f}<extra></extra>'
            ))
            
            # Add improvement annotations
            for i, (prev, curr) in enumerate(zip(previous_scores, current_scores)):
                improvement = curr - prev
                if improvement > 0:
                    fig.add_annotation(
                        x=areas[i],
                        y=curr + 2,
                        text=f"+{improvement:.1f}",
                        showarrow=False,
                        font=dict(color=self.colors['success'], size=12)
                    )
            
            fig.update_layout(
                title=dict(
                    text='Sustainability Score Trends - Period Comparison',
                    font=dict(size=16, color=self.colors['primary'])
                ),
                xaxis=dict(
                    title='Areas',
                    tickangle=45
                ),
                yaxis=dict(
                    title='Sustainability Score',
                    range=[0, 100]
                ),
                barmode='group',
                plot_bgcolor=self.colors['light'],
                paper_bgcolor='white',
                font=dict(color=self.colors['dark']),
                height=500,
                margin=dict(l=50, r=50, t=80, b=100),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            return fig.to_html(include_plotlyjs=False, config={'displayModeBar': True})
            
        except Exception as e:
            print(f"Error generating trend analysis: {e}")
            return self._generate_error_html("Trend Analysis Chart")

    def _generate_error_html(self, chart_name):
        """Generate error message HTML"""
        return f"""
        <div class="alert alert-warning text-center p-4">
            <h5>📊 {chart_name} Not Available</h5>
            <p class="mb-0">Data processing error. Please try refreshing the page.</p>
            <small>If the problem persists, check the console for errors.</small>
        </div>
        """