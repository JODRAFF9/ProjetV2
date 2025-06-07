import streamlit as st
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
