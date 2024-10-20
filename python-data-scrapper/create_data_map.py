import numpy as np
import csv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from geopy.distance import geodesic
import random

REFERENCE_POINTS_FILE = "./cresesb_collect_points.csv"
MESH_POINTS_FILE = "./reference_mesh_points.csv"
OUTPUT_FILE = "./mesh_points_with_values.csv"

def read_csv(file_path):
    return pd.read_csv(file_path, delimiter=';')

def calculate_value(mesh_point, reference_points):
    mesh_lat = mesh_point['latitude']
    mesh_lon = mesh_point['longitude']
    
    # Calculate distances to all reference points
    distances = []
    for _, ref_point in reference_points.iterrows():
        ref_lat = ref_point['latitude']
        ref_lon = ref_point['longitude']
        distance = geodesic((mesh_lat, mesh_lon), (ref_lat, ref_lon)).meters
        distances.append((distance, ref_point))
    
    # Sort by distance and get the 3 closest reference points
    distances.sort(key=lambda x: x[0])
    closest_points = distances[:3]
    
    # Calculate the weighted average of maior_min_mensal values
    total_weight = sum(1 / d for d, _ in closest_points)
    weighted_value = sum(ref_point['maior_min_mensal'] / d for d, ref_point in closest_points) / total_weight
    
    return weighted_value

def main():
    # Read mesh points and reference points
    mesh_points = read_csv(MESH_POINTS_FILE)
    reference_points = read_csv(REFERENCE_POINTS_FILE)
    
    # Ensure there are at least 3 reference points
    if len(reference_points) < 3:
        raise ValueError("There must be at least 3 reference points in the dataset.")
    
    # Calculate values for all mesh points
    mesh_points['value'] = mesh_points.apply(lambda row: calculate_value(row, reference_points), axis=1)
    
    # Save the calculated values to the OUTPUT_FILE
    mesh_points.to_csv(OUTPUT_FILE, sep=';', index=False)
    
    # Create a scatter plot for reference points
    fig = px.scatter_mapbox(reference_points, lat='latitude', lon='longitude', hover_name='maior_min_mensal',
                            color_discrete_sequence=['red'], zoom=12)
    
    # Create a bubble map for the mesh points
    fig.add_trace(go.Scattermapbox(
        lat=mesh_points['latitude'],
        lon=mesh_points['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=mesh_points['value'] + 10,
            color=mesh_points['value'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Solar Radiation Intensity', x=0.95, xanchor='left')
        ),
        text=mesh_points['value'],
        hoverinfo='text',
        name='Mesh Points'
    ))
    
    # Update layout to make the map full screen with a top margin and hide the legend
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":50,"t":50,"l":0,"b":0},  # Add top margin
        height=800,  # Set height to occupy full screen
        showlegend=False,  # Hide the legend
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=[{"visible": [True if trace.name == 'Mesh Points' else False for trace in fig.data]}],
                        label="Show Algorithm Demo",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": [True if trace.name != 'Mesh Points' else False for trace in fig.data]}],
                        label="Show Reference Points",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": [True for _ in fig.data]}],
                        label="Show All",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": [False for _ in fig.data]}],
                        label="Hide All",
                        method="update"
                    )
                ]),
                direction="down",
                showactive=True,
                x=0.17,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
    )
    
    # Save the map to an HTML file
    fig.write_html('map.html')

if __name__ == "__main__":
    main()