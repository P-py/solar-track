import pandas as pd
import folium
from folium.plugins import HeatMap
import plotly.express as px

dataframe = pd.read_csv('coordenadas.csv', sep=';')


#fig = px.density_mapbox(
#	dataframe, 
#	lat='latitude', 
#	lon='longitude', 
#	z='valor', 
#	radius=20,
#	center=dict(lat=dataframe.latitude.mean(), lon=dataframe.longitude.mean()),
#	zoom=25,
#	height=900,
#	mapbox_style='open-street-map'
#	)
#
#fig.show()

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

m = folium.Map(
	location=[-23.47002, -47.42965],
	zoom_start=17,
	control_scale=True,
    zoom_control=False,
    tiles="OpenStreetMap"
	)

folium.TileLayer("OpenStreetMap")

mapValues = dataframe [['latitude', 'longitude', 'valor']]

data = mapValues.values.tolist()
print(data[0][0])
print(data[0][1])

custom_gradient = {0.0:'blue', 1000:'red'}
heatMap = HeatMap(
 	data,
    name = "Solar Radiation Map",
 	radius=55,
    min_opacity=0.3,
    blur=30,
    control=True,
).add_to(m)

folium.LayerControl().add_to(m)
folium.CircleMarker(north).add_to(m)
folium.CircleMarker(south).add_to(m)
folium.CircleMarker(east).add_to(m)
folium.CircleMarker(west).add_to(m)

m.save("test_map.html")