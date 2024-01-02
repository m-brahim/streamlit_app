import streamlit as st
import pandas as pd

# Titre de la page

st.title(":green[Suivi géographique des ventes]")

url = "Exemple - Hypermarché_Achats.csv"

df = pd.read_csv(url, delimiter=";")

st.write(df)

  
