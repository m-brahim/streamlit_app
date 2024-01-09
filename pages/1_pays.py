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

# Titre de la page
st.set_page_config("Suivi géographique des ventes :shopping_trolley:", page_icon="", layout="wide")

# Colonne pour le titre à l'extrême droite
col_title, col_dropdown = st.columns([3, 1])  # Ajustez les proportions en conséquence

with col_title:
    st.subheader("Suivi géographique des ventes :shopping_trolley:")

# Liste déroulante à côté du titre
with col_dropdown:
    selected_country = st.selectbox("Sélectionnez un pays", df['Pays/Région'].unique())

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

# Calculer le nombre total de clients pour le pays sélectionné
num_clients = filtered_data['ID client'].nunique()

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

col_map, col_space, col_pie= st.columns([3, 1, 2])

# Agréger le nombre de clients par pays
clients_by_country = df.drop_duplicates(subset=['ID client', 'Pays/Région']).groupby('Pays/Région')['ID client'].count().reset_index()

# Fusionner les données agrégées avec les données filtrées
merged_data = pd.merge(filtered_data, clients_by_country, how='left', on='Pays/Région')

# Icône personnalisée pour représenter un client (remplacez 'path/vers/votre/icone_client.png' par le chemin de votre propre icône)
icon_path = 'pages/Kiloutou_logo.jpg'
client_icon = folium.CustomIcon(icon_image=icon_path, icon_size=(30, 30))

# Ajoutez une carte Folium avec une taille spécifique
with col_map:
    st.subheader("Nombre de clients par pays")
    my_map = folium.Map(location=[merged_data['Latitude'].iloc[0], merged_data['Longitude'].iloc[0]], zoom_start=5)
    
    # Ajoutez une seule marqueur pour représenter le pays avec le nombre de clients dans l'infobulle
    folium.Marker([merged_data['Latitude'].iloc[0], merged_data['Longitude'].iloc[0]], 
                  popup=f"Nombre de clients: {num_clients}", 
                  icon=client_icon).add_to(my_map)
    
    # Affichez la carte avec Streamlit Folium
    st_folium(my_map, width=1000, height=400)

with col_pie:
    st.subheader("Quantités vendues par catégorie")
    # Calculer les quantités vendues par catégorie pour le pays sélectionné
    quantity_by_category = filtered_data.groupby('Catégorie')['Quantité'].sum().reset_index()
    # Créer le graphique en secteur avec Plotly Express et spécifier les couleurs
    colors = ['#2F2E28','#DEAB05', '#DECF05']
    fig = px.pie(quantity_by_category, values='Quantité', names='Catégorie',
             color_discrete_sequence=colors)
    st.plotly_chart(fig, use_container_width=True)

    # Appliquer la personnalisation de la colonne avec du CSS
    st.markdown("""
    <style>
        .element-container {
            opacity: 0.8 !important;
            padding: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)
