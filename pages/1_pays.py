import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

url = "Exemple - Hypermarché_Achats.csv"

df = pd.read_csv(url, delimiter=";")
df['Ventes'] = df['Ventes'].str.replace('[^\d]', '', regex=True)
df['Ventes'] = pd.to_numeric(df['Ventes'], errors='coerce', downcast='integer')

# Titre de la page
st.set_page_config("Suivi géographique des ventes :shopping_trolley:", page_icon="", layout="wide")

# Colonne pour le titre à l'extrême droite
col_title, col_dropdown = st.columns([3, 1])  # Ajustez les proportions en conséquence

with col_title:
    st.subheader("Suivi géographique des ventes :shopping_trolley:")

# Liste déroulante à côté du titre
with col_dropdown:
    selected_country = st.selectbox("Sélectionnez un pays", filtered_data['Pays/Région'].unique(), key="unique_key_for_selectbox")

st.header("")

# Ajouter le 2ème titre
st.subheader("Indicateurs :mag_right:")

st.header("")

# Filtrer les données pour le pays sélectionné
filtered_data = df[df['Pays/Région'] == selected_country]

# Calculer le chiffre d'affaires pour le pays sélectionné
country_revenue = filtered_data['Ventes'].sum()

# Trouver la ville avec la vente maximale pour le pays sélectionné
max_city = filtered_data.loc[filtered_data['Ventes'].idxmax(), 'Ville']

# Calculer le nombre total de commandes pour le pays sélectionné
num_orders = filtered_data.groupby('ID commande').size().sum()

# Créer trois colonnes pour aligner les widgets côte à côte
col_ca, col_ville, col_orders = st.columns(3)

# Afficher le chiffre d'affaires dans la première colonne
col_ca.metric(label=f"Chiffre d'affaires pour {selected_country}", value=f"{int(country_revenue)} €")

# Afficher la ville avec la plus grande vente dans la deuxième colonne
col_ville.metric(label=f"Ville avec la plus grande vente ({selected_country})", value=max_city)

# Afficher le nombre total de commandes dans la troisième colonne
col_orders.metric(label=f"Nombre total de commandes pour {selected_country}", value=num_orders)

st.header("")

# Visualisation
st.subheader("Visualisations :bar_chart: :chart_with_upwards_trend:")

st.header("")

col_pie, col_space, col_map = st.columns([2, 1, 2])

with col_pie :
    st.subheader("Quantités vendues par catégorie")
    # Calculer les quantités vendues par catégorie pour le pays sélectionné
    quantity_by_category = filtered_data.groupby('Catégorie')['Quantité'].sum().reset_index()
    # Créer le graphique en secteur avec Plotly Express
    fig = px.pie(quantity_by_category, values='Quantité', names='Catégorie')
    st.plotly_chart(fig, use_container_width=True)

# Filtrer les données où les coordonnées existent
filtered_data = df[df['Latitude'].notnull() & df['Longitude'].notnull()]

# Sélectionner un pays spécifique
selected_country = st.selectbox("Sélectionnez un pays", filtered_data['Pays/Région'].unique())

# Filtrer les données pour le pays sélectionné
country_data = filtered_data[filtered_data['Pays/Région'] == selected_country]

# Créer une carte avec les coordonnées géographiques du pays sélectionné
country_map = folium.Map(location=[country_data['Latitude'].mean(), country_data['Longitude'].mean()], zoom_start=6)

# Ajouter un marqueur pour le pays avec la somme des ventes
folium.Marker(
    location=[country_data['Latitude'].mean(), country_data['Longitude'].mean()],
    popup=f"{selected_country}: {country_data['Ventes'].sum()} ventes"
).add_to(country_map)

# Afficher la carte du pays dans Streamlit
with col_map:
    st_folium(country_map)
