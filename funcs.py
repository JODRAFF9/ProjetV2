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
    with open("code/final_model/rl_model.pkl", "rb") as f:
        return dill.load(f)

def map(data):
    binary_mapping = {0: 'No', 1: 'Yes'}
    binary_cols = ['HasCrCard', 'IsActiveMember', 'Exited']

    cat_cols = ['Geography', 'Gender', 'Tenure', 'NumOfProducts', 'HasCrCard',
        'IsActiveMember']

    num_cols = ['CreditScore', 'Age', 'Balance', 'EstimatedSalary']

    target = 'Exited'

    for col in binary_cols:
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
    
    noms_descriptifs = [
    "le score de crédit",
    "le pays de résidence",
    "le genre du client",
    "l'âge du client",
    "la durée de relation client",
    "le solde du compte",
    "le nombre de produits souscrits",
    "la possession d'une carte crédit",
    "le statut de membre actif",
    "le revenu annuel estimé",
    "l'indicateur d'attrition"
]