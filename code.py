import streamlit as st
import pandas as pd

# Données
data = {
    "Nom": ["Carrefour", "Auchan", "Leclerc"],
    "Nombre de magasins en France": [253, 136, 585],
    "Chiffre d'affaires (en millions d'euros)": [35000, 21000, 32000],
}

df = pd.DataFrame(data)

# En-tête de la page
st.title("Tableau de bords Streamlit - Suivi des commerces")

# Sélection du commerce
selected_commerce = st.sidebar.selectbox("Sélectionnez un commerce", df["Nom"])

# Filtrer les données en fonction du commerce sélectionné
filtered_data = df[df["Nom"] == selected_commerce]

# Afficher le nombre de magasins comme une métrique
st.metric("Nombre de Magasins", filtered_data["Nombre de magasins en France"].values[0])

# Afficher le chiffre d'affaires comme une métrique
st.metric("Chiffre d'Affaires (en millions d'euros)", filtered_data["Chiffre d'affaires (en millions d'euros)"].values[0])

# Afficher d'autres informations sous forme de texte
st.subheader(f"Informations sur {selected_commerce}")
st.text(f"{selected_commerce} a {filtered_data['Nombre de magasins en France'].values[0]} magasins en France.")
st.text(f"Le chiffre d'affaires est de {filtered_data['Chiffre d'affaires (en millions d'euros)'].values[0]} millions d'euros.")
