import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("faq-documents")

# Initialize embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

def extract_text_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def chunk_text(text, max_chunk_size=1000):
    chunks = []
    # Split by question to keep Q&A pairs intact
    questions = text.split("question:")
    for q in questions[1:]:  # Skip first split (before first question)
        chunk = "question:" + q.strip()
        if len(chunk) <= max_chunk_size:
            chunks.append(chunk)
        else:
            # If too long, split further
            words = chunk.split()
            current_chunk = ""
            for word in words:
                if len(current_chunk) + len(word) + 1 <= max_chunk_size:
                    current_chunk += word + " "
                else:
                    chunks.append(current_chunk.strip())
                    current_chunk = word + " "
            if current_chunk:
                chunks.append(current_chunk.strip())
    return chunks

def generate_embeddings(chunks):
    return model.encode(chunks, convert_to_tensor=False).tolist()

def store_in_pinecone(chunks, embeddings, doc_name):
    vectors = [
        {"id": f"{doc_name}_chunk_{i}", "values": embedding, "metadata": {"text": chunk}}
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
    ]
    index.upsert(vectors=vectors)
    print(f"Stored {len(vectors)} chunks from {doc_name} in Pinecone")

def process_document(file_path):
    doc_name = os.path.basename(file_path).split('.')[0]
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.md') or file_path.endswith('.txt'):
        text = extract_text_from_file(file_path)
    else:
        print(f"Unsupported file format: {file_path}")
        return

    if not text:
        print(f"No text extracted from {file_path}")
        return

    chunks = chunk_text(text)
    embeddings = generate_embeddings(chunks)
    store_in_pinecone(chunks, embeddings, doc_name)

# Process documents
documents_dir = "data/sample-documents"
os.makedirs(documents_dir, exist_ok=True)

for filename in os.listdir(documents_dir):
    file_path = os.path.join(documents_dir, filename)
    print(f"Processing {file_path}")
    process_document(file_path)