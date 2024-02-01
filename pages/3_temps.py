import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
import markdown
from streamlit_folium import st_folium
from streamlit_extras.metric_cards import style_metric_cards
from mitosheet.streamlit.v1 import spreadsheet
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#config du titre de la page
st.set_page_config("Suivi des ventes de la société", page_icon="", layout="wide")

#collecte des données
url = "Exemple - Hypermarché_Achats.csv"

#charger le fichier CSS
with open("pages/style.css") as f:
    css_code = f.read()

st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)

#modif sur colonne Ventes
df = pd.read_csv(url, delimiter=";")
df['Ventes'] = df['Ventes'].str.replace('[^\d]', '', regex=True)
df['Ventes'] = pd.to_numeric(df['Ventes'], errors='coerce', downcast='integer')

#ajout d'une colonne année et une colonne mois qui extrait l'année de la date de commande
df['Année'] = pd.to_datetime(df['Date de commande'], format='%d/%m/%Y').dt.year
df['Mois'] = pd.to_datetime(df['Date de commande'], format='%d/%m/%Y').dt.month_name()

df = df.sort_values(by=['Année', 'Mois'])

df = df.reset_index(drop=True)

#tri dans l'ordre des années
sorted_years = sorted(df['Année'].unique())
sorted_years_2 = sorted(df['Année'].unique())

#création de colonnes
col_1, col_title, col_2 = st.columns([1, 2, 1])

#une colonne pour le titre & une pour les listes déroulantes
with col_title:
    st.title("Suivi des ventes de la société")

with st.sidebar:
    st.header("Paramètres des graphiques")
    graph_height = st.slider("Hauteur des graphiques", min_value=300, max_value=1200, value=500)


#PARTIE Vis'

#1) analyse client

col_h1, col2, col3 = st.columns([1,1,1])

with col_h1:
    st.header("1. Analyse client")


# tableau

# Collecte des données
df_table = pd.read_csv(url, delimiter=";").reset_index(drop=True)

# Créer des colonnes pour les listes déroulantes
col_space, col_country, col_space, col_category, col_space, col_client, col_space = st.columns([0.5, 1, 0.5, 1, 0.5, 1, 0.5])

# Liste déroulante pour le pays
with col_country:
    selected_country = st.selectbox('Sélectionnez le pays', df_table['Pays/Région'].unique(), index=None, placeholder="Choisir un pays",)

# Liste déroulante pour la catégorie
with col_category:
    selected_category = st.selectbox('Sélectionnez la catégorie', df_table['Catégorie'].unique(), index=None, placeholder="Choisir une catégorie",)

# Liste déroulante pour le client
with col_client:
    selected_client = st.selectbox('Sélectionnez le client', df_table['Nom du client'].unique(), index=None, placeholder="Choisir un client",)

# Sélectionner les colonnes à afficher dans le DataFrame
selected_columns_table = ['Catégorie', 'Date de commande', 'ID client', 'Nom du client', 'Nom du produit', 'Pays/Région', 'Segment', 'Statut des expéditions', 'Ville', 'Quantité', 'Remise', 'Ventes']

# Appliquer les filtres
df_filtre = df_table[(df_table['Pays/Région'] == selected_country) & (df_table['Catégorie'] == selected_category) & (df_table['Nom du client'] == selected_client)]

df_filtre.reset_index(drop=True, inplace=True)

# Définir une variable pour vérifier si les listes déroulantes ont été sélectionnées
selection_effectuee = False

# Condition pour vérifier si les éléments nécessaires sont sélectionnés
if selected_country is not None and selected_category is not None and selected_client is not None:
    selection_effectuee = True

