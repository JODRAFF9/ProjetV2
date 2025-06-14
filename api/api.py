from fastapi import FastAPI
from pydantic import BaseModel
from funcs import load_model
import pickle
import pandas as pd


app = FastAPI()

@app.get("/")
def read_root():
    return {"message":"Hello,FastAPI!"}

# # Classe qui représente les données d'entrée
class ClientFeatures(BaseModel):
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float
# Charger le modèle une fois au démarrage
model = load_model()
# with open("rl_model.pkl","rb") as f:
#     model=pickle.load(f)

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
