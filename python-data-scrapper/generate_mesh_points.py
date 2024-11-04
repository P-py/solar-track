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

def main():
    limits = read_city_limits(FILE_PATH)
    mesh_spacing = 111
    output_mesh_file = 'reference_mesh_points.csv'
    mesh_points = generate_reference_points_mesh(limits, mesh_spacing, output_mesh_file)

    print(f"Mesh points saved to {output_mesh_file}")

if __name__ == "__main__":
    main()