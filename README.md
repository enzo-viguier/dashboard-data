# Dashboard

## Auteurs

[Enzo VIGUIER](https://github.com/enzo-viguier)  
[Tristan GAIDO](https://github.com/tristan-gaido)  
[Morgan NAVEL](https://github.com/MorganNavel)  
[Eric GILLES](https://github.com/eric-gilles)

## Introduction

Ce projet utilise Streamlit et un modèle fine-tuné d'OpenAI pour générer des résumés d'articles de presse. L'application
permet à l'utilisateur de télécharger un fichier texte contenant un article, de générer un résumé, et de télécharger le
résumé annoté. Les éléments clés (qui, quand, où) sont mis en évidence dans le résumé pour une meilleure lisibilité et
compréhension.

## Comment utiliser le projet

### Fichier d'environnement

Créez un fichier `.env` à la racine du projet et ajoutez les variables suivantes :

```bash
OPENAI_API=
OPEN_AI_MODEL=
```

### Avec Makefile

1. **Installation des dépendances** :
   Assurez-vous d'avoir Python installé sur votre machine. Clonez ce dépôt et installez les dépendances en utilisant le
   `Makefile` :
   ```bash
   make install

2. **Lancer l'application** :
    Pour lancer l'application, utilisez la commande suivante :
    ```bash
    make run
    ```
   
### Sans Makefile

1. **Installation des dépendances** :
   Assurez-vous d'avoir Python installé sur votre machine. Clonez ce dépôt et installez les dépendances en utilisant le
   `requirements.txt` :
   ```bash
   pip install -r requirements.txt
   ```
   
2. **Lancer l'application** :
    Pour lancer l'application, utilisez la commande suivante :
    ```bash
    streamlit run main.py
    ```

### FineTuning du modèle

Pour réaliser un modèle fine-tuné, vous pouvez utiliser le fichier `donnees_fine_tuning_chat.jsonl` et utiliser OpenAI pour entraîner un modèle sur ces données.

Si vous souhaitez utiliser notre modèle fine-tuné, vous pouvez renseigné la variable `OPEN_AI_MODEL` dans le fichier `.env` avec la valeur `ft:gpt-3.5-turbo-0125:personal::AFeX2hYK`.
Il est encouragé de fine-tuner le modèle sur vos propres données pour de potentiels meilleurs résultats.

### Conclusion

Ce projet permet de générer des résumés d'articles de presse de manière simple et efficace. 
Il utilise un modèle fine-tuné avec OpenAI pour générer des résumés de qualité. 
Les éléments clés sont mis en évidence pour une meilleure lisibilité et compréhension grâce à l'annotation des résumés sur l'interface web.