import random

def enrich_lead(lead_data: dict) -> dict:
    """
    Simulated lead enrichment module.
    In a real scenario, this would call Clearbit, Apollo, or LinkedIn APIs.
    """
    industry_options = ["Technology", "Healthcare", "Finance", "Retail", "Manufacturing", "SaaS"]
    size_options = ["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"]
    revenue_options = ["<$1M", "$1M-$10M", "$10M-$50M", "$50M-$100M", ">$100M"]

    # Mock enrichment based on company name length just for consistency in testing
    seed = len(lead_data.get("company", "A"))
    random.seed(seed)
    
    enriched_data = {
        "industry": random.choice(industry_options),
        "company_size": random.choice(size_options),
        "estimated_revenue": random.choice(revenue_options)
    }
    return enriched_data
