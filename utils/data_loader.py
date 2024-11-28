import pandas as pd
import streamlit as st

# Dictionnaire des URL
COUNTRY_FILES = {
    'FR': 'https://drive.google.com/uc?id=1sv6E1UsMV3fe-T_3p94uAUt1kz4xlXZA',
    'Belgium': 'https://drive.google.com/uc?id=1fqu_YgsovkDrpqV7OsFStusEvM-9axRg',
    'UK': 'https://drive.google.com/uc?id=1ROT0ide8EQfgcWpXMY6Qnyp5nMKoLt-a',
    'US': 'https://drive.google.com/uc?id=1HsxBxGpq3lSwJKPALDsDNvJXNi6us2j-'
}

@st.cache_data
def load_country_data(country):
    """Charge et met en cache les données d'un pays."""
    url = COUNTRY_FILES[country]
    data = pd.read_excel(url)
    return data
