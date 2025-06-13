#import requests
import streamlit as st
import pandas as pd
from funcs import nom_variable,correspondance,load_model

def prediction(data):
    model=load_model()
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

    if st.checkbox("📋 Afficher les données saisies"):
        input_data_renamed = input_data.rename(columns=correspondance)
        st.dataframe(input_data_renamed)
        st.write("---")


    if st.button("🔮 Prédire"):
        st.write("---")
        data = input_data.iloc[0].to_dict()
        try:
            prediction = model.predict(input_data)[0]
            proba = model.predict_proba(input_data)[0][1]  # Proba de churn

            if prediction == "Yes":
                st.error(f"❌ Le client est susceptible de quitter la banque. (Probabilité : {proba:.2%})")
            else:
                st.success(f"✅ Le client est susceptible de rester. (Probabilité de churn : {proba:.2%})")

        except Exception as e:
            st.error(f"Erreur lors de la prédiction : {e}")

    st.write("---")