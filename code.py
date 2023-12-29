# Import python packages
import branca
import folium
import folium.plugins
import streamlit as st
import streamlit.components.v1 as components
from jinja2 import UndefinedError
from streamlit_folium import st_folium

m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker(
    [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)
