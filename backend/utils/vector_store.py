import os
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

# Setup persistent directory path inside the project root (data/chroma_db)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHROMA_DATA_PATH = os.path.join(BASE_DIR, "data", "chroma_db")

# Initialize the persistent storage client
chroma_client = PersistentClient(path=CHROMA_DATA_PATH)

# Initialize the vector encoder engine
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def get_or_create_collection(collection_name="job_postings"):
    """
    Retrieves an existing vector collection or initializes a new one.
    """
    try:
        return chroma_client.get_collection(name=collection_name)
    except Exception:
        return chroma_client.create_collection(name=collection_name)


def add_jobs_to_vector_store(jobs_list, collection_name="job_postings"):
    """
    Encodes job text profiles and indexes them into the vector database.
    Expects a list of dicts containing: id, title, company, description, requirements/skills
    """
    collection = get_or_create_collection(collection_name)
    
    ids = []
    documents = []
    embeddings = []
    metadatas = []
    
    for job in jobs_list:
        job_id = str(job["id"])
        
        # Convert requirements or skills list into a comma-separated string
        if isinstance(job.get("requirements"), list):
            skills_str = ", ".join(job["requirements"])
        elif isinstance(job.get("skills"), list):
            skills_str = ", ".join(job["skills"])
        else:
            skills_str = str(job.get("requirements", job.get("skills", "")))

        doc_text = job["description"]
        combined_text_for_embedding = (
            f"Role: {job['title']} at {job['company']}. "
            f"Description: {doc_text}. "
            f"Skills: {skills_str}"
        )
        
        vector = embedding_model.encode(combined_text_for_embedding).tolist()
        
        ids.append(job_id)
        documents.append(doc_text)
        embeddings.append(vector)
        
        # Metadata dictionary containing all keys expected by matcher.py
        metadatas.append({
            "job_title": job["title"],
            "company": job["company"],
            "description": doc_text,
            "required_skills": skills_str
        })
        
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    print(f"Successfully loaded and indexed {len(ids)} positions into the vector store.")