import streamlit as st
import base64

def apropos():
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