# Condition pour afficher le tableau uniquement si la sélection a été effectuée
if selection_effectuee:
    # Assurez-vous que la colonne 'Ventes' contient uniquement des chaînes de caractères
    df_filtre['Ventes'] = df_filtre['Ventes'].astype(str)

    # Appliquer la modification sur la colonne 'Ventes'
    df_filtre['Ventes'] = df_filtre['Ventes'].str.replace('[^\d]', '', regex=True)

    # Convertir la colonne 'Ventes' en type numérique
    df_filtre['Ventes'] = pd.to_numeric(df_filtre['Ventes'], errors='coerce', downcast='integer')

    # Trouver l'indice de la cellule avec la vente la plus élevée
    max_sales_index = df_filtre['Ventes'].idxmax()

    # Créer une copie du DataFrame pour ajouter des styles
    styled_df = df_filtre[selected_columns_table].style.apply(lambda row: ['background: green' if row.name == max_sales_index else '' for _ in row], axis=1)

    # Afficher le tableau avec les styles
    st.table(styled_df)

    # Afficher un graphique (vous pouvez ajuster le style selon vos préférences)
    fig = go.Figure(data=[go.Table(
        columnorder=list(range(len(selected_columns_table))),
        columnwidth=[120, 120, 80, 180, 180, 100, 80, 120, 100, 80, 80, 100],
        header=dict(
            values=selected_columns_table,
            font=dict(size=14, color='white'),
            fill_color='#264653',
            line_color='rgba(255,255,255,0.2)',
            align=['center'],
            height=30
        ),
        cells=dict(
            values=[df_filtre[K].tolist() for K in selected_columns_table],
            font=dict(size=12),
            align=['center'],
            line_color='rgba(255,255,255,0.2)',
            height=30))
    ])

    fig.update_layout(title_text="Current Table Title", title_font_color='#264653', title_x=0,
                      margin=dict(l=0, r=10, b=10, t=30), height=480)

    st.plotly_chart(fig, use_container_width=True)




#2) analyse temporelle

col_h2, col_2, col_3 = st.columns([1, 1, 1])

with col_h2:
    st.header("2. Analyses temporelles")

#création de colonnes et attribution de dimensions
col_dd1, col_sp1, cold_dd2, col_sp2, col_mlt = st.columns([0.5,0.5,0.5,0.5,2])

with col_dd1:
    selected_year = st.selectbox("Sélectionnez N", sorted_years, index=3, placeholder="Choisir N")

with cold_dd2:
    if selected_year in sorted_years_2:
        sorted_years_2.remove(selected_year)
        selected_comparison_year = st.selectbox("Sélectionnez N-*", [year for year in sorted_years_2 if year < selected_year])

with col_mlt:
    available_months = sorted(df['Mois'].unique())
    selected_months = st.multiselect("", available_months, default=available_months)
    filtered_df = df[df['Mois'].isin(selected_months)]

#création de colonnes identiques
col_txt, col_sp1, col_clients, col_sp2, col_orders, col_sp3, col_ca, col_sp4= st.columns([1.5, 0.5, 1.25, 0.5, 1.25, 0.5, 1.25, 0.5])

with col_txt:
    st.write("*Chiffres clés N vs N-* * :")

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

#graphique qui permet d'observer l'évolution du nombre de clients selon N et N-*

col_txt, col_v1, col_space, col_v2 = st.columns([1,2,0.5,2])

with col_txt:
    st.write("*Graphiques* :")

with col_v1:
    # Agréger le nombre de clients par mois pour l'année sélectionnée
    monthly_clients_selected_year = filtered_df[filtered_df['Année'] == selected_year].drop_duplicates('ID client').groupby(
    'Mois')['ID client'].count().reset_index()

    # Tri des mois dans l'ordre
    sorted_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    monthly_clients_selected_year['Mois'] = pd.Categorical(monthly_clients_selected_year['Mois'], categories=sorted_months, ordered=True)
    monthly_clients_selected_year = monthly_clients_selected_year.sort_values('Mois')

    # Agréger le nombre de clients par mois pour l'année de comparaison
    monthly_clients_comparison_year = filtered_df[filtered_df['Année'] == selected_comparison_year].drop_duplicates(
    'ID client').groupby('Mois')['ID client'].count().reset_index()

    # Tri des mois dans l'ordre
    monthly_clients_comparison_year['Mois'] = pd.Categorical(monthly_clients_comparison_year['Mois'], categories=sorted_months, ordered=True)
    monthly_clients_comparison_year = monthly_clients_comparison_year.sort_values('Mois')

    # Affiche l'évolution du nombre de clients pour N
    fig_clients_evolution = go.Figure()
    fig_clients_evolution.add_trace(go.Scatter(
        x=monthly_clients_selected_year['Mois'],
        y=monthly_clients_selected_year['ID client'],
        mode='lines',
        name=f"{selected_year}",
        line=dict(color='#fcc200')
    ))
     
    # Affiche l'évolution du nombre de clients pour N-*
    fig_clients_evolution.add_trace(go.Scatter(
        x=monthly_clients_comparison_year['Mois'],
        y=monthly_clients_comparison_year['ID client'],
        mode='lines',
        name=f"{selected_comparison_year}",
        line=dict(color='#9b870c')
    ))

    target_value = 80
    fig_clients_evolution.add_shape(
        go.layout.Shape(
            type="line",
            x0=monthly_clients_selected_year['Mois'].min(),
            x1=monthly_clients_selected_year['Mois'].max(),
            y0=target_value,
            y1=target_value,
            line=dict(color="black", width=2, dash="dash"),
        )
    )
    
    # Mise en forme
    fig_clients_evolution.update_layout(title=f"Évolution du nombre de clients en {selected_year} et {selected_comparison_year}",
                                       xaxis=dict(title='Mois', tickfont=dict(size=12), title_font=dict(size=12)),
                                       yaxis=dict(title='Nombre de clients', tickfont=dict(size=12), title_font=dict(size=12)),
                                       title_font=dict(size=15),
                                       title_x = 0.2,
                                       height=graph_height,
                                       width=500)
    
    # Affichage
    st.plotly_chart(fig_clients_evolution, use_container_width=True)


