import streamlit as st
import pandas as pd

# Diviser la page en 4 colonnes
col1, col2, col3, col4 = st.columns(4)

# Contenu de chaque colonne
with col1:
    st.header("Colonne 1")
    # Ajoutez le contenu de la première colonne ici

with col2:
    st.header("Colonne 2")
    # Ajoutez le contenu de la deuxième colonne ici

with col3:
    st.header("Colonne 3")
    # Ajoutez le contenu de la troisième colonne ici

with col4:
    st.header("Colonne 4")
    # Ajoutez le contenu de la quatrième colonne ici



