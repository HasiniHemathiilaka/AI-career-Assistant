import numpy as np
from backend.utils.vector_store import get_or_create_collection, embedding_model

def calculate_cosine_similarity(vec1, vec2):
    """
    Computes standard cosine similarity between two numeric arrays.
    """
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    return float(dot_product / (norm_vec1 * norm_vec2))

def match_resume_to_jobs(student_skills):
    """
    Queries ChromaDB, checks direct keyword overlap metrics,
    and returns a structured list of compatible internship matches.
    """
    collection = get_or_create_collection()
    results = collection.get(include=["documents", "metadatas"])
    
    # If the collection is completely empty, exit early
    if not results["ids"]:
        return []
        
    # Convert student skill list to lowercase for bulletproof comparison check
    student_skills_lower = [skill.lower() for skill in student_skills]
    
    # Vectorize the student's semantic background profile
    student_profile_text = " ".join(student_skills)
    student_vector = embedding_model.encode(student_profile_text)
    
    match_reports = []
    
    for i in range(len(results["ids"])):
        metadata = results["metadatas"][i]
        doc_text = results["documents"][i]
        
        # 1. Calculate semantic vector match score
        job_vector = embedding_model.encode(doc_text)
        semantic_score = calculate_cosine_similarity(student_vector, job_vector)
        
        # 2. Extract job skills from metadata string
        job_skills = [s.strip() for s in metadata["required_skills"].split(",") if s.strip()]
        
        # 3. Calculate keyword matching overlap analytics
        matched_skills = []
        missing_skills = []
        
        for skill in job_skills:
            if skill.lower() in student_skills_lower:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
                
        # Calculate a hybrid match percentage (Semantic weight + Skill overlap)
        overlap_ratio = len(matched_skills) / len(job_skills) if job_skills else 0
        final_score = round(((semantic_score * 0.4) + (overlap_ratio * 0.6)) * 100, 1)
        
        match_reports.append({
            "job_title": metadata["job_title"],
            "company": metadata["company"],
            "match_score": final_score,
            "strengths": matched_skills,
            "missing_skills": missing_skills,
            "description": doc_text
        })
        
    # Sort opportunities automatically from highest match percentage down to lowest
    return sorted(match_reports, key=lambda x: x["match_score"], reverse=True)

