import streamlit as st
import pandas as pd

url = "Exemple - Hypermarché_Achats.csv"

df = pd.read_csv(url, delimiter=";")

# Nettoyer la colonne 'Ventes' en supprimant les caractères non numériques
df['Ventes'] = df['Ventes'].str.replace('[-?\d+]', '', regex=True)

# Convertir la colonne 'Ventes' en entiers
df['Ventes'] = pd.to_numeric(df['Ventes'], errors='coerce', downcast='integer')

# Titre de la page
st.set_page_config("Suivi géographique des ventes", page_icon="", layout="wide")

# Colonne pour le titre à l'extrême droite
col_title, col_dropdown = st.columns([3, 1])  # Ajustez les proportions en conséquence

# Titre à l'extrême droite
with col_title:
    st.subheader("Suivi géographique des ventes")

# Liste déroulante à côté du titre
with col_dropdown:
    selected_country = st.selectbox("Sélectionnez un pays", df['Pays/Région'].unique())

# Ajouter le deuxième titre "Indicateurs" en dessous du premier
st.subheader("Indicateurs")

st.header("")

# Filtrer les données pour le pays sélectionné
filtered_data = df[df['Pays/Région'] == selected_country]

# Calculer le chiffre d'affaires pour le pays sélectionné
country_revenue = filtered_data['Ventes'].sum()

# Afficher le chiffre d'affaires pour le pays sélectionné
formatted_revenue = f"{int(country_revenue)} €" if country_revenue else "N/A"
st.metric(label=f"Chiffre d'affaires pour {selected_country}", value=formatted_revenue)

# Trouver la ville avec la vente maximale pour le pays sélectionné
max_city = filtered_data.loc[filtered_data['Ventes'].idxmax(), 'Ville']

# Afficher la ville avec la vente maximale
st.metric(label=f"Ville avec la plus grande vente ({selected_country})", value=max_city)



