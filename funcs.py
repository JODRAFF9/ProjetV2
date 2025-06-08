import streamlit as st
import pandas as pd
import dill

# Fonction pour charger les données (mise en cache)
@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Le fichier {file_path} est introuvable.")
        return pd.DataFrame()


@st.cache_resource
def load_model():
    with open("code/saved_models/rl_model.pkl", "rb") as f:
        return dill.load(f)

def map(data):
    """Mappe les valeurs binaires 0/1 vers 'No'/'Yes'."""
    binary_mapping = {0: 'No', 1: 'Yes'}
    binary_cols = ['HasCrCard', 'IsActiveMember', 'Exited']
    for col in binary_cols:
        if col in data.columns:
            data[col] = data[col].map(binary_mapping)
    return data

def unmap(data):
    """Remappe les valeurs 'No'/'Yes' vers 0/1 pour la prédiction."""
    binary_mapping = {'No':0., 'Yes':1.}
    binary_cols = ['HasCrCard', 'IsActiveMember']
    for col in binary_cols:
        if col in data.columns:
            data[col] = data[col].map(binary_mapping)
    return data


def nom_variable(nom, mode='vers_descriptif'):
    """
    Convertit entre noms techniques et noms descriptifs de variables.

    Args:
        nom (str): Nom à convertir (technique ou descriptif)
        mode (str): Direction de conversion
            'vers_descriptif' : convertit nom technique → descriptif
            'vers_technique' : convertit nom descriptif → technique

    Returns:
        str: Nom converti
    """
    correspondance = {
        # Format: 'nom_technique': 'nom descriptif'
        'id': "l'identifiant unique",
        'CustomerId': "l'identifiant du client",
        'Surname': 'le nom du client',
        'CreditScore': "le score de crédit",
        'Geography': 'le pays de résidence',
        'Gender': 'le genre du client',
        'Age': "l'âge du client",
        'Tenure': 'la durée de relation client',
        'Balance': 'le solde du compte',
        'NumOfProducts': 'le nombre de produits souscrits',
        'HasCrCard': "la possession d'une carte crédit",
        'IsActiveMember': "le statut de membre actif",
        'EstimatedSalary': "le revenu annuel estimé",
        'Exited': "l'indicateur d'attrition"
    }

    # Création du dictionnaire inverse pour la conversion dans l'autre sens
    correspondance_inverse = {v: k for k, v in correspondance.items()}

    if mode == 'vers_descriptif':
        # Conversion nom technique → descriptif
        return correspondance.get(nom, nom)
    elif mode == 'vers_technique':
        # Conversion nom descriptif → technique
        return correspondance_inverse.get(nom, nom)
    else:
        raise ValueError("Le mode doit être soit 'vers_descriptif' soit 'vers_technique'")
def style():
    st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://urlr.me/JbhpKx");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }

        /* Styliser les titres */
    h1{
        color: white;
    }
    h2, h3 {
        color: black;
    }

    /* Centrer les colonnes de la navbar */
    div[data-testid="column"] {
        display: flex;
        justify-content: center;
    }

    /* Styliser les boutons */
    .stButton>button {
        background-color: black;
        color: white;
        border: #7ED957;
        padding: 0.5em 1.2em;
        border-radius: 8px;
        font-weight: bold;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #7ED957;
        color: black;
        transform: scale(1.05); /* agrandissement de 5% */
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        border-radius: 25px;
        border: 2px solid #7ED957;
    }
    </style>
    """,
    unsafe_allow_html=True
)

correspondance = {
    # Format: 'nom_technique': 'nom descriptif'
    'id': "l'identifiant unique",
    'CustomerId': "l'identifiant du client",
    'Surname': 'le nom du client',
    'CreditScore': "le score de crédit",
    'Geography': 'le pays de résidence',
    'Gender': 'le genre du client',
    'Age': "l'âge du client",
    'Tenure': 'la durée de relation client',
    'Balance': 'le solde du compte',
    'NumOfProducts': 'le nombre de produits souscrits',
    'HasCrCard': "la possession d'une carte crédit",
    'IsActiveMember': "le statut de membre actif",
    'EstimatedSalary': "le revenu annuel estimé",
    'Exited': "l'indicateur d'attrition"
}