import numpy as np
import csv
import random

# Coordenadas dos pontos extremos
north = (-23.405542244773343, -47.41309792195946)
east = (-23.4906559932759, -47.38672677714279)
west = (-23.502674354122384, -47.546992585249605)
south = (-23.54892310696484, -47.47348514185095)

# Definindo os limites de latitude e longitude
lat_max = north[0]
lat_min = south[0]
long_min = west[1]
long_max = east[1]

# Definindo a precisão
precision = 0.05

# Gerando as coordenadas
latitudes = np.arange(lat_min, lat_max, precision)
longitudes = np.arange(long_min, long_max, precision)

# Nome do arquivo CSV de saída
output_file = 'coordenadas.csv'

# Escrevendo os dados no arquivo CSV
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['latitude', 'longitude', 'valor'])

    for lat in latitudes:
        for lon in longitudes:
            valor = round(random.uniform(0, 1000), 6)
            writer.writerow([lat, lon, valor])

print(f"Arquivo CSV '{output_file}' criado com sucesso!")