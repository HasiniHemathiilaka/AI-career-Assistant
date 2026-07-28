import os
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

# Setup persistent directory path inside the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHROMA_DATA_PATH = os.path.join(BASE_DIR, "data", "chroma_db")

# Initialize the persistent storage client
chroma_client = PersistentClient(path=CHROMA_DATA_PATH)

# Initialize the vector encoder engine 
# (Downloads automatically on first run; maps text into numerical vectors)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_or_create_collection(collection_name="job_roles"):
    """
    Retrieves an existing vector collection or initializes a new one.
    """
    try:
        # Try to get the existing collection
        return chroma_client.get_collection(name=collection_name)
    except Exception:
        # If it doesn't exist, build a clean collection instance
        return chroma_client.create_collection(name=collection_name)

def add_jobs_to_vector_store(jobs_list, collection_name="job_roles"):
    """
    Encodes job text profiles and indexes them into the vector database.
    Expects a list of dicts containing: id, title, company, description, requirements
    """
    collection = get_or_create_collection(collection_name)
    
    ids = []
    documents = []
    embeddings = []
    metadatas = []
    
    for job in jobs_list:
        job_id = str(job["id"])
        
        # Combine parameters to form a rich text context block for matching
        combined_text = f"Role: {job['title']} at {job['company']}. " \
                        f"Description: {job['description']}. " \
                        f"Requirements: {', '.join(job['requirements'])}"
        
        # Generate raw mathematical vector array
        vector = embedding_model.encode(combined_text).tolist()
        
        ids.append(job_id)
        documents.append(combined_text)
        embeddings.append(vector)
        metadatas.append({
            "title": job["title"],
            "company": job["company"]
        })
        
    # Upsert the items directly into ChromaDB
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    print(f"Successfully loaded and indexed {len(ids)} positions into the vector store.")