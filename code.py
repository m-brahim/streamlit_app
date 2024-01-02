import streamlit as st
import pandas as pd

st.title("Tableau de bords Streamlit")

# Données
data = {
    "Nom": ["Carrefour", "Auchan", "Leclerc"],
    "Nombre de magasins en France": [253, 136, 585],
}

df = pd.DataFrame(data)

# Diviser la page en 2 colonnes
col1, col2 = st.columns(2)

# Contenu de chaque colonne
with col1:
    st.header("Données sur les commerces")

    # Afficher le tableau de données sans le nombre de magasins
    st.write(df[["Nom"]])

with col2:
    st.header("Graphique en barres")

    # Afficher le graphique en barres avec le "Nom" comme étiquettes d'axe et le nombre de magasins comme valeurs
    st.bar_chart(df.set_index("Nom"), use_container_width=True)
