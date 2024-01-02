import streamlit as st
import pandas as pd

# Titre de la page
st.set_page_config("Suivi géographique des ventes", page_icon="", layout="wide")

# Diviser la page en 10 colonnes
col1, _, _, _, _, _, _, _, _, _ = st.columns(10)

# Sous-titre dans la première colonne
col1.subheader("Suivi géographique des ventes")

url = "Exemple - Hypermarché_Achats.csv"

df = pd.read_csv(url, delimiter=";")

# Afficher le dataframe dans une des colonnes (ici, la deuxième colonne)
col2.write(df)