#graphique qui permet d'observer l'évolution du nombre de clients selon N et N-*

fig_orders_evolution = go.Figure()

# Graphique qui permet d'observer l'évolution du nombre de commandes selon N et N-*

with col_v2:
    # Agréger le nombre de commandes par mois pour l'année sélectionnée
    monthly_orders_selected_year = filtered_df[filtered_df['Année'] == selected_year].groupby('Mois')['ID commande'].count().reset_index()

    # Tri des mois dans l'ordre croissant
    monthly_orders_selected_year['Mois'] = pd.Categorical(monthly_orders_selected_year['Mois'], categories=sorted_months, ordered=True)
    monthly_orders_selected_year = monthly_orders_selected_year.sort_values('Mois')

    # Agréger le nombre de commandes par mois pour l'année de comparaison
    monthly_orders_comparison_year = filtered_df[filtered_df['Année'] == selected_comparison_year].groupby('Mois')['ID commande'].count().reset_index()

    # Tri des mois dans l'ordre croissant
    monthly_orders_comparison_year['Mois'] = pd.Categorical(monthly_orders_comparison_year['Mois'], categories=sorted_months, ordered=True)
    monthly_orders_comparison_year = monthly_orders_comparison_year.sort_values('Mois')
    
    # Ajustez la taille des barres ici
    bar_width = 0.3

    # Affiche l'évolution du nombre de commandes pour N-*
    fig_orders_evolution.add_trace(go.Bar(
        x=monthly_orders_comparison_year['Mois'],
        y=monthly_orders_comparison_year['ID commande'],
        name=f"{selected_comparison_year}",
        text=monthly_orders_comparison_year['ID commande'],
        textposition='outside',
        marker=dict(color='#f7e98e', line=dict(width=2, color='black')),
        width=bar_width,
    ))

    # Affiche l'évolution du nombre de commandes pour N
    fig_orders_evolution.add_trace(go.Bar(
        x=monthly_orders_selected_year['Mois'],
        y=monthly_orders_selected_year['ID commande'],
        name=f"{selected_year}",
        text=monthly_orders_selected_year['ID commande'],
        textposition='outside',
        marker=dict(color='#fcc200', line=dict(width=2, color='black')),
        width=bar_width,
    ))

    target_value = 150  # Remplacez cela par la valeur cible souhaitée
    fig_orders_evolution.add_shape(
        go.layout.Shape(
            type="line",
            x0=monthly_orders_comparison_year['Mois'].min(),
            x1=monthly_orders_comparison_year['Mois'].max(),
            y0=target_value,
            y1=target_value,
            line=dict(color="black", width=2, dash="dash"),
        )
    )

    # Mise à jour de la mise en forme
    fig_orders_evolution.update_layout(barmode='group', title=f"Évolution du nombre de commandes en {selected_year} et {selected_comparison_year}",
                                       xaxis=dict(title='Nombre de commandes', tickfont=dict(size=12), title_font=dict(size=12)),
                                       yaxis=dict(title='Mois', tickfont=dict(size=12), title_font=dict(size=12)),
                                       title_font=dict(size=15),
                                       title_x=0.2,
                                       height=graph_height,
                                       width=500)

    # Affichage
    st.plotly_chart(fig_orders_evolution, use_container_width=True)

   









