from flask import Flask, request, jsonify, render_template, send_from_directory
from feature_extractor import FeatureExtractor
from flask_cors import CORS
from elasticsearch import Elasticsearch
import numpy as np
from PIL import Image
import os
import io
import base64

app = Flask(__name__)
extractor = FeatureExtractor()  # Make sure FeatureExtractor is properly implemented
CORS(app)

# Elasticsearch Configuration
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Image folder
UPLOAD_FOLDER = r"D:/Search_with_images/images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Route to serve images ---
@app.route('/images/<folder>/<filename>')
def uploaded_file(folder, filename):
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
    
    # Clean the filename to remove suffixes (1), (2), etc.
    filename_clean = filename.split('(')[0].replace('.txt', '') 
    print(filename_clean)
    # Check for possible image extensions (jpg, jpeg, png)
    for ext in ['.jpg', '.jpeg', '.png']:
        file_path = os.path.join(folder_path, filename_clean + ext)
        if os.path.isfile(file_path):
            return send_from_directory(folder_path, filename_clean + ext)
    
    return jsonify({"error": "Image not found"}), 404


# --- Home route ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Extract features from an image ---
@app.route('/extract_features', methods=['POST'])
def extract_features():
    try:
        data = request.json
        img_data = base64.b64decode(data['image'])  # Decode base64 image
        img = Image.open(io.BytesIO(img_data))
        features = extractor.extract(img)
        return jsonify({'features': features.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# --- Search similar images ---
@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query_features = np.array(data['features'])
        metric = data.get('metric', 'cosine')
        top_n = data.get('top_n', 10)  # Number of similar images to fetch
        similar_images = search_similar_images(query_features, metric, top_n)
        return jsonify(similar_images)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# --- Search images by text (tags) ---
@app.route('/search_text', methods=['GET'])
def search_text():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])  # Return empty list if no query is given

    # Elasticsearch fuzzy query for text matching
    query_body = {
        "query": {
            "match": {
                "tags": {
                    "query": query,  # The search term entered by the user
                    "fuzziness": "AUTO"  # This allows for fuzzy matching
                }
            }
        }
    }

    try:
        response = es.search(index="text_tags", body=query_body)
        results = []

        for hit in response['hits']['hits']:
            image_id = hit['_source']['image_id']
            relative_path = hit['_source']['relative_path']

            # Clean the relative_path to remove suffixes like (1), (2)
            relative_path = relative_path.split('(')[0]

            results.append({
                'image_id': image_id,
                'tags': hit['_source']['tags'],
                'relative_path': relative_path
            })

        return jsonify(results)
    
    except Exception as e:
        print(f"Elasticsearch Error: {e}")
        return jsonify([])

# --- Search function in Elasticsearch ---
def search_similar_images(query_features, metric, top_n=5):
    query_vector = query_features.tolist()

    # Select script based on similarity metric
    if metric == 'cosine':
        script_source = "cosineSimilarity(params.query_vector, 'image_embedding') + 1.0"
    elif metric == 'l1':
        script_source = "1 / (1 + l1norm(params.query_vector, 'image_embedding'))"
    elif metric == 'l2':
        script_source = "1 / (1 + l2norm(params.query_vector, 'image_embedding'))"
    else:
        script_source = "cosineSimilarity(params.query_vector, 'image_embedding') + 1.0"

    query = {
        "size": top_n,
        "_source": ["image_id", "image_name", "relative_path"],
        "query": {
            "script_score": {
                "query": {"match_all": {}} ,
                "script": {"source": script_source, "params": {"query_vector": query_vector}}
            }
        }
    }

    try:
        response = es.search(index='embeddings', body=query)
        similar_images = []
        for hit in response['hits']['hits']:
            image_id = hit['_source']['image_id'].split('(')[0]  # Clean up suffix
            relative_path = hit['_source']['relative_path'].split('(')[0]
            image_name = hit['_source']['image_name']
            similar_images.append({
                'image_id': image_id,
                'image_name': image_name,
                'relative_path': relative_path
            })
        return similar_images
    except Exception as e:
        print("Elasticsearch Error:", e)
        return []

# --- Run the server ---
if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
