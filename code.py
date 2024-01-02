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
    "Aldi": "https://github.com/m-brahim/streamlit_app/blob/65c6285b6652a3294fb2e395de2a2d31e4bacae7/.logo/Aldi_logo.png",
    "Intermarché": "https://github.com/m-brahim/streamlit_app/blob/65c6285b6652a3294fb2e395de2a2d31e4bacae7/.logo/Intermarche_logo.png",
    "Carrefour": "https://github.com/m-brahim/streamlit_app/blob/36be0bf7d0730efdd5ddbe320c5f9eeccfd79fd2/.logo/Lidl_logo.png",
}

# En-tête de la page
st.title("Tableau de bords Streamlit")

# Sélection du commerce
selected_commerce = st.sidebar.selectbox("Sélectionnez un commerce", df["Entreprise"])

# Filtrer les données en fonction du commerce sélectionné
filtered_data = df[df["Entreprise"] == selected_commerce]

# Récupérer le chemin du logo en fonction du commerce sélectionné
logo_path = logo_paths.get(selected_commerce, "Chemin par défaut si le logo n'est pas trouvé")

# Afficher les métriques dans trois colonnes
col1, col2, col3 = st.columns(3)

# Métrique 1 - Entreprise avec logo
col1.image(logo_path, width=100, caption=selected_commerce, use_container_width=False)

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
