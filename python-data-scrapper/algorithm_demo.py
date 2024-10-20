import numpy as np
import csv
import folium
from geopy.distance import geodesic
import random

REFERENCE_POINTS_FILE = "./cresesb_collect_points.csv"
MESH_POINTS_FILE = "./reference_mesh_points.csv"

def read_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file, delimiter=';')
        return [row for row in reader]

def calculate_value(mesh_point, reference_points):
    mesh_lat = float(mesh_point['latitude'])
    mesh_lon = float(mesh_point['longitude'])
    
    # Calculate distances to all reference points
    distances = []
    for ref_point in reference_points:
        ref_lat = float(ref_point['latitude'])
        ref_lon = float(ref_point['longitude'])
        distance = geodesic((mesh_lat, mesh_lon), (ref_lat, ref_lon)).meters
        distances.append((distance, ref_point))
    
    # Sort by distance and get the 3 closest reference points
    distances.sort(key=lambda x: x[0])
    closest_points = distances[:3]
    
    # Calculate the weighted average of media_horizontal values
    total_weight = sum(1 / d[0] for d in closest_points)
    weighted_value = sum(float(d[1]['media_horizontal']) / d[0] for d in closest_points) / total_weight
    
    return weighted_value

def main():
    # Read mesh points and reference points
    mesh_points = read_csv(MESH_POINTS_FILE)
    reference_points = read_csv(REFERENCE_POINTS_FILE)
    
    # Ensure there are at least 3 reference points
    if len(reference_points) < 3:
        raise ValueError("There must be at least 3 reference points in the dataset.")
    
    # Create a new map centered around the average latitude and longitude of the reference points
    avg_lat = np.mean([float(point['latitude']) for point in reference_points])
    avg_lon = np.mean([float(point['longitude']) for point in reference_points])
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)
    
    # Create a feature group for the algorithm demo
    algorithm_demo_fg = folium.FeatureGroup(name='Algorithm Demo')

    # Add markers for all reference points with red color and labels showing their media_horizontal value
    for ref_point in reference_points:
        folium.Marker(
            location=[float(ref_point['latitude']), float(ref_point['longitude'])],
            popup=f"Media Horizontal: {ref_point['media_horizontal']}",
            icon=folium.Icon(color='red')
        ).add_to(algorithm_demo_fg)

    # Select 3 random points from the mesh dataset
    random_mesh_points = random.sample(mesh_points, 1)

    for mesh_point in random_mesh_points:
        mesh_lat = float(mesh_point['latitude'])
        mesh_lon = float(mesh_point['longitude'])
        
        # Calculate the value for the mesh point
        value = calculate_value(mesh_point, reference_points)
        
        # Add marker for the mesh point with the calculated value in the popup
        folium.Marker(
            location=[mesh_lat, mesh_lon],
            popup=f"Random Mesh Point\nCalculated Value: {value:.2f}",
            icon=folium.Icon(color='blue')
        ).add_to(algorithm_demo_fg)
        
        # Find the 3 closest reference points
        distances = []
        for ref_point in reference_points:
            ref_lat = float(ref_point['latitude'])
            ref_lon = float(ref_point['longitude'])
            distance = geodesic((mesh_lat, mesh_lon), (ref_lat, ref_lon)).meters
            distances.append((distance, ref_point))
        
        distances.sort(key=lambda x: x[0])
        closest_points = distances
        
        # Draw lines from the mesh point to the 3 closest reference points and add labels
        for d in closest_points:
            ref_point = d[1]
            folium.PolyLine(
                locations=[[mesh_lat, mesh_lon], [float(ref_point['latitude']), float(ref_point['longitude'])]],
                color='green'
            ).add_to(algorithm_demo_fg)
            
            # Calculate the midpoint of the line
            mid_lat = (mesh_lat + float(ref_point['latitude'])) / 2
            mid_lon = (mesh_lon + float(ref_point['longitude'])) / 2
            
            # Add a marker at the midpoint with the distance as the label
            folium.Marker(
                location=[mid_lat, mid_lon],
                icon=folium.DivIcon(html=f'''
                    <div style="font-size: 14px; font-style: bold; color: green; background-color: white; width: 80px">
                        {d[0]:.2f} m
                    </div>
                ''')
            ).add_to(algorithm_demo_fg)

    # Add the feature group to the map
    algorithm_demo_fg.add_to(m)
    
    # Save the map to an HTML file
    m.save('algorithm_demo_map.html')

if __name__ == "__main__":
    main()