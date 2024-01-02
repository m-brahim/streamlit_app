import streamlit as st
import matplotlib.pyplot as plt
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

    # Créer le graphique en barres avec Matplotlib
    fig, ax = plt.subplots()
    ax.bar(df["Enseigne"], df["Nombre de Magasins"])
    ax.set_ylabel("Nombre de Magasins")
    ax.set_title("Nombre de Magasins par Enseigne")

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)
