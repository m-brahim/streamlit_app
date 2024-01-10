import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

#nom du fichier
url = "Exemple - Hypermarché_Achats.csv"

#stockage dans un df pandas + modifs sur la colonne Ventes
df = pd.read_csv(url, delimiter=";")
df['Ventes'] = df['Ventes'].str.replace('[^\d]', '', regex=True)
df['Ventes'] = pd.to_numeric(df['Ventes'], errors='coerce', downcast='integer')

#config du titre de la page
st.set_page_config("Suivi géographique des ventes :earth_africa:", page_icon="", layout="wide")

#création de colonnes avec dimensions différentes
col_title, col_dropdown = st.columns([3, 1])  # Ajustez les proportions en conséquence

#colonne contenant le titre
with col_title:
    st.subheader("Suivi géographique des ventes :earth_africa:")

#colonne contenant la liste déroulante
with col_dropdown:
    selected_country = st.selectbox("Sélectionnez un pays", df['Pays/Région'].unique())

#espacement
st.header("")



#PARTIE KPI

#titre
st.subheader("Indicateurs :mag_right:")

#espacement
st.header("")

#filtrage des données pour le pays sélectionné
filtered_data = df[df['Pays/Région'] == selected_country]

#calcul du CA pour le pays sélectionné
country_revenue = filtered_data['Ventes'].sum()

#trouver la ville avec la vente maximale pour le pays sélectionné
max_city = filtered_data.loc[filtered_data['Ventes'].idxmax(), 'Ville']

#calculer le nombre total de clients pour le pays sélectionné
num_clients = filtered_data['ID client'].nunique()

#calculer le nombre total de commandes pour le pays sélectionné
num_orders = filtered_data.groupby('ID commande').size().sum()

#création de colonnes avec dimensions identiques
col_ca, col_ville, col_orders = st.columns(3)

#afficher le chiffre d'affaires dans la première colonne
col_ca.metric(label=f"Chiffre d'affaires pour {selected_country}", value=f"{int(country_revenue)} €")

#afficher la ville avec la plus grande vente dans la deuxième colonne
col_ville.metric(label=f"Ville avec la plus grande vente ({selected_country})", value=max_city)

#afficher le nombre total de commandes dans la troisième colonne
col_orders.metric(label=f"Nombre total de commandes pour {selected_country}", value=num_orders)

#espacement
st.header("")



#PARTIE VISUALISATION

#titre
st.subheader("Visualisations :bar_chart: :chart_with_upwards_trend:")

#espacement
st.header("")

#création de colonnes avec dimensions différentes
col_map, col_space, col_pie= st.columns([3, 1, 2])

#agréger le nombre de clients par pays
clients_by_country = df.drop_duplicates(subset=['ID client', 'Pays/Région']).groupby('Pays/Région')['ID client'].count().reset_index()

#fusionner les données agrégées avec les données filtrées
merged_data = pd.merge(filtered_data, clients_by_country, how='left', on='Pays/Région')

#icône personnalisée pour représenter un client (ici l'exemple c'est Kiloutou)
icon_path = 'pages/Kiloutou_logo.jpg'
client_icon = folium.CustomIcon(icon_image=icon_path, icon_size=(30, 30))



#affiche une carte qui indique le nombre de clients par pays
with col_map:
    #titre
    st.subheader("Nombre de clients par pays")
    #définition d'une localisation initiale
    my_map = folium.Map(location=[merged_data['Latitude'].iloc[0], merged_data['Longitude'].iloc[0]], zoom_start=5)
    
    #ajoutez un seul marqueur pour représenter le pays avec le nombre de clients dans l'infobulle
    folium.Marker([merged_data['Latitude'].iloc[0], merged_data['Longitude'].iloc[0]], 
                  popup=f"Nombre de clients: {num_clients}", 
                  icon=client_icon).add_to(my_map)
    
    #affichage de la carte
    st_folium(my_map, width=1000, height=400)



#affiche un graphique en secteur qui indique le nombre de commandes pour les différentes catégories par pays
with col_pie:
    #titre
    st.subheader("Quantités vendues par catégorie")
    #calculer les quantités vendues par catégorie pour le pays sélectionné
    quantity_by_category = filtered_data.groupby('Catégorie')['Quantité'].sum().reset_index()
    #création du graphique en secteur
    colors = ['#2F2E28','#DEAB05', '#DECF05']
    fig = px.pie(quantity_by_category, values='Quantité', names='Catégorie',
             color_discrete_sequence=colors)
    #séparation des morceaux du graphique
    fig.update_traces(marker=dict(line=dict(color='#FFFFFF', width=2)))
    #affichage
    st.plotly_chart(fig, use_container_width=True)
