import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
import markdown
from streamlit_folium import st_folium
from streamlit_extras.metric_cards import style_metric_cards
from mitosheet.streamlit.v1 import spreadsheet

#config du titre de la page
st.set_page_config("Suivi temporel des ventes :hourglass_flowing_sand:", page_icon="", layout="wide")

st.markdown(style, unsafe_allow_html = True)

css_code = """
<link rel="stylesheet" href="pages/style.css">
"""

#collecte des données
url = "Exemple - Hypermarché_Achats.csv"

#modif sur colonne Ventes
df = pd.read_csv(url, delimiter=";")
df['Ventes'] = df['Ventes'].str.replace('[^\d]', '', regex=True)
df['Ventes'] = pd.to_numeric(df['Ventes'], errors='coerce', downcast='integer')

#ajout d'une colonne année et une colonne mois qui extrait l'année de la date de commande
df['Année'] = pd.to_datetime(df['Date de commande'], format='%d/%m/%Y').dt.year
df['Mois'] = pd.to_datetime(df['Date de commande'], format='%d/%m/%Y').dt.month_name()

# Tri dans l'ordre des années
sorted_years = sorted(df['Année'].unique())
sorted_years_2 = sorted(df['Année'].unique())

# Création de colonnes
col_title, col_2, col_3 = st.columns([3, 1, 1])

# Une colonne pour le titre & une pour les listes déroulantes
with col_title:
    st.title("Suivi temporel des ventes :hourglass_flowing_sand:")

col_side1, col_side2 = st.columns(2)

with st.sidebar:
    st.header("Sélection des années")
    
    col_side1, col_side2 = st.columns(2)

    with col_side1:
        selected_year = st.selectbox("Sélectionnez N", sorted_years)
        
    with col_side2:
        # Vérifier si l'année sélectionnée dans la première liste déroulante est également dans la deuxième liste
        if selected_year in sorted_years_2:
            # Supprimer l'année sélectionnée de la deuxième liste déroulante
            sorted_years_2.remove(selected_year)
        
        # Exclure également l'année suivante à la première sélection dans la deuxième liste déroulante
        selected_comparison_year = st.selectbox("Sélectionnez N-*", [year for year in sorted_years_2 if year < selected_year])

    st.header("Filtre sur les mois")
    available_months = sorted(df['Mois'].unique())
    selected_months = st.multiselect("", available_months, default=available_months)
    filtered_df = df[df['Mois'].isin(selected_months)]

col_1, col_h1, col_2 = st.columns([1, 3, 1])

with col_h1:
    st.header("Données utilisées")
    new_dfs, code = spreadsheet(url)

#PARTIE KPI

col_1, col_h2, col_2 = st.columns([1, 3, 1])

with col_h2:
    st.header("Chiffres clés pour l'année courante :mag_right:")

#création de colonnes identiques
col_sp1, col_clients, col_sp2, col_orders, col_sp3, col_ca, col_sp4= st.columns([1, 1, 1, 1, 1, 1, 1])

#calculs
num_clients = df[df['Année'] == selected_year].drop_duplicates('ID client')['ID client'].count()
num_orders = len(df[df['Année'] == selected_year]['ID commande'])
ca_by_year = df[df['Année'] == selected_year]['Ventes'].sum()

#calculs des différences pour comparatif entre N et N-*
diff_clients = num_clients - df[df['Année'] == selected_comparison_year].drop_duplicates('ID client')['ID client'].count()
diff_orders = num_orders - len(df[df['Année'] == selected_comparison_year]['ID commande'])
diff_ca = ca_by_year - df[df['Année'] == selected_comparison_year]['Ventes'].sum()

#conversion des données pour conserver uniquement la partie entière
diff_clients = int(diff_clients)
diff_orders = int(diff_orders)
diff_ca = int(diff_ca)

#affiche le nombre de clients selon l'année
col_clients.metric(label="Nombre de clients", value=num_clients, delta=diff_clients)

#affiche le nombre de commandes selon l'année + comparatif avec N-*
col_orders.metric(label="Nombre de commandes", value=num_orders, delta=diff_orders)

#affiche le chiffre d'affaires selon l'année + comparatif avec N-*
col_ca.metric(label=f"Chiffre d'affaires", value=f"{int(ca_by_year)} €", delta=f"{int(diff_ca)} €")

