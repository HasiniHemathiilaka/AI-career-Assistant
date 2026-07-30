import streamlit as st
import os
from pathlib import Path

# Fix path scoping so frontend can seamlessly import backend utilities
import sys
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from backend.utils.extractor import extract_text_from_pdf
from backend.utils.parser import parse_resume_sections
from backend.utils.matcher import match_resume_to_jobs
from backend.utils.ai_engine import (
    generate_learning_roadmap, 
    generate_interview_feedback,
    generate_cover_letter,
    generate_portfolio_project_ideas,
    generate_project_readme_starter
)

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Career Assistant | Enterprise Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- BALANCED HIGH-CONTRAST STYLING & TOP HEADER REMOVAL ---
st.markdown("""
    <style>
    /* HIDE DEFAULT STREAMLIT TOP WHITE BAR & FIX PADDING */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        display: none !important;
    }

    .block-container {
        padding-top: 1.5rem !important;
    }

    /* Global Background & Default White Typography */
    .stApp {
        background-color: #0F172A;
        color: #FFFFFF !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Primary Text Elements - Crisp White */
    p, span, label, div, .stMarkdown {
        color: #FFFFFF !important;
    }

    /* Brand Header */
    .brand-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 12px;
        border-bottom: 1px solid #334155;
        margin-bottom: 25px;
    }
    .brand-logo {
        font-size: 1.6rem;
        font-weight: 800;
        color: #00FF88;
        letter-spacing: -0.5px;
    }
    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.8px;
        margin-bottom: 8px;
    }
    .subtitle {
        font-size: 1.15rem;
        color: #E2E8F0 !important;
        margin-bottom: 30px;
        max-width: 850px;
        line-height: 1.5;
        font-weight: 400;
    }

    /* Hero & Container Cards */
    .hero-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-left: 4px solid #00FF88;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 1px solid #334155;
    }

    /* 1. File Uploader Container in Sidebar */
    [data-testid="stFileUploader"] section {
        background-color: #334155 !important;
        border: 1px dashed #64748B !important;
    }

    [data-testid="stFileUploaderFileName"], 
    [data-testid="stFileUploaderFileData"],
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] div,
    [data-testid="stFileUploaderFile"] * {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* 2. Terminal Code Blocks */
    .stCodeBlock, [data-testid="stCodeBlock"], code {
        background-color: #1E293B !important;
        border: 1px solid #475569 !important;
    }
    
    .stCodeBlock code, [data-testid="stCodeBlock"] *, code span {
        color: #00FF88 !important;
        font-weight: 700 !important;
    }

    /* 3. Typing Inputs (Text Area & Text Input) */
    .stTextArea textarea, .stTextInput input {
        background-color: #334155 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: 1px solid #64748B !important;
        border-radius: 8px !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #00FF88 !important;
    }

    /* 4. Closed Selectbox Container and Selected Role Text */
    div[data-baseweb="select"] > div {
        background-color: #E2E8F0 !important;
        border: 1px solid #94A3B8 !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] span, 
    div[data-baseweb="select"] div,
    [data-testid="stSelectbox"] div[data-baseweb="select"] *,
    [data-testid="stSelectbox"] span {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }

    div[data-baseweb="select"] svg {
        fill: #0F172A !important;
    }

    /* 5. Expanded Dropdown Options Menu Popover */
    [data-baseweb="popover"], 
    [data-baseweb="menu"],
    ul[role="listbox"],
    li[role="option"],
    div[role="listbox"] {
        background-color: #1E293B !important;
    }

    ul[role="listbox"] li,
    ul[role="listbox"] li span,
    ul[role="listbox"] li div,
    [role="option"] *,
    [data-baseweb="menu"] * {
        color: #FFFFFF !important;
        background-color: #334155 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* Option Hover State */
    ul[role="listbox"] li:hover,
    [role="option"]:hover,
    ul[role="listbox"] li:hover * {
        background-color: #00FF88 !important;
        color: #0F172A !important;
    }

    /* Primary Action Buttons */
    .stButton>button {
        background-color: #00FF88 !important;
        color: #0F172A !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 22px !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background-color: #00E575 !important;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.4) !important;
        transform: translateY(-1px);
    }

    /* Download Buttons */
    .stDownloadButton>button {
        background-color: transparent !important;
        color: #00FF88 !important;
        border: 1px solid #00FF88 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }
    .stDownloadButton>button:hover {
        background-color: rgba(0, 255, 136, 0.1) !important;
        color: #FFFFFF !important;
    }

    /* Navigation Tabs */
    div[data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #0B0F19;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 25px;
    }

    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #FFFFFF !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.2s ease-in-out !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #00FF88 !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #1E293B !important;
        color: #00FF88 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        border: 1px solid #00FF88 !important;
    }

    div[data-baseweb="tab-highlight"] {
        display: none !important;
    }

    /* Expandable Cards Header */
    .streamlit-expanderHeader {
        background-color: #1E293B !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- PROFESSIONAL BRAND HEADER ---
st.markdown("""
    <div class="brand-header">
        <div class="brand-logo">AI Career Assistant</div>
        <div style="color:#00FF88; font-size:0.95rem; font-weight:600;">RAG Engine | Powered by Gemini & ChromaDB</div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Accelerate Your Engineering Career</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your resume to evaluate compatibility with active target roles, bridge skill gaps, build portfolio projects, and practice interactive mock interviews.</div>', unsafe_allow_html=True)

# --- SIDEBAR: RESUME CONFIGURATION PANEL ---
with st.sidebar:
    st.markdown("<h3 style='color:#FFFFFF;'>Candidate Portal</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    
    st.markdown("---")
    st.markdown("<span style='color:#00FF88; font-weight:600;'>System Note:</span> Seed your database first by running:", unsafe_allow_html=True)
    st.code("python seed_jobs.py", language="bash")

# --- APP ROUTING & CORE ENGINE STATE MANAGEMENT ---
if uploaded_file is not None:
    # Caching extraction execution
    @st.cache_data
    def process_resume(file):
        raw_text = extract_text_from_pdf(file)
        return parse_resume_sections(raw_text)
        
    with st.spinner("Analyzing resume semantics..."):
        profile = process_resume(uploaded_file)
        
    # --- DASHBOARD NAVIGATION TABS ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "Compatibility Matrix", 
        "Skill Gap Roadmap", 
        "Portfolio Projects", 
        "AI Interview Coach"
    ])
    
    with tab1:
        st.markdown(f"""
            <div class="hero-card">
                <h3 style="margin:0; color:#FFFFFF;">Welcome, {profile['name']}</h3>
                <p style="margin:5px 0 0 0; color:#FFFFFF;"><b>Extracted Skills:</b> {', '.join(profile['skills']) if profile['skills'] else 'None detected.'}</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("Calculating vector similarity scores..."):
            matches = match_resume_to_jobs(profile['skills'])
            
        if not matches:
            st.warning("No jobs indexed yet. Run python seed_jobs.py in your terminal to seed mock roles.")
        else:
            for i, match in enumerate(matches):
                with st.expander(f"{match['job_title']} — {match['company']}  [ Compatibility: {match['match_score']}% ]"):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.metric(label="Match Ratio", value=f"{match['match_score']}%")
                    with col2:
                        st.write(f"**Role Summary:** {match['description']}")
                    
                    st.markdown("---")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.success(f"**Matching Strengths:** {', '.join(match['strengths']) if match['strengths'] else 'None'}")
                    with c2:
                        st.error(f"**Missing Skills:** {', '.join(match['missing_skills']) if match['missing_skills'] else 'None'}")
                    
                    # --- COVER LETTER GENERATOR ---
                    st.markdown("---")
                    st.subheader("Automated Cover Letter Generator")
                    
                    if st.button("Generate Tailored Cover Letter", key=f"cover_btn_{i}_{match['company']}"):
                        with st.spinner("Drafting custom cover letter..."):
                            cover_letter_text = generate_cover_letter(
                                role_title=match['job_title'],
                                company=match['company'],
                                job_description=match['description'],
                                candidate_name=profile['name'],
                                candidate_skills=profile['skills']
                            )
                            
                            st.text_area(
                                label="Generated Cover Letter:",
                                value=cover_letter_text,
                                height=280,
                                key=f"text_area_{i}"
                            )
                            
                            st.download_button(
                                label="Download Cover Letter (.txt)",
                                data=cover_letter_text,
                                file_name=f"Cover_Letter_{match['company']}.txt",
                                mime="text/plain",
                                key=f"download_{i}"
                            )
                        
    with tab2:
        st.subheader("Strategic Skill Gap Bridging Curriculum")
        
        if not matches:
            st.warning("Populate your vector store first to analyze skill gaps.")
        else:
            job_options = [f"{m['job_title']} ({m['company']})" for m in matches]
            selected_job = st.selectbox(
                "Select a target role to analyze your path for:",
                options=job_options
            )
            
            idx = job_options.index(selected_job)
            target_match = matches[idx]
            
            if st.button("Generate Tailored Learning Path", key="roadmap_btn"):
                with st.spinner("Drafting custom learning syllabus..."):
                    roadmap = generate_learning_roadmap(target_match['job_title'], target_match['missing_skills'])
                    st.markdown(roadmap)

    with tab3:
        st.subheader("Portfolio Project Recommender & Repository Starter")
        st.write("Turn your missing technical skills into high-impact portfolio projects.")
        
        if not matches:
            st.warning("Populate your vector store first to generate portfolio concepts.")
        else:
            job_options_proj = [f"{m['job_title']} ({m['company']})" for m in matches]
            selected_proj_job = st.selectbox(
                "Select a target role to generate tailored projects for:",
                options=job_options_proj,
                key="proj_job_select"
            )
            
            proj_idx = job_options_proj.index(selected_proj_job)
            proj_target_match = matches[proj_idx]
            
            st.markdown("---")
            st.markdown("### 1. Tailored Portfolio Project Concepts")
            
            if st.button("Brainstorm Project Ideas", key="ideas_btn"):
                with st.spinner("AI generating custom project concepts..."):
                    ideas = generate_portfolio_project_ideas(
                        role_title=proj_target_match['job_title'],
                        strengths=proj_target_match['strengths'],
                        missing_skills=proj_target_match['missing_skills']
                    )
                    st.markdown(ideas)
            
            st.markdown("---")
            st.markdown("### 2. GitHub README.md Starter Generator")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                proj_name = st.text_input("Project Name", placeholder="e.g., Microservice-Docker-Pipeline")
                proj_stack = st.text_input("Tech Stack", placeholder="e.g., Python, Docker, FastAPI, PostgreSQL")
            
            with col2:
                st.write("") 
                st.write("")
                generate_readme_btn = st.button("Generate README.md Template", key="readme_btn")
            
            if generate_readme_btn:
                if proj_name.strip() and proj_stack.strip():
                    with st.spinner("Drafting repository README.md template..."):
                        readme_content = generate_project_readme_starter(
                            project_name=proj_name,
                            role_title=proj_target_match['job_title'],
                            tech_stack=proj_stack
                        )
                        st.code(readme_content, language="markdown")
                        
                        st.download_button(
                            label="Download README.md File",
                            data=readme_content,
                            file_name="README.md",
                            mime="text/markdown",
                            key="download_readme"
                        )
                else:
                    st.warning("Please enter both a Project Name and Tech Stack before generating.")

    with tab4:
        st.subheader("Live Interactive Mock Interview Session")
        
        if not matches:
            st.warning("Populate your vector store first to practice mock interviews.")
        else:
            selected_int_job = st.selectbox(
                "Select target role for interview training:",
                options=[m['job_title'] for m in matches],
                key="interview_job_select"
            )
            
            mock_question = "Explain how you would handle an imbalanced dataset when building a machine learning model."
            if "backend" in selected_int_job.lower():
                mock_question = "What is the difference between an Inner Join and a Left Join in SQL, and how do indexes affect query speed?"
                
            st.info(f"**Interviewer Question:** {mock_question}")
            
            student_ans = st.text_area("Type your technical answer here:", height=150)
            
            if st.button("Submit Answer for AI Evaluation"):
                if not student_ans.strip():
                    st.warning("Please type an answer before submitting.")
                else:
                    with st.spinner("Senior Engineer reviewing response structures..."):
                        feedback = generate_interview_feedback(selected_int_job, mock_question, student_ans)
                        st.markdown("### AI Interviewer Evaluation")
                        st.markdown(feedback)
else:
    st.info("Upload your candidate resume PDF in the sidebar panel to launch the career assistant.")