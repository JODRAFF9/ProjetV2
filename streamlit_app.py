#############################################   Parametrage
import streamlit as st
import pandas as pd
from pages.accueil import accueil
from pages.analyse import analyse
from pages.prediction import prediction
from pages.apropos import apropos
from funcs import load_data,map,style


# Configuration de la page Streamlit
st.set_page_config(page_title="Prédiction du BANK CHURN ",page_icon="docs/icon.png" , layout="wide")

# Chargement des données
train_df = load_data("data/cleaned data/train_df.csv")
train_df_labelled=train_df.drop(['id',"CustomerId","Surname"], axis=1)
map(train_df_labelled)

############################################ Pages
with st.sidebar:
    st.title("🏢 À propos de l'entreprise")
    st.markdown("""
    **Bank Analytics**  
    Spécialiste en analyse de données bancaires et en fidélisation client.  
    Notre objectif est de vous aider à **prédire le churn** et à optimiser la **rétention client** grâce à l'**intelligence artificielle**.
    
    📍 Basée à Dakar  
    📞 Contact : support@bankanalytics.com  
    """)


# Initialisation de l'état de la page (si ce n'est pas déjà fait)
if "page" not in st.session_state:
    st.session_state.page = "Accueil"
    
# Titre de l'application
st.title("🏡 **Application de Prédiction du BANK CHURN**")
style()


# Fonction pour changer la page active dans st.session_state
def set_page(page_name):
    st.session_state.page = page_name

# Barre de navigation horizontale avec des boutons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠 Accueil"):
        set_page("Accueil")
with col2:
    if st.button("📊 Analyse"):
        set_page("Analyse")
with col3:
    if st.button("🔍 Prédiction"):
        set_page("Prédiction")
with col4:
    if st.button("ℹ️ A-propos"):
        set_page("A-propos")

# Section Accueil
if st.session_state.page == "Accueil":
    accueil()

# Section Analyse
if st.session_state.page == "Analyse":
    analyse(train_df_labelled)
    
# Section Prédiction  
if st.session_state.page == "Prédiction":
    prediction(train_df_labelled)
    
# Section A-propos
if st.session_state.page == "A-propos":
    apropos()