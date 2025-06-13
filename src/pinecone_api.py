from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

# Initialize Pinecone and model
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("faq-documents")
model = SentenceTransformer("all-MiniLM-L6-v2")

@app.route('/search', methods=['POST'])
def search():
    try:
        query = request.json['query']
        query_embedding = model.encode([query])[0].tolist()
        results = index.query(
            vector=query_embedding,
            top_k=3,
            include_metadata=True
        )
        return jsonify({
            'documents': [match['metadata']['text'] for match in results['matches']],
            'ids': [match['id'] for match in results['matches']],
            'scores': [match['score'] for match in results['matches']]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)