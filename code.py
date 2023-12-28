import folium
import streamlit as st
from streamlit_folium import st_folium

dot = (39.949610, -75.150282)
m = folium.Map(location=dot, zoom_start=16)
folium.Marker(location, popup="Liberty Bell", tooltip="Liberty Bell").add_to(m)
st_folium(m, width=725)
