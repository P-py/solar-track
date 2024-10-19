import numpy as np
import csv

FILE_PATH = './map_base_assets/sorocaba_geo_limits.csv'

def read_city_limits(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file, delimiter=';')
        limits = {row['direction']: (float(row['latitude']), float(row['longitude'])) for row in reader}
    return limits

def meters_to_degrees(meters, latitude):
    km = meters / 1000
    lat_degree = km / 111.0
    lon_degree = km / (111.0 * np.cos(np.radians(latitude)))
    return lat_degree, lon_degree

def generate_reference_points_mesh(limits, spacing_meters, output_csv):
    north, south = limits['north'][0], limits['south'][0]
    west, east = limits['west'][1], limits['east'][1]
    
    lat_spacing, lon_spacing = meters_to_degrees(spacing_meters, (north + south) / 2)
    
    lat_points = np.arange(south, north, lat_spacing)
    lon_points = np.arange(west, east, lon_spacing)
    
    reference_points = [(lat, lon) for lat in lat_points for lon in lon_points]

    # Save reference points to a CSV file
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['latitude', 'longitude'])
        writer.writerows(reference_points)

    return reference_points

def create_heatmap(mesh_points, geo_limits, output_file):
    # Center the map around the average latitude and longitude
    avg_lat = np.mean([point[0] for point in mesh_points])
    avg_lon = np.mean([point[1] for point in mesh_points])
    
    # Create a map centered around the average point
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12, control_scale=True, zoom_control=True, min_zoom=10, max_zoom=18)

    # Create feature groups for geo limit points
    geo_limits_fg = folium.FeatureGroup(name='Geo Limits')

    # Add geo limit points to the feature group in red color with labels
    for direction, point in geo_limits.items():
        folium.Marker(location=point, popup=f"{direction.capitalize()}: Lat: {point[0]}, Lon: {point[1]}", icon=folium.Icon(color='red')).add_to(geo_limits_fg)

    # Add feature groups to the map
    geo_limits_fg.add_to(m)

    # Add heatmap to the map with adjusted radius and blur
    heat_data = [[point[0], point[1], point[2]] for point in mesh_points]
    HeatMap(heat_data, radius=15, blur=25).add_to(m)

    # Create a color scale legend
    colormap = cm.LinearColormap(colors=['blue', 'green', 'yellow', 'red'], vmin=0, vmax=100)
    colormap.caption = 'Heatmap Intensity'
    m.add_child(colormap)

    # Add custom CSS to style the color scale legend
    custom_css = """
    <style>
        .legend {
            font-size: 14px !important;
            background-color: white !important;
            border-radius: 5px !important;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.2) !important;
        }
    </style>
    """
    m.get_root().html.add_child(folium.Element(custom_css))

    # Add layer control to the map
    folium.LayerControl().add_to(m)

    # Save the map to an HTML file
    m.save(output_file)

def main():
    limits = read_city_limits(FILE_PATH)
    mesh_spacing = 111
    output_mesh_file = 'reference_mesh_points.csv'
    mesh_points = generate_reference_points_mesh(limits, mesh_spacing, output_mesh_file)

    print(f"Mesh points saved to {output_mesh_file}")

if __name__ == "__main__":
    main()