import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Use SQLite for local development without Docker/Postgres
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sales_agent.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    company = Column(String, index=True)
    job_title = Column(String)
    
    # Enriched data
    industry = Column(String, nullable=True)
    company_size = Column(String, nullable=True)
    estimated_revenue = Column(String, nullable=True)
    
    # AI Scoring
    lead_score = Column(Float, nullable=True)
    lead_category = Column(String, nullable=True) # Hot, Warm, Cold
    
    # AI Email
    email_subject = Column(String, nullable=True)
    email_body = Column(Text, nullable=True)
    
    # Status tracking
    status = Column(String, default="captured")
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)