style_metric_cards()



#PARTIE VISUALISATION

col_1, col_h3, col_2 = st.columns([1, 3, 1])

with col_h3:
    #titre
    st.header("Visualisations :bar_chart: :chart_with_upwards_trend:")


#création de colonnes et attribution de dimensions
col_v1, col_v2 = st.columns([2,2])

#graphique qui permet d'observer l'évolution du nombre de clients selon N et N-*

with col_v1:
    #agréger le nombre de clients par mois pour l'année sélectionnée
    monthly_clients_selected_year = df[df['Année'] == selected_year].drop_duplicates('ID client').groupby(
        'Mois')['ID client'].count().reset_index()

    #agréger le nombre de clients par mois pour l'année de comparaison
    monthly_clients_comparison_year = df[df['Année'] == selected_comparison_year].drop_duplicates(
        'ID client').groupby('Mois')['ID client'].count().reset_index()

    #affiche l'évolution du nombre de clients pour N
    fig_clients_evolution = go.Figure()
    fig_clients_evolution.add_trace(go.Scatter(
        x=monthly_clients_selected_year['Mois'],
        y=monthly_clients_selected_year['ID client'],
        mode='lines',
        name=f"{selected_year}",
        line=dict(color='#44566f')
    ))

    #affiche l'évolution du nombre de clients pour N-*
    fig_clients_evolution.add_trace(go.Scatter(
        x=monthly_clients_comparison_year['Mois'],
        y=monthly_clients_comparison_year['ID client'],
        mode='lines',
        name=f"{selected_comparison_year}",
        line=dict(color='#4678b9')
    ))

    #mise en forme
    fig_clients_evolution.update_layout(title=f"                                                                                                     Évolution du nombre de clients en {selected_year} et {selected_comparison_year}",
                                        xaxis=dict(title='Mois'),
                                        yaxis=dict(title='Nombre de clients'),
                                        height=600,
                                        width=800)
    
    #affichage
    st.plotly_chart(fig_clients_evolution, use_container_width=True)


#graphique qui permet d'observer l'évolution du nombre de clients selon N et N-*

fig_orders_evolution = go.Figure()

# Graphique qui permet d'observer l'évolution du nombre de commandes selon N et N-*
with col_v2:
    # Agréger le nombre de commandes par mois pour l'année sélectionnée
    monthly_orders_selected_year = df[df['Année'] == selected_year].groupby('Mois')['ID commande'].count().reset_index()

    # Agréger le nombre de commandes par mois pour l'année de comparaison
    monthly_orders_comparison_year = df[df['Année'] == selected_comparison_year].groupby(
        'Mois')['ID commande'].count().reset_index()

    # Triez les mois dans l'ordre décroissant du nombre de commandes
    monthly_orders_selected_year = monthly_orders_selected_year.sort_values(by='ID commande', ascending=True)
    monthly_orders_comparison_year = monthly_orders_comparison_year.sort_values(by='ID commande', ascending=True)

    # Affiche l'évolution du nombre de commandes pour N-*
    fig_orders_evolution.add_trace(go.Bar(
        x=monthly_orders_comparison_year['ID commande'],
        y=monthly_orders_comparison_year['Mois'],
        name=f"{selected_comparison_year}",
        orientation='h',
        marker=dict(color='#4678b9')
    ))
    
    # Affiche l'évolution du nombre de commandes pour N
    fig_orders_evolution.add_trace(go.Bar(
        x=monthly_orders_selected_year['ID commande'],
        y=monthly_orders_selected_year['Mois'],
        name=f"{selected_year}",
        orientation='h',
        marker=dict(color='#44566f')
    ))

    # Inversez l'ordre des traces dans la légende
    fig_orders_evolution.update_layout(legend=dict(traceorder='reversed'))

    # Mise en forme
    fig_orders_evolution.update_layout(barmode='group', title=f"                                                                                                     Évolution du nombre de commandes en {selected_year} et {selected_comparison_year}",
                                      xaxis=dict(title='Nombre de commandes'),
                                      yaxis=dict(title='Mois'),
                                      height=600,
                                      width=800)
    
    # Affichage
    st.plotly_chart(fig_orders_evolution, use_container_width=True)
    
