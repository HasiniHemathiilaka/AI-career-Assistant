import os
from pathlib import Path
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

# 1. Setup absolute paths for the vector storage engine
BASE_DIR = Path(__file__).resolve().parent.parent.parent
VECTOR_DB_DIR = os.path.join(BASE_DIR, "data", "chroma_db")

# 2. Initialize the persistent ChromaDB client
chroma_client = PersistentClient(path=VECTOR_DB_DIR)

# 3. Load the embedding model locally
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_or_create_collection(collection_name="internships"):
    """Retrieves an existing collection or creates a new one."""
    return chroma_client.get_or_create_collection(name=collection_name)

def add_job_description(job_id, job_title, company, description_text, required_skills):
    """
    Converts job text to embeddings and inserts it into ChromaDB with metadata.
    """
    collection = get_or_create_collection()
    
    # Generate the vector embedding for the raw job description text
    vector = embedding_model.encode(description_text).tolist()
    
    # Store the document along with structural metadata
    collection.add(
        ids=[str(job_id)],
        embeddings=[vector],
        documents=[description_text],
        metadatas=[{
            "job_title": job_title,
            "company": company,
            "required_skills": ", ".join(required_skills)
        }]
    )
    print(f"✅ Successfully ingested: {job_title} at {company}")