import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from geopy.distance import geodesic
import random
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt


SOROCABA_INTERVAL_POINTS_FILE = "./sorocaba_interval_points.csv"
INTERVAL_POINTS_MAP_FILE = "./sorocaba_interval_points_map.html"

REFERENCE_POINTS_FILE = "./cresesb_collect_points.csv"
OUTPUT_FILE = "./mesh_points_with_values.csv"

ALGORITHM_DEMO_FILE = "./algorithm_demo_map.html"

def read_csv(file_path):
    return pd.read_csv(file_path, delimiter=';')

def main():
    st.set_page_config(
        page_title="Solar Track",
        page_icon= "🌞",
        layout="wide"
    )
    st.title("☀️:bar_chart: Dashboard de análise de incidência solar")
    
    # Read data
    sorocaba_interval_points = read_csv(SOROCABA_INTERVAL_POINTS_FILE)
    reference_points = read_csv(REFERENCE_POINTS_FILE)
    mesh_points = read_csv(OUTPUT_FILE)
    kwh_values = mesh_points.iloc[:, 2]
    average_kwh = kwh_values.mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pontos de intervalo em Sorocaba e região", len(sorocaba_interval_points))
    col2.metric("Pontos no Mesh", len(mesh_points))
    col3.metric("Pontos de referência no CRESESB", len(reference_points))
    col4.metric("Média de kWh/m² por dia", round(average_kwh, 2))

    col1, col2, col3 = st.columns(3)
    plt.figure(figsize=(10, 6))
    plt.hist(kwh_values, bins=30, edgecolor='k', alpha=0.7)
    plt.title('Distribution of kWh/m²/day')
    plt.xlabel('kWh/m²/day')
    plt.ylabel('Frequency')
    plt.grid(True)
    col2.pyplot(plt, use_container_width=True)
    
    st.header("Pontos de intervalo em Sorocaba e região")
    st.text(
        """O mapa abaixo é composto para demonstrar os pontos de intervalo utilizados para consultar os pontos de consulta disponíveis na API do CRESESB, identificados por marcadores de cor azul. 
        \nAlém de demonstrar os pontos de limite na cidade de Sorocaba, identificados por um marcador vermelho."""
        )
    
    # Embed the content of the HTML file
    with open(INTERVAL_POINTS_MAP_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()
    components.html(html_content, height=600)

    st.header("Pontos de referência no CRESESB e Algoritmo de Mesh")
    st.text(
        """O gráfico abaixo é composto para demonstrar os pontos de referência disponíveis na API do CRESESB, identificados por marcadores de cor azul. 
        \nAlém de demonstrar os pontos de mesh gerados pelo algoritmo, identificados por marcadores de cor verde."""
        )
    with open(ALGORITHM_DEMO_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()
    components.html(html_content, height=600) 


if __name__ == "__main__":
    main()