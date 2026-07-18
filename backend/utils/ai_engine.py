import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Automatically load variables from the .env file
load_dotenv()

# Pull the token from memory
api_key_env = os.environ.get("GEMINI_API_KEY")

if not api_key_env:
    raise ValueError(
        "❌ Critical: GEMINI_API_KEY was not found! "
        "Please ensure you created a '.env' file in the root directory "
        "containing: GEMINI_API_KEY=your_actual_key"
    )

MODEL_ID = 'gemini-3.5-flash'

def generate_learning_roadmap(role_title, missing_skills):
    """
    Module 4: Generates a tailored, structured 4-week learning roadmap.
    """
    if not missing_skills:
        return "✨ You already have all the core technical skills listed for this position!"
        
    skills_str = ", ".join(missing_skills)
    prompt = f"""
    You are an expert technical career coach. A student wants to apply for the role of '{role_title}', 
    but they are missing the following critical technical skills: [{skills_str}].
    
    Generate a highly actionable, structured 4-week learning roadmap to help them bridge this gap.
    Structure the output strictly using Markdown headings for Week 1, Week 2, Week 3, and Week 4.
    Keep the explanations concise, direct, and practical.
    """
    
    try:
        # Using a context manager ensures the SDK correctly binds the client credentials
        with genai.Client(api_key=api_key_env) as client:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt
            )
            return response.text
    except Exception as e:
        return f"❌ Error connecting to Gemini API: {e}"

def generate_interview_feedback(role_title, question, student_answer):
    """
    Module 6: Evaluates a user's mock interview answer.
    """
    prompt = f"""
    Role: {role_title}
    Interview Question: {question}
    Student's Answer: {student_answer}
    
    Act as a senior technical interviewer. Evaluate the student's answer thoroughly but encouragingly.
    Provide your evaluation in the following strict format:
    
    Score: [Give a rating out of 10, e.g., 8/10]
    
    Strengths:
    - [Bullet points highlighting what they explained well]
    
    Areas to Improve:
    - [Bullet points highlighting what technical concepts or terminology they missed]
    """
    
    try:
        with genai.Client(api_key=api_key_env) as client:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt
            )
            return response.text
    except Exception as e:
        return f"❌ Error evaluating answer: {e}"