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
from backend.utils.ai_engine import generate_learning_roadmap, generate_interview_feedback

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Internship & Career Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING & CUSTOM ATTRACTIVE INTERFACE ACCENTS ---
st.markdown("""
    <style>
    .main-title { font-size: 2.6rem; font-weight: 700; color: #1E3A8A; margin-bottom: 5px; }
    .subtitle { font-size: 1.1rem; color: #4B5563; margin-bottom: 25px; }
    .metric-card { background-color: #F3F4F6; padding: 15px; border-radius: 10px; border-left: 5px solid #2563EB; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 AI Internship & Career Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your resume, analyze compatibility with active roles, bridge skill gaps, and practice mock interviews.</div>', unsafe_allow_html=True)

# --- SIDEBAR: RESUME CONFIGURATION PANEL ---
with st.sidebar:
    st.header("📄 Candidate Profile")
    uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
    
    st.markdown("---")
    st.markdown("💡 **Tip:** Pre-populate the system with job roles by running `seed_jobs.py` first!")

# --- APP ROUTING & CORE ENGINE STATE MANAGEMENT ---
if uploaded_file is not None:
    # 1. Cache text extraction execution to prevent processing spikes
    @st.cache_data
    def process_resume(file):
        raw_text = extract_text_from_pdf(file)
        return parse_resume_sections(raw_text)
        
    with st.spinner("🧠 NLP Engine parsing resume data structure..."):
        profile = process_resume(uploaded_file)
        
    # --- DASHBOARD LAYOUT & ENGINE PRESENTATION TABS ---
    tab1, tab2, tab3 = st.tabs(["🎯 Job Matching Matrix", "🗺️ Skill Gap Roadmap", "🤖 AI Interview Coach"])
    
    with tab1:
        st.subheader(f"Welcome, {profile['name']}!")
        st.write(f"**Identified Core Skills:** {', '.join(profile['skills'] if profile['skills'] else ['None found. Use dictionary validation.'])}")
        
        with st.spinner("🎯 Evaluating vector similarity matching scores..."):
            matches = match_resume_to_jobs(profile['skills'])
            
        if not matches:
            st.warning("No job records indexed yet. Please populate your vector store!")
        else:
            for i, match in enumerate(matches):
                # Unique display layout using expandable cards
                with st.expander(f"💼 {match['job_title']} at {match['company']} — **Match Score: {match['match_score']}%**"):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.metric(label="Compatibility Ratio", value=f"{match['match_score']}%")
                    with col2:
                        st.write(f"**Description Summary:** {match['description']}")
                    
                    st.markdown("---")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.success(f"**✅ Your Strengths:** {', '.join(match['strengths']) if match['strengths'] else 'None'}")
                    with c2:
                        st.error(f"**❌ Missing Targets:** {', '.join(match['missing_skills']) if match['missing_skills'] else 'None'}")
                        
    with tab2:
        st.subheader("🗺️ Strategic Skill Gap Bridging Curriculum")
        selected_job = st.selectbox(
            "Select a target role to analyze your path for:",
            options=[f"{m['job_title']} ({m['company']})" for m in matches]
        )
        
        # Get the current selected index block data mapping
        idx = [f"{m['job_title']} ({m['company']})" for m in matches].index(selected_job)
        target_match = matches[idx]
        
        if st.button("🚀 Generate Tailored Learning Path", key="roadmap_btn"):
            with st.spinner("🤖 Asking Gemini to draft your custom syllabus..."):
                roadmap = generate_learning_roadmap(target_match['job_title'], target_match['missing_skills'])
                st.markdown(roadmap)
                
    with tab3:
        st.subheader("🤖 Live Interactive Mock Interview Session")
        selected_int_job = st.selectbox(
            "Select target role for interview training:",
            options=[m['job_title'] for m in matches],
            key="interview_job_select"
        )
        
        # Static mock questions mapping for robust testing framework
        mock_question = "Explain how you would handle an imbalanced dataset when building a machine learning model."
        if "backend" in selected_int_job.lower():
            mock_question = "What is the difference between an Inner Join and a Left Join in SQL, and how do indexes affect query speed?"
            
        st.info(f"**Interviewer Question:** {mock_question}")
        
        student_ans = st.text_area("Type your technical answer here:", height=150)
        
        if st.button("🎯 Submit Answer for AI Evaluation"):
            if not student_ans.strip():
                st.warning("Please type an answer before submitting!")
            else:
                with st.spinner("🧐 Senior Engineer reviewing response structures..."):
                    feedback = generate_interview_feedback(selected_int_job, mock_question, student_ans)
                    st.markdown("### 📋 AI Interviewer Evaluation")
                    st.markdown(feedback)
else:
    st.info("💡 Please upload a candidate resume PDF in the sidebar panel to launch the assistant analytics matrix.")