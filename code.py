import streamlit as st
import pandas as pd

commerces = ["Auchan", "Carrefour", "Leclerc", "Lidl", "Aldi"]

# Diviser la page en 4 colonnes
col1, col2, col3, col4 = st.columns(4)

# Contenu de chaque colonne
with col1:
    st.header("Liste des commerces")
    st.write(commerces)
