import matplotlib.pyplot as plt
import io
import base64
import folium
from folium import plugins
import pandas as pd
import numpy as np
from branca.colormap import LinearColormap

class DataVisualizer:
    def __init__(self):
        plt.style.use('default')
        # New color scheme based on #50589C
        self.colors = {
            'primary': '#50589C',        # Main blue-purple
            'secondary': '#7A6FBE',      # Lighter purple
            'accent': '#FF6B6B',         # Coral accent
            'dark': '#2D3748',           # Dark gray
            'light': '#F7FAFC',          # Light gray
            'success': '#48BB78',        # Green
            'warning': '#ED8936',        # Orange
            'danger': '#F56565',         # Red
            'info': '#4299E1'            # Blue
        }
    
    def generate_cesium_map(self, analysis_data):
        """Generate Cesium JS 3D map HTML"""
        cesium_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Bhopal 3D Satellite View</title>
            <script src="https://cesium.com/downloads/cesiumjs/releases/1.107/Build/Cesium/Cesium.js"></script>
            <link href="https://cesium.com/downloads/cesiumjs/releases/1.107/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
            <style>
                html, body, #cesiumContainer {{
                    width: 100%; height: 100%; margin: 0; padding: 0; overflow: hidden;
                }}
                .cesium-info-box {{
                    background: {self.colors['primary']};
                    color: white;
                }}
            </style>
        </head>
        <body>
            <div id="cesiumContainer"></div>
            <script>
                // Your access token can be found at: https://cesium.com/ion/tokens.
                // Replace with your own token if needed
                Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJlYWE1N2QxMy02MWZjLTQ3ODktODgyYS1jYjJkMjY0MWE1MWUiLCJpZCI6MjA0MzA2LCJpYXQiOjE3MTE4MTU5ODN9.8a3m9QuT3Xx1p1z0Y7W0vVQ6t6X3Y3Q2Q3X3Y3Q2Q3X3Y3Q2Q3X3Y3Q';
                
                const viewer = new Cesium.Viewer('cesiumContainer', {{
                    terrainProvider: Cesium.createWorldTerrain(),
                    baseLayerPicker: false,
                    homeButton: false,
                    sceneModePicker: false,
                    navigationHelpButton: false,
                    animation: false,
                    timeline: false,
                    fullscreenButton: false,
                    geocoder: false
                }});
                
                // Set initial view to Bhopal
                viewer.camera.setView({{
                    destination: Cesium.Cartesian3.fromDegrees(77.4126, 23.2599, 15000.0),
                    orientation: {{
                        heading: 0.0,
                        pitch: -0.5,
                        roll: 0.0
                    }}
                }});
                
                // Add Bhopal areas as 3D points
                const areas = {json.dumps([
                    {
                        'name': data['name'],
                        'lat': data['coordinates']['lat'],
                        'lon': data['coordinates']['lon'],
                        'score': data['sustainability_score'],
                        'transport': data['transport_index'],
                        'pollution': data['pollution_index'],
                        'energy': data['energy_index']
                    }
                    for data in analysis_data.values()
                ])};
                
                areas.forEach(area => {{
                    const color = area.score >= 70 ? Cesium.Color.GREEN : 
                                 area.score >= 50 ? Cesium.Color.YELLOW : 
                                 Cesium.Color.RED;
                    
                    const entity = viewer.entities.add({{
                        name: area.name,
                        position: Cesium.Cartesian3.fromDegrees(area.lon, area.lat),
                        point: {{
                            pixelSize: 15,
                            color: color,
                            outlineColor: Cesium.Color.WHITE,
                            outlineWidth: 2,
                            heightReference: Cesium.HeightReference.CLAMP_TO_GROUND
                        }},
                        label: {{
                            text: area.name,
                            font: '14pt Arial',
                            pixelOffset: new Cesium.Cartesian2(0, -20),
                            fillColor: Cesium.Color.WHITE,
                            outlineColor: Cesium.Color.BLACK,
                            outlineWidth: 2,
                            style: Cesium.LabelStyle.FILL_AND_OUTLINE,
                            heightReference: Cesium.HeightReference.CLAMP_TO_GROUND
                        }},
                        description: `
                            <div style="padding: 10px; background: {self.colors['primary']}; color: white; border-radius: 5px;">
                                <h3>${{area.name}}</h3>
                                <p><strong>Sustainability Score:</strong> ${{area.score}}</p>
                                <p><strong>Transport:</strong> ${{area.transport}}</p>
                                <p><strong>Pollution:</strong> ${{area.pollution}}</p>
                                <p><strong>Energy:</strong> ${{area.energy}}</p>
                            </div>
                        `
                    }});
                }});
                
                // Add satellite imagery layer
                viewer.imageryLayers.addImageryProvider(new Cesium.IonImageryProvider({{
                    assetId: 3954  // Sentinel-2 imagery
                }}));
            </script>
        </body>
        </html>
        """
        return cesium_html
    
    def generate_area_sustainability_chart(self, area_data):
        """Generate sustainability chart for individual area"""
        metrics = ['Transport', 'Pollution', 'Energy', 'Sustainability']
        values = [
            area_data['transport_index'],
            100 - area_data['pollution_index'],  # Invert pollution for positive scale
            area_data['energy_index'],
            area_data['sustainability_score']
        ]
        
        colors = [self.colors['primary'], self.colors['danger'], 
                 self.colors['success'], self.colors['accent']]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(metrics, values, color=colors, alpha=0.8)
        
        ax.set_ylabel('Score (0-100)', fontsize=12, fontweight='bold')
        ax.set_title(f'Sustainability Metrics - {area_data["name"]}', 
                    fontsize=14, fontweight='bold', color=self.colors['dark'])
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)
        ax.set_facecolor(self.colors['light'])
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        img.seek(0)
        chart_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{chart_url}"
    
    def generate_sustainability_chart(self, analysis_data):
        """Generate sustainability score chart with new colors"""
        areas = [data['name'] for data in analysis_data.values()]
        scores = [data['sustainability_score'] for data in analysis_data.values()]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        colors = []
        for score in scores:
            if score >= 70:
                colors.append(self.colors['success'])
            elif score >= 50:
                colors.append(self.colors['warning'])
            else:
                colors.append(self.colors['danger'])
        
        bars = ax.bar(areas, scores, color=colors, alpha=0.8)
        ax.set_ylabel('Sustainability Score (0-100)', fontsize=12, fontweight='bold')
        ax.set_title('Overall Sustainability Scores - Bhopal Areas', 
                    fontsize=14, fontweight='bold', color=self.colors['dark'])
        ax.set_xticklabels(areas, rotation=45, ha='right')
        ax.grid(True, alpha=0.3)
        ax.set_facecolor(self.colors['light'])
        
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{score:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        img.seek(0)
        chart_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{chart_url}"
    
    # ... (keep all other methods the same but update colors to use the new scheme)