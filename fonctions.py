import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def str_to_numeric(colonne):
    # Remplacer les symboles '€' et convertir en entier
    return pd.to_numeric(colonne.str.replace('[^\d-]', '', regex=True), errors='coerce')


def to_date(df,colonne):
    return pd.to_datetime(df[colonne])


def get_lst_categorie(df):
    categories_uniques = df['Catégorie'].unique()
    list_categories = list(categories_uniques)
    return list_categories

def get_kpis(categorie, df):

    categorie_df = df[df['Catégorie'] == categorie]
    #print(categorie_df)
    quantite_totale = categorie_df['Quantité'].sum()
    ventes = categorie_df['Ventes'].sum()
    prev_ventes = categorie_df['Prévision des ventes'].sum()
    profit = categorie_df['Profit'].sum()
    return [quantite_totale, prev_ventes, ventes, profit]

def get_CA_genere(categorie,df):
    pass

def ventes_totales_par_categorie(dataframe,group_by_col,ventes_col):

    ventes_par_categorie = dataframe.groupby(group_by_col)[ventes_col].sum().reset_index()
    return ventes_par_categorie


def bar_chart(df, x_label, y_label):
    fig = px.bar(df, x=x_label, y=y_label)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


