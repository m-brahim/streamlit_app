import streamlit as st
import pandas as pd

st.title("Tableau de bords Streamlit")

# Données
data = {
    "Enseignes": ["Carrefour", "Auchan", "Leclerc"],
    "Nombre de magasins en France": [253, 136, 585],
}

df = pd.DataFrame(data)

# Sidebar pour la sélection du commerce
selected_commerce = st.sidebar.selectbox("Sélectionnez un commerce", df["Enseignes"])

# Filtrer les données en fonction du commerce sélectionné
filtered_df = df[df["Enseignes"] == selected_commerce]

# Diviser la page en 2 colonnes
col1, col2 = st.columns(2)

# Contenu de chaque colonne
with col1:
    st.header("Données sur les commerces")

    # Afficher le tableau de données sans le nombre de magasins
    st.write(filtered_df[["Enseignes"]])

with col2:
    st.header("Graphique en barres")
    st.write(f"{selected_commerce} a {filtered_df['Nombre de magasins en France'].values[0]} magasins.")
