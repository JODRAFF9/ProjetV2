#import requests
import streamlit as st
import pandas as pd
from funcs import nom_variable,correspondance,load_model

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

    if st.checkbox("📋 Afficher les données saisies"):
        input_data_renamed = input_data.rename(columns=correspondance)
        st.dataframe(input_data_renamed)
        st.write("---")

    model=load_model()
    if st.button("🔮 Lancer la prédiction"):
        st.markdown("---")
        st.markdown("<h3 style='color:#4B8BBE;'>📊 Résultat de la prédiction</h3>", unsafe_allow_html=True)

        data = input_data.iloc[0].to_dict()

        try:
            prediction = model.predict(input_data)[0]
            proba = model.predict_proba(input_data)[0][1]  # Probabilité de churn

            if prediction == 1:
                st.markdown(
                    f"""
                    <div style="background-color:#FFCCCC;padding:20px;border-radius:10px;border:1px solid #FF4B4B;">
                        <h4 style="color:#C70039;">❌ Risque de départ</h4>
                        <p>Le modèle prédit que ce client <strong>pourrait quitter la banque</strong>.</p>
                        <p><strong>Probabilité de churn :</strong> {proba:.2%}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style="background-color:#D4EDDA;padding:20px;border-radius:10px;border:1px solid #28A745;">
                        <h4 style="color:#155724;">✅ Fidélité probable</h4>
                        <p>Le modèle prédit que ce client <strong>va probablement rester fidèle</strong>.</p>
                        <p><strong>Probabilité de churn :</strong> {proba:.2%}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.markdown(
                f"""
                <div style="background-color:#FFF3CD;padding:20px;border-radius:10px;border:1px solid #FFDD57;">
                    <h4 style="color:#856404;">⚠️ Erreur lors de la prédiction</h4>
                    <pre>{str(e)}</pre>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
