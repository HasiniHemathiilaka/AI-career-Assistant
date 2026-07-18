import spacy
from spacy.matcher import PhraseMatcher

# Load the lightweight English NLP model
nlp = spacy.load("en_core_web_sm")

# Baseline tech skill dictionary. Feel free to expand this list later!
SKILL_DB = [
    "python", "java", "c++", "javascript", "typescript", "sql", "nosql",
    "html", "css", "react", "angular", "vue", "node.js", "django", "flask",
    "fastapi", "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "power bi",
    "tableau", "aws", "azure", "gcp", "docker", "kubernetes", "git", "github",
    "ci/cd", "agile", "scrum", "data structures", "algorithms", "excel"
]

def extract_skills(text):
    """
    Uses spaCy PhraseMatcher to reliably extract matching tech skills.
    """
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
    # Convert our skill strings into spaCy document match patterns
    patterns = [nlp.make_doc(skill) for skill in SKILL_DB]
    matcher.add("TechSkills", patterns)
    
    doc = nlp(text)
    matches = matcher(doc)
    
    extracted = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        extracted.add(span.text.strip().title()) # Title case looks cleaner in dashboards
        
    return list(extracted)

def parse_resume_sections(text):
    """
    Isolates key structural elements from raw text using localized rules.
    """
    skills = extract_skills(text)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    name = "Unknown Candidate"
    if lines:
        # A common heuristic: the first clean text line of a resume is the name
        if len(lines[0].split()) <= 4:
            name = lines[0]
            
    return {
        "name": name,
        "skills": skills,
        "raw_text": text
    }