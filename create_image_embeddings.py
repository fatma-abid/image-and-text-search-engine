from feature_extractor import FeatureExtractor
from elasticsearch import Elasticsearch
from PIL import Image
import os
import time  # Pour les pauses entre les tentatives

def create_image_embeddings(es_host, images_directory, start_folder=16, end_folder=30, max_retries=2):
    """
    Crée des embeddings d'images pour les dossiers numérotés de start_folder à end_folder inclus,
    puis les indexe dans Elasticsearch. En cas d'erreur, réessaye plusieurs fois avant de passer
    au fichier suivant. Si le dossier entier pose problème, passe au dossier suivant.
    """
    # Connexion à Elasticsearch
    es = Elasticsearch(
        es_host,
        request_timeout=360000,
    )
    
    index_name = 'embeddings2002'  # Index de test pour ne pas polluer le vrai index
    
    # Créer l'index s'il n'existe pas
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        print(f"✅ Index '{index_name}' créé avec succès.")
    else:
        print(f"⚠️ L'index '{index_name}' existe déjà.")
    
    feature_extractor = FeatureExtractor() 
    
    # Parcours des dossiers
    for folder in range(start_folder, end_folder + 1):
        folder_name = str(folder)
        folder_path = os.path.join(images_directory, folder_name)

        try:  # Gestion des erreurs au niveau du dossier
            # Vérifie que le dossier existe
            if not os.path.isdir(folder_path):
                print(f"❌ Dossier introuvable : {folder_path}")
                continue

            print(f"\n📂 Traitement du dossier : {folder_name}")

            # Parcours des fichiers dans le dossier
            for file in os.listdir(folder_path):
                if file.lower().endswith(('jpeg', 'jpg', 'png')):
                    # Ignorer les images dont le nom se termine par (1)
                    if file.endswith('(1).jpg') or file.endswith('(1).jpeg') or file.endswith('(1).png'):
                         print(f"⏩ Image ignorée (nom se terminant par (1)) : {file}")
                         continue
                    
                    image_path = os.path.join(folder_path, file)
                    image_id = f"{folder_name}_{os.path.splitext(file)[0]}"
                    
                    retries = 0
                    while retries < max_retries:
                        try:
                            # Ouverture de l'image et extraction des features
                            img = Image.open(image_path)
                            embedding = feature_extractor.extract(img)

                            # Création du document à indexer
                            doc = {
                                "image_id": image_id,
                                "image_name": file,
                                "image_embedding": embedding.tolist(),  
                                "relative_path": os.path.relpath(image_path, images_directory)
                            }

                            # Indexation dans Elasticsearch
                            es.index(index=index_name, document=doc)
                            print(f"✅ Image indexée : {image_id}")
                            break  # Sortie de la boucle retry si succès
                        
                        except Exception as e:
                            retries += 1
                            print(f"⚠️ Erreur lors du traitement de {file} (tentative {retries}/{max_retries}): {e}")
                            if retries == max_retries:
                                print(f"❌ Impossible de traiter {file} après {max_retries} tentatives. ➡️ Passage au fichier suivant.\n")
                            else:
                                time.sleep(5)

        except Exception as e_folder:
            print(f"❌ Erreur sur le dossier {folder_name} : {e_folder} ➡️ Passage au dossier suivant.\n")


if __name__ == '__main__':
    # Paramètres Elasticsearch
    ES_HOST = "http://127.0.0.1:9200/"
    ES_USER = "elastic"
    ES_PASSWORD = "changeme"
    ES_TIMEOUT = 360000

    DEST_INDEX = "embeddings2002"
    DELETE_EXISTING = True
    CHUNK_SIZE = 100

    PATH_TO_IMAGES = "../app/static/images/**/*.jp*g"
    PREFIX = "../app/static/images/"

    # Chemin vers ton dataset principal (inchangé)
    IMAGES_DIRECTORY = r"D:\Search_with_images\images"

    # Exécution sur les dossiers 11 à 30 uniquement
    try:
        create_image_embeddings(ES_HOST, IMAGES_DIRECTORY, start_folder=16, end_folder=30)
        print("\n✅ Test terminé avec succès sur les dossiers 11 à 30.")
    except Exception as e:
        print(f"❌ Une erreur est survenue : {e}")
