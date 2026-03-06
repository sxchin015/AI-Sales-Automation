def score_lead(lead_data: dict) -> dict:
    """
    Simulated AI lead scoring module.
    Returns a score from 0-100 and a category (Hot, Warm, Cold).
    """
    score = 0
    
    # Weights for company size
    size_weights = {
        "1000+": 30,
        "501-1000": 25,
        "201-500": 20,
        "51-200": 15,
        "11-50": 10,
        "1-10": 5
    }
    
    # Weights for industry
    industry_weights = {
        "Technology": 35,
        "SaaS": 35,
        "Finance": 30,
        "Healthcare": 25,
        "Manufacturing": 15,
        "Retail": 15
    }
    
    # Weights for job title (simple keyword matching)
    title = str(lead_data.get("job_title", "")).lower()
    title_weight = 10
    if any(role in title for role in ["ceo", "cto", "cio", "founder", "vp", "chief", "director", "head"]):
        title_weight = 35
    elif any(role in title for role in ["manager", "lead", "supervisor"]):
        title_weight = 20
        
    # Calculate score
    company_size = lead_data.get("company_size", "")
    industry = lead_data.get("industry", "")
    
    score += size_weights.get(company_size, 10)
    score += industry_weights.get(industry, 10)
    score += title_weight
    
    # Cap score at 100
    score = min(score, 100)
    
    # Categorize
    if score >= 80:
        category = "Hot"
    elif score >= 50:
        category = "Warm"
    else:
        category = "Cold"
        
    return {
        "lead_score": score,
        "lead_category": category
    }
