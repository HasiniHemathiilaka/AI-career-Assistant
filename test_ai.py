import os
from backend.utils.ai_engine import generate_learning_roadmap

def test_ai():
    print("🤖 Checking Gemini API connection...")
    
    # Quick sanity check for the token variable
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ Critical: GEMINI_API_KEY is not set in your terminal environment!")
        print("Please run: $env:GEMINI_API_KEY='your_key'")
        return
        
    role = "Backend Engineering Intern"
    missing = ["Docker", "Java"]
    
    print(f"⏳ Asking Gemini to draft a roadmap for missing skills: {missing}...")
    roadmap = generate_learning_roadmap(role, missing)
    
    print("\n🗺️ --- Generated Learning Path ---")
    print(roadmap)
    print("---------------------------------")

if __name__ == "__main__":
    test_ai()