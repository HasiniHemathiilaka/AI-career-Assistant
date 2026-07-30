import os
import time
from google import genai
from dotenv import load_dotenv

# Force reload of environment variables from .env
load_dotenv(override=True)

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "❌ Critical: No valid Gemini API Key found! "
        "Please add GEMINI_API_KEY=AIzaSy... to your .env file."
    )

# Explicitly pass api_key to the client
client = genai.Client(api_key=api_key)

# Active Gemini model identifier (Kept as requested)
MODEL_ID =  'gemini-3.5-flash'


def call_gemini_with_retry(prompt: str, max_retries: int = 3) -> str:
    """
    Central helper to invoke Gemini with exponential backoff retry logic
    to gracefully handle temporary 503 UNAVAILABLE server spikes.
    """
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            err_msg = str(e)
            
            # Catch temporary 503 high-demand / server overload errors
            if ("503" in err_msg or "UNAVAILABLE" in err_msg) and attempt < max_retries - 1:
                # Exponential wait time: 2s, 4s, etc.
                time.sleep(2 * (attempt + 1))
                continue
            
            # Raise the final error if retries are exhausted or for non-503 errors
            raise e


def generate_learning_roadmap(role_title, missing_skills):
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
        return call_gemini_with_retry(prompt)
    except Exception as e:
        return f"❌ Error connecting to Gemini API: {e}"


def generate_interview_feedback(role_title, question, student_answer):
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
        return call_gemini_with_retry(prompt)
    except Exception as e:
        return f"❌ Error evaluating answer: {e}"


def generate_cover_letter(role_title, company, job_description, candidate_name, candidate_skills):
    skills_str = ", ".join(candidate_skills) if candidate_skills else "software engineering concepts"
    
    prompt = f"""
    You are a professional career coach and expert resume writer.
    Write a highly tailored, persuasive, and professional cover letter for an applicant named {candidate_name}.
    
    Target Role: {role_title}
    Target Company: {company}
    Job Description: {job_description}
    Candidate Key Skills: {skills_str}
    
    Requirements:
    - Keep it under 350 words and structure it with 3-4 clear paragraphs.
    - Highlight how the candidate's skills align directly with the job requirements.
    - Sound authentic, confident, and professional.
    - Include formal placeholders like [Date] or [City, State] where necessary.
    """
    
    try:
        return call_gemini_with_retry(prompt)
    except Exception as e:
        return f"❌ Error generating cover letter: {e}"


def generate_portfolio_project_ideas(role_title, strengths, missing_skills):
    """
    Generates 2-3 tailored portfolio project concepts combining current strengths 
    with missing skills.
    """
    if not missing_skills:
        return "✨ You already match all required skills! You can build advanced showcase projects for your existing stack."

    strengths_str = ", ".join(strengths) if strengths else "Software Development Basics"
    missing_str = ", ".join(missing_skills)

    prompt = f"""
    You are a principal software engineer and tech career mentor.
    Target Role: {role_title}
    Candidate Strengths: [{strengths_str}]
    Missing Skills to Master: [{missing_str}]

    Propose 2 or 3 realistic, impressive portfolio project ideas that bridge this gap.
    Each project MUST combine at least 2 of their current strengths with at least 1 of their missing skills.

    Format the output using clear Markdown headers for each project:
    ### 🚀 [Project Name]
    * **Objective**: Concise summary of what the project does.
    * **Core Stack**: Strengths used + Missing skills integrated.
    * **Key Features**: 3 bullet points.
    * **Why it Stands Out**: How it proves readiness for {role_title}.
    """

    try:
        return call_gemini_with_retry(prompt)
    except Exception as e:
        return f"❌ Error generating project ideas: {e}"


def generate_project_readme_starter(project_name, role_title, tech_stack):
    """
    Generates a production-grade README.md starter template for a recommended project.
    """
    prompt = f"""
    Generate a professional, production-ready README.md file template for a GitHub project named '{project_name}' 
    tailored for a candidate applying for a {role_title} position.
    Tech Stack: {tech_stack}

    Include the following sections strictly in Markdown syntax:
    # {project_name}
    Brief project description and value proposition.

    ## 🛠️ Architecture & Tech Stack
    Bullet points of tech components.

    ## 🚀 Features
    Key features list.

    ## ⚡ Quick Start & Installation
    Clear step-by-step terminal instructions for cloning, setup, `.env` configuration, and running locally.

    ## 📊 Folder Structure
    A clean directory tree layout.

    ## 📝 License & Contact
    Standard placeholders.
    """

    try:
        return call_gemini_with_retry(prompt)
    except Exception as e:
        return f"❌ Error generating README starter: {e}"