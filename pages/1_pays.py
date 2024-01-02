import streamlit as st
import pandas as pd

# Titre de la page

st.set_page_config("Suivi géographique des ventes", page_icon="", layout="wide")
st.subheader("Suivi géographique des ventes")

url = "Exemple - Hypermarché_Achats.csv"

df = pd.read_csv(url, delimiter=";")

st.write(df)
