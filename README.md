# 🔍 Recherche d’Images par Similarité avec Elasticsearch

## 📘 Description du Projet
Ce projet consiste à développer une **application web** permettant la recherche d’images par **similarité visuelle** ou par **requête textuelle**.  
Elle repose sur un **backend Flask** en Python et une **base Elasticsearch** pour la recherche vectorielle et textuelle.

L’objectif est de combiner la puissance de l’**apprentissage profond** pour l’extraction des caractéristiques visuelles et la flexibilité d’**Elasticsearch** pour un système de recherche rapide, précis et extensible.

---

## 🧠 Fonctionnalités Principales

### 🔹 Recherche par Image
- Téléversement ou glisser-déposer d’une image.
- Extraction automatique des caractéristiques visuelles via un modèle **VGG16 pré-entraîné**.
- Recherche des images les plus similaires dans Elasticsearch selon plusieurs métriques (cosinus, L1, L2).

### 🔹 Recherche par Texte
- Entrée d’une description textuelle.
- Génération et comparaison des **embeddings textuels** pour trouver les images sémantiquement proches.

### 🔹 Interface Web Interactive
- Conçue avec **HTML, CSS et JavaScript (AJAX)**.
- Affichage instantané des résultats avec score de similarité.
- Deux modes : recherche par image et recherche par texte.

---

---

## 🚀 Installation et Exécution

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/08Youssef08/ElasticSearch_ImageSimiliarities_VGG16featureExtractor_JS_Python.git
cd ElasticSearch_ImageSimiliarities_VGG16featureExtractor_JS_Python
2️⃣ Créer un environnement virtuel
conda create -n searchenv python=3.8
conda activate searchenv

3️⃣ Installer les dépendances
pip install -r requirements.txt

4️⃣ Lancer Elasticsearch

Ouvre le dossier bin d’Elasticsearch et exécute :

elasticsearch.bat


Attends qu’il démarre sur le port 9200.

5️⃣ Indexer les images et les textes
python create_image_embeddings.py
python create_text_embeddings.py

6️⃣ Démarrer l’application
python app.py


➡️ Ouvre ton navigateur à l’adresse :
http://127.0.0.1:5000

🧪 Exemple de Fonctionnement

Recherche par image : téléverse une photo (ex : un chat 🐱), le système affiche les images visuellement similaires.

Recherche par texte : entre un mot-clé comme fleur 🌸, les images correspondantes s’affichent instantanément.

📊 Résultats et Performance

Temps de réponse moyen : < 500 ms

Précision de similarité visuelle : élevée

Évolutivité avec de grandes bases d’images

🏁 Conclusion

Ce projet démontre l’efficacité de l’intégration entre Deep Learning et moteurs de recherche modernes.
Il offre une solution rapide, précise et extensible pour la recherche visuelle et textuelle d’images.
Des améliorations futures incluent :

L’intégration de modèles plus performants (ResNet, EfficientNet)

La recherche multimodale combinant texte et image.

👩‍💻 Auteurs

Emna Belguith

Fatma Abid

Rimel Hammami

Encadré par : M. Riadh Tebourbi
📍 Sup’Com – Tunisie



