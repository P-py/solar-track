import numpy as np
import csv
import folium

FILE_PATH = './map_base_assets/sorocaba_geo_limits.csv'

def read_city_limits(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file, delimiter=';')
        limits = {row['direction']: (float(row['latitude']), float(row['longitude'])) for row in reader}
    return limits

def km_to_degrees(km, latitude):
    # Approximate conversion
    lat_degree = km / 111.0
    lon_degree = km / (111.0 * np.cos(np.radians(latitude)))
    return lat_degree, lon_degree

def generate_interval_points(limits, spacing_km, output_csv):
    north, south = limits['north'][0], limits['south'][0]
    west, east = limits['west'][1], limits['east'][1]
    
    lat_spacing, lon_spacing = km_to_degrees(spacing_km, (north + south) / 2)
    
    lat_points = np.arange(south, north, lat_spacing)
    lon_points = np.arange(west, east, lon_spacing)
    
    interval_points = [(lat, lon) for lat in lat_points for lon in lon_points]

    # Save interval points to a csv
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['latitude', 'longitude'])
        writer.writerows(interval_points)

    return interval_points

def create_map(interval_points, geo_limits, output_file):
    # Center the map around the average latitude and longitude
    avg_lat = np.mean([point[0] for point in interval_points])
    avg_lon = np.mean([point[1] for point in interval_points])
    
    # Create a map centered around the average point
    # Create a map centered around the average point with zoom control precision
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12, control_scale=True, zoom_control=True, min_zoom=10, max_zoom=18)

    # Create feature groups for interval points and geo limit points
    interval_points_fg = folium.FeatureGroup(name='interval Points')
    geo_limits_fg = folium.FeatureGroup(name='Geo Limits')

    # Add interval points to the feature group with labels
    for point in interval_points:
        folium.Marker(location=point, popup=f"Lat: {point[0]}, Lon: {point[1]}").add_to(interval_points_fg)

    # Add geo limit points to the feature group in red color with labels
    for direction, point in geo_limits.items():
        folium.Marker(location=point, popup=f"{direction.capitalize()}: Lat: {point[0]}, Lon: {point[1]}", icon=folium.Icon(color='red')).add_to(geo_limits_fg)

    # Add feature groups to the map
    interval_points_fg.add_to(m)
    geo_limits_fg.add_to(m)

    # Add layer control to the map
    folium.LayerControl().add_to(m)

    # Save the map to an HTML file
    m.save(output_file)

def main():
    limits = read_city_limits(FILE_PATH)
    spacing_km = 2.5
    interval_points_file = 'sorocaba_interval_points.csv'
    interval_points = generate_interval_points(limits, spacing_km, interval_points_file)

    # Create and save the map
    output_file = 'sorocaba_interval_points_map.html'
    create_map(interval_points, limits, output_file)
    print(f"Map saved to {output_file}")
    print(f"Interval points saved to {interval_points_file}")

if __name__ == "__main__":
    main()