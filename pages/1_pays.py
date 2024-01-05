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
st.set_page_config("Suivi géographique des ventes", page_icon="", layout="wide")

# Colonne pour le titre à l'extrême droite
col_title, col_dropdown = st.columns([3, 1])  # Ajustez les proportions en conséquence

with col_title:
    st.subheader("Suivi géographique des ventes")

# Liste déroulante à côté du titre
with col_dropdown:
    selected_country = st.selectbox("Sélectionnez un pays", df['Pays/Région'].unique())

st.header("")

# Ajouter le 2ème titre
st.subheader("Indicateurs")

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
st.subheader("Visualisation")

st.header("")

col_pie, col_space, col_map = st.columns([2, 1, 2])

with col_pie :
    st.subheader("Quantités vendues par catégorie")
    # Calculer les quantités vendues par catégorie pour le pays sélectionné
    quantity_by_category = filtered_data.groupby('Catégorie')['Quantité'].sum().reset_index()
    # Créer le graphique en secteur avec Plotly Express
    fig = px.pie(quantity_by_category, values='Quantité', names='Catégorie')
    st.plotly_chart(fig, use_container_width=True)
    
with col_map:
    st.subheader("Carte des ventes par ville")

    # Créer une carte Folium centrée sur le pays sélectionné
    map_center = filtered_data.groupby(['Pays/Région']).size().reset_index().mean()[['Latitude', 'Longitude']]
    my_map = folium.Map(location=[map_center['Latitude'], map_center['Longitude']], zoom_start=6)

    # Ajouter des marqueurs pour chaque ville avec le chiffre d'affaires comme popup
    for index, row in filtered_data.iterrows():
        folium.Marker([row['Pays/Région']], 
                      popup=f"{row['Ville']} - {row['Ventes']} €").add_to(my_map)

    # Utiliser le wrapper streamlit pour afficher la carte
    st_folium(my_map, width=800, height=500)
