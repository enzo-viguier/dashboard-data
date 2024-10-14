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

# Fonction qui permet de résumer un article avec des annotation donné en paramètre
def summarize_to_at(article_text):
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system",
             "content": "Vous êtes un assistant spécialisé dans le résumé d'articles de presse. Générez un résumé en une seule phrase avec les éléments Qui, Quand et Où mis en évidence selon le format spécifié."},
            {"role": "user", "content": f"""Résumez cet article en une phrase contenant l'événement principal et ses informations clés. 
            Utilisez le format suivant pour mettre en évidence les éléments Qui, Quand et Où :
            ("texte", "Quand") pour la date/période
            ("texte", "Qui") pour les acteurs principaux
            ("texte", "Ou") pour le lieu

            Exemple de format:
            "Le", ("16 janvier 2024", "Quand"), ("les forces navales iraniennes et pakistanaises", "Qui"), " ont mené des exercices conjoints ", ("au large de Bandar Abbas, dans le détroit d'Ormuz", "Ou"), " visant à renforcer leur coopération militaire et à promouvoir les accords maritimes bilatéraux."
            
            Construis le résumé en commençant par des guillemets doubles, suivis du début de la phrase. Pour chaque élément clé (Quand, Qui, Où), insérez une virgule suivie d'un espace, puis ouvrez une parenthèse. À l'intérieur de cette parenthèse, placez d'abord le texte pertinent entre guillemets doubles, suivi d'une virgule et d'un espace, puis l'étiquette correspondante ('Quand', 'Qui', ou 'Ou') également entre guillemets doubles. Fermez la parenthèse. Continuez la phrase avec le texte non mis en évidence entre les éléments clés, en utilisant des virgules et des espaces pour séparer les différentes parties. Terminez la phrase avec un point à l'intérieur des guillemets doubles de fermeture. 
            Le texte doit se terminer par un guillemet double fermant et pas de point final ou de virgule.
            
            Article à résumer : {article_text}"""}
        ],
        temperature=0.01  # Réduire la température pour des réponses plus cohérentes
    )
    return response.choices[0].message.content

def remove_trailing_period(text):
    if text.endswith('.'):
        return text[:-1]
    return text

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

            # Générer un résumé
            summary = summarize_article(summary_text)

            # Simuler un résumé
            #summary = "le 15 janvier 2024 la NASA a découvert une nouvelle exoplanète possible habitable, nommée Kepler-452c, située à 1400 années-lumière de la Terre."

            st.subheader("Résumé :")
            st.write_stream(stream_data(summary))


            # Résumer l'article avec des annotations
            summary_at = summarize_to_at(summary)
            summary_at = remove_trailing_period(summary_at)
            print(summary_at)

            # Convertir le résumé annoté en une liste de tuples
            try:
                summary_at_list = eval(summary_at)
            except Exception as e:
                st.error(f"Erreur lors de la conversion du résumé annoté : {e}")
                summary_at_list = []

            st.subheader("Résumé annoté :")
            annotated_text(*summary_at_list)

            st.download_button(
                label="Télécharger le résumé",
                data=summary,
                file_name="resume.txt",
                mime="text/plain",
                key="download_button"
            )

            st.download_button(
                label="Télécharger le résumé au format .at",
                data=summary_at,
                file_name="resume.at",
                mime="text/plain",
                key="download_button_at"
            )

    else:
        st.error("Le fichier doit être au format txt.")

# SECTION ANNOTATION

st.title("Annotation d'un résumé d'article")

if summary is None:

    # Variable .at file
    annotation_upload = st.file_uploader("Choisissez un fichier .at vous l'annotation du résumé", type="at", key="annotation_uploader")

    if annotation_upload is not None:

        if is_at_file(annotation_upload):

            content = annotation_upload.read().decode("utf-8")
            at_file = process_at_file(content)

            if at_file:
                annotated_text(*at_file)
