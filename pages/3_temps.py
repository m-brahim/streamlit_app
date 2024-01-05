import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

url = "Exemple - Hypermarché_Achats.csv"

df = pd.read_csv(url, delimiter=";")
df['Ventes'] = df['Ventes'].str.replace('[^\d,]', '', regex=True)  # Supprimer tout sauf les chiffres et la virgule
df['Ventes'] = df['Ventes'].str.replace(',', '.', regex=True)  # Remplacer la virgule par le point pour le format numérique
df['Ventes'] = pd.to_numeric(df['Ventes'], errors='coerce', downcast='float')  # Convertir en nombre à virgule flottante

# Ajouter une colonne pour l'année à partir de la colonne de dates de commande
df['Année'] = pd.to_datetime(df['Date de commande'].str.replace(',', '', regex=False), format='%d/%m/%Y').dt.year

# Convertir les colonnes 'Année' et 'Ventes' en entiers après suppression des virgules
df['Année'] = df['Année'].astype(int)
df['Ventes'] = df['Ventes'].astype(int)

# Obtenir les années triées
sorted_years = sorted(df['Année'].unique())

# Titre de la page
st.set_page_config("Suivi temporel des ventes", page_icon="", layout="wide")

# Colonne pour le titre à l'extrême droite
col_title, col_dropdown = st.columns([3, 1])  # Ajustez les proportions en conséquence

with col_title:
    st.subheader("Suivi temporel des ventes")

# Liste déroulante à côté du titre
with col_dropdown:
    selected_year = st.selectbox("Sélectionnez une année", sorted_years)

st.header("Indicateurs")

st.subheader("")

# Créer trois colonnes pour aligner les widgets côte à côte
col_clients, col_orders, col_ca = st.columns(3)

# Nombre de clients
num_clients = df[df['Année'] == selected_year].drop_duplicates('ID client')['ID client'].count()
col_clients.metric(label="Nombre de clients", value=num_clients)

# Nombre de commandes pour l'année sélectionnée
num_orders = len(df[df['Année'] == selected_year]['ID commande'])
col_orders.metric(label="Nombre de commandes", value=num_orders)

# Chiffre d'affaires pour l'année sélectionnée
ca_by_year = df[df['Année'] == selected_year]['Ventes'].sum()
col_ca.metric(label=f"Chiffre d'affaires pour {selected_year}", value=f"{int(ca_by_year)} €")

# Afficher le DataFrame avec les nouvelles colonnes
st.write(df[['Date de commande', 'Année', 'Ventes']])