col_h3, col2, col3 = st.columns([1,1,1])

with col_h3:
    st.header("3. Analyses géographiques")


col_country, col_space = st.columns([0.5, 1])

# Liste déroulante pour le pays
with col_country:
    selected_pays = st.selectbox('Sélectionnez le pays', df['Pays/Région'].unique(), index=None, placeholder=" ")

selection = False

if selected_pays is not None:
    selection = True

data_f = df[df['Pays/Région'] == selected_pays]

# Colonne pour le classement par pays des 5 produits les plus achetés
col_map, col_sp, col_class = st.columns([2, 0.5, 2])

with col_class:
    if selection:
        # Grouper par produit et calculer la quantité totale achetée
        top_products = data_f.groupby('Nom du produit')['Quantité'].sum().reset_index()

        # Trier par quantité croissante et sélectionner les 5 premiers produits
        top_products = top_products.sort_values(by='Quantité', ascending=True).tail(5)

        target_value = data_f['Quantité'].mean()
        
        colors = ['#faf1b7', '#f7e888', '#ffdd1a', '#ffd54d', '#fcc200']

        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=top_products['Nom du produit'],
            x=top_products['Quantité'],
            orientation='h',
            marker=dict(color=colors),
            text=top_products['Quantité'],
            textposition='outside',
        ))

        fig.add_shape(
            go.layout.Shape(
                type='line',
                x0=target_value,
                x1=target_value,
                y0=0,
                y1=len(top_products),
                line=dict(color='black', dash='dash', width=2),
            )
        )

        fig.update_layout(
            title='Classement des 5 produits les plus achetés',
            yaxis=dict(title='Produit', tickfont=dict(size=12)),
            xaxis=dict(title='Quantité achetée', tickfont=dict(size=12)),
            title_x=0.25,
            title_font=dict(size=15),
            height=400,
            width=800,
        )
        
        st.plotly_chart(fig, use_container_width=True)

# agréger le nombre de clients par pays
clients_by_country = df.drop_duplicates(subset=['ID client', 'Pays/Région']).groupby('Pays/Région')['ID client'].count().reset_index()

# fusionner les données agrégées avec les données filtrées
merged_data = pd.merge(data_f, clients_by_country, how='left', on='Pays/Région')

# icône personnalisée pour représenter un client (ici l'exemple c'est Kiloutou)
icon_path = 'pages/Kiloutou_logo.jpg'
client_icon = folium.CustomIcon(icon_image=icon_path, icon_size=(30, 30))

# affiche une carte qui indique le nombre de clients par pays
with col_map:
    if selection:
        # définition d'une localisation initiale
        my_map = folium.Map(location=[merged_data['Latitude'].iloc[0], merged_data['Longitude'].iloc[0]], zoom_start=6)

        # ajoutez un seul marqueur pour représenter le pays avec le nombre de clients dans l'infobulle
        folium.Marker([merged_data['Latitude'].iloc[0], merged_data['Longitude'].iloc[0]],
                      popup=f"Nombre de clients: {num_clients}",
                      icon=client_icon).add_to(my_map)

        st_folium(my_map, width=1000, height=400)


with col_class :
    quantity_by_category = data_f.groupby('Catégorie')['Quantité'].sum().reset_index()
        
    colors = ['#fcc200', '#ffe033', '#f7e98e']
    fig = px.pie(quantity_by_category, values='Quantité', names='Catégorie',
                 color_discrete_sequence=colors)
        
    fig.update_traces(marker=dict(line=dict(color='#FFFFFF', width=2)))
    
    fig.update_layout(title='Quantités vendues par catégorie',
                      title_x=0.25,
                      title_font=dict(size=15),
                      height=350,
                      width=800)
    
    if selection :
        st.plotly_chart(fig, use_container_width=True)








#col_1, col_csv, col_2 = st.columns([1,2,1])

#with col_csv :
#        new_dfs, code = spreadsheet(url)
