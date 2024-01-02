import streamlit as st
import pandas as pd  # Ajout de l'import manquant

selection = st.sidebar.radio("Aller à :", ["Commerces", "Activité"])

if selection == "Commerces":
    # Titre de la page
    st.title(":green[Liste des commerces]")
    file_path = st.file_uploader("Sélectionnez un fichier CSV", type=["csv"])
    if file_path is not None:
        # Lire le fichier CSV
        df = pd.read_csv(file_path)
        # Afficher le DataFrame
        st.write(df)
