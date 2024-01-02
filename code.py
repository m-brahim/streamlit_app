import streamlit as st
import pandas as pd

# Données
data = {
    "Entreprise": ["Aldi", "Intermarché", "Carrefour"],
    "Nombre de magasins": [1300, 1800, 253],
    "CA 2022": [27000000000, 14500000000, 42000000000],
}

df = pd.DataFrame(data)

# Dictionnaire de correspondance entre le commerce et le chemin du logo
logo_paths = {
    "Aldi": "Aldi_logo.png",
    "Intermarché": "Intermarche_logo.png",
    "Carrefour": "Lidl_logo.png",
}

# En-tête de la page
st.set_page_config("Tableau de bords de suivi", page_icon="", layout="wide")
st.subheader("Tableau de bords de suivi")

# Sélection du commerce
selected_commerce = st.sidebar.selectbox("Sélectionnez un commerce", df["Entreprise"])

# Filtrer les données en fonction du commerce sélectionné
filtered_data = df[df["Entreprise"] == selected_commerce]

# Récupérer le chemin du logo en fonction du commerce sélectionné
logo_path = logo_paths.get(selected_commerce, "Chemin par défaut si le logo n'est pas trouvé")

# Taille des métriques
metric_size = (100, 60)

# Afficher les métriques dans trois colonnes
col1, col2, col3 = st.columns(3)

# Métrique 1 - Entreprise avec logo
col1.image(logo_path, width=metric_size[0], use_container_width=False)
col1.header("Enseigne")

# Métrique 2 - Nombre de Magasins
col2.metric("Nombre de Magasins", filtered_data["Nombre de magasins"].values[0])

# Métrique 3 - CA 2022
# Convertir le chiffre d'affaires en milliards d'euros avec deux chiffres
ca_milliards = filtered_data['CA 2022'].values[0] / 1e9
ca_str = f"{ca_milliards:.2f} Mds €"
col3.metric("CA 2022", ca_str)

# Afficher d'autres informations sous forme de texte
st.subheader(f"Informations sur {selected_commerce}")
st.text(f"{selected_commerce} a {filtered_data['Nombre de magasins'].values[0]} magasins.")
st.text(f"Le chiffre d'affaires pour 2022 est de {ca_str}.")
