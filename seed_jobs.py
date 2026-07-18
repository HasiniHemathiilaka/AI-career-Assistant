from backend.utils.vector_store import add_job_description

def seed():
    print("🌾 Seeding vector database with sample internship opportunities...")
    
    jobs = [
        {
            "id": 1,
            "title": "Data Science Intern",
            "company": "TechCorp Solutions",
            "description": "Looking for a Data Science Intern eager to work with large datasets. You will build predictive models, run SQL queries to retrieve unstructured data, and visualize patterns using Power BI. Heavy use of Python and Scikit-Learn expected.",
            "skills": ["Python", "SQL", "Machine Learning", "Scikit-Learn", "Power BI"]
        },
        {
            "id": 2,
            "title": "Backend Engineering Intern",
            "company": "CloudScale Apps",
            "description": "Join our infrastructure engineering team. Responsibilities include building robust internal REST APIs using Python, optimizing relational database schemas via SQL, managing git workflows, and containerizing application clusters via Docker.",
            "skills": ["Python", "SQL", "Git", "Docker", "Java"]
        },
        {
            "id": 3,
            "title": "Frontend Developer Intern",
            "company": "Designify Studio",
            "description": "Seeking an enthusiastic frontend intern to construct interactive user interfaces. Perfect knowledge of HTML, CSS, JavaScript, and framework libraries like React or Vue is required. Experience with Git is mandatory.",
            "skills": ["Html", "Css", "JavaScript", "React", "Git"]
        }
    ]
    
    for job in jobs:
        add_job_description(
            job_id=job["id"],
            job_title=job["title"],
            company=job["company"],
            description_text=job["description"],
            required_skills=job["skills"]
        )
        
    print("🎉 Ingestion complete! Data is safely stored inside 'data/chroma_db/'.")

if __name__ == "__main__":
    seed()