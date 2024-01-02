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

    # Afficher le graphique en barres avec les noms des magasins au-dessus des barres
    chart = st.bar_chart(df.set_index("Nom"), use_container_width=True)

    # Personnaliser l'axe des abscisses
    chart.set_axis_labels("Nombre de magasins par enseigne", "Nombre de magasins")
    chart.set_axis_types("ordinal", "linear")
    chart.set_title("Nombre de magasins par enseigne")

    # Ajouter les noms des magasins au-dessus de chaque barre
    for i, label in enumerate(df["Nom"]):
        st.text(label)
