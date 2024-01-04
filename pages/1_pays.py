import streamlit as st
import pandas as pd

url = "Exemple - Hypermarché_Achats.csv"

df = pd.read_csv(url, delimiter=";")

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

# Convertir la colonne 'Ventes' en nombres (floats)
df['Ventes'] = df['Ventes'].str.replace('€', '').astype(float)

# Calculer le chiffre d'affaires par pays
revenue_by_country = df.groupby('Pays/Région')['Ventes'].sum()

# Afficher le chiffre d'affaires pour le pays sélectionné
country_revenue = revenue_by_country.get(selected_country, 0)
st.metric(label=f"Chiffre d'affaires pour {selected_country}", value=f"{country_revenue:.2f} €")
