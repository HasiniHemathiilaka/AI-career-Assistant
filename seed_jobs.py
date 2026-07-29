import sys
from pathlib import Path

# Ensure root folder path is available to imports
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from backend.utils.vector_store import add_jobs_to_vector_store

def seed_database():
    """
    Populates ChromaDB with mock job roles and required skills using backend.utils.vector_store.
    """
    print("🌱 Initializing ChromaDB vector store...")
    
    # Mock Job Postings matching vector_store requirements
    jobs = [
        {
            "id": "job_1",
            "title": "Backend Engineering Intern",
            "company": "TechCorp Solutions",
            "description": "Looking for a backend intern proficient in Python, SQL, REST APIs, and Docker to build scalable microservices.",
            "requirements": ["Python", "SQL", "REST APIs", "Docker", "PostgreSQL", "Git"]
        },
        {
            "id": "job_2",
            "title": "Machine Learning Engineer Intern",
            "company": "DataMind AI",
            "description": "Seeking an ML intern to assist in training Deep Learning models, working with PyTorch, Scikit-Learn, and dataset preparation.",
            "requirements": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "Scikit-Learn", "Computer Vision"]
        },
        {
            "id": "job_3",
            "title": "Full Stack Web Developer",
            "company": "NextGen Web",
            "description": "Building interactive web platforms using React, Node.js, HTML/CSS, and MongoDB with CI/CD deployment pipelines.",
            "requirements": ["React", "Node.Js", "Javascript", "Html", "Css", "MongoDB", "Ci/Cd", "Github"]
        },
        {
            "id": "job_4",
            "title": "Cloud & DevOps Intern",
            "company": "CloudScale Systems",
            "description": "Work on AWS infrastructure, Kubernetes orchestration, Docker containers, and automated CI/CD workflows.",
            "requirements": ["Aws", "Azure", "Docker", "Kubernetes", "Ci/Cd", "Linux", "Bash"]
        }
    ]
    
    # Add jobs using the existing vector store utility
    add_jobs_to_vector_store(jobs)
    print("✅ Successfully seeded job database!")

if __name__ == "__main__":
    seed_database()