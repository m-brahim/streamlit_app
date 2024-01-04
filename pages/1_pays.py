import streamlit as st
import pandas as pd
import plotly.express as px

url = "Exemple - Hypermarché_Achats.csv"

df = pd.read_csv(url, delimiter=";")
df['Ventes'] = df['Ventes'].str.replace('[^\d]', '', regex=True)
df['Ventes'] = pd.to_numeric(df['Ventes'], errors='coerce', downcast='integer')

# Titre de la page
st.set_page_config("Suivi géographique des ventes", page_icon="", layout="wide")

# Colonne pour le titre à l'extrême gauche
col_title, col_dropdown = st.columns([3, 1])

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

# Colonne pour la visualisation à gauche
col_visualization, col_others = st.columns(2)

with col_visualization:
    st.subheader("Visualisation")

    # Liste déroulante à côté du titre
    selected_category = st.selectbox("Sélectionnez une catégorie", df['Catégorie'].unique())

    # Filtrer les données par catégorie
    filtered_data_category = df[df['Catégorie'] == selected_category]

    # Calculer les quantités vendues par pays pour la catégorie sélectionnée
    quantity_by_country = filtered_data_category.groupby('Pays/Région')['Quantité'].sum().reset_index()

    # Créer le graphique en secteur avec Plotly Express
    fig = px.pie(quantity_by_country, values='Quantité', names='Pays/Région', title=f"Quantités vendues par pays - Catégorie: {selected_category}")
    st.plotly_chart(fig, use_container_width=True)

# Colonne pour les autres visualisations à droite
with col_others:
    st.subheader("Autres Visualisations")
    # Ajoutez d'autres visualisations à droite de votre choix


