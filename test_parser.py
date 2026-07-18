from backend.utils.parser import parse_resume_sections

def test_run():
    mock_resume_text = """
    Alex Mercer
    Data Science Intern
    Email: alex@example.com
    
    Education:
    B.S. in Computer Science - University of Technology (2025)
    
    Skills:
    Python, SQL, Machine Learning, Data Structures, and Power BI.
    Experienced with Git and building interactive dashboards.
    
    Experience:
    Built an end-to-end classification model using Scikit-Learn.
    """
    
    print("⏳ Parsing mock resume text using NLP engine...")
    profile = parse_resume_sections(mock_resume_text)
    
    print("\n🚀 --- Parsed Results ---")
    print(f"👤 Name: {profile['name']}")
    print(f"🛠️ Extracted Skills: {profile['skills']}")
    print("------------------------")

if __name__ == "__main__":
    test_run()