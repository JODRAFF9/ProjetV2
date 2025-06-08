#############################################   Parametrage
import streamlit as st
import pandas as pd

# je nomme le dossier de mes pages par branch au lieu de "pages" qui est un mot clé dans streamlit détectant les pages et génère automatiquement le sidebar
from branch.accueil import accueil
from branch.analyse import analyse
from branch.prediction import prediction
from branch.apropos import apropos
from funcs import load_data, map, style

# Configuration de la page Streamlit
st.set_page_config(page_title="Prédiction du BANK CHURN ",page_icon="docs/icon.png" , layout="wide")

# Chargement des données
train_df = load_data("data/cleaned data/train_df.csv")
train_df_labelled=train_df.drop(['id',"CustomerId","Surname"], axis=1)
map(train_df_labelled)
##################################################################

# Sidebar personnalisée
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: black; /* Bleu clair */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Contenu de la sidebar
with st.sidebar:
    st.image("docs/icon.png", width=350)
    st.markdown("""
    ### À propos de l'entreprise
    
    Bienvenue dans notre application de prédiction du churn bancaire.
    
    Cette solution vise à analyser les comportements des clients et prédire les départs potentiels pour améliorer la fidélisation.
    """)
    
#############################################################################
# Initialisation de l'état de la page (si ce n'est pas déjà fait)
if "pag" not in st.session_state:
    st.session_state.pag = "Accueil"
    
# Titre de l'application
st.title("🏡 **Application de Prédiction du BANK CHURN**")
style()


# Fonction pour changer la page active dans st.session_state
def set_page(page_name):
    st.session_state.pag = page_name

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
if st.session_state.pag == "Accueil":
    accueil()

# Section Analyse
if st.session_state.pag == "Analyse":
    analyse(train_df_labelled)
    
# Section Prédiction  
if st.session_state.pag == "Prédiction":
    prediction(train_df_labelled)
    
# Section A-propos
if st.session_state.pag == "A-propos":
    apropos()