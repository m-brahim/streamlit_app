import streamlit as st
import pandas as pd
import fonctions as fts
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.title("Catégories de produit 📈 ")

df_achats = pd.read_csv("Exemple - Hypermarché_Achats.csv", sep=";")



# Appliquer la fonction à chaque colonne à convertir
col_to_convert_num = ['Profit', 'Prévision des ventes', 'Ventes']
for colonne in col_to_convert_num:
    df_achats[colonne] = fts.str_to_numeric(df_achats[colonne])


col_to_convert_date = ['Date d\'expédition', 'Date de commande']
for colonne in col_to_convert_date:
    df_achats[colonne] = fts.to_date(df_achats, colonne)


#Choix de l'année
lst_year = list(np.sort(df_achats["Date de commande"].dt.year.unique()))
selected_year = st.multiselect(" Choix années 🎰 ", lst_year, default=[max(lst_year)])


df_achats = df_achats[df_achats["Date de commande"].dt.year.isin(selected_year)]

#--------------------------------------------------ANALYSE GLOBALE----------------------------------------------------

st.markdown("## Ventes totales par catégorie de produits 📊")
ventes_par_categorie = fts.ventes_totales_par_categorie(df_achats,"Catégorie",'Ventes')
fts.bar_chart(ventes_par_categorie, 'Catégorie', 'Ventes')


#Liste catégorie
lst_categories = fts.get_lst_categorie(df_achats)

#Choix de la catégorie
selected_category = st.selectbox(" Choix catégorie 🎰 ", lst_categories)


# Filtrage de la DataFrame pour la catégorie sélectionnée
df_achats = df_achats[df_achats['Catégorie'] == selected_category]


st.markdown("## Premiers indicateurs ")
ventes = fts.get_kpis(selected_category, df_achats)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    label="Quantité vendue",
    value=f"{round(ventes[0]):,}".replace(',', ' ')
)

kpi2.metric(
    label="Previsions ventes ",
    value=f"{format(round(ventes[1]), ',').replace(',', ' ')} €"
)

kpi3.metric(
    label="Ventes réelles",
    value=f"{format(round(ventes[2]), ',').replace(',', ' ')} €",
    delta=f"{format (ventes[2] - ventes[1])} €"
)

kpi4.metric(
    label="Profit",
    value=f"{format(round(ventes[3]), ',').replace(',', ' ')} €"
)

st.markdown("## Ventes par catégorie de produits 📊")
# Calcul des ventes totales par sous-catégorie
ventes_sous_categorie = fts.ventes_totales_par_categorie(df_achats, 'Sous-catégorie', 'Ventes')
# Affichage du bar chart pour les sous-catégories de la catégorie sélectionnée
fts.bar_chart(ventes_sous_categorie, 'Sous-catégorie', 'Ventes')


col1, col2 = st.columns([1,2])

with col1:
    st.markdown("## Top 5 des produits les plus vendus AAAA")
    # Obtenir le top 5 des sous-catégories les plus vendues
    top_5_produits = df_achats.groupby('Nom du produit')['Ventes'].sum().nlargest(5)

    # Afficher le résultat
    st.write(top_5_produits)


with col2:
    st.markdown("## Top 5 des produits les plus rentables OOOO")