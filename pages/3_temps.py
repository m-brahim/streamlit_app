import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
import markdown
from streamlit_folium import st_folium

#config du titre de la page
st.set_page_config("Suivi temporel des ventes :hourglass_flowing_sand:", page_icon="", layout="wide")

#style de la page

style = """
<style>

[data-testid="stHeader"]{
background-image: url("https://th.bing.com/th/id/OIP.9c2dn34dgf4XNAfwfq7dyAHaEK?rs=1&pid=ImgDetMain");
background-size: cover;
}

[class="main st-emotion-cache-uf99v8 ea3mdgi3"] {
background-image: url("https://www.nsbpictures.com/wp-content/uploads/2020/08/COLORFULL-GRADIENTS-6-scaled.jpg");
background-size: cover;
}



[class="st-emotion-cache-fplge5 e1f1d6gn3"]{
border : solid;
border-color : white;
}

[class="st-emotion-cache-j5r0tf e1f1d6gn3"]{
border : solid;
border-color : white;
}

[class="st-emotion-cache-j5r0tf e1f1d6gn3"]{
border : solid;
border-color : white;
}

[class="st-emotion-cache-10trblm e1nzilvr1"]{
text-align : center;
margin-top : 10px;
}

[class="st-emotion-cache-zt5igj e1nzilvr4"]{
border : solid;
border-color : white;
}

</style>
"""

st.markdown(style, unsafe_allow_html = True)

#collecte des données
url = "Exemple - Hypermarché_Achats.csv"

#modif sur colonne Ventes
df = pd.read_csv(url, delimiter=";")
df['Ventes'] = df['Ventes'].str.replace('[^\d]', '', regex=True)
df['Ventes'] = pd.to_numeric(df['Ventes'], errors='coerce', downcast='integer')

#ajout d'une colonne année et une colonne mois qui extrait l'année de la date de commande
df['Année'] = pd.to_datetime(df['Date de commande'], format='%d/%m/%Y').dt.year
df['Mois'] = pd.to_datetime(df['Date de commande'], format='%d/%m/%Y').dt.month_name()

#tri dans l'ordre des années
sorted_years = sorted(df['Année'].unique())

#création de colonnes
col_title, col_dropdown, col_dropdown2 = st.columns([3, 1, 1])  # Ajustez les proportions en conséquence

#une colonne pour le titre & une pour les listes déroulantes
with col_title:
    st.title("Suivi temporel des ventes :hourglass_flowing_sand:")

with col_dropdown:
    selected_year = st.selectbox("Sélectionnez une année", sorted_years)

with col_dropdown2:
    selected_comparison_year = st.selectbox("Sélectionnez une année de comparaison", sorted_years)



#PARTIE KPI

#titre 
st.header("Indicateurs :mag_right:")

#espacement
st.subheader("")

#création de colonnes identiques
col_clients, col_orders, col_ca = st.columns(3)

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
col_ca.metric(label=f"Chiffre d'affaires pour {selected_year}", value=f"{int(ca_by_year)} €", delta=f"{int(diff_ca)} €")

#espacement
st.subheader("")



#PARTIE VISUALISATION

#titre
st.header("Visualisations :bar_chart: :chart_with_upwards_trend:")

#espacement
st.subheader("")

#création de colonnes et attribution de dimensions
col_v1, col_v2, col_v3 = st.columns([2,1,2])

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
        line=dict(color='blue')
    ))

    #affiche l'évolution du nombre de clients pour N-*
    fig_clients_evolution.add_trace(go.Scatter(
        x=monthly_clients_comparison_year['Mois'],
        y=monthly_clients_comparison_year['ID client'],
        mode='lines',
        name=f"{selected_comparison_year}",
        line=dict(color='red')
    ))

    #mise en forme
    fig_clients_evolution.update_layout(title=f"Évolution du nombre de clients en {selected_year} et {selected_comparison_year}",
                                        xaxis=dict(title='Mois'),
                                        yaxis=dict(title='Nombre de clients'))
    
    #affichage
    st.plotly_chart(fig_clients_evolution, use_container_width=True)


#graphique qui permet d'observer l'évolution du nombre de clients selon N et N-*

fig_orders_evolution = go.Figure()

# Graphique qui permet d'observer l'évolution du nombre de commandes selon N et N-*
with col_v3:
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
        marker=dict(color='red')
    ))
    
    # Affiche l'évolution du nombre de commandes pour N
    fig_orders_evolution.add_trace(go.Bar(
        x=monthly_orders_selected_year['ID commande'],
        y=monthly_orders_selected_year['Mois'],
        name=f"{selected_year}",
        orientation='h',
        marker=dict(color='blue')
    ))

    # Inversez l'ordre des traces dans la légende
    fig_orders_evolution.update_layout(legend=dict(traceorder='reversed'))

    # Mise en forme
    fig_orders_evolution.update_layout(barmode='group', title=f"Évolution du nombre de commandes en {selected_year} et {selected_comparison_year}",
                                      xaxis=dict(title='Nombre de commandes'),
                                      yaxis=dict(title='Mois'),
                                      height=600,
                                      width=800)

    # Affichage
    st.plotly_chart(fig_orders_evolution, use_container_width=True)

