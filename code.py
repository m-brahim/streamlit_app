import streamlit as st
import pandas as pd  # Ajout de l'import manquant

selection = st.sidebar.radio("Aller à :", ["Commerces", "Activité"])

if selection == "Commerces":
    # Titre de la page
    st.title(":green[Liste des commerces]")
    
    def afficher_info_commerce(nom, logo, nombre_magasins, secteur_activite, autres_infos):
    """
    Affiche les informations d'un commerce.
    """
    st.markdown(f"## {nom}")
    st.image(logo, caption=f"Logo de {nom}", use_column_width=True)
    st.write(f"**Nombre de magasins en France:** {nombre_magasins}")
    st.write(f"**Secteur d'activité:** {secteur_activite}")
    st.write(f"**Autres informations:** {autres_infos}")

    def main():
    st.title("Commerces")

    commerce_selectionne = st.sidebar.selectbox("Sélectionnez un commerce", ["Auchan", "Carrefour", "Leclerc", "Lidl", "Aldi"])

    commerces = {
        "Auchan": {
            "logo": "auchan_logo.png",  # Mettez le chemin correct vers le logo Auchan
            "nombre_magasins": 1443,
            "secteur_activite": "Hypermarché",
            "autres_infos": "Informations supplémentaires pour Auchan.",
        },
        "Carrefour": {
            "logo": "carrefour_logo.png",  # Mettez le chemin correct vers le logo Carrefour
            "nombre_magasins": 1200,
            "secteur_activite": "Hypermarché",
            "autres_infos": "Informations supplémentaires pour Carrefour.",
        },
        "Leclerc": {
            "logo": "leclerc_logo.png",  # Mettez le chemin correct vers le logo Leclerc
            "nombre_magasins": 732,
            "secteur_activite": "Hypermarché",
            "autres_infos": "Informations supplémentaires pour Leclerc.",
        },
        "Lidl": {
            "logo": "lidl_logo.png",  # Mettez le chemin correct vers le logo Lidl
            "nombre_magasins": 1600,
            "secteur_activite": "Supermarché",
            "autres_infos": "Informations supplémentaires pour Lidl.",
        },
        "Aldi": {
            "logo": "aldi_logo.png",  # Mettez le chemin correct vers le logo Aldi
            "nombre_magasins": 1200,
            "secteur_activite": "Supermarché",
            "autres_infos": "Informations supplémentaires pour Aldi.",
        },
    }

    afficher_info_commerce(commerce_selectionne, **commerces[commerce_selectionne])

if __name__ == "__main__":
    main()
