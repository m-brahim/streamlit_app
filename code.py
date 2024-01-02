import streamlit as st
import pandas as pd

# Données
data = {
    "Entreprise": ["Aldi", "Intermarché", "Carrefour"],
    "Nombre de magasins": [1300, 1800, 253],
    "CA 2022": [27000000000, 14500000000, 42000000000],
}

df = pd.DataFrame(data)

# En-tête de la page
st.title("Tableau de bords Streamlit - Suivi des commerces")

# Sélection du commerce
selected_commerce = st.sidebar.selectbox("Sélectionnez un commerce", df["Entreprise"])

# Filtrer les données en fonction du commerce sélectionné
filtered_data = df[df["Entreprise"] == selected_commerce]

# Afficher les métriques dans trois colonnes
col1, col2, col3 = st.columns(3)

# Métrique 1 - Entreprise
col1.metric("Entreprise", selected_commerce)

# Métrique 2 - Nombre de Magasins
col2.metric("Nombre de Magasins", filtered_data["Nombre de magasins"].values[0])

# Métrique 3 - CA 2022
col3.metric("CA 2022", f"{filtered_data['CA 2022'].values[0]:,} euros")

# Afficher d'autres informations sous forme de texte
st.subheader(f"Informations sur {selected_commerce}")
st.text(f"{selected_commerce} a {filtered_data['Nombre de magasins'].values[0]} magasins.")
st.text(f"Le chiffre d'affaires pour 2022 est de {filtered_data['CA 2022'].values[0]:,} euros.")
