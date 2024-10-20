import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from geopy.distance import geodesic
import random
import streamlit.components.v1 as components

REFERENCE_POINTS_FILE = "./cresesb_collect_points.csv"
MESH_POINTS_FILE = "./reference_mesh_points.csv"
OUTPUT_FILE = "./mesh_points_with_values.csv"
INTERVAL_POINTS_MAP_FILE = "./sorocaba_interval_points_map.html"

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
    reference_points = read_csv(REFERENCE_POINTS_FILE)
    mesh_points = read_csv(MESH_POINTS_FILE)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pontos de intervalo em Sorocaba e região", len(reference_points))
    col2.metric("Pontos no Mesh", len(mesh_points))
    
    st.header("Sorocaba Interval Points")
    st.text(
        """O mapa abaixo é composto para demonstrar os pontos de intervalo utilizados para consultar os pontos de consulta disponíveis na API do CRESESB, identificados por marcadores de cor azul. 
        \nAlém de demonstrar os pontos de limite na cidade de Sorocaba, identificados por um marcador vermelho."""
        )
    
    # Embed the content of the HTML file
    with open(INTERVAL_POINTS_MAP_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()
    components.html(html_content, height=600)


if __name__ == "__main__":
    main()