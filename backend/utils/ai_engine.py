import os
import google.generativeai as genai
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

# Configure the SDK with your key (works perfectly with AQ. prefixes)
genai.configure(api_key=api_key_env)

# Using the robust gemini-1.5-flash model
MODEL_NAME = 'gemini-1.5-flash'

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
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
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
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error evaluating answer: {e}"

def generate_cover_letter(role_title, company, job_description, candidate_name, candidate_skills):
    """
    Module 7: Generates a professional, personalized cover letter based on 
    the user's resume profile and job specifications.
    """
    skills_str = ", ".join(candidate_skills) if candidate_skills else "software engineering concepts"
    
    prompt = f"""
    You are a professional career coach and expert resume writer.
    Write a highly tailored, persuasive, and professional cover letter for an applicant named {candidate_name}.
    
    Target Role: {role_title}
    Target Company: {company}
    Job Description: {job_description}
    Candidate Key Skills: {skills_str}
    
    Requirements:
    - Keep it under 350 words and structure it with 3-4 clear paragraphs (Hook/Opening, Value Match, Closing).
    - Highlight how the candidate's skills align directly with the job requirements.
    - Sound authentic, confident, and professional without using overly clunky AI buzzwords (like 'delve' or 'tapestry').
    - Include formal placeholders like [Date] or [City, State] where necessary.
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"❌ Error generating cover letter: {e}"