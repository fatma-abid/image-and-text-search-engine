# 🔍 Recherche d'Images par Similarité avec Elasticsearch

## 📋 Description

Ce projet propose une application web de recherche d'images par similarité visuelle et par requête textuelle, combinant les techniques de Deep Learning et le moteur de recherche Elasticsearch.

### Fonctionnalités principales

L'application offre deux modes de recherche complémentaires :

* **Recherche par image** : Retrouvez des images visuellement similaires à partir d'une image téléversée
* **Recherche par texte** : Trouvez des images pertinentes à partir de mots-clés ou de descriptions

## 🚀 Installation et Configuration

### Prérequis

- Python 3.8+
- Elasticsearch 9.x
- Conda (recommandé) ou virtualenv

### Étapes d'installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/fatma-abid/image-and-text-search-engine.git
cd image-and-text-search-engine
```

2. **Créer et activer un environnement virtuel**
```bash
conda create -n searchenv python=3.8
conda activate searchenv
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancer Elasticsearch**

Naviguez vers le dossier `bin` de votre installation Elasticsearch et exécutez :
```bash
elasticsearch.bat  # Windows
# ou
./elasticsearch    # Linux/Mac
```

Attendez que le service démarre sur le port par défaut `9200`.

## 📊 Indexation des Données

Avant d'utiliser l'application, indexez vos images et descriptions textuelles :
```bash
python create_image_embeddings.py
python create_text_embeddings.py
```

Ces scripts effectuent les opérations suivantes :
- Extraction des caractéristiques visuelles via le modèle VGG16
- Analyse et traitement des descriptions textuelles associées
- Stockage optimisé dans Elasticsearch pour des recherches rapides

## 🎯 Démarrage de l'Application

Lancez le serveur Flask :
```bash
python app.py
```

Accédez ensuite à l'application via votre navigateur : **http://127.0.0.1:5000**

## 💡 Exemple d'Utilisation

### Recherche par image
1. Téléversez une photo (exemple : un chat)
2. Le système analyse l'image et affiche instantanément les images les plus similaires visuellement

### Recherche par texte
1. Entrez un mot-clé ou une description (exemple : "fleur")
2. L'application retourne immédiatement les images correspondantes

## 📈 Performances

- **Temps de réponse moyen** : < 500 ms
- **Précision de similarité visuelle** : Élevée grâce au modèle VGG16
- **Évolutivité** : Architecture capable de gérer de grandes bases d'images

Le système combine efficacement Flask, Elasticsearch et VGG16 pour offrir rapidité, précision et scalabilité.

## 🏗️ Architecture du Projet
```
.
├── app.py                          # Application Flask principale
├── create_image_embeddings.py      # Extraction et indexation des features d'images
├── create_text_embeddings.py       # Indexation des descriptions textuelles
├── feature_extractor.py            # Implémentation du modèle VGG16
├── requirements.txt                # Dépendances Python
├── README.md                       # Documentation
├── static/
│   ├── script.js                   # Scripts JavaScript côté client
│   └── styles.css                  # Feuilles de style CSS
└── templates/
    └── index.html                  # Interface web
```


