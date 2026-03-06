import os
import json
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import openai
from dotenv import load_dotenv

from database import get_db, Lead, engine, Base
from enrichment import enrich_lead
from lead_scoring import score_lead
from crm_integration import push_to_crm

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="AI Autonomous Sales Workflow Agent")

class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    company: str
    job_title: str

class CRMPushRequest(BaseModel):
    lead_id: int

def generate_outreach_email(lead: Lead) -> dict:
    """Generate a personalized email using OpenAI, or a fallback if no key is set."""
    if not openai.api_key or openai.api_key == "YOUR_OPENAI_API_KEY":
        # Fallback for local testing without an API key
        return {
            "subject": f"Enhance {lead.company}'s Workflow, {lead.name}",
            "body": f"Hi {lead.name},\\n\\nI noticed you are the {lead.job_title} at {lead.company}. "
                    f"Given that your focus is in {lead.industry}, I wanted to share how our AI workflows can boost your productivity.\\n\\n"
                    f"Let's chat next week!\\n\\nBest,\\nAI Workflow Agent"
        }
    
    try:
        prompt = f"""
        You are an expert sales workflow agent. Write a personalized cold outreach email.
        Lead Name: {lead.name}
        Job Title: {lead.job_title}
        Company: {lead.company}
        Industry: {lead.industry}
        Company Size: {lead.company_size}
        
        Keep it concise, professional, and focus on selling AI automation services.
        Return ONLY a JSON object with 'subject' and 'body' keys.
        """
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"Error generating email: {e}")
        return {"subject": "Automate your workflows today", "body": f"Hi {lead.name}, let's talk about automation."}

@app.post("/api/leads")
def process_lead(lead_in: LeadCreate, db: Session = Depends(get_db)):
    # 1. Check if exists
    db_lead = db.query(Lead).filter(Lead.email == lead_in.email).first()
    if db_lead:
        raise HTTPException(status_code=400, detail="Lead already exists")
    
    # Save initial lead
    new_lead = Lead(
        name=lead_in.name,
        email=lead_in.email,
        company=lead_in.company,
        job_title=lead_in.job_title,
        status="captured"
    )
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    # 2. Enrich Lead
    enriched_data = enrich_lead({"company": new_lead.company})
    new_lead.industry = enriched_data["industry"]
    new_lead.company_size = enriched_data["company_size"]
    new_lead.estimated_revenue = enriched_data["estimated_revenue"]
    new_lead.status = "enriched"
    
    # 3. AI Lead Scoring
    scoring_data = {
        "company_size": new_lead.company_size,
        "industry": new_lead.industry,
        "job_title": new_lead.job_title
    }
    score_result = score_lead(scoring_data)
    new_lead.lead_score = score_result["lead_score"]
    new_lead.lead_category = score_result["lead_category"]
    new_lead.status = "scored"
    db.commit()

    # 4. Generate Email
    email_content = generate_outreach_email(new_lead)
    new_lead.email_subject = email_content.get("subject")
    new_lead.email_body = email_content.get("body")
    new_lead.status = "email_generated"
    db.commit()

    # Return structured payload for n8n
    return {
        "status": "success",
        "lead_id": new_lead.id,
        "score": new_lead.lead_score,
        "category": new_lead.lead_category,
        "email_subject": new_lead.email_subject,
        "email_body": new_lead.email_body
    }

@app.post("/api/crm/push")
def crm_push(request: CRMPushRequest, db: Session = Depends(get_db)):
    # Find lead
    lead_obj = db.query(Lead).filter(Lead.id == request.lead_id).first()
    if not lead_obj:
        raise HTTPException(status_code=404, detail="Lead not found")
        
    success = push_to_crm({"name": lead_obj.name, "email": lead_obj.email})
    if success:
        lead_obj.status = "crm_pushed"
        db.commit()
        return {"status": "success", "message": "Pushed to CRM"}
    
    return {"status": "error", "message": "Failed to push to CRM"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
