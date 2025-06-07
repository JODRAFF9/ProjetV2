import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import dill
from sklearn.linear_model import LogisticRegression

# Configuration de la page Streamlit
st.set_page_config(page_title="Prédiction du BANK CHURN ",page_icon="docs/icon.png" , layout="wide")

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

@st.cache_resource
def load_model():
    with open("code/final_model/rl_model.pkl", "rb") as f:
        return dill.load(f)

model = load_model()

# Fonction pour charger les données (mise en cache)
@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Le fichier {file_path} est introuvable.")
        return pd.DataFrame()

# Chargement des données
train_df = load_data("data/cleaned data/train_df.csv")
train_df_labelled=train_df.drop(['id',"CustomerId","Surname"], axis=1)

binary_mapping = {0: 'No', 1: 'Yes'}
binary_cols = ['HasCrCard', 'IsActiveMember', 'Exited']

cat_cols = ['Geography', 'Gender', 'Tenure', 'NumOfProducts', 'HasCrCard',
       'IsActiveMember']

num_cols = ['CreditScore', 'Age', 'Balance', 'EstimatedSalary']

target = 'Exited'

for col in binary_cols:
    train_df_labelled[col] = train_df_labelled[col].map(binary_mapping)


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

# Initialisation de l'état de la page (si ce n'est pas déjà fait)
if "page" not in st.session_state:
    st.session_state.page = "Accueil"

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


    # # 1. Répartition du Churn par Pays
    # col4, col5 = st.columns(2)
    # with col4:
    #     fig1 = px.histogram(train_df_labelled, x="Geography", color="Exited", barmode="group",
    #                         title="Churn par Géographie", color_discrete_map={"No":"green", "Yes":"red"})
    #     st.plotly_chart(fig1, use_container_width=True)

    # # 2. Répartition homme/femme dans le churn
    # with col5:
    #     gender_churn = train_df_labelled.groupby(['Gender', 'Exited']).size().reset_index(name='count')
    #     fig2 = px.bar(gender_churn, x='Gender', y='count', color='Exited',
    #                 title="Churn par Sexe", barmode="group",
    #                 color_discrete_map={"No":"green", "Yes":"red"})
    #     st.plotly_chart(fig2, use_container_width=True)

    # # 3. Age vs Churn
    # st.markdown("### 🎯 la rélation entre âge et Churn")
    # fig3 = px.box(train_df_labelled, x='Exited', y='Age', color='Exited', 
    #             title='Répartition de l\'âge selon le statut (Churn)', 
    #             color_discrete_map={"No": "green", "Yes": "red"})
    # st.plotly_chart(fig3, use_container_width=True)

    # # 4. Corrélation entre variables numériques
    # st.markdown("### 🔍 Corrélation")
    # correlation = train_df_labelled[num_cols].corr()
    # fig4 = px.imshow(correlation, text_auto=True, color_continuous_scale='RdBu_r',
    #                 title="Matrice de Corrélation")
    # st.plotly_chart(fig4, use_container_width=True)

    # # 5. Sélection interactive : Salary vs Churn selon le pays
    # st.markdown("### 📊 Analyse personnalisée")
    # selected_country = st.selectbox("Choisir un pays", train_df_labelled["Geography"].unique())
    # filtered_train_df_labelled = train_df_labelled[train_df_labelled["Geography"] == selected_country]

    # fig5 = px.scatter(filtered_train_df_labelled, x="EstimatedSalary", y="Age", color="Exited",
    #                 title=f"Salaire vs Âge ({selected_country})",
    #                 color_discrete_map={0:"green", 1:"red"})
    # st.plotly_chart(fig5, use_container_width=True)
        
    
    
# """     """
#     if st.checkbox("Afficher les données brutes"):
#         st.dataframe(train_df.head(100))

#     st.write("### Statistiques descriptives")
#     st.write(train_df_labelled[num_cols].describe())

#     st.write("### Visualisation de deux variables")

#     nomx = st.selectbox("Variable X", noms_descriptifs)
#     nomy = st.selectbox("Variable Y", noms_descriptifs)

#     variable_x=nom_variable(nomx,mode="vers_technique")
#     variable_y=nom_variable(nomy,mode="vers_technique")


#     # Visualisation des relations entre les variables
#     fig, ax = plt.subplots(figsize=(10, 8))
#     if variable_x in num_cols and variable_y in num_cols:
#         sns.scatterplot(data=train_df_labelled, x=variable_x, y=variable_y, ax=ax, color="teal", s=100, edgecolor='black')
#         ax.set_title(f"Nuage de points entre {nomx} et {nomy}", fontsize=16, fontweight='bold')
#         ax.set_xlabel(variable_x, fontsize=14)
#         ax.set_ylabel(variable_y, fontsize=14)
#         ax.tick_params(axis='both', which='major', labelsize=12,rotation=45)
#         ax.grid(True, linestyle='--', alpha=0.7)
#     elif (variable_x in cat_cols or variable_x in target) and (variable_y in cat_cols or variable_y in target):
#         grouped_train_df_labelled = train_df_labelled.groupby([variable_x, variable_y]).size().unstack()
#         grouped_train_df_labelled.plot(kind='bar', stacked=True, ax=ax, cmap='coolwarm')
#         ax.set_title(f"Graphique en barres empilées de {nomx} par {nomy}", fontsize=16, fontweight='bold')
#         ax.set_xlabel(variable_x, fontsize=14)
#         ax.set_ylabel("Effectifs", fontsize=14)
#         ax.tick_params(axis='both', which='major', labelsize=12,rotation=45)
#         ax.legend(title=variable_y, fontsize=12)
#     else:
#         sns.boxplot(data=train_df_labelled, x=variable_x, y=variable_y, ax=ax, palette="Set2")
#         ax.set_title(f"Graphique de boîte de {nomy} par {nomx}", fontsize=16, fontweight='bold')
#         ax.set_xlabel(variable_x, fontsize=14)
#         ax.set_ylabel(variable_y, fontsize=14)
#         ax.tick_params(axis='both', which='major', labelsize=12,rotation=45)

#     st.pyplot(fig)
#     st.write("---")

#     st.write("### Matrice de Corrélation")
#     correlation_matrix = train_df_labelled[num_cols].corr()
#     mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
#     fig_corr, ax_corr = plt.subplots(figsize=(14, 12))
#     sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", mask=mask, fmt=".2f")
#     st.pyplot(fig_corr)*/
#     """ """
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
    