import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

url = "Exemple - Hypermarché_Achats.csv"

df = pd.read_csv(url, delimiter=";")
df['Ventes'] = df['Ventes'].str.replace('[^\d]', '', regex=True)
df['Ventes'] = pd.to_numeric(df['Ventes'], errors='coerce', downcast='integer')

# Ajouter une colonne pour l'année à partir de la colonne de dates de commande
df['Année'] = pd.to_datetime(df['Date de commande'], format='%d/%m/%Y').dt.year

# Obtenir les années triées
sorted_years = sorted(df['Année'].unique())

# Titre de la page
st.set_page_config("Suivi temporel des ventes", page_icon="", layout="wide")

# Colonne pour le titre à l'extrême droite
col_title, col_dropdown = st.columns([3, 1])  # Ajustez les proportions en conséquence

with col_title:
    st.subheader("Suivi temporel des ventes")

    # Ajouter le premier métrique (nombre de clients)
    num_clients = df[df['Année'] == selected_year]['ID client'].unique()
    st.metric(label="Nombre de clients", value=num_clients)

# Liste déroulante à côté du titre
with col_dropdown:
    selected_year = st.selectbox("Sélectionnez une année", sorted_years)