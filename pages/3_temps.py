import streamlit as st
import pandas as pd
import plotly.express as px

url = "Exemple - Hypermarché_Achats.csv"

df = pd.read_csv(url, delimiter=";")
df['Ventes'] = df['Ventes'].str.replace('[^\d]', '', regex=True)
df['Ventes'] = pd.to_numeric(df['Ventes'], errors='coerce', downcast='integer')

# Ajouter une colonne pour l'année à partir de la colonne de dates de commande
df['Année'] = pd.to_datetime(df['Date de commande'], format='%d/%m/%Y').dt.year

# Ajouter une colonne pour le mois à partir de la colonne de dates de commande
df['Mois'] = pd.to_datetime(df['Date de commande'], format='%d/%m/%Y').dt.month_name()

# Obtenir les années triées
sorted_years = sorted(df['Année'].unique())

# Titre de la page
st.set_page_config("Suivi temporel des ventes", page_icon="", layout="wide")

# Colonne pour le titre à l'extrême droite
col_title, col_dropdown = st.columns([3, 1])  # Ajustez les proportions en conséquence

with col_title:
    st.subheader("Suivi temporel des ventes")

# Liste déroulante à côté du titre
with col_dropdown:
    selected_year = st.selectbox("Sélectionnez une année", sorted_years)
    selected_comparison_year = st.selectbox("Sélectionnez une année de comparaison", sorted_years)

st.subheader("Indicateurs")

st.subheader("")

# Créer trois colonnes pour aligner les widgets côte à côte
col_clients, col_orders, col_ca = st.columns(3)

num_clients = df[df['Année'] == selected_year].drop_duplicates('ID client')['ID client'].count()
num_orders = len(df[df['Année'] == selected_year]['ID commande'])
ca_by_year = df[df['Année'] == selected_year]['Ventes'].sum()

# Calcul des différences pour les indicateurs
diff_clients = num_clients - df[df['Année'] == selected_comparison_year].drop_duplicates('ID client')['ID client'].count()
diff_orders = num_orders - len(df[df['Année'] == selected_comparison_year]['ID commande'])
diff_ca = ca_by_year - df[df['Année'] == selected_comparison_year]['Ventes'].sum()

# Nombre de clients
col_clients.metric(label="Nombre de clients", value=num_clients, delta=diff_clients)

# Nombre de commandes pour l'année sélectionnée
col_orders.metric(label="Nombre de commandes", value=num_orders, delta=diff_orders)

# Chiffre d'affaires pour l'année sélectionnée
col_ca.metric(label=f"Chiffre d'affaires pour {selected_year}", value=f"{int(ca_by_year)} €", delta=f"{int(diff_ca)} €")

st.subheader("")

st.subheader("Visualisations")

st.subheader("")

# Créer 2 colonnes pour aligner les widgets côte à côte
col_v1, col_v2, col_v3 = st.columns([2, 1, 2])

with col_v1:
    # Agréger le nombre de clients par mois pour l'année sélectionnée
    monthly_clients_selected_year = df[df['Année'] == selected_year].drop_duplicates('ID client').groupby('Mois')['ID client'].count().reset_index()

    # Agréger le nombre de clients par mois pour l'année de comparaison
    monthly_clients_comparison_year = df[df['Année'] == selected_comparison_year].drop_duplicates('ID client').groupby('Mois')['ID client'].count().reset_index()

    # Utiliser la variable num_clients avec drop_duplicates pour construire le graphique en ligne
    fig_clients_evolution = px.line(
        monthly_clients_selected_year,
        x='Mois',
        y='ID client',
        title=f"Évolution du nombre de clients en {selected_year} et {selected_comparison_year}",
        labels={'ID client': 'Nombre de clients', 'Mois': 'Mois'}
    )

    # Ajouter la deuxième série temporelle pour l'année de comparaison
    fig_clients_evolution.add_trace(px.line(
        monthly_clients_comparison_year,
        x='Mois',
        y='ID client',
        labels={'ID client': 'Nombre de clients', 'Mois': 'Mois'}
    ).data[0])

    st.plotly_chart(fig_clients_evolution, use_container_width) 

with col_v3:
    # Agréger le nombre de commandes par mois pour l'année sélectionnée
    monthly_orders = df[df['Année'] == selected_year].groupby('Mois')['ID commande'].count().reset_index()

    # Visualisation de l'évolution du nombre de commandes par mois
    fig_orders_evolution = px.bar(
        monthly_orders,
        x='Mois',
        y='ID commande',
        title=f"Évolution du nombre de commandes en {selected_year}",
        labels={'ID commande': 'Nombre de commandes', 'Mois': 'Mois'}
    )

    st.plotly_chart(fig_orders_evolution, use_container_width=True)
