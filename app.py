import streamlit as st
from utils.data_loader import load_country_data
from utils.apriori_analysis import get_top_products, apriori_analysis

# Configurer la page
st.set_page_config(
    page_title="Analyse de Complémentarité",
    layout="wide"
)

# Initialisation des variables de session pour conserver l'état
if 'selected_product' not in st.session_state:
    st.session_state['selected_product'] = None
if 'complementary_results' not in st.session_state:
    st.session_state['complementary_results'] = None

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
        product_choice = st.selectbox("Choisissez un produit :", top_products, key="product_choice")

        # Conserver le produit sélectionné dans la session
        st.session_state['selected_product'] = product_choice

    # Vérifiez si un produit a été sélectionné
    if st.session_state['selected_product']:
        st.write(f"Produit sélectionné : {st.session_state['selected_product']}")

        if st.button("Analyser les produits complémentaires"):
            # Charger les données (de nouveau pour éviter les erreurs)
            data = load_country_data(country)

            # Effectuer l'analyse de complémentarité
            results = apriori_analysis(data, st.session_state['selected_product'])

            # Conserver les résultats dans la session
            st.session_state['complementary_results'] = results

    # Afficher les résultats si disponibles
    if st.session_state['complementary_results'] is not None:
        st.write("Produits complémentaires les plus probables :")
        st.dataframe(st.session_state['complementary_results'])
