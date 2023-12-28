import streamlit as st
import folium

# Titre de l'application
st.title("Visualisation de point avec Folium dans Streamlit")

# Coordonnées du point à afficher
latitude = 39.949610
longitude = -75.150282

# Création de la carte Folium
m = folium.Map(location=[latitude, longitude], zoom_start=16)

# Ajout d'un marqueur sur la carte
folium.Marker([latitude, longitude], popup="Votre point").add_to(m)

# Affichage de la carte dans Streamlit
st.write(m)
