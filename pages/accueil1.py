import streamlit as st
def accueil():
    st.write("---")
    st.header("Bienvenue 👋")
    st.write("""
        Cette application vous offre des outils intuitifs pour :
        - 🟡 **Prévoir si un client risque de quitter la banque.**
        - 📊 **Analyser les Caractéristiques de ces clients**
    """)

    st.info("Utilisez la barre de navigation pour explorer les différentes fonctionnalités.")