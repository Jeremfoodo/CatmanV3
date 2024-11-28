import streamlit as st
from utils.data_loader import load_country_data
from utils.apriori_analysis import get_top_products, apriori_analysis

# Configurer la page
st.set_page_config(
    page_title="Analyse de Complémentarité",
    layout="wide"
)

# Page de démarrage
st.title("Application d'Analyse")
option = st.selectbox(
    "Que voulez-vous faire ?",
    ["Choisir une option", "Analyse de segmentation", "Analyse de complémentarité"]
)

if option == "Analyse de complémentarité":
    st.header("Analyse de Complémentarité")

    # Entrée de l'utilisateur
    country = st.selectbox("Choisissez un pays :", ["FR", "Belgium", "UK", "US"])
    category = st.text_input("Entrez une catégorie de produit (optionnel) :")

    if st.button("Afficher les 30 produits les plus achetés"):
        # Charger les données
        data = load_country_data(country)

        # Filtrer par catégorie si renseignée
        if category:
            data = data[data['Product Category'].str.contains(category, na=False)]

        # Obtenir le top 30 des produits
        top_products = get_top_products(data)
        product_choice = st.selectbox("Choisissez un produit :", top_products)

        if st.button("Analyser les produits complémentaires"):
            results = apriori_analysis(data, product_choice)
            st.write("Produits complémentaires les plus probables :")
            st.dataframe(results)

