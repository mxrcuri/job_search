import json
import os

# Path to the JSON file relative to this file
SOURCES_FILE = os.path.join(os.path.dirname(__file__), "company_ats_filtered.json")

def get_job_sources():
    """
    Load sources from the company_ats_filtered.json file.
    Returns a list of dicts: [{"company": "...", "ats": "...", "url": "..."}]
    """
    if not os.path.exists(SOURCES_FILE):
        return []
    
    with open(SOURCES_FILE, "r") as f:
        data = json.load(f)
    
    sources = []
    for company, info in data.items():
        sources.append({
            "company": company,
            "ats": info.get("ats"),
            "url": info.get("url")
        })
    
    return sources
