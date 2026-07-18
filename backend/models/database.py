import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# 1. Dynamically calculate the absolute path to your project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_DIR = os.path.join(BASE_DIR, 'data')

# 2. Force Windows to physically create the data folder if it doesn't exist yet
os.makedirs(DATABASE_DIR, exist_ok=True)

# 3. Formulate the concrete absolute database URL path
DATABASE_URL = f"sqlite:///{os.path.join(DATABASE_DIR, 'career_assistant.db')}"

Engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
Base = declarative_base()

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    target_role = Column(String, nullable=True)
    raw_resume_text = Column(Text, nullable=False)
    extracted_skills = Column(Text, nullable=True)  # Stored as comma-separated string
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to track match history logs over time
    matches = relationship("MatchHistory", back_populates="profile")

class MatchHistory(Base):
    __tablename__ = "match_history"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    match_score = Column(Float, nullable=False)      
    missing_skills = Column(Text, nullable=True)     
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("StudentProfile", back_populates="matches")

# Helper function to initialize the database tables
def init_db():
    Base.metadata.create_all(bind=Engine)

# Dependency to get db session utility
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()