import streamlit as st
import pandas as pd

# Données
data = {
    "Enseigne": ["Carrefour", "Auchan", "Leclerc"],
    "Nombre de Magasins": [253, 136, 585]
}

df = pd.DataFrame(data)

# Diviser la page en 2 colonnes
col1, col2 = st.columns(2)

# Contenu de chaque colonne
with col1:
    st.header("Données sur les magasins")

    # Afficher le tableau de données
    st.write(df)

with col2:
    st.header("Graphique en barres")

    # Afficher le graphique en barres
    st.bar_chart(df.set_index("Enseigne"))
