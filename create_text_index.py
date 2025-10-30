import os
import time
import re
from elasticsearch import Elasticsearch

def is_repeated_image(image_id):
    """
    Vérifie si l'image a un suffixe comme (1), (2), etc.
    """
    # L'ID de l'image ne doit pas se terminer par (1), (2), ...
    return bool(re.search(r"\(\d+\)$", image_id))

def create_text_embeddings(es_host, tags_directory, start_folder=10, end_folder=30, max_retries=2):
    """
    Crée un index Elasticsearch pour les tags textes contenus dans des fichiers .txt,
    en parcourant les dossiers numérotés de start_folder à end_folder.
    """
    # Connexion à Elasticsearch
    es = Elasticsearch(es_host, request_timeout=360000)
    
    index_name = "text_tags"

    # Créer l'index s'il n'existe pas
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body={
            "mappings": {
                "properties": {
                    "image_id": {"type": "keyword"},
                    "relative_path": {"type": "keyword"},
                    "tags": {"type": "text", "analyzer": "french"}
                }
            }
        })
        print(f"✅ Index '{index_name}' créé avec succès.")
    else:
        print(f"⚠️ L'index '{index_name}' existe déjà.")
    
    # Parcours des dossiers
    for folder in range(start_folder, end_folder + 1):
        folder_name = str(folder)
        folder_path = os.path.join(tags_directory, folder_name)

        try:
            if not os.path.isdir(folder_path):
                print(f"❌ Dossier introuvable : {folder_path}")
                continue

            print(f"\n📂 Traitement du dossier de tags : {folder_name}")

            for file in os.listdir(folder_path):
                if file.lower().endswith(".txt"):
                    text_path = os.path.join(folder_path, file)
                    image_id = f"{folder_name}_{os.path.splitext(file)[0]}"

                    # Vérifier si l'image est répétée avant d'indexer les tags
                    if is_repeated_image(image_id):
                        print(f"⏩ Ignorer les tags pour l'image répétée : {image_id}")
                        continue

                    retries = 0
                    while retries < max_retries:
                        try:
                            with open(text_path, "r", encoding="utf-8") as f:
                                tags_text = f.read().strip()

                            doc = {
                                "image_id": image_id,
                                "relative_path": os.path.relpath(text_path, tags_directory),
                                "tags": tags_text
                            }

                            es.index(index=index_name, document=doc)
                            print(f"✅ Tags indexés : {image_id}")
                            break
                        except Exception as e:
                            retries += 1
                            print(f"⚠️ Erreur sur {file} (tentative {retries}/{max_retries}): {e}")
                            if retries == max_retries:
                                print(f"❌ Impossible de traiter {file}. ➡️ Passage au fichier suivant.")
                            else:
                                time.sleep(5)

        except Exception as e_folder:
            print(f"❌ Erreur sur le dossier {folder_name}: {e_folder} ➡️ Passage au dossier suivant.")

if __name__ == "__main__":
    ES_HOST = "http://127.0.0.1:9200/"
    TAGS_DIRECTORY = r"D:\Search_with_images\tags"
    
    try:
        create_text_embeddings(ES_HOST, TAGS_DIRECTORY, start_folder=10, end_folder=30)
        print("\n✅ Indexation texte terminée pour les dossiers 10 à 30.")
    except Exception as e:
        print(f"❌ Une erreur est survenue : {e}")
