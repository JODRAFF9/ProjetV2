import requests
import streamlit as st
import pandas as pd
from funcs import unmap,nom_variable,correspondance

def prediction(data):
    st.write("---")
    st.subheader("🔍 Prédiction de Churn Client")
    form_data = {}
    input_features = data.drop("Exited", axis=1)
    
    st.markdown("**Veuillez saisir les caractéristiques du client :**")
    
    for col_label in input_features.columns:
        if input_features[col_label].dtype == 'object':
            form_data[col_label] = st.selectbox(f"{nom_variable(col_label)}", options=sorted(input_features[col_label].unique()))
        else:
            form_data[col_label] = st.number_input(f"{nom_variable(col_label)}", value=float(input_features[col_label].mean()))

    input_data = pd.DataFrame([form_data])
    input_data=unmap(input_data)

    if st.checkbox("📋 Afficher les données saisies"):
        input_data_renamed = input_data.rename(columns=correspondance)
        st.dataframe(input_data_renamed)
        st.write("---")


    if st.button("🔮 Prédire"):
        st.write("---")
        data = input_data.iloc[0].to_dict()
        try:
            response = requests.post("http://localhost:8000/predict", json=data)
            if response.status_code == 200:
                result = response.json()
                if result["prediction"] == 1:
                    st.error(f"❌ Client susceptible de quitter la banque (Probabilité : {result['probability']:.2%})")
                else:
                    st.success(f"✅ Client susceptible de rester (Probabilité : {result['probability']:.2%})")
            else:
                st.error(f"Erreur API : {response.status_code}")
        except Exception as e:
            st.error(f"Erreur lors de la requête API : {e}")

    st.write("---")

