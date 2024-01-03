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


st.subheader("Indicateurs")






