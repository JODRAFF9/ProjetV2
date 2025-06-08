from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from funcs import load_model
import sklearn
from sklearn.linear_model import LogisticRegression

app = FastAPI()

# Classe qui représente les données d'entrée
class ClientFeatures(BaseModel):
    CreditScore: float
    Geography: float
    Gender: float
    Age: float
    Tenure: float
    Balance: float
    NumOfProducts: float
    HasCrCard: float
    IsActiveMember: float
    EstimatedSalary: float

# Charger le modèle une fois au démarrage
model = load_model()

@app.post("/predict")
def predict_churn(features: ClientFeatures):
    # Transformer les données reçues en DataFrame
    data_dict = features.model_dump()
    df = pd.DataFrame([data_dict])
    
    # Prédiction
    prediction = model.predict(df)[0]
    proba = model.predict_proba(df)[0][1]
    
    return {
        "prediction": int(prediction),
        "probability": float(proba)
    }