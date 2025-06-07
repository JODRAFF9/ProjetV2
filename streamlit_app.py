#############################################   Parametrage
import streamlit as st
import pandas as pd
import base64
import plotly.express as px
from funcs import *
import sklearn
from sklearn.linear_model import LogisticRegression

# Configuration de la page Streamlit
st.set_page_config(page_title="Prédiction du BANK CHURN ",page_icon="docs/icon.png" , layout="wide")

model = load_model()

# Chargement des données

train_df = load_data("data/cleaned data/train_df.csv")
train_df_labelled=train_df.drop(['id',"CustomerId","Surname"], axis=1)
map(train_df_labelled)


############################################ Pages

# Initialisation de l'état de la page (si ce n'est pas déjà fait)
if "page" not in st.session_state:
    st.session_state.page = "Accueil"

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
    h1, h2, h3 {
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


# Section Accueil
if st.session_state.page == "Prédiction":
    st.write("---")

if st.session_state.page == "A-propos":
    st.header(" Description des données")
    file_path="docs/description.txt"
    
    try:
        with open(file_path, "r") as file:
            description = file.read()
    except FileNotFoundError:
        st.error(f"Le fichier '{file_path}' est introuvable.")
        st.stop()

    st.code(description, language="markdown")

    def get_download_button_html(text, filename, button_text, bg_color="#4CAF50", text_color="white"):
        b64 = base64.b64encode(text.encode()).decode()
        return f"""
        <a href="data:text/plain;base64,{b64}" download="{filename}">
            <button style="
                background-color:{bg_color};
                color:{text_color};
                padding:10px 20px;
                border:none;
                border-radius:5px;
                cursor:pointer;
                font-size:16px;
            ">{button_text}</button>
        </a>
        """

    custom_button = get_download_button_html(description, "description.txt", "📥 Télécharger la description", "#007acc")
    st.markdown(custom_button, unsafe_allow_html=True)

    st.write("---")
    


# Titre de l'application
st.title("🏡 **Application de Prédiction du BANK CHURN**")
# Fonction pour changer la page active dans st.session_state
def set_page(page_name):
    st.session_state.page = page_name

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
if st.session_state.page == "Accueil":
    st.write("---")
    st.header("Bienvenue 👋")
    st.write("""
        Cette application vous offre des outils intuitifs pour :
        - 🟡 Prédire le **BANK CHURN** à partir de caractéristiques clés.
        - 📊 Analyser les **Caractéristiques des clients**
    """)

    st.info("Utilisez la barre de navigation pour explorer les différentes fonctionnalités.")

# Section Analyse
elif st.session_state.page == "Analyse":
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div style="background-color:#f0f8ff;color:black; padding:10px; border-radius:10px; text-align:center">
                <h3>👥 Clients</h3>
                <p style="font-size:28px; color:#007acc;"><strong>{train_df_labelled.shape[0]}</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        churn_rate = (train_df_labelled['Exited'] == "Yes").mean() * 100
        st.markdown(
            f"""
            <div style="background-color:#fff0f0;color:black; padding:10px; border-radius:10px; text-align:center">
                <h3>❌ Churn Rate</h3>
                <p style="font-size:28px; color:#cc0000;"><strong>{churn_rate:.2f} %</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        avg_salary = train_df_labelled["EstimatedSalary"].mean()
        st.markdown(
            f"""
            <div style="background-color:#f0fff0;color:black; padding:10px; border-radius:10px; text-align:center">
                <h3>💰 Salaire Moyen</h3>
                <p style="font-size:28px; color:#008000;"><strong>{avg_salary:,.0f} €</strong></p>
            </div>
            """,
            unsafe_allow_html=True
    )

    st.markdown("---")
    
    @st.cache_data
    def compute_gender_churn(df):
        return df.groupby(['Gender', 'Exited']).size().reset_index(name='count')

    @st.cache_data
    def compute_figs(df):
        fig1 = px.histogram(df, x="Geography", color="Exited", barmode="group",
                            title="Churn par Géographie", color_discrete_map={"No": "green", "Yes": "red"})
        fig1.update_layout(transition=dict(duration=0))

        gender_churn = compute_gender_churn(df)
        fig2 = px.bar(gender_churn, x='Gender', y='count', color='Exited',
                    title="Churn par Sexe", barmode="group",
                    color_discrete_map={"No": "green", "Yes": "red"})
        fig2.update_layout(transition=dict(duration=0))

        fig3 = px.box(df, x='Exited', y='Age', color='Exited',
                    title='Âge selon Churn', color_discrete_map={"No": "green", "Yes": "red"})
        fig3.update_layout(transition=dict(duration=0))

        return fig1, fig2, fig3
    
    fig1, fig2, fig3 = compute_figs(train_df_labelled)
    
    col4, col5 = st.columns(2)
    with col4:
        st.plotly_chart(fig1, use_container_width=True)
    with col5:
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 🎯 la relation entre âge et Churn")
    st.plotly_chart(fig3, use_container_width=True)