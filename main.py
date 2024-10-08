import os
import time
import streamlit as st
from annotated_text import annotated_text
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# OPEN API
api_key = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=api_key)
model_name = "ft:gpt-3.5-turbo-0125:personal::AFeX2hYK" # Model Finetuned

# Global variable
summary = None

# Fonction qui permet de résumer un article donné en paramètre
def summarize_article(article_text):
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "Vous êtes un assistant spécialisé dans le résumé d'articles de presse."},
            {"role": "user", "content": f"Résumez cet article en une phrase contenant l'événement principal et ses informations clés (qui, quand, où) : {article_text}"}
        ]
    )
    return response.choices[0].message.content

# Fonction qui permet d'afficher un message mot par mot
def stream_data(text_to_display):
    for word in text_to_display.split():
        yield word + " "
        time.sleep(0.05)

# Fonction permettant de traiter le contenu d'un fichier .at
def process_at_file(content):
    # Remplacer les nouvelles lignes et espaces superflus
    content = content.strip()

    # Évaluer le contenu pour le transformer en une liste d'éléments
    try:
        # Utilisez eval pour évaluer le contenu comme du code Python
        return eval(content)
    except Exception as e:
        st.error(f"Erreur lors du traitement du fichier : {e}")
        return []

def is_txt_file(file):
    return file.name.endswith('.txt')

def is_csv_file(file):
    return file.name.endswith('.csv')

def is_at_file(file):
    return file.name.endswith('.at')

# Titre de l'application
st.markdown("<h1 style='text-align: center;'>Groupe 2 - Data</h1>", unsafe_allow_html=True)


## SECTION RESUME D'ARTICLE

st.title("Résumé d'articles de presse")

summary_upload = st.file_uploader("Choisissez un fichier txt", type="txt", key="summary_uploader")

if summary_upload is not None:
    if is_txt_file(summary_upload):
        # Lire le contenu du fichier txt
        summary_text = summary_upload.getvalue().decode("utf-8")

        # Afficher le contenu original
        st.subheader("Contenu original :")
        st.text(summary_text)


        # Résumer l'article
        if st.button("Générer le résumé de l'article"):

            # Commenter / Décommenter si on souhaite utiliser l'API OpenAI
            # summary = summarize_article(summary_text)

            # Simuler un résumé
            summary = "le 15 janvier 2024 la NASA a découvert une nouvelle exoplanète possible habitable, nommée Kepler-452c, située à 1400 années-lumière de la Terre."

            st.subheader("Résumé :")
            # st.write(summary)
            st.write_stream(stream_data(summary))
            # message(summary)

            st.download_button(
                label="Télécharger le résumé",
                data=summary,
                file_name="resume.txt",
                mime="text/plain",
                key="download_button"
            )
    else:
        st.error("Le fichier doit être au format txt.")

# SECTION ANNOTATION

st.title("Annotation d'un résumé d'article")

if summary is None:

    # Variable .at file
    annotation_upload = st.file_uploader("Choisissez un fichier .at pour l'annotation", type="at", key="annotation_uploader")

    if annotation_upload is not None:

        if is_at_file(annotation_upload):

            content = annotation_upload.read().decode("utf-8")
            at_file = process_at_file(content)

            if at_file:
                annotated_text(*at_file)
