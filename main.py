import os
import time

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPEN_API_KEY")

client = OpenAI(api_key=api_key)

model_name = "ft:gpt-3.5-turbo-0125:personal::AFeX2hYK"

def summarize_article(article_text):
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "Vous êtes un assistant spécialisé dans le résumé d'articles de presse."},
            {"role": "user", "content": f"Résumez cet article en une phrase contenant l'événement principal et ses informations clés (qui, quand, où) : {article_text}"}
        ]
    )
    return response.choices[0].message.content

def stream_data(text_to_display):
    for word in text_to_display.split():
        yield word + " "
        time.sleep(0.05)

def is_txt_file(file):
    return file.name.endswith('.txt')

def is_csv_file(file):
    return file.name.endswith('.csv')

# Titre de l'application
st.markdown("<h1 style='text-align: center;'>Groupe 2 - Data</h1>", unsafe_allow_html=True)


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
                mime="text/plain"
            )


    else:
        st.error("Le fichier doit être au format txt.")
