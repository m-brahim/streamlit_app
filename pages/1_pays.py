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

# Filtrer les données en fonction du pays sélectionné
filtered_data = df[df['Pays/Région'] == selected_country]

# Calculer le chiffre d'affaires (CA)
ca_by_country = filtered_data['Ventes'].sum()

# Afficher le chiffre d'affaires en tant que métrique
st.metric(label="CA par Pays", value=f"{ca_by_country:.2f} €")




