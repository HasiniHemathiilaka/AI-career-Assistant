from backend.utils.matcher import match_resume_to_jobs

def test_matching():
    # Pass the exact list parsed from Alex's resume in Module 1
    alex_skills = ['Power Bi', 'Sql', 'Data Structures', 'Scikit-Learn', 'Machine Learning', 'Python', 'Git']
    
    print("🎯 Evaluating resume against available internship database records...")
    matches = match_resume_to_jobs(alex_skills)
    
    print("\n📋 --- Career Recommendation Matrix ---")
    for rank, report in enumerate(matches, 1):
        print(f"\nRank #{rank}: {report['job_title']} at {report['company']}")
        print(f"📊 Compatibility Score: {report['match_score']}%")
        print(f"✅ Matching Strengths: {report['strengths']}")
        print(f"❌ Missing Core Skills: {report['missing_skills']}")
        print("-" * 45)

if __name__ == "__main__":
    test_matching